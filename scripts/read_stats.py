#!/usr/bin/env python3
import argparse
import csv
import sys
from Bio import SeqIO


def calculate_gc_content(sequence):
    if len(sequence) == 0:
        return 0.0
    g_count = sequence.count("G") + sequence.count("g")
    c_count = sequence.count("C") + sequence.count("c")
    return round((g_count + c_count) / len(sequence) * 100, 4)


def calculate_mean_quality(quality_scores):
    if not quality_scores:
        return 0.0
    return round(sum(quality_scores) / len(quality_scores), 4)


def parse_fastq_and_compute_stats(input_path, output_path):
    fieldnames = ["read_id", "read_length", "gc_content_pct", "mean_quality_score"]
    total_reads = 0

    print(f"[INFO] Reading FASTQ file: {input_path}")
    print(f"[INFO] Writing stats to:   {output_path}")

    with open(output_path, "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for record in SeqIO.parse(input_path, "fastq"):
            sequence = str(record.seq)
            quality_scores = record.letter_annotations["phred_quality"]
            writer.writerow({
                "read_id": record.id,
                "read_length": len(sequence),
                "gc_content_pct": calculate_gc_content(sequence),
                "mean_quality_score": calculate_mean_quality(quality_scores),
            })
            total_reads += 1

    print(f"[INFO] Done! Processed {total_reads} reads.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        parse_fastq_and_compute_stats(args.input, args.output)
    except FileNotFoundError:
        print(f"[ERROR] Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
