# Direct projector splitting for stiff matrix equations: an obstruction and conditional bounds

Problem 30003094, queue row 1829, OWR-14226-001. Research date: 20 October 2026.

## Status and scope

**PARTIAL PROGRESS; original question remains unresolved in its full, unspecified PDE scope.** We prove an obstruction to a natural unrestricted extension of the original robust bound, and give precisely delimited positive results for the original method. We do not replace the open question by an invented universal conjecture, claim a new literature priority, or claim that fixed smooth PDE data with exact spatially projected initialization must fail.

The original request concerns extending the error analysis of the direct, fixed-rank tangent-projector splitting to spatial discretizations of PDEs. It specifies no PDE, spatial order, boundary conditions, or regularity class. The 2019 stiff/nonstiff method is different: it applies projector splitting only to the nonstiff term, then applies the stiff semigroup. Its theorem cannot simply be relabeled a theorem for the original method.

The main new calculation here is a full-step, **exact-subflow** counterexample, not instability of an approximate backward S solver. Contractive analytic semigroups, small uniformly bounded forcing and normal defect, and small initial error in the underlying Hilbert norm alone do not give a stiffness-uniform robust convergence estimate for direct K–S–L. A two-sided example satisfies the stated hypotheses of the 2019 theorem and sharply distinguishes its modified method from the direct one.

See `SUBCLASS_BOUNDS.md` for a direct-method conditional global error theorem and a concrete periodic Fourier-Galerkin PDE corollary. The conditions include numerical-subspace regularity and are not claimed automatic.

## 1. Method and notation

All mathematical arguments below use finite-dimensional real matrices and the Frobenius norm; complex versions replace transposes by adjoints. Let Y=USVᵀ have rank r, orthonormal U,V and invertible S. Its tangent projector is

P(Y)Z = ZVVᵀ − UUᵀZVVᵀ + UUᵀZ.

An exact direct K–S–L step of length τ for X′=F(X), starting from U₀S₀V₀ᵀ, is:

1. K′=F(KV₀ᵀ)V₀, K(0)=U₀S₀; factor K(τ)=U₁ Ŝ.
2. S′=−U₁ᵀF(U₁SV₀ᵀ)V₀, S(0)=Ŝ; write S̃=S(τ).
3. L′=F(U₁Lᵀ)ᵀU₁, L(0)=V₀S̃ᵀ; return Y₁=U₁L(τ)ᵀ.

The final QR does not change the returned matrix. We assume the required QR ranks are maintained. Every counterexample below has a positive first K component and nonzero final rank for every integer n≥2 in its displayed sequence, and for sufficiently large stiffness in its fixed-τ limit. Thus no rank-deficient QR choice is used.

Kieri–Lubich–Walach, SIAM J. Numer. Anal. 54 (2016), 1020–1038, §2.2 supplies this method. The OWR summary's K equation drops its terminal V₀, a dimensional typo corrected by the cited paper. Theorem 2.1 gives c₀δ+c₁ε+c₂τ for **both** Lie and Strang, with constants depending on the full-field Lipschitz and boundedness constants. It is not a robust second-order theorem.

Primary sources:
- Original report: https://ems.press/journals/owr/articles/14226 and https://ems.press/content/serial-article-files/46621, printed pp. 910–912.
- Original robust ODE analysis: https://doi.org/10.1137/15M1026791; published text at https://www.diva-portal.org/smash/get/diva2%3A874116/FULLTEXT01.pdf.
- Modified stiff splitting: https://doi.org/10.1137/18M1177901 and https://arxiv.org/html/1803.10473v2.

## 2. Exact endpoint identity for right-affine equations

**Lemma 1.** Suppose F(Y)=YB+C with constant B,C. Let U₁ be the K-step endpoint basis, of full column rank r, and P₁=U₁U₁ᵀ. Then the original direct exact-subflow KSL step satisfies

Y₁ = P₁ Φτ(Y₀),

where Φτ(Y₀)=Y₀e^{τB}+∫₀^τ Ce^{sB} ds is the exact full affine flow.

