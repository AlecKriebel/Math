# Pass 3: exact certification of coupled variations and weighted cores

E-6322, 2026-10-16. The fixed density, full admissible class, positive coefficient family and whole-boundary conclusion remain unchanged. This report independently checks the pass's new mathematical claims. It does not establish the missing regularity or a minimizing counterexample.

## 1. Inverse density, stress orientations and coupled transformations

Write F=Dy, J=det F, P=DW(F), and use

E=W I−F^T P,   T=P F^T.

For the actual almost-everywhere inverse, write H=Dv=F^(−1), K=det H=J^(−1). The inverse density is

V(H)=K W(H^(−1))
=a|cof H|^6/K^5+b|H|^3/K^2+c/K+dK^3.

Each of the first two terms is a convex perspective in the independent minor variables: K f(C/K) for f(C)=a|C|^6, and K g(H/K) for g(H)=b|H|^3. The remaining scalar terms are convex for K>0. Thus V is polyconvex. Minimizing b X^3/K^2+dK^3 over K gives a constant times X^(9/5), and minimizing a Z^6/K^5+dK^3 gives a constant times Z^(9/4). To obtain one summed coercivity inequality, split dK^3 into three positive portions, reserving one to control K^3 itself.

These facts do not justify a direct method on an unrestricted low-exponent inverse class. For the exact inverse class of the original full admissible class, compactness can instead be transported from the primal side: bounded inverse energy gives bounded primal W^{1,6}; the primal maps converge uniformly along a subsequence, and their actual inverses converge almost everywhere after weak W^{1,9/5} compactness. Passing in y_j(v_j(X))=X identifies the limit inverse. An interior X cannot have v(X) on the primal boundary, since the fixed trace maps that boundary onto the target boundary. This uses the previously verified almost-everywhere inverse theorem; it is not a claim that a smooth-diffeomorphism subclass is closed.

### 1.1 Exact derivative

The identities dK=K tr(F dH) and dF=−F(dH)F give

S:=DV(H)=K[W F^T−F^T P F^T]=K E F^T.

Consequently,

S H^T=K E,
H^T S=K(W I−T),
V I−H^T S=K T.

The change of variables dX=J dx cancels K. Thus inverse outer composition stationarity is precisely primal inner stationarity, and inverse inner stationarity is precisely primal outer stationarity. There is no extra independent first-order equation merely from writing the same system in inverse coordinates.

### 1.2 Coupled finite transformation

For material and target diffeomorphisms phi and Psi, put A=Dphi and L=DPsi. The finite map

y_tilde=Psi composed with y composed with phi^(−1)

has almost-everywhere inverse

v_tilde=phi composed with v composed with Psi^(−1),

and the exact energy identity is

I(y_tilde)=integral_Omega det A(x) W(L(y(x))F(x)A(x)^(−1)) dx.

The identity is independent of any unproved additive Euler equation. Trace-fixing and admissibility of the chosen diffeomorphisms remain required.

For constant infinitesimal matrices M,N, the mixed derivative of

f(s,t)=det(I+tM)W((I+sN)F(I+tM)^(−1))

at zero is

f_st=tr(M) P:(NF)−D^2W(F)[NF,FM]−P:(NFM).

This is a pointwise algebraic identity. Using it as an integrated second variation additionally requires the appropriate differentiability and integrable-domination argument.

## 2. Sharp energy thresholds for ordinary equilibrium

Safe composition identities do not initially imply ordinary additive equilibrium. The variations lane supplies two conditional upgrades, and their exponent calculations and changes of variables check as follows.

### 2.1 Ordinary inverse equilibrium at the energy exponent 7/6

Suppose the minimizer additionally satisfies W(Dy) in L^(7/6). The energy controls |F|^6, while |E|<=C W. Therefore

integral_target |S| dX
=integral_Omega |E F^T| dx
<=C integral_Omega W^(7/6) dx<infinity.

