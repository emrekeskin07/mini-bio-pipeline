#!/usr/bin/env nextflow
nextflow.enable.dsl = 2

params.fastq   = "${projectDir}/data/barcode77.fastq"
params.outdir  = "${projectDir}/results"
params.scripts = "${projectDir}/scripts"

log.info """
    ╔══════════════════════════════════════════════╗
    ║       Mini Bioinformatics Pipeline           ║
    ║       Long-Read QC & Statistics              ║
    ╚══════════════════════════════════════════════╝
    Input FASTQ  : ${params.fastq}
    Output dir   : ${params.outdir}
    """.stripIndent()

process NANOSTAT_QC {
    tag "NanoStat QC"
    publishDir "${params.outdir}/nanostat_report", mode: "copy"
    conda "bioconda::nanostat=1.6.0"

    input:
    path fastq_file

    output:
    path "nanostat_report.txt"

    script:
    """
    NanoStat --fastq ${fastq_file} --outdir . --name nanostat_report.txt --threads ${task.cpus}
    """
}

process READ_STATS {
    tag "Per-read statistics"
    publishDir "${params.outdir}", mode: "copy"
    conda "conda-forge::python=3.10 conda-forge::biopython=1.81 conda-forge::pandas=2.0.3"

    input:
    path fastq_file

    output:
    path "read_stats.csv", emit: stats_csv

    script:
    """
    python ${params.scripts}/read_stats.py \
        --input  ${fastq_file} \
        --output read_stats.csv
    """
}

process VISUALIZE {
    tag "Generate plots"
    publishDir "${params.outdir}/plots", mode: "copy"
    conda "conda-forge::python=3.10 conda-forge::pandas=2.0.3 conda-forge::matplotlib=3.7.2 conda-forge::seaborn=0.12.2"

    input:
    path stats_csv

    output:
    path "*.png"

    script:
    """
    python ${params.scripts}/visualize.py \
        --input  ${stats_csv} \
        --outdir .
    """
}

workflow {
    fastq_ch = Channel.fromPath(params.fastq, checkIfExists: true)
    NANOSTAT_QC(fastq_ch)
    READ_STATS(fastq_ch)
    VISUALIZE(READ_STATS.out.stats_csv)
}

workflow.onComplete {
    log.info (workflow.success ? "Pipeline completed successfully! ✓" : "Pipeline FAILED.")
}