**Proof.** Set B₀=V₀ᵀBV₀ and D=U₁ᵀCV₀. The K equation is K′=KB₀+CV₀. Consequently Q(t)=U₁ᵀK(t) satisfies Q′=QB₀+D, and Q(τ)=Ŝ. The S equation S′=−SB₀−D is the exact inverse autonomous affine flow for the same elapsed time. Hence S̃=Q(0)=U₁ᵀU₀S₀. The last equation, written for Lᵀ, is (Lᵀ)′=LᵀB+U₁ᵀC. Thus

L(τ)ᵀ = U₁ᵀY₀e^{τB}+∫₀^τ U₁ᵀCe^{sB} ds.

Multiplication by U₁ proves the identity. ∎

If B+Bᵀ≤0, the output norm is at most ||Y₀||+τ||C||. Thus even this norm-stable full method can be grossly inaccurate uniformly in stiffness: stability alone is not convergence. The dangerous effect is the selection of the wrong column space during K, not exponential blow-up of the final result.

## 3. A rank-one counterexample with dissipative right stiffness

Take m=n=2, rank r=1, standard basis e₁,e₂, and

Bλ=diag(0,−λ),  Cη=η e₂e₁ᵀ,  v=(e₁+e₂)/√2,  Y₀=e₁vᵀ,

with λ,η,τ>0. The exact full solution is

X(τ) = [[1/√2, e^{−λτ}/√2], [ητ, 0]].

Here b=vᵀBλv=−λ/2, so the K endpoint is

k = e^{−λτ/2}e₁ + (√2η/λ)(1−e^{−λτ/2})e₂.

Let u=k/||k||. Lemma 1 gives Y₁=uuᵀX(τ) exactly. At fixed τ,η>0, as λ→∞,

u→e₂,  Y₁→ητ e₂e₁ᵀ,  X(τ)→(e₁/√2+ητe₂)e₁ᵀ,

and therefore

lim ||Y₁−X(τ)|| = 1/√2.

For a simultaneous small-error sequence, put λ=n² and τ=η=1/n. Then

[e^{−λτ/2}]/[(√2η/λ)(1−e^{−λτ/2})] = n³e^{−n/2}/[√2(1−e^{−n/2})] → 0,

so the same error limit holds although τ+η→0. Initial error is zero for this comparison.

The linear term YBλ is tangent to every fixed-rank manifold. At every rank-one Y=usvᵀ,

||(I−P(Y))Cη|| = ||(I−uuᵀ)Cη(I−vvᵀ)|| ≤ η.

Thus the normal/tangency remainder has a global bound ε=η, while ||Cη||=η and its state derivative vanishes. The full semigroup is contractive and analytic with constants independent of λ. There can be no bound of the form C₀δ+C₁ε+C₂τ, or C₀δ+C₁ε+C₂τ(1+|log τ|), with constants and a step threshold determined solely by these uniform bounds, a bounded initial norm, and a fixed final time. The contradiction already occurs at the first grid point, which belongs to any fixed interval [0,T] for all sufficiently large n.

This is an obstruction to that **specified unrestricted estimate**, not a disproof of every PDE-compatible error theorem. In the zero-initial-error version, the data contain a high spatial mode of nonvanishing amplitude and have unbounded spatial graph norms as λ grows.

## 4. Stronger initialization variant: a smooth exact target and vanishing rough error

Let αₙ=n^{−1/4}, cₙ=√(1−αₙ²), vₙ=(cₙ,αₙ)ᵀ, λₙ=n², τₙ=ηₙ=1/n, for n>1. Use the same B and forcing C, but initialize the numerical method with

Y₀,ₙ=e₁vₙᵀ.

Compare it with the exact solution initialized at the **fixed** matrix X₀=e₁e₁ᵀ. Then

δₙ=||Y₀,ₙ−X₀||=√(2−2cₙ)→0,

and the exact target solution is

Xₙ(t)=(e₁+ηₙt e₂)e₁ᵀ,

which has rank exactly one and is uniformly smooth in the spatial embedding below. Thus the target does not intrinsically need any rank truncation.

For the numerical K equation,

bₙ=−λₙαₙ²=−n^{3/2},

kₙ=e^{−√n}e₁ + n^{−5/2}cₙ(1−e^{−√n})e₂.

