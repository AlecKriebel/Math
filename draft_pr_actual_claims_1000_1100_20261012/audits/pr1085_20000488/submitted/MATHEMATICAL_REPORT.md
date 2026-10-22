# Robin bound states under compact half-space perturbations: a dimension dichotomy

AIM Problem 1.4, *Shape optimization with surface interactions*, corpus 20000488 / AIM-ANALYSIS-0020. Accepted negative answer to the dimension-unrestricted universal question, substantive attempt 1 of 5. This AI-assisted, unrefereed edition includes an [independent mathematical audit](MATHEMATICAL_AUDIT.md) and [public source metadata](SOURCE_METADATA.json).

## 1. Conventions, scope, and results

Write n=m+1≥2, z=(x,y)∈R^m×R, and H={y>0}. The attractive Robin realization H_{β,Ω}, β>0, is associated with the closed semibounded form

q_{β,Ω}[u]=∫_Ω |∇u|²−β∫_{∂Ω}|u|² dS,   D(q)=H¹(Ω).

Its boundary condition is ∂_νu=βu with the outward unit normal ν. Thus the source's negative parameter α is −β, and the flat threshold is −β².

A smooth compact half-space perturbation means a connected open set Ω with C∞ boundary, Ω△H contained in a bounded set, and Ω≠H. The boundary may be disconnected and may have overhangs; no graph or boundary-topology restriction is imposed. One can replace C∞ by a uniformly Lipschitz compact perturbation where the almost-everywhere normal and standard trace/density properties apply, but the main nongraph theorem is deliberately stated in the smooth class. The graph theorem below is proved for f∈W^{1,∞}_c(R^m), Ω_f={y>f(x)}.

**Theorem A (full nongraph binding in n=2,3).** Every smooth compact half-space perturbation in ambient dimension 2 or 3 has σ_ess(H_{β,Ω})=[−β²,∞) and at least one discrete eigenvalue below −β² for every β>0.

**Theorem B (weak-coupling stability in every n≥4).** For each f∈W^{1,∞}_c(R^m), m≥3, there is β₀(f)>0 such that

σ(H_{β,Ω_f})=σ_ess(H_{β,Ω_f})=[−β²,∞),   0<β≤β₀(f).

In particular this applies to nonzero C∞ compactly supported graphs. It disproves the dimension-unrestricted universal binding claim with nontrivial connected smooth domains and connected boundary. It does not claim absence at large coupling, and does not classify all nongraph domains in n≥4.

**Explicit counterexample.** In every m≥3, let

h(x)=exp(−1/(1−|x|²)) for |x|<1, and h(x)=0 for |x|≥1,
f(x)=h(x)/100.

At β=1 the Robin Laplacian on Ω_f has no spectrum below −1. The graph is nonzero, C∞, compactly supported, and diffeomorphic to R^m; Ω_f is connected and diffeomorphic to H.

## 2. Closed form and essential spectrum

For the geometries under consideration the local Lipschitz trace inequality and the flat trace inequality give, for every ε>0,

∫_{∂Ω}|u|²≤ε∫_Ω|∇u|²+C_ε∫_Ω|u|².

A finite cover suffices for the compact nonflat part; the rest is flat. Hence q is closed and semibounded on H¹(Ω). Smooth compactly supported functions on the closure are a form core in the smooth class; for a Lipschitz graph use the bi-Lipschitz flattening from H and density there. No operator-boundary condition is imposed on trial functions.

On H one has the exact identity

q_{β,H}[u]+β²||u||²=∫_H|∇_x u|²+∫_H|∂_y u+βu|²≥0. (2.1)

Tangential Fourier transform shows the flat spectrum is [−β²,∞), with no L² eigenfunction at or below the bottom for m≥1.

We give details of essential-spectrum stability rather than infer it from a negative form value. Let χ²+ζ²=1 be a smooth real partition, with χ compactly supported and ζ vanishing on a neighborhood of every geometrical change. The function ζu, extended by zero where necessary, belongs to H¹(H); thus its shifted form is nonnegative by (2.1). IMS localization gives

