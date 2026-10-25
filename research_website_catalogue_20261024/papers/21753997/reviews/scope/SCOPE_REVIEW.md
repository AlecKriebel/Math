# Acquisition and scope review: Zenodo 21753997

Completed 2026-10-25 UTC. Assignment: acquisition, reader coverage, claim scope, provenance and primary-source interfaces. **SCOPE_COMPLETE; mathematical verdict not assigned.** This report does not certify the algebraic computations, optimality enumeration or Sturm counts. No submitted mathematical verifier was executed in this scope review.

## Identity and eligibility

The freshly retrieved [Zenodo record](https://zenodo.org/records/21753997) explicitly publishes *A four-parameter family of reversible three-species mass-action continua without a common factor*, Alec Kriebel, version 2.0.0, 2 August 2026. Although Zenodo labels the resource “Software,” its title and description identify this manuscript, summarize its theorems, and identify the scoped manuscript and verification release. Eligibility is established by that explicit naming, not by finding an incidental paper inside a repository archive.

The version citation is **10.5281/zenodo.21753997**. The metadata expressly says that concept DOI 10.5281/zenodo.21753404 groups unrelated monorepo releases and is not a paper-specific all-versions DOI. The earlier edition and current edition are one work. The older eight-page PDF must not become a separate publication entry. Historical release text and the one-page statement still contain pre-release or earlier DOI information; current record metadata controls current publication identity.

There is exactly one public Zenodo asset: `AlecKriebel/Math-wr-continuum-v2.0.0.zip`, 180,108,207 bytes, MD5 `4d4c43174a28c17a82b8365ead817975`, SHA256 `d92c83fd79fc1a723bcaa3fd0674f9fcf04dec18bb6a220c583f6bef4cbdc9fd`. Both size and checksum agree with the fresh record and frozen queue. The archive is the release-tagged monorepo, not a standalone PDF upload.

The current main manuscript is the exact original ZIP member:

`AlecKriebel-Math-26f7e00/weakly_reversible_continuum_no_common_factor/releases/v2.0/output/pdf/manuscript-v2.0.0.pdf`

It has 14 pages, 108,423 bytes, SHA256 `fe429cf073b30cacfe1ba75624236cda2545c44076f711d4319dcb22ff79512b` and MD5 `30ac81f4d861406ec3e468dd8ca578b6`. The archive member and checksum, rather than a fabricated top-level Zenodo PDF URL, must bind any later display copy. The whole archive should remain an external Zenodo download. No site asset was created here.

## Acquisition and reader coverage

`sources/receipt.json` records fresh metadata, exact download URLs, checksums and the whole ZIP inventory. Acquisition used validated HTTP byte ranges after a slow initial stream was interrupted. Every assembled byte was authenticated by the final full-file MD5 and SHA256. All 4,246 member paths/types were checked against traversal, absolute paths, backslash paths, links and special nodes. All 126 regular files in this named work's subtree were safely extracted and individually hashed; their ZIP CRCs were checked on reading. Unrelated monorepo projects were not extracted or read. A final rehash found no changes to those 126 extracted files.

The five direct reader-PDF occurrences reduce to three distinct documents:

| Document | Pages | SHA256 | Reading coverage |
|---|---:|---|---|
| Current v2.0.0 main paper | 14 | `fe429cf073b30cacfe1ba75624236cda2545c44076f711d4319dcb22ff79512b` | All 14 pages, including both appendices; selected equation/table pages visually inspected |
| Historical v1.0.0 paper | 8 | `8b333f8d3e08d5b2a66ca2b78474079ef4be6b23cb497fbd991f41fae9558e4d` | All 8 pages; treated as the frozen earlier specialization |
| Specialist one-page statement | 1 | `b7429aed0e5edf572848cbcf856b3da89ff05447967c3dc12d9d386e0270f3d2` | Entire reader-facing statement |

The six nested release archives were separately inventoried without running their contents. They add eight PDF occurrences, all byte-identical to these three documents: **13 total occurrences, three distinct reader PDFs, 23 distinct pages**. One AppleDouble file with a `.pdf` suffix is macOS metadata, not a PDF; its magic bytes were checked. See `reader_document_map.json` and `nested_archive_reader_map.json`.

Necessary mathematical support read in full: current `family/README.md`, `strengthening/CLEAN_RATES_AND_STABILITY.md`, `minimality/MINIMALITY_ANALYSIS.md`, and `audit_packet/THEOREMS.md`, together with current release README, the one-page statement and main paper. Reproduction launcher and dependency lock were read to map the claimed checks. The machine matrix, submitted code and result files are acquired and hash-bound, but this scope assignment did not independently replay their mathematics. The current Markdown manuscript is also preserved and bound in the source manifest; its reader PDF is the reading target.

## Exact mathematical scope

**Model.** This is a deterministic polynomial mass-action ODE, `F(x) = sum k_(y→y') x^y (y'−y)`, with nonnegative integer complexes, strictly positive rate constants, and positive concentrations. Reversibility means each directed reaction has its reverse. It does not mean detailed balance. There is no stochastic reaction-process or experimental chemistry conclusion. The support includes the zero complex, has ten complexes and ten reversible pairs (20 directed reactions), is connected, has full stoichiometric rank three, and has deficiency six. Its one positive compatibility class is the whole positive orthant. It is not a closed mass-conserving chemical model.

**Units and normalization.** The construction is in formal concentration/time coordinates; no empirical units or calibrated chemical mechanism are supplied. Rate coefficients of differing reaction orders ordinarily have different physical dimensions. The integer maximum and sum are algebraic objectives in the fixed normalization, not dimension-independent comparisons of physical reaction speeds. Common positive scaling of every rate rescales time. The smaller integer vector is primitive.

**Common curve (pp. 2–4).** The prescribed ideal is generated by `L = z−x−y+1` and `Q = 7x²−2xy−16x+7y²−16y+16`. The nonsingular conic is a compact ellipse wholly in the positive orthant. Its rational parametrization is

`(x,y,z) = ((t²+3)/(2d), (3t²+1)/(2d), (t²+t+1)/d)`, `d=t²−t+1`.

Finite real `t` omits the projective limit `(1/2,3/2,1)`, which is included in the full ellipse. The interval `−1<t<1` already gives infinitely many distinct positive equilibria. The paper's full-ellipse statement must not be reduced to only that interval, nor should the limit point be omitted from a global stability description.

**Complete constrained rate family (Theorem 3.1 and Corollary 3.2, pp. 4–6).** For this exact support and this exact conic, the paper gives every rational rate vector for which all three coordinate polynomials lie in `(L,Q)`. The four free coordinates are `(a,b,c,d) = (k29,k43,k95,k98)`. The claimed canonical remainder matrix is 21 by 20, of rank 16, with nullity four; the seven remainder monomials and a specific 16-minor provide the completeness certificate. All 20 rates are positive exactly when `a,b,c,d>0`, `b<c`, and `192a+221c<154d`. This is a relatively open cone in a four-dimensional linear space, of codimension 16 in the ambient 20-dimensional rate space. The theorem is formulated over the rationals; the linear formulas have a natural real extension, but rational coefficient-ring conclusions should retain their stated field. Nothing asserts persistence under arbitrary ambient rate perturbations.

**Generic absence of a common factor (Theorem 4.2, pp. 6–7).** A nonempty Zariski-open part of the constrained family has coordinate gcd one geometrically. The scalar-extension lemma covers rational coefficients and common factors over the reals or complexes. The paper does not assert gcd one for every positive parameter choice. All positive choices preserve the curve; for the coprime choices, the height-two argument makes the conic an actual irreducible component, rather than a common-factor hypersurface. Genericity here is inside the constrained four-dimensional family.

**Clean specialization (Theorem 5.1, pp. 7–8).** The parameter point `(653,1,70,915)` gives the displayed primitive positive integer vector, largest entry 10,296 and sum 52,464. The coordinate polynomials are claimed pairwise coprime. Its steady ideal is claimed radical, with two minimal primes over the rationals: the conic prime and a disjoint degree-15 maximal ideal. After passing to an algebraic closure, the latter gives 15 reduced isolated points. The paper does not claim all 15 are real or positive; public explanations must not call them 15 additional positive equilibria.

**Integer optimality (Proposition 5.2, p. 8).** The clean vector minimizes both the largest entry and the sum among all positive integral rate vectors preserving this conic on this fixed support. Integrality forces `15|d` and `14|c`; a strictly better maximum forces `d<1755`, and a strictly better sum forces `d<2714`. Positivity supplies finite bounds on the remaining integer coordinates. These reductions specify finite exact enumeration. This does not prove global minimality of reaction supports, numbers of reactions, complexes, deficiency, or physical rate magnitudes.

**Frozen earlier member (Theorem 6.1, pp. 8–9).** The current paper retains the original specialization `(3920,3920,15680,658560)`. Its much larger integer rates are a separate member, not combined with the clean rates. Its conic-plus-degree-15 radical decomposition is another exact claim requiring verification. The historical eight-page PDF establishes which older construction is retained; it is not a second current publication.

**Stability (Theorem 7.1, pp. 9–10).** The transverse trace, determinant and discriminant are derived for the frozen earlier rates only. One tangent eigenvalue is zero. Exact polynomials and Sturm counts purportedly give a normally attracting arc and a saddle arc, separated by roots `alpha in (−4,−3)` and `beta in (9/10,1)`. At each transition another eigenvalue is zero and normal hyperbolicity is lost. The projective point at infinity is saddle-type. Decimal roots are orientation only. This is transverse linear/normal stability along the equilibrium set; it is not a global attraction claim or a full nonlinear classification at the transitions. It is not a stability theorem for the clean vector or every family member.

**Structural lower bounds (pp. 11–12 and full minimality note).** Three species are necessary for a nonzero coprime polynomial field with a positive-dimensional equilibrium set of the stated kind. With one linkage class in three species, rank two is excluded by weighted scaling transverse to a compatibility plane, so full rank is necessary; that proof requires the one-linkage hypothesis. Weak reversibility and deficiency zero imply at most one positive equilibrium per compatibility class. Combining these arguments gives at least five complexes for any three-species weakly reversible target. The note derives weaker count bounds (at least four reversible pairs under one linkage, maximum total complex degree at least two). The present ten-complex/ten-pair/cubic example is not proved minimal in those quantities. Earlier restricted numerical searches are expressly not a global impossibility proof.

## Primary literature interfaces and attribution

Fresh primary PDFs, exact URLs and hashes are in `primary_source_receipts.json`; downloaded binaries and text live in the ignored `.reference-cache`.

1. **Boros–Craciun–Yu (2020), *Weakly Reversible Mass-Action Systems With Infinitely Many Positive Steady States*.** Read definitions, examples and the Section 5 question in the author's ten-page [primary manuscript](https://pollyyu.web.illinois.edu/manuscripts/2020-WR%20systems%20with%20infinitely%20many%20steady%20states.pdf). Its Section 5 explicitly asks about infinitely many positive steady states without a right-hand-side common factor. It already contains reversible/connected examples and a fixed-support same-curve parameter family with a common scalar factor. Reversibility, existence of a continuum and rate flexibility alone are not new here. The relevant claimed advance is a compatibility-class continuum without a common factor, together with the exact constrained family structure. This scope review authenticates the question and attribution interface, not an exhaustive global priority search.

2. **Feliu–Henriksson–Pascual-Escudero (2026), *The Generic Geometry of Steady State Varieties*.** The fresh arXiv PDF is v3, 14 May 2026, available before the August release; the journal pagination refers to the later September issue. Read the exact hypotheses/conclusions of Theorems 3.1 and 3.4, Corollary 3.5, Corollary 3.13 and the weakly reversible discussion in Section 3.4 of [v3](https://arxiv.org/pdf/2412.17798v3). The finiteness theorem uses the augmented steady-state system with full stoichiometric-rank representation, a conservation-law matrix, and the indicated positive kernel/nondegeneracy conditions. Its generic-finiteness result and exceptional algebraic locus are compatible with this paper's codimension-16 rate constraint. It answers the separate full-parameter-open-set question negatively. The present cone must not be presented as an ambient open set contradicting that result.

No new external priority search beyond these load-bearing comparisons was performed. The record's conservative historical audit statement was read as metadata, not adopted as fresh evidence of “first ever.”

## Evidence, independence and remaining gap

Freshly checked in this assignment: complete public-asset authentication; safe named-work extraction; nested-reader identity; actual page counts; full reader-document and necessary support reading; exact claimed domains and version distinctions; primary-source problem statement and genericity interface. These are acquisition and scope facts, not a mathematical acceptance verdict.

The launcher names eight checks: release metadata, frozen construction, clean-room frozen construction, family, clean rates/radical/optimality/stability, minimality arithmetic, v2 independent audit, and integrated manuscript wrapper. Dependencies are pinned to SymPy 1.14.0 and mpmath 1.3.0. Their existence and intended coverage were read; none was executed by this reviewer. Whether their implementation proves each claim and whether fresh independent controls agree remain for the mathematical reviewers.

Dedicated historical `AUDIT`, `PROOF_AUDIT`, `AUDIT_RESULTS`, priority audit and result-verdict files were not read. Incidental status text was necessarily seen in fresh Zenodo metadata, release README, the manuscript's exact-verification section, the one-page specialist statement (“already tested”), and the strengthening/minimality notes. Those statements are author-supplied claims, not independent evidence. No sibling review report or mathematical finding was consulted.

The strongest completed result here is an authenticated, explicitly eligible, fully scoped 14-page current manuscript with its historical and companion readers consolidated into one work. The remaining publication gate is independent verification of the algebra, genericity argument, ideal decompositions, bounded integer-optimality census, stability polynomial identities/Sturm counts and structural lower-bound proofs. This scope review neither establishes a substantive defect nor clears those claims. `CONTENT_CANDIDATE.md` is conditional drafting material only.

Follow-up recommendation: **null**. The manuscript lists plausible minimality questions, but this assignment has not established a sufficiently sharp new question, mechanism or novelty case to recommend a paper-worthy follow-up. No outreach was prepared or initiated. No publication, website, spreadsheet or Git changes were made.
