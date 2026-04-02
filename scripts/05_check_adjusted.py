import sqlite3

conn = sqlite3.connect("data/gpu_project.db")
cursor = conn.cursor()

cursor.execute("""
    SELECT manufacturer, generation,
           COUNT(*) as count,
           ROUND(AVG(msrp_usd), 0) as avg_msrp_raw,
           ROUND(AVG(msrp_2024_adjusted), 0) as avg_msrp_adj,
           ROUND(AVG(passmark_per_dollar), 2) as raw_g3d_per_dollar,
           ROUND(AVG(passmark_per_dollar_adjusted), 2) as adj_g3d_per_dollar
    FROM gpu_analysis
    WHERE passmark_g3d IS NOT NULL
    GROUP BY manufacturer, generation
    ORDER BY manufacturer, MIN(launch_year)
""")

print(f"{'Mfr':<7} {'Generation':<25} {'#':>2} {'RawMSRP':>8} {'AdjMSRP':>8} {'G3D/$':>7} {'AdjG3D/$':>8}")
print("-" * 75)
for row in cursor.fetchall():
    print(f"{row[0]:<7} {row[1]:<25} {row[2]:>2}   ${row[3]:>5.0f}   ${row[4]:>5.0f}  {row[5]:>6.2f}   {row[6]:>6.2f}")

conn.close()