# Full independent source/proof review request: 2525

Proposed original disposition: unsolved5/5, scoped reductions only. Please audit all five proofs, the exact original statement, the source-credit limits and every frozen control. No sixth author search or final publication before the full review.

## Source paths and numbering

SOURCE_MANIFEST.json binds six PDFs; TURN_5_SOURCE_MANIFEST.json adds Rosendal, for seven in total.
- October2026 Kourovka21st edition: printed/PDF179, Problem21.16, visually checked. No target solution marker or updates-only annotation.
- Bergman arXivmath/0401304: definitions(3),(4), preceding proof and Question9, pp4–5; positive-cone warning Lemma11 p6. The published BLMS paper has different page numbers.
- Maltcev thesis chapter2 pp21–28: group/semigroup distinction, cofinality and strong-cofinality. Do not certify its brief Khelif assertion as an independently verified construction.
- Khelif CRMath2006 pp377–380: full announcement read; the missing detailed counterexample construction is not a proof dependency.
- Jarnevic–Osin–Oyakawa arXiv2206.10712 introduction: Corollary1.6 and the following narrower countable-CB open question, reported with historical scope.
- Rosendal author manuscript: definitions p4, Theorem3.6 and full Proposition3.9 compact2-Bergman proof pp8–9. Earlier arXiv numbering differs. Classical analytic-set Baire regularity is explicit and credited.

## Main scrutiny points

Turn1: finite inverse-cost equivalence needs CB for all generating sets, not merely finite symmetric diameter of S; the canonical symmetric-core closures need not themselves be CB. Check the no-finite-supplement conclusion and bounded-order quantifiers.

Turn2: positive Schreier telescoping for a possibly nonnormal finite-index subgroup, right-coset conventions and inverse-representative costs; the strong-kernel lemma must bound the ambient length, rather than assuming S intersect N generates N. General MB extensions remain unproved.

Turn3: general finite-extension factor-set normal form, exact saturation length inequalities, both directions of the finite-semigroup-action CB/MB characterizations, and the true algebraic positive generation of the infinite-dihedral example. It is not itself CB. Read the additive control-description clarification.

Turn4: normal generation must be finite and bounded normal width is obtained by CB; conjugacy invariance or a uniform substitute is necessary for positive costs. Inverse-producing relations use a fixed finite family of conjugators and a common length bound.

Turn5: coordinate-word choice and padding in the Cartesian formula, compactness in the closed profinite formula, dense versus algebraic generation of Z_2, and the positive-product Baire proof using B_n B_n rather than a difference set. Analytic and word-ball Baire hypotheses are not part of the original and cannot be discarded. No finite matrix or residue calculation replaces these arguments.

## Replay

Run `python REPLAY_ALL.py`, optionally `--sources /path/to/sources`. Standard library only. It checks every final/historical binding and reproduces all five JSON receipts byte-for-byte. The recommended verdict must remain scoped even if every proof passes; no target example or universal equivalence proof is claimed.
