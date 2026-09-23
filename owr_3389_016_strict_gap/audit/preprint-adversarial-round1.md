# Fresh adversarial preprint review, round 1

Review checkpoint: **2026-09-23 13:39 UTC** (2026-09-23 06:39 America/Los_Angeles).

Reviewer: independent AI subagent `preprint_adversarial_round1`. Scope: the complete mathematical argument, source normalization, bibliographic assertions, priority wording, standalone readability, rendered equations, and the supporting exact verifier. The manuscript and PDF were read before any earlier proof or priority audit. The prior priority audit was inspected only after forming an independent proof view and independently checking the main historical sources. No human was contacted; no delegated subagents were used; no manuscript or package files were edited or committed by this reviewer.

**Verdict: no new actionable issue found.** The theorem and stronger threshold proposition have a complete proof under the stated hypotheses. No mathematical repair is requested. The baseline PDF is readable and agrees with the TeX. Two minor publication improvements supplied by the parent reviewer are recorded separately below; they are not independent mathematical findings.

Scoped review completion: **100%**. Best-guess overall preprint readiness of this reviewed baseline: **98%**, allowing for those two small presentation improvements and a final review of the resulting files. This is a practical readiness estimate, not a probability that the theorem is true or a certification of priority.

## Frozen reviewed files

SHA-256 digests, rechecked at the end of substantive review:

| File, relative to this effort | SHA-256 |
|---|---|
| `manuscript/paper.tex` | `910cc4017390df7c33e08cd80c84a606047e145cd4ff9d6df6f76c5b67e83aff` |
| `output/pdf/paper.pdf` | `530187134c9166c1d88d6dedf0237f383bd0505bce89578d3b793e2007b83473` |
| `verification/verify.py` | `79d3698942534faf50418495300ca052634913a20aac2b90b8672b0e09e73ccf` |
| `verification/results.json` | `27d8ac9f1338dcc3b2709579f0e3eba78876675bc11c7db4e2492574ee898d0f` |
| `sources/OWR_2009_06-source-audit.pdf` | `a3ab668409f786c7c1783150d9f937b2d6e06471a48b76c5721b58a49bf3a683` |
| `sources/ashbaugh2002.pdf` | `453638f18bba69a103f65d724ae3a062adedff6a61cdc2be351f6a679b17eb69` |
| `sources/harrell-stubbe-1995-preprint.amstex` | `a619cc3c6600137e468a5ef0cb2b3905e44f12339a369b2784b6fb739d7007c8` |
| `sources/ashbaugh-hermi-2004-source-audit.pdf` | `b05b440330f9fe127b22a701998673125541aa542d0b5a8c335197746deb1b54` |

Temporary extracts, rendered pages, and the reproduced verification result are under `tmp/pdfs/preprint-adversarial-round1/`. They are not additions to the distributed mathematical claims.

## Exact claim and independent reconstruction

The hypotheses are: an integer dimension n >= 1; a nonempty bounded open subset Omega of Euclidean space; and the nonnegative form-defined Dirichlet Laplacian with form domain H_0^1(Omega). Eigenvalues are counted with multiplicity. The claimed result is

\[
\left(\frac{n+2}{n}\frac1J\sum_{j\leq J}E_j\right)^2
-\frac{n+4}{n}\frac1J\sum_{j\leq J}E_j^2
>\frac{(E_{J+1}-E_J)^2}{4}
\]

for every positive integer J. The stronger intermediate result is strict Yang at every real threshold z > E_1, with the sums over E_j < z. This excludes z = E_1, where both sums are zero, and correctly does not claim strict Yang at a repeated ground-state endpoint equal to E_1.

My reconstruction has the following dependency chain:

