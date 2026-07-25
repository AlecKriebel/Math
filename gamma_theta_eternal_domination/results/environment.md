# Computational environment

Captured 2026-07-25 on campaign day 1.

| Item | Value |
|---|---|
| Host model | MacBookPro18,1 |
| CPU | Apple M1 Pro, 10 physical/logical cores |
| Physical memory | 17,179,869,184 bytes |
| System Python | CPython 3.14.6 at `/opt/homebrew/bin/python3` |
| Filesystem free at launch | approximately 11 GiB |
| nauty/Traces | 2.9.3 official source release |
| nauty archive SHA-256 | `9fc4edae04f88a0f5883985be3b39cf7f898fd6cc96e96b9ee25452743cc1b5b` |
| Build flags | `gcc -O3 -march=native`, arm64 |

The system already had a separate symbolic-computation process using one full
CPU core and about 1 GiB resident memory. Swap usage was about 8 GiB at the
start of this campaign. Consequently, exploratory runs begin single-threaded;
no more than two memory-heavy jobs may run concurrently.

No third-party Python graph or SAT package was present in the system Python at
launch. The trusted evaluators therefore use the standard library. Solver
dependencies will be pinned before synthesis begins.
