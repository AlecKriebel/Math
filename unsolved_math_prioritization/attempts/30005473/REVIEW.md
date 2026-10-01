# Independent mathematical review: discotope exposed-point irreducibility

**Target:** 30005473 / OWR-12697711-006  
**Review date:** 2026-09-30 UTC  
**Reviewer execution:** gpt-6-astra, xhigh  
**Candidate reviewed:** `candidate.md`, SHA-256 `be17b06e33f9daa887038218d01a7ff783393481d03f2c39caebaf05e2f6252d`  
**Preserved snapshot:** `reviewed_candidate.md`

## Verdict

**Mathematical audit: PASS.** I found no gap in Theorem 1 (Sections 1–4), which proves the entire 2023 OWR target, indeed without its genericity assumption. The generic bridge in Theorem 4 (Section 5) also passes and establishes the 2022 article's conjecture for its different variety S. The nongeneric separating example is correct and usefully prevents a misleading unconditional identification of S and E.

**Historical priority: UNRESOLVED.** The checked sources pose the conjectures, and the targeted current search did not locate a later resolution. That is not a certification that this is the first proof. A claim of a new discovery or first resolution should remain qualified pending further literature/expert assessment. This report is an independent AI mathematical audit, not journal peer review or a formal proof certificate.

No mandatory mathematical revision was found. Keep the distinction between the exact target E, the separately proved generic statement about S, and the unproved critical-locus/degree questions.

## 1. Source verification

The requested problem page was attempted first and was inaccessible to the web tool. I then read the complete pinned dataset record, the relevant original source sections, and the candidate. The pinned report dictionary has no entry for this problem code.

The official OWR report, printed p. 830, explicitly defines E as the Zariski closure of the exposed points, then states Conjecture 1 for generic summands of dimensions at least two. The page was also inspected visually. The candidate's target agrees with this source. The article's genericity is described through transverse linear spans.

In contrast, the 2022 paper defines S using sums of relative-boundary points which also lie on the boundary of the total sum (Definition 3.3, p. 149). Its Conjecture 8.2, p. 167, concerns S. That printed page was independently inspected. The candidate correctly does not treat E=S as a definition.

The 2022 article's Section 2 defines generic discs using injective matrices/bases and assumes full-dimensional total sum after restricting the ambient span. These conventions match the hypotheses used for Theorem 4. Theorem 1's lower-dimensional extension is genuinely extra and does not create a gap in the requested case.

