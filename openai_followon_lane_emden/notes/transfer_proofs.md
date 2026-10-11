# Conditional Lane–Emden transfer package

Independent transfer audit, 2026-10-06 21:31 PDT (2026-10-07 04:31 UTC).
Author of this audit: automated research subagent, reporting to the lead agent.
This note does **not** certify the upstream entire Liouville theorem.

Checkpoint estimate: conditional transfer proofs 100%; unconditional core
resolution and publication readiness not assessed by this subagent. No Git,
publication, or external communication action was taken here.

## 1. Exact dependency and claimed scope

Fix an integer n≥3 and p,q>1, and define

\[
 \alpha=\frac{2(p+1)}{pq-1},\qquad
 \beta=\frac{2(q+1)}{pq-1}.
\]

The only nonlinear Liouville input for this package is:

**(L)** Every bounded pair U,V∈C²(Rⁿ), U,V≥0, satisfying
−ΔU=Vᵖ and −ΔV=Uᑫ on Rⁿ is identically zero.

The following implications hold for any p,q>1 for which (L) holds. The strict
subcritical inequality is used only in a separately validated proof of (L).
It must not be assumed in place of that proof. In particular, this note does
not promote the unreviewed family-370 claim to an established theorem.

An entire Liouville theorem formulated for strictly positive pairs supplies
(L): each component is nonnegative and superharmonic. If one component
vanishes at one point, the strong minimum principle makes it identically
zero, and its equation then makes the other identically zero. Otherwise
both components are strictly positive. The same dichotomy holds on any
connected open domain. A component cannot vanish identically while its
partner remains nonzero.

**Conditional theorem.** Assuming (L):

1. For every proper open domain Ω⊊Rⁿ and every nonnegative classical pair
   u,v∈C²(Ω) satisfying the system, with no boundary condition or boundary
   regularity assumption, there is C=C(n,p,q) such that, for d(x)=dist(x,∂Ω),
   \[
   u(x)\le C d(x)^{-\alpha},\quad
   v(x)\le C d(x)^{-\beta},\quad
   |\nabla u(x)|\le C d(x)^{-\alpha-1},\quad
   |\nabla v(x)|\le C d(x)^{-\beta-1}.
   \]
   The classical space C²(Ω) is local; no boundedness on Ω is assumed.
2. If Ω contains {x:|x|>R}, R>0, the preceding four bounds hold for
   |x|≥2R with d(x) replaced by |x| (after enlarging C). No condition at
   infinity is assumed.
3. For H={x∈Rⁿ:x_n>0}, the only nonnegative pair
   u,v∈C²(H)∩C(closure H) solving the system with u=v=0 on ∂H is zero.
   Neither global boundedness nor finite-strip boundedness is required.
4. For each fixed bounded domain Ω with C² boundary, all nonnegative pairs
   u,v∈C²(Ω)∩C(closure Ω) solving the system and vanishing on ∂Ω obey a
   uniform L∞ bound C=C(Ω,n,p,q). For every 1<r<∞, they belong to
   W²,r(Ω)∩W¹,r_0(Ω) and have uniformly bounded W²,r norms, with constants
   allowed to depend additionally on r. The solution set including zero is
   sequentially compact in W²,r(Ω)² for every finite r and in
   C¹,γ(closure Ω)² for every 0≤γ<1, with γ=0 meaning the usual C¹ norm.
5. If this fixed domain has C²,θ boundary, with 0<θ<1, there are uniform
   C²,θ(closure Ω) bounds. In particular, the solution set is compact in
   C²,η(closure Ω)² for every 0≤η<θ. Here η=0 denotes the usual C² norm.

The statements are initially for classical solutions. The fixed-domain
assertion also includes pairs u,v∈H¹_0(Ω)∩L∞(Ω) that solve both equations
distributionally: bounded sources and the linear Dirichlet regularity in
Section 7 put them in the same classical class before applying the theorem.
No assertion is made about arbitrary unbounded weak solutions or an
unspecified weak boundary trace on the half-space. The W¹,r_0 notation
denotes zero trace, not zero normal derivative; W²,r_0 would be a different
and incorrect space here.

## 2. Scaling and constants

