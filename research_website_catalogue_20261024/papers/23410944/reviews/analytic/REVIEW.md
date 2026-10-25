# Analytic review — Zenodo 23410944

**Verdict: no substantive mathematical defect identified.** The paper supplies a valid qualitative existence argument for a connected quasi-conical screen domain with pure point Dirichlet spectral type. The completeness argument, rather than merely persistence of some eigenvalues, is the decisive step. The result is restricted to the precise geometric and operator scope stated in the paper.

## Identity, complete coverage, and independence

The reviewed paper is *Pure point Dirichlet spectrum on quasi-conical domains*, research note version 1.0, dated 15 October 2026. The six-page PDF has SHA256 `4459315138e36ce3b8427f59f8b600ec6f5ba9e3b4a836688cd31395d9fcabe0`; the source/verification ZIP has SHA256 `af22581307f623218d829c06d23302103412ef0329586ef0161ef853a3894e51`; the main TeX has SHA256 `5a8bf95f931685c747777b8db6a22a37705036dccada037a6ff4b136347fd1ba`.

All six published pages, complete main TeX, the complete 305-line authored mathematical `PROOF.md`, and the author's exact checker were read. The bundle-verification and guard code were inspected for replay safety. Historical or current sibling mathematical report/decision bodies were not opened. The main paper and package metadata mention prior audits, a corrected historical source-reading error, and bounded priority searches. These incidental descriptions were encountered and were not treated as mathematical evidence.

The independent mathematical conclusion was frozen in `pre_bundle_conclusion.json` before replaying the complete package. That replay internally reads archived metadata to validate identities; its output was subsequently used only as reproducibility evidence. No old opinion was used to establish the conclusion here.

A fresh source build succeeds, and all six corresponding pages have identical extracted text. The binaries differ; the rebuilt SHA256 is `6820295da0c41a347603886ef255c6448d41578490b3aa2ac0a9ab6386e5e4e8`. Page 1 was also rendered and inspected: the closure bar over the point spectrum is visibly present. Plain PDF text extraction drops that bar, but this is not an error in the published theorem. `source_bindings.json` and `source_build.log` preserve identities and build evidence.

## Exact theorem and terminology

For each integer `d≥2`, the theorem constructs **some** connected open quasi-conical subset of `R^d`. Quasi-conical means it contains balls of arbitrarily large radius. The Dirichlet Laplacian is the nonnegative self-adjoint operator associated with the closed, densely defined form on `H_0^1(Ω)`, without a boundary regularity assumption. The conclusion is

\[
\sigma(A)=\sigma_{\rm ess}(A)=\overline{\sigma_{\rm p}(A)}=[0,\infty),
\quad \ker A=0,
\quad\mathcal H_{\rm ac}(A)=\mathcal H_{\rm sc}(A)=0,
\]

together with a complete orthonormal eigenbasis. The operator has pure point **spectral type**; this does not say that every spectral value is an eigenvalue, that its resolvent is compact, or that its continuous spectrum as a set is empty. In particular zero belongs to the essential spectrum but is not an eigenvalue. Positive eigenvalues are dense and need not be isolated.

Both cube widths and positive apertures are chosen inductively. The windows are holes in zero-thickness screens at common faces. The paper does not prove the assertion for an arbitrarily fixed tower, smooth boundaries, Neumann conditions, positive-length passages, or explicit numerical apertures. It gives no effective convergence modulus. Those exclusions are material, and the proof does not silently use a stronger claim.

## Proof reconstruction

### Finite geometry and the shrinking-window limit — pages 2–3

Successive cube centers are separated by the sum of their half-widths. Thus their interiors are disjoint and the new cube touches the previous cube along a face. Since the connector half-width is smaller than the old cube's half-width, its negative and positive halves already lie inside the adjacent cubes. Only the middle-face patch is added. Nevertheless the union is open, because the full connector cube is included, and it is connected. The set difference is Lebesgue-null, so the `L^2` spaces are canonically the same; the form domains genuinely differ. The proof correctly distinguishes these two facts.

