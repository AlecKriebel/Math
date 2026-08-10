# Research Log

## 2026-08-10 04:40:24 PDT

Created isolated review effort `reviews/zero_sum_descriptor_cleanroom/`.
Read `primary/hard_cover_compiler.py`, `primary/atlas_compiler.py`,
`primary/jc_tensor.py`, and the quarantined
`descriptor_cache_scope_failure/schema3_n3` graph stream as source text/data
only.  No primary or prior-review modules were imported.

Checkpoint estimate: 35% complete.  The active hard-cover source declares
quartet-width complement normalization and a descriptor cache keyed by
selected port count plus exact rooted graph id.  The atlas source intentionally
uses raw rooted selected-side masks.

## 2026-08-10 04:40:24 PDT

Reconstructed the preserved quarantine failure from graph encodings.  The
same mixed-code rooted graph ids
`513afdd7dd8826c2bba2eaff47af1d37bacf98fd3a2906de825bf5705a70f2a2`
and
`83fbeab153b433dea88528707b25a74898a924b90b1eff000c5a7c10257c8dd8`
have different raw chunk-5 descriptors and invariant-50 pullbacks, reproducing
the README hashes `e53478...` and `070141...`.  Their complement-normalized
descriptors and normalized pullbacks agree.

Checkpoint estimate: 70% complete.  Remaining work is packaging the independent
verifier, mutation tests, certificates, and final review text.

## 2026-08-10 04:45:10 PDT

Implemented and ran `cleanroom_verifier.py` through `verify_all.sh`.  The
verifier passed, generated deterministic JSON certificates, rejected all five
required mutations, and recorded the release verdicts in
`certificates/manifest.json`.

Checkpoint estimate: 100% complete for this review goal.  Residual risk is
limited to future primary changes invalidating the inspected source-text
markers, which would make this verifier fail closed.

## 2026-08-10 05:00:00 PDT — adversarial harness correction

An adversarial reread found two weaknesses in the first verifier, without
changing its substantive verdict.  First, the noncomplement-separation loop
compared the full `Z_2 x Z_2` sums, whereas JC distinguishes only zero from
nonzero.  Second, the quarantine regression trusted the stored mixed-code hash
instead of independently reducing and canonicalizing the two mixed graphs.

Corrected both points.  The verifier now checks the JC zero/nonzero indicator
for every noncomplement mask pair, independently suppresses the root and
brute-force canonicalizes labelled mixed graphs, and treats the stored mixed
hash only as regression metadata.  It also AST-binds the active source
semantics, proves the positive product map using an exact rational global
section, checks root-arc factors on all quartets of both actual reticulate
quarantine graphs, regenerates every corresponding JC coordinate pullback, and
rejects direct source mutations.

The bounded-atlas question was closed explicitly: raw rooted descriptors are
not canonical on the standard semi-directed quotient, but graph-specific
zero/nonzero/strict-sign classification is exact through the surjective
submersion `(x_left,x_right)->x_left*x_right`.  No atlas regeneration is
required for this convention.  Overall review status changed to
`VERIFIED_AFTER_CORRECTION` to preserve the audit trail.

## 2026-08-10 05:17:03 PDT — independent adversarial release review

A separately launched read-only reviewer independently reproduced the core
zero-sum, product-section, graph-reduction, and quarantine-regression checks.
Its initial verdict was `ACCEPT_WITH_CORRECTIONS`: the mathematical conclusions
survived, but source/report hashes were stale after concurrent edits, the AST
checker accepted a normalization hidden under `if False`, and the quarantined
graphs did not actually contain a root arc entering a reticulation.

Hardened the package without editing primary code.  Verification is now
check-only and compares regenerated in-memory bytes with every stored
certificate and the manifest; `--regenerate` is explicit.  Reachability-aware
AST inspection rejects literal-dead declarations and a corresponding mutation.
Added a valid LSA-rooted strongly tree-child quartet fixture with a root arc
entering a reticulation, its pendant-root relocation, independent standard
mixed reductions, both switching cases `(3,12)` and `(15,0)`, all 64 zero-sum
assignments per switching, all 15 coordinate pullbacks, and parent-flip
invariance.

## 2026-08-10 05:29:22 PDT — preserved `if 0` call-site failure

The final narrow reviewer produced an exact bypass of the intermediate source
checker: correct `cached_deck` graph-ID calls placed under `if 0` masked live
calls changed to mixed-code arguments.  The reviewer correctly returned
`REJECT` for that intermediate harness; the active primary source remained
correct.

Corrected and preserved the failure.  Literal truth values are now evaluated
uniformly, and the call-site checker requires exactly two live calls in their
structural source and target positions with the matching graph and graph-ID
arguments.  Added the exact `if 0` decoy mutation to the permanent mutation
certificate.  The regenerated package and check-only wrapper pass with all
requested and adversarial mutations rejected.

## 2026-08-10 05:31:40 PDT — final scoped acceptance

A fresh read-only reviewer checked the corrected `if 0` regression, exact two
live graph-ID call-site bindings, first-class invariant-input hashes, and the
check-only wrapper.  It found no blocker and returned `ACCEPT`.  This is a
scoped gate acceptance only, not a verdict on the full landmark theorem.