Hence its normalized direction uₙ tends to e₂. By Lemma 1, Y₁,ₙ is the uₙ-projection of the full solution starting from Y₀,ₙ. That latter solution at τₙ is

[[cₙ, αₙe^{−n}], [n^{−2}, 0]].

It tends to e₁e₁ᵀ, while its uₙ-projection tends to zero. Therefore

||Y₁,ₙ−Xₙ(τₙ)|| → 1,

although δₙ+εₙ+τₙ→0 with εₙ=ηₙ.

This strengthens the scope of the obstruction: strong convergence of the initial approximations in the underlying Hilbert norm, and even a smooth rank-one exact target, do not suffice for a uniform estimate that permits arbitrary norm-small initialization errors. It does **not** show failure when the numerical initialization is the exact spatial projection of that fixed smooth datum. Its vanishing initialization errors are spatially rough: ||Y₀,ₙBλₙ|| is unbounded. The forcing shape is fixed and smooth, but its amplitude ηₙ varies.

### A cleaner parameter sequence

The same conclusion follows with αₙ=1/n, cₙ=√(1−n⁻²), λₙ=n⁴, and τₙ=ηₙ=1/n. Then δₙ=√(2−2cₙ) is asymptotic to 1/n, and

kₙ=e^{−n}e₁+(cₙ/n³)(1−e^{−n})e₂.

Its normalized direction again tends to e₂, while the exact flow from the numerical initializer tends to e₁e₁ᵀ. Therefore the same error limit one holds with δₙ+εₙ+τₙ=O(1/n). In the Fourier embedding this corresponds to the integer high frequency N=n², not N=n. The graph norm is ||Y₀,ₙBλₙ||=n³. This alternative is also useful for the symmetric-composition calculation in STRANG_OBSTRUCTION.md.

### The exact rank-one projected dynamics does not break down

For either right-affine family, start the exact rank-one dynamical approximation at Y₀=e₁v₀ᵀ with v₀=(c,α)ᵀ, c>0, α>0. Write Y(t)=s(t)u(t)v(t)ᵀ with unit u,v and initial s=1, u=e₁. A standard orthogonal gauge gives

u′=(I−uuᵀ)C v/s,
s′=s vᵀBv+uᵀC v,
v′=(I−vvᵀ)(Bᵀv+Cᵀu/s).

For B=diag(0,−λ), C=ηe₂e₁ᵀ these equations preserve the nonnegative quadrants while s>0. Explicitly,

u₁′=−ηu₁u₂v₁/s,  u₂′=ηu₁²v₁/s,
v₁′=λv₁v₂²+ηu₂v₂²/s,
v₂′=−λv₁²v₂−ηu₂v₁v₂/s.

The (1,1) entry of the projected matrix equation satisfies

Y₁₁′=ηu₁u₂v₂²≥0.

Consequently s(t)=||Y(t)||≥Y₁₁(t)≥c. Also s′≤η, so s(t)≤1+ηt. The factor equations therefore remain regular on every fixed finite interval for each λ; compactness of the unit factors and these bounds exclude finite-time breakdown. Along the smoother-target sequences cₙ stays bounded away from zero.

If X_Y denotes the exact full affine solution with the same initializer, E=Y−X_Y obeys

E′=EB−(I−P(Y))C,  E(0)=0.

The normal remainder is at most η and the right semigroup is contractive, so variation of constants gives ||Y(t)−X_Y(t)||≤ηt. Relative to the fixed-target solution in the initialization variant, the bound is δ+ηt. Thus the order-one direct-step error is not forced by loss of rank or order-one modeling error in the exact dynamical approximation.

## 5. A fully two-sided parabolic example with nonvanishing output singular value

To compare directly with the published semilinear Lyapunov form, take

Aλ=Bλ=diag(0,−λ),  Cη=ηI₂,  Y₀=vvᵀ,  v=(1,1)ᵀ/√2,

and F(Y)=AλY+Y Aλ+Cη. Again r=1 and all subflows are exact.

Put E=e^{−λτ/2}. The K endpoint and normalized vector are

