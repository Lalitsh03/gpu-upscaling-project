import csv
import sqlite3

db_path = "data/gpu_project.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create passmark table
cursor.execute("DROP TABLE IF EXISTS gpu_passmark")
cursor.execute("""
    CREATE TABLE gpu_passmark (
        gpu_name TEXT PRIMARY KEY,
        passmark_g3d INTEGER,
        passmark_source TEXT
    )
""")

# Load passmark data
with open("data/raw/gpu_passmark.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cursor.execute("INSERT OR IGNORE INTO gpu_passmark VALUES (?, ?, ?)", (
            row["gpu_name"],
            int(row["passmark_g3d"]),
            row["passmark_source"],
        ))

# Rebuild analysis table with passmark scores
cursor.execute("DROP TABLE IF EXISTS gpu_analysis")
cursor.execute("""
    CREATE TABLE gpu_analysis AS
    SELECT 
        s.gpu_name,
        s.manufacturer,
        s.generation,
        s.architecture,
        s.release_date,
        m.launch_year,
        m.msrp_usd,
        s.base_clock_mhz,
        s.boost_clock_mhz,
        s.memory_size_gb,
        s.memory_type,
        s.memory_bus_bits,
        s.memory_bandwidth_gb_s,
        s.tdp_watts,
        s.process_size_nm,
        s.die_size_mm2,
        s.transistor_count_m,
        s.shading_units,
        s.tensor_cores,
        s.ray_tracing_cores,
        s.single_float_tflops,
        p.passmark_g3d,
        ROUND(s.single_float_tflops / m.msrp_usd, 2) AS tflops_per_dollar,
        ROUND(CAST(p.passmark_g3d AS REAL) / m.msrp_usd, 2) AS passmark_per_dollar,
        CASE
            WHEN m.msrp_usd < 250 THEN 'Budget'
            WHEN m.msrp_usd < 500 THEN 'Midrange'
            WHEN m.msrp_usd < 900 THEN 'High-end'
            ELSE 'Flagship'
        END AS market_tier
    FROM gpu_specs s
    INNER JOIN gpu_msrp m ON s.gpu_name = m.gpu_name
    LEFT JOIN gpu_passmark p ON s.gpu_name = p.gpu_name
    ORDER BY s.manufacturer, s.release_date
""")

conn.commit()

# Verify
cursor.execute("SELECT COUNT(*) FROM gpu_analysis WHERE passmark_g3d IS NOT NULL")
with_scores = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM gpu_analysis WHERE passmark_g3d IS NULL")
without_scores = cursor.fetchone()[0]

print(f"GPUs with PassMark scores: {with_scores}")
print(f"GPUs without PassMark scores: {without_scores}")

# Show passmark per dollar by generation
cursor.execute("""
    SELECT manufacturer, generation, 
           COUNT(*) as count,
           ROUND(AVG(msrp_usd), 0) as avg_msrp,
           ROUND(AVG(passmark_g3d), 0) as avg_passmark,
           ROUND(AVG(passmark_per_dollar), 2) as avg_passmark_per_dollar
    FROM gpu_analysis
    WHERE passmark_g3d IS NOT NULL
    GROUP BY manufacturer, generation
    ORDER BY manufacturer, MIN(launch_year)
""")

print(f"\n{'Manufacturer':<10} {'Generation':<25} {'Count':>5} {'Avg MSRP':>9} {'Avg G3D':>9} {'G3D/$':>8}")
print("-" * 75)
for row in cursor.fetchall():
    print(f"{row[0]:<10} {row[1]:<25} {row[2]:>5} {row[3]:>9.0f} {row[4]:>9.0f} {row[5]:>8.2f}")

conn.close()