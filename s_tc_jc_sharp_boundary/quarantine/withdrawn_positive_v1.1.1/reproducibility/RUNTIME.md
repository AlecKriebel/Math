# Runtime and memory

Reference environment: Debian Linux, Python 3.13.5, NumPy 2.3.5, SymPy 1.14.0,
NetworkX 3.6.1, GCC 14.2.0, TeX Live 2025/dev, latexmk 4.86, biber 2.20.

Measured publication-regenerator costs in the distributed environment:

| Task | Wall time | Peak RSS |
|---|---:|---:|
| Primitive five-outgoing theta signatures | 34.65 s | 156 MB |
| Primitive six-outgoing theta signatures | 2 min 4.46 s | 569 MB |
| Directed theta join, five outgoing | 0.43 s | 18 MB |
| Directed theta join, six outgoing | 5.79 s | 350 MB |
| Independent directed review, five outgoing | 1.43 s | 15 MB |
| Independent directed review, six outgoing | 20.44 s | 275 MB |
| Each primitive cycle atlas | under 1.5 s | at most 124 MB |

The exact theorem release's default verifier normally completes in minutes.
The `--full-adversarial` mode additionally recomputes all 547 pointwise-cut
Bernstein expansions and may take substantially longer.  Complete measured
transcripts from this release are in `transcripts/`.

`verify_quick.sh` checks integrity, recompiles the paper, replays the exact
release in default mode, and validates all frozen publication certificates.
`verify_full.sh` performs the compositional full release check: it reruns the complete new structural rooting universe independently in Python and C++, and verifies every unchanged base statistical/atlas file against the preserved clean full-adversarial transcript. `verify_regenerate_all.sh` is the slower optional command that regenerates every large bounded signature stream, directed join, and relation universe from scratch.

## Automatic triangle theorem

The dependency-free Python census and the independent C++ census each complete in well under one second and use negligible memory relative to the atlas jobs. They enumerate 864 raw orientation attempts, 25 binary acyclic rooted presentations, seven symmetry orbits, and zero tree-child presentations.