Direct calculation gives
\[
 p\beta=\alpha+2,\qquad q\alpha=\beta+2,
 \qquad \alpha,\beta>0.
\]
Thus for λ>0 and x₀∈Ω,
\[
 U(y)=\lambda^\alpha u(x_0+\lambda y),\qquad
 V(y)=\lambda^\beta v(x_0+\lambda y)
\]
solves the same system on λ⁻¹(Ω−x₀). The normalization gauge
\[
 M(x)=u(x)^{1/\alpha}+v(x)^{1/\beta}
\]
scales as an inverse length. This choice is essential: an unweighted
u+v normalization would not preserve both equations when α≠β.

Algebra also verifies that the strict subcritical inequality in the brief is
equivalent to α+β>n−2: multiplying positive denominators gives
n(p+q+2)>(n−2)(pq+p+q+1), which rearranges to
2(p+q+2)>(n−2)(pq−1). No equality or supercritical claim is included.

## 3. Interior doubling proof, with convergence spaces

The pointwise u,v estimate is the established PQS transfer [PQS,
Theorem 4.3]. The argument is reproduced to make the normalization and
compactness explicit.

For a nonzero solution on a connected Ω the strong minimum principle gives
M>0, and M is locally bounded. If no universal constant bounded M(x)d(x),
there would be domains Ω_k, solutions (u_k,v_k), and y_k∈Ω_k with
M_k(y_k)d_k(y_k)>2k. The doubling lemma [PQS, Lemma 5.1] gives x_k such that
\[
 M_k(x_k)\ge M_k(y_k),\quad
 M_k(x_k)d_k(x_k)>2k,\quad
 M_k(z)\le 2M_k(x_k)\quad
 (|z-x_k|\le k/M_k(x_k)).
\]
The last ball lies inside Ω_k. Set λ_k=M_k(x_k)⁻¹ and scale at x_k.
On B_k the resulting pair satisfies
\[
 U_k^{1/\alpha}(0)+V_k^{1/\beta}(0)=1,
 \qquad U_k^{1/\alpha}+V_k^{1/\beta}\le2.
\]
Hence U_k≤2^α and V_k≤2^β, with both sources uniformly bounded on B_k.
For every fixed R and 1<r<∞, the interior Poisson estimate gives uniform
W²,r(B_R) bounds once k>R+1. Choosing r>n yields uniform C¹,γ bounds
for every γ<1−n/r. The functions s↦sᵖ,sᑫ are Lipschitz on the bounded
nonnegative amplitude ranges, so the sources have uniform C⁰,γ bounds.
Interior Schauder estimates then give uniform C²,γ bounds on smaller
balls. Diagonal compactness supplies a subsequence converging in
C²_loc(Rⁿ) (indeed C²,γ′ on each fixed ball for γ′<γ) to a bounded
nonnegative classical entire pair.

The normalization passes to the limit by C⁰ convergence, making the limit
nonzero. This contradicts (L). Consequently M(x)≤K(n,p,q)/d(x); raising
each summand bound to its own positive exponent proves the u,v estimates.
One common C may be chosen by taking the larger of K^α and K^β.

This proof needs no relation among different domains, no boundary charts,
and no claim that λ_k→0; the expanding rescaled balls B_k suffice.

## 4. Gradients and exterior decay

The elementary interior Poisson estimate on B_r(x) is
\[
 |\nabla w(x)|\le C_n\left(r^{-1}\|w\|_{L^\infty(B_r(x))}
              +r\|\Delta w\|_{L^\infty(B_r(x))}\right).
\]
For n≥3 this follows by splitting w into its Newtonian potential of the
bounded source on B_r and a harmonic remainder. The gradient of the
potential is bounded by C_nr times the source norm, its value by C_nr²
times that norm, and the harmonic gradient estimate contributes the
first displayed term. Thus no boundary regularity enters this step.

Take r=d(x)/2. On this ball d(y)≥d(x)/2, so the pointwise estimates give
\[
 \sup_{B_r(x)}u\le C d(x)^{-\alpha},\qquad
 \sup_{B_r(x)}v^p\le C d(x)^{-p\beta}
                           =C d(x)^{-\alpha-2}.
\]
The gradient bound for u follows, and the argument for v uses qα=β+2.
Equivalently one may state
u+|∇u|^{α/(α+1)}≤Cd⁻α and
v+|∇v|^{β/(β+1)}≤Cd⁻β, but the separate gradient powers are less
ambiguous. [PQS, Remark 7.4] explicitly mentions the gradient extension;
the calculation above supplies it for these pure powers.

