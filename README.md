# 🧬 Mini Bioinformatics Pipeline

A reproducible long-read sequencing QC pipeline built with **Nextflow (DSL2)** and **Conda**.

## Project Structure
```
mini-bio-pipeline/
├── pipeline/main.nf        # Nextflow DSL2 pipeline
├── scripts/read_stats.py   # Per-read GC, length, quality stats
├── scripts/visualize.py    # Distribution plots
├── scripts/dashboard.py    # QC dashboard
├── environment.yml         # Conda environment
└── email_to_professor.md   # Communication draft
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

## Results
- `results/read_stats.csv` — Per-read statistics
- `results/nanostat_report/` — NanoStat QC report
- `results/plots/` — Distribution plots + dashboard
