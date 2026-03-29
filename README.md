# Cache Performance Analysis & Optimization

An empirical study of cache associativity and replacement policies on a 16kB data cache, simulated using the **gem5** infrastructure. This project evaluates how different mapping techniques (1, 2, 4, and 8-way set-associative) and replacement algorithms (LRU, FIFO) impact system performance metrics like Hit Rate, AMAT, and CPI.

## 📊 Project Overview

Modern CPU performance is heavily dependent on the efficiency of the cache hierarchy. This lab explores the trade-offs between hardware complexity (associativity) and eviction intelligence (replacement policies) through a series of controlled simulations.

### Key Configurations Tested:
- **Associativity:** 1-way (Direct Mapped), 2-way, 4-way, and 8-way set-associative.
- **Replacement Policies:** Least Recently Used (LRU) and First-In, First-Out (FIFO).
- **Cache Geometry:** 16kB total size, 64-Byte line size (256 lines).

## 🚀 Key Findings

- **The "2-Way" Leap:** Moving from 1-way to 2-way associativity provides the single largest performance gain, reducing the miss rate by approximately **50%**.
- **LRU Superiority:** LRU consistently outperforms FIFO across all associative configurations. The advantage is most pronounced at 8-way associativity, where LRU achieved a near-perfect **99.81% hit rate**.
- **The Sweet Spot:** **4-Way LRU** represents the optimal balance for this workload, capturing over 99.5% of hits while maintaining lower hardware complexity compared to 8-way designs.
- **Latency Impact:** Increasing associativity from 1-way to 8-way (LRU) reduced the system CPI from **5.12** to **3.90**—a **24% improvement** in overall execution efficiency.

## 🛠️ Simulation & Methodology

The simulations were performed using **gem5** in System-Call Emulation (SE) mode with an x86 TimingSimpleCPU model.

### Workload Details (`test.c`):
The benchmark generates pathological memory access patterns designed to stress-test cache logic:
- **Conflict Stress:** Accesses memory locations mapped to the same set using 16kB strides.
- **Replacement Stress:** Iterates through 257 distinct cache lines (1 more than the total capacity) to force evictions and test the efficiency of LRU vs FIFO.

## 📁 Repository Structure

- `index.html`: Main interactive dashboard for result visualization.
- `graph.html`: Comparative performance charts (LRU vs FIFO).
- `direct.html` / `2way.html` / `4way.html` / `8way.html`: Detailed analysis for each associativity.
- `results.json`: Raw simulation data for all 8 configurations.
- `PERFORMANCE_SUMMARY.md`: High-level technical summary.

## 📚 References

**Benchmark Methodology**
- McVoy, L. and Staelin, C. (1996). *lmbench: Portable Tools for Performance Analysis.* Proceedings of USENIX ATC.

**Simulation Infrastructure**
- Binkert, N. et al. (2011). *The gem5 Simulator.* ACM SIGARCH Computer Architecture News, 39(2).
- Lowe-Power, J. et al. (2020). *The gem5 Simulator: Version 20.0+.* arXiv:2007.03152.

**Cache Architecture**
- Hill, M.D. and Smith, A.J. (1989). *Evaluating Associativity in CPU Caches.* IEEE Transactions on Computers, 38(12).
- Hennessy, J. L. and Patterson, D. A. (2019). *Computer Architecture: A Quantitative Approach.* 6th ed. Morgan Kaufmann.
