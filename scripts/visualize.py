#!/usr/bin/env python3
import argparse
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns


sns.set_theme(style="whitegrid", palette="muted", font_scale=1.15)
PLOT_DPI = 150
FIGURE_SIZE = (9, 5)


def load_data(csv_path):
    required_cols = {"read_length", "gc_content_pct", "mean_quality_score"}
    df = pd.read_csv(csv_path)
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in CSV: {missing}")
    print(f"[INFO] Loaded {len(df):,} reads from {csv_path}")
    return df


def calculate_n50(lengths):
    sorted_lengths = lengths.sort_values(ascending=False).values
    total = sorted_lengths.sum()
    cumsum = 0
    for length in sorted_lengths:
        cumsum += length
        if cumsum >= total / 2:
            return length
    return 0.0


def print_summary_statistics(df):
    metrics = {
        "Read Length (bp)":       "read_length",
        "GC Content (%)":         "gc_content_pct",
        "Mean Quality Score (Q)": "mean_quality_score",
    }
    print("\n" + "=" * 55)
    print("        SUMMARY STATISTICS")
    print("=" * 55)
    for label, col in metrics.items():
        s = df[col]
        print(f"\n  {label}")
        print(f"    Mean   : {s.mean():.2f}")
        print(f"    Median : {s.median():.2f}")
        print(f"    Std    : {s.std():.2f}")
        print(f"    Min    : {s.min():.2f}")
        print(f"    Max    : {s.max():.2f}")
        if col == "read_length":
            print(f"    N50    : {calculate_n50(df['read_length']):.0f}")
    print("=" * 55 + "\n")


def plot_gc_content(df, outdir):
    fig, ax = plt.subplots(figsize=FIGURE_SIZE)
    sns.histplot(df["gc_content_pct"], bins=50, kde=True, color="#4C8BE0", edgecolor="white", ax=ax)
    ax.axvline(df["gc_content_pct"].mean(),   color="#E05C4C", linestyle="--", linewidth=1.5, label=f"Mean: {df['gc_content_pct'].mean():.1f}%")
    ax.axvline(df["gc_content_pct"].median(), color="#4CE05C", linestyle=":",  linewidth=1.5, label=f"Median: {df['gc_content_pct'].median():.1f}%")
    ax.set_title("GC Content Distribution", fontweight="bold")
    ax.set_xlabel("GC Content (%)")
    ax.set_ylabel("Read Count")
    ax.legend()
    plt.tight_layout()
    out_path = os.path.join(outdir, "gc_content_distribution.png")
    plt.savefig(out_path, dpi=PLOT_DPI)
    plt.close()
    print(f"[INFO] Saved → {out_path}")


def plot_read_lengths(df, outdir):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    mean_val   = df["read_length"].mean()
    median_val = df["read_length"].median()
    n50_val    = calculate_n50(df["read_length"])
    for ax in axes:
        ax.axvline(mean_val,   color="#E05C4C", linestyle="--", linewidth=1.5, label=f"Mean: {mean_val:,.0f} bp")
        ax.axvline(median_val, color="#4CE05C", linestyle=":",  linewidth=1.5, label=f"Median: {median_val:,.0f} bp")
        ax.axvline(n50_val,    color="#F39C12", linestyle="-.", linewidth=1.5, label=f"N50: {n50_val:,.0f} bp")
    sns.histplot(df["read_length"], bins=60, kde=True,  color="#9B59B6", edgecolor="white", ax=axes[0])
    sns.histplot(df["read_length"], bins=60, kde=False, color="#9B59B6", edgecolor="white", ax=axes[1], log_scale=(True, False))
    axes[0].set_title("Read Length (Linear)", fontweight="bold")
    axes[1].set_title("Read Length (Log Scale)", fontweight="bold")
    for ax in axes:
        ax.set_xlabel("Read Length (bp)")
        ax.set_ylabel("Read Count")
        ax.legend(fontsize=9)
    plt.tight_layout()
    out_path = os.path.join(outdir, "read_length_distribution.png")
    plt.savefig(out_path, dpi=PLOT_DPI, bbox_inches="tight")
    plt.close()
    print(f"[INFO] Saved → {out_path}")


def plot_quality_scores(df, outdir):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.histplot(df["mean_quality_score"], bins=50, kde=True, color="#27AE60", edgecolor="white", ax=axes[0])
    axes[0].axvline(df["mean_quality_score"].mean(),   color="#E05C4C", linestyle="--", linewidth=1.5, label=f"Mean: {df['mean_quality_score'].mean():.1f}")
    axes[0].axvline(df["mean_quality_score"].median(), color="#4C8BE0", linestyle=":",  linewidth=1.5, label=f"Median: {df['mean_quality_score'].median():.1f}")
    axes[0].axvline(10, color="#E74C3C", linestyle="-", linewidth=1.2, alpha=0.5, label="Q10 threshold")
    axes[0].set_title("Quality Score — Histogram", fontweight="bold")
    axes[0].set_xlabel("Mean Phred Quality Score")
    axes[0].set_ylabel("Read Count")
    axes[0].legend()
    sns.violinplot(y=df["mean_quality_score"], color="#27AE60", inner="box", ax=axes[1])
    axes[1].axhline(10, color="#E74C3C", linestyle="-", linewidth=1.2, alpha=0.6, label="Q10 threshold")
    axes[1].set_title("Quality Score — Violin", fontweight="bold")
    axes[1].set_ylabel("Mean Phred Quality Score")
    axes[1].legend()
    plt.tight_layout()
    out_path = os.path.join(outdir, "quality_score_distribution.png")
    plt.savefig(out_path, dpi=PLOT_DPI, bbox_inches="tight")
    plt.close()
    print(f"[INFO] Saved → {out_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input",  required=True)
    parser.add_argument("--outdir", required=True)
    args = parser.parse_args()
    os.makedirs(args.outdir, exist_ok=True)
    try:
        df = load_data(args.input)
    except (FileNotFoundError, ValueError) as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
    print_summary_statistics(df)
    plot_gc_content(df, args.outdir)
    plot_read_lengths(df, args.outdir)
    plot_quality_scores(df, args.outdir)
    print("[INFO] All plots generated successfully.")


if __name__ == "__main__":
    main()