Q[u]:=q_{β,Ω}[u]+β²||u||²
=Q[χu]+Q[ζu]−∫_Ω(|∇χ|²+|∇ζ|²)|u|²
≥−C∫_K|u|² (2.2)

for a fixed bounded K and constant C, using semiboundedness for χu. If a real λ<−β² lay in essential spectrum, a normalized operator Weyl sequence u_j⇀0 with (H_{β,Ω}−λ)u_j→0 would have uniformly bounded H¹ norm by the trace inequality and bounded form energies. Local Rellich compactness implies ∫_K|u_j|²→0. Formula (2.2) would yield liminf Q[u_j]≥0, contradicting Q[u_j]→λ+β²<0. Thus there is no essential spectrum below −β².

Conversely fix k∈R^m and λ=|k|²−β². Choose normalized tangential wave packets η_j(x)e^{ik·x}, where η_j is a dilation by R_j→∞ and a translation so far horizontally that its support lies outside the projection of the compact perturbation. Multiply by the normalized transverse mode (2β)^{1/2}e^{−βy}. These functions obey the Robin condition on their flat boundary support, belong to the operator domain, tend weakly to zero, and have residual norm O(R_j^{−1})+O(R_j^{−2}). They are Weyl sequences at λ. Therefore

σ_ess(H_{β,Ω})=[−β²,∞). (2.3)

The same proof works for compact Lipschitz graph perturbations. Any spectrum below −β² is discrete, with finite multiplicity, and can accumulate only at the threshold.

## 3. A global ground-state identity, including overhangs

Set φ(x,y)=e^{−βy}; then Δφ=β²φ and ∂_νφ=−βν_yφ. Integration by parts gives, initially for smooth real v compactly supported on the closure,

Q[φv]=∫_Ω φ²|∇v|² + ∫_{∂Ω}φ(∂_νφ−βφ)|v|² dS
=∫_Ω e^{−2βy}|∇v|²−β∫_{∂Ω}(1+ν_y)e^{−2βy}|v|² dS. (3.1)

For complex v take real parts in the cross term and obtain the same identity. The coefficient 1+ν_y is always nonnegative and vanishes on the flat boundary. This sign requires the attractive convention above.

Define

B_β(Ω)=∫_{∂Ω}(1+ν_y)e^{−2βy}dS. (3.2)

The integrand is supported in the compact nonflat boundary part, so B_β is finite. Moreover B_β>0 for every nontrivial smooth compact perturbation. Indeed if it vanished, continuity and nonnegativity force ν=−e_y everywhere. Every connected component of the smooth boundary would then be locally a horizontal hyperplane. A connected component is closed in R^n and open in its containing horizontal plane, hence it is the full plane. Compact agreement with ∂H excludes any plane except y=0, so ∂Ω={y=0}; agreement with H at infinity and connectedness imply Ω=H. This contradicts nontriviality. In particular compact obstacle boundaries also contribute positively rather than invalidating the argument.

Choose R₀ with the projection of all geometrical changes contained strictly in B_{R₀}. For any compactly supported Lipschitz ψ(x) equal to 1 near B_{R₀}, use v(x,y)=ψ(x) in (3.1). Although v is not compact in y, u=φψ belongs to H¹(Ω): Ω is bounded below, its bounded nonflat portion causes no integrability problem, and its upward tail is exponentially integrable. Truncation at y→+∞ justifies (3.1), with every truncation error tending to zero. Since ∇ψ is supported where the vertical fiber is exactly (0,∞),

Q[e^{−βy}ψ(x)]=(1/(2β))∫_{R^m}|∇ψ|²−βB_β(Ω). (3.3)

This is the promised coordinate-free boundary-defect identity. It does not require single-valued projection, connected boundary, or a tubular coordinate map.

For m=1 take ψ=1 on [−R₀,R₀] and taper linearly to zero over length L on each side; ∫|ψ′|²=2/L→0. For m=2 take ψ=1 on r≤R₀, ψ=log(R/r)/log(R/R₀) on R₀<r<R, and ψ=0 on r≥R; then

∫_{R²}|∇ψ|²=2π/log(R/R₀)→0.

Lipschitz trial functions are admissible; smoothing is optional. Thus (3.3) is negative for large cutoffs. Equations (2.3) and the min–max principle prove Theorem A.

