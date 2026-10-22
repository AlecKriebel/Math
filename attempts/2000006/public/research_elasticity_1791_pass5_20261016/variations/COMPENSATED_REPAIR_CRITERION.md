# Final pass: a quantitative compensated determinant-repair criterion

E-6322, 2026-10-16. This is a proved conditional comparison theorem and an explicit admissible construction. It is not a proof of the frozen positivity target: the uniform repair-cost hypothesis in Section 3 has not been obtained for arbitrary minimizers.

## 1. Exact inverse baseline and admissible endpoint paths

Let y be a full-class minimizer, v its actual almost-everywhere Sobolev inverse on D=G(Omega), H=Dv, K=det H, and C=cof H. The accepted inverse theorem gives

H=(Dy composed with v)^{-1},
v in W^{1,9/5}(D), C in L^{9/4}(D), K in L^3(D),
integral_D K=|Omega|.

Write

V(H)=X(H)+dK^3,
X(H)=a|C|^6/K^5+b|H|^3/K^2+c/K.

Suppose an endpoint u in W^{1,9/5}(D) has the same full inverse boundary condition and, writing H_e=Du, C_e=cof H_e and K_e=det H_e, satisfies

rank(H_e-H)<=1,
|H_e|<=M|H|,
|C_e|<=M|C|,
0<=K_e<=MK

for some finite M>=1. In addition, require an established mechanism placing every segment v_t=(1-t)v+tu, 0<=t<1, in the exact inverse comparison class. Two valid mechanisms are:

- a compact W^{1,9/4} difference u-v, followed by the accepted compact-addition theorem;
- the actual triangular material construction of Section 4, whose inverse equivalence is explicit even if u-v has only its natural W^{1,9/5} regularity.

More general accepted graph transformations may also establish membership when their hypotheses apply. Membership is not inferred solely from a natural-exponent Sobolev difference.

All rank-one minors are affine along the segment. Therefore

K_t=(1-t)K+tK_e >=(1-t)K,
V(H_t)<=M^6(1-t)^{-5}V(H).

The whole one-sided segment has finite energy, even if the endpoint itself has zero determinant and infinite energy. Differentiation at zero is justified by the relative bounds, which dominate the derivative by an integrable multiple of V(H). Minimality yields

3d integral_D K^2(K-K_e) <= R(u;v),                 (1)

where the signed positive-energy first cost is

R(u;v)=integral_D DX(H):(H_e-H).

This derivative notation means the derivative of X along the rank-one segment; explicitly, with Delta H=H_e-H, Delta C=C_e-C and Delta K=K_e-K,

DX(H):Delta H
 =6a|C|^4 C:Delta C/K^5
  +3b|H| H:Delta H/K^2
  -(5a|C|^6/K^5+2b|H|^3/K^2+c/K) Delta K/K.

Every term is integrable under the relative bounds. No ordinary inverse Piola integrability is being assumed.

The determinant mass is conserved also at the potentially degenerate endpoint. Indeed, for any fixed 0<t<1, exact inverse membership gives integral K_t=|Omega|=integral K. Affinity then gives integral K_e=integral K.

## 2. Compensation on a low-determinant recipient set

Assume the endpoint determinant change has disjoint donor and recipient sets A,B:

q=K-K_e>=0 on A,
p=K_e-K>=0 on B,
K_e=K elsewhere.

Assume the transferred determinant mass is nonzero. Conservation gives

m=integral_A q=integral_B p>0.

If K>=lambda on A and K<=kappa on B, then (1) implies the exact estimate

3d (lambda^2-kappa^2) m <= R(u;v).                (2)

Proof: the left side of (1), divided by 3d, is

integral_A K^2 q - integral_B K^2 p
 >=lambda^2 integral_A q-kappa^2 integral_B p
 =(lambda^2-kappa^2)m.

This estimate makes the compensation cost explicit. The coefficient is 3d because the inverse barrier is dK^3. Neither the endpoint's finite energy nor a pointwise inequality K_e<=K everywhere is required. The latter would in fact be incompatible with nonzero compact determinant reduction and conservation.

There is a more flexible weighted formulation, useful because a measurable high-K set need not contain any open set on which a smooth repair can be supported. Put q=(K-K_e)_+ and p=(K_e-K)_+ on all of D. With their common nonzero mass m,

3d [integral_D K^2 q-integral_D K^2 p] <=R(u;v).  (2a)

Thus the support assumptions can be replaced by the two moment conditions

integral_D K^2 q >=lambda^2 m,
integral_D K^2 p <=kappa^2 m.

The same conclusion (2) follows. If the donor lower bound loses epsilon*m and the recipient upper bound gains epsilon*m, the coefficient becomes lambda^2-kappa^2-2epsilon. This records exactly what a smooth approximation to a measurable level-set repair must control; smooth support inside the level set is not presumed.

## 3. A sufficient repair theorem that would close E-6322

Here are the full quantifiers needed for an actual conclusion.

Suppose there are constants kappa>0 and C_0>=0, depending on the particular minimizer and permitted data but independent of lambda, with this property:

For every lambda>kappa for which |{K>lambda}|>0, there is an endpoint satisfying Section 1 and donor/recipient conditions satisfying Section 2, with

A contained in {K>lambda},
B contained in {K<=kappa},
m>0,
R(u;v)<=C_0 m.