If Ω⊊Rⁿ contains the exterior of B_R, then ∂Ω⊂closure B_R and
d(x)≥|x|−R≥|x|/2 for |x|≥2R. Substituting into all four bounds proves
the claimed exterior decay, with constants still depending only on n,p,q.

## 5. The exact half-space dependency

We invoke [PQS, Theorem 4.2] with the hypothesis (L) exactly as stated.
Its conclusion is zero-Dirichlet nonexistence for nonnegative
C²(H)∩C(closure H) solutions, bounded or unbounded. In the source H uses
the first rather than the nth coordinate; rotation makes this immaterial.

The source does not assume the conjecture as a formal hyperbola condition:
its hypothesis is explicitly absence of bounded nontrivial nonnegative
entire solutions. Therefore a genuinely verified upstream positive entire
Liouville theorem, combined with the strong minimum principle in Section 1,
matches its hypothesis without a hidden boundedness restriction.

For provenance, PQS obtains this from its flat-boundary local estimate
(Proposition 7.1) followed by R→∞. Its flat-boundary blow-up uses the
established bounded half-space reduction to Rⁿ⁻¹, cited there to
Birindelli–Mitidieri (1998) and Dancer (1992). A bounded entire solution in
Rⁿ⁻¹ lifts to Rⁿ by adding a constant coordinate, so (L) in dimension n
does exclude that alternative. This note relies on the published PQS
theorem rather than pretending to provide a new proof of moving planes.

Modern stronger half-space results exist, as recorded by the independent
priority audit. None is needed for this conditional package.

## 6. Fixed-domain blow-up: the boundary argument that distance bounds omit

Let Ω be fixed, bounded, and of class C². A classical pair continuous up
to ∂Ω is bounded for each individual solution, but its bound may initially
depend on that solution. Suppose a uniform bound fails. Choose solutions
for which
\[
 m_k=\max_{\overline\Omega}
       \bigl(u_k^{1/\alpha}+v_k^{1/\beta}\bigr)\longrightarrow\infty.
\]
Zero boundary values imply that a maximizing x_k lies in Ω. Put
λ_k=m_k⁻¹→0, d_k=dist(x_k,∂Ω), and δ_k=d_k/λ_k. Scale at x_k.
The scaled pair obeys gauge≤1 on its whole scaled domain and gauge=1
at the origin.

### Interior case

If δ_k→∞, every fixed ball around the scaled origin lies in the domain
eventually. The same W²,r/Schauder compactness argument as Section 3 yields
a bounded nonzero entire classical pair, contradicting (L).

### Boundary case: charts and spaces

Otherwise take a subsequence with δ_k→δ∈[0,∞). Then d_k→0 and x_k
approaches ∂Ω. Choose a nearest boundary point z_k and an orthogonal Q_k
which maps e_n to the inward normal at z_k. For k large the fixed C²
domain has a uniform tubular neighborhood, so
x_k=z_k+d_k Q_ke_n. Centering at z_k instead of x_k gives
\[
 \widehat U_k(y)=\lambda_k^\alpha
       u_k(z_k+\lambda_k Q_ky),\qquad
 \widehat V_k(y)=\lambda_k^\beta
       v_k(z_k+\lambda_k Q_ky).
\]
Their maximum occurs at ξ_k=δ_ke_n, with gauge 1 there and gauge≤1
everywhere.

In these coordinates a uniform boundary chart is x_n>ρ_k(x′), with
ρ_k(0)=0, ∇ρ_k(0)=0 and a uniformly bounded C² norm. The scaled graph is
ψ_k(y′)=λ_k⁻¹ρ_k(λ_ky′). On every fixed disk,
\[
 \|\psi_k\|_\infty=O(\lambda_k),\quad
 \|\nabla\psi_k\|_\infty=O(\lambda_k),\quad
 \|D^2\psi_k\|_\infty=O(\lambda_k).
\]
Thus the domains converge to H in C² on fixed compact charts. The local
chart radius tends to infinity after scaling, and no other boundary part
enters a fixed compact set.

Flatten using T_k(t)=(t′,t_n+ψ_k(t′)). The pullbacks
W_k=Û_k∘T_k and Z_k=V̂_k∘T_k vanish on t_n=0. Their equations have
uniformly elliptic principal coefficients a_k→I and bounded first-order
coefficients b_k→0 uniformly on compact sets; in graph coordinates a_k
depends on ∇ψ_k and b_k on D²ψ_k. Importantly, a fixed C² boundary does
**not** provide a uniform Hölder seminorm for D²ψ_k. This step therefore
uses local boundary W²,r estimates, not an unjustified boundary Schauder
estimate at C² regularity.

