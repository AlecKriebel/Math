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
| SAT solver | CaDiCaL 3.0.1, commit `c60730422e758ef1cebe7aeddf2dda31c996bf04` |
| CaDiCaL source archive SHA-256 | `2dccd6ecc1878348dd70194d51df6b69006bf86439b5b3c395a5c5dd8863201e` |
| CaDiCaL binary SHA-256 | `51c3c82b354f455c925fc60b37c701e8498afcf0f3bfab9a06e62149485df5f6` |
| Proof checker | DRAT-trim, commit/tag `2e5e29cb0019d5cfd547d4208dca1b3ec290349f` / `v05.22.2023` |
| DRAT-trim source archive SHA-256 | `2ac28cd9e38e050b4f78fbff0efd4a1aa2349d157aef08c9b1fb6c7139949108` |
| DRAT-trim binary SHA-256 | `31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb` |

The system already had a separate symbolic-computation process using one full
CPU core and about 1 GiB resident memory. Swap usage was about 8 GiB at the
start of this campaign. Consequently, exploratory runs begin single-threaded;
no more than two memory-heavy jobs may run concurrently.

No third-party Python graph or SAT package was present in the system Python at
launch. The trusted evaluators therefore use the standard library. The SAT
solver and its independently developed proof checker were subsequently pinned
and built locally by `tools/bootstrap_sat.sh`, using at most two compiler jobs.
A smoke test generated a proof for CaDiCaL's bundled unsatisfiable `ph4.cnf`;
DRAT-trim returned `s VERIFIED`. This checks the toolchain plumbing only, not
any campaign synthesis instance.
