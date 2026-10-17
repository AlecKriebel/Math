# E-6322, pass 4: exact comparison and tangent certificates

16 October 2026. All four coefficients a,b,c,d are fixed and positive. The frozen full-class benchmark is unchanged. Write J=det F, C=cof F and

\[
W(F)=H(F)+dJ^{-2},\qquad H(F)=a|F|^6+b|C|^3+cJ^2.
\]

Every nonminimizing example below is identified explicitly. None is a counterexample to the asserted determinant lower bound for global minimizers.

## 1. Smooth compatible obstruction to affine interpolation

### Construction

Fix A>1. Choose a smooth radial cutoff χ(|x|²), equal to one on B(0,1/8) and zero outside B(0,1/4), and set

\[
\mathcal H_A(x)=(\log A)x_1x_2\chi(|x|^2),\qquad
X_A=(\partial_2\mathcal H_A,-\partial_1\mathcal H_A,0).
\]

The vector field is smooth, compactly supported and divergence free. Its time-one flow S_A is a global smooth volume-preserving diffeomorphism, identical to the identity outside B(0,1/4). For |x|<1/(32A), its entire time interval [0,1] stays inside B(0,1/8), because the linear trajectory there is

\[
S_A^t(x)=(A^t x_1,A^{-t}x_2,x_3),\qquad |S_A^t(x)|\le A|x|<1/32.
\]

Consequently S_A(x)=diag(A,A^{-1},1)x on that smaller ball.

Choose a smooth radial angle θ(r), equal to π for r≤1/8 and zero for r≥1/4. Let

\[
T(x)=R_z(\theta(|x|))x.
\]

This is a global smooth diffeomorphism: it preserves |x| and its inverse uses the angle −θ(|x|). For r>0,

