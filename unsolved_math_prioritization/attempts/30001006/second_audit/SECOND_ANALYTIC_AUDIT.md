# Second analytic audit of the scalar Weyl cone bridge

Problem 30001006, OWR-2045-003, rank 817. Review date: 2026-10-06 UTC.

## Verdict and exact scope

**ACCEPT THE SCOPED THEOREM. No mathematical gap requiring a correction was found. The classification problem remains UNSOLVED HERE.**

For each integer n ≥ 4 and each fixed real d > 0, let K_d be the closed cone of algebraic curvature operators satisfying scal(R) ≥ d‖W(R)‖, where the norm is the Hilbert–Schmidt norm on endomorphisms of Λ². The frozen argument proves that preservation by the Hamilton ODE is equivalent to preservation under every smooth Ricci flow on every closed n-manifold, throughout smooth existence. Every ODE failure is realized by a smooth initial metric on Sⁿ satisfying the condition everywhere and violating it after a sufficiently short positive time.

This is a proof-level analytic review of the argument and its dependencies, including a fresh challenge of the compact extension. It is not formal proof-assistant verification, journal acceptance, historical-novelty clearance, or a solution of the global Weyl optimization problem. The original author freeze and first audit freeze were preserved unchanged. The first audit and its clarifying supplement were read, but their acceptance was not used as a premise in the reasoning below.

## Authenticated inputs

- Author archive: RICCI_INVARIANT_CONES_30001006_AUTHOR_SAFE_FREEZE.zip; 17,241 bytes; SHA-256 c7b2700050482bec8b74874b61ed050c07b3a08e1a8d06eee52d794682b1d8c1.
- First audit archive: RICCI_INVARIANT_CONES_30001006_INDEPENDENT_AUDIT_SAFE.zip; 19,293 bytes; SHA-256 25a812cf211700e23835cd92b187d15969e897f0318d8c636cfc33a72d3d527b.
- The two embedded manifests, complete member sets, member hashes, and mathematical output replays passed in ordinary and optimized Python. Results are in INPUT_REPLAYS.json. This second review did not rerun the inputs' entire mutation harnesses.

## 1 Norm convention and conformal identity

Take e_i∧e_j, i<j, orthonormal in Λ², and write the operator matrix as R_(ij),(kl)=R_ijkl. Then

‖R‖²_HS = Σ_(i<j,k<l) R_ijkl²,

whereas the unnormalized full covariant tensor contraction is

|Rm|² = Σ_(i,j,k,l) R_ijkl² = 4‖R‖²_HS.

Thus |W|_tensor = 2‖W‖_HS, with these conventions. A tensor-norm coefficient t corresponds to the operator-norm coefficient d=2t. No spectral operator norm is being substituted. The identity operator has ‖I‖²=n(n−1)/2 and scal(I)=n(n−1).

For ĝ=λ²g, the covariant Weyl tensor has weight λ², while a ĝ-orthonormal frame has vectors λ⁻¹e_i. Therefore its operator matrix in orthonormal frames has weight λ⁻², and ‖W_ĝ‖_HS=λ⁻²‖W_g‖_HS. With λ=v^(2/(n−2)), the weight is v^(−4/(n−2)). Combining this with the scalar-curvature conformal formula gives exactly

F_d(ĝ)=v^(−(n+2)/(n−2)) [−a_n Δ_gv+F_d(g)v],

a_n=4(n−1)/(n−2), Δ=div grad.