For zeta smooth and compactly supported in the target, eta=zeta composed with y is in W_0^{1,7}(Omega). The inner equation with E in L^(7/6) extends to this test by density. The contraction

E:[D zeta(y)F]=(E F^T):D zeta(y)

then gives the ordinary inverse weak equation integral S:D zeta=0.

The global pressure estimate from earlier passes shows that Dy in L^7 suffices for W(Dy) in L^(7/6). This conclusion depends on minimizer stationarity, not merely on the positive-power energy.

#### Sharpness for energy-only stress integrability

Use the already sealed admissible power family

y_alpha=(r^(−alpha)x1,r^(−alpha)x2,r^(5alpha)x3)

with unit coefficients and alpha=3/7. It is not a minimizer. On the positive third axis set q=1+5alpha. The leading coefficients are

positive energy P_+=9r^(−6alpha)+lower-order terms,
(U_+)11=27r^(−6alpha)+lower-order terms,
B=q^(−2)r^(−6alpha).

Hence E11 has nonzero coefficient −18+3/q^2 and (E F^T)11 has order r^(−7alpha). By continuity of the angular coefficient this lower bound holds on an angular cone, not merely on an axis. At alpha=3/7 its integral diverges logarithmically, while W belongs to every L^r with r<7/6. Therefore no smaller energy moment uniformly guarantees inverse-stress integrability over the full admissible class.

### 2.2 Ordinary primal equilibrium at the energy exponent 11/6

Assume W(Dy) in L^r for r>1. For t>=1, the actual inverse derivative satisfies

integral_target |H|^t dX
=integral_Omega |cof F|^t J^(1−t) dx
<=C integral_Omega W^((5t−3)/6) dx.

Thus one may take t=(6r+3)/5. For the Cauchy stress sigma=(P F^T/J) composed with v, the stress-growth bound |P F^T|<=C W gives

integral_target |sigma|^q dX
<=C integral_Omega W^((3q−1)/2) dx,

so one may take q=(2r+1)/3. The test psi=varphi composed with v, for varphi compactly supported in Omega, is in W_0^{1,t} of the target. Duality with sigma requires t>=q'. Algebraically this is equivalent to

12r^2−16r−11>=0,

or r>=11/6. At the endpoint,

t=14/5,   q=14/9,   t=q'.

The exact contraction is

(P F^T):[D varphi F^(−1)]=P:D varphi.

Consequently testing ordinary target stress equilibrium with psi and changing variables gives integral P:D varphi=0. The inverse trace and Sobolev chain rule used here are supplied by the actual inverse baseline, rather than assumed for a merely formal inverse matrix.

Also, directly,

|P|<=C[W^(5/6)+W^(11/6)],

so P is integrable at this threshold. The earlier pressure estimate shows that Dy in L^11 suffices for W(Dy) in L^(11/6).

#### Sharpness for energy-only Piola integrability

For the same anisotropic power family, the barrier contribution to P33 is exactly

−2d r^(−11alpha)
 (1−alpha+alpha n3^2)/(1−alpha+6alpha n3^2)^3,

and the positive contribution is O(r^alpha). The angular coefficient is uniformly nonzero for the relevant alpha. Thus P is not integrable if alpha>=3/11, while W^r is integrable if alpha<1/(2r). For every 1<=r<11/6 these inequalities admit a choice of alpha, with alpha<1/2 as required for finite baseline energy. This proves sharpness of the 11/6 energy-only threshold. These competitors remain nonminimizing.

## 3. Relative barrier identity and quantitative stress anisotropy

For positive J,j, the exact relative barrier identity is

J^(−2)−j^(−2)+2j^(−3)(J−j)
=(J−j)^2(2J+j)/(j^3J^2).

In particular the relative barrier remainder is nonnegative, with its full singular coefficient visible. Using it in a global comparison still requires an admissible comparison and control of the remaining minor terms.

