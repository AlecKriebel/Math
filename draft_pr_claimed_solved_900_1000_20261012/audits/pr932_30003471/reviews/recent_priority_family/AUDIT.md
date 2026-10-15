# Independent recent-priority audit: PR932 / 30003471

Audit date: 2026-10-15 UTC. Scope: recent spin/Dirac/smooth-approximation priority, exact fixed-face-lattice comparison in dimension three, and the candidate's stronger entire normal-Gram conclusion. This audit adds zero author proof-search turns; the original accounting remains 1/5. No sibling report or historical audit verdict was consulted. No external person was contacted and no outreach was prepared. No Git, service, tracker, publication or original-packet mutation was performed.

## Finding

The original comparison and the full Gram conclusion are **already asserted in prior preprints** under hypotheses that can be checked for arbitrary fixed combinatorial equivalence, including nonsimple vertices. This is stronger priority evidence than a vague connection to Gromov's conjecture. The critical regularity bridge is supplied explicitly in `PRIOR_IMPLICATION.md`, rather than inferred from a PL map.

Wang-Xie-Yu, arXiv:2606.30130v1, Theorem 1.2, literally implies the original comparison. The actual endpoint proof on pp72-73 yields a nonzero parallel section satisfying all assigned facet conditions. In Euclidean source and target trivializations, those conditions yield **every** normal inner product, even between disjoint facets; the exact algebraic derivation is recorded. Wang-Xie, arXiv:2203.09511v2, Theorem 2.9(iii), already states the transported-normal conclusion directly. The older Wang-Xie-Yu v6 comparison theorem also applies. The shared analytic index proofs have not been independently audited in this priority review.

The candidate honestly already disclaims novelty and credits WXY and Bi. There is no newly identified correctness defect in its claimed use of the prior smooth-domain input. Publication framing must retain the difference between an independently checked candidate proof, earlier asserted preprint conclusions, and accepted literature. It cannot be presented as the first solution, a new full normal-Gram rigidity theorem, or proof that a currently open problem has just been settled for the first time.

## Independent reconstruction and authentication

Before looking at any historical audit verdict or current family report, I read the complete charter, exact original `public/PROOF.md`, original `SOURCE_STATUS.md`/`SOURCE_METADATA.json`, and complete private cached source record. I wrote `INITIAL_RECONSTRUCTION.md`. The cached record's dated open classification is a lead to recheck, not evidence of openness on the audit date.

The independent start authentication compared all 29 original selected files against **actual** Git blobs at `c09ef9df8b1f4642be0396ba6343344be8fa25b0`. Every byte matched. The exact proof hash was `6015fcacefd914217ddadc816a5c84c1be250ec58838df891f267835f9198415`; the outer publication-manifest hash was `d1b3a0528bf518640a117c2cfecff5bc81d21f58632f7b4f647ae998eb4dcedd`. End authentication repeats that comparison. Current checkout is `main`; no change to its state was requested or made by this family.

The exact target denies strict dominance at all corresponding edges for a **given** face-lattice isomorphism. The candidate's stronger claim is all weak angle inequalities imply equality of the entire outward-normal Gram matrix. A theorem giving only edge-angle equality is not automatically the stronger statement. A fixed polytope with a smooth neighborhood metric is also not automatically a pair of arbitrary realizations. These distinctions drive the audit.

## Primary sources and exact status

All version information below was checked against the actual unversioned arXiv abstract pages on 2026-10-15; version-pinned PDF bodies were downloaded, hashed, extracted privately, and material formula pages were inspected as actual pixels. Source hashes and retrieval times are in `SOURCE_RETRIEVAL.json`. Journal access limitations are in `JOURNAL_ACCESS.json`.