k₁=[E+2η(1−E)/λ]/√2,
k₂=[E³+2η(1−E³)/(3λ)]/√2,
u=k/||k||.

Define a=−λu₂², b=−λ/2, q=a+b, d=η(u₁+u₂)/√2 and ŝ=||k||. Direct integration gives

s̃=e^{−qτ}(ŝ+d/q)−d/q,

L(τ)=e^{τ(Aλ+aI)}v s̃+∫₀^τ e^{s(Aλ+aI)}ηu ds.

Although the S value can be enormous, cancellation in the subsequent L step is retained in the following exact identity. From k′(τ)=(Aλ+bI)k+Cηv,

q ŝ+d=uᵀk′(τ),

and therefore

L(τ)=e^{τ(Aλ−bI)}v [uᵀk′(τ)/q] −e^{τ(Aλ+aI)}v d/q +∫₀^τ e^{s(Aλ+aI)}ηu ds.

At fixed τ,η>0, u→(3,1)ᵀ/√10, a/λ→−1/10 and q/λ→−3/5. The last two terms vanish. Since

k′(τ)=((−λ/2+η)E, (−3λ/2+η)E³)ᵀ/√2,

the first component of the first term tends to 5u₁/12, while its second component tends to zero. Consequently

Y₁=uL(τ)ᵀ → [[3/8,0],[1/8,0]].

The exact full solution is

X(τ)=[[1/2+ητ, e^{−λτ}/2], [e^{−λτ}/2, e^{−2λτ}/2+η(1−e^{−2λτ})/(2λ)]],

so the limiting error is

√[(1/8+ητ)²+(1/8)²] ≥ 1/(4√2).

For λ=n², τ=η=1/n the same endpoint and error limits follow because n³e^{−n/2}→0 and aτ→−∞. The initial nonzero singular value is 1, and the limiting numerical singular value is √10/8>0. Thus neither an initially small singular value nor a vanishing output singular value is necessary for this failure; the internal K factor does become small.

### Exact low-rank target and the 2019 comparison

For symmetric rank-one Y=suuᵀ, projection of ηI gives ηuuᵀ. The exact rank-one dynamical approximation exists globally: let

r(t)=||e^{tAλ}v||²,  u(t)=e^{tAλ}v/√r(t),
s(t)=r(t)[1+η∫₀^t r(z)^{−1} dz].

Then s(t)>0, u′=(I−uuᵀ)Aλu, and s′=2(uᵀAλu)s+η. The trajectory is a valid rank-one solution for every finite λ on any finite [0,T]. Its stiff limit agrees with the correct slow component, 1/2+ηt. The order-one numerical error above is consequently a splitting effect, not forced by a large best rank-one approximation error.

The assumptions stated in Ostermann–Piazzola–Walach (2019), §4, are satisfied uniformly for this family:

- e^{tAλ}Ze^{tAλ} is contractive in Frobenius norm, with ω=0.
- The generator on entries has eigenvalues 0,−λ,−λ,−2λ. Since x e^{−tx}≤1/(et), its smoothing estimate holds with C_s=1/e, independently of λ.
- G(Y)=ηI₂ is C¹ with derivative zero and ||G||=√2η≤√2 for 0<η≤1.
- Its normal defect is at most η globally on rank-one matrices, because each of I−uuᵀ and I−vvᵀ has rank one and operator norm one.
- Initial error is zero and the exact full and exact rank-one solutions exist on [0,T]. No uniform bound on AλY₀+Y₀Aλ or higher initial spatial regularity is required in that theorem's stated assumptions.

That paper's modified scheme applies KSL only to G, then the exact two-sided linear flow. Here its G step is exactly (1+ητ)vvᵀ because v is an eigenvector of I. Its complete output is

(1+ητ)e^{τAλ}vvᵀe^{τAλ}.

The slow-component discrepancy is O(ητ), not order one. The theorem's Cτ(1+|log τ|)+Cδ+Cε bound is therefore consistent with this calculation and is **not** a bound for the unchanged direct full-F KSL.

## 6. Honest PDE embeddings and the norm

