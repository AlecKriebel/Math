# Research log

## 2026-07-27 PDT

- Formalized the color-restricted safe kernel directly from the one-guard
  definition in `probe.py`; no campaign evaluator or transition core is
  imported.
- Independently reproduced the named controls `K{eYptMJynEn`, `HCQebjw`,
  `FDzro`, `GFznc{` (canonical `G@~~fc`), and `IFjLBXiow`.
- Proved that a three-clique partition always supplies a surviving restricted
  kernel for the color containing the full-list target.
- Exhausted all 273,193 connected unlabeled graphs through order 9.  There
  are 623,732 static-full incidences overall; 24 lie in 15 equality graphs,
  but none is full in the greatest eternal 3-family.
- Audited only the existing local 56-graph MMV Table 9 catalog at orders
  10--11; no broad enumeration was run.  Of 581 greatest-family full-list
  incidences, 33 succeed and 548 fail.  MMV-021 is the first exact
  safe-kernel success with \(\theta=4\), while MMV-001 is the first failure.
- Final bounded run: 51.43 s wall time, 47.56 s user time, 0.46 s system
  time, 27,213,824 bytes maximum resident set size, no swaps.
- Final source SHA-256:
  `24ecc23a5b19890ac3f6101e40ab930e28415fe6a575cabaa157901150ec181a`;
  this matches the hash embedded in `result.json`.
- `result.json` SHA-256 at run completion:
  `8750e272a8d048ec85fdd44707342f039c8bf83cb6e7397ca0382b6a9d1feb4d`.

Outcome: the candidate equality-case lemma remains open.  The invariant is
noncircular in the wider \(\alpha=\gamma^\infty=3\) class, but a second
equality-specific mechanism is required to derive a clique partition.
