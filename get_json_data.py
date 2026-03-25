import os
import json

def extract_metric(stats_path, metric_name):
    if not os.path.exists(stats_path):
        return None
    with open(stats_path, 'r') as f:
        for line in f:
            if metric_name in line:
                parts = line.split()
                if len(parts) >= 2:
                    return parts[1]
    return None

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
    
    parts = folder.split('_')
    assoc = parts[0].title()
    policy = parts[1].upper()
    
    sim_seconds = extract_metric(stats_path, "simSeconds")
    miss_rate = extract_metric(stats_path, "system.cpu.dcache.overallMissRate::total")
    misses = extract_metric(stats_path, "system.cpu.dcache.overallMisses::total")
    accesses = extract_metric(stats_path, "system.cpu.dcache.overallAccesses::total")
    cpi = extract_metric(stats_path, "system.cpu.cpi")
    avg_miss_latency = extract_metric(stats_path, "system.cpu.dcache.overallAvgMissLatency::total")
    
    # 1.0 GHz clock -> 1 tick = 1 ns? Wait, gem5 default tick is 1ps.
    # If clock is 1GHz, period is 1000 ticks.
    # overallAvgMissLatency is in ticks.
    # AMAT (cycles) = HitLatency (cycles) + MissRate * (MissLatency / ClockPeriod)
    
    m_rate = float(miss_rate) if miss_rate else 0
    m_latency_ticks = float(avg_miss_latency) if avg_miss_latency else 0
    clock_period_ticks = 1000 # 1GHz
    
    hit_latency = 2 # From index.html specs
    amat = hit_latency + m_rate * (m_latency_ticks / clock_period_ticks)
    
    results.append({
        "id": folder,
        "assoc": assoc,
        "policy": policy,
        "time": float(sim_seconds) if sim_seconds else 0,
        "missRate": m_rate * 100,
        "hitRate": (1 - m_rate) * 100,
        "misses": int(misses) if misses else 0,
        "accesses": int(accesses) if accesses else 0,
        "cpi": float(cpi) if cpi else 0,
        "amat": amat
    })

with open("results.json", "w") as f:
    json.dump(results, f, indent=4)
