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

### 1. Effect of Associativity
- Increasing associativity generally reduces **conflict misses**. Moving from 1-way (Direct Mapped) to 8-way significantly improves performance.
- Full Associativity represents the theoretical limit for minimizing conflict misses for a given cache size.

### 2. Replacement Policy Comparison
- **LRU (Least Recently Used):** Typically performs best by exploiting temporal locality.
- **FIFO (First-In, First-Out):** A simpler policy that often performs slightly worse than LRU but better than Random.
- **Random:** Usually the worst-performing policy but requires the least hardware complexity.

### 3. Benchmark Characteristics (`test.c`)
- The benchmark includes loops specifically designed to stress the cache (Phases 1, 2, and 5).
- Phase 5 forces evictions by accessing 257 lines in a 256-line cache, making the replacement policy critical.
