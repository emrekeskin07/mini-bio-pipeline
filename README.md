# 🧬 Mini Bioinformatics Pipeline

A reproducible long-read sequencing QC pipeline built with **Nextflow (DSL2)** and **Conda**.

## Project Structure

    mini-bio-pipeline/
    pipeline/main.nf        # Nextflow DSL2 pipeline
    scripts/read_stats.py   # Per-read GC, length, quality stats
    scripts/visualize.py    # Distribution plots + summary statistics
    scripts/dashboard.py    # QC summary dashboard
    environment.yml         # Conda environment
    Dockerfile              # Docker container definition
    nextflow.config         # Pipeline configuration
    example_output/         # Sample results and plots
    email_to_professor.md   # Full report for Professor Kilic

## Why These Plot Types?

| Metric | Plot Type | Reason |
|--------|-----------|--------|
| GC Content | Histogram + KDE | Shows distribution shape, easy to spot contamination |
| Read Length | Histogram linear + log | Linear shows bulk, log reveals ultra-long reads |
| Quality Score | Histogram + Violin | Histogram shows distribution, violin reveals bimodal patterns |

## Quick Start

### Option A: Conda

    git clone https://github.com/emrekeskin07/mini-bio-pipeline.git
    cd mini-bio-pipeline
    conda env create -f environment.yml
    conda activate mini-bio-pipeline
    nextflow run pipeline/main.nf -with-conda \
      --fastq data/barcode77.fastq \
      --outdir results/ \
      --scripts scripts/

### Option B: Docker

    docker build -t mini-bio-pipeline .
    docker run -v "$PWD/data:/pipeline/data" \
               -v "$PWD/results:/pipeline/results" \
               mini-bio-pipeline

## Outputs

| File | Description |
|------|-------------|
| results/read_stats.csv | Per-read statistics |
| results/nanostat_report/ | NanoStat QC summary |
| results/plots/dashboard.png | Combined QC dashboard |
| example_output/summary_stats.txt | Summary statistics |

## Key Findings (barcode77.fastq)

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Total Reads | 81011 | Good dataset size |
| Median Read Length | 547 bp | Expected for Nanopore |
| N50 | 1761 bp | Sufficient for alignment |
| Median Quality | Q17.3 | Above Q10 threshold |
| Reads above Q10 | 77.7% | Good quality rate |
| Mean GC Content | 53.0% | Normal, no contamination |

Conclusion: Data quality is sufficient to proceed with alignment using Minimap2.

## Communication

See email_to_professor.md for the full report addressed to Professor Kilic.

Summary: 81011 reads analysed. Median quality Q17.3 with 77.7% above Q10. GC content clean at 53%. Recommendation: proceed to alignment with Minimap2.

## QC Dashboard


## QC Dashboard

![QC Dashboard](example_output/plots/dashboard.png)