1. Coordinate multiplication puts w = x_alpha u in Dom H and gives (H-E)w = -2 partial_alpha u and the scalar identity <w,(H-E)w> = 1.
2. If w had finite spectral support, v = (H-E)w would be in Dom H. Distributional commutation with a partial derivative gives (H-E)v = 0. Self-adjointness then forces ||v||^2 = 0, contradicting <w,v> = 1.
3. The two spectral moment identities for w give the exact nonnegative high-energy remainder after cancellation of the finite low-energy block.
4. Vanishing of that remainder at z > E_1 would give finite spectral support to x_alpha u_1, contradicting step 2. Thus the threshold inequality is strict.
5. The correctly normalized quadratic is Q(t) = (t-M_1)^2-D. Its lower endpoint is nonpositive and, unless the upper endpoint is also the ground energy, its upper endpoint is strictly negative. The gap is therefore strictly shorter than 2 sqrt(D). The repeated-ground case gives D = 4E_1^2/n^2 > 0 directly.

No step in this chain assumes the target strictness or transfers it to an unsupported equivalent assertion.

## Adversarial proof checks

### Arbitrary open sets and operator domains — pass

TeX lines 48–66 correctly use the form operator, rather than an unjustified H^2 boundary-domain identification. For an arbitrary open set, the stated characterization follows by testing the form identity on compactly supported smooth functions and extending the resulting distributional identity to H_0^1 by density. Extension by zero into an enclosing box supplies both compactness of the form embedding and a positive Poincare bound. Nonemptiness and openness also guarantee an infinite-dimensional L^2 space.

The multiplier x_alpha and its first derivatives are bounded on the bounded set. Multiplying smooth compactly supported approximants by x_alpha proves preservation of H_0^1. The distributional product rule yields

\[
-\Delta(x_\alpha u)=E x_\alpha u-2\partial_\alpha u\in L^2,
\]

so w belongs to Dom H. No trace theorem, smooth boundary, normal derivative, or extension of the PDE across the boundary is required.

### Integration by parts and real eigenfunctions — pass

The real Dirichlet form is invariant under complex conjugation, so a real orthonormal basis can be chosen within every finite-dimensional eigenspace. Thus the scalar identity and the exact symmetry a_jk = a_kj are legitimate as written. They would require conjugation conventions for an arbitrary complex basis, but the manuscript explicitly avoids that issue.

For real smooth compactly supported approximants, integrating the derivative of x_alpha u^2 gives -2 integral x_alpha u partial_alpha u = ||u||^2. Strong H^1 convergence, boundedness of x_alpha, and Cauchy–Schwarz pass this to the normalized eigenfunction. Normalization of the approximants themselves is unnecessary. The right side 1 and its sign are correct.

### Finite-support obstruction — pass

Finite spectral support gives membership in every operator power domain, in particular Dom H^2. Hence v = (H-E)w belongs to Dom H, which is the crucial additional boundary information. Partial derivatives commute with the constant-coefficient distributional equation inside Omega, so (-Delta-E)v = 0. Applying the already stated operator-domain characterization now is valid.

The identity ||v||^2 = <(H-E)w,v> = <w,(H-E)v> = 0 uses two vectors in Dom H and real E. It does not assume that an arbitrary derivative of an eigenfunction satisfies Dirichlet conditions: that conclusion is obtained only under the finite-support contradiction hypothesis. This is the principal possible hidden-domain trap, and the proof handles it correctly. It works for every eigenspace and coordinate without simplicity, positivity, or unique continuation.

### Spectral convergence and cancellation — pass

The second weighted coefficient series is Parseval applied to (H-E_j)x_alpha u_j, a genuine L^2 vector. For the first series,

\[
\sum_k |E_k-E_j||a_{jk}|^2
\leq\left(\sum_k(E_k-E_j)^2|a_{jk}|^2\right)^{1/2}
\left(\sum_k|a_{jk}|^2\right)^{1/2}<\infty.
\]

Thus signed terms at low energies do not create conditional-convergence problems. The remainder summand is exactly t_j^2(E_k-E_j)-t_j(E_k-E_j)^2, multiplied by |a_jk|^2. The active set L is finite, so no exchange of two unbounded spectral index sums occurs.

For j,k in L, the two ordered terms have the common symmetric factor (z-E_j)(z-E_k)|a_jk|^2 and opposite factor E_k-E_j. Diagonal terms and equal-energy terms are zero. Terms at E_k = z are zero even with multiplicity. The displayed sign and coefficient n in equation (7) are correct.

