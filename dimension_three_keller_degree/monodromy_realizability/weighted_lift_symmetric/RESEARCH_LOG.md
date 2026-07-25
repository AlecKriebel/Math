# Research log

## 2026-07-25T19:47:04Z

- Reframed Gallagher's simple weighted-lift seed through the inverse
  polynomial \(T^d-T^2+UT+V\).
- Derived a uniform critical-value collision eliminant
  \[
  (d-2)r^d-dr^{d-1}+dr-(d-2).
  \]
  Its nonvanishing shows that the generic one-parameter polynomial is
  Morse.
- Used simple finite inertia, total ramification at infinity, and
  connectedness to obtain \(S_d\) for every \(d\ge3\).
- Exact SymPy branch-polynomial checks pass through \(d=10\).
- The single arithmetic specialization
  \(X^d-X^2-3X-5\) has PARI/GP Galois group \(S_d\) for every
  \(3\le d\le10\).
- Located Brink 2004, Theorem 13, which proves the polynomial Galois lemma in
  greater generality.  Demoted that lemma explicitly to prior art; the
  candidate contribution is now framed only as the Keller realization
  obtained by combining Brink with Gallagher and rational recovery.
- Observed that Brink's theorem does not depend on the fixed higher
  coefficients.  Gallagher's general inverse equation is
  \(\Phi(T)-PT+cQ\), so the same proof gives \(S_d\) for every admissible
  seed of degree \(d-1\), not only the displayed simple seed.  Strengthened
  the theorem to this family-wide classification.
- Began independent hostile proof and priority audits.  The result
  remains a candidate until those audits close.

## 2026-07-25T20:08:55Z

- The hostile mathematical audit passed the family-wide theorem, including
  the target-field change, exact root recovery, geometric base field, and
  composite degrees.
- Added the identity
  \[
  (\Phi(T)-PT+cQ)'|_{T=w}=p(w)-P=-c\gamma
  \]
  as a direct certificate that recovery denominators do not create generic
  roots.
- The independent priority audit found direct finite-range overlap:
  MathOverflow answer 513470 and its linked Note 19 proved \(S_d\) for
  Gallagher's canonical tower for \(3\le d\le13\) on 21 July 2026.
- Corrected the claim boundary.  The candidate contribution is only the
  uniform all-\(d\), all-admissible-seed Brink--Gallagher corollary.  The
  finite canonical rows and the abstract two-free-coefficient Galois
  theorem are prior art.
- Demoted number-field specializations to arithmetic consistency checks;
  they do not independently certify geometric monodromy.