For every fixed R and finite r>1 these boundary estimates, together with
the bounded sources and gauge≤1, give uniform W²,r bounds on a smaller
half-ball. Constants are uniform because the scaled charts have uniformly
controlled C¹,¹ norms (in fact their second derivatives tend uniformly to
zero). There is no estimate near the artificial curved edge of that
half-ball; a nested-half-ball estimate avoids the edge.

For r>n, Sobolev embedding gives uniform C¹,γ bounds on compact subsets
of closure H for γ<1−n/r. A diagonal subsequence converges in C¹_loc up
to the flat boundary, and weakly in W²,r_loc. Passing to the flattened
equations is justified by a_k→I, b_k→0, strong C⁰ convergence of W_k,Z_k,
and weak convergence of the second derivatives. The limit U,V satisfies
−ΔU=Vᵖ, −ΔV=Uᑫ distributionally on H and is zero on ∂H. Interior
regularity makes it C²(H); its uniform C¹_loc convergence up to the
boundary gives continuity there. Gauge≤1 makes it globally bounded.

Because ψ_k(0)=0, T_k(δ_ke_n)=δ_ke_n. Consequently strong C⁰ convergence
on a compact half-ball containing these points gives
\[
 U(\delta e_n)^{1/\alpha}+V(\delta e_n)^{1/\beta}=1.
\]
If δ=0 this contradicts the zero boundary trace. If δ>0 the limit is
nontrivial, contradicting the exact half-space theorem in Section 5. Both
alternatives are impossible, establishing the uniform bound for m_k and
hence for u,v.

This is the missing argument if one merely integrates or maximizes the
arbitrary-domain distance estimate: that estimate diverges as d→0 and
alone does not control peaks at distances comparable to their blow-up
scale.

## 7. Fixed-domain regularity and compactness

The linear estimates used here are the standard Dirichlet Poisson
W²,r theory on bounded C¹,¹ (and hence C²) domains and the Schauder theory
on C²,θ domains. The exact assertions needed are:

* For finite 1<r<∞, −Δ:W²,r(Ω)∩W¹,r_0(Ω)→Lʳ(Ω) is invertible, and
  \[\|w\|_{W^{2,r}}\le C(\Omega,n,r)\|\Delta w\|_{L^r}.\]
* Their localized boundary form bounds W²,r on a smaller patch by the
  Lʳ norms of the function and its source on a larger patch, when the
  function has zero trace on the physical boundary portion. Constants are
  uniform over the C¹,¹ charts occurring in Section 6.
* On a C²,θ domain, a zero-boundary solution with source f∈C⁰,θ satisfies
  \[\|w\|_{C^{2,\theta}}\le
    C(\Omega,n,\theta)(\|w\|_{C^0}+\|f\|_{C^{0,\theta}}).\]

A standard reference is Gilbarg–Trudinger, *Elliptic Partial Differential
Equations of Second Order*, 2nd edition/reprint 2001, Chapters 6 and 9,
DOI https://doi.org/10.1007/978-3-642-61798-0. The book's bibliographic
identity was checked against its publisher; no claim is made here that a
subscription-only full book or every proof in it was reproduced.

There is a small regularity point for our initial class C²(Ω)∩C(closure Ω).
For a bounded continuous source, first solve the linear Dirichlet problem
in W²,r with r>n. This solution is continuous on closure Ω. Its difference
from the given classical solution is harmonic, continuous up to ∂Ω, and
zero there, so the maximum principle identifies them. This upgrades the
given solution to the global W²,r class. Other finite r follow from the
same linear theorem or compatibility/uniqueness.

Uniform L∞ bounds make uᑫ,vᵖ uniformly bounded, so the global linear
estimate yields the claimed uniform W²,r bounds. Given a sequence, choose
r sufficiently large to obtain a subsequence converging in C¹,γ for any
specified γ<1 (use a slightly larger embedding exponent to get compactness).
Uniform convergence makes the powers converge uniformly, and the limit is
again nonnegative, zero on the boundary, and a weak solution. Interior
elliptic bootstrapping makes it classical. Applying the global estimate to
the differences gives
\[
 \|u_k-u\|_{W^{2,r}}\le C_r\|v_k^p-v^p\|_{L^r}\longrightarrow0,
\]
and similarly for v, for every finite r. Thus the convergence is strong in
W²,r, not merely weak. A diagonal subsequence can give all exponents
simultaneously; no claim at r=∞ or γ=1 is needed.

