# Independent audit addendum: weaker annular tangent hypotheses

16 October 2026. This is a conditional singular-profile exclusion for the unchanged E-6322 problem. It does not establish that an arbitrary minimizer possesses any such tangent, and it gives no boundary estimate.

## Statement

Let y be a full-class global minimizer, or a local minimizer for which compactly supported sufficiently small W^{1,6} variations are allowed. Fix an interior point x0 and y0=y(x0). Set A={1/2<|z|<2}.

There are no positive exponents 0<α1≤α2≤α3, with s=α1+α2+α3>3, and radii rk↓0 such that

Yk,i(z)=rk^{-αi}(yi(x0+rk z)−y0,i)

converges strongly in W^{1,∞}(A) to

Ui(z)=|z|^{αi} φi(z/|z|),   φ∈C¹(S²;R³),

with det DU>0 on the closed annulus. The homogeneous profile is understood to extend by the displayed formula to the punctured space.

Thus the actual maps on the selected annuli need only be Lipschitz, and no second derivatives of the profile are required. The stronger C¹-convergence/C²-profile hypotheses in the frozen counterexample-lane report are sufficient special cases.

## 1. Admissibility and stress passage under essential gradient bounds

Write m=α1, γ=s−3 and Dk=diag(rk^{αi−1}). At the corresponding physical points,

Dy=Dk DYk,   det Dy=rk^γ det DYk.

Strong W^{1,∞} convergence puts det DYk between fixed positive constants for all sufficiently large k, almost everywhere. For each fixed k, the physical gradients therefore lie almost everywhere in a compact subset of GL⁺(3). Compact smooth additive variations preserve determinant positivity for sufficiently small parameters, with the allowed parameter depending on k and on the test. The ordinary first derivative of the energy is then dominated on that annulus. Consequently every stress row satisfies

div_z [DW(Dk DYk)]i=0 in distributions on A.

This argument requires no pointwise continuity of DYk. The normalized stress coefficients converge in L∞, which is sufficient to pass the weak equations against fixed compact tests.

Absolute continuity of the original finite-energy integrals and a nonzero first limiting row give

0←∫_{x0+rk A}|Dy|⁶ ≥ c rk^{6m−3},

0←∫_{x0+rk A}J^{-2} ≥ c rk^{9−2s}.

Therefore m>1/2 and s<9/2. Disjointness of the annuli is unnecessary.

## 2. Barrier-dominated range without second derivatives

Set η=2(3m+α2+2α3−6). When η>0, the normalized third stress row converges in L∞ to

−2d (det DU)^{-3}(cof DU)3.

Indeed, the barrier stress exponent is τ3=α1+α2−2−3γ; the positive stress row is O(rk^{4m+α3−5}), and the difference of the two exponents is η. The limiting weak equation is

div[J_U^{-3}(cof DU)3]=0.

Since U is C¹ with positive determinant, it is a C¹ local diffeomorphism. In a local coordinate chart X=U(z), use a compact test ψ(z)=χ(U(z)). Such C¹ tests are legitimate by compact C¹ approximation, since the flux is locally bounded. The cofactor identity gives

(cof DU)3·Dψ = J_U ∂_{X3}χ(U(z)).

Changing variables yields

∫ J_U(U^{-1}(X))^{-3} ∂_{X3}χ(X) dX=0.

Hence the continuous scalar J_U∘U^{-1} is constant along every sufficiently short vertical target segment in the chart. One may first deduce constancy on almost every vertical line by distributions and then use continuity to include every line.

The positive local-degree argument supplies θ0 with φ1(θ0)=φ2(θ0)=0. Here φ3(θ0)≠0, and the ray rθ0 is mapped into the third target axis. To recall why degree applies: positivity of det DU implies φ never vanishes, so the extension U(0)=0 has an isolated zero; a sufficiently small regular target value attained near that zero has finitely many positive preimages in a fixed ball, giving strictly positive degree on a target ball. Such a target ball contains third-axis values.

Along the ray,

U3(rθ0)=r^{α3}φ3(θ0),   J_U(rθ0)=r^γ j(θ0),

with j(θ0)>0 and γ>0. The first relation parametrizes a nonconstant local vertical segment, while the second is strictly nonconstant. This contradicts the weak equation. No derivative of j or of DU was used.

The same local argument works for a C¹ angularly degenerate profile on any positive-J patch containing a regular preimage of the third target axis. It does not manufacture such a preimage for a degenerate profile.

## 3. Strain-dominated range with C¹ angular data

If η≤0, the previously checked exponent algebra gives

α2>m,   1/2<m<1,   s+3m<6.

The normalized first stress row converges in L∞ to 6a|∇U1|⁴∇U1. The four relative gaps are

2(α2−m),   3(α2−m),   2s−6m,   2(6−s−3m),

all strictly positive. Thus U1 is weakly 6-harmonic on A. Its exact homogeneity extends this weak equation to the punctured ball.

Only first derivatives are needed for the spherical weak identity. With φ=φ1 and Aφ=(m²φ²+|∇Sφ|²)², testing with a radial cutoff times φ yields

∫S² Aφ |∇Sφ|² = m(5m−3)∫S² Aφ φ².

For 1/2<m<3/5 this forces φ=0, contrary to positive determinant. At m=3/5 it forces φ to be constant; a nonzero constant would make U1 one-signed, contradicting the positive degree just described. The zero constant also contradicts positive determinant.

For 3/5<m<1, U1∈W^{1,6} across the puncture, and the scalar stress is O(r^{5m−5}). Removing a ball with a cutoff produces an error bounded by C r^{5m−3}→0. Hence U1 is weakly 6-harmonic across zero. The scalar interior gradient regularity theorem makes its gradient bounded near zero, whereas any nonzero degree-m homogeneous C¹ profile with m<1 has an unbounded gradient. This is a contradiction.

The scalar regularity input is the corollary on printed p.222 of K. Uhlenbeck, *Regularity for a class of non-linear elliptic systems*, Acta Mathematica 138 (1977), 219–240, with the paper's parameter p=4. Its primary statement was inspected in pass 3. It is applied only to the scalar weak 6-harmonic limit.

https://doi.org/10.1007/BF02392316

## Limits

Uniform positivity of the limiting angular Jacobian is an explicit hypothesis. Finite original energy does not imply it for a rescaled limit. Strong W^{1,∞} annular convergence is also an additional hypothesis, even though it is weaker than the frozen report's C¹ convergence requirement. No tangent existence, convergence theorem, boundary conclusion, global regularity theorem, or solution of E-6322 is inferred.
