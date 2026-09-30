# Research log

## 2026-09-30 07:03 UTC — source and prior-attempt gate

The exact original statement and normalization were recovered from Ohtsuki Section 2.4, pp.403–405. The target ranges over all classical knots and all diagrams, not only prime or torus knots. The invariant is additive, mirror-odd, integer-valued, and takes value 1 on the right trefoil. The original source also records the weaker Okuda bound with denominator 15.

No previous attempt, matching branch, or matching PR was found in the repository checks. The older imported report was unsourced triage and is not a proof certificate. Problem 10400032 asks the larger joint-range question and is related rather than identical.

Willerton’s 2001 preprint gives the normalization and sharp two-strand torus examples. Abe’s later primary thesis and published torus-knot paper address the torus subclass; that result does not settle the present full target. Current literature verification continues. No substantive proof attempt yet. Estimated completion toward a full new resolution: 0%.

## 2026-09-30 07:11 UTC — Attempt 1: tournament completion

A candidate all-diagram mechanism has emerged from the unbased Polyak–Viro formula (1994, Theorem 2). Its triangle pattern induces a directed cycle in the oriented chord-intersection graph; its path pattern induces a directed two-edge path. Completing missing graph edges by fair independent orientations makes each counted path cyclic with probability one half and preserves each counted triangle. Thus the unsigned diagram score appears bounded by the expected cyclic-triangle count. The usual tournament degree count has the desired sharp cubic upper bound. The arrow formula was calibrated against a separate exact Jones bracket state sum on six named braid families/examples and 53 fixed-seed classical braid closures. A numerical implementation issue involving negative integer powers of -1 was corrected to use an exact parity sign before those checks passed. No mathematical conclusion is based on floating-point arithmetic.

The full proof and exact pattern correspondence are being formalized before separate adversarial review. Historical novelty remains unknown. Best estimate of completion toward a valid full proof: 70%; this is a planning estimate, not a correctness probability.

## 2026-09-30 07:19 UTC — frozen candidate and source correction

The complete tournament argument is frozen for separate adversarial review. The final publication verifier passes 42,867 exact assertions with no numerical approximation. The central arrow-pattern graph correspondence and the treatment of signs and automorphism multiplicities are explicit in the candidate. The proof yields the requested universal bound and its even-crossing refinement. Estimated mathematical completion: 90% pending independent review; historical novelty remains unestablished.

A visual check of the original p403 confirms the older denominator-15 display, but that expression is incompatible with the same source’s small torus-knot examples. It is therefore recorded only as a source discrepancy and is not used as a theorem or proof input. The conjecture on p405 and the normalized Polyak–Viro formula are unaffected.
