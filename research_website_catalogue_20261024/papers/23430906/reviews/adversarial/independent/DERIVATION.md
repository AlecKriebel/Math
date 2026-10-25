# Independent falsification derivation, sealed before submitted-checker inspection

The complete seven-page published manuscript was read first, using the exact-hash
locator and then the fresh deposited PDF and TeX. No submitted checker, archived
verdict, archived proof body, or current sibling mathematical opinion was used
to construct this derivation or `controls.py`.

## Exact target and avenues of attack

The target is a lower bound for every real square-integrable function F of both
complete uniform observation grids, for the *iterated integral* X, at every
fixed H in (1/4,1), T>0, n>=1. The constant is the literal constant in (3),
not an unspecified smaller constant. No uniformity in H or sampling adaptation
is implicit. Success means establishing all these quantifiers. An example
outside those assumptions is a boundary control, not a counterexample.

Potential failures tested: Fourier sign; 2π or D normalization; zero-extension
regularity; periodization uniformity; signed off-diagonal covariance; hidden
independence of cells; nonlinear estimators; auxiliary Gaussian directions;
canonical versus antisymmetric area; the H=3/4 summability transition; n=1;
H tending to 1 or 1/4; and simultaneous-limit circularity.

## Independent minimal convergence interface

Accept the established existence of the canonical polygonal L2 limit P_m -> X.
For any finite mesh, direct deterministic integration gives P_m=L_m+Q_m,
Q_m=(1/2) sum ΔB1_k ΔB2_k. This identity needs no stochastic-integral theorem.
Independence of the components gives exactly

 E Q_m² = T^(4H)/(4 m^(4H)) [m+2 sum_(r=1)^(m-1) (m-r) ρ_H(r)²].

For r>=2, twice integrating the second derivative of x^(2H) bounds
|ρ_H(r)| by H|2H-1|(r-1)^(2H-2). The r=1 term is finite.
Thus E Q_m² is O_H(T^(4H)m^(1-4H)) below H=3/4,
O(T³m^-2(1+log m)) at H=3/4, and O_H(T^(4H)m^-2) above it.
All go to zero for the claimed open H interval. Therefore L_m -> X without
using any exact Euler-error coefficient, same-cell area kernel or separated-cell
regularization argument. This confirms the only convergence interface needed
by the witness proof directly from the defining polygonal convention.

There is no circular lower-bound assumption in canonical-area existence.
The primary dependency remains existence of the polygonal L2 limit for H>1/4;
the proof does not claim to establish that classical existence theorem anew.

## Orthogonal tensor formulation

For independent Gaussian components let K be the real conjugate-symmetric
Fourier Hilbert space and S=span{K_(jT/n):1<=j<=n}. The bilinear Gaussian
isometry J maps u⊗v to W1(u)W2(v), with
E[J(u⊗v)J(u'⊗v')]=<u,u'><v,v'>. Every finite polygonal area lies in this
closed second chaos, and so does X by L2 convergence. Write X=J(x).

Conditional expectation on both grids acts on this chaos as
J((P_S⊗P_S)x). This follows first for elementary tensors by independence
of the two Gaussian families and orthogonal Gaussian decompositions, then
by L2 closure. It remains the optimal estimator even among nonlinear grid
functions: the ordinary conditional-expectation orthogonality theorem includes
all of L2(G). Hence a residual pairing in S-perp⊗S-perp cannot be canceled
by any nonlinear estimator.

For any real compactly supported h with sufficient Sobolev regularity set
u_h=√D/(2π)|ξ|^(H+1/2) conjugate(hhat). Direct multiplication gives
<K_t,u_h>=(1/(2π))∫(exp(itξ)-1)hhat(ξ)dξ=h(t)-h(0).
The conjugation is essential: omitting it reflects h to h(-t), making a
positive-time bump give zero pairing with the target path. This is an
adversarial sign control, not a defect of the correctly printed formula.

Take phi=x⁴(1-x)⁴ on [0,1], zero otherwise; f=phi', g=phi.
The zero extensions f,g have third weak derivatives in L1: their first
three traces r,r',r'' vanish at both endpoints. A jump of f''' does not
produce a boundary mass in the third derivative. Three integrations by
parts give |rhat|<=min(L_r,N_r|ξ|^-3). Consequently the covariance-path
vectors lie in K for α=2H+1<3, including H arbitrarily close to 1.

