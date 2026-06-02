#!/usr/bin/env python3

import argparse
from collections import Counter

# ---------- ARGUMENTS ----------
parser = argparse.ArgumentParser(description="Discover core and extended motifs from input motifs")
parser.add_argument("-i", "--input", required=True, help="Input motif file (motif count format)")
parser.add_argument("-o", "--output", default="final_motifs.txt", help="Output file")
parser.add_argument("--min_len", type=int, default=5, help="Minimum core motif length")

args = parser.parse_args()

# ---------- LOAD MOTIFS ----------
motifs = []
weights = {}

with open(args.input) as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) >= 2:
            motif = parts[0].upper()
            count = int(parts[1])
            motifs.append(motif)
            weights[motif] = count

print(f"\nLoaded {len(motifs)} motifs")

# ---------- FIND COMMON SUBSTRINGS ----------
substring_counts = Counter()

for motif, weight in weights.items():
    L = len(motif)
    for i in range(L):
        for j in range(i + args.min_len, L + 1):
            sub = motif[i:j]
            substring_counts[sub] += weight

# ---------- FILTER CORE MOTIFS ----------
# Keep substrings that appear in multiple motifs
core_motifs = {}

for sub, score in substring_counts.items():
    if len(sub) >= args.min_len:
        occurrences = sum(1 for m in motifs if sub in m)
        if occurrences >= 3:  # appears in ≥3 motifs
            core_motifs[sub] = score

# ---------- REMOVE REDUNDANT (keep longest) ----------
final_core = []

for m in sorted(core_motifs, key=len, reverse=True):
    if not any(m in longer for longer in final_core):
        final_core.append(m)

# ---------- EXTEND MOTIFS ----------
def extend_motif(core, motifs):
    extensions = []

    for m in motifs:
        if core in m:
            idx = m.find(core)
            left = m[:idx]
            right = m[idx + len(core):]
            extensions.append((left, right))

    return extensions

extended_motifs = []

for core in final_core:
    ext = extend_motif(core, motifs)
    extended_motifs.append((core, ext))

# ---------- SAVE ----------
with open(args.output, "w") as out:
    out.write("=== CORE MOTIFS ===\n")
    for m in final_core:
        out.write(m + "\n")

    out.write("\n=== EXTENDED CONTEXT ===\n")
    for core, ext in extended_motifs:
        out.write(f"\n{core}:\n")
        for l, r in ext[:5]:  # show few examples
            out.write(f"{l}[{core}]{r}\n")

print(f"\nSaved final motifs to: {args.output}")
