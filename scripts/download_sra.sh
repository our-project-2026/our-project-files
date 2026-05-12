#!/usr/bin/env bash
set -euo pipefail
mkdir -p data
while read -r SRR; do
  [ -z "$SRR" ] && continue
  echo "Downloading $SRR"
  prefetch "$SRR" --output-directory data/sra_cache
  fasterq-dump "data/sra_cache/$SRR" --outdir data --threads 4 --split-files
  # If paired-end files are created, keep them as SRR_1.fastq and SRR_2.fastq.
  # If single-end, fasterq-dump creates SRR.fastq.
done < sra_ids.txt