For a fixed finite stage all sets fit inside one bounded box. Zero extension identifies their `H_0^1` spaces with closed subspaces of the box's `H_0^1`. As the aperture decreases, these subspaces decrease. I checked the claimed intersection directly. For a bounded function lying in all the subspaces, remove a neighborhood of the limiting interface point with a cutoff. Choose an aperture small enough that its entire connector lies in the zero neighborhood. Multiplying smooth approximants by that cutoff then gives compactly supported functions in the disconnected limiting domain. The cutoff products converge to the original function in `H^1` because the removed point has zero `H^1` capacity in dimensions at least two.

The dimensional detail is correct. For `d≥3`, an annular cutoff has gradient energy proportional to `r^(d-2)`. In `d=2` that simple cutoff would not tend to zero; the paper instead uses a logarithmic transition from radius `r^2` to `r`. Radial change of variables gives exactly the stated energy `2π∫|θ'|²/log(1/r)`. Boundedness controls the product with the cutoff gradient. Truncating real and imaginary parts first treats general Sobolev functions, since truncations preserve every form space and converge in `H^1`. The limiting form space is closed, completing the argument.

For nonmonotone sequences of aperture values tending to zero, eventual containment in every fixed larger-aperture form space gives the required weak-limit condition. The old limiting space itself supplies recovery vectors. The norm-resolvent argument then uses a common box and Rellich compactness: hypothetical bad unit inputs admit a weak subsequence, their variational solutions admit strongly `L^2`-convergent subsequences, and testing against the limiting form space identifies the limit. Compactness of the limiting resolvent gives the contradiction. This verifies **operator-norm** convergence for this bounded finite-window step, rather than confusing it with mere strong convergence. The same box gives compact resolvents and a positive Poincaré lower bound.

Dimension one is correctly excluded: every positive connector fills the shared point between adjacent intervals, and that point cannot be removed at negligible `H^1` cost. Earlier windows remain fixed throughout each use of the lemma.

### Full spectral clusters and the induction — pages 3–4

For a finite protected set of positive eigenvalues, only finitely many new cube widths in the proposed bounded interval cause a resonance. Indeed, the cube formula bounds every positive integer mode index whenever it equals a protected value. Each bounded multi-index/value pair excludes at most one width. Choosing a width outside this finite set does not alter earlier parameters and guarantees that each protected eigenspace of the disconnected sum is exactly the old one, extended by zero.

The resolvent's corresponding eigenvalues `(1+λ)^(-1)` are isolated and nonzero. Fixed contours in its resolvent set yield norm convergence of the associated Riesz projections. Projection distance below one gives equal finite ranks by injectivity of either projection on the other's range. A multiple eigenvalue may split, but its entire cluster is retained. The argument never selects one unstable eigenvector from a splitting multiple eigenspace.

At each stage there are only finitely many protected projections and isolating intervals. Their summed spectral projections converge in norm, so one sufficiently small **positive** aperture satisfies every transport bound as well as the geometric upper bounds. Disjoint intervals and use of complete eigenspaces preserve both nesting and ranks. The new largest projection is a sufficiently high spectral cutoff, chosen above every transported cluster and large enough to approximate the finite current probe set. Compact-resolvent completeness permits this. Old protected projections are not required to remain initial low-energy cutoffs, which avoids an unjustified ordering constraint.

The tail budget is summable: `Σ_(j≥n) 2^(-j-2)=2^(-n-1)`. Widths increase by more than one, so they diverge. The resulting countable induction is qualitative; it neither assumes a uniform spectral gap nor computes admissible apertures.

### Final Hilbert space and strong resolvent limit — page 4