Use an orthonormal real Fourier basis on the periodic torus (0,2π), with f₀=1/√(2π) and f_N=cos(Ny)/√π. Coefficient Frobenius norm is exactly the function L² norm; no grid-dependent unweighted sample norm is being passed off as L².

For the right-sided examples, consider

∂ₜz=∂²_y z+η g₁(x)f₀(y)

on the two-dimensional torus, where g₀,g₁ are fixed orthonormal smooth x modes. Take y Fourier-Galerkin cutoff N, and identify the active right modes f₀,f_N and left modes g₀,g₁. The Galerkin operator on the active block is B=diag(0,−N²). All other Galerkin coefficients remain zero both in the exact equation and the KSL substeps. Thus the 2-by-2 calculation is an exact invariant block of a standard increasing-dimensional spatial spectral discretization, not a two-dimensional matrix with no PDE interpretation.

Section 3 uses initial data g₀(x)[f₀(y)+f_N(y)]/√2, a bounded but not strongly convergent and not uniformly spatially smooth family.

Section 4 uses the fixed smooth exact initial datum g₀(x)f₀(y) and a rank-one numerical initialization g₀(x)[c_N f₀(y)+α_N f_N(y)]. Its L² error tends to zero, but its high-mode derivative norm diverges. The exact target is [g₀(x)+η_N t g₁(x)]f₀(y), and is exactly represented by every sufficiently large Galerkin space: its spatial discretization error is zero. It remains inappropriate to call the numerical initializer the exact projection of the target datum.

For Section 5, use the two-dimensional heat equation ∂ₜz=(∂²_x+∂²_y)z+η(f₀⊗f₀+f_N⊗f_N), with the active two-mode block in both coordinates and initial data (f₀+f_N)⊗(f₀+f_N)/2. This is a bounded data family with nonuniform spatial derivatives; here the forcing's high-frequency shape also varies with N. It satisfies uniform analytic-semigroup and bounded-forcing assumptions, not uniform spatial smoothness.

The bound η for the two-sided normal remainder holds on the active 2-by-2 block and along its embedded rank-one trajectory. On arbitrary rank-one matrices elsewhere in the larger Galerkin space, the universally safe bound is ||C||=√2η instead. Both are uniform and vanish along the counterexample sequence; no claim of a global η bound on all larger-space rank-one matrices is needed.

A separate positive theorem must specify which such roughness is excluded. Requiring smoothness of the target alone does not exclude the initialization perturbation in Section 4; one also needs appropriate control of the numerical initialization or a theorem that handles it differently.

## 7. Checks and boundaries

The analytic identities and limits above are the proofs. The following executable checks are corroboration only:

- `check_affine_counterexample.py` evaluates the two-sided affine example with arbitrary precision, both as literal three-subflow formulas and a cancellation-aware rearrangement. At n=1000 (λ=10⁶, τ=η=10⁻³), the error is approximately 0.1767773985, approaching 1/(4√2). The precision is increased with stiffness to avoid treating floating-point cancellation as a counterexample.
- `check_subclass_identities.py` checks 24 seeded rank-two examples, including initial retained singular values down to 10⁻⁸: separable homogeneous exactness, the right-affine projection identity, the left-affine endpoint identity, and the conditional local bound. Maximum identity discrepancies were below 6×10⁻¹⁶. These tests are not a substitute for the proofs.
- `STRANG_OBSTRUCTION.md` proves that standard KSL-half/LSK-half Strang has the same order-one error against the smooth target with rough initialization. Its LSK endpoint identity and complete exact-subflow composition are checked by `check_strang_obstruction.py`. This is a first-order stiff-uniform obstruction under the same weak assumptions, not a general second-order theorem.
- A fresh independent mathematical audit is recorded separately in `AUDIT_COUNTEREXAMPLE.md` when present. Its result, rather than its mere existence, governs acceptance.

The five distinct mathematical approaches and their limits are summarized in `FIVE_AVENUE_SUMMARY.md`. We did not prove a robust general theorem for a two-sided nonlinear parabolic PDE, a spatially unrestricted hyperbolic PDE, tensor formats, adaptive ranks, numerically inexact subflows, or second-order Strang convergence. No queue edit or publication was performed by this research task.