Primary sources:
- [OWR report, official PDF](https://publications.mfo.de/bitstream/handle/mfo/4031/OWR_2023_15.pdf?sequence=4), Meroni contribution, pp. 829–832; exact target p. 830
- [Gesmundo–Meroni, published PDF](https://lematematiche.dmi.unict.it/index.php/lematematiche/article/download/2338/1156/6734), Le Matematiche 77(1) (2022), 143–171; §§2–3 and Conjecture 8.2
- [Article landing page](https://lematematiche.dmi.unict.it/index.php/lematematiche/article/view/2338), DOI 10.4418/2022.77.1.8

## 2. Exact support parametrization: checked independently

Let D_i=A_i B^{m_i}, where A_i has full column rank and m_i≥2. For a nonzero linear functional represented by u, maximizing on the ball reduces to maximizing the functional A_i^T u. Thus:

- If A_i^T u≠0, the unique maximizer is A_i(A_i^T u)/||A_i^T u||.
- If A_i^T u=0, the maximizing face is the entire positive-dimensional D_i.

For a Minkowski sum, the support values add and the exposed face is the sum of the exposed faces. A sum of nonempty sets cannot be a singleton if any one summand is nonsingleton: fixing points in the other summands gives an injective translate of that summand inside the sum. Therefore the singleton-face normals are **exactly**

\[
 U=\mathbb R^d\setminus\bigcup_i\ker A_i^T.
\]

This proves both inclusions in Exp(D)=F(U), not just density or a generic inclusion. The support formula uses Q_i=A_iA_i^T, the correct matrix. No inverse quadratic-form matrix is inadvertently used. In particular, arbitrary ellipsoidal shapes, repeated discs and non-orthonormal bases cause no change.

The origin lies in every removed kernel, so the domain contains no zero normal. Every disc has positive dimension, so no special singleton summand is hidden in the face argument.

## 3. Connectedness and analytic-to-algebraic passage: checked independently

### Connectedness

For x,y outside the finite union of kernels, every space ker(A_i^T)+Rx has dimension at most d−1, and the analogous statement holds for y. A finite union of such proper real subspaces cannot fill R^d. Choose a point z outside all of them. If the segment xz met a kernel at an interior point, solving the affine equation for z would place z in that kernel plus Rx, a contradiction. The same works for yz. Thus U is path connected.

This handles codimension exactly two, not just larger codimensions. In the smallest possible ambient dimension d=2, every full-rank disc removes only the origin, and the argument still applies. The proof does not infer connectedness from mere Zariski openness, which would be incorrect in general.

### Analyticity

On U, each u^TQ_i u=||A_i^T u||² is strictly positive. The positive-real function t↦t^{-1/2} is real analytic on (0,∞). Hence the stated F is a globally defined real-analytic map on the connected open real domain U. Complex square-root branch choices never enter this assertion.

### Primality

For any complex polynomials p and q, if (pq)∘F vanishes identically but p∘F does not, continuity gives a nonempty real open subset on which p∘F is nonzero. Then q∘F vanishes on that subset. The real-analytic identity theorem, applied separately to the real and imaginary parts, makes q∘F vanish on all of U. Thus the ideal of complex polynomial relations on F(U) is proper and prime.

It is exactly the ideal of the complex Zariski closure of F(U), so the closure is irreducible. No complex analytic continuation to a globally defined holomorphic square-root map is required. No smoothness or injectivity of the image, nonvanishing Jacobian, dimension calculation, or independence of the quadratic radicals is needed.

I specifically tested the apparent shortcut “a connected image has irreducible Zariski closure.” That shortcut alone is false; however the candidate does not use it. The real-analytic identity theorem supplies the missing ingredient and makes the argument valid.

## 4. Generic equality S=E: checked independently

Take x=Σ_i x_i in D^boundary∩∂D. Full dimensionality gives a nonzero supporting normal u. Equality in the support sum forces each x_i to lie in the u-exposed face of D_i. Let J be the indices with A_j^T u=0.

All L_j for j∈J lie in the proper hyperplane u^perp. The candidate's general-position assumption says their span has the largest possible dimension. Consequently their dimensions sum to at most d−1 and these subspaces are in direct sum. This is the exact step requiring genericity.

Write x_j=A_jv_j with ||v_j||=1. Since the concatenated A_J is injective, its transpose is surjective. Therefore a vector w can be chosen with A_j^T w=v_j simultaneously for all j∈J. This remains correct for non-orthonormal A_j; no inverse or metric identification is being assumed.

For positive ε, the normal u+εw has A_j^T(u+εw)=εv_j and therefore exposes exactly x_j on each killed summand. For the remaining indices, the previously nonzero projected normals stay nonzero and their unique support points converge to the original x_i. Thus x is a limit of exposed points. The closed algebraic variety E contains it. The reverse inclusion E⊂S follows because every exposed point is already a sum of relative-boundary points on ∂D.

The general-position condition is a finite collection of maximal-rank conditions on concatenated matrices. Each is a nonempty Zariski-open condition in the product matrix parameter space. That space is irreducible and the full-rank restrictions are also nonempty open, so their finite intersection is nonempty open. The argument consequently covers generic discotopes of each feasible full-dimensional type in Conjecture 8.2.

The case J=∅ is already an exposed point and is handled explicitly. If some disc is full-dimensional, it cannot belong to J for nonzero u. Neither case creates an exception.

## 5. Boundary cases and adversarial tests

- **Single disc:** the theorem gives the complexified ellipsoidal boundary, irreducible when its dimension is at least two
- **Lower-dimensional total sum:** the analytic-normal argument remains valid in the original ambient space; normals orthogonal to the whole sum are removed
- **Repeated discs/dependent radicals:** the proof still works because it relies on the positive real support map, not the irreducibility of an auxiliary radical covering
- **One-dimensional summands:** the candidate appropriately excludes them; a segment already gives two exposed points and a reducible closure
- **Nongeneric S:** the candidate does not claim S=E universally, and its explicit counterexample is valid
- **Affine versus projective:** the proof directly establishes complex affine irreducibility, the convention used in the sources; projective closure would also preserve irreducibility
- **Degree, birationality, critical locus:** none follows merely from the proof, and the candidate does not claim them

For the nongeneric example, I independently derived the polynomial relation from two equations a²+Y²=4 and b²+Z²=1 with X=a+b. These imply

\[
 (X^2+Y^2+Z^2-5)^2=4(4-Y^2)(1-Z^2).
\]

At (0,0,1) the difference is 16. Thus this point in S cannot lie in E. A separate exact polynomial remainder calculation reproduces the identity without using the candidate's support-map substitution. The result is saved in `independent_checks.json`.

I also ran the candidate's complete `checks.py`; all exact checks passed with SymPy 1.14.0. These calculations test examples and transcription only. The theorem is justified by the argument in Sections 2–4, not by finite computation.

## 6. Novelty assessment and its limits

I checked the published 2022 paper, the 2023 OWR formulation, the authors' current research/publication pages, and targeted searches for discotope irreducibility, Conjecture 8.2, analytic proofs, and results dated 2024–2026. I did not locate a later primary-source resolution of either exact formulation.

The author's research page still lists the 2022 paper; this does not itself prove that the conjecture remains open. A separate 2026 benchmark contribution was followed because it appeared on that page; its public paper contains no occurrence of discotope and provides no evidence of a resolution. No private benchmark access was attempted and no inference about unpublished work is warranted.

Primary pages checked:
- [Fulvio Gesmundo's publications](https://fulges.github.io/publications.html)
- [Chiara Meroni's research](https://merochia.wixsite.com/chiara-meroni/research)
- [arXiv record for the original paper](https://arxiv.org/abs/2111.01241)

The source labels and absence of a found resolution support continued novelty investigation, not a categorical historical-priority claim. No one was contacted.

## 7. Provenance and final recommendation

Source PDF SHA-256 values:
- OWR report: `32c4fbd8b25f445613300ed0a00ba2082d653a154a3b2f64734f19c678d351ff`
- Published discotopes paper: `76d7033365db98c4cc4ce166aaa5bda2b1aaa25d5ba3386d3d66651a849c9adb`

The review snapshot is preserved separately so that later candidate edits do not silently inherit this verdict. The rendered source pages in this review directory are for private verification, not proposed public repository attachments.

**Recommendation:** retain the complete proof as mathematically passed by this independent audit, with two separately stated conclusions: unconditional irreducibility of E, and generic equality S=E yielding the 2022 conjecture. Keep historical priority qualified. No further proof-search turn is needed to repair this candidate. Future edits affecting mathematical content require a fresh check against this snapshot.
