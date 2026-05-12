# Bioinformatics Programming Project

This project processes FASTQ files from SRA accessions, computes custom QC metrics, runs Docker-based QC/trimming, extracts fastp features, extracts k-mer frequencies, builds `features.csv`, and optionally trains a machine learning classifier.

## SRA samples
The sample IDs are in `sra_ids.txt`. Edit `sample_metadata.csv` if your real classes are different.

## Folder structure

```text
bio_project_ready/
├── data/
├── results/
├── scripts/
├── src/
├── README.md
├── requirements.txt
├── sample_metadata.csv
└── sra_ids.txt
```

## 1. Create environment

Windows CMD/PowerShell:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Mac/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 2. Download FASTQ files

Install NCBI SRA Toolkit first, then run:

```bash
bash scripts/download_sra.sh
```

On Windows, run this from Git Bash. The FASTQ files will be saved in `data/`.

## 3. Run custom Python QC

```bash
python src/fastq_parser.py data/SRR37278450.fastq
python src/quality_control.py --input data --output results/custom_qc_summary.csv
```

## 4. Run Docker QC and trimming

Make sure Docker Desktop is running, then run from Git Bash:

```bash
bash scripts/run_docker_qc.sh
```

This creates FastQC, fastp, trimmed FASTQ, and MultiQC outputs in `results/`.

## 5. Extract fastp features

```bash
python src/feature_extraction.py --fastp-dir results/fastp --metadata sample_metadata.csv --output results/fastp_features.csv
```

## 6. Extract k-mer features

```bash
python src/kmer_extraction.py --input data --metadata sample_metadata.csv --k 3 --output results/kmer_features.csv
```

## 7. Build final features.csv

```bash
python src/build_features.py --fastp results/fastp_features.csv --kmers results/kmer_features.csv --output results/features.csv
```

## 8. Optional ML

```bash
python src/ml_model.py --features results/features.csv
```

## Important viva questions

- FASTQ sequence is the DNA/RNA read; quality scores show confidence in each base.
- Phred score: Q = -10 log10(error probability). Q30 means about 0.1% error.
- GC content is the percentage of G and C bases. Abnormal GC can suggest contamination or bias.
- K-mers are short overlapping subsequences. They capture sequence composition and can be used as ML features.
- Docker volume mapping `-v` connects your local folder to the container so outputs are saved on your computer.
- FastQC diagnoses quality problems; fastp trims/filter reads to improve quality.
