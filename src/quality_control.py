"""Compute custom FASTQ QC metrics."""
import argparse
from pathlib import Path
import pandas as pd
from Bio import SeqIO


def qc_for_fastq(file_path: Path) -> dict:
    total_reads = 0
    total_length = 0
    gc_count = 0
    total_bases = 0
    q20_count = 0
    q30_count = 0
    per_base_quality_sum = []
    per_base_quality_count = []

    for record in SeqIO.parse(str(file_path), "fastq"):
        seq = str(record.seq).upper()
        qual = record.letter_annotations["phred_quality"]
        total_reads += 1
        total_length += len(seq)
        gc_count += seq.count("G") + seq.count("C")
        total_bases += len(seq)
        q20_count += sum(q >= 20 for q in qual)
        q30_count += sum(q >= 30 for q in qual)

        for i, q in enumerate(qual):
            if i >= len(per_base_quality_sum):
                per_base_quality_sum.append(0)
                per_base_quality_count.append(0)
            per_base_quality_sum[i] += q
            per_base_quality_count[i] += 1

    if total_reads == 0 or total_bases == 0:
        return {"sample_id": file_path.stem, "total_reads": 0}

    per_base_avg = [round(s / c, 3) for s, c in zip(per_base_quality_sum, per_base_quality_count)]

    return {
        "sample_id": file_path.stem.replace(".fastq", ""),
        "file": file_path.name,
        "total_reads": total_reads,
        "average_read_length": round(total_length / total_reads, 3),
        "gc_content_percent": round((gc_count / total_bases) * 100, 3),
        "q20_percent": round((q20_count / total_bases) * 100, 3),
        "q30_percent": round((q30_count / total_bases) * 100, 3),
        "per_base_quality_first_20": ";".join(map(str, per_base_avg[:20])),
    }


def find_fastq_files(input_dir: Path):
    patterns = ["*.fastq", "*.fq", "*.fastq.gz", "*.fq.gz"]
    files = []
    for pattern in patterns:
        files.extend(input_dir.glob(pattern))
    return sorted(files)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data", help="FASTQ directory")
    parser.add_argument("--output", default="results/custom_qc_summary.csv")
    args = parser.parse_args()

    input_dir = Path(args.input)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    rows = [qc_for_fastq(path) for path in find_fastq_files(input_dir)]
    df = pd.DataFrame(rows)
    df.to_csv(output, index=False)
    print(df)
    print(f"Saved: {output}")


if __name__ == "__main__":
    main()
