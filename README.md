# 🧬 Mini Bioinformatics Pipeline

A reproducible long-read sequencing QC pipeline built with **Nextflow (DSL2)** and **Conda**.

## Project Structure
```
mini-bio-pipeline/
├── pipeline/main.nf        # Nextflow DSL2 pipeline
├── scripts/read_stats.py   # Per-read GC, length, quality stats
├── scripts/visualize.py    # Distribution plots
├── scripts/dashboard.py    # QC summary dashboard
├── environment.yml         # Conda environment
├── nextflow.config         # Pipeline configuration
├── example_output/         # Sample results and plots
└── email_to_professor.md   # Communication draft → see below
```

## Quick Start

### 1. Clone
```bash
git clone https://github.com/emrekeskin07/mini-bio-pipeline.git
cd mini-bio-pipeline
```

### 2. Create Conda environment
```bash
conda env create -f environment.yml
conda activate mini-bio-pipeline
```

### 3. Run pipeline
```bash
nextflow run pipeline/main.nf -with-conda \
  --fastq "$PWD/data/barcode77.fastq" \
  --outdir "$PWD/results" \
  --scripts "$PWD/scripts"
```

### 4. Generate dashboard (optional)
```bash
python scripts/dashboard.py \
  --input results/read_stats.csv \
  --outdir results/plots/
```

## Outputs

| File | Description |
|------|-------------|
| `results/read_stats.csv` | Per-read statistics (length, GC%, quality) |
| `results/nanostat_report/` | NanoStat QC summary |
| `results/plots/gc_content_distribution.png` | GC content histogram |
| `results/plots/read_length_distribution.png` | Read length histogram |
| `results/plots/quality_score_distribution.png` | Quality score distribution |
| `results/plots/dashboard.png` | Combined QC dashboard |

## Example Output

Sample results from `barcode77.fastq` are available in `example_output/`.

![QC Dashboard](example_output/plots/dashboard.png)

## Communication

See [`email_to_professor.md`](email_to_professor.md) for the full report addressed to Professor Kılıç.

## Key Findings (barcode77.fastq)

| Metric | Value |
|--------|-------|
| Total Reads | 81,011 |
| Median Read Length | 547 bp |
| N50 | 1,761 bp |
| Median Quality | Q17.3 |
| Reads > Q10 | 77.7% |
| Mean GC Content | 53.0% |
