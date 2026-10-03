# A compact domino game without a periodic minimizer

**Problem:** 30005528 / OWR-13750333-009  
**Date:** 3 October 2026  
**Outcome:** Complete counterexample to the abstract compact-alphabet question as printed, subject to independent review. This is not a result about the more restrictive interval-packing problem.

Let α=√2, let Σ=S¹×[0,1], and put

\[
F(z,t)=(e^{2\pi i(\alpha+t)}z,t),\qquad
T=\{[x,F(x)]:x\in\Sigma\},\qquad s(z,t)=1+t.
\]

The alphabet is compact and connected, the tiles form a closed set, and F is a homeomorphism. A legal sequence starting at height t stays there, so its average size is exactly 1+t. The minimum 1 is attained on the bottom circle t=0. Every orbit there is aperiodic because α is irrational.

There are nevertheless densely many periodic starting points: an orbit at height t is periodic exactly when α+t is rational. All those heights are strictly positive. Periodic average sizes approach 1 but never attain it.

## Files

- [Complete proof](PROOF.md)
- [Source and scope check](SOURCE_GATE.md)
- [Research and verification record](RESEARCH_LOG.md)
- [Exact arithmetic checks](checks/verify_rotation_family.py)
- [Recorded check output](checks/verification_results.json)

Run the finite checks with:

    python3 checks/verify_rotation_family.py

The proof is exact and independent of computation. The script checks finite algebraic instances; it cannot replace the all-period irrationality argument.

The construction uses elementary circle rotations. No historical-priority, first-resolution, or novel-method claim is made. The primary source is Felipe Gonçalves's Question 1 on p.1254 of [Oberwolfach Report 22/2023](https://ems.press/content/serial-article-files/47016).
