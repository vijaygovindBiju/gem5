# Cache Performance Analysis Summary

This report summarizes the performance of various data cache configurations (16kB) across different associativities and replacement policies.

## 📊 Summary Table

| Configuration | Execution Time (s) | D-Cache Miss Rate | D-Cache Misses | D-Cache Accesses | CPI |
|:---|:---:|:---:|:---:|:---:|:---:|
| 1 Fifo | 0.030148 | 3.43% | 145548 | 4241101 | 5.122588 |
| 1 Lru | 0.030148 | 3.43% | 145548 | 4241101 | 5.122588 |
| 1 Random | 0.030148 | 3.43% | 145548 | 4241101 | 5.122588 |
| 2 Fifo | 0.026485 | 1.79% | 75928 | 4241101 | 4.500055 |
| 2 Lru | 0.025379 | 1.29% | 54505 | 4241101 | 4.312176 |
| 2 Random | 0.025840 | 1.49% | 62992 | 4241101 | 4.390577 |
| 4 Fifo | 0.023952 | 0.69% | 29269 | 4241101 | 4.069676 |
| 4 Lru | 0.023467 | 0.46% | 19448 | 4241101 | 3.987402 |
| 4 Random | 0.023355 | 0.39% | 16742 | 4241101 | 3.968233 |
| 8 Fifo | 0.023744 | 0.55% | 23220 | 4241101 | 4.034377 |
| 8 Lru | 0.022929 | 0.19% | 7960 | 4241101 | 3.895874 |
| 8 Random | 0.023006 | 0.22% | 9273 | 4241101 | 3.909076 |
| Full Assoc (Fifo) | 0.034124 | 5.03% | 213391 | 4241101 | 5.798175 |
| Full Assoc (Lru) | 0.023162 | 0.30% | 12518 | 4241101 | 3.935470 |
| Full Assoc (Random) | 0.023047 | 0.22% | 9508 | 4241101 | 3.915927 |

## 🔍 Observations & Insights

### 1. The Associativity Paradox (8-Way vs Full-Assoc)
- Counter-intuitively, **8-way LRU** (0.19% miss rate) performs better than **Full-Assoc LRU** (0.30%).
- This is due to the specific access pattern in `test.c` (Phase 5), which accesses 257 lines. In an 8-way cache, only one set (Set 0) experiences conflict misses and thrashing, while the other 31 sets remain unaffected. In a Fully Associative cache, *every* access to the 257th line can evict a line that is needed soon by *any* part of the program.

### 2. The FIFO Thrashing Anomaly
- **Fully Associative FIFO** experiences massive thrashing (5.03% miss rate).
- Because FIFO evicts the oldest line regardless of reuse, it enters a pathological state in cyclic access patterns where the working set is slightly larger than the cache. The line just evicted is the one needed next, creating a 'worst-case' scenario for cache performance.

### 3. Random Replacement Policy Efficiency
- The **Random** policy is surprisingly robust, often matching or even beating LRU at lower associativities (e.g., 4-way Random @ 0.39% vs LRU @ 0.46%).
- Random replacement avoids the pathological eviction patterns that can cripple FIFO or LRU in specific workloads, making it a viable low-complexity alternative for hardware implementation.

### 4. CPI & Hardware Design Implications
- There is a clear **diminishing returns** curve. Moving from 1-way to 4-way provides the largest performance leap.
- The transition from 4-way to 8-way or Full-Assoc offers marginal gains at the cost of significantly increased hardware complexity (more comparators, higher power, and potentially higher hit latency).