### Strictness and endpoint transfer — pass

If the remainder vanishes, each summand with j = 1 and E_k > z has strictly positive weight, because z > E_1. Therefore all those coefficients vanish for every coordinate. Compact resolvent makes the spectral space below or at z finite-dimensional, including the entire threshold eigenspace. The finite-support lemma applies directly.

At t = E_J, all omitted indices have energy at least t, and any repeated endpoint terms vanish. At t = E_{J+1}, exactly the indices with energy strictly below t occur among the first J; any additional first-J indices at t contribute zero. Thus applying the threshold proposition to Q at the endpoints is valid even when J cuts through a multiple eigenvalue.

When E_{J+1} > E_1, Q(E_{J+1}) < 0 implies D > 0, justifying sqrt(D). Combining E_J >= M_1-sqrt(D) with E_{J+1} < M_1+sqrt(D) gives a strict gap bound before squaring; its nonnegative sign is stated. If E_{J+1} = E_1, the separate direct calculation is correct. No simplicity of the ground state is assumed.

### Boundary and limiting counterexample attempts — pass

- **One dimension and J = 1:** on an interval with eigenvalues normalized to j^2, D = 4 while the squared gap divided by four is 9/4; the margin is 7/4. At z = 4, the strict Yang remainder is 3.
- **Repeated ground energies:** disjoint identical components can realize E_{J+1} = E_1, but the zero-gap case has the strictly positive D stated in the manuscript.
- **Higher multiplicities and thresholds:** no selection of eigenbasis inside a repeated eigenspace changes finite-dimensionality or the nonnegative remainder argument.
- **Infinitely many components and irregular boundary:** compact form embedding in the enclosing box still supplies finite-dimensional spectral cutoffs. The proof uses no connectedness or boundary regularity.
- **z approaching E_1:** the deficit can approach zero, which is consistent with strictness for every z > E_1 and equality at the excluded endpoint.
- **Scaling and large index:** energy scaling sends both sides of the gap inequality to the same quadratic energy scale. Strict finite-index inequality does not imply a uniform scale-free positive margin or conflict with leading Weyl sharpness.
- **Oscillator/periodic equality examples:** these do not fall under the theorem. A potential adds a derivative term to the differentiated eigen-equation; a periodic coordinate multiplier does not preserve the periodic operator domain. They provide no counterexample to the stated proof.

## Source normalization, citations, and priority language

The following were independently checked, rather than accepted from earlier audit conclusions:

