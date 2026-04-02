import csv

rows = list(csv.DictReader(open('data/raw/gpu_specs_raw.csv')))

# Flag GPUs that might be OEM, regional, or alternate die variants
flags = ['OEM', 'GRE', 'D V2', 'GA10', 'AD10', 'TiM', 'GDDR6', '3840SP', 'TU104', '4090 D']

print("=== POTENTIALLY EXCLUDE ===")
for r in rows:
    name = r['gpu_name']
    for flag in flags:
        if flag in name:
            print(f"{r['manufacturer']:6} | {name}")
            break

print()
print("=== CLEAN GPUs ===")
count = 0
for r in rows:
    name = r['gpu_name']
    flagged = False
    for flag in flags:
        if flag in name:
            flagged = True
            break
    if not flagged:
        count += 1
        print(f"{r['manufacturer']:6} | {r['generation']:25} | {name}")

print(f"\nClean count: {count}")