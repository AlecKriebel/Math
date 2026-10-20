# Ádám’s arc-reversal conjecture: finite-certificate audit

**Disposition: already disproved by Carsten Thomassen (2023), not a new disproof.**

This authored package reviews and independently checks one finite instance of the construction in Carsten Thomassen, *Ádám’s conjecture*, Journal of Combinatorial Theory, Series B **161** (2023), 15–20, Theorem 1, [DOI: 10.1016/j.jctb.2023.01.005](https://doi.org/10.1016/j.jctb.2023.01.005). Its catalog target is row 1819, ID 3264, OPG-46432, the unrestricted directed-cycle arc-reversal question. Row numbering is a workflow locator, not a mathematical identifier.

## Result and scope

The published theorem gives counterexamples among strongly 2-connected, self-reverse, simple oriented graphs. This package certifies the parameters **d = 64, k = 24**, giving **1,530 vertices and 80,520 arcs**. Reversing any one arc does not decrease the number of simple directed cycles, counted up to cyclic rotation.

- Exterior arc reversals strictly increase the count in this instance: an exact integer lower bound for the created cycles exceeds the exact maximum destroyed count.
- Interior arc reversals satisfy a non-strict inequality by an injective cycle transformation. Some interior reversals preserve the count. There is no claim of strict increase for every arc.
- There is no minimality or smallest-counterexample claim.
- These are not tournaments. The tournament restriction is a separate question and is not resolved by this construction or this audit. The package makes no assertion that a current comprehensive search establishes that variant's status.
- The identically named circulant-isomorphism conjecture is not the target.
- The large graph's cycle count is computed symbolically using exact integers, exhaustive enumeration of a small base's contracted trails, and proved gadget formulas. It is **not** obtained by brute-force enumeration of all large-graph cycles.
- The full large graph is explicitly materialized only for structural checks: graph size, orientation, reverse isomorphism, and strong connectivity after every single-vertex deletion.
- The computations supplement the mathematical reduction and published proof; they are not a proof-assistant formalization.

## Contents

- `REVIEW.md`: authored mathematical reconstruction, counting identities, formulas, and finite certificate argument.
- `AUDIT.md`: separate authored audit of the reduction, counting multiplicities, and structural checks.
- `certificate.json`: exact finite certificate, including the positive exterior margin. Its ratio is explicitly an approximation and is not used for the strict inequality.
- `check_counts.py`: first standard-library implementation, using base-arc trail search.
- `independent_audit.py`: independently implemented verifier, using two-step transitions between unexpanded vertices; it does not import the first implementation.
- `counts.json`: saved small-base enumeration and contracted-trail coefficients.
- `small_crosschecks.json`: direct enumeration of three small expanded graphs compared with the symbolic formula.
- `independent_audit.json`: second implementation's exact results, local-gadget checks, and full-graph structural checks.
- `reproduce.py`: portable replay harness; compares all four JSON outputs with fresh computations.
- `REPLAY.txt`: transcript from the packaging replay.
- `SOURCE_PROVENANCE.md`: public bibliographic links and retrieval/inspection metadata only.
- `MANIFEST.json`: byte counts and SHA-256 hashes for every payload file other than itself.

## Reproduction

Use Python 3.8 or newer with only its standard library. Assertions must be enabled; do not use `-O` or `-OO`. No network connection, downloaded manuscript, credentials, private files, or third-party Python packages are needed.

From the package directory:

```sh
python3 reproduce.py
```

The same command works with an absolute path from another directory. The harness runs the first implementation's base counts, certificate, and small explicit-graph tests, then runs the separate second implementation in a fresh process. It requires exact saved-output agreement and a zero exit status. Runtime is machine-dependent because the small-graph tests enumerate millions of cycles and the structural test checks all 1,530 vertex deletions.

For the independent check alone:

```sh
python3 independent_audit.py
```

The first implementation alone prints base counts when run as `python3 check_counts.py`; `reproduce.py` also invokes its certificate and small-expansion functions. The replay is read-only apart from ordinary Python bytecode caches; set `PYTHONDONTWRITEBYTECODE=1` to suppress those caches. The manifest excludes caches and itself, avoiding self-referential hashing. A matching manifest establishes file integrity, not mathematical correctness.

## Publication boundaries

This package contains authored review/audit/code/test outputs and public verification metadata only. It intentionally excludes third-party source PDFs and extracted text, catalog copies or datasets, private coordination files, and workflow status files. No queue file is included or edited. Preparing this package does not itself publish anything externally.
