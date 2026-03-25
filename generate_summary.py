import os
import re

def extract_metric(stats_path, metric_name):
    if not os.path.exists(stats_path):
        return "N/A"
    with open(stats_path, 'r') as f:
        for line in f:
            if metric_name in line:
                parts = line.split()
                if len(parts) >= 2:
                    return parts[1]
    return "N/A"

folders = [
    "1_fifo", "1_lru", "1_random",
    "2_fifo", "2_lru", "2_random",
    "4_fifo", "4_lru", "4_random",
    "8_fifo", "8_lru", "8_random",
    "fully_fifo", "fully_lru", "full_random"
]

results = []

for folder in folders:
    stats_path = os.path.join(folder, "stats.txt")
    if not os.path.exists(stats_path):
        continue
    
    # Clean folder name for display
    display_name = folder.replace("_", " ").title()
    if "Fully" in display_name or "Full " in display_name:
        display_name = "Full Assoc (" + display_name.split()[-1] + ")"
    
    sim_seconds = extract_metric(stats_path, "simSeconds")
    miss_rate = extract_metric(stats_path, "system.cpu.dcache.overallMissRate::total")
    misses = extract_metric(stats_path, "system.cpu.dcache.overallMisses::total")
    accesses = extract_metric(stats_path, "system.cpu.dcache.overallAccesses::total")
    cpi = extract_metric(stats_path, "system.cpu.cpi")
    
    # Convert miss rate to percentage
    try:
        miss_rate_pct = f"{float(miss_rate) * 100:.2f}%"
    except ValueError:
        miss_rate_pct = "N/A"
        
    results.append({
        "Config": display_name,
        "Time (s)": sim_seconds,
        "Miss Rate": miss_rate_pct,
        "Misses": misses,
        "Accesses": accesses,
        "CPI": cpi
    })

# Write to Markdown
with open("PERFORMANCE_SUMMARY.md", "w") as f:
    f.write("# Cache Performance Analysis Summary\n\n")
    f.write("This report summarizes the performance of various data cache configurations (16kB) across different associativities and replacement policies.\n\n")
    
    f.write("## 📊 Summary Table\n\n")
    f.write("| Configuration | Execution Time (s) | D-Cache Miss Rate | D-Cache Misses | D-Cache Accesses | CPI |\n")
    f.write("|:---|:---:|:---:|:---:|:---:|:---:|\n")
    for r in results:
        f.write(f"| {r['Config']} | {r['Time (s)']} | {r['Miss Rate']} | {r['Misses']} | {r['Accesses']} | {r['CPI']} |\n")
    
    f.write("\n## 🔍 Observations & Insights\n\n")
    f.write("### 1. Effect of Associativity\n")
    f.write("- Increasing associativity generally reduces **conflict misses**. Moving from 1-way (Direct Mapped) to 8-way significantly improves performance.\n")
    f.write("- Full Associativity represents the theoretical limit for minimizing conflict misses for a given cache size.\n\n")
    
    f.write("### 2. Replacement Policy Comparison\n")
    f.write("- **LRU (Least Recently Used):** Typically performs best by exploiting temporal locality.\n")
    f.write("- **FIFO (First-In, First-Out):** A simpler policy that often performs slightly worse than LRU but better than Random.\n")
    f.write("- **Random:** Usually the worst-performing policy but requires the least hardware complexity.\n\n")
    
    f.write("### 3. Benchmark Characteristics (`test.c`)\n")
    f.write("- The benchmark includes loops specifically designed to stress the cache (Phases 1, 2, and 5).\n")
    f.write("- Phase 5 forces evictions by accessing 257 lines in a 256-line cache, making the replacement policy critical.\n")

print("Generated PERFORMANCE_SUMMARY.md")
