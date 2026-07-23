# Environment audit

Audited 2026-07-23.

## Hardware and storage

- Computer: MacBook Pro (MacBookPro18,1)
- CPU: Apple M1 Pro, 10 cores (8 performance, 2 efficiency)
- Memory: 16 GB unified memory
- Integrated GPU: 16 cores; unused by the recorded experiments
- Architecture: arm64
- Storage at audit: 460 GiB volume, about 16 GiB available, 97% allocated

## Operating system and toolchain

- macOS 26.5.2, Darwin 25.5.0
- Python 3.14.6
- Apple clang 21.0.0
- Apple SDK 26.5
- Git 2.38.2
- GNU Make 3.81
- Node.js 22.16.0
- Go 1.25.6
- Docker 20.10.21 is present; no container image was used.

## Graph and solver audit

The default `python3` 3.14 environment has no queried graph, SAT, or numeric
packages. Alternate local Python interpreters have NumPy/SciPy/SymPy, but no
NetworkX, igraph, graph-tool, rustworkx, pynauty, PySAT, pycosat, OR-Tools,
z3, cvc5, or other queried graph/SAT packages.

No command-line installation was detected for Kissat, CaDiCaL, MiniSat,
Glucose, CryptoMiniSat, Lingeling, PicoSAT, z3, cvc5, Boolector, nauty/Traces,
bliss, drat-trim, LRAT checkers, GRAT, or CakeLPR. A command named `clasp` is
the Google Apps Script CLI, not the ASP/SAT solver.

Consequences:

- The verifier and local-search baseline are dependency-free C++17/Python.
- No third-party proof-producing SAT solver or DRAT/LRAT checker is available.
  The fixed-core experiments therefore use an in-repository deterministic
  DPLL solver that emits a complete exhaustive search tree, plus separately
  written checkers that replay every branch, cited unit step, and conflict
  against the original clauses. Those checked tree certificates support the
  narrowly scoped certified claims in `CLAIMS.md`; they are not yet a
  practical route to a global order-43 proof.
- With only about 16 GiB free, large CNFs and proof traces require an explicit
  storage estimate before launch.

## Measured kernel baseline

Command:

```sh
build/search43 --benchmark --n 43 --seed 20260723
```

Measured output:

- five-subsets: 962,598
- edge-to-subset incidence entries: 9,625,980
- precomputation: 0.020514 s
- 100 full exact recomputations: 0.232385 s (430.32/s)
- 100,000 exact incremental flip evaluations: 0.717463 s (139,380/s)