| Source, actual latest version | Exact relevant hypothesis/result | Applicability and certification boundary |
| --- | --- | --- |
| [Bi 2608.06320v1](https://arxiv.org/abs/2608.06320v1), 2026-08-06; 18 pp | Theorem 1.1: smooth metric on a neighborhood of one fixed convex polytope; nonnegative scalar/facet mean curvature and weak dihedral comparison; flatness and incident normal equality. | Its headline theorem alone needs a smooth nondegenerate metric bridge absent for arbitrary realizations. Full body read for mechanism comparison; no journal record verified. |
| [WXY3 2606.30130v1](https://arxiv.org/abs/2606.30130v1), 2026-06-29; 74 pp | Theorem 1.2/6.7: connected spin 3D polyhedral source, convex Euclidean target, nonzero-degree polyhedral map, curvature/dihedral inequalities. Definition 2.8 permits vertex nonsmoothness; Remark 2.9 permits degeneracy with an assigned face map. | Every geometric/map/spin hypothesis is checked here. Original comparison follows from the stated theorem; full Gram follows from its actual parallel-section output. Full singular index proof not independently checked; no journal record verified. |
| [WXY 2112.01510v6](https://arxiv.org/abs/2112.01510v6), 2023-03-08; 116 pp | Theorem 1.7 permits derivative factors multiplying target scalar/facet mean curvatures; nonzero Euler characteristic and A-hat-degree; stricter stratum-preserving polytope map. | Explicit smooth slack-weight map satisfies the map definition; flat target kills derivative factors; equal dimensions reduce A-hat-degree to degree. Prior asserted exact comparison. Full proof not audited; BHS v2 says this version remains under verification. |
| [WX 2203.09511v2](https://arxiv.org/abs/2203.09511v2), 2023-03-21; 27 pp | Theorem 2.9(iii): equality of inner products of arbitrary transported facet normals. Theorem needs a polytope degree map and boundary contraction; Remark 2.12 removes contraction on flat target faces. | Exact all-Gram conclusion in the Euclidean case; alternatively enforce contraction by constant source scaling, which preserves angles and normal inner products. Proof relies on older WXY; not independently audited or verified as journal accepted. |
| [Bär-Hanke-Schick 2202.05180v2](https://arxiv.org/abs/2202.05180v2), 2026-07-15; 4 pp | Explicit counterexamples to particular WXY **v2** index/general statements; Discussion 7 says WXY v6 remains under verification. | Complete note read. Nonconvex examples do not falsify this convex comparison. Does not directly refute WXY3 v1 or Bi v1; no inference of current openness is licensed. |
| [Brendle 2301.05087v4](https://arxiv.org/abs/2301.05087v4), 2023-11-28 | Polytope theorem has matching-angle hypothesis. Section 2 separately treats smooth convex domains with a smooth sphere map homotopic to the Euclidean Gauss map; Propositions 2.9, 2.14, 2.15 supply the energy, regularity, positive index. | Published [Invent. Math. 235 (2024), 669-708](https://link.springer.com/article/10.1007/s00222-023-01229-x), online 2023-11-29. Actual author manuscript Section 2 inspected. Journal PDF attempt returned publisher HTML; exact final journal body not compared. Smooth propositions, unlike the headline theorem, apply to the candidate input. |
| [Brendle-Wang 2308.08000v2](https://arxiv.org/abs/2308.08000v2), 2025-07-07 | Theorem 1.3 assumes smooth neighborhood metric and all incident target-normal inner products nonpositive, with source comparison; uses smoothing and Morrey/Fefferman-Phong control. | Published [J. Reine Angew. Math. 827 (2025), 191-225](https://www.degruyterbrill.com/document/doi/10.1515/crelle-2025-0048/html), online 2025-07-31, print 2025-10-01, per indexed official publisher result; author's publication page confirms record. Direct body/PDF returned empty responses or 405 through web. Actual arXiv theorem/caveat body inspected. Not a literal unrestricted pair-realization theorem. |

The table is not a declaration that any whole preprint is correct merely because a theorem is printed. The checked implication and the unchecked analytic premise are separately identified.

## The regularity and metric bridges are substantive

The PL face homeomorphism h is used only for topological degree. It is not asserted smooth. A finite ambient smooth partition subordinate to balls avoiding every nonincident facet produces a genuinely smooth Lipschitz degree map f with the assigned face inclusions; it can be constant near vertices, as WXY3 explicitly permits. Face-preserving straight homotopy to h proves degree, with no regularity assumption on h.

For the older definitions, the explicit weights

    w_H(x) = product_{F_i not containing H} b(-u_i(x)),
    b(t)=exp(-1/t) for t>0 and 0 otherwise,
    f_s(x) = sum_H w_H(x)y_phi(H) / sum_H w_H(x)

give a globally smooth map that takes relative interior H into relative interior phi(H). This is proved from face incidence and positivity, not assumed. It has the required smooth base directions and nonzero degree. Every map uses the **specified** correspondence. Spin follows from the trivial Euclidean tangent bundles; the polyhedral-manifold definition allows the actual nonsimple tangent cones. These maps can have singular derivative, so their existence emphatically does not supply a nondegenerate pulled-back metric for Bi's fixed-domain theorem.

## Mechanism overlap and identifiable added value

The candidate's proof follows the recent smooth approximation program very closely. The strongest overlap is with Bi: the same Phi inner approximation and active-set localization, the same two-facet spherical arclength transport, the same positive hemisphere condition, the same logarithmic vertex transition with delta=lambda^(-1/4), and the same trace absorption, normalized strong nonzero parallel limit and Clifford-intertwining finish. Bi's pp10-11 explicitly make the form of q inessential, give the hemisphere contraction and logarithmic cutoff; pp15-18 give the sliced L2/H1-L4 bound, existence, strong nonzero limit and rigidity. These are verified method correspondences, not suspicions based on an abstract.

The candidate's identifiable adaptation is an explicit degree-one collar map q with simultaneous positive inner products against the **target** normals for arbitrary fixed face correspondence. In Euclidean 3D its two-face transport has exact rank-one contraction rather than Bi's bounded metric error. This removes the bounded edge defect and makes the global boundary L2 argument particularly transparent. The nonsimple case is handled without inventing a vertex diffeomorphism. The candidate also spells out uniform trace/extension, no loss of mass, and full Gram algebra.

Those features can support a useful specialized independent proof, exposition or simplification built on Brendle and Bi. This audit does not establish that the target-normal compatibility observation or exact simplification is novel. WXY/WX's earlier conclusions prevent a new-result claim for either the target comparison or the full Gram assertion, while their distinct singular-domain index route is not a dependency of the candidate. An independent smooth proof may still reduce reliance on that delicate analytic route.

## Required framing, optional improvements and exact gaps

Required for any promoted research output: retain explicit Bi/Brendle credit; acknowledge that the exact comparison and full normal-Gram statement occur in the earlier asserted comparison program; describe WXY3 and older results as prior preprint assertions unless independently checked or publication evidence is obtained; separate the checked applicability derivation from a full proof audit; do not label the dated cached problem status as current openness. These are publication-framing constraints. The exact original proof already contains substantial appropriate credit and disclaims firstness, so this audit has not found an existing false firstness statement to correct.

Optional improvement: cite WX Theorem 2.9(iii) and Remark 2.12 directly for the stronger Gram overlap, and include a compact smooth carrier-map lemma to make the WXY3 corollary transparent. Describe the contribution as an independent Euclidean three-dimensional adaptation of Bi's smooth method, conditional only on the separately audited published smooth-domain input. Avoid calling the smoothing/logarithmic cutoff method itself new.

Remaining gaps in **this priority certification**: the full WXY3 singular analytic proof and the older WXY/WX proofs are not independently verified here; no journal acceptance of the 2026 preprints was found in bounded official-primary checks; the two journal final PDFs were not retrieved for byte/text comparison; unindexed work and later changes after the audit timestamp are outside coverage. The actual latest version records and material bodies support no blanket declaration that the problem is currently open, nor that all prior literature is accepted as settled.

## Release boundary

Only the explicit curated files listed in `MANIFEST.json` are public audit artifacts. All downloaded bodies, HTML, extracts, page images and temporary files remain excluded under `private_sources/` or `tmp/`; the complete cached source body was never copied into the release set. The manifest excludes itself and is externally pinned by its final SHA256 supplied to root. No paper, acceptance, service or publication write is authorized by this review.
