# Pass 3: precise energy-moment thresholds for ordinary equilibrium

E-6322, 2026-10-16. These are conditional theorems for the actual full-class minimizer. The additional integrability hypotheses are not established by the baseline energy, and the conclusions do not assert Jacobian positivity uniformly away from zero.

## 1. Notation and available equations

Let y be a full-class minimizer, F=Dy, J=det F, w=W(F), Pi=DW(F), T=Pi F^T, and E=wI-F^T Pi. Let v be its genuine Sobolev a.e. inverse on D=G(Omega), H=Dv, K=det H.

The justified identities are div E=0 on Omega and, in the deformed domain,

div sigma=0,
sigma(z)=[T(F)/J] at x=v(z).

Initially E is L^1(Omega) and sigma is L^1(D). The latter follows from change of variables. The inverse ordinary stress is

S(z)=DV(H(z))=[J^{-1} E(F)F^T] at x=v(z).

These ordinary stress formulas are initially pointwise, not assertions of integrability.

## 2. Direct energy bounds on the stresses

For constants depending on the positive coefficients,

|Pi(F)|<=C[w^{5/6}+w^{11/6}].

Indeed the positive-power derivatives have degree five and are bounded by C|F|^5, while the barrier derivative is -2dJ^{-3}cof F. The latter is bounded by C w^{3/2}w^{1/3}=Cw^{11/6}.

Likewise,

integral_D |S| dz = integral_Omega |E F^T| dx
<=C integral_Omega w^{7/6} dx.

The equality is the exact stress transformation; the inequality uses |E|<=Cw and |F|<=Cw^{1/6}.

## 3. Ordinary inverse equilibrium from w in L^{7/6}

### Conditional theorem A

If w belongs to L^{7/6}(Omega), then S belongs to L^1(D) and

integral_D S:Dzeta dz=0 for every zeta in C_c^infinity(D;R^3).

Proof. The energy moment supplies F in L^7, and E in L^{7/6}. For a given zeta set eta=zeta composed with y. Then eta belongs to W^{1,7}(Omega), with

Deta=Dzeta(y)F.

It has zero boundary trace because y maps the boundary to partial D and zeta vanishes near partial D. In fact its support is compact in Omega by continuity of y on the closure. Density of compactly supported smooth fields in W_0^{1,7}, paired with E in L^{7/6}, extends div E=0 to eta. Thus

0=integral_Omega E:[Dzeta(y)F] dx
 =integral_Omega EF^T:Dzeta(y) dx
 =integral_D S:Dzeta dz.

The previously displayed bound justifies every integral. This derives the ordinary inverse weak Euler-Lagrange equation without assuming that arbitrary inverse additive perturbations are admissible, or that v minimizes V over an enlarged inverse class. QED.

By the accepted pressure estimate, the sufficient hypothesis Dy in L^7(Omega) already implies w in L^{7/6}(Omega), and hence this conclusion. The missing step is proving that gradient gain for the actual minimizer.

## 4. Actual inverse and Cauchy-stress moment bounds

Suppose w belongs to L^r(Omega), r>1. Change variables and use the energy bounds on the minors to obtain

integral_D |H|^t dz
=integral_Omega |cof F|^t J^{1-t} dx
<=C integral_Omega w^{(5t-3)/6} dx,

for t>=1. Hence H belongs to L^t with

t=(6r+3)/5.

Similarly,

integral_D |sigma|^q dz
=integral_Omega |T|^q J^{1-q} dx
<=C integral_Omega w^{(3q-1)/2} dx,

for q>=1, since |T|<=Cw and J^{-(q-1)}<=Cw^{(q-1)/2}. Thus sigma belongs to L^q with

q=(2r+1)/3.

Because v takes values in bounded Omega almost everywhere, the derivative estimate gives v in W^{1,t}(D), with the same full inverse trace.

## 5. Ordinary primal equilibrium from w in L^{11/6}