\[
DT=R_z(\theta)[I+\theta'(r)(A_zx)\otimes n],\qquad n=x/r,
\]

where A_z is the skew matrix generating rotations around the third axis. The determinant lemma and n·A_zx=0 give det DT=1. Smoothness at zero follows from the angle being constant there.

Thus u_A=T∘S_A is a smooth volume-preserving diffeomorphism, equal to the identity outside B(0,1/4), with

\[
Du_A=\operatorname{diag}(-A,-A^{-1},1)
\quad\text{on }B(0,1/(32A)).
\]

### Exact interpolation failure

For z_t=(1−t)id+t u_A, the determinant on this open core equals

\[
\det Dz_t=[1-(A+1)t][1-(1+A^{-1})t].
\]

It is negative for

\[
\frac1{A+1}<t<\frac A{A+1},
\]

and zero on an open ball at the two endpoints. In particular A=2,t=1/2 gives det Dz_t=−1/8. For every prescribed t∈(0,1), choosing

\[
A>\max\{(1-t)/t,t/(1-t)\}
\]

makes that prescribed interpolation orientation reversing on the core. A spatial cutoff interpolation has the same defect whenever its cutoff is constant with value t on this core.

### Arbitrarily small total excess

Put u_{A,ε}(x)=εu_A(x/ε), using the global map u_A. On B(0,1), this is a smooth diffeomorphism with identity boundary trace and determinant identically one, equal to the identity outside B(0,ε/4). Exact change of variables gives

\[
\begin{aligned}
\|Du_{A,\varepsilon}-I\|_{L^6(B_1)}&=\varepsilon^{1/2}c_A,\\
\|u_{A,\varepsilon}-id\|_{L^6(B_1)}&=\varepsilon^{3/2}c'_A,\\
\|u_{A,\varepsilon}-id\|_{L^\infty(B_1)}&=\varepsilon c''_A,\\
I(u_{A,\varepsilon})-I(id)&=\varepsilon^3\Delta_A>0.
\end{aligned}
\]

The strict positivity follows, for instance, from strict Jensen for a|F|⁶, the null-Lagrangian averages of F and cof F, and J≡1. All these maps are therefore **nonminimizers** for their identity trace. They nevertheless show that compatibility, smoothness, J≡1 and arbitrarily small total W¹,⁶ distance/uniform distance/energy excess do not by themselves make an affine blend admissible. Shrinking its amplitude alone gives no universal remedy across this family.

This does not contradict a scale-invariant epsilon-regularity theorem requiring suitably small normalized excess on every relevant small ball: the rescaled core keeps its fixed large distortion.

## 2. Actual inverse Piola and the precise addition scope

Suppose y is an original admissible map and v is its actual a.e. inverse on D=G(Ω), with the inverse and change-of-variables properties established in the previous passes. Set H=Dv, K=det H. Then

\[
V(H)=a\frac{|\operatorname{cof}H|^6}{K^5}
+b\frac{|H|^3}{K^2}+\frac cK+dK^3.
\]

For ζ∈C_c∞(D;R³), change of variables and J(cof Dv)∘y=Fᵀ give

\[
\int_D\operatorname{cof}Dv:D\zeta
=\int_\Omega F^T:D\zeta(y)
=\int_\Omega\operatorname{div}_x[\zeta(y)] =0.
\]

The last map belongs to W¹,⁶ and vanishes on a source boundary collar because y is continuous up to the boundary, takes that boundary into ∂D, and ζ is compactly supported in D.

If h is smooth, the cofactor expansion is exact:

\[
\operatorname{cof}(Dv+Dh)=\operatorname{cof}Dv+M(Dv,Dh)+\operatorname{cof}Dh,
\]

where each row of M is the sum of two cross products of one weak gradient of a component of v and one smooth gradient of a component of h. Each such cross product has zero distributional divergence. This follows from curl of a gradient being zero and the product rule with a smooth coefficient, or by strong W¹,⁹/⁵ approximation in the terms linear in Dv. Thus smooth additions preserve the weak Piola identity. They need not preserve positive determinant or finite V, as the next section shows.

This argument is restricted to actual inverses plus smooth additions. It does not prove weak Piola for every arbitrary W¹,⁹/⁵ map with finite V. The natural-exponent generic minor-identification problem is not resolved here.

## 3. Every nonzero amplitude of a smooth inverse addition can have infinite energy

Let 1/3≤α<1/2 and, on B₁, set

\[
y_\alpha(x)=(r^{-\alpha}x_1,r^{-\alpha}x_2,r^{5\alpha}x_3),
\qquad y_\alpha(0)=0.
\]

As proved and exactly checked in pass 2, this is a finite-energy homeomorphism of B₁ onto itself with identity trace. Its Jacobian is

\[
J=r^{3\alpha}q(n),\quad q(n)=1-\alpha+6\alpha n_3^2,
\]

and W(Dy_α)≈r^−6α. Let v be its actual inverse. Choose χ∈C_c∞(B₁), χ=1 near zero, and put ζ(z)=−χ(z)z₁e₁. For all sufficiently small primal r, y_α(x) lies in the set χ=1. There,

\[
D(v+t\zeta)=H-t e_1\otimes e_1,\qquad
K_t=K(1-tF_{11}),\qquad
F_{11}=r^{-\alpha}(1-\alpha n_1^2)\ge(1-\alpha)r^{-\alpha}.
\]

For every t>0, K_t<0 on a set of positive target measure near zero, so the dual energy is infinite. For every t<0, the cubic determinant term alone yields

\[
\begin{aligned}
\int_{B_1}V(Dv+tD\zeta)
&\ge d|t|^3\int_{\{r<r_0\}}J^{-2}F_{11}^3\,dx\\
&\ge c|t|^3\int_0^{r_0}r^{2-9\alpha}\,dr=\infty.
\end{aligned}
\]

At α=1/3 the divergence is logarithmic. Thus **every nonzero real amplitude** of this fixed smooth compactly supported inverse addition has infinite energy, even though v itself has finite V and the weak Piola property is preserved by the addition.

The map y_α is not a minimizer for its identity trace. This is an exact obstruction to deriving nonvacuous finite additive intervals from coercivity alone, not a minimizer counterexample.

## 4. Mixed cofactor growth is not controlled by endpoint dual energies

For L≥1 put m=L^−1/5 and

\[
H_1=\operatorname{diag}(L,m,m),\qquad H_2=\operatorname{diag}(m,L,m).
\]

Each has K=L^3/5, |cof H_i|≈L^4/5, and V(H_i)≈L^9/5. But

\[
\operatorname{cof}(H_1+H_2)-\operatorname{cof}H_1-\operatorname{cof}H_2
=\operatorname{diag}(Lm+m^2,Lm+m^2,L^2+m^2).
\]

Consequently no universal pointwise bound of the mixed cofactor by C[1+V(H₁)+V(H₂)] holds. The same endpoint V controls the natural endpoint cofactor powers |cof H_i|^9/4≈L^9/5 but not this mixed term of size L². This is a **matrix-only growth obstruction**. No compatible-gradient construction or failure of inverse-class closure is inferred from it.

## 5. Structured natural-exponent cutoffs: independent chain-rule check

Here the earlier audited reduced inverse-class characterization is an input theorem. For a smooth graph transformation Φ(z,x), equal to x near ∂D, put

\[
u(z)=\Phi(z,v(z)),\qquad k(x)=\Phi(y(x),x).
\]

The inverse map is bounded, so u∈W¹,⁹/⁵. The primal auxiliary k belongs to W¹,⁶ and equals id on a source boundary collar. With A=D_zΦ(y,x), B=D_xΦ(y,x), the identities are

\[
Dk=AF+B,\quad Du\circ y=A+BF^{-1}=DkF^{-1},
\]

\[
J(\det Du)\circ y=\det Dk,\qquad
J(\operatorname{cof}Du)\circ y=(\operatorname{cof}Dk)F^T.
\]

For smooth ψ near Dbar and compactly supported smooth φ on R³, the transported volume expression is

\[
\int_\Omega\left[\psi(y)\det Dk\,\operatorname{div}\phi(k)
+\phi(k)\cdot(\operatorname{cof}Dk)D(\psi\circ y)\right]dx.
\]

For smooth maps its integrand is the divergence of

\[
\psi(y)(\operatorname{cof}Dk)^T\phi(k).
\]

Approximate k−id and y−G strongly in W¹,⁶ by compactly supported smooth maps. The maps converge uniformly, the cofactor strongly in L³, the determinant strongly in L², and the chain gradient strongly in L⁶. Every displayed product therefore converges in L¹. The boundary term is exactly

\[
\int_{\partial\Omega}\psi(G(x))\phi(x)\cdot\nu_\Omega\,dS.
\]

This verifies the full transported identity with correct orientations. Conditional on finite V(Du), the earlier characterization supplies exact inverse-class membership. In particular it covers u=θv+(1−θ)ℓ, with θ smooth, θ=1 near ∂D and ℓ smooth, despite the difference having only the natural inverse Sobolev exponent. Finiteness of V remains an essential separate hypothesis. The counterexample in Section 1 precludes inferring orientation preservation from positive endpoint determinants alone.

## 6. One-row comparison: mixed moment and sharp barrier source

Let y be a global minimizer and let v have the same trace and the same two unchanged components. Assume H(Dv) is integrable and J_v≥0; v need not itself have finite barrier energy. Since every minor is affine in the changed row,

\[
y_t=(1-t)y+tv,\qquad J_t=(1-t)J_y+tJ_v>0\quad(0<t<1).
\]

The function H is convex along this row segment, so its secant quotients have an integrable positive majorant and converge to

\[
L_+=DH(Dy):(Dv-Dy),\qquad
L_+\le H(Dv)-H(Dy).
\]

Here L_+ is the positive-density directional derivative, not its scalar positive part. Standard Young inequalities for the affine minor differences show |L_+|≤C[H(Dy)+H(Dv)].

For 0<t≤1/2, the positive part of the barrier secant obeys

\[
\left(\frac{dJ_t^{-2}-dJ_y^{-2}}t\right)^+
\le dJ_y^{-2}\frac{(1-t)^{-2}-1}t
=dJ_y^{-2}\frac{2-t}{(1-t)^2}\le6dJ_y^{-2}.
\]

The convex barrier secants decrease to −2dJ_y^−3(J_v−J_y) as t↓0. Minimality and reverse Fatou, using the preceding integrable upper bounds, imply that the limiting negative part is integrable and

\[
2d\int_\Omega J_vJ_y^{-3}
\le\int_\Omega L_++2d\int_\Omega J_y^{-2}
\le\int_\Omega[H(Dv)-H(Dy)]+2d\int_\Omega J_y^{-2}.
\]

There is no claim that suitable v has J_v uniformly positive on the desired low-J region.

The coefficient 2 multiplying the original barrier source cannot be reduced by taking t smaller: at the nonnegative endpoint J_v=0, the exact cost per t is

\[
dJ_y^{-2}\frac{2-t}{(1-t)^2}\ge2dJ_y^{-2},
\]

with equality only in the limit t↓0. Such a zero-J endpoint is compatible with an identity minimizer: choose a smooth nondecreasing one-variable f equal to id outside a compact interval, with f′=0 on a smaller interval, and a transverse cutoff η∈[0,1] compactly supported, equal to one on a small disk. Then v=(x₁,x₂,x₃+η(x₁,x₂)[f(x₃)−x₃]) has J_v=1+η(f′−1)≥0 and J_v=0 on an open box. Use a ball containing its support. The endpoint has infinite barrier; all t<1 segments are finite-energy competitors. This certifies the sharp source calculation even at an actual identity minimizer.

## 7. Controlled annular tangents: stress, rather than divergence, scaling

Consider componentwise rescalings

\[
Y_{k,i}(z)=r_k^{-\alpha_i}[y_i(x_0+r_kz)-y_{0,i}]
\longrightarrow U_i(z)=|z|^{\alpha_i}\phi_i(z/|z|)
\]

in C¹ on the closed annulus 1/2≤|z|≤2, with C² angular profile, det DU>0 there, 0<α₁≤α₂≤α₃ and s=Σα_i>3. Put m=α₁, γ=s−3.

The physical gradient is D_kDY_k with D_k=diag(r_k^(α_i−1)). Absolute continuity of the original finite-energy integrals and the nondegenerate limit yield

\[
\int_{x_0+r_kA}|Dy|^6\gtrsim r_k^{6m-3}\to0,
\qquad
\int_{x_0+r_kA}J^{-2}\gtrsim r_k^{9-2s}\to0.
\]

Therefore m>1/2 and s<9/2, including strict exclusion of both equality cases.

Because the original map is C¹ and its determinant has a positive lower bound on each sufficiently late annulus, the local additive weak Euler equation is justified there. After rescaling it reads div_z[P(D_kDY_k)]_i=0. The overall spatial rescaling factor is common and cancels; one must normalize the **stress** exponent, not its divergence exponent.

For row 3, the barrier stress exponent is

\[
\tau_3=\alpha_1+\alpha_2-2-3\gamma,
\]

while the positive stress is O(r_k^(4m+α₃−5)). Their difference is

\[
\eta=2(3\alpha_1+\alpha_2+2\alpha_3-6).
\]

If η>0, division by r_k^τ₃ and uniform C¹ convergence give the limiting barrier-only equation. If η≤0, the already checked exponent algebra yields α₂>m, m<1 and 6−s−3m>0. Dividing row 1 by r_k^(5m−5) gives scalar 6-harmonic flux 6a|DU₁|⁴DU₁; the other relative stress exponents are

\[
2(\alpha_2-m),\quad3(\alpha_2-m),\quad2s-6m,
\quad2(6-s-3m),
\]

all strictly positive.

Uniform convergence of the normalized stress coefficients suffices to pass against a fixed smooth test. No second-derivative convergence or differentiation of the remainder is used. Exact homogeneity of the limiting map then extends its equation from one annulus, and the pass-3 angular-ray/scalar argument excludes the profile. This independently certifies the new annular-limit step in the sibling report `counterexample/ANNULAR_TANGENT_EXCLUSION.md`; it does not supply such a tangent for an arbitrary minimizer.

## 8. Angular repair: finite energy does not make a limiting angular Jacobian positive

On B₁ consider, for γ=δ=1/2,

\[
y(x)=(x_1,x_2,f(x)),\qquad
f=x_3^3r^{\gamma-2}+x_3r^{\gamma+\delta},\quad y(0)=0.
\]

It has the full smooth permitted trace G(x)=(x₁,x₂,x₃³+x₃), a global smooth orientation-preserving diffeomorphism. Direct differentiation gives

\[
J=r^\gamma n_3^2[3+(\gamma-2)n_3^2]
+r^{\gamma+\delta}[1+(\gamma+\delta)n_3^2]>0\quad(r>0).
\]

Its gradient is bounded. More generally for positive γ,δ the angular comparison is

\[
J\asymp r^\gamma(\mu^2+r^\delta),\quad\mu=n_3,
\]

with constants fixed by γ,δ. Since

\[
\int_{-1}^1(\mu^2+\varepsilon)^{-2}d\mu
=\frac1{\varepsilon(1+\varepsilon)}
+\frac{\arctan(1/\sqrt\varepsilon)}{\varepsilon^{3/2}}
\asymp\varepsilon^{-3/2},
\]

the inverse determinant is integrable precisely when 2γ+3δ/2<3. At γ=δ=1/2 the angular integral is comparable to r^−7/4, leaving the integrable radial power r^1/4. The leading weighted profile nevertheless has a quadratic angular Jacobian zero along the equator.

This map is **not stationary**, hence is not a minimizer. Since the first two components are identities, (cof Dy)₃=e₃. On the positive third axis t>0,

\[
J(t)=\tfrac32t^{1/2}+2t,\qquad
\operatorname{div}P^{bar}_3=6dJ^{-4}\partial_3J
=\tfrac{8d}{9}t^{-5/2}[1+o(1)].
\]

The positive-density third-row divergence is only O(t^−1/2), so it cannot cancel. The example certifies the necessity of a positive limiting angular-Jacobian hypothesis in the annular-tangent exclusion. Its finite energy is not evidence for minimization.

## 9. Conditional controlled inverse endpoint lemma

Let v be an actual inverse minimizer, let ζ∈W¹,⁹/⁴ be compactly supported, and write H_e=H+Dζ, C_e=cof H_e and K_e=det H_e. Assume pointwise rank(Dζ)≤1 and, for M≥1,

\[
|H_e|\le M|H|,\qquad |C_e|\le M|C|,\qquad 0\le K_e\le MK.
\]

Rank one makes all minors affine along H_t=H+tDζ. For 0≤t<1,

\[
|H_t|\le M|H|,\quad |C_t|\le M|C|,\quad
(1-t)K\le K_t\le MK,
\]

and therefore

\[
V(H_t)\le M^6(1-t)^{-5}V(H).
\]

The earlier sufficient inverse-addition theorem applies, so these are admissible inverse comparisons. Set X=a|C|⁶/K⁵+b|H|³/K²+c/K. The elementary endpoint difference bounds are |H_e−H|≤(M+1)|H|, |C_e−C|≤(M+1)|C| and |K_e−K|≤(M+1)K. Differentiation at zero is dominated by C_M V(H), and the three X terms have derivative bounds respectively 11(M+1), 5(M+1) and (M+1) times their original values. If ζ vanishes off E, minimality gives

\[
3d\int_E K^2(K-K_e)\le11(M+1)\int_E X.
\]

The hypotheses are conditional, including actual construction of this endpoint with the domination estimates. The inequality does not assert that an endpoint reducing K in a desired region exists. Section 3 shows why this is a substantive condition.

## 10. Compatible obstruction to uniformly positive one-component repair

This independently verifies the radial projection argument proposed by the positivity lane. Fix 1/6<κ≤1/2 and put

\[
L(r)=\log(e/r),\qquad y(x)=r^{1/2}L(r)^\kappa x\quad(0<r<1),\qquad y(0)=0.
\]

The target radius R=r³ᐟ²L^κ is strictly increasing, since

\[
R'=r^{1/2}L^\kappa q,\qquad q=3/2-\kappa/L\ge1.
\]

Thus y is an identity-trace radial homeomorphism B₁→B₁. Its gradient is bounded and

\[
J=r^{3/2}L^{3\kappa}q,\qquad
\int_{B_1}J^{-2}\asymp\int_0^1\frac{dr}{rL^{6\kappa}}<\infty.
\]

Let K be its inverse Jacobian, evaluated in target coordinates z. Since |z|=R=r³ᐟ²L^κ,

\[
K(z)=R^{-1}L^{-2\kappa}/q,\qquad
\log(e/R)=\tfrac32L-\kappa\log L-\tfrac12\asymp L.
\]

Consequently, near zero,

\[
K(z)\asymp\frac1{|z|[\log(e/|z|)]^{2\kappa}}.
\]

For any fixed two-dimensional orthogonal projection π, the source pushforward under πy has density

\[
\rho(z')=\int_{\{t:(z',t)\in B_1\}}K(z',t)\,dt.
\]

