import re
import pandas as pd

input_file = "analyzed_structures.txt"
ed_file = "ed_results.txt"

# -----------------------------
# LOAD ED VALUES
# -----------------------------
ed_dict = {}

with open(ed_file) as f:
    for line in f:
        line = line.strip()

        if "\tED=" in line:
            header, ed = line.split("\tED=")
            ed_dict[header.strip()] = float(ed.strip())

# -----------------------------
# PARSE ANALYZED STRUCTURES
# -----------------------------
records = []

with open(input_file) as f:
    content = f.read().strip().split("\n\n")

for block in content:

    lines = block.strip().split("\n")

    if len(lines) < 3:
        continue

    header = lines[0]
    sequence = lines[1]
    structure = lines[2]

    # Extract values
    mfe_match = re.search(r'MFE=([-0-9.]+)', header)
    gc_match = re.search(r'GC=([0-9.]+)', header)
    sim_match = re.search(r'SIM=([0-9.]+)', header)

    # Read count and RPM from header
    header_name = header.split("|")[0].replace(">", "").strip()

    parts = header_name.split("_")

    read_count = int(parts[0])
    rpm = float(parts[1])

    mfe = float(mfe_match.group(1))
    gc = float(gc_match.group(1))
    sim = float(sim_match.group(1))

    ed = ed_dict.get(header, 999)

    # -----------------------------
    # SCORING SYSTEM
    # -----------------------------
    score = 0

    # LOW ED = BEST
    score += max(0, (20 - ed)) * 3

    # MORE NEGATIVE MFE = BETTER
    score += abs(mfe) * 2

    # RPM
    score += rpm * 0.5

    # GC optimal range 45-60
    if 45 <= gc <= 60:
        score += 10

    # similarity
    score += sim * 5

    records.append({
        "Header": header,
        "Read_Count": read_count,
        "RPM": rpm,
        "MFE": mfe,
        "GC": gc,
        "SIM": sim,
        "ED": ed,
        "Score": round(score, 2),
        "Sequence": sequence,
        "Structure": structure
    })

# -----------------------------
# CREATE DATAFRAME
# -----------------------------
df = pd.DataFrame(records)

# Rank by score
df = df.sort_values(by="Score", ascending=False)

# Save full ranking
df.to_csv("ranked_aptamers.csv", index=False)

# -----------------------------
# PRINT TOP 5
# -----------------------------
print("\n=== TOP 5 APTAMERS ===\n")

top5 = df.head(5)

for i, row in top5.iterrows():

    print(f"Rank Score : {row['Score']}")
    print(f"RPM        : {row['RPM']}")
    print(f"MFE        : {row['MFE']}")
    print(f"GC         : {row['GC']}")
    print(f"ED         : {row['ED']}")
    print(f"SIM        : {row['SIM']}")
    print(f"Sequence   : {row['Sequence']}")
    print(f"Structure  : {row['Structure']}")
    print("-" * 60)

print("\nSaved: ranked_aptamers.csv")