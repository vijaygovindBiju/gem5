# Cache Performance Analysis with gem5

An empirical computer-architecture study using **gem5** to evaluate how cache associativity and replacement policies affect CPU performance.

## Overview

The project investigates a 16 KiB data cache using controlled memory-access workloads. It compares direct-mapped, 2-way, 4-way, and 8-way set-associative caches together with LRU and FIFO replacement policies.

The goal is to connect cache-design decisions with measurable system metrics such as hit rate, AMAT, miss rate, and CPI.

## Experimental Configuration

| Parameter | Configuration |
|---|---|
| Cache size | 16 KiB |
| Cache line size | 64 bytes |
| Cache lines | 256 |
| Associativity | 1, 2, 4, 8-way |
| Replacement | LRU, FIFO |
| CPU model | x86 TimingSimpleCPU |
| gem5 mode | System-Call Emulation (SE) |

## Key Findings

- Moving from direct-mapped to 2-way associativity produced the largest improvement for the tested workload.
- LRU consistently performed better than FIFO in the evaluated configurations.
- 4-way LRU provided a strong balance between hit rate and associativity for this workload.
- The tested LRU configuration reduced CPI substantially as associativity increased.

> Results are workload-specific and should be interpreted as an experimental study rather than a universal cache-design rule.

## Workload

`test.c` generates memory-access patterns designed to stress cache behavior, including:

- **Conflict stress** using addresses mapped to the same cache set.
- **Replacement stress** by accessing more cache lines than the cache can hold simultaneously.

## Repository Contents

```text
index.html                 Interactive results dashboard
graph.html                 Comparative performance charts
direct.html                Direct-mapped analysis
2way.html                  2-way analysis
4way.html                  4-way analysis
8way.html                  8-way analysis
results.json               Raw simulation results
PERFORMANCE_SUMMARY.md     Technical performance summary
test.c                     Benchmark workload
```

## What This Project Demonstrates

- CPU cache organization and associativity
- Cache replacement policies
- Performance measurement and interpretation
- gem5 simulation methodology
- Experimental comparison of architecture configurations
- Presenting simulation data through visualizations

## References

- Binkert et al., *The gem5 Simulator*, ACM SIGARCH Computer Architecture News.
- Lowe-Power et al., *The gem5 Simulator: Version 20.0+*.
- Hennessy & Patterson, *Computer Architecture: A Quantitative Approach*.
- Hill & Smith, *Evaluating Associativity in CPU Caches*.

## License

Academic and educational project.
