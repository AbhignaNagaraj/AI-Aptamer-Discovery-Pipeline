#!/usr/bin/env python3

import argparse
import re

# ---------- ALIGNER ----------
try:
    from Bio.Align import PairwiseAligner
    aligner = PairwiseAligner()
    aligner.mode = "global"
    use_alignment = True
except ImportError:
    use_alignment = False

# ---------- ARGUMENTS ----------
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True)
parser.add_argument("-o", "--output", default="analyzed_structures.txt")

args = parser.parse_args()

# ---------- FUNCTIONS ----------
def gc_content(seq):
    return (seq.count("G") + seq.count("C")) / len(seq) * 100 if seq else 0


def similarity(seq1, seq2):
    if not seq1 or not seq2:
        return 0.0

    if use_alignment:
        try:
            score = aligner.score(seq1, seq2)
            return score / max(len(seq1), len(seq2))
        except:
            return 0.0
    else:
        length = min(len(seq1), len(seq2))
        matches = sum(1 for i in range(length) if seq1[i] == seq2[i])
        return matches / length if length > 0 else 0


# ---------- READ CLEAN ----------
lines = []
with open(args.input) as f:
    for line in f:
        line = line.strip()
        if line:
            lines.append(line)

# ---------- PARSE (3-line blocks) ----------
records = []

for i in range(0, len(lines), 3):
    if i + 2 >= len(lines):
        break

    header = lines[i]
    seq = lines[i+1]
    struct_line = lines[i+2]

    # extract MFE from header OR structure
    mfe = 0.0

    # try from header first
    match = re.search(r"MFE=(-?\d+\.\d+)", header)
    if match:
        mfe = float(match.group(1))
    else:
        # fallback to structure line
        match = re.search(r"\((-?\d+\.\d+)\)", struct_line)
        if match:
            mfe = float(match.group(1))

    records.append({
        "header": header.split("|")[0].strip(),  # clean header
        "seq": seq,
        "struct_line": struct_line,
        "mfe": mfe
    })

# ---------- GC ----------
for r in records:
    r["gc"] = gc_content(r["seq"])

# ---------- SIM ----------
ref_seq = records[0]["seq"] if records else ""

for r in records:
    r["sim"] = similarity(r["seq"], ref_seq)

# ---------- SAVE ----------
with open(args.output, "w") as out:
    for r in records:
        out.write(
            f"{r['header']} | MFE={r['mfe']:.2f} | GC={r['gc']:.2f}% | SIM={r['sim']:.2f}\n"
        )
        out.write(f"{r['seq']}\n")
        out.write(f"{r['struct_line']}\n\n")

# ---------- SUMMARY ----------
print("\n=== Analysis Complete ===")
print(f"Total sequences: {len(records)}")
print(f"Output: {args.output}")