# Independent source, topology and quotient review of PR 463

Reviewer: `/root/pr463_source_topology`. Problem: 6000016 / AMR-059-0016, Stability of Hessian Metrics. Reviewed frozen PR head: `982fcf87d60c9f8d4ec853d5dd5f4ad6021a6649`. This family checks the mathematical target and deformation mechanism. It does not certify historical priority, readiness of a future preprint, or permission to publish.

**Verdict: PASS for the source/topology family.** The proposed torus connections are genuine arbitrarily small smooth affine deformations of a compact positive-definite Hessian manifold. Every noncentral connection fails to admit any positive-definite Hessian metric. The argument addresses the unrestricted printed question; it does not address a hyperbolic, fixed-linear-holonomy or indefinite reformulation. No blocking issue, required repair or mathematical gap was found in this family's scope.

## 1. Independence and frozen input

`INITIAL_INTERPRETATION.md` was written before reading the supplied `PROOF.md`, the historical `audit/AUDIT_REPORT.md`, or any new peer verdict. The supplied `SOURCE_GATE.md` located the primary papers. The primary PDFs were independently downloaded and the relevant complete pages were rendered and visually inspected. The historical audit report and all new peer verdicts have not been read for this review. The root's source receipt was read only after the independent derivations, to bind the eligible head and check source integrity.

The supplied proof was then read in full. Its SHA-256 is `783f927e0e1bcc309547ad58371a64aeb4428553bfc329df22c980a2b8f0bdb0`. All 14 frozen attempt files were checked byte-for-byte against the root's source receipt without relying on their verdicts. The exact eligible status is `claimed_solved`, at 1/5 attempts. No snapshot, queue row, Git index, branch, service record or peer output was modified. This was verification, with zero new original proof-search attempts.

## 2. Printed target and definitions

