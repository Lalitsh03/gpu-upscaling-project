import csv

specs = [r['gpu_name'] for r in csv.DictReader(open('data/raw/gpu_specs_raw.csv'))]
prices = [r['gpu_name'] for r in csv.DictReader(open('data/raw/gpu_msrp.csv'))]

missing = [s for s in specs if s not in prices]
matched = [s for s in specs if s in prices]

print(f"Matched: {len(matched)}")
print(f"Missing MSRP: {len(missing)}")
print()
for m in missing:
    print(f"  {m}")