## 4. Compact graphs and a sufficient binding condition

For Ω_f={y>f(x)}, ν=(∇f,−1)/s, s=sqrt(1+|∇f|²), and dS=s dx. Therefore (1+ν_y)dS=(s−1)dx. Direct integration gives, for u=e^{−βy}ψ(x),

Q[u]=(1/(2β))∫e^{−2βf}|∇ψ|²−β∫e^{−2βf}(s−1)|ψ|². (4.1)

This identity includes the boundary Jacobian and has no derivatives of f in the physical-coordinate bulk gradient. Let K=supp f and J_β(f)=∫e^{−2βf}(s−1). If f is nonzero and compactly supported, ∇f is nonzero on a set of positive measure, so J_β(f)>0. For cutoffs equal to 1 near K, their gradients are supported where f=0. Hence

cap_m(K)<2β²J_β(f) (4.2)

is a sufficient binding condition, with homogeneous capacity defined by compactly supported smooth cutoffs equal to 1 near K. In m=1,2 capacity is zero and Theorem A includes this graph conclusion within its larger nongraph scope. In m≥3 this is a sufficient condition only. Failure of (4.2) does not prove absence; the next section supplies a separate lower-bound argument on all functions in the form domain.

## 5. A self-contained Hardy–trace estimate

Assume m≥3 and K⊂closed B_R(0). Put A=4R²/(m−2)². The tangential Hardy inequality gives

∫_K |a(x)|² dx ≤ A∫_{R^m}|∇a|² dx. (5.1)

For completeness, with p_δ=x/(|x|²+δ²) and a₀=(m−2)/2, expand 0≤∫|∇a+a₀p_δa|². Since

div p_δ=((m−2)|x|²+mδ²)/(|x|²+δ²)²,

integration by parts yields ∫|∇a|²≥a₀²∫|x|²/(|x|²+δ²)² |a|². Fatou as δ↓0 proves ∫|a|²/|x|²≤4/(m−2)²∫|∇a|². On B_R, 1≤R²/|x|², proving (5.1). Density extends it from smooth compact support to H¹.

For smooth compactly supported w on R^m×[0,∞), set

E_x=∫_H e^{−2βt}|∇_xw|²,  E_t=∫_H e^{−2βt}|∂_tw|²,  E=E_x+E_t,
L_K=∫_{K×(0,∞)} e^{−2βt}|w|²,  T_K=∫_K|w(x,0)|².

Applying (5.1) at each t gives L_K≤A E_x. Integrating the derivative of e^{−2βt}|w|² gives

T_K=2βL_K−2Re∫_{K×(0,∞)}e^{−2βt} w̄∂_tw
≤2βA E_x+2sqrt(A E_xE_t)
≤(2βA+sqrt A)E. (5.2)

Every coefficient is explicit. The estimate fails in this homogeneous form in m=1,2, exactly where the logarithmic/linear cutoff sequence has energy tending to zero but nonzero local trace. No higher-dimensional stability claim is extrapolated into those dimensions.

## 6. Lower bound on all functions for graph domains

Let M=||f||_∞, G=||∇f||_∞, D=sqrt(1+G²)−1, and

c(G)=1/[2(1+G²)].

For arbitrary u in a form core, flatten y=t+f(x) and define w by

u(x,t+f(x))=e^{−β(t+f(x))}w(x,t).

The unit-Jacobian flattening map yields the exact identity below. For Lipschitz f this does not require a smooth-boundary divergence theorem: use the weak chain rule, write v(x,y)=w(x,y−f(x)), expand ∇(e^{−βy}v), and integrate the term −β∂_y(e^{−2βy}|v|²) over each vertical fiber (f(x),∞). This contributes +βe^{−2βf}|w(x,0)|², which combines with the Robin trace −βsqrt(1+|∇f|²)e^{−2βf}|w(x,0)|². Fubini is legitimate on the compact-support core. Thus

Q[u]=∫_H e^{−2β(t+f)} (|∇_xw−∇f∂_tw|²+|∂_tw|²)
      −β∫_{R^m} e^{−2βf}(sqrt(1+|∇f|²)−1)|w(x,0)|² dx. (6.1)

