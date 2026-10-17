# Pass 2: an admissible finite radial comparison and its exact information

E-6322, 2026-10-16. This note concerns full-class global minimizers of the frozen target. It derives a local quantitative barrier-mass inequality from actual comparison maps. It does not establish higher gradient integrability or a positive essential lower Jacobian bound.

## 1. Positive and barrier parts

For F=Dy, C=cof F and J=det F, set

P(F)=a|F|^6+b|C|^3+cJ^2,
B(F)=dJ^{-2}.

Thus W=P+B. P is homogeneous of degree six. Its right stress is

U_+(F)=F^T DP(F)
=6a|F|^4 F^T F+3b|C|(|C|^2 I-C^T C)+2cJ^2 I.

It satisfies

U_+ is positive semidefinite, tr U_+=6P, and 0<=n^T U_+ n<=6P for every unit vector n.

Positive semidefiniteness follows term by term; in particular, |C|^2 I-C^T C is positive semidefinite. These are pointwise algebraic facts, not extra regularity assumptions.

For a measurable set A, write P(A)=integral_A P(Dy) and B(A)=integral_A B(Dy).

## 2. A genuine finite comparison map

Fix concentric closed balls B_r(x0) contained in B_R(x0), with the closure of B_R contained in Omega, and 0<r<R. Write rho=|x-x0|, n=(x-x0)/rho, and

m=r^3/(R^3-r^3), ell=mR^3.

For sufficiently small |t|, define a radial map phi_t centered at x0 by the radius function

f_t(rho)=(1-t)^(1/3)rho,                 0<=rho<=r,
f_t(rho)=[(1+mt)rho^3-ell t]^(1/3),    r<rho<R,
f_t(rho)=rho,                           rho>=R.

The formulas match continuously at r and R. Their radial derivatives and tangential stretches are positive and uniformly bounded above and below for t in a sufficiently small interval around zero. Thus phi_t is an orientation-preserving bi-Lipschitz homeomorphism of R^3, fixes the complement of B_R, and maps Omega onto itself. Its derivative may jump on the two spheres; this is harmless for a finite comparison in the full Sobolev class.

Let A_t=Dphi_t and k_t=det A_t. Then

k_t=1-t on B_r,
k_t=1+mt on B_R minus B_r,
k_t=1 outside B_R.

Define y_t=y composed with phi_t^{-1}. This preserves the entire boundary trace. The Sobolev composition theorem for bi-Lipschitz changes of variables gives y_t in W^{1,6}, and

Dy_t(phi_t(x))=F(x)A_t(x)^{-1},
det Dy_t(phi_t(x))=J(x)/k_t(x)>0 a.e.

Because A_t, A_t^{-1}, k_t and k_t^{-1} are bounded, every term in I(y_t) is bounded by a constant times W(Dy). In particular, y_t is an actual member of the full A_g for each sufficiently small positive or negative t. Neither inverse Sobolev regularity nor injectivity of y is involved.

The exact change-of-variables formula is

I(y_t)=integral_Omega [k_t P(F A_t^{-1})+k_t^3 B(F)] dx.

Minimality applies to this finite expression before any differentiation is attempted.

## 3. Differentiation of the finite expression

On the core, k_t P(FA_t^{-1})=(1-t)^{-1}P and k_t^3 B=(1-t)^3 B. The derivative at zero is P-3B.

On the shell, put v(rho)=ell/rho^3-m. The derivative H=(d/dt)|_0 A_t has tangential eigenvalues -v/3 and radial eigenvalue m+2v/3, so

H=(m+v)n tensor n-(v/3)I,
tr H=m.

The derivative of the positive part is

L=mP-U_+:H
 =(m+2v)P-(m+v)n^T U_+ n.

The derivative of the barrier part is 3mB. Every derivative is dominated by a fixed multiple of P+B, with constants depending on r/R but not on F. Dominated convergence and two-sided minimality therefore yield the exact identity

0=P(B_r)-3B(B_r)
  +integral_{B_R minus B_r} [(m+2v)P-(m+v)n^T U_+ n+3mB] dx.

This argument also legitimizes the piecewise-Lipschitz test field directly; it does not rely on approximating it in a topology stronger than the available L^1 stress control.

## 4. Exact rearrangement and a quantitative barrier-mass estimate

Set s=(r/R)^3. The preceding identity rearranges to

B(B_r)=s B(B_R)+(1-s)P(B_r)/3
 + (1/3) integral_shell [2(r/rho)^3-s]P dx
 - (1/3) integral_shell (r/rho)^3 n^T U_+ n dx.

All terms are finite. Dropping the last, nonnegative, integral gives the new proved estimate

B(B_r)<=s B(B_R)+(1-s)P(B_r)/3
 + (1/3) integral_shell [2(r/rho)^3-s]P dx.       (A)

A simpler consequence is

B(B_r)<=s B(B_R)+P(B_r)/3
 +(2/3) integral_shell (r/rho)^3 P dx.           (B)

Let omega_3=|B_1|. After dividing by |B_r|,

average_{B_r} B <= average_{B_R} B
 + (1/3)average_{B_r} P
 + (2/(3 omega_3)) integral_shell P(x)/|x-x0|^3 dx.

In particular, if one independently knows P<=M on B_R, then

average_{B_r} B <= average_{B_R} B+M/3+2M log(R/r).

This logarithmic average growth is compatible with the pressure/BMO picture. It is not an L-infinity bound and does not supply the missing boundedness of P.

For every epsilon>0, the same estimate gives

|{J<epsilon} intersect B_r| <= epsilon^2 B(B_r)/d,

with B(B_r) estimated by (A) or (B). Nothing here forces this measure to be zero for any fixed epsilon.

## 5. Why the scalar inequality does not bootstrap positive energy

For any arbitrary nonnegative L^1 function P and any 0<c0<=1/3, put B=c0 P. Inequality (A) then holds for every concentric ball pair, without any extra integrability assumption: indeed,

B(B_r)-sB(B_R)
=c0[P(B_r)-sP(B_R)]
<=c0(1-s)P(B_r)
<=(1-s)P(B_r)/3,

and the shell integral in (A) is nonnegative. Thus (A) alone is compatible with P failing a given L^{1+delta} bound, or even failing every L^{1+delta} bound.

At the abstract stress level, B=P/3 and U_+=2P I even make the energy-momentum tensor zero and satisfy positive semidefiniteness and tr U_+=6P. These freely specified fields need not come from the actual constitutive law and a gradient; this is NOT a minimizer counterexample. It identifies the information discarded by the scalar estimate: a successful bootstrap must exploit further constitutive-gradient compatibility, not just these algebraic stress properties and the ball comparison inequality.

## 6. Boundary and conclusion

The comparison is an interior one because B_R is compactly contained in Omega. It remains available at points arbitrarily close to the boundary by shrinking R, but the reference average and potential then depend on that shrinking scale. No estimate uniform through the entire boundary follows by that observation.

A boundary analogue would need actual trace-fixing comparisons adapted to a boundary chart. Flattening the boundary introduces position-dependent factors in the energy, so the exact isotropic scaling identities cannot simply be copied without estimating the additional terms. A separate trace-fixing normal collar comparison, including curvature terms, is supplied in `BOUNDARY_COLLAR.md`; it yields an integral hole-filling estimate but no determinant lower bound.

Established in this pass: an explicit full-class admissible finite comparison and the exact identity and inequality above. Remaining gap: an estimate that improves P(Dy) beyond L^1, or uses additional constitutive structure to eliminate low-J sets. No resolution of E-6322 is claimed.
