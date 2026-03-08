#!/usr/bin/env python3
import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns

sns.set_theme(style="whitegrid", palette="muted", font_scale=1.0)

def calculate_n50(lengths):
    sorted_lengths = lengths.sort_values(ascending=False).values
    cumsum = 0
    total = sorted_lengths.sum()
    for length in sorted_lengths:
        cumsum += length
        if cumsum >= total / 2:
            return length
    return 0.0

def make_dashboard(df, outdir):
    fig = plt.figure(figsize=(18, 12))
    fig.suptitle("Long-Read Sequencing QC Dashboard\nbarcode77.fastq",
                 fontsize=16, fontweight="bold", y=0.98)
    gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35)

    # Panel 1: GC Content
    ax1 = fig.add_subplot(gs[0, 0])
    sns.histplot(df["gc_content_pct"], bins=50, kde=True, color="#4C8BE0", edgecolor="white", ax=ax1)
    ax1.axvline(df["gc_content_pct"].mean(), color="#E05C4C", linestyle="--", linewidth=1.5, label=f"Mean: {df['gc_content_pct'].mean():.1f}%")
    ax1.axvline(df["gc_content_pct"].median(), color="#2ECC71", linestyle=":", linewidth=1.5, label=f"Median: {df['gc_content_pct'].median():.1f}%")
    ax1.set_title("GC Content Distribution", fontweight="bold")
    ax1.set_xlabel("GC Content (%)")
    ax1.set_ylabel("Read Count")
    ax1.legend(fontsize=8)

    # Panel 2: Read Length linear (outlier temizlenmiş)
    ax2 = fig.add_subplot(gs[0, 1])
    p99 = df["read_length"].quantile(0.99)
    df_clipped = df[df["read_length"] <= p99]
    n50 = calculate_n50(df["read_length"])
    sns.histplot(df_clipped["read_length"], bins=60, kde=True, color="#9B59B6", edgecolor="white", ax=ax2)
    ax2.axvline(df["read_length"].mean(), color="#E05C4C", linestyle="--", linewidth=1.5, label=f"Mean: {df['read_length'].mean():,.0f}")
    ax2.axvline(df["read_length"].median(), color="#2ECC71", linestyle=":", linewidth=1.5, label=f"Median: {df['read_length'].median():,.0f}")
    ax2.axvline(n50, color="#F39C12", linestyle="-.", linewidth=1.5, label=f"N50: {n50:,.0f}")
    ax2.set_title("Read Length (Linear, 99th pct)", fontweight="bold")
    ax2.set_xlabel("Read Length (bp)")
    ax2.set_ylabel("Read Count")
    ax2.legend(fontsize=8)

    # Panel 3: Read Length log
    ax3 = fig.add_subplot(gs[0, 2])
    sns.histplot(df["read_length"], bins=60, kde=False, color="#9B59B6", edgecolor="white", ax=ax3, log_scale=(True, False))
    ax3.set_title("Read Length (Log Scale)", fontweight="bold")
    ax3.set_xlabel("Read Length (bp) — log")
    ax3.set_ylabel("Read Count")

    # Panel 4: Quality Histogram
    ax4 = fig.add_subplot(gs[1, 0])
    sns.histplot(df["mean_quality_score"], bins=50, kde=True, color="#27AE60", edgecolor="white", ax=ax4)
    ax4.axvline(df["mean_quality_score"].mean(), color="#E05C4C", linestyle="--", linewidth=1.5, label=f"Mean: {df['mean_quality_score'].mean():.1f}")
    ax4.axvline(df["mean_quality_score"].median(), color="#2ECC71", linestyle=":", linewidth=1.5, label=f"Median: {df['mean_quality_score'].median():.1f}")
    ax4.axvline(10, color="#E74C3C", linestyle="-", linewidth=1.2, alpha=0.5, label="Q10")
    ax4.set_title("Quality Score Distribution", fontweight="bold")
    ax4.set_xlabel("Mean Phred Quality Score")
    ax4.set_ylabel("Read Count")
    ax4.legend(fontsize=8)

    # Panel 5: Quality Violin
    ax5 = fig.add_subplot(gs[1, 1])
    sns.violinplot(y=df["mean_quality_score"], color="#27AE60", inner="box", ax=ax5)
    ax5.axhline(10, color="#E74C3C", linestyle="-", linewidth=1.2, alpha=0.6, label="Q10")
    ax5.set_title("Quality Score Violin", fontweight="bold")
    ax5.set_ylabel("Mean Phred Quality Score")
    ax5.legend(fontsize=8)

    # Panel 6: Summary Table
    ax6 = fig.add_subplot(gs[1, 2])
    ax6.axis("off")
    table_data = [
        ["Metric", "Value"],
        ["Total Reads", f"{len(df):,}"],
        ["Mean Read Length", f"{df['read_length'].mean():,.0f} bp"],
        ["Median Read Length", f"{df['read_length'].median():,.0f} bp"],
        ["N50", f"{n50:,.0f} bp"],
        ["Mean Quality", f"Q{df['mean_quality_score'].mean():.1f}"],
        ["Median Quality", f"Q{df['mean_quality_score'].median():.1f}"],
        ["Mean GC Content", f"{df['gc_content_pct'].mean():.1f}%"],
        ["Reads > Q10", f"{(df['mean_quality_score'] > 10).sum():,} ({(df['mean_quality_score'] > 10).mean()*100:.1f}%)"],
    ]
    table = ax6.table(cellText=table_data[1:], colLabels=table_data[0],
                      cellLoc="center", loc="center", bbox=[0, 0, 1, 1])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_facecolor("#2C3E50")
            cell.set_text_props(color="white", fontweight="bold")
        elif row % 2 == 0:
            cell.set_facecolor("#ECF0F1")
        cell.set_edgecolor("#BDC3C7")
    ax6.set_title("Summary Statistics", fontweight="bold", pad=12)

    out_path = os.path.join(outdir, "dashboard.png")
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[INFO] Dashboard saved → {out_path}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--outdir", required=True)
    args = parser.parse_args()
    os.makedirs(args.outdir, exist_ok=True)
    df = pd.read_csv(args.input)
    make_dashboard(df, args.outdir)

if __name__ == "__main__":
    main()