This is an equality of continuous functions even at Weyl zeros; it does not differentiate the norm there. Equations (2.9)–(2.11) of [Branca, Catino, Dameno and Mastrolia](https://link.springer.com/article/10.1007/s10455-025-09996-x) were freshly inspected and give the corresponding modified-scalar-curvature transformation. The norm conversion above is established directly.

**Finding:** all weights, the Laplacian sign, and the fixed-d interpretation are correct.

## 2 The analytic boundary germ is an actual metric

At a smooth boundary point R_* the Weyl component is nonzero. The quadratic normal model h_ij=δ_ij−R_*ikjl x^k x^l/3 is symmetric, positive definite on a sufficiently small ball, and has the requested curvature with the stated sectional-positive convention. The normal-coordinate curvature formula gives R_h(0)=R_*. Because h is even, its first and third derivatives vanish at 0. At that point the Christoffel symbols vanish, so the derivative of curvature has no residual connection term: ∇R_h(0)=0.

The algebraic curvature symmetries, including Bianchi, are needed for this reconstruction. They are part of the input definition. No arbitrary incompatible curvature derivative is prescribed. In fact, an actual quadratic metric is already present before the analytic PDE is solved.

Metric inversion, curvature, and the squared Weyl norm are analytic near the origin. The latter is strictly positive there after shrinking, so its positive square root is analytic. Consequently f=F_d(h)/a_n is analytic, f(0)=0, and ∂f(0)=0. The last assertion can also be seen from evenness and the stationary metric at 0.

Writing Δ_hv=h^{ij}v_ij+b^jv_j, the equation Δ_hv=fv can be solved for v_nn because h^{nn}>0 near the Cauchy hypersurface. It is a second-order analytic equation with analytic Cauchy data v(x′,0)=1 and v_n(x′,0)=0. These are the local non-characteristic hypotheses of Cauchy–Kowalevski; the relevant theorem and definition were freshly checked in [Tataru's course notes transcribed by Ning Tang, Section 13](https://math.berkeley.edu/~ning_tang/files/notes/graduate/Math222B_Spring2023.pdf). No smooth elliptic Cauchy stability assertion is required. The local analytic solution has v(0)=1 and hence is positive after shrinking.

The jet claim can be verified exhaustively by the number of normal indices:

1. Cauchy data make derivatives with zero normal indices, and derivatives with exactly one normal index, vanish at 0 through all needed orders.
2. At 0 the equation gives v_nn=0; all other second derivatives are already zero.
3. Differentiate the equation once. Terms involving coefficient derivatives multiply v_j or v_ij and vanish. The right side is f_kv+fv_k=0. Since h^{ij}(0)=δ_ij, the remaining equation is Σ_i v_iik=0.
4. Each i<n term is killed by the Cauchy data, including k=n. Therefore v_nnk=0 for every k, including v_nnn=0.

Thus v−1 has vanishing 3-jet. The full metric 3-jet of g=v^(4/(n−2))h equals that of h, while the conformal identity makes F_d(g) identically zero on a neighborhood. This preserves both R_* and ∇R=0, rather than only selected curvature contractions. Fourth and higher metric derivatives are whatever the actual analytic solution supplies.

**Finding:** CK is applied legitimately, positivity is local and sufficient, and the full 3-jet preservation is proved. Finite Taylor calculations alone would not prove existence; the argument does not make that substitution.

## 3 The compact extension withstands the gluing challenge

### Uniform geometry before the conformal correction

Rechoose geodesic normal coordinates for the constructed germ. This changes coordinates, not its invariant curvature data or the local identity F_d=0. For the more general extension lemma, only a smooth germ with F_d≥0 is needed. Fix a sufficiently small radius r_0 within that germ and within the round sphere's normal chart. All choices below are made with this r_0 fixed.

Gauss' lemma gives g_ij x^j=x_i. The round normal metric b satisfies the identical equation. A convex cutoff g_ε=b+χ(r/ε)(g−b), with 0≤χ≤1, consequently stays positive definite and satisfies the same radial gauge exactly. Thus ∇r=x/r and |∇r|=1. No assertion about a global distance function or the cut locus is needed.

On the small chart, g−b=O(r²), ∂(g−b)=O(r), and ∂²(g−b)=O(1). On the only cutoff shell, r is between 2ε and 3ε. Product differentiation gives

|g_ε−δ|≤C r², |∂g_ε|≤C r, |∂²g_ε|≤C,

with C independent of ε. Terms with two cutoff derivatives have size ε⁻²O(r²)=O(1); terms involving a second derivative of r have the same bound because r is comparable to ε. Shrinking the fixed chart makes the inverse metrics uniformly bounded. The coordinate curvature formula then bounds the whole curvature tensor, and hence its scalar and Weyl contractions and Hilbert–Schmidt norm. In particular F_d(g_ε)≥−B for a fixed B, allowed to depend on d and the germ.

The radial divergence formula is

Δ_(g_ε)r=(n−1)/r+(1/2) tr(g_ε⁻¹ ∂_r g_ε).

The trace term is O(r), uniformly through the moving cutoff shell. Therefore a fixed A≥0 gives Δr≥(n−1)/r−Ar. Uniform control of third or higher metric derivatives is unnecessary. Those derivatives may deteriorate as ε→0; the construction chooses one sufficiently small positive ε and does not claim a uniform Ricci-flow lifetime.

### The source, sign, and positive conformal factor

Choose a smooth nonnegative φ supported in [1,4], flat at its endpoints, with φ≥1 on [2,3]. Put w=r^(n−1)e^(−Ar²/2), and set

v′=−M w⁻¹ ∫_ε^r w(s)φ(s/ε) ds, v(ε)=1,

extending v=1 to r≤ε. Choose M>B/a_n once, before ε. Positivity of w and φ gives v′≤0. The defining ODE is

v″+[(n−1)/r−Ar]v′=−Mφ(r/ε).

Multiplying the lower drift bound by the nonpositive v′ reverses the inequality, giving Δv≤−Mφ. Reversing that comparison would ruin the construction; the frozen proof uses the correct sign.

Let L=e^(Ar_0²/2), Φ=sup φ. Before r=4ε, the source integral is at most Φrⁿ/n, so |v′|≤MLΦr/n. After r=4ε it is at most Φ4ⁿεⁿ/n, so |v′|≤MLΦ4ⁿεⁿr^(1−n)/n. Integrating gives

0≤1−v(r)≤M C ε² for ε≤r≤r_0,

where, for example, C=LΦ[15/(2n)+16/(n(n−2))] suffices. This bound is uniform in ε and uses n>2. Choosing ε still smaller gives 1/2≤v≤1.

The only possibly negative region of F_d(g_ε) is [2ε,3ε]. On that shell the conformal numerator is at least a_nM−Bv≥a_nM−B>0. Before the shell the metric is the original germ; after the shell it is round. Wherever the initial F_d is nonnegative, the two terms −a_nΔv and F_dv are both nonnegative. This covers the entire inner chart, including the extra source intervals and the harmonic-comparison tail.

### Returning to the round metric on a fixed annulus

Choose a fixed 0≤η≤1, equal to one on r≤r_0/2 and zero near r≥r_0. Ensure 4ε<r_0/2. On the annulus r_0/2≤r≤r_0, the source integral is constant O(εⁿ), and r is bounded away from zero. Hence v′ and v″ are O(Mεⁿ), while v−1 is O(Mε²).

For ṽ=1+η(v−1), the product rule therefore gives a C² error O(Mε²) on this fixed annulus, including the η′ and η″ terms multiplying v−1. The background is exactly round there. Its margin F_d(b)=n(n−1) is positive independently of d, because its Weyl tensor is zero. For a fixed C′,

−a_nΔ_bṽ+n(n−1)ṽ≥n(n−1)−C′Mε²>0

for sufficiently small ε. This is where the global integral obstruction to a nonconstant superharmonic function is avoided: Δṽ may be positive on the outer annulus, and the round scalar margin pays for that error.

The resulting conformal metric equals the germ on an open inner ball and equals the round metric on an open neighborhood of the chart boundary. Flat source/cutoff endpoints and constancy near r=0 give smoothness at every seam and at the center. The construction yields an honest smooth positive-definite metric on the fixed closed sphere.

**Finding:** no sign, scale, seam, positivity, or parameter-choice gap was found. The uniform curvature estimate and the separate fixed-annulus estimate are sufficient. This proves the extension for this conformally covariant family; it supplies no gluing theorem for arbitrary curvature cones.

## 4 The curvature Laplacian contributes zero normal velocity

At the selected center the Weyl norm is smooth. Write u=W/‖W‖. In the Euclidean curvature-operator fiber,

DF_d[H]=scal(H)−d⟨u,P_WH⟩,

D²F_d[H,H]=−d/‖W‖ (‖P_WH‖²−⟨u,P_WH⟩²).

The invariant fiber function satisfies

ΔF_d(R)=DF_d[ΔR]+Σ_i D²F_d[∇_iR,∇_iR].

Local equality F_d=0 alone would not kill the second term. Indeed its sign is nonpositive and the corresponding normal curvature diffusion could prevent an outward reaction from winning. The separately constructed ∇R=0 kills every Hessian term. Local equality then gives DF_d[ΔR]=0 exactly.

The compact metric has a smooth short-time Ricci flow. In moving orthonormal frames the curvature equation is ∂_tR=ΔR+2Q(R). The frame choice incorporates the changing metric into the bundle identification, so there is no omitted derivative of the norm or scalar contraction. Therefore

∂_t F_d(R)(0,0)=2 DF_d(R_*)[Q(R_*)].

A strict negative value remains a genuine violation at the fixed spatial point for all sufficiently small positive times. The Weyl component stays nonzero for that differentiation interval. Only one finite ε and its short-time flow are needed.

**Finding:** the proof cancels precisely the normal Laplacian component. It neither assumes nor needs ΔR=0 or ∇²R=0.

## 5 Tangent cones and the nonsmooth boundary

K_d is the inverse image of a Lorentz-type cone under the linear map R↦(scal(R),W(R)); the traceless-Ricci subspace is unrestricted. It is closed, convex, and O(n)-invariant, with I in its interior. At W≠0 its tangent cone is {V:DF_d[V]≥0}. At scal=W=0, translation by that traceless-Ricci operator leaves K_d unchanged, so the tangent cone is exactly {V:scal(V)≥d‖W(V)‖}.

For completeness, the tangency-to-ODE implication does not require a global flow for the quadratic vector field. Let x(t) be a local solution and y=P_Kx its Euclidean projection onto the closed convex cone. If Q(y) belongs to the tangent cone, then ⟨x−y,Q(y)⟩≤0. On any bounded trajectory interval Q is Lipschitz with some L, and

(1/2)d/dt dist(x,K)²=⟨x−y,Q(x)⟩≤L‖x−y‖².

The projection stays bounded, and Gronwall gives zero distance for initial points in K. Conversely, an invariant local trajectory starting at y has initial derivative in the tangent cone. This proves the exact criterion used in the author argument and accounts for possible later ODE blow-up.

At a nonsmooth point R_0, a strict tangency violation obeys scal(Q(R_0))<d‖W(Q(R_0))‖. With the adopted normalization scal(Q)=|Ric|²≥0, so its Weyl component is nonzero. Let U=W(Q(R_0))/‖W(Q(R_0))‖ and c=n(n−1)/d. Then R_ε=R_0+εI+cεU has scal=n(n−1)ε and ‖W‖=cε, so it is exactly on the smooth boundary. Its unit Weyl direction is exactly U. Polynomial continuity of Q makes

DF_d(R_ε)[Q(R_ε)] → scal(Q(R_0))−d‖W(Q(R_0))‖<0.

Thus an outward witness always exists at a smooth boundary point, and Sections 2–4 apply. Merely approaching the boundary without controlling the Weyl direction would not suffice; the given formula controls it exactly.

For the reverse implication, the hypotheses of Hamilton's tensor maximum principle all hold: a closed convex O(n)-invariant fiber set is invariant under parallel translation, the reaction preserves it, and the smooth curvature is bounded on every compact time subinterval of a closed-manifold flow. Noncoercivity is not an obstruction. [Richard and Seshadri, Definition 1.5 through Remark 1.8](https://arxiv.org/pdf/1308.1190) were freshly read and confirm the normalization and distinguish their ODE definition from literal PDE preservation. Their theorem supplies sufficiency, not the converse established here.

**Finding:** the apex reduction and both directions of the equivalence are justified, with the factor 2 changing only time scale.

## 6 Source scope and fresh provenance

The official [2008 Oberwolfach report](https://ems.press/content/serial-article-files/46179) was independently retrieved again: 422,818 bytes, SHA-256 70d07d22627a077dce6979e9f142b3d79515dbddb184d5c341b0fbf4d2879363. PDF page 10, printed page 1942, was rendered and visually inspected. The definition uses a strict inequality; both preservation statements in Theorem 1 and the necessity conjecture visibly use closure bars. Accordingly K_d=closure({scal>d‖W‖}) is the correct scope for this bridge. The supplied catalog shorthand omits those bars; it is not used to override the primary statement.

All three full corpus files became available during this second review. They were freshly hashed and parsed; the unique target record was read. The report key is absent and is represented by {}, not null. Python's default sorted serialization of [record,{}] has 4,187 bytes and SHA-256 4f6560adcbd9605e5b1367049b29d387a12d30f3c6f68dbbcb49395a2c20a863, matching the catalog review hash. FRESH_CORPUS_VERIFICATION.json records file-level sizes, hashes, and counts. The catalog ID is a string and the problem-record ID an integer; matching was normalized without changing the record serialization.

This fresh PASS is separate from the first audit's historically correct NOT_RUN statement. Neither frozen input was rewritten. Source PDFs, rendered images, extracts, records, and corpus contents are excluded from this release.

## 7 Imported consequences and limitations

The formula nβ_n≤d≤(n−2)/μ_n is conditional here on the separately audited rank-815 algebraic criterion. That separate proof and its five approaches were not re-audited in this second bridge review. The elementary convention conversion is consistent: if R=aI+E+W, then the coefficient c in ‖W‖²≤c‖aI‖² equals 2n(n−1)/d². The central d²=2(n−2)(n−1) corresponds to c=n/(n−2).

No global Weyl-cubic maximum is evaluated here. In particular β_12²≤55/36 is still an unproved obligation in this work: d(12)²/12²=220/144=55/36. The threshold n_0=12, larger even-dimensional sharp estimates, and odd-dimensional margin are not solved by the bridge. No fresh complete literature search or inspection of Xu's published version of record is claimed in this second review.

## 8 New executable checks and release status

The new independent_stress_checks.py uses its own exact rational tensor calculation. Twelve four-dimensional cutoff-shell cases compare complete curvature computed from metric second derivatives with an independent Christoffel-connection calculation: 432 component comparisons. The cutoff metric jets obey the expected ε², ε, and constant scaling in 3,024 exact component comparisons. The script checks radial gauge, positive definiteness, scalar normalization, the factor four between squared full-tensor and operator norms, and the norm's conformal scaling. Eight shell cases have negative F at d=2, so the diagnostic genuinely exercises the potentially bad transition geometry. Three negative controls detect the missing norm factor, loss of radial gauge, and a reversed drift comparison.

These are finite diagnostics with quadratic normal models and a C² quintic shell cutoff. The diagnostic background is the round second-jet model, not a substitute for the actual round background in the proof. They neither prove analytic existence nor establish a uniform theorem for every metric or smooth cutoff. The analytic arguments above supply those obligations. The saved result is replayed by the release verifier.

There is no correction patch because the reviewed theorem survived the challenge. This package contains only newly authored mathematical review, executable diagnostics, and permitted verification metadata. No remote mutation, publication, external communication, copied third-party source document, dataset content, or private coordination material is included or was performed by this review.
