# Reviewer correction to Proposition 4

**Problem:** 2301039 / AMR-022-1039, rank 564.  
**Date:** 4 October 2026 UTC.  
**Disposition:** the corrected scoped packet passes review; the original problem remains **unsolved, 5/5**.

This correction is required whenever the frozen author packet is published or reused. It supersedes only the displayed estimate and its explanation in `PROOF.md`, Proposition 4, lines 94–99. The theorem and every subsequent conclusion are unchanged. The author packet has not been edited.

The frozen author `SHA256SUMS` has SHA-256

    27fa158bea7288368c1e1b5b275f72b4e78ca7166bfda923c9ab90e77da41eae

and its `PROOF.md` has SHA-256

    3f4b852db08bf2f361cec2c4139cefc2c6ea954567566a98a186c3761839e236

## Defect

The displayed sub-divisor estimate omits an origin-cancellation correction. Under the packet's convention, an order-k zero at zero contributes k log r to its integrated counting function, which is negative for 0<r<1. Therefore simply removing a zero at the origin need not decrease the integrated counting function.

For example, take g(z)=z and h(z)=2z. Then f=g/h=1/2, after removal of the common zero. For 1/2<r<1,

    T(r,f)=0,
    m(r,g)+m(r,h)-log 2 = log r < 0.

Thus the displayed inequality in the frozen proof is literally false, even arbitrarily close to the boundary. The next sentence in that proof already acknowledges that an O(1) correction is needed. The issue is a missing term in the display, rather than a false bounded-characteristic theorem.

## Corrected statement and proof

Let g,h be bounded holomorphic functions in D, with h not identically zero, and let f=g/h be the meromorphic quotient after cancellation. Write

    h(z)=c z^k+O(z^(k+1)),  c≠0,  k≥0,

and let p≥0 be the pole order of f at zero, with p=0 if f is holomorphic there. Then p≤k. For every 0<r<1 the corrected estimate is

    T(r,g/h)
      ≤ m(r,g)+m(r,1/h)+N(r,0,h)+(k-p) log(1/r)
      = m(r,g)+m(r,h)-log|c|+(k-p) log(1/r).       (C1)

At each nonzero point a with |a|<r, the pole multiplicity of f is at most the zero multiplicity of h. Its counting weight log(r/|a|) is nonnegative, so these contributions may be compared term by term. At zero the two contributions are p log r and k log r. Consequently

    N(r,∞,f) ≤ N(r,0,h)+(p-k) log r
               = N(r,0,h)+(k-p) log(1/r).

Also, the pointwise product inequality gives

    m(r,g/h) ≤ m(r,g)+m(r,1/h).

Finally, Jensen's formula, with the same origin convention, gives

    m(r,1/h)+N(r,0,h)=m(r,h)-log|c|.

Adding these relations proves (C1). Circular means through zeros or poles are understood using their integrable logarithmic singularities; equivalently the identities extend by continuity in r.

For r≥1/2 the correction is between 0 and k log 2. Both proximity functions on the right of (C1) are uniformly bounded because g and h are bounded. A lower bound is T(r,f)≥p log r≥-p log 2. Thus T(r,f)=O(1) and alpha(f)=0. In fact the correction term tends to zero as r tends to one. Every rational function is a quotient of two polynomials, both bounded on D, so the rational-function corollary still follows.

For the counterexample above k=1 and p=0; the added term is log(1/r), and the corrected right-hand side is exactly zero. No correction to Propositions 1–3, Theorem 5, or the modular obstruction is needed as a consequence of this issue.

## Publication gate

The PASS verdict applies only to the frozen packet accompanied by this correction and the separate audit. It is not a verdict that the uncorrected displayed estimate is valid. Keep this correction visible alongside the author proof, and preserve the source limitations and **unsolved, 5/5** disposition.