The final domain is an increasing union of connected open finite towers. It contains each expanding cube and hence arbitrarily large balls. Apart from the countable union of null face patches, it is the disjoint union of the cubes. Therefore its Hilbert space is the direct sum of the cube Hilbert spaces, and the fixed cube sine functions form a complete orthonormal probe family. These probes need only be `L^2` vectors for the argument.

The finite resolvents extended by zero have kernels on all future cube summands. The paper explicitly recognizes that they are not genuine resolvents on the final full space. Their norms are at most one. Increasing zero-extended form spaces are closed, and their union is form-dense: any compactly supported smooth function in the final open domain has support in a single finite stage by compactness and the increasing open cover. The finite variational solution is the form-orthogonal projection of the final solution, so it converges in form norm and in `L^2`. This proves exactly the required **strong** operator convergence. No global norm-resolvent convergence is assumed or needed.

### Fixed-rank limits and exhaustive completeness — pages 4–5

For each birth index, summable transport gives an operator-norm limit of the protected projections. Norm continuity preserves self-adjoint idempotence; distance below one preserves its finite rank, and nesting survives the limit. Commutation with the final resolvent follows from uniform boundedness of the finite resolvents, their strong convergence, and norm convergence of the projections. It does not require a norm limit of the resolvents.

Each limiting finite-dimensional range is reducing for the final positive resolvent. Its restriction is injective, because a genuine resolvent is injective, so all eigenvalues on that range are strictly positive. A resolvent eigenvector consequently belongs to the operator domain and becomes a finite-energy Dirichlet eigenvector under the inverse spectral transform. This excludes loss of a nonzero protected vector into the zero-resolvent eigenspace, or equivalently infinite energy.

The proof then addresses the otherwise substantial completeness gap. Every fixed cube/basis-index pair belongs to every sufficiently late probe set. At each such stage, the **newly born** largest projection approximates it with error below `2^(-n)`; the entire future transport contributes at most `2^(-n-1)`. Thus this vector is approximated arbitrarily well by vectors in the closed pure point subspace. Since all probes form a basis, that subspace is the entire Hilbert space. This establishes absence of both absolutely continuous and singular continuous spectral subspaces. It is stronger than merely constructing countably many eigenvalues or showing that they are dense.

The nested limiting projections converge strongly to the identity. Their successive finite-dimensional orthogonal differences reduce the resolvent and admit orthonormal eigenbases, giving the asserted complete basis.

### Spectral support and zero — page 5

Normalized compactly supported bumps inside the expanding cubes, multiplied by plane waves of energy `λ≥0`, have residual norm at most `r^(-2)||Δχ||+2|ξ|r^(-1)||∇χ||`. The supports are disjoint, so the unit test functions are orthonormal and weakly zero. The singular-sequence form of Weyl's criterion therefore places every `λ≥0` in the essential spectrum, including zero. Nonnegativity gives the reverse spectral inclusion. Completeness then identifies the spectrum with the closure of the eigenvalues.

A zero eigenfunction has zero form energy, hence zero weak gradient. On the connected open domain it is constant; infinite volume rules out a nonzero `L^2` constant. This proves the endpoint claim without confusing an approximate zero-energy sequence with a zero eigenfunction.

## Primary sources checked

