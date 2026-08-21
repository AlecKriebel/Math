# Hostile review checklist: marked fixed-linear \(\delta=1\)

Audit `MARKED_DELTA1_NOTE.md` without importing its branch conclusions.

## Normalization and exact-stratum scope

- Starting with \(P=pA_3,Q=pB_3\), prove that the marked common divisor
  \(p\) forces \(R=pS_2\).
- Justify the target normalization of the \(q^3\)-coefficients of
  \((A_3,B_3)\) to \((0,1)\), including all residual target freedom.
- Check that exact \(\delta=1\) forces the \(q^2\)-coefficient of \(S_2\)
  to be nonzero.
- Reconstruct the source shear and scaling that leave exactly
  \(S_2=q^2\) and \(S_2=p^2+q^2\).  Track the fixed divisor \(p\), and
  check that the target normalization can be restored afterward.

## Contact calculation

- Independently derive the minimal tangent
  \(N=(A_{3,q},B_{3,q},S_{2,q})\) from Hilbert--Burch, including
  uniqueness on exact \(\delta=1\).
- Recompute the signed curvature \(K_N\) and the criterion
  \(K_N\in\langle\alpha,\beta\rangle_{\mathbb C}\).
- On \(S_2=q^2\), verify the division-free endpoint argument:
  contact gives \(a_0b_1-a_1b_0=0\), and this makes \(q\) divide all
  three reduced multipliers.
- On \(S_2=p^2+q^2\), check the \(a_2=0\) contradiction without dividing
  by \(a_0\), then prove that the gauges \(a_2=1,b_2=0\) are legal on the
  complementary open.
- Reproduce equations (7)--(8), and verify the literal common factors
  \(pG_1\) and \(pG_2\) for every value of \(t\), including \(t=0\).
- Inject a sign error in the curvature, change one coefficient in (8),
  and delete the \(a_2=0\) leaf; require the independent suite to reject
  each mutation.

## Automorphism exit and wording

- When \(\kappa=0\), replay both \(E_6\) blocks that make every nonlinear
  term binary; do not invoke the stronger \(\delta=0\) statement without
  checking the exact-\(\delta=1\) nullities.
- Audit the plane-plus-shear exit and its use of the unconditional plane
  degree bound.
- The allowed conclusion is only the marked exact-\(\delta=1\) exclusion.
  The unmarked \(\delta=1\) component and every \(\delta\ge2\) component
  remain open here.
