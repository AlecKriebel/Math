# Audit report for release 2.0.0

Date: 2026-08-09
Final status: **VERIFIED SHARPNESS THEOREM; POSITIVE CLASSIFICATION WITHDRAWN**

## Executive conclusion

The supplied omnibus auditor package did not contain a valid proof of the
claimed positive classification for standard strongly tree-child level-2 JC
networks.  That claim remains unresolved.  It has been removed from the
active paper, metadata, public page, and submission artifacts.

The maximal theorem supported by independent exact evidence is now packaged
as a standalone manuscript:

> For every `n >= 4`, two nonisomorphic and nonordinary-`T`-equivalent binary
> level-2 semi-directed networks in `W_TC \ S_TC` have open Jukes--Cantor
> model images sharing a regular relatively open region of full dimension
> `2n`.

This theorem is verified and submission-ready.  It is a sharpness result for
the full weakly tree-child class.  Because the pair also contains a triangle,
it does not resolve the triangle-free weakly tree-child subclass, and it says
nothing positive or negative about the still-open standard strongly
tree-child classification.

## Why the former positive release was withdrawn

Independent audits identified four load-bearing failures in the old release:

1. the claimed reciprocal-only bridge gauge was false; the correct
   full-incidence scaling kernel was not converted into a complete intrinsic
   local-to-global chart;
2. frozen local-atlas tables lacked an end-to-end topology-to-polynomial
   binding theorem and required compiler inputs were absent;
3. the seven-port verifiers certified only a downstream conditional map and
   still passed after most upstream census rows were deleted; and
4. arbitrary-subdivision and no-cross-blob-compensation steps remained
   conditional, while standard reduction and two-sub-blob conventions were
   mixed inconsistently.

No exact counterexample to the intended standard strongly tree-child theorem
was found.  Accordingly, its status is **UNRESOLVED**, not false.

## Evidence for the active theorem

The release includes two independent implementations.

- `reproducibility/verify_primary.py` reconstructs the displayed-tree JC maps
  from the rooted arc encodings and checks the six identities, exact common
  point, all 256 Fourier coordinates, and both rank-eight certificates.
- `reproducibility/independent/verify_sharpness.py` uses only the Python
  standard library and independently implements rooted-network validation,
  the locked narrow semi-directed reduction, mixed-graph isomorphism,
  displayed-tree enumeration, sparse polynomial arithmetic, quadratic-field
  arithmetic, rational interval bounds, automatic differentiation, and exact
  determinants.

The independent implementation regenerates the canonical certificate at
SHA-256
`38266537a7966d83bdb94c6fb90fa68f93fbd227b82579f1bf311005925366d7`.
It is byte-identical under `PYTHONHASHSEED=0`, `1`, and `987654`.

The all-`n` theorem is not inferred from a finite census.  The manuscript
proves a positive analytic inverse for cherry substitution and then applies
it inductively, repeatedly replacing labelled leaf 2 while retaining labelled
leaf 1 as the topology separator.

## Adversarial review disposition

The first final manuscript review found no P0 issue and identified three P1
and seven P2 corrections.  Those corrections tightened the cherry inverse,
scope, standard reduction, all-taxa construction, reconstruction references,
terminology, provenance, and comments.

The final rereview again found no mathematical defect.  Its HOLD concerned
only four release-engineering residues: a whitespace-sensitive scope check,
stale ZIPs, an obsolete sentence in a supporting review, and a stale nested
hash.  All four were corrected.  The final manifest was generated only after
the deterministic archives and public PDF were frozen.

The first clean-worktree replay then exposed one further packaging defect:
the manifest generator had included eleven ignored review screenshots under
`tmp/`, which are absent from a checkout.  Both manifest programs now exclude
that nonrelease cache; a regenerated manifest and a second clean-worktree
replay passed.

The complete review record is preserved in:

- `repair/reviews/SHARPNESS_GATE_REVIEW.md`;
- `repair/reviews/MANUSCRIPT_FINAL_REVIEW.md`;
- `repair/reviews/MANUSCRIPT_FINAL_REREVIEW.md`; and
- `repair/FINAL_RELEASE_AUDIT.md`.

## Reproduction

From the project directory, install the pinned requirements and run:

```sh
python3 reproducibility/verify_release.py
```

The driver first verifies every file against `MANIFEST.sha256`, then replays
both exact implementations and the scope contract.  The manuscript is built
deterministically with:

```sh
reproducibility/build_paper.sh
```

The submission directory contains the ten-page PDF, its canonical source ZIP,
and the independently replayed reproducibility ZIP.

## Submission recommendation

**Proceed with the sharpness manuscript after completing journal-specific
author metadata and formatting.**  Do not submit or cite the quarantined
positive-classification manuscript as an established result.
