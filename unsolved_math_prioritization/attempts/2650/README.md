# KOU-21.141: coherence of polycyclic pro-p amalgams

**ID 2650. Unresolved after 5/5 substantive attempts.**

Zalesskii's question asks whether a proper free pro-p amalgam of coherent
pro-p groups over a polycyclic subgroup is coherent. Generation,
subgroups, normal closures and presentations in these notes are in the
pro-p category. No full proof or counterexample is claimed.

The independently audited scoped results are in
[the corrected research package](reviewed/README.md):

- A finite-decomposition criterion with presentation bounds
- Coherence for virtually procyclic amalgamation
- A common polycyclic normal-kernel reduction, including normal and central
  edge special cases
- Proper two-generator examples with arbitrarily long reduced rank-two
  graphs, ruling out a rank-only uniform edge bound
- Two explicit failures of proposed infinite counterexample constructions

Known procyclic-edge and malnormal analytic-edge theorems are credited.
Historical novelty of the elementary deductions has not been established.
The higher-rank core-free general problem remains unresolved.

## Audit history and exact snapshots

The [full independent audit](reviewed/INDEPENDENT_AUDIT.md) retained the
scoped mathematical conclusions but identified a missing faithfulness
qualification in one source theorem application. The correction uses the
already established kernel and permanence lemmas. The
[narrow re-review](NARROW_REVIEW.md) gives PASS for that exact corrected
package, resolves the initial hold and retains the unsolved 5/5 status.
This is independent AI-assisted review, not external expert acceptance.

Both snapshots are preserved byte-for-byte:

- [Original author package](original/README.md)
- [Corrected, independently re-reviewed package](reviewed/README.md)
- [Exact original-to-corrected change map](reviewed/CHANGE_MAP.json)

Historical HOLD and pending-review fields inside those snapshots describe
their respective freeze dates. The current disposition is recorded in
[status.json](status.json) and the narrow review, without rewriting history.
The outer manifest binds the complete publication package and both reviews.

## Reproduce

From this directory, with Python 3 and its standard library:

    python verify_publication.py

The portable verifier checks every publication byte, both snapshot pins,
review bindings and the change map, then replays the controls in temporary
copies. Checks cover 128 chain cases, 15 finite lattice systems, 65,536
exponent-frontier subsets and 64 exponent-cover cases. These are finite
auxiliary checks; the universal arguments are written proofs and have not
been machine formalized.

Primary sources are linked in [SOURCE_GATE.md](reviewed/SOURCE_GATE.md).
The exact UnsolvedMath page returned HTTP 403; the pinned catalogue and
October 2026 Notebook p.198 supplied the verified identity. No source PDF,
screenshot, raw corpus, private correspondence or credentials are included.