The exact support assumptions may instead be replaced by the weighted moment conditions after (2a). The relative bound M may depend on lambda; it only supplies legitimate differentiation for that endpoint. The cost C_0 and recipient threshold kappa must be uniform.

Then

K<=sqrt(kappa^2+C_0/(3d)) almost everywhere on D.  (3)

Otherwise choose lambda between the displayed bound and the essential supremum of K. The assumed repair has m>0 and contradicts (2). Since J(x)=1/K(y(x)) almost everywhere and the area formula transfers null sets, (3) gives the sought whole-domain primal bound

J>=1/sqrt(kappa^2+C_0/(3d)) almost everywhere on Omega.

This is a conditional theorem, not an assertion that its repair hypotheses hold. The requirement is a controlled signed positive-energy cost per unit determinant mass transported from high K to a fixed low-K region. Baseline finite energy supplies neither this cost bound nor a construction of the corresponding level-set repairs.

A recipient region of positive measure is available at a fixed finite threshold without any regularity theorem. Since integral_D K=|Omega|, choosing kappa=2|Omega|/|D| gives |{K<=kappa}|>=|D|/2 by Markov's inequality. What remains unproved is a compatible finite-energy transport to that region with the required uniform cost, not the bare existence of some low-K region.

The estimate also gives a necessary cost statement without assuming a repair family: every particular legitimate repair moving mass from K>=lambda to K<=kappa must pay at least 3d(lambda^2-kappa^2) per unit mass in its positive-energy first variation.

## 4. An actual volume-compensated finite-energy construction

Let Q=I times S be an open rectangular box compactly contained in Omega, with I=(alpha,beta). Choose h in C_c^infinity(Q) such that

h>=-1,
integral_alpha^beta h(s,x') ds=0 for every x' in S.

Set

f(x_1,x')=integral_alpha^{x_1} h(s,x') ds,
xi=e_1 f,
phi_t(x)=x+t xi(x), 0<=t<1,

and extend f by zero outside Q. The fiberwise zero integral and compact support of h make f smooth and compactly supported in Q. Moreover

Dphi_t=I+t e_1 tensor Df,
k_t=det Dphi_t=1+t h >=1-t>0.

Each fiber map x_1 -> x_1+t f(x_1,x') is strictly increasing, fixes both ends, and maps I onto I. Thus phi_t is an orientation-preserving smooth diffeomorphism of Omega onto itself, equal to the identity outside Q and on the whole boundary. Its inverse is Lipschitz for each fixed t<1.

The primal map y_t=y composed with phi_t^{-1} is therefore a full-class finite-energy competitor. Its actual inverse is

v_t=phi_t composed with v=v+t xi composed with v.

This proves comparison membership directly; it does not require the inverse difference to belong to W^{1,9/4}.

Put A_t=Dphi_t and F=Dy, J=det F, C_F=cof F. Exact change of variables gives

I(y_t)=integral_Omega [
 a k_t |F-(t/k_t)(Fe_1) tensor Df|^6
 +b k_t^{-2}|C_F+t(C_F Df) tensor e_1|^3
 +cJ^2/k_t+dJ^{-2} k_t^3 ].                       (4)

For each fixed t<1 all matrix multipliers are bounded, so (4) is finite by the baseline energy. At t=1 the endpoint phi_1 may collapse portions of fibers; it is not claimed to be an admitted endpoint. Nevertheless its derivative gives the rank-one endpoint of Section 1:

H_e=Dphi_1(v)H,
K_e=(1+h(v))K.

With L=||Df||_infinity, one can take M=1+2L, since

|Dphi_1|_operator<=1+L,
|cof Dphi_1|_operator<=1+2L,
0<=1+h<=1+L.

Let P(F)=a|F|^6+b|cof F|^3+cJ^2 and U_+(F)=F^T DP(F). Then U_+ is positive semidefinite, trace U_+=6P, and

E_+=P I-U_+,
|E_+|<= (sqrt(3)+6)P <8P.

The inverse positive-energy first cost has the exact primal expression

R(u;v)=integral_Omega E_+(F):Dxi
       <=8 integral_Omega P(F)|Df|.              (5)

For source donor and recipient sets where h has the appropriate signs, transported mass is

m=integral_source-donor (-h) dx
 =integral_source-recipient h dx.

The factor K in inverse transferred mass cancels J in the area formula. If the donor additionally lies where J<=1/lambda and the recipient where J>=1/kappa, formulas (2) and (5) give the genuine estimate

3d(lambda^2-kappa^2)m <=8 integral_Omega P(F)|Df|. (6)

Thus admissible compensated compressions do exist for prescribed smooth fiber-compatible h. The unresolved step is producing such h that detects every relevant low-J level set while uniformly controlling the right side per transferred mass. Neither measurable level sets nor their fiber integrals have transverse derivative bounds in the stated full class.

## 5. Final status

This pass supplies an exact quantitative terminal comparison lemma, an actual finite-energy volume-compensated construction, and a precise missing estimate. The criterion repackages safe inner stationarity and does not add an independent equilibrium equation. It does not supply the uniform level-set repair family of Section 3. The companion note shows why determinant amplitude and total baseline energy alone do not control the cost of the triangular construction.

All conclusions apply to the full original class and all boundary components. No topological homeomorphism assumption, unproved inverse derivative, ordinary stress integrability, or positive finite-amplitude interval has been silently used.