For every vector a and scalar b, with |g|≤G,

|a|²+|b|²≤2|a−gb|²+(2G²+1)|b|²
≤2(1+G²)(|a−gb|²+|b|²).

Thus the bulk term is at least e^{−2βM}c(G)E. The defect is supported in K=supp f⊂closed B_R and is at most βe^{2βM}D T_K. By (5.2),

Q[u]≥[e^{−2βM}c(G)−βe^{2βM}D(2βA+sqrt A)]E. (6.2)

Consequently the explicit condition

βD e^{4βM}(2βA+sqrt A)≤c(G) (6.3)

implies H_{β,Ω_f}≥−β² on the entire form domain. To justify the last assertion without assuming bounded multiplication by e^{βy} in ordinary H¹, establish (6.1)–(6.2) first for compactly supported w, equivalently for the dense flattened compact-support core of u; the map y=t+f(x) is bi-Lipschitz and e^{−β(t+f)} and its inverse are bounded on each compact support. Pass to all u by H¹ density and continuity of q. The weighted energy need not be invoked outside that core.

The left side of (6.3) tends to zero as β↓0 for each fixed f, while c(G)>0. Therefore (6.3) holds on (0,β₀] for some β₀>0. Combined with the essential-spectrum equality, this proves Theorem B. For f=0 the negative defect vanishes identically; the flat conclusion holds for every β.

## 7. Exact constants for a nontrivial smooth counterexample

Let h and f=h/100 be as specified in Section 1. Standard one-variable differentiation of exp(−1/s), extended by zero for s≤0, proves h∈C∞_c(R^m). It is positive at x=0, so it is nonzero. Its maximum is e^{−1}<1. For r=|x|<1 and q=(1−r²)^{−1}≥1,

|∇h|=2r q²e^{−q}≤2q²e^{−q}≤8/e²<2.

The scalar function q²e^{−q} reaches its maximum at q=2. Therefore M<1/100, G<1/50, D≤G²/2<1/5000. At β=1 and m≥3, R=1 and A≤4, so 2A+sqrt A≤10. Also e^{4M}<e^{1/25}<2, and

βD e^{4βM}(2βA+sqrt A)<(1/5000)·2·10=1/250.

Meanwhile c(G)>1/[2(1+1/2500)]>1/3. Hence (6.3) holds with a margin greater than 1/3−1/250>0. This is an exact analytic certificate. In particular the n=4 instance is a smooth connected, connected-boundary, nonzero compact perturbation for which σ(H_{1,Ω_f})=[−1,∞).

For every prescribed β*>0 one can alternatively use f=εh and choose ε>0 sufficiently small. Thus the failure of universal binding in n≥4 persists at every prescribed coupling, by a nonzero smooth perturbation depending on that coupling.

## 8. Exact conclusions and limitations

1. The dimension-unrestricted original question receives a negative answer from the explicit n=4 graph at β=1. This is not the excluded undeformed half-space.
2. The positive n=2 statement in the standard C⁴ same-line setting was already proved by Exner–Minakov. No novelty is claimed for that case.
3. The argument here proves the full connected smooth compact-perturbation n=3 result, including overhangs and compact extra boundary components. Its scope includes the graph case and extends to nongraph domains.
4. Weak-coupling stability for every compact graph in n≥4 is proved; a classification of every nongraph perturbation in n≥4 at every coupling is not claimed or required for the counterexample.
5. Large-coupling binding under positive maximum mean curvature is compatible with the weak-coupling absence theorem. The sufficient capacity test and sufficient absence test apply in different ranges and have a gap; neither is asserted necessary.
6. The original source does not fix ambient dimension. If a separately documented intended version fixes n=3, Theorem A addresses that version positively. If it fixes n≥4 but a particular graph and every coupling, Theorem B disproves it.
7. Literature novelty is not a mathematical consequence of this proof. The bounded searches and primary-source observations recorded in [SOURCE_METADATA.json](SOURCE_METADATA.json) did not establish that these higher-dimensional statements were already published, but they also do not prove novelty. The [independent mathematical audit](MATHEMATICAL_AUDIT.md) accepts the stated mathematical claims, subject to its explicit scope and review limits.
