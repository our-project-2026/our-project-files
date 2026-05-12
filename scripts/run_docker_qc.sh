#!/usr/bin/env bash
set -euo pipefail
mkdir -p results/fastqc_raw results/fastp results/fastqc_trimmed results/multiqc data/trimmed

for fq in data/*.fastq data/*.fq data/*.fastq.gz data/*.fq.gz; do
  [ -e "$fq" ] || continue
  base=$(basename "$fq")
  sample=${base%%.fastq.gz}
  sample=${sample%%.fq.gz}
  sample=${sample%%.fastq}
  sample=${sample%%.fq}

  echo "Raw FastQC: $base"
  docker run --rm -v "$(pwd):/work" biocontainers/fastqc:v0.11.9_cv8 fastqc "/work/$fq" -o /work/results/fastqc_raw

  echo "fastp trimming: $base"
  docker run --rm -v "$(pwd):/work" staphb/fastp fastp \
    -i "/work/$fq" \
    -o "/work/data/trimmed/${sample}_trimmed.fastq" \
    -j "/work/results/fastp/${sample}_fastp.json" \
    -h "/work/results/fastp/${sample}_fastp.html"

  echo "Trimmed FastQC: ${sample}_trimmed.fastq"
  docker run --rm -v "$(pwd):/work" biocontainers/fastqc:v0.11.9_cv8 fastqc "/work/data/trimmed/${sample}_trimmed.fastq" -o /work/results/fastqc_trimmed
done

echo "Running MultiQC"
docker run --rm -v "$(pwd):/work" ewels/multiqc multiqc /work/results -o /work/results/multiqc