On C²,θ domains, W²,r for large r gives uniformly bounded C¹ norms.
On the fixed bounded amplitude range, sᵖ,sᑫ are Lipschitz, so the sources
have uniformly bounded C⁰,θ norms for every θ<1. Schauder estimates give
the uniform C²,θ bound, and the compact embedding into C²,η for η<θ
gives the stated compactness. C² boundary alone is sufficient for L∞,
W²,r, and C¹,γ assertions; C²,θ is the explicit stronger hypothesis for
the Schauder assertions. This note does not claim C²(closure Ω) from
merely C² boundary.

## 8. Attribution and optional perturbations

All the nonlinear transfer mechanisms are inherited. PQS established the
conditional whole-space, arbitrary-domain, exterior, and half-space
statements in 2007. Quittner–Souplet, *Liouville theorems and universal
estimates for superlinear elliptic problems without scale invariance*,
Rev. Mat. Complutense 38 (2025), 1–69, arXiv:2407.04154v2,
Theorem 4.1(ii), explicitly states fixed-domain zero-Dirichlet bounds for
uniformly regular C² domains under the pure-power Liouville input.
Its Remark 4.1(ii) attributes the p,q>1 pure-power case to PQS2007.
Its Section 7.2 points to the boundary blow-up mechanism and PQS4.2.
Thus neither fixed-domain blow-up nor elementary regularity compactness
should be presented as a new independent solution of Lane–Emden.

[PQS, Theorem 7.3] additionally assumes continuous f,g:[0,∞)→R with
f(s)/sᵖ→ℓ₁>0 and g(s)/sᑫ→ℓ₂>0 as s→∞. Under (L) it concludes
u≤C(n,f,g)(1+d⁻α), v≤C(n,f,g)(1+d⁻β), even when f,g have arbitrary
behavior on bounded argument ranges. These are already established
perturbation transfers, not new results. This note does not promote a
spatially varying coefficient theorem by analogy.

For checking the asymptotic limit, the constant-coefficient system
−ΔU=ℓ₁Vᵖ, −ΔV=ℓ₂Uᑫ reduces to the unit-coefficient system by
\[
 \widehat U=(\ell_1\ell_2^p)^{1/(pq-1)}U,
 \qquad
 \widehat V=(\ell_2\ell_1^q)^{1/(pq-1)}V.
\]
Positive constants are essential for this matching. Additive 1 terms
cannot be removed merely by citing Theorem 7.3.

## 9. Source provenance and audit boundary

PQS source requested in the brief:
https://www-users.cse.umn.edu/~polacik/Publications/pqs1.pdf

Local files: `sources/pqs1.pdf`, `sources/pqs1.txt`.
Downloaded 2026-10-06 PDT. PDF SHA-256:
`3c647b8f01e277812a2d3c7974d48ddb91695b7aa350d19f52a6449d15811ee6`.
Text was extracted using the locally available pdftotext utility.
The downloaded PDF is an author-hosted 22-page preprint, with some
references marked preprint/to appear; it is not visibly the typeset final
Duke journal version. Exact statements inspected: Theorems 4.1–4.3,
Lemma 5.1, Proposition 7.1, Theorem 7.3, Remark 7.4, and their displayed
proofs. Journal citation: Duke Math. J. 139 (2007), no. 3, 555–579,
DOI https://doi.org/10.1215/S0012-7094-07-13935-8.

Modern QS primary source, supplied locally by the priority-audit subagent:
`sources/priority_qs2407v2.pdf` and `.txt`; inspected Theorem 4.1,
Remark 4.1(ii), Section 7.2, and the initial strong-solution definition.

No third-party PDFs are recommended for the public upload kit without
redistribution permission. References/URLs/hashes suffice.

The precise remaining gap for an unconditional all-subcritical theorem is
a validated proof of (L) throughout that range. The present transfer note
does not shift or solve that gap. If the upstream entire theorem fails
audit, the arbitrary-domain, full half-space, and fixed-domain claims here
remain a conditional package, with only independently established
Liouville exponent regions becoming unconditional.