* [Krejčířík–Lotoreichik, arXiv v2](https://arxiv.org/pdf/2205.08172v2): §2.1 has the same form-defined operator on arbitrary open domains. Definition 2.1 and Propositions 2.2–2.3 require the relevant form convergence and a common bounded containing set, not smooth boundaries or connectedness of the disconnected limit. Section 3 explicitly uses the point-window geometry and allows future cube sizes to be chosen. Remark 3.1 warns about multiplicity and individual eigenvectors; the current full-cluster proof respects that warning. Section 5 poses the stated existential spectral-type question. The current paper additionally proves the needed bounded-window fact directly.
* [Hempel–Seco–Simon](https://math.caltech.edu/SimonPapers/217.pdf), printed page 458, Proposition 1.4 and its preceding paragraph: full spectral families are explicitly used to handle degeneracies. This supports the attribution. Their Neumann rooms-and-passages estimates are not misapplied as a Dirichlet screen-domain theorem here; the present proof supplies its own convergence and Riesz argument.
* [Oberwolfach report 36/2023](https://ems.press/content/serial-article-files/47475), printed pages 2077–2078, asks for the absence of both continuous spectral types in a connected quasi-conical construction. [Krejčířík's 2026 notes](https://arxiv.org/pdf/2609.28602v1), PDF page 16, repeat the question. These verify the problem match; they do not establish worldwide current openness. The construction answers the existential version with cube-size freedom, not a stronger preassigned-width assertion.

Acquisition URLs, hashes, sizes and timestamps are in `reference_acquisition.json` and `hss_acquisition.json`. No inaccessible reference is a remaining mathematical dependency.

## Reproduction and materially distinct controls

The authored checker passes all 4,187 exact conditions with assertions enabled. Its tests concern finite algebra, nonresonance examples, scheduling and error budgets. Assertions in that original script are not presented as meaningful under optimized Python; the supplied wrapper explicitly launches assertion-enabled children.

After the independently frozen conclusion, the complete published bundle verifier passes, including the actual published-PDF binding, 120-file inventory, original archive identities, author replay, 2,911 portable historical conditions, 2,923 optional-archive conditions, 2,304 second exact tail checks, geometric and spectral controls, and nine intended corruption rejections. The wrapper intercepts its spectral diagnostic's adjacent-file output, and confirms that source bytes remain unchanged. Some packaged geometric diagnostics use the declared relative tolerance `10^-12`; this is not a validated PDE approximation. Optional external historical corpora and queue checks are not replayed because they are outside the distribution and the present theorem.

My `fresh_exact_controls.py` imports no submitted code and passes 1,218 counted exact conditions. Its distinct mechanisms are:

* Exact polynomial integration of cutoff energies, including the logarithmic two-dimensional energy and the failure of a simple annular rescaling in dimensions one and two. The piecewise cubic cutoff used in this control is an `H^1` test with smooth approximations; the paper's smooth cutoff remains the proof object.
* Exact normalized gradient and Laplacian norms for a compact radial `H^2` bump in dimensions 2–10, giving a direct residual-squared formula `L/R^4 + 4λG/(dR^2)` for modulated Weyl tests. This is an independent valid test family, not a numerical aperture calculation.
* A failed-shortcut control: finite-rank dyadic compressions of multiplication by `1+x` on `L^2[0,1]` converge strongly to an absolutely continuous operator. Successive normalized-cell eigenprojections remain at squared norm distance `1/2`; the required summable protected transport fails. This explains why dense finite-stage eigenvalues and strong convergence alone would be insufficient.
* An injectivity control: a fixed protected direction can converge to a zero eigenvalue of a noninjective positive limit. The actual resolvent's injectivity is therefore essential to the inverse spectral step.

The exact source and results are retained. These checks corroborate estimates and reject invalid substitutes; they do not formally verify the infinite-dimensional theorem or produce concrete admissible apertures.

## Strongest verified claim and remaining limits

The strongest supported claim is Theorem 1 exactly as published, including existence for every `d≥2`, connectedness, quasi-conical geometry, a complete eigenbasis, the full essential spectral half-line, dense positive eigenvalues, and absence of a zero eigenfunction and both continuous spectral subspaces. No substantive mathematical gap was identified.

Remaining limits are the qualitative parameter choice, the explicitly restricted screen-domain geometry, absence of formal or conventional human certification, and lack of exhaustive novelty/priority determination. No arbitrary-width, smooth-domain, positive-length-passage or Neumann extension is established. Completion is **100% of the assigned analytic review**, not certainty beyond those limits. No repair, publication, site, spreadsheet, Git, Zenodo or outreach action was performed.