Let C=F^T F, let its eigenvalues be x1,x2,x3>0, and put

S0=x1+x2+x3,   T0=x1x2+x1x3+x2x3,
H(F)=a S0^3+b T0^(3/2)+cJ^2,
U=F^T DH(F).

In the same eigenbasis,

U_i=6a S0^2 xi+3b sqrt(T0)xi(S0−xi)+2cJ^2.

For distinct indices i,j,k,

U_i−U_j=(xi−xj)[6aS0^2+3b sqrt(T0)xk].

Since sum_{i<j}(zi−zj)^2=3 sum_i(zi−average z)^2, one obtains the coordinate-invariant estimate

|dev U|>=6a S0^2 |dev C|.

### 3.1 A determinant/anisotropy consequence

Put D0=|dev C|. The tracefree cubic identity gives

J^2=S0^3/27−S0 D0^2/6+det(dev C),

and the sharp tracefree inequality is

|det(dev C)|<=D0^3/(3sqrt(6)).

Equality in the latter is attained by deviations proportional to (−2,1,1). Therefore, with

tau=|dev U|/(6a S0^3),

one has D0/S0<=tau and, whenever tau<1/sqrt(6),

J^2>=S0^3[1/27−tau^2/6−tau^3/(3sqrt(6))]
   =S0^3(1−sqrt(6)tau)(2+sqrt(6)tau)^2/108>0.

This bounds the determinant relative to the gradient scale when the stress is sufficiently isotropic. It does not bound that gradient scale away from zero. No uncontrolled conversion of this algebraic bound into a spatial regularity estimate is asserted.

### 3.2 Exact conformal subclass

If a finite-energy inner-stationary map satisfies F^T F=lambda^2 I almost everywhere, then, with A0=27a+3sqrt(3)b+c,

H=A0 lambda^6,   U=2H I,
E=(3d lambda^(−6)−A0 lambda^6)I.

The inner equation makes the scalar coefficient distributionally constant on the connected domain. The function lambda ->3d lambda^(−6)−A0 lambda^6 is strictly decreasing on (0,infinity), so lambda, and hence J=lambda^3, is a positive constant almost everywhere. This proves the determinant conclusion for that exact subclass without a regularity or rigidity theorem. It does not extend to approximate conformality without additional estimates.

### 3.3 Exact Legendre–Hadamard condition numbers at an isotropic matrix

At F=tI, t>0, let A=u tensor v be a rank-one direction with |u||v|=1 and z=u dot v. Direct differentiation gives

D^2W(tI)[A,A]
=(54a+3sqrt(3)b)t^4
 +[(72a+7sqrt(3)b+2c)t^4+6d t^(−8)]z^2.

Thus the exact minimum over unit rank-one directions is the shear value

mu(t)=(54a+3sqrt(3)b)t^4,

and the exact maximum is the longitudinal value

Lambda(t)=(126a+10sqrt(3)b+2c)t^4+6d t^(−8).

The ellipticity ratio is Lambda(t)/mu(t), in particular at least

[6d/(54a+3sqrt(3)b)]t^(−12).

Therefore rank-one positivity does not give a uniform positive ellipticity constant or a uniform condition number as the isotropic determinant tends to zero. This is an exact constitutive calculation, not a claim about which matrices a minimizer attains.

## 4. Completion of the exact weighted-homogeneous core exclusion

The counterexample lane's pass-3 argument was checked independently. Consider an exact interior core

y_i(r,theta)=r^(alpha_i)phi_i(theta),
0<alpha1<=alpha2<=alpha3,
phi in C^2(S^2),
s=alpha1+alpha2+alpha3>3.

Write m=alpha1 and J=r^(s−3)j(theta).

### 4.1 Finite energy removes angular determinant zeros

