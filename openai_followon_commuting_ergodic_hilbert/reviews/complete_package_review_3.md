# Fresh independent complete-package review 3

Review completed: 2026-10-07 05:55 UTC (2026-10-06 Pacific).
Reviewer: new internal complete-package research agent, with independent analytic and primary-source support agents. This is an automated adversarial review, not conventional human peer review or formal certification.

## Verdict

**No substantive issue found in the exact current complete publication candidate identified below. No known substantive mathematical, attribution, scope, package, or reproducibility concern remains from this review.** The candidate gives the requested arbitrary-commuting symmetric bilinear ergodic Hilbert variation, maximal bound, almost-everywhere convergence, and norm convergence at complex L3 inputs and every r>2, as an explicit restriction/transference consequence of the attributed full annular continuous theorem. Its stronger maximal-tail norm convergence follows from the same domination argument.

The central continuous dependency was reconstructed from its primary pinned source rather than accepted because it appeared in a release, had earlier favorable audits, or had a related Lean directory. The current dependency has no identified substantive gap. The proof adds no noncommuting, r=2, one-sided Cesaro, or broader-exponent conclusion. Its contribution is a newly available consequence with explicit singular-kernel restriction and complete finite-window transfer; the continuous breakthrough and established reduction machinery are credited.

The exact remaining gap **within the reviewed mathematical and publication candidate is none identified**. This verdict does not assert worldwide first priority, human refereeing, Lean verification, or successful Zenodo publication. Production staging, checking the actual remote metadata/file bytes, publication, DOI confirmation, and tracker verification are subsequent operations and were not performed or presumed by this reviewer. If a reviewed payload or mathematical/metadata claim changes, this verdict does not automatically apply to the replacement.

Checkpoint estimates: mathematical-resolution review 100%; publication-candidate review 100%. These are completion estimates for this review, not proof, and not an estimate that remote publication/tracking has completed.

## Independence, instructions, and reviewed inputs

I read `/Users/alec/Documents/Math/AGENTS.md` and `research/ORIGINAL_REQUEST.txt` first. I then read the candidate `main.tex` and the primary copied October 5 annular manuscript sources before relying on any earlier audit conclusion. I did not open `complete_package_review_1.md`, `complete_package_review_2.md`, their responses, research history, or the research log. The required ledgers were checked for claim correspondence; their favorable status entries were not used to validate mathematics. I recorded a direct-primary mathematical verdict in `complete_package_review_3-assets/independent-before-comparison.json` before comparing the packaged scoped audit reports. The later comparison was part of checking what the supplement actually says.

I directly read all nine primary annular section sources: introduction, preliminaries, matrix, heat, smooth, frequency, rough, completion, and consequences, plus the manuscript README, bibliography, main source, repository README and family 082 Lean scope. I read the actual pinned `lean/OAI/Analysis/TriangularHilbert/Main.lean` declaration with a read-only Git object query. I read all current candidate source, READMEs, manifest, theorem/dependency/approach ledgers, the independent restriction proof, root analytic reconstruction, priority audit/evidence/BibTeX, scoped matrix/heat/smooth and frequency/rough/completion audits, geometry code/result, and source hashes. The exact `source.zip` and `verification-supplement.zip` were extracted and checked, not inferred from their builders or receipts. All archived members match the corresponding current files.

The independent analytic support agent received the original request, instructions, current candidate and primary sources without previous review conclusions. It independently reconstructed the full analytic chain, then assigned an additional unprimed adversary to the delicate matrix/heat/frequency/rough route. Both found no substantive gap; the detailed support is `complete_package_review_3-assets/analytic_reconstruction.md`. The primary-source support agent independently checked the theorem/version records and exact citations. Its inventory query incidentally exposed short completed-agent status summaries from review 2; it disclosed that exposure and its report is treated as primary-source verification evidence, not as the fresh whole-package verdict. I independently checked the named primary arXiv histories and theorem passages as well. A separately unprimed DT/DKST comparator report is retained in the assets.