### Conditional theorem B

If w belongs to L^{11/6}(Omega), then Pi belongs to L^1(Omega) and

integral_Omega Pi:Dvarphi dx=0 for every varphi in C_c^infinity(Omega;R^3).

Proof. The direct pointwise bound in Section 2 gives integrability of Pi. Section 4 supplies

H in L^{14/5}(D), sigma in L^{14/9}(D).

These exponents are conjugate. Given varphi, set psi=varphi composed with v. The Sobolev chain rule gives

psi in W^{1,14/5}(D),
Dpsi=Dvarphi(v)H.

Its trace vanishes: the inverse trace is G^{-1} on partial D, while varphi vanishes on partial Omega. Hence psi belongs to W_0^{1,14/5}(D). Standard smooth-test density extends div sigma=0 to psi. Changing variables and contracting matrices gives

0=integral_D sigma:Dpsi dz
 =integral_Omega (Pi F^T):[Dvarphi F^{-1}] dx
 =integral_Omega Pi:Dvarphi dx.

Every pairing is justified by the stated conjugate moments. No lower bound on J and no admissibility of y+t varphi is assumed. QED.

By the accepted pressure estimate, Dy in L^{11}(Omega) implies w in L^{11/6}(Omega). Thus that additional gradient estimate would suffice to recover ordinary primal equilibrium.

For the general moment r, the duality above closes exactly when

1/[(6r+3)/5]+1/[(2r+1)/3]<=1,

which is equivalent to r>=11/6. This is the threshold of this energy-moment and unweighted Holder-duality route, not a theorem that no other argument can recover equilibrium below it.

## 6. Sharpness of the energy-only integrability thresholds

Use the pass-2 admissible anisotropic family on B_1:

y_alpha=(r^{-alpha}x_1,r^{-alpha}x_2,r^{5alpha}x_3),
0<alpha<1/2,
J=r^{3alpha}(1-alpha+6alpha n_3^2).

It has identity trace and finite target energy, with w comparable to r^{-6alpha}. It is not a minimizer.

For the primal ordinary stress,

Pi_{33}=-2d r^{-11alpha}
 (1-alpha+alpha n_3^2)/(1-alpha+6alpha n_3^2)^3
 +O(r^alpha).

The angular factor is bounded above and below by positive constants. Thus Pi is not L^1 when alpha>=3/11, while w is L^r when 6alpha r<3. For every r<11/6 one can choose 3/11<=alpha<min(1/2,1/(2r)). Consequently no energy-only assertion w in L^r implies Pi in L^1 can hold uniformly over the full admissible class for r<11/6.

The inverse ordinary-stress threshold is sharp as an energy-only integrability implication as well. Set a=b=c=d=1 and alpha=3/7. At n=e_3, writing q0=1+5alpha, the leading top diagonal entries of E have coefficient

-18+3/q0^2

times r^{-6alpha}, which is nonzero. On a fixed nearby angular cone, |EF^T| is bounded below by a positive constant times r^{-7alpha}. Therefore

integral_D |S| dz=integral_Omega |EF^T| dx=infinity

at alpha=3/7, whereas w belongs to every L^r with r<7/6. This does not contradict theorem A: the endpoint w in L^{7/6} fails for that example.

These are sharp integrability obstructions for arbitrary admissible maps, not counterexamples to ordinary equilibrium or determinant positivity for minimizers.

## 7. Exact remaining gap

The baseline yields only w in L^1. Neither the coupled finite identities nor the pass-2 scalar mass inequalities establish w in L^{7/6}, let alone L^{11/6}. The conditional results isolate concrete useful next estimates:

- Dy in L^7 would yield ordinary inverse equilibrium.
- Dy in L^{11} would yield ordinary primal equilibrium.

Neither conclusion alone is the E-6322 essential lower-Jacobian theorem. Further regularity or a direct positivity argument would still be needed. No bootstrap is claimed here.
