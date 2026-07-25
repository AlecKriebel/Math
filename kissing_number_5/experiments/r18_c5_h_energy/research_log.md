# Research log

## 2026-07-24 02:11 PDT

- Created an isolated work area for the five-point `C5` quartic-energy lemma.
- Recorded the angle substitution \(L=\pi/3\):
  cycle distances are \(\pi-LA_i\), with \(0\le A_i\le1\), and chord
  distances are \(L(1+C_i)\), with \(0\le C_i\le1\).
- Put \(F(x)=h(\cos(Lx))\) and
  \(P(x)=F(x)+F(1-x)-3/4\).  The trigonometric identity
  \[
  F(x)+F(1-x)+h(\cos(L(1+x)))=3/4
  \]
  gives the exact total-energy formula
  \[
  E=\sum_i F(A_i)-\sum_i P(C_i).
  \]
- If \(y=\cos((2\pi/3)(x-1/2))\), then
  \[
  P(x)=\frac{(1-y)(2y-1)}8\ge0
  \]
  on \([0,1]\).  Thus the chord term is an explicit nonnegative correction
  to the cycle-only energy.
- Previously obtained numerical optimization and 102-vertex evaluation of the
  angle metric polytope remain discovery evidence only, not a proof.

## 2026-07-24 02:42 PDT

- Independently audited and wrote a proof of the sharp auxiliary frame bound
  \(\lambda_{\max}(G)\le3\) on the closed `C5` sign cell.
- The proof switches signs according to a top Gram eigenvector and separates
  the resulting cyclic sign word into its \(0\)-, \(2\)-, and \(4\)-cut cases.
  It explicitly handles zero eigenvector coordinates and weak boundary
  inequalities.
- Added a small exact checker for the trigonometric coefficient identities,
  all 32 sign words, and the rational mass bookkeeping, plus normal,
  optimized-mode, and tamper tests.
- This frame bound is intentionally kept separate from the unproved quartic
  energy inequality.
- Discovery evidence for the metric-face adjacent-mass operation suggests the
  quantitative secant gap
  \[
  D\ge 2xy(a+c).
  \]
  This is now proved by a degree-18 rational-polynomial/Bernstein certificate.
  The exact verifier checks all 69,632 coefficients, a rational
  \(\pi\)-bracket, and the complete \(C^3\) approximation error.  It follows
  by adjacent merging that the target energy is at most \(3/2\) everywhere on
  the minimal metric face \(\sum A_i=3\).  This is not yet an off-face proof.