No candidate, upstream-clone, Git, deposit, tracker, or publication state was changed. The only writes were this report and assets in the authorized review directory. No external individual was contacted. The upstream clone remained at the pinned commit. All 15 copied-source hash entries were checked against the corresponding actual Git blobs at that commit, not merely against the manifest.

## Exact reviewed package

All four intended payloads are inside `publication/upload-kit/`; the manifest specifies those four files individually. There is no outer kit archive substituted for the paper and source/supplement downloads.

| File | Bytes | SHA-256 | MD5 |
| --- | ---: | --- | --- |
| `paper.pdf` | 79,186 | `5bfcfe064052e7e23005fbb45a8c83c2d1e3188ec4ef29ff97f46ea19edd60ea` | `c63ad8716687753d928852902d4e4932` |
| `source.zip` | 12,751 | `651984b7acf1186de939b437ec7216e90a34d06681ff3e6fc41f0bee89c45f6d` | `a765ae3c66e8a5b311dd70d4fbd224f7` |
| `verification-supplement.zip` | 41,798 | `36fa0e0213bce168fb1abda715fb3fd133d914dc1ceb5bcdf1624a998abc5fc9` | `867f2b2ffba3252c49346d39b09893a2` |
| `README.md` | 4,552 | `d735b20b62f2a3cf5fbba5eae95cc5a42d1b2e7faec890035742d25aaf11c252` | `7c14e66e99b9269d501feb49a25d57bb` |
| Project `zenodo-deposit.json` | 2,896 | `5cff48980a8898e552f0b1945235b3cb3a8725b295ea351fdb010d0f3e8a3845` | `5d08e557827cad999b690b78c2c07b60` |