Finite barrier energy on any fixed radial annulus implies integral_S2 j^(−2)<infinity. Orientation almost everywhere and continuity give j>=0. Since C^2 angular data makes j C^1, a zero would imply j(theta)<=C dist(theta,theta0), and the two-dimensional integral of its inverse square would diverge logarithmically. Thus min j>0 follows from admissibility rather than requiring a separate hypothesis.

The radial restrictions are m>1/2 and s<9/2. They do not alone decide stationarity.

### 4.2 Previously excluded range and its complement

Set

eta=2(3m+alpha2+2alpha3−6).

The previously audited third-component/ray argument excludes eta>0. If eta<=0, then alpha2>m: equality would imply eta=4(s−3)>0. Moreover m<1 and

6−s−3m
=[6−3m−alpha2−2alpha3]+(alpha3−m)>0.

Thus the first gradient row has a unique lowest homogeneity exponent.

### 4.3 First-component orders in the remaining range

The leading first stress divergence is

6a div(|grad y1|^4 grad y1),

with exponent 5m−6. The other contributions and their gaps above this exponent are:

- sixth-power correction: exponent 3m+2alpha2−6, gap 2(alpha2−m)
- cofactor-cubic term: exponent 2m+3alpha2−6, gap 3(alpha2−m)
- determinant-square term: exponent 2s−m−6, gap 2s−6m
- inverse-square barrier: exponent 6−2s−m, gap 2(6−s−3m)

All gaps are positive. The cofactor order uses the fact that differentiating with respect to row 1 affects only cofactor rows 2 and 3. The estimates remain valid after differentiation because the angular coefficients are C^1 and j has a positive minimum.

On compact punctured subsets, ordinary additive variations are admissible, so stationarity there is justified. Divide its first equation by r^(5m−6) and send r to zero at fixed angle. The exact scalar leading function u=y1 satisfies

div(|grad u|^4 grad u)=0

throughout the punctured ball.

### 4.4 Spherical scalar equation and the critical exponent

For u=r^m varphi(theta), put

A(theta)=(m^2 varphi^2+|grad_S varphi|^2)^2.

The spherical equation is

div_S(A grad_S varphi)+m(5m−3)A varphi=0,

and its integrated identity is

integral A|grad_S varphi|^2=m(5m−3) integral A varphi^2.

For 1/2<m<3/5 this forces varphi=0, contrary to j>0. At m=3/5 it forces varphi constant. The nonzero constant option has one sign, contrary to the positive local degree of the exact core, which requires nearby target values of both signs in the first coordinate to be attained.

For 3/5<m<1, the shrinking-sphere flux is O(r^(5m−3)) and tends to zero. Since u belongs to W^{1,6}, its scalar 6-harmonic equation therefore extends weakly across 0. The scalar interior C^1 regularity theorem then contradicts the nonzero homogeneous gradient r^(m−1). Only this scalar equation is extended; no unproved full elasticity Euler equation at the singularity is used.

The scalar regularity theorem and its exponent convention were checked against Uhlenbeck's original paper by the counterexample lane; the source and inspection scope are recorded in its `SOURCE_METADATA.json` and `EXACT_WEIGHTED_CORE_EXCLUSION.md`. The present certificate independently verifies the reduction, exponent gaps, spherical coefficient and removable-puncture calculation.

Together the two exponent ranges exclude every such exact C^2-angular weighted-power collapsing core. This does not exclude merely asymptotic profiles, rough angular dependence, nonhomogeneous singularities or boundary collapse.

## 5. Verification and limitations

`verify_coupled.py` checks stress orientations and contractions, all conditional-equilibrium thresholds, relative-barrier and principal-stress identities, the tracefree cubic formula, conformal monotonicity, and the remaining weighted-core exponent arithmetic. Its machine-readable output is `verification.json`.

The newly used anisotropic examples are applications of the already sealed compatible family to distinct stress-integrability thresholds. They are not minimizers. Inverse polyconvexity, conditional ordinary equilibrium and exact-core exclusions do not supply the missing unconditional regularity theorem. E-6322 remains unresolved by this report.