The scaled translates h_j(t)=Δ^H h(t/Δ-j), Δ=T/n, vanish at all
observations, including 0 and T. Thus u_fj,u_gj belong to S-perp.
Their Gram matrices have entries independent of Δ, since the scale power is
2H+2-(2H+1)-1=0. For any finite real b,

 ||sum b_j u_rj||² = D/(4π²)∫_-π^π P_r(θ)|sum b_j exp(ijθ)|²dθ
 <= D Pbar_r/(2π) sum b_j².

The periodized tail is bounded using (2|ell|-1)π and exponent α-6<-3.
The odd series is at most 1+1/[2(5-α)]. Thus the printed Pbar bounds the
entire periodization, uniformly in n and Δ; no lower eigenvalue of the
increment covariance is assumed. This matters for H<1/2: the variance of
the sum of n increments is n^(2H), incompatible with a lower multiple of n.

Let y=sum_(j=0)^(n-1) u_fj⊗u_gj. If A,C are the two Gram matrices,
||y||²=tr(AC)<=||A||op tr(C)<=n M_f M_g. This does not discard any signed
lag and does not require the matrices to commute. It is a positive-matrix
trace inequality. The tensor is nonzero because of the positive pairing below.

For fixed n,T,j, pair finite L_m with J(u_fj⊗u_gj). Wick factorization
between components gives the deterministic left sum of f_j against dg_j.
Its limit is ∫f_j g_j'=Δ^(2H) a, where a=∫(phi')²=4/45045.
The stochastic limit is valid by Cauchy-Schwarz and the preceding L2
convergence; n is fixed throughout that limit. Therefore <x,y>=nΔ^(2H)a.
Since y is orthogonal to grid-observable second chaos, and hence J(y) is
orthogonal to all L2(G),

 ||X-F||₂ >= nΔ^(2H)a / sqrt(n M_f M_g)
 = [2πa/(D sqrt(Pbar_f Pbar_g))] T^(2H)n^(1/2-2H).

The literal constant in the manuscript is recovered. No replacement
assumption contains the desired lower bound. A construction on an enlarged
Gaussian space suffices because (X, observations) has the same joint law,
and every F is a Borel grid function up to null sets.

## Boundary and independent Brownian controls

At H=1/2, D=2π, Plancherel gives <u_rj,u_rk>=∫r'_j r'_k.
Disjoint interiors make both Gram matrices diagonal. Therefore this same
choice of bumps actually gives the stronger constant sqrt(a/b),
b=∫(phi'')², for Brownian motion. Compare this with the exact Brownian
optimal constant 1/2. `controls.py` checks the polynomial integrals exactly.

An independent finite-dimensional conditional calculation supplies a separate
normalization control. For N Brownian fine increments of covariance (T/N)I,
the polygonal area is XᵀAY, where A is upper triangular with diagonal 1/2
and entries 1 strictly above the diagonal. Given n coarse increment sums
with N a multiple of n, conditional component means are block averages.
Thus E[P_N|coarse]=P_n and the residual variance is exactly
T²/4(1/n-1/N). Its N->infinity limit is T²/(4n), recovering the
claimed prior Brownian optimum T/(2√n). In particular n=1 has positive
residual even though both final endpoints are observed.

The H=1 endpoint is a true excluded countercontrol: B_t=tZ, X_T=T²Z1Z2/2,
recoverable from endpoints, while D diverges. At H=1/4 the diagonal
Q_m variance is T/4 and the above canonical bridge fails; existence is
not being asserted there. At H=3/4 the logarithm occurs only in the
convergence interface, not the lower-bound scaling or periodized Gram bound.

If the components coincide, X_T=B_T²/2 is grid measurable for smooth
integration; if arbitrary adaptive information or both full paths are given,
the orthogonality premise can fail. These are controls confirming why
independence and the specified observation sigma-field are indispensable.
The theorem makes neither such extension. T scaling is T^(2H), as required
by bilinearity; the antisymmetric difference carries twice the error,
while half that difference and the iterated integral share the conditional
residual because their difference B1_T B2_T/2 is observed.

At this independent checkpoint no counterexample or central unsupported
inference has been identified. This is an adversarial mathematical review,
not certification of novelty, worldwide openness, human peer review,
formal proof-assistant correctness, or publication clearance.
