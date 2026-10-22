# Subcritical profiles with a simple lowest weight and dense positive set

16 October 2026. This final-pass addendum narrows the remaining conditional tangent class. It is not a regularity theorem for arbitrary minimizers and does not resolve E-6322.

## Statement

Use the same full-class minimizer, interior point, weighted annular rescaling and strong W^{1,infinity} convergence as in `DEGENERATE_TANGENT_OBSTRUCTIONS.md`. Let the limiting profile U_i=r^{alpha_i}phi_i(theta) have C^2 angular data, and suppose

    0<m=alpha_1<alpha_2<=alpha_3,
    s=alpha_1+alpha_2+alpha_3>3,
    s+3m<6.

Assume J_U=det DU is not identically zero and its positive set is dense in the annulus. Such a limiting profile is impossible.

Nonnegativity J_U>=0 follows from the essential uniform gradient convergence and original determinant positivity. For a continuous nonnegative angular determinant, density of the positive set is equivalent to the zero set having empty interior.

## 1. Scalar leading equation on positive patches

Set H(F)=a|F|^6+b|cof F|^3+c(det F)^2 and L_r=diag(r^{alpha_i-m}). The exact strain-normalized density is

    r^{-6(m-1)} W(diag(r^{alpha_i-1})P)
      = H(L_rP)+d r^{2(6-s-3m)}(det P)^{-2}.       (1.1)

Here the barrier coefficient tends to zero. The lowest weight is simple, so L_r tends to the projection onto row 1 and

    H(L_rP) -> a|p_1|^6

in C^1 on bounded matrix sets. On every compact positive-J patch, the same rescaled component variations and dominated weak passage used in the adjacent theorem therefore give

    div(|grad U_1|^4 grad U_1)=0.                  (1.2)

Since U is C^2 on the annulus, the scalar residual in (1.2) is continuous throughout it. The positive set is dense, so the residual vanishes throughout the annulus, including its determinant-zero set. Exact homogeneity extends (1.2) to the whole punctured space.

A positive-J patch also forces m>1/2 by the shrinking-annulus strain bound. The assumed inequalities s>3 and s+3m<6 give m<1. Thus

    1/2<m<1.

## 2. Homogeneous scalar identity

Write U_1=r^m phi(theta) and

    A_phi=(m^2 phi^2+|grad_S phi|^2)^2.

The scalar spherical equation and integration against phi give

    integral_{S^2} A_phi |grad_S phi|^2
       =m(5m-3) integral_{S^2} A_phi phi^2.        (2.1)

If 1/2<m<3/5, this forces phi=0, contradicting a nontrivial determinant. At m=3/5, it forces phi to be constant. The critical case needs care: a positive-degree argument cannot simply be imported for a degenerate profile. The following exact integral replaces it.

## 3. Critical exponent: a zero total angular determinant

Suppose phi_1=c is constant. If c=0, J_U vanishes identically. Otherwise, at r=1,

    grad U_1=cm theta,
    grad U_i=alpha_i phi_i theta+grad_S phi_i  (i=2,3).

Consequently the angular determinant is

    j(theta)=cm theta dot (grad_S phi_2 cross grad_S phi_3).

With the outward orientation on S^2,

    integral_{S^2} j d sigma
      =cm integral_{S^2} dphi_2 wedge dphi_3
      =cm integral_{S^2} d(phi_2 dphi_3)
      =0.                                        (3.1)

The last equality is Stokes' theorem on the closed sphere. But j is continuous, nonnegative and nontrivial, so its integral is strictly positive. This contradiction excludes m=3/5 without any assumption about an isolated zero or a regular target-axis preimage.

## 4. Above the critical exponent: removable scalar equation

If 3/5<m<1, U_1 belongs to W^{1,6} across the puncture because m>1/2. Its scalar stress is O(r^{5m-5}). Testing the punctured equation with a cutoff that removes B_r incurs an error bounded by

    C r^{5m-3} -> 0.

Hence U_1 is weakly 6-harmonic across zero. Scalar interior gradient regularity then makes grad U_1 bounded near zero. A nonzero degree-m homogeneous C^1 function with m<1 instead has an unbounded gradient there. This contradiction completes the proof.

The regularity input is the scalar corollary on printed p.222 of K. Uhlenbeck, *Regularity for a class of non-linear elliptic systems*, Acta Mathematica 138 (1977), 219-240, with its parameter p=4. The original statement and its parameter match were visually inspected in pass 3; the proof of the full external theorem was not re-proved. DOI: https://doi.org/10.1007/BF02392316 . Its role is solely regularity of the scalar weak 6-harmonic limit, not regularity of the elasticity minimizer.

## 5. Resulting narrow remaining class

Combine this addendum with the final balanced/superbalanced obstruction. For an assumed strong W^{1,infinity} weighted annular tangent with C^2 angular data, positive weights and s>3, any nontrivial nonnegative determinant must lie in the subcritical range s+3m<6 and must satisfy at least one of:

- the lowest weight is repeated, alpha_1=alpha_2;
- the angular determinant is identically zero on a nonempty open angular region.

In addition, a leading determinant that vanishes identically remains unexcluded in every scaling range. These are necessary residual alternatives, not constructions, stationarity certificates, or minimizer existence statements. Lower regularity, absent or weaker tangent convergence, non-power asymptotics, and boundary degeneration are outside this conditional classification. The separate critical-axis family calculation rejects one explicit repeated-lowest-weight family, including subcritical members, but supplies no theorem for the full repeated-weight system.

No actual full-class global minimizing counterexample was obtained in the five passes.
