FROM continuumio/miniconda3:23.10.0-1

LABEL maintainer="Emre Keskin"
LABEL description="Mini Bioinformatics Pipeline - Long-read QC"

WORKDIR /pipeline

COPY environment.yml .

RUN conda env create -f environment.yml && \
    conda clean -afy

SHELL ["conda", "run", "-n", "mini-bio-pipeline", "/bin/bash", "-c"]

COPY scripts/ ./scripts/
COPY pipeline/ ./pipeline/

ENV PATH /opt/conda/envs/mini-bio-pipeline/bin:$PATH

CMD ["bash"]
