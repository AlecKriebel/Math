# Circular coloring of triangle-free subcubic planar graphs: partial results

Problem: OPG-401, catalog ID 3227. Research assessment: **unsolved, 5/5 turns**.
The full assertion that every finite simple triangle-free planar graph of maximum
 degree at most three has circular chromatic number at most 20/7 remains
unresolved by this work. No novelty or exhaustive current-literature claim is made.

## Contents and proved scope

- `EXTENSIONS.md`: exact path/tripod extension lemmas; a proof for triangle-free
  subcubic graphs with maximum average degree strictly below 12/5; the planar
  girth-at-least-12 corollary; and a separate fully-subdivided-core theorem.
- `PHASE_ATTEMPT.md`: failures of restricted phase approaches; the minimum
  real phase interval width is exactly nine for the dodecahedron over all
  enumerated even-factor/biparity choices, not for an arbitrary graph.
- `computation/`: seven explicit (20,7) SAT certificates; a complete 172-node
  (17,6) UNSAT tree for the same dodecahedron graph; independent checkers and
  negative controls; and `exact_dodecahedron_value.md`, the tight-cycle,
  rounding, and numerator-gap bridge proving the known benchmark value 20/7.
- `AUDIT.md`: mathematical review, computational cross-checks, and trust limits.
- `SOURCE_GATE.md`: public citations and precise source-inspection limits.
- `SCOPE.md`: inclusion/exclusion and interpretation boundaries.

The conjecture is stated by [Open Problem Garden](https://www.openproblemgarden.org/op/circular_chromatic_number_of_triangle_free_planar_graphs)
and [Xuding Zhu](https://www.math.nsysu.edu.tw/~zhu/open-problems/chic-k3free-planar.htm).
Ghebleh's 2007 thesis, *Theorems and Computations in Circular Colourings of
Graphs*, Conjecture 6.1, is an indexed primary appearance; the complete thesis
was not retrieved. The theoretical benchmark bridge is self-contained; the
[Hatami–Tusserkani article](https://arxiv.org/pdf/cs/0701007) supplies a literature
cross-check, not an assumed proof dependency.

## Reproduce without third-party packages

From this package directory, use ordinary Python 3, without `-O`:

    python replay_checks.py

This runs all standard-library checks, compares the generated local reduction
results with the stored JSON, checks the certificate hashes, and runs both
negative-control suites. It performs no network access and does not rewrite
certificates. See `REPLAY_RESULTS.json` for the recorded replay. The optional independent
audit passed (`AUDIT_REPLAY.txt`); both producers were also replayed in a
disposable copy with all eight certificate files byte-identical
(`PRODUCER_REPLAY.json`).

For the additional independently implemented graph-identification and
Floyd–Warshall audit, with NetworkX importable (tested with 3.7):

    python audit_check.py

Optional producer scripts are retained for transparency. `computation/run_search.py`
requires NetworkX; `computation/make_unsat_certificate.py` uses only the standard
library. These producers overwrite output artifacts and may change timings or
certificate bytes. Run them only in a disposable copy, not before verifying
this sealed package. The documented verification replay does not need them.

Verify every sealed payload file and byte count with:

    python verify_manifest.py

`MANIFEST.json` covers all package files except itself; its SHA-256 is returned
separately with the package receipt. The older `computation/SHA256SUMS` covers
only the eight explicit SAT/UNSAT certificate JSON files.