Furuhata, Matsuzoe and Urakawa's 1998 source attributes item 5 to Satoru Shimizu. Item 5(b), printed p. 126, asks whether every sufficiently small deformation of the affine structure of a compact Hessian manifold still admits a Hessian metric. It separately records the affirmative hyperbolic case, characterized by a convex developing domain containing no complete straight line. No fixed-holonomy, nonflatness or excluded-dimension condition appears. Item 5(c)'s explicit inclusion of flat compact Hessian manifolds also confirms that the central flat torus is an admissible source example. The workshop occurred in December 1996; 1998 is the publication year. [Original source](https://www.jstage.jst.go.jp/article/iis/4/2/4_2_125/_pdf/-char/en).

The positive-definite, local-potential meaning is independently verified in Shima's 1995 introduction, printed p. 735: a Hessian metric is a Riemannian metric locally equal to the affine Hessian of a smooth function. A global function on the compact manifold is not required. [Primary definition](https://www.jstage.jst.go.jp/article/jmath1948/47/4/47_4_735/_pdf/-char/en).

Koszul's 1968 paper, pp. 103-104, gives a compact-open topology on flat torsion-free connections and an openness result for hyperbolic connections. Its compact characterization uses a global closed one-form with positive covariant derivative; this is stronger than the local-potential condition used here. Its domain excludes complete lines. [Primary paper](https://numdam.org/item/10.5802/aif.279.pdf), DOI [10.5802/aif.279](https://doi.org/10.5802/aif.279). No proof of Koszul's general theorem is needed for the counterexample.

The exact falsifiable claim under review is therefore:

> There exists a compact smooth manifold with a central positive-definite Hessian affine structure and arbitrarily small smooth flat torsion-free affine deformations admitting no positive-definite Hessian metric whatsoever.

The claim is existential and disproves an unrestricted universal stability assertion. It is not a classification of Hessian manifolds or a negative answer inside the hyperbolic subclass.

## 3. Independent construction on the fixed smooth torus

Set `T² = R²/Z²`, with global commuting vector fields `X = ∂x`, `Y = ∂y` and global one-forms `dx`, `dy`. Angular coordinate functions are only local; these vectors and forms descend because translations preserve them. The connection

\[
D_t=D_0+t\,dx\otimes dx\otimes Y
\]

is globally defined: the difference of two connections is a tensor, and the added tensor descends under integer translations. In this global frame its only nonzero coefficient is

\[
(\Gamma_t)^y_{xx}=t.
\]

The symmetry of the two input indices gives torsion zero. The derivative terms in curvature vanish since the coefficient is constant. Every quadratic curvature term has two connection coefficients; a nonzero first factor forces an intermediate `y` index, whereas every coefficient having a lower `y` index vanishes. Thus curvature is identically zero for every real `t`, including both signs and zero. This proves that each `D_t` defines an affine structure, rather than merely a torsion-free nonflat statistical connection.

An independent developing-map reconstruction yields the same connection. On the universal cover let

\[
F_t(x,y)=(u,v)=(x,y+tx^2/2).
\]

Its inverse is `F_{-t}`, its Jacobian determinant is one, and its derivative matrix is

\[
J_t=\begin{pmatrix}1&0\\tx&1\end{pmatrix}.
\]

For a pullback of the standard affine connection,

\[
\Gamma^k_{ij}=(J_t^{-1})^k{}_a\,\partial_i\partial_j(F_t)^a.
\]

The only nonzero second derivative is `(0,t)` in the `xx` slot; its image under `J_t^{-1}` is again `(0,t)`. Therefore `F_t^*D_{mathrm{std}} = D_t`, with the sign and factor `1/2` checked independently.

### Equivariance, quotient and completeness

For `(m,n) ∈ Z²`, define

\[
\rho_t(m,n)(u,v)=(u+m,\ v+n+tm u+tm^2/2).
\]

Expanding the quadratic polynomial gives

\[
F_t(x+m,y+n)=\rho_t(m,n)F_t(x,y).
\]

Composing two such affine maps adds their integer pairs: the cross term is `tmp`, which combines with `tm²/2 + tp²/2` to give `t(m+p)²/2`. Consequently `ρ_t` is a representation of the fixed deck group, with linear part

\[
L_t(m,n)=\begin{pmatrix}1&0\\tm&1\end{pmatrix}.
\]

The identity `ρ_t = F_t τ F_t^{-1}`, where `τ` denotes integer translations, proves free and proper discontinuous action, without a mistaken assertion that `F_t` is affine in the original coordinates. Conjugation by a diffeomorphism preserves properness: inverse images of two compact sets are compact, and only finitely many integer translations can make them intersect. The equivariant map induces a diffeomorphism from the fixed smooth torus to `R²/ρ_t(Z²)`. This supplies its marking and compact quotient.

The developing image is all of `R²`, and `F_t` is a global diffeomorphism, so the affine structure is complete. Directly, a lifted geodesic with initial data `(x0,y0,a,b)` is

\[
x(\sigma)=x_0+a\sigma,\qquad
y(\sigma)=y_0+b\sigma-ta^2\sigma^2/2,
\]

for every `σ ∈ R`. Applying `F_t` sends this polynomial to an affine line, with second component

\[
y_0+tx_0^2/2+(b+tx_0a)\sigma.
\]

No finite-time escape or incompleteness is concealed by the quotient.

The connection preserves the global area form `dx∧dy`. Its connection trace `Γ^k_{ik}` is zero for both `i`, and the holonomy linear matrices have determinant one. Equivalently, `F_t^*(du∧dv)=dx∧dy`. Completeness and volume preservation strengthen the example; the target does not require either one.

### Smooth smallness in structures and developing maps

On the fixed compact torus, `D_t-D_0` is exactly `t` times a fixed smooth tensor. It converges to zero in every `C^k` norm. In the fixed frame its positive-order derivatives all vanish. The coefficient dependence on `t` is smooth, with a nonzero first derivative at the central connection.

For developing maps, on a compact set with `|x|≤R`, the difference `F_t-F_0` and its derivatives have respective bounds

\[
|t|R^2/2,\quad |t|R,\quad |t|,
\]

through derivative order two; derivatives of higher order are zero. This proves `C∞` compact-open convergence of developing maps. A fixed finite cover by small lifted torus neighborhoods gives charts `F_t` on fixed local domains. Their transitions are the affine maps `ρ_t(m,n)`, depending smoothly on `t`. Thus the construction also works directly at the atlas level.

Baues-Goldman explicitly use the `C∞` compact-open topology on developing maps on printed p. 8. On p. 20 they display this same family and distinguish a smooth family of structures from smoothness of its period curve. Their p. 14-15 construction agrees after interchanging coordinates. These inspected passages establish a precise source concordance, not novelty. [Version inspected: arXiv:math/0401257v2](https://arxiv.org/pdf/math/0401257v2).

In their normalized period coordinates the same family has

\[
p(t)=(0,-\sqrt[3]{t}),
\]

where the cube root is real. It is continuous and approaches zero; it is not differentiable at zero in parameter `t`. This does not obstruct ordinary smallness: the developing maps are smooth and their classes converge in the quotient topology. Even a requirement of a smooth period curve can be met by `t=s³`, yielding `p(s³)=(0,-s)` and `D_{s³}=D_0+s³dx⊗dx⊗Y`. The reparametrized connection has zero first derivative at zero but noncentral fibers for every nonzero `s`; no immersion hypothesis occurs in the printed stability question.

### The deformation is not a disguised affine gauge change

For `t≠0`, `L_t(1,0)` is nonidentity, whereas the central connection has trivial linear holonomy on every loop. An affine equivalence conjugates the entire linear holonomy image and changes the labeling of loops by a group automorphism. Neither operation can convert a nontrivial image into the trivial image. Therefore no diffeomorphism, even without preserving the marking, gives an affine equivalence between `D_t` and `D_0`.

The developing-map linear holonomy above and tangent parallel transport around the positive `x` loop have opposite shear signs: the latter is `I-tE_{21}` from the equation `v'=-tE_{21}v`. They are inverses under the usual deck/development comparison; both are nonidentity for `t≠0`. A sign-convention difference cannot eliminate the gauge obstruction.

Although `F_t` is a diffeomorphism of the universal cover, it does not descend to an ordinary self-diffeomorphism of the standard quotient for `t≠0`: translating `x` by one changes its second component by `tx+t/2`, which is not a constant integer. Its valid equivariant descent goes to the varying affine quotient described above.

## 4. Central Hessian metric and all-candidate obstruction

The central metric `g_0=dx²+dy²` is positive definite and locally Hessian for `D_0`, with local potential `(x²+y²)/2`. On two lifted neighborhoods differing by `(m,n)`, the potentials differ by the affine function

\[
mx+ny+(m^2+n^2)/2.
\]

Their Hessians therefore agree. A periodic global potential is not asserted. Compactness also makes this central Riemannian metric complete. The central developing image contains lines, so it is outside the hyperbolic case.

Now allow an arbitrary smooth symmetric bilinear form on the fixed torus,

\[
g=A\,dx^2+2B\,dx\,dy+C\,dy^2.
\]

Its three lifted coefficients are smooth and separately one-periodic; this follows from their expression in the fixed global frame, not from any homogeneity assumption. If `g` is Hessian for `D_t`, the tensor `D_t g` is fully symmetric because in local affine coordinates it is the third derivative of a smooth potential. The `X,Y,X` Codazzi identity is

\[
\begin{aligned}
(D_Xg)(Y,X)&=B_x-tC,\\
(D_Yg)(X,X)&=A_y,
\end{aligned}
\qquad\Longrightarrow\qquad B_x-A_y=tC.
\]

For completeness the other independent equation is `C_x-B_y=0`. The first equation alone gives the obstruction. Define the globally descended one-form `α=g(X,·)=A dx+B dy`. It satisfies

\[
d\alpha=(B_x-A_y)dx\wedge dy=t\,g(Y,Y)dx\wedge dy.
\]

Stokes' theorem on the closed torus implies

\[
0=t\int_{T^2}g(Y,Y)\,dx\wedge dy.
\]

For a positive-definite metric, `g(Y,Y)>0` everywhere since `Y` never vanishes. It has a positive minimum on the compact torus, so the integral is strictly positive. The equation forces `t=0`. The same argument can be read as cancellation of derivative integrals over a fundamental square, with all opposite-edge terms canceling by periodicity.

This proves nonexistence for every nonzero real `t` and every smooth positive-definite Hessian candidate, including ones that are nonconstant, not parallel, not close to `g_0`, or not members of a continuous metric family. It does not transfer the main difficulty to an unsupported solvability theorem. Holonomy by itself is used only for the gauge distinction, not as a false assertion that Hessian metrics must be parallel.

## 5. Adversarial boundary and hypothesis checks

| Potential hidden requirement or counterexample | Independent check and disposition |
| --- | --- |
| Only the chosen central metric ceases to be Hessian | The integral argument applies to arbitrary coefficients `A,B,C`, hence rules out every positive-definite Hessian candidate. |
| Translation invariance or a constant metric is assumed | No such restriction enters; coefficients are periodic solely because the metric is globally defined on the fixed quotient. |
| A global potential is needed | The definition is local. Central potentials differ by affine functions. Requiring one periodic global potential would even wrongly exclude `g_0`. |
| An atlas, quotient or completeness failure | The exact equivariant global diffeomorphism and conjugate translation action prove a genuine complete marked compact affine quotient. |
| The holonomy representation does not compose | Expanding its quadratic translation term proves the representation law for all integer pairs; independent exact controls also test nontrivial pairs. |
| The deformation is pure affine gauge | Nontrivial linear holonomy is invariant under affine conjugacy and relabeling; the central image is trivial. |
| Smoothness in period coordinates is required | Their cube-root curve is continuous; reparametrizing `t=s³` makes it smooth while preserving arbitrarily small noncentral examples. |
| The hyperbolic special case must also fail | It is outside the proved claim: the developing image is the whole plane, which contains complete lines for every `t`. |
| Fixed linear holonomy is required | That restriction is absent from the target; this family changes linear holonomy for every `t≠0`. No conclusion inside a fixed-holonomy stratum is asserted. |
| Sign of `t` creates an exception | The contradiction uses `t` times a strictly positive integral and works for either nonzero sign. At `t=0` the supplied central example works. |
| Indefinite metrics also fail | They need not fail: the global Lorentzian metric `2dxdy` is Hessian for every `D_t`. In developing coordinates its potential is `uv-(t/3)u³`; pulling back its Hessian gives `2dxdy`. Positivity is essential. |
| Positive-semidefinite metrics also fail | They need not fail: `dx²` is locally Hessian for every `D_t` and has `g(Y,Y)=0`. Strict positivity is essential. |
| Positive Hessian metrics cannot exist on the cover | They do exist: `F_t^*(du²+dv²)` is positive and Hessian on `R²`, with components `A=1+t²x²`, `B=tx`, `C=1`. For `t≠0` it is not periodic and does not descend. Compactness/global descent is essential. |
| Non-Riemannian affine family alone settles Hessian nonexistence | It does not: having a connection that is not a metric's Levi-Civita connection is weaker than lacking any Hessian metric. The explicit Codazzi/Stokes obstruction is the additional argument. |
| Classical availability of the affine family proves first priority or old resolution | It proves neither. A separate priority audit must investigate whether earlier work explicitly implies or states this Hessian obstruction and its stability application. |

## 6. Checkable computations and their limits

`check_source_topology.py` is independently authored and uses only the standard-library `Fraction` type. It checks 691 explicitly named exact rational equalities or Boolean properties, covering positive, negative and central parameters; both quotient coordinates; nontrivial deck pairs; group composition; the pullback connection; all torsion and curvature components; area preservation; inverse developing maps; inverse holonomy/parallel-transport signs; developed geodesic lines; local-potential transitions; and the indefinite and noncompact boundary examples. The geodesic control uses actual second finite differences of the polynomial, not a floating numerical derivative.

Both normal Python and `python -O` runs pass all 691 checks and produce byte-identical JSON of 19,691 bytes, SHA-256 `f1523325c0d949740739901cbbf11b7f18c924c99d4d286d5ed786a26566b3b2`. The checker source SHA-256 is `66af25129a720c05d32955b8c18ea05b898419eccf5446fe71e993833e58ad29`. Explicit exceptions enforce the controls; no `assert` is required.

Four deliberately incorrect private variants independently changed the developing-map coefficient, holonomy shear sign, quadratic holonomy term, and upper connection index. Each exited nonzero with `VerificationError` in both modes: eight expected detections. `CONTROL_RECEIPT.json` preserves the exact results without distributing invalid source fixtures. No dependency environment or network operation is needed to rerun the checker:

```sh
python3 check_source_topology.py
python3 -O check_source_topology.py
```

These finite controls cannot establish identities for all real parameters or exclude an infinite-dimensional space of metrics. The independent analytic derivations above establish those universal claims. No empirical approximation, numerical integration, unit convention, or tolerance enters the conclusion.

## 7. Acceptance and exact remaining gap

All source/topology success criteria are met: an admissible compact positive Hessian central structure; globally descended smooth complete volume-preserving affine deformations; arbitrarily smallness in connection and developing-map topologies; genuine change under affine gauge; nonexistence of all positive Hessian candidates; explicit separation of hyperbolic, fixed-holonomy and indefinite boundaries; source attribution of the classical family; and reproducible exact controls.

Remaining mathematical gaps in this family: **0**. Blocking issues: **0**. Required repairs: **0**. No source or proof amendment is required for the reviewed frozen `PROOF.md`.

The exact remaining gate outside this family is historical priority and publication-package verification. This review does not determine whether the negative resolution was already in the literature, and does not claim novelty or first resolution from a bounded source search. It also does not review any yet-unwritten paper or operational upload package. A separate clean full-package adversarial review remains necessary before publication.

All source PDFs, text extracts, page images and deliberate invalid variants are private and excluded from the explicit authored-output whitelist. The report contains original derivations, short source summaries, bibliographic links and verification receipts. No person was contacted, and no external message or service write was made.