Current and archived `main.tex`: 14,748 bytes, SHA-256 `b487be2a3233d56facde9713681733e5e6d7a8539ff6d78a94cf7d7db796f10f`. Pinned upstream commit: `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. Upstream public PDF SHA-256: `f5857c58037fa5289f2f9fe1fe4421af11df8d9fa9b2914ba041469f1195ea31`.

`complete_package_review_3-assets/exact-inputs.json` records every archive member's bytes and hash, as well as all four payloads and the manifest. `pinned-blob-comparison.json` records all 15 copied-source comparisons. Both archives pass the ZIP CRC test, contain no traversal/absolute members, and contain only the advertised source or verification materials. Source contents are `main.tex`, `README.md`, `references.bib`, `restriction_geometry_check.py` and `SOURCE_HASHES.json`. The supplement contains the listed ledgers, original audit/proof/priority materials, geometry code/result and source-hash references. It includes no credentials, caches, private communications, executable binary, or redistributed upstream manuscript/source tree. The external citation blocks are retained as attribution.

## Direct reconstruction of the new proof

The fixed geometry has input half-width h=1/8 and output half-width q=1/16. On an output point `(i+a,j+b)` the static coordinates uniquely select the corresponding lattice strips. The moving support intervals can overlap only if their integer shifts agree, because `|k-l| <= 2h+|a-b| <= 3/8 < 1`. Their exact common offset interval is

`I(a,b)=[-h-min(a,b), h-max(a,b)]`, with `ell=2h-|a-b| >= 1/8` and `|s| <= 3/16`.

Half-integer radii `rho_N=N+1/2` include an entire nonzero window precisely when `M<|k|<=N`. This is true also for negative k, with the negative denominator retained. The zero window lies inside radius 3/16 and is excluded by the smallest endpoint 1/2. No principal value or boundary partial-window contribution is hidden in the identity.

For either sign of k,

`K_k=integral_I ds/(k+s)=ell/k+delta_k`,

and `1/(k+s)-1/k=-s/[k(k+s)]` gives `|delta_k|/ell <= 3/(13 k^2)` because `|k+s| >= (13/16)|k|`. The proof does not falsely assume `K_-k(a,b)=-K_k(a,b)` at asymmetric phases. For every increasing truncation list its radial shells are disjoint, so the whole error variation is bounded by its sum of absolute coefficients. Minkowski, lattice translation invariance and Hölder give the exact error norm `pi^2/13 * ||A||_3 ||B||_3`. This is a variation bound, not just a separate bound at every N.

Every integer truncation partition maps to permitted rational continuous endpoints. Countability permits one common exceptional set. Integrating the boxwise inequality over disjoint output boxes of fixed area 1/64, using input box area 1/16 and `ell^-1<=8`, gives exactly

`D_r = 8 * 4^(2/3) C_r + pi^2/13`.

The area factor is fixed. There is no null suspension diagonal, shrinking-width limit, or constant depending on the array support.

The ergodic transfer first fixes the finite menu `{0,...,M}` and then forms orbit arrays on `Q_(L+M)`. On `Q_L`, all terms agree exactly with `H_N(S^i T^j x)` by commutation. Raising the lattice estimate to p=3/2 gives each cubic sum exponent 1/2. Integrating with measure invariance and Cauchy–Schwarz yields

`|Q_L| ||W_M||_p^p <= D_r^p |Q_(L+M)| ||f||_3^(3/2) ||g||_3^(3/2)`.

Thus integrability is established before it is used. At fixed M the outer/inner cardinality ratio tends to one. Monotone convergence over the countable menus gives the full pointwise supremum inside the output norm. The representative argument removes the countable group-word orbit of the input exceptional sets; the stated modulo-null convention likewise applies to a measurable conull witness of the relations. The main theorem assumes exactly commuting invertible measurable transformations with measurable inverses.

Finite r-variation gives a scalar Cauchy sequence by recursively selecting ordered disjoint pairs with a fixed nonzero separation if Cauchyness failed. Taking r=3 is enough to obtain a.e. convergence. `H_*=sup_N |H_N| <= V^3(H)` is in L^(3/2); both the limit and every truncation are dominated by it. The full measurable maximal tail tends pointwise to zero and is bounded by `2H_*`, proving the stated tail and norm convergence by dominated convergence. Norm limits preserve complex bilinearity.

I attacked zero inputs, identity/equal transformations, negative and small lattice indices, phase asymmetry, overlap degeneration, arbitrarily long/point-dependent partitions, inverse-word exceptional sets, transference before integrability, and the order of the two window/menu limits. None produced a counterexample or unsupported hypothesis. The ordinary one-sided average problem is not inferred from the odd symmetric kernel.

## Direct reconstruction of the pivotal continuous dependency

The full annular statement is exactly upstream Theorem 1.1: complex L3(R2) inputs; r>2; all finite rational positive partitions; supremum at each output before the L^(3/2) norm. The continuous count quantity permits disjoint annuli with output-dependent choices. I reconstructed its current proof through the following steps; the separate analytic asset supplies detailed equation and line references.

1. The supported Hessian of `tr(P^(3/2))` has entries `(3/2)|K_ij|^2/(sqrt(p_i)+sqrt(p_j))`. Supported regularization, square-root order, and inverse order justify comparison even when supports differ. Joint averaging uses vector Cauchy–Schwarz and the inverse quadratic variational formula, with no commutativity or uniform smallest-eigenvalue assumption.
2. The three-block Hermitian cycle embeds the star costs in a common metric. Grouping the cubic trace by the multiplicity of its smallest eigenvalue index gives the asserted dimension-free bound. A unit phase rotation of one edge preserves the original costs and recovers the full complex trace. Complex diagonal windows are split into eight Hermitian products. Singular or rank-zero Grams do not introduce an inverted zero eigenvalue.
3. Gaussian row and column derivatives use the correct Gram and its fixed support. Joint smoothness is separately justified by a constant-rank factorization. Plane identities are integrated derivative identities, with Gaussian domination; they are not asserted pointwise. The neighbor comparison loses only sqrt(2), leaving positive dissipation for rates `(1,11/10,11/10)`. Very unequal rates are handled by separate single-edge dissipation, not by extending that strict-star claim.
4. Repeated output masks have total jump modulus at most `2n|A_0|`. Rank-changing gradient bounds, probability Gaussian center integration and line-maximal majorants produce mixed jumps with two copies of the dual norm. Rescaling to `(n^-1/2,1,1)` gives the smooth `sqrt(n)` estimate. The hard/smooth identity has nonzero `c_0=2g_3''(0)`; no positive-sign assumption is required.
5. With `theta=1/(16D^2)`, a modulated Gaussian is expressed exactly as an average of derivatives of a narrower Gaussian. The inserted cost gains `theta s`. The averaged plane heat coefficient is `(2+theta)+(1-theta)=3`. Single-edge costs retain wide-column rate one. The delicate mixed boundary covariance is `s[[2theta,-theta],[-theta,3]]`, with determinant `theta(6-theta)s^2`; its domination by a fixed product Gaussian is uniform in theta. The resulting maximal majorant is invariant under a unimodular lattice shear. Square integration of the coefficients, rather than frequency suprema, pays all boundaries.
6. The rough family uses three vanishing moments, a broad Gaussian primitive quotient and BV derivative bounds. A translated third derivative plus Plancherel gives a single-block Fourier square bound. The cutoff error is controlled by Hölder exponents `5/2,5/2,5` and line maximal bounds strictly above exponent one. Normalizing `mu=Dc/sqrt(n)` against `d xi/D` leaves no frequency-size loss. Odd moment removal uses a summable dilation identity. Endpoint pairing uses disjointness to bound total paired length, leaves at most two unpaired endpoints in a group, and treats only `O(sqrt(n))` high-count groups pointwise.
7. Rectangle approximation handles arbitrary measurable finite-menu selectors. Finite phase choices capture complex absolute increments in duality. Smooth-input approximation is applied first to finite menus; countable rational exhaustion then obtains the genuine pointwise supremum. Dyadic rank grouping gives the convergent series `sum_j (1+j)2^(j(1/r-1/2))` precisely for r>2.

No step transfers the central difficulty to an equivalent unsupported assertion. In particular the **current** source invokes neither a Mikhlin theorem nor cross-scale orthogonality of entangled operators; its Fourier energy step is BV translation plus ordinary Plancherel within a block and the frequency-block estimate it proves. The scope of the old maximal Lean declaration is accurately distinguished: the inspected `main_estimate : MainEstimate` concerns maximal truncations, and no Lean build or formal certification is claimed for annular variation or the follow-on.

## Primary priority, version and attribution checks

I checked the current official histories of [Becker–Durcik](https://arxiv.org/abs/2603.20173) and [Demeter](https://arxiv.org/abs/math/0601277): each lists only v1. Becker–Durcik's Corollary 1.4 concerns opposite powers of one transformation and bilinear averages; at this output exponent its range includes every r>2. Their discussion around (1.8) distinguishes arbitrary commuting averages. Demeter's Theorem 1.2 treats symmetric Hilbert series with opposite powers of one transformation; Remark 1.3 includes L3 inputs in that special case. These exact theorem checks support the manuscript's narrow comparisons, not an inference from the abstracts. [Becker–Durcik v1](https://arxiv.org/html/2603.20173v1), [Demeter theorem text](https://arxiv.org/html/math/0601277).

[Demeter–Thiele Section 6, footnote 36](https://arxiv.org/html/0803.1268) credits the continuous-to-lattice and orbit-array routes. The proved nearby result is a two-parameter averaging consequence, while the triangular singular integral is described as a further goal. [DKST Section 5](https://arxiv.org/html/1603.00631) supplies positive-area phase integration for averages; its main estimate is fixed-partition norm variation, not this full pointwise Hilbert variation. The supplied OpenAI manuscript-specific BibTeX is preserved verbatim in the archive; the paper additionally points to the immutable exact commit. The pinned annular consequences were read and contain continuous maximal/PV/scalar consequences, not the requested discrete arbitrary-commuting theorem.

The primary-source support report also checked further restriction precedents. Blasco–Carro–Gillespie Proposition 3.6 supplies a one-dimensional `c/n+O(n^-2)` cell restriction; its later transfer uses opposite powers under an intertwining assumption. This does not duplicate the arbitrary two-generator full r>2 theorem. An additional machinery citation could be useful, but is optional because the candidate already credits the established reductions and disclaims inventing them. No substantive attribution repair is required.

At 2026-10-07 05:52 UTC my read-only live remote query still returned `adc7f1241b42e322a6451854ab7e4b4c146bf78a` for upstream `main`. The primary support agent separately found live raw source files equal to the pin. No later version was identified in those checked official histories/repository. GitHub API rate limiting constrained fresh creation/path-history metadata retrieval; the current remote and raw-file comparisons still work. Neither commit timestamps nor the manuscript's October 5 date establishes its exact first public-access instant, and the candidate correctly makes no such claim. No exact duplicate theorem was found in the inspected primary sources; this is a scoped negative check, not exhaustive proof of priority.

## Clean reproduction and full PDF inspection

I extracted `source.zip` into a new review-owned clean directory and ran its stated instructions with Tectonic 0.16.9 and Python 3.14.6. The fixed epoch is `SOURCE_DATE_EPOCH=1791349200`. The build succeeded; only two underfull bibliography paragraph warnings occurred. There were no missing citations or fatal diagnostics. The rebuilt PDF is **byte-for-byte identical** to the actual deposit `paper.pdf` at the SHA-256 above. Workspace `publication/main.pdf` and `publication/paper.pdf` also match it. These comparisons are recorded in `complete_package_review_3-assets/reproduction.json`.

The extracted geometry check passes all 14,850 advertised assertions and reproduces every field of the packaged result exactly: 70-digit Decimal precision, 25 phase pairs, signed coefficients, support separation, half-integer radial inclusion, large indices, seed 20261006, 30 complex-increment trials and all anchored partition menus through M=7. Its result and purpose are recorded in `kernel-check-reproduction.json`. No matrix/frequency/continuous-theorem numerical probe is used as evidence or included in the upload archives. Both READMEs and the manuscript explicitly limit these computations to Section 2 kernel bookkeeping, as required by the original request.

I rendered and visually inspected **all five pages of the actual upload-kit PDF**. The title, author/ORCID, equations, theorem, proof, page transitions, cross-references, disclosure and bibliography are readable, with no clipping, overlap, missing glyph boxes, unresolved reference or placeholder. All fonts are embedded. The PDF is unencrypted, five US-letter pages, PDF 1.5, with no form or JavaScript. Its actual PDF title and author metadata agree with the intended manuscript and manifest. The two underfull paragraph warnings produce no visual defect. The complete rendered pages and extracted text are retained only as review assets.

## Exact metadata and package correspondence

The manifest title is `Bilinear ergodic Hilbert variation for commuting transformations as a consequence of annular triangular variation`; creator is `Kriebel, Alec`, ORCID `0009-0001-9320-500X`, with no invented coauthor or affiliation. Publication kind is preprint; date is `2026-10-06`, version `1.0.0`, language `eng`, access is open, and license is `cc-by-4.0`, matching the established repository convention described in the README. Its `isDerivedFrom` relation points to the exact pinned annular PDF URL. The advertised four filenames and scoped mathematical description agree with the archived paper and README.

The title, abstract, theorem, README and deposit description preserve every defining boundary: complex L3 inputs, arbitrary commuting invertible probability-preserving transformations, symmetric odd sums, H0=0, every r>2, supremum inside L^(3/2), maximal bound, a.e./norm convergence and maximal-tail convergence. They accurately attribute the continuous analytic breakthrough, describe the restriction/transference contribution, and disclose extensive AI use and absence of conventional human peer review. They neither call automated reviews human refereeing nor claim annular/follow-on Lean verification. The fixed supplement's pending-status ledgers are expressly labeled checkpoint records; they do not assert an already published DOI or completed tracker entry. Later review and receipts are appropriately kept outside the already-reviewed payload so it does not need to contain its own future verdict.

All changes required by this review: **none**. The optional additional machinery citation is not a correctness, attribution, originality-scope or publication blocker. The exact hash-bound candidate above has passed this fresh whole-package pass.
