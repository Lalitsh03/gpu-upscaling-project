import sqlite3

db_path = "data/gpu_project.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# CPI-based inflation multipliers to convert past dollars to 2024 dollars
# Source: US Bureau of Labor Statistics CPI-U annual averages
inflation_to_2024 = {
    2018: 1.19,
    2019: 1.16,
    2020: 1.15,
    2021: 1.10,
    2022: 1.02,
    2023: 0.99,
    2024: 1.00,
    2025: 0.97,
}

# Add inflation-adjusted MSRP column to analysis table
cursor.execute("PRAGMA table_info(gpu_analysis)")
columns = [col[1] for col in cursor.fetchall()]

if "msrp_2024_adjusted" not in columns:
    cursor.execute("ALTER TABLE gpu_analysis ADD COLUMN msrp_2024_adjusted REAL")
    cursor.execute("ALTER TABLE gpu_analysis ADD COLUMN passmark_per_dollar_adjusted REAL")

# Update each row
for year, multiplier in inflation_to_2024.items():
    cursor.execute("""
        UPDATE gpu_analysis 
        SET msrp_2024_adjusted = ROUND(msrp_usd * ?, 2),
            passmark_per_dollar_adjusted = ROUND(CAST(passmark_g3d AS REAL) / (msrp_usd * ?), 2)
        WHERE launch_year = ?
    """, (multiplier, multiplier, year))

conn.commit()

# Show the difference inflation makes
cursor.execute("""
    SELECT gpu_name, launch_year, msrp_usd, msrp_2024_adjusted, 
           passmark_per_dollar, passmark_per_dollar_adjusted
    FROM gpu_analysis
    ORDER BY manufacturer, launch_year, msrp_usd
""")

print(f"{'GPU':<35} {'Year':>4} {'MSRP':>6} {'Adj$':>7} {'G3D/$':>7} {'AdjG3D/$':>8}")
print("-" * 78)
for row in cursor.fetchall():
    print(f"{row[0]:<35} {row[1]:>4} ${row[2]:>5} ${row[3]:>6.0f}  {row[4]:>6.2f}  {row[5]:>7.2f}")

conn.close()
print("\nInflation adjustment complete.")