For every sufficiently small |z′|>0, with a fixed small R₀,

\[
\rho(z')\ge c\int_{2|z'|}^{R_0}
\frac{dt}{t[\log(e/t)]^{2\kappa}}\longrightarrow\infty
\quad\text{as }|z'|\downarrow0.
\]

The divergence is a power of log when κ<1/2 and log-log when κ=1/2. In particular ρ is essentially unbounded, not merely infinite on one null fiber.

Suppose there were any full-class identity-trace map v with πv=πy a.e. and J_v≥δ>0 a.e. The established positive-degree change-of-variables formula for this full class gives, for every nonnegative compactly supported smooth f on the projection plane,

\[
\int_{B_1}f(\pi y)\,dx
=\int_{B_1}f(\pi v)\,dx
\le\delta^{-1}\int_{B_1}f(\pi v)J_v\,dx
=\delta^{-1}\int_{B_1}f(\pi z)\,dz
\le2\delta^{-1}\int_{\mathbb R^2}f(z')\,dz'.
\]

This would force ρ≤2/δ a.e., a contradiction. Hence no uniformly positive full-trace repair can keep two fixed target components unchanged, for this finite-energy map. Radial symmetry makes the conclusion valid for every fixed target direction chosen for the component change.

The starting y is **not a minimizer**, because it is a nonidentity map with identity trace and the affine uniqueness theorem applies. The result blocks an unconditional class-wide construction of such repairs. It does not rule out a minimizer-specific repair theorem, or a repair changing several target components.

## 11. Verification scope

`verify_comparisons.py` checks the exact determinant, cofactor, row-secant, angular integral, ray-leading-coefficient and stress-exponent identities used above. General smooth-flow existence, the stated distributional product arguments, and the inherited exact inverse-class characterization are mathematical proof inputs, not claims certified by numerical sampling. The script's successful output is recorded in `verification.json`.
