# Cache Performance Analysis Summary

This report summarizes the performance of various data cache configurations (16kB) across different associativities and replacement policies.

## 📊 Summary Table

| Configuration | Hit Rate | Miss Rate | AMAT (cycles) | CPI | Exec Time (s) |
|:---|:---:|:---:|:---:|:---:|:---:|
| 1 Fifo | 96.57% | 3.43% | 3.881 | 5.122588 | 0.030148 |
| 1 Lru | 96.57% | 3.43% | 3.881 | 5.122588 | 0.030148 |
| 1 Random | 96.57% | 3.43% | 3.881 | 5.122588 | 0.030148 |
| 2 Fifo | 98.21% | 1.79% | 2.984 | 4.500055 | 0.026485 |
| 2 Lru | 98.71% | 1.29% | 2.713 | 4.312176 | 0.025379 |
| 2 Random | 98.51% | 1.49% | 2.826 | 4.390577 | 0.025840 |
| 4 Fifo | 99.31% | 0.69% | 2.365 | 4.069676 | 0.023952 |
| 4 Lru | 99.54% | 0.46% | 2.246 | 3.987402 | 0.023467 |
| 4 Random | 99.61% | 0.39% | 2.218 | 3.968233 | 0.023355 |
| 8 Fifo | 99.45% | 0.55% | 2.313 | 4.034377 | 0.023744 |
| 8 Lru | 99.81% | 0.19% | 2.114 | 3.895874 | 0.022929 |
| 8 Random | 99.78% | 0.22% | 2.133 | 3.909076 | 0.023006 |
| Full Assoc (Fifo) | 94.97% | 5.03% | 4.851 | 5.798175 | 0.034124 |
| Full Assoc (Lru) | 99.70% | 0.30% | 2.171 | 3.935470 | 0.023162 |
| Full Assoc (Random) | 99.78% | 0.22% | 2.142 | 3.915927 | 0.023047 |
## 💡 Core Concepts

### Cache Mapping strategies
- **Direct Mapped (1-way):** Fixed memory-to-line mapping; fast but high conflict.
- **Set-Associative (N-way):** Mapping to a set of N possible locations; balances speed and flexibility.
- **Fully Associative:** Flexible mapping to any line; eliminates conflict misses but complex hardware.

### Replacement Policies
- **LRU (Least Recently Used):** Evicts the line with the oldest access time; exploits temporal locality.
- **FIFO (First-In, First-Out):** Evicts the 'oldest' line regardless of access; prone to thrashing.
- **Random:** Evicts victims at random; simple, immune to pathological access patterns.

## 🛠️ Technical Specifications
- **Simulation:** gem5 SE (System-call Emulation), x86_64 ISA
- **Geometry:** 16kB Cache, 64-Byte Lines (Total 256 lines)
- **Address Decoding (Offset):** 6 bits for all configurations
- **Address Decoding (Index/Tag):** Variable (from 1-way: 8 index/50 tag bits to Full: 0 index/58 tag bits)
- **L1i Cache:** 16kB, 4-way associative (fixed across all runs)

## 🔍 Observations & Insights

### 1. The Associativity Paradox (8-Way vs Full-Assoc)
- Counter-intuitively, **8-way LRU** performs better than **Full-Assoc LRU**.
- This is due to the specific access pattern in `test.c` (Phase 5), which accesses 257 lines. In an 8-way cache, only one set (Set 0) experiences conflict misses and thrashing, while the other 31 sets remain unaffected. In a Fully Associative cache, *every* access to the 257th line can evict a line that is needed soon by *any* part of the program.

### 2. The FIFO Thrashing Anomaly
- **Fully Associative FIFO** experiences massive thrashing (5.03% miss rate).
- Because FIFO evicts the oldest line regardless of reuse, it enters a pathological state in cyclic access patterns where the working set is slightly larger than the cache. The line just evicted is the one needed next, creating a 'worst-case' scenario for cache performance.

### 3. Random Replacement Policy Efficiency
- The **Random** policy is surprisingly robust, often matching or even beating LRU at lower associativities.
- Random replacement avoids the pathological eviction patterns that can cripple FIFO or LRU in specific workloads, making it a viable low-complexity alternative for hardware implementation.

### 4. CPI & AMAT Correlation
- There is a strong linear correlation between **Average Memory Access Time (AMAT)** and **CPI**.
- Our best configuration (8-way LRU) achieved an AMAT of **2.11 cycles**, proving that high associativity with LRU can effectively hide memory latency for this workload.