1. [Harrell–Stubbe author preprint](https://web.ma.utexas.edu/mp_arc/e/95-431.amstex), Proposition 6(i)–(iii): the discriminant contains the mean of squared eigenvalues, and the gap is bounded by twice its square root. Setting their kinetic parameter to 1 gives exactly the manuscript's normalization. The authors' [publication record](https://people.epfl.ch/joachim.stubbe?lang=en) confirms the 1997 journal, volume, and pages; the manuscript's DOI also matches the archival record.
2. [Official OWR report](https://ems.press/content/serial-article-files/46205), printed p. 415, visually rendered from the cached primary PDF: M_p is defined with the 1/p root, but the gap displays literally contain M_1^2-M_2. The manuscript accurately makes the missing-square correction explicit and limits its conclusion to saturation. The [publisher record](https://ems.press/journals/owr/articles/3389) confirms the organizers, title, volume 6, year 2009, pages 355–428, and DOI.
3. Ashbaugh 2002, printed p. 12: the passage leaving Yang1 strictness undecided was checked in extracted text and visually in the primary published PDF. Thus TeX line 31 is accurate. The [DOI record](https://doi.org/10.1007/BF02829638), including Crossref metadata, confirms the title, author, volume 112, year 2002, and pages 3–30.
4. [Current UnsolvedMath problem](https://www.unsolvedmath.com/problems/OWR-3389-016): browser inspection on this review date confirmed the squared-mean formula and finite-index equality question. Its own source-review text inaccurately says the original source already has both squared means; the manuscript does **not** repeat that mistake and instead explicitly states the printed typo.
5. [Levitin–Parnovski DOI record](https://doi.org/10.1006/jfan.2001.3913) and [Harrell–Stubbe 2010 DOI record](https://doi.org/10.1137/090763743): bibliographic metadata matches the manuscript. The author preprint record [arXiv:0808.1133](https://arxiv.org/abs/0808.1133) matches the linked 2010 work. Their classical-role attribution is appropriately broad; no new trace identity is claimed here.
6. Ashbaugh–Hermi 2004, inspected cached full text, especially printed p. 212: its strictness observation uses a positive lower bound on the potential. It is not a zero-potential Dirichlet counterexample to the manuscript's limited contribution claim.

Focused independent searches for strict Yang1, eigenvalue equality, and Harrell–Stubbe saturation did not locate a conflicting explicit theorem. Broad searches were noisy and frequently returned unrelated Yang–Yau inequalities; those were not treated as evidence. The 2017 Ashbaugh chapter was located in indexed excerpts, but direct full-book retrieval failed with an HTTP 403. After the independent checks, I read `audit/priority-audit-independent.md` as an additional search trail, not as a substitute for a proof or as independent evidence of absence.

No universal priority certification follows from this bounded check. The manuscript's statement that the trace identities and non-strict inequalities are classical, and that priority is limited to inspected literature, is proportionate. It does not assert a first proof, a new trace identity, or a verified currently-open status. I found no actionable overclaim.

## PDF, standalone exposition, and reproducibility

All three manuscript PDF pages were rendered and visually inspected. Theorem 1, Lemma 2, Proposition 3, equations (1)–(8), signs, subscripts, exponents, summation conditions, bibliography, and proof-end marks agree with the TeX. There is no clipped display, unreadable symbol, missing citation, or overlapping content. The page break after equation (7) interrupts a proof but not an equation and is acceptable.

The proof is standalone for a reader familiar with the form-defined Dirichlet Laplacian and the spectral theorem. It supplies the analytic domain characterization, multiplier step, integration-by-parts justification, equality lemma, sum rules, convergence explanation, remainder, and endpoint algebra. No external inequality needs to be accepted on authority to check the main theorem.

The dependency-free verifier was read in full and rerun with its result directed to this review's temporary directory. It completed **7,016 exact checks**, including **1,312 certified box/index cases** and **three negative controls**. Its output is byte-for-byte identical to the checked-in `verification/results.json`. The omitted-mode bound correctly certifies each needed box-spectrum prefix, including multiplicities. The synthetic symmetric-matrix checks explicitly avoid claiming to realize impossible finite-dimensional Dirichlet commutator sum rules. Numerical scope is accurately distinguished from an analytic proof in both the script and manuscript.

## Parent-supplied publication suggestions, separated from this independent verdict

While this review was in progress, the parent reviewer reported two planned presentation changes:

- **P3, discoverability:** the standalone PDF refers to an accompanying package and audit but contains no URL to them. Exact proposed repair: add one stable repository or project-site link to the provenance paragraph. This changes discoverability, not the validity or checkability of the self-contained proof.
- **P3, PDF metadata:** the baseline PDF has no embedded title or author metadata. Exact proposed repair: add explicit title/author metadata in the PDF build, then inspect the resulting metadata and rendered PDF.

These are clearly attributed to the parent review and are not counted as new independent issues. They are reasonable publication improvements. Any changed manuscript/PDF will have new hashes and should receive a final check against that new baseline.

## Remaining caveats and strongest verified result

There is no identified mathematical gap. The strongest verified result is the strict threshold inequality on every nonempty bounded Euclidean open set, and hence the strict finite-index gap inequality, including disconnected and rough-boundary sets.

This review is not a formal proof-assistant verification, an exhaustive literature search, or a claim of peer acceptance. It did not independently inspect every paper cited by prior audits or systematically search non-English and unindexed literature. Those limitations do not expose a specific repairable defect in the paper's current, qualified claims. No outside contact is proposed or initiated.
