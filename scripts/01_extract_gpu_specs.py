from dbgpu import GPUDatabase
import csv

db = GPUDatabase.default()

# Exact generation strings for desktop consumer GPUs only
target_generations = [
    # Nvidia desktop
    "GeForce 20",
    "GeForce 30",
    "GeForce 40",
    "GeForce 50",
    # AMD desktop
    "Navi(RX 5000)",
    "Navi II(RX 6000)",
    "Navi III(RX 7000)",
    "Navi IV(RX 9000)",
    # Intel desktop
    "Alchemist(Arc 3)",
    "Alchemist(Arc 5)",
    "Alchemist(Arc 7)",
    "Battlemage(Arc 5)",
]

rows = []
for key, spec in db.specifications.items():
    gen = spec.generation if spec.generation else ""

    # Only exact generation matches
    if gen not in target_generations:
        continue

    rows.append({
        "gpu_name": spec.name,
        "manufacturer": spec.manufacturer,
        "generation": spec.generation,
        "architecture": spec.architecture,
        "release_date": str(spec.release_date) if spec.release_date else "",
        "base_clock_mhz": spec.base_clock_mhz,
        "boost_clock_mhz": spec.boost_clock_mhz,
        "memory_size_gb": spec.memory_size_gb,
        "memory_type": spec.memory_type,
        "memory_clock_mhz": spec.memory_clock_mhz,
        "memory_bus_bits": spec.memory_bus_bits,
        "memory_bandwidth_gb_s": spec.memory_bandwidth_gb_s,
        "tdp_watts": spec.thermal_design_power_w,
        "process_size_nm": spec.process_size_nm,
        "die_size_mm2": spec.die_size_mm2,
        "transistor_count_m": spec.transistor_count_m,
        "shading_units": spec.shading_units,
        "tensor_cores": spec.tensor_cores,
        "ray_tracing_cores": spec.ray_tracing_cores,
        "single_float_tflops": spec.single_float_performance_gflop_s,
        "bus_interface": spec.bus_interface,
        "tpu_url": spec.tpu_url,
    })

# Sort by manufacturer then release date
rows.sort(key=lambda r: (r["manufacturer"], r["release_date"]))

# Write to CSV
output_path = "data/raw/gpu_specs_raw.csv"
with open(output_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Exported {len(rows)} GPUs to {output_path}")
print()
# Show what we got
for r in rows:
    print(f"{r['manufacturer']:6} | {r['generation']:25} | {r['gpu_name']}")