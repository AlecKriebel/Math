# A genuinely multi-component mixed-moment comparison

E-6322, fifth and final shared pass, 16 October 2026.

## 1. The coupled endpoint theorem

Let y be a full-class global minimizer for the frozen benchmark. Let v belong to W^{1,6} with the same complete trace. At almost every point set

F=Dy, A=Dv, J=det F, j=det A,
M_1=cof F:A,  M_2=cof A:F.

Assume the three explicit coupled sign conditions

j>=0,  M_1>=0,  M_2>=0 almost everywhere.                 (1)

There is no rank-one restriction on A-F. The endpoint v may have infinite inverse-determinant energy. Then

integral M_1 J^{-3}<infinity,                             (2)

and, with H(F)=a|F|^6+b|cof F|^3+c(det F)^2,

2d integral M_1 J^{-3}
 <= integral DH(F):(A-F)+6d integral J^{-2}.              (3)

The full domain and full trace are retained. This is an actual consequence of the minimizer inequality for every endpoint satisfying (1), not a formal Euler test. It supplies a larger comparison class than the fixed-component or rank-one-connected theorem from pass 4.

It does not assert that a useful endpoint satisfying (1) exists for every minimizer. In particular, taking v=y gives M_1=3J and only the baseline inverse-square moment.

## 2. Exact determinant expansion makes the segment admissible

For 0<=t<1 put y_t=(1-t)y+tv. Multilinearity gives the cubic Bernstein expansion

J_t=det((1-t)F+tA)
=(1-t)^3J+t(1-t)^2M_1+t^2(1-t)M_2+t^3j.                (4)

Thus (1) implies J_t>=(1-t)^3J>0 almost everywhere, and

J_t^{-2}<=(1-t)^{-6}J^{-2}.                              (5)

The gradients remain in L^6, so all positive minor terms are integrable. The trace is unchanged. Consequently every y_t with t<1 is a genuine competitor, even if v itself has zero determinant on a set of positive measure.

No pointwise matrix field is being substituted for a compatible gradient: y_t is the displayed Sobolev map, and F,A are its actual endpoint gradients.

## 3. The one-sided derivative and reverse Fatou

The positive density has |DH(F)|<=C(a,b,c)|F|^5. Therefore

L=DH(F):(A-F)

belongs to L^1, and its integrated difference quotients converge to integral L by the bound C(|F|+|A|)^5|A-F|.

Let q_t=(J_t^{-2}-J^{-2})/t. Equation (5) gives, for 0<t<=1/2,

q_t <= [(1-t)^{-6}-1]J^{-2}/t <=126 J^{-2}.             (6)

The final numerical constant is the secant slope of the convex function (1-t)^{-6} at t=1/2. Pointwise differentiation of (4) gives

lim_{t down to 0} q_t
=-2J^{-3}(M_1-3J)
=6J^{-2}-2M_1J^{-3}.                                   (7)

Unlike the rank-one case, q_t need not be monotone: the determinant path is cubic, and the entire density need not be convex along this multi-component segment. Instead apply reverse Fatou using the integrable upper bound (6). If the moment (2) were infinite, equations (6)-(7) would imply

limsup_{t down to 0} integral q_t=-infinity.

The positive-density derivative is finite, so this would contradict [I(y_t)-I(y)]/t>=0. The mixed moment is therefore finite. Reverse Fatou and minimality then give exactly (3).

We have not claimed equality between the integral derivative and the integral of (7), or an unrestricted additive Euler equation.

## 4. Quantitative content and comparison with the earlier theorem

The right side is finite without any unknown stress norm. For example the elementary cofactor derivative bound |D(cof)(F)[R]|<=2|F||R| and the minor inequalities give

|DH(F)| <= C_H |F|^5,
C_H=6a+2b+2c/9.

Young's inequality yields the convenient bound

integral |DH(F):(A-F)|
 <= [C_H/(6a)] integral [H(A)+11H(F)].                   (8)

Thus (3) is a quantitative weighted inverse-Jacobian estimate in terms of finite endpoint energies and the original barrier integral.

For rank(A-F)<=1, the identities

M_1=2J+j,  M_2=J+2j

show that j>=0 automatically implies the two other signs in (1). Substituting M_1=2J+j into (3) cancels four copies of the original barrier term and recovers exactly

2d integral jJ^{-3} <= integral DH(F):(A-F)+2d integral J^{-2},

the pass-4 theorem. The extension genuinely permits full-rank changes: for y(x)=x, any v(x)=x+epsilon grad phi(x), with phi smooth and compactly supported and epsilon small enough that I+epsilon D^2 phi is positive definite, satisfies (1); D^2 phi can have rank three on an open set. Such endpoints are not rank-one-connected to y there.

If v=y outside a measurable set E, the unchanged terms cancel to give

2d integral_E M_1 J^{-3}
 <= integral_E DH(F):(A-F)+6d integral_E J^{-2}.          (9)

There is no general replacement of DH(F):(A-F) by H(A)-H(F) here. The positive density is polyconvex, not known to be convex along an arbitrary full matrix segment. That favorable rank-one inequality is deliberately not imported.

A lower bound M_1>=m_0>0 on a set gives inverse-cube integrability on that set via (3). A lower bound M_1>=m_0|cof F| gives integrability of the corresponding barrier-stress magnitude there. Such lower bounds are additional properties of the actual endpoint, not consequences of (1).

## 5. This coupled test bypasses the fixed-direction obstruction in one exact example

Consider the pass-4 radial example on B_1,

y(x)=s(r)x,  s=r^{1/2}[log(e/r)]^kappa,
1/6<kappa<=1/2,
q=3/2-kappa/log(e/r).

That map has finite energy and admits no globally uniformly positive same-trace repair in any single fixed target direction. Nevertheless the full endpoint v(x)=x meets all the coupled sign conditions: the eigenvalues of F are s,s,sq>0, and

j=1,
M_1=tr(cof F)=s^2(1+2q)>0,
M_2=tr F=s(2+q)>0.

Since J=s^3q,

M_1J^{-3}=s^{-7}(1+2q)/q^3.

Its radial integral is comparable to

integral_0 r^2s(r)^{-7}dr
=integral_0 r^{-3/2}[log(e/r)]^{-7kappa}dr=infinity.

Thus (2) gives a separate direct nonminimality certificate for that example. Indeed the right energy derivative along the coupled interpolation toward the identity is negative infinity. The finite-energy segment is explicitly admissible, so this is a real multi-component improvement over the unavailable one-direction repair.

The example was already known to be nonminimizing from affine uniqueness. This calculation is used to test the strength and legitimacy of the new method, not presented as a new benchmark counterexample.

## 6. The unresolved coupled-repair step

The full smooth extension G is always an available finite-energy endpoint, but its mixed determinants with Dy need not satisfy (1). The smooth compatible blending example from pass 4 has an interior diagonal gradient diag(-2,-1/2,1) against the identity endpoint; both mixed traces are negative there. Smooth trace data, positive endpoint determinants, and small total excess therefore do not establish the coupled signs.

Nor does pointwise replacement by a favorable matrix produce a deformation with that gradient. Enforcing the signs while matching the original trace is a differential compatibility problem. Fixed-distortion compositions are safe but do not directly remove a genuine gradient-integrability tail; unrestricted reference truncation retains the previously proved level ceiling.

No endpoint construction meeting the needed coupled signs and quantitative lower bounds was obtained for an arbitrary minimizer. Consequently (2)-(3) are rigorous new necessary conditions, not a proof of the full essential lower bound.
