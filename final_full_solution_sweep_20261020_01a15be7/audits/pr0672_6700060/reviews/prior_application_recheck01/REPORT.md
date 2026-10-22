# PR 672: independent prior-application and completeness review

Review date: 2026-10-21 UTC. Exact immutable input: `13d9b2d944ce8ec121381a4bc21e48d2bb19846e`. Target supplied by the parent: 6700060 / AMR-066-0060, Gromov 2017 Question 64. This review is a fresh source-implication and originality-boundary assessment, not a fresh validation of all analytic foundations of a prior geometric PDE theorem.

## Verdict

**The candidate contains a complete immediate application of a credited prior preprint theorem in its explicitly ambient-smooth category. It contains no genuinely new full-resolution mechanism. It fails a gate requiring a new mathematical discovery for a new findings publication, while passing the narrower application-consistency check conditional on Bi's stated theorem.** This is positive dated overlap, not a novelty inference from empty search results.

The decisive prior source is Yuchen Bi, *Dihedral Rigidity for Convex Polytopes by Smooth Approximation*, [arXiv:2608.06320v1](https://arxiv.org/html/2608.06320v1), Theorem 1.1. Version 1 was submitted August 6, 2026 at 17:35:23 UTC. The exact candidate head's author and committer dates are October 5, 2026 at 09:24:40 UTC; its proof/status records also date themselves October 5. The theorem is therefore a concrete earlier source for the submitted result. The candidate explicitly credits it and explicitly disclaims a new theorem, priority, and new discovery. This review identifies a selection/novelty failure, not concealed appropriation or a mathematical counterexample to the qualified application.

The source is a recent preprint. The live [arXiv abstract page](https://arxiv.org/abs/2608.06320) showed only v1 and no journal reference at this check. No journal acceptance, conventional human peer review, formal verification, or community consensus is certified. I freshly checked the original question, the exact theorem statement and its conventions, and independently derived the implication. I did **not** freshly verify the entire 18-page smoothing/Dirac/trace/compactness proof or Brendle's imported analytic foundations. The earlier candidate audit's stronger claim of finding no analytic gap is an inspected historical assessment, not a conclusion independently reproduced by this review.

## Scope and independence

A fresh read-only GWS ledger query preceded substantive mathematical work. It returned 178 rows (177 data rows plus header), with zero exact target entries. Broad lexical hits at row 4 (AMR-066-0025) and row 61 (Fuchs 2021 Conjecture 2.7, 5000006 / AMR-049-0006, PR 152) were independently excluded. `GWS_RECEIPT.json` pins the response and its scope. This ledger result concerns duplication only and contributes nothing to the mathematical priority finding. The parent's full authenticated Zenodo check is outside this subreview and is not claimed as my independent work.

Before reading candidate mathematical bodies or old target acceptances, I retrieved the original Gromov and exact Bi v1 sources, derived the pullback implication and the category boundary, and preserved `INDEPENDENT_DERIVATION.md` with a timestamped digest in `INDEPENDENCE_CHECKPOINT.json`. That checkpoint is unchanged. Only the supplied 24-path binding list had been inspected before it. Candidate acceptance was read subsequently, for comparison rather than as evidence establishing my independent implication.

All 24 candidate files were then extracted read-only with `git show <exact-head>:<path>` into a new private directory. Their sizes and SHA-256 digests all match the supplied exact-head bindings. A separately authored passive manifest check confirms the 24-file release inventory and the nested 11-file author / 7-file audit inventories. No candidate verifier or certificate-writing script was executed by this reviewer. The parent handles original-script replay separately. All scholarly source bodies and extracted texts remain under this review's `private/` directory.

## Exact target

Gromov's [October 1, 2017 compilation](https://www.ihes.fr/~gromov/wp-content/uploads/2018/08/101-problemsOct1-2017.pdf), §22, printed page 60, concerns compact, full-dimensional convex Euclidean polyhedra. Convex extremality means that a combinatorially corresponding convex competitor cannot weakly decrease all corresponding interior dihedral angles unless all are equal. Mean-convex extremality prohibits a diffeomorphic Euclidean domain with nonnegative mean curvature on each corresponding face, all corresponding interior dihedral angles at most the originals, and at least one strict angle inequality at a point. Question 64 asks whether convex extremality implies that prohibition. Printed page 61 gives cube context. The original source does not add distance contraction, boundary isometry, fixed volume, or fixed edge-length hypotheses.

The candidate's controlling README and release status impose a face-preserving closed-domain map and inverse smooth in the ambient-extension sense, with differential nonsingular through every corner. This restriction is indispensable to the submitted route. The 2017 paragraph does not itself settle every possible interpretation of differentiability at a nonsimple corner. Gromov's [September 20, 2013 author manuscript](https://www.ihes.fr/~gromov/wp-content/uploads/2018/08/Plateauhedra_modified_apr23.pdf), §1 printed pp.2–3, uses ambient-extension cornered smooth structures, supporting the naturalness of this convention. That definition does not prove equivalence with a broader facewise/interior smooth singular category.

## Checkable implication

Let P be such a convex polytope and let f:P→D be a prohibited competitor map under the explicit ambient-smooth convention. Locally smooth ambient extensions of f and f^{-1} satisfy the chain-rule identity on the interior. Density and derivative continuity give the same inverse-derivative identity on every closed corner. Thus DF is invertible at every point of P. Compactness yields a neighborhood on which its determinant remains nonzero. Local component extensions can be glued by a partition of unity: they agree to every order along P because they agree on its interior. The resulting ambient extension F gives

    g = DF^T DF,       det(g) = det(DF)^2 > 0.

It is a smooth positive definite neighborhood metric. The inverse function theorem makes F a local Euclidean isometry there, so R_g=0. Global injectivity of the extension outside P is unnecessary. The candidate's alternative direct tensor-gluing construction is also sufficient; all jets match on P, and the theorem does not constrain curvature outside P. This closes the often missed neighborhood, positive-definiteness, and boundary-jet issues rather than assuming that an interior pullback extends regularly.

At a facet interior, Df maps the tangent hyperplane to the corresponding tangent hyperplane and maps the domain's inward side to its inward side. It consequently maps the outward g-unit normal to the outward Euclidean normal, independent of whether F preserves ambient orientation. The second fundamental form and its trace are transported by the isometry. Hence the given sphere-positive outward mean-curvature inequality on D becomes the required inequality on P. Smoothness extends it to the closed facet. A convention in which the sphere has negative mean curvature would not be interchangeable here.

For outward-normal angles α and α_g, the interior angles satisfy θ_P=π−α and θ_D=π−α_g. Therefore

    θ_D ≤ θ_P  ⇔  α_g ≥ α.

This is precisely the direction required by Bi. His stated theorem applies for every n≥3, arbitrary compact full-dimensional convex polytope in an irredundant halfspace presentation, and a smooth neighborhood metric. Its statement imposes no simplicity, acute-angle, upper dimension, or additional spin hypothesis. No orthant chart at a nonsimple vertex has been used in the application.

The essential conclusion is equality of metric and Euclidean outward-normal inner products on every nonempty intersection of two distinct closed facets. Since arccos is injective on [-1,1], α_g=α and θ_D=θ_P. This excludes strict decrease anywhere on a codimension-two face, including its closed endpoints or higher-corner boundary. Even continuity from the relative interior would suffice for that last extension.

The scalar-flat conclusion alone would do nothing: every such Euclidean pullback was already flat. An affine shear is flat and has straight, totally geodesic faces but changes some angles. It is the theorem's equality clause under the simultaneous angle inequalities that completes the contradiction.

P's assumed convex extremality was never used. Thus, **conditional on the prior theorem**, all compact full-dimensional convex P have the desired mean-convex extremality in this category. The implication asked in Question 64 follows as an immediate corollary of a strictly more general prior statement.

## Dimensions two and one

Bi's theorem is stated for n≥3, so n=2 needs a bridge. For a curvilinear polygon diffeomorphic to a disk, orient the boundary positively. The signed turning curvature k has the sphere-positive outward mean-curvature sign. Planar Gauss–Bonnet gives

    integral k ds + sum_i(π−θ_D,i) = 2π.

The reference convex polygon has sum_i(π−θ_P,i)=2π. Nonnegative k and all θ_D,i≤θ_P,i force equality in each angle. Thus the separate planar proof is complete and classical. Alternatively P×[0,1], g⊕dt² meet the dimension-three hypotheses: scalar curvature is zero, cap faces are totally geodesic, old side curvature retains its sign, cap-side angles are π/2 and side-side angles are inherited. This alternative product reduction independently confirms that no dimension-two gap is concealed in the application.

For n=1 no codimension-two stratum supports the required strict angle inequality. Its strict-angle obstruction is vacuous. Neither observation yields a new research mechanism.

## Adversarial controls and remaining boundary

`exact_application_controls.py` is newly authored for this review. Its 358 exact rational/polynomial diagnostics pass under normal and optimized Python with identical outputs. It checks a nonlinear smooth shear and inverse, derives its metric/connection and all zero Riemann components, checks positive outward mean curvature of an epigraph facet, verifies orientation reversal, checks nonsimple cross-polytope vertices in dimensions 3, 4, and 7 and product normal pairings, detects the wrong use of flatness alone, and checks the planar turning budget. Details and equations are in `DERIVATION_ADDENDUM.md`; exact execution bindings are in `EXACT_CONTROLS_RECEIPT.json`.

Dropping smooth inverse/nonsingularity invalidates the central bridge: x↦x³ has a smooth forward map but the pullback 9x⁴ dx² degenerates at the endpoint. A map only smooth on open faces/interior can similarly fail to produce a smooth positive definite neighborhood metric. This is a counterexample to an unjustified reduction, not a counterexample to Bi or the qualified result. Neither the candidate nor this review supplies a regularization theorem preserving all weak curvature/angle inequalities, or any other bridge resolving that broader category. Its status is unverified here; no assertion that it is globally open follows from this bounded review.

These checks do not certify an index theorem, trace inequality, compactness argument, the source's analytic proof, or every dimension by computation. Nor does a failure of novelty constitute a refutation of the imported theorem.

## Candidate-wide mechanism inventory

The exact candidate's `public_packet/PROOF_APPLICATION.md` describes itself as a source application, imports Bi Theorem 1.1, gives the standard pullback/neighborhood bridge and a planar turning proof, and states that the extremality hypothesis is unused. `PROOF_VERIFICATION.md` and `independent_audit/INDEPENDENT_AUDIT.md` explain checks of Bi's smoothing/analytic route and its published smooth-boundary input. Their claimed acceptance remains qualified by the recent-preprint and ambient-smooth scope. They do not replace Bi with a new theorem or enlarge the competitor category.

The controlling README and `RELEASE_STATUS.json` expressly set `new_discovery_claim=false` and retain broader-category nonverification. `APPROACH_LOG.md` says new theorem hunting stopped after the credited implication. The finite controls test conventions and analytic algebra/scaling; the verification wrappers, manifests, statuses, and replay records test integrity or report earlier checks. No remaining file supplies a novel construction, a stronger original theorem, a new all-category reduction, or another mechanism giving a new full resolution. The two fresh PDFs also exactly match the candidate's Gromov/Bi PDF size and SHA-256 records.

## Disposition and limits

Strongest independently established result: a fully checkable implication from **the stated** Bi v1 theorem to the complete ambient-smooth Euclidean competitor claim, with a separate classical n=2 proof and vacuous n=1 case. Strongest originality finding: the exact head is an openly credited October 2026 application of a concrete August 2026 preprint, and is unsuitable as a new discovery under that criterion.

No fresh full analytic validity certificate is issued. No unrestricted corner-category full resolution is issued. The current problem detail page, its private AI reports/corpora, exhaustive literature/history, WXY/Bär–Hanke–Schick status, Brendle's proof, and the authenticated Zenodo account were not independently rechecked in this subreview. Claims about them in the historical candidate are not silently adopted.

Recommended action for a sweep requiring novel findings: exclude this candidate from new-result publication on positive prior-source overlap, retaining the credited and scoped application as a historical review result if useful. No source correction or new DOI is needed to establish this exclusion. No provider mutation, tracked source edit, branch/index change, commit, push, release, external contact, inter-agent message, or skill generation was performed by this reviewer.

Completion estimate: **100% of this bounded prior-application review**. No percentage of solving a broader corner-singular problem or independently validating Bi's full theorem is assigned. `SEALED_MANIFEST.json` binds the completed outputs and private inputs; `SEAL.json` records that manifest's digest and this report's digest.
