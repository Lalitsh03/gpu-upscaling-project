import csv
import sqlite3

# Connect to SQLite database (creates it if it doesn't exist)
db_path = "data/gpu_project.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create gpu_specs table
cursor.execute("DROP TABLE IF EXISTS gpu_specs")
cursor.execute("""
    CREATE TABLE gpu_specs (
        gpu_name TEXT PRIMARY KEY,
        manufacturer TEXT,
        generation TEXT,
        architecture TEXT,
        release_date TEXT,
        base_clock_mhz REAL,
        boost_clock_mhz REAL,
        memory_size_gb REAL,
        memory_type TEXT,
        memory_clock_mhz REAL,
        memory_bus_bits INTEGER,
        memory_bandwidth_gb_s REAL,
        tdp_watts INTEGER,
        process_size_nm INTEGER,
        die_size_mm2 REAL,
        transistor_count_m REAL,
        shading_units INTEGER,
        tensor_cores INTEGER,
        ray_tracing_cores INTEGER,
        single_float_tflops REAL,
        bus_interface TEXT,
        tpu_url TEXT
    )
""")

# Load gpu_specs_raw.csv into the table
with open("data/raw/gpu_specs_raw.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cursor.execute("""
            INSERT OR IGNORE INTO gpu_specs VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
        """, (
            row["gpu_name"],
            row["manufacturer"],
            row["generation"],
            row["architecture"],
            row["release_date"],
            float(row["base_clock_mhz"]) if row["base_clock_mhz"] else None,
            float(row["boost_clock_mhz"]) if row["boost_clock_mhz"] else None,
            float(row["memory_size_gb"]) if row["memory_size_gb"] else None,
            row["memory_type"],
            float(row["memory_clock_mhz"]) if row["memory_clock_mhz"] else None,
            int(row["memory_bus_bits"]) if row["memory_bus_bits"] else None,
            float(row["memory_bandwidth_gb_s"]) if row["memory_bandwidth_gb_s"] else None,
            int(row["tdp_watts"]) if row["tdp_watts"] else None,
            int(row["process_size_nm"]) if row["process_size_nm"] else None,
            float(row["die_size_mm2"]) if row["die_size_mm2"] else None,
            float(row["transistor_count_m"]) if row["transistor_count_m"] else None,
            int(row["shading_units"]) if row["shading_units"] else None,
            int(row["tensor_cores"]) if row["tensor_cores"] else None,
            int(row["ray_tracing_cores"]) if row["ray_tracing_cores"] else None,
            float(row["single_float_tflops"]) if row["single_float_tflops"] else None,
            row["bus_interface"],
            row["tpu_url"],
        ))

# Create gpu_msrp table
cursor.execute("DROP TABLE IF EXISTS gpu_msrp")
cursor.execute("""
    CREATE TABLE gpu_msrp (
        gpu_name TEXT PRIMARY KEY,
        msrp_usd INTEGER,
        msrp_source TEXT,
        launch_year INTEGER
    )
""")

# Load gpu_msrp.csv into the table
with open("data/raw/gpu_msrp.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cursor.execute("""
            INSERT OR IGNORE INTO gpu_msrp VALUES (?, ?, ?, ?)
        """, (
            row["gpu_name"],
            int(row["msrp_usd"]),
            row["msrp_source"],
            int(row["launch_year"]),
        ))

conn.commit()

# Quick verification
cursor.execute("SELECT COUNT(*) FROM gpu_specs")
spec_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM gpu_msrp")
msrp_count = cursor.fetchone()[0]

cursor.execute("""
    SELECT COUNT(*) FROM gpu_specs s
    INNER JOIN gpu_msrp m ON s.gpu_name = m.gpu_name
""")
matched_count = cursor.fetchone()[0]

print(f"gpu_specs table: {spec_count} rows")
print(f"gpu_msrp table: {msrp_count} rows")
print(f"Matched (specs + price): {matched_count} rows")

conn.close()
print(f"\nDatabase saved to {db_path}")