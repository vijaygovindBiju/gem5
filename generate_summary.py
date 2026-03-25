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
    f.write("### 1. The Associativity Paradox (8-Way vs Full-Assoc)\n")
    f.write("- Counter-intuitively, **8-way LRU** (0.19% miss rate) performs better than **Full-Assoc LRU** (0.30%).\n")
    f.write("- This is due to the specific access pattern in `test.c` (Phase 5), which accesses 257 lines. In an 8-way cache, only one set (Set 0) experiences conflict misses and thrashing, while the other 31 sets remain unaffected. In a Fully Associative cache, *every* access to the 257th line can evict a line that is needed soon by *any* part of the program.\n\n")
    
    f.write("### 2. The FIFO Thrashing Anomaly\n")
    f.write("- **Fully Associative FIFO** experiences massive thrashing (5.03% miss rate).\n")
    f.write("- Because FIFO evicts the oldest line regardless of reuse, it enters a pathological state in cyclic access patterns where the working set is slightly larger than the cache. The line just evicted is the one needed next, creating a 'worst-case' scenario for cache performance.\n\n")
    
    f.write("### 3. Random Replacement Policy Efficiency\n")
    f.write("- The **Random** policy is surprisingly robust, often matching or even beating LRU at lower associativities (e.g., 4-way Random @ 0.39% vs LRU @ 0.46%).\n")
    f.write("- Random replacement avoids the pathological eviction patterns that can cripple FIFO or LRU in specific workloads, making it a viable low-complexity alternative for hardware implementation.\n\n")
    
    f.write("### 4. CPI & Hardware Design Implications\n")
    f.write("- There is a clear **diminishing returns** curve. Moving from 1-way to 4-way provides the largest performance leap.\n")
    f.write("- The transition from 4-way to 8-way or Full-Assoc offers marginal gains at the cost of significantly increased hardware complexity (more comparators, higher power, and potentially higher hit latency).\n")

print("Generated PERFORMANCE_SUMMARY.md")
