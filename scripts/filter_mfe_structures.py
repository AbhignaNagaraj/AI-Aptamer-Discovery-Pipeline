#!/usr/bin/env python3

import argparse
import re

# ---------- ARGUMENTS ----------
parser = argparse.ArgumentParser(description="Filter RNAfold structures by MFE")
parser.add_argument("-i", "--input", required=True, help="structures.txt from RNAfold")
parser.add_argument("-o", "--output", default="filtered_structures.txt")
parser.add_argument("-t", "--threshold", type=float, default=-5.0)

args = parser.parse_args()

threshold = args.threshold

kept = 0
total = 0

with open(args.input) as f, open(args.output, "w") as out:

    lines = f.readlines()

    # process 3 lines per record
    for i in range(0, len(lines), 3):

        header = lines[i].strip()
        seq = lines[i+1].strip()
        struct_line = lines[i+2].strip()

        # extract MFE
        match = re.search(r"\((-?\d+\.\d+)\)", struct_line)
        if not match:
            continue

        mfe = float(match.group(1))
        structure = struct_line.split()[0]

        total += 1

        if mfe <= threshold:
            out.write(f"{header} | MFE={mfe}\n")
            out.write(f"{seq}\n")
            out.write(f"{structure}\n\n")
            kept += 1

# ---------- SUMMARY ----------
print("\n=== MFE Filtering Summary ===")
print(f"Total sequences: {total}")
print(f"Kept (MFE <= {threshold}): {kept}")
print(f"Output saved to: {args.output}")
