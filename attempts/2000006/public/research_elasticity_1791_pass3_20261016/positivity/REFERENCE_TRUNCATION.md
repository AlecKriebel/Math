# An unconditional admissible reference truncation, and its threshold ceiling

E-6322, shared pass 3, 16 October 2026.

## 1. Statement in the original comparison class

Fix one permitted smooth diffeomorphic extension G of the prescribed trace. Let y be an arbitrary full-class global minimizer and put w=y-G on Omega, extended by zero to R^3. This is a W^{1,6}(R^3) map because w has zero complete trace. Define the centered Hardy-Littlewood maximal function

f(x)=M(|Dw|)(x),

using the gradient of this zero extension. Set

m=min_{closure Omega} sigma_min(DG)>0,
M_0=max_{closure Omega}|DG|.

There is a finite constant C_Omega, depending only on the smooth domain, such that, for every

0<lambda<=lambda_0=m/(2C_Omega),

there is a full-class competitor z_lambda with

z_lambda=y almost everywhere on Omega minus E_lambda,
E_lambda={x in Omega:f(x)>lambda},
|Dz_lambda|<=M_0+m/2,
det Dz_lambda>=(m/2)^3 almost everywhere.               (1)

Consequently minimality implies the unconditional estimate

integral_{E_lambda} W(Dy) <= C_G |E_lambda|,
                  0<lambda<=lambda_0,                 (2)

where one explicit upper bound is

C_G=[a+b/(3sqrt(3))+c/27](M_0+m/2)^6+d(2/m)^6.          (3)

No injectivity, stress integrability, or extra regularity of y is assumed. The competitor belongs to the full frozen class directly. This construction supplies a genuine admissible truncation, unlike an arbitrary cutoff interpolation. Its important restriction is the upper ceiling on the truncation threshold.

## 2. Boundary-preserving Lipschitz extension of the good set

The following elementary Sobolev good-set facts suffice.

First, for any x,z where the displayed maximal functions are finite,

|w(x)-w(z)| <= C |x-z|[M(|Dw|)(x)+M(|Dw|)(z)].           (4)

One proof compares point values with averages on concentric balls, telescopes the averages using the L^1 Poincare inequality, and compares the two radius-|x-z| averages in a common larger ball. The continuous representative exists because 6>3, so the limiting averages give the point values. The vector estimate follows componentwise.

Second, for x in Omega,

|w(x)| <= C_Omega dist(x,Omega^c) M(|Dw|)(x).             (5)

To see this, write delta=dist(x,Omega^c). The smooth boundary gives uniform exterior measure density on small boundary balls, so a ball B_{C delta}(x) contains a fixed positive fraction outside Omega. On that portion w=0. Poincare and the zero portion bound the ball average by C delta M(|Dw|)(x); the same telescoping bound compares w(x) with that average. For delta above the fixed boundary-chart scale, enlarge the ball by a domain-dependent fixed factor until it contains a fixed exterior fraction. This preserves a constant depending only on the bounded smooth domain. Thus (5) holds also away from the boundary.

On the set

A_lambda=({x in Omega:M(|Dw|)(x)<=lambda}) union Omega^c,

the assigned data w, with value zero on Omega^c, are therefore C_Omega lambda-Lipschitz: use (4) for two interior good points, (5) for an interior/exterior pair, and zero for two exterior points.

Extend each scalar component by the McShane formula

(w_lambda)_i(x)=inf_{a in A_lambda} [w_i(a)+L|x-a|],

with L equal to a sufficiently large domain constant times lambda. The formula is finite, agrees with its data on A_lambda, and is L-Lipschitz, as follows immediately from the Lipschitz inequality for the data and the triangle inequality. Each component remains zero on the whole complement of Omega. Absorbing the factor sqrt(3) into C_Omega gives

||Dw_lambda||_infinity<=C_Omega lambda,
w_lambda=0 on Omega^c,
w_lambda=w on the interior good set.                    (6)

In particular the restriction has zero Sobolev trace. Sobolev locality also gives Dw_lambda=Dw almost everywhere where the two functions agree. This extension does not require the original deformation to be a homeomorphism.

## 3. Determinant control and the comparison inequality

Put z_lambda=G+w_lambda on Omega. For the allowed thresholds, ||Dw_lambda||_op<=m/2. Along the matrix segment DG+sDw_lambda, 0<=s<=1, the smallest singular value is at least m/2, so the determinant cannot change its positive sign. Therefore

det Dz_lambda >= (m/2)^3,
|Dz_lambda| <= M_0+m/2.

Together with the prescribed trace these bounds prove full-class admissibility and (1). The elementary minor bounds

|cof F|<=|F|^2/sqrt(3),   |det F|<=|F|^3/(3sqrt(3))

give W(Dz_lambda)<=C_G with (3). Outside E_lambda the map and gradient coincide with y, so canceling those equal energy integrals in I(y)<=I(z_lambda) proves (2).

The argument uses an actual finite competitor. It does not infer admissibility from the small measure of a negative-determinant set; the new determinant is uniformly positive everywhere in the almost-everywhere sense required by the target.

## 4. Why this does not produce the missing higher-integrability gain

A conventional high-level truncation or distribution-function proof needs useful inequalities as the level lambda tends to infinity. Here admissibility is ensured by keeping the entire new gradient within a fixed small operator-norm neighborhood of DG. That requires lambda<=lambda_0, not lambda>=lambda_0. The bound C_G in (2) applies only to these low-level bad sets.

For a small level, E_lambda can be nearly the whole domain, and (2) can carry no more information than a global energy comparison. In any event the present proof gives no analogue of (2) at arbitrarily high gradient thresholds, and it gives no control on the energy of arbitrary subsets of E_lambda. One cannot substitute E_lambda intersect {f>L} for E_lambda: the constructed competitor does not generally agree with y on the rest of E_lambda. Thus a distribution-function integration intended to reach L^{6+delta} lacks its high-level input.

The estimate is therefore a genuine unconditional admissible-comparison result with an explicit ceiling, not a reverse-Holder or epsilon-regularity theorem. It corrects an overly broad interpretation of the earlier obstruction: admissible additive truncations do exist near the fixed smooth reference; what remains unavailable is a controlled orientation-preserving high-level truncation or localized replacement that yields the needed gain.
