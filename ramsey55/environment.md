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

## Isolated proof-producing SAT follow-up

The “not available” observations above describe the initial machine audit.
For the 2026-07-23 exact-completion cycle, a pinned proof-producing toolchain
was installed into isolated temporary directories rather than the default
Python environment:

- Python 3.11.8:
  `/opt/homebrew/opt/python@3.11/bin/python3.11`
- Python-SAT 1.9.dev7:
  `/tmp/ramsey55-pysat.4YSXId`
- `drat-trim` and `lrat-check` from commit
  `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`:
  `/tmp/ramsey55-drat-trim.x3nb3p/src/`
- Zstandard 1.5.7:
  `/opt/homebrew/bin/zstd`

The bootstrap operations were:

```sh
/opt/homebrew/opt/python@3.11/bin/python3.11 -m pip install \
  --target /tmp/ramsey55-pysat.4YSXId python-sat==1.9.dev7

git clone https://github.com/marijnheule/drat-trim.git \
  /tmp/ramsey55-drat-trim.x3nb3p/src
git -C /tmp/ramsey55-drat-trim.x3nb3p/src checkout \
  2e3b2dc0ecf938addbd779d42877b6ed69d9a985
make -C /tmp/ramsey55-drat-trim.x3nb3p/src
```

Pinned executable/source hashes:

```text
Python executable
831365631dac62f232a720858703d0b2ddca5eed33e0a51986cf06aac9d38bc0

pysat/solvers.py
253654d8efabae650a0d136ad2f2e6d30b57206b1fb70846c714197468a28f7e

PySAT pysolvers extension
e9828032a114da49429305e5afcf58db259034687a9c098c996da65e5e099ded

drat-trim
f58f63b0f76945d4c4c9ff6e87afaf870f579e67c0f7cca589492df8fc7ebd47

lrat-check
bd7eb8052623525814a0a37502b47f05375d9d9dfaf96ddc2fcd858958517cea

zstd
aff8169fb421bb925fb16c44a7e0143fa2c7a941dc45cce76b15062a2ce54917
```

These `/tmp` paths are ephemeral. The exact versions, commits, commands,
hashes, solver statistics, and checker transcripts are also embedded in the
retained result JSON files and
`certificates/residual_completion_workflow.report.md`.
