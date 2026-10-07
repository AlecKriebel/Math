# Independent complete-package review 02

Checkpoint: 2026-10-07 04:30 UTC. Assigned independent review completed: 100%.

## Verdict and exact reviewed version

**PASS for the exact corrected candidate identified below.** I found no unresolved substantive mathematical defect in the claimed scope, no mismatch between that scope and the deposit description, and no failure of the current extracted-package tests. This is an independent analytic assessment, not a reproduced Lean certificate, a novelty certificate, human peer review, or verification of any external publication state.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `main.tex` | 16302 | `a79834253a16ffd6258d53cde81494d812470052b4f11732636c9dcc39932f57` |
| `publication/upload-kit/paper.pdf` | 79097 | `6192382c55a3ac50ee76ce2514579a330dda1da6d873a32944a03bef26ed3179` |
| `publication/upload-kit/source-and-verification.zip` | 98624 | `e28bedc9de3547082c660bc00699961f333ac3cb81c07fbee58a6b79deaa29d9` |
| `publication/upload-kit/README.md` | 6229 | `386d94cd217b609a1509bc6b3015bc583e3c7470d86a999fa6cbb5dcc930dac6` |
| `zenodo-deposit.json` | 2875 | `e07287fadc017b6fd4f0a3db4853dadfbafa978fa23eb1e2934e3af77fd0ec91` |

The ZIP's internal `PACKAGE_CONTENTS.json` has SHA-256 `d0d7abd687e19886635f74bc43c82cbddc1f0fba960721b7c5fea38fbb3eccc0`. The ZIP is marked `candidate-for-complete-review`, and the external builder receipt has `publication_ready_asserted_by_lead=false`. Those statuses are appropriate: this review was not yet in the archive. Adding this report or changing the final-status assertion necessarily creates a different ZIP; the later assembled-package check must identify that new archive exactly. This verdict does not silently extend to a changed mathematical source or upload artifact.

## Scope and independence

I treated the original targets as hypotheses: every ambient `n>=2`, every `0<=p<1`, and every smooth strictly positive even spherical datum must admit exactly one positive even smooth support solution with positive curvature-radius matrix; arbitrary full-dimensional origin-symmetric bodies with identical `S_p` must coincide for `0<p<1`. General singular-measure uniqueness at `p=0` must be excluded.

I read the complete manuscript and the project requirements in `RESEARCH_LOG.md` and `CURRENT_THEOREMS.md`, both READMEs, dependency ledger, approach table, intended deposit metadata, source inventories, all narrow analytic/formal/priority audit reports, root validation, computation and reproduction records, and the actual packaging/reproduction programs. I inspected the selected actual Lean statement and definitions, not merely the catalogue entry or comparator. I independently checked the needed upstream analytic proof at the pinned checkout and the pivotal primary external sources. I formed my mathematical assessment without consulting another complete review's substantive opinions. The current ZIP's historical review/response files were checked as archived bytes and version evidence, not used as proof premises. I additionally delegated a narrowly scoped, independent primary-source falsification of the regularity passage; its report is `review_02_regularity.md`.

The upstream scope was the analytic chain needed for the all-body logarithmic Brunn–Minkowski inequality: introduction/reduction, moment construction, integration identities, density, tensor algebra, variance, and the slab/all-body limit. Separate measure and B-conjecture applications and the claimed equality classification are not needed here and were not certified by this review. I did not manually audit every line of the 1.2-MB Lean proof or attempt a second kernel build. No upstream file was modified.

## Substantive finding, now resolved

The earlier candidate's claim that positive bounded local Monge–Ampère density itself gives local strict convexity was insufficient and, as a standalone implication in chart dimension at least three, false. This was a real logical defect in the explanation of smooth existence, not an aesthetic citation preference. An explicit counterexample and exact primary-source mechanism are preserved in `review_02_regularity.md`. For example, on a small cylinder in three variables,

`v(x_1,x_2,t)=1+(x_1^2+x_2^2)^(2/3)(1+t^2)`

is positive and convex with smooth positive bounded Alexandrov density `(32/27)(1+t^2)(1-7t^2)`, but is constant on the interior axis. Thus a density-only localization statement cannot supply the missing strict-convexity hypothesis.

The corrected `main.tex:165` now invokes the required global geometry: BBC Theorem 1.1(i), the origin-interior condition, the empty exceptional set, `C^1` boundary, and support-function duality before Chou–Wang Proposition 1.2. I rechecked that precise correction in the final source, page 4 of the exported PDF, the smooth-transfer report, root validation, and dependency D7. It resolves the defect without narrowing the theorem. The child's regularity report describes the pre-repair issue; the final-version conclusion in this complete review supersedes its request for correction.

## Independent mathematical checks

### Nonsmooth variation and positive-p rigidity

The first-variation lemma does not assume that a logarithmic interpolation is already a support function. For `A=W[a]`, compactness gives an active defining half-space at each boundary point. At almost every boundary point the outer normal is unique, so an active direction is that normal and `h_A=a` almost everywhere for `S_A`. The exceptional boundary points have zero boundary-area measure. This justifies both uses of the contact property in the manuscript's mixed-volume sandwich.

I independently checked the two inequalities in that sandwich from the classical first Minkowski inequality, in both body orders. Uniform positivity and uniform convergence of the data give the stated dilational inclusions and Hausdorff convergence. Weak surface-measure convergence and uniform convergence of the difference quotient then give the same derivative from both sides; reversing the order after division by negative `t` does not alter the result. The factor in the volume derivative is exactly one, and the normalized log-Minkowski inequality has the factor `1/n` on its volume logarithm.

Jensen is applied to the strictly convex exponential of `p log(h_L/h_K)`, with `p>0`. Equality forces the support ratio to be constant only `S_K`-almost everywhere. The manuscript correctly avoids promoting that assertion to pointwise equality for a singular surface-area measure. Instead the ratio gives `V_1(K,L)=cV(K)` and equality in the ordinary first Minkowski inequality, hence a homothetic translate. Origin symmetry removes the translation by boundedness. The reverse implication for dilates is immediate. This argument needs no log-BM equality classification and no full-support assumption on `S_K`.

For identical `S_p`, the two mixed volumes are respectively `V(L)` and `V(K)`. Comparing both orders with `n-p>0` gives equal volumes and then equality of the bodies. The proposition validly states the mixed inequality for every `p>0`; the identical-measure theorem uses it only for `0<p<1`, so the necessary positive exponent is present. Full dimensionality and origin symmetry ensure positive support throughout.

### Smooth p=0 endpoint

I read the actual [He–Liu v1 theorem and Section 3](https://arxiv.org/html/2510.21530v1), rather than using the abstract. Its ambient/sphere dimension conventions change, and the displayed positive-p derivative calculation contains omissions. The present manuscript does not depend on that positive-p calculation: it supplies the stronger general-body proof above. Its p=0 local proof is independently checkable.

Both endpoint solutions have `M=nV`, so their common cone-volume probability measure is `f dω/M`. The log-Minkowski inequality makes each a global minimizer of the scale-invariant functional `F`. Applying the inequality in both orders shows that their logarithmic integrals agree. The path `q_t=h_0 exp(tw)` has positive curvature matrix on a neighborhood of zero by compactness and openness. Consequently, for small `t>=0` it is a genuine smooth support function, the log-BM inequality gives `V(q_t)>=v`, and global minimality gives the reverse inequality. Thus its volume is `v`, and it is a minimizer, throughout a small one-sided interval. Arbitrary even support variations yield `q_t det Q(q_t)=f` pointwise because the continuous integrand is even.

This only requires right derivatives at zero, exactly as the repaired manuscript says. The path itself is smooth through zero; an equation established on `[0,δ)` has the stated first and second right derivatives. No assertion that the entire interpolation from zero to one has positive curvature is needed.

Writing `A=Q(hw)`, I independently obtained

`Q(hw²)=2wA-w²Q+2h dw⊗dw`,

`tr(Q^-1 A)=-w`, and

`0=-tr((Q^-1 A)²)-(n+1)w²+2h Q^-1(dw,dw)`.

The coefficient is `n+1` because the tangent dimension is `n-1`. The matrix in the trace is similar to a real symmetric matrix, so its squared trace is nonnegative. At a maximum and a minimum of `w`, its gradient vanishes and the identity forces the extremal value to be zero. This gives `w=0` everywhere, including ambient dimension two. Neither a maximum-principle regularity gap nor a hidden two-sided interval assumption remains.

### Existence and support regularity in every dimension

The primary [BBCY v2 paper](https://arxiv.org/pdf/1710.04401v2), Theorem 1.7 (PDF p. 4) and Proposition 7.3 (PDF p. 18), covers `-n<p<1` with positive bounded density and preserves invariance under any closed subgroup of `O(n)`. I read the group-invariant proof on pp. 18–19: averaging a support function over Haar measure gives an invariant convex body, and invariant measures transfer the variational identity back to arbitrary support tests. This is an existence argument and does not assume uniqueness. Its directly stated origin-interior guarantee is restricted to `p<=2-n`; that restriction would be insufficient here. The manuscript correctly obtains an interior origin from full dimensionality and `K=-K`, using `G={I,-I}`.

The primary [BBC smoothness paper](https://www.renyi.hu/~carlos/lp-chou-wang-smoothness-jga.pdf), Theorem 1.1(i) (PDF p. 3, extracted lines 118–129), defines an exceptional set by boundary normal cones contained in `N(K,0)`. An interior origin gives `N(K,0)={0}`, making the set empty, hence every boundary point has a unique tangent plane and the boundary is `C^1`. The duality stated immediately before that theorem (lines 110–114) gives strict convexity of the homogeneous support function on affine hyperplanes avoiding the origin. The proof on pp. 21–22 uses global support/normal-cone geometry and Caffarelli localization, providing exactly the ingredient that a bare determinant bound lacks. Part (iv) confirms `C^{2,α}` boundary regularity; the manuscript appropriately uses the support regularity proposition rather than silently identifying boundary and support smoothness.

Chou–Wang Proposition 1.2, published PDF p. 8/journal p. 40, applies to locally strictly convex support charts away from their zero set. Positive support makes the zero set empty and makes the weighted measure equation equivalent to the generalized equation in that paper. Its `C^{2,α}` and higher support regularity statements therefore apply to the smooth datum. I checked its sphere/ambient convention against `n-1` here. For `n=2`, the stated distributional equation `h''+h=fh^(p-1)` independently gives `C²`, then smoothness by iteration; its right side is continuous at the first step because `h` is positive and continuous. After support regularity, convexity gives `Q>=0` and the positive determinant makes every eigenvalue positive. Higher regularity or local elliptic bootstrapping gives `C∞`. No dimension-dependent density-only strict-convexity theorem is presumed in the final version.

### Normalizations and excluded endpoint

I checked `dS_p=h^(1-p)dS`, `dν=h dS/(nV)`, curvature determinant on the `(n-1)`-dimensional tangent space, dilation exponent `n-p`, and the p=0 relation `M=nV`. For each signed normal of a box the ordinary area mass is `V/(2a_i)`, the `S_0` mass is `V/2`, and the unnormalized cone-volume mass is `V/(2n)`. The equal-volume boxes with side parameters `(1,…,1)` and `(s,s^-1,1,…,1)` are distinct for `s!=1`, in every `n>=2`. They falsify the excluded general singular p=0 uniqueness, while their atomic data do not contradict the claimed smooth positive-data theorem.

## Pivotal upstream analytic dependencies

The exact input is OpenAI family091 at `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. I read the relevant pinned analytic source files and checked the all-body quantifiers. I did not treat a repository label or the comparator's unfinished declaration as evidence of proof.

The delicate moment construction uses smooth truncated densities on balls. [Berman–Berndtsson Theorem 1.1](https://numdam.org/item/10.5802/afst.1386.pdf), journal p. 651, has the required centered positive density and convex-target hypotheses; reflection/translation uniqueness gives an even potential. Klartag [v1 Proposition 3.1 and Remark 3.5](https://arxiv.org/abs/1309.2767v1) applies to each smooth ball target and gives the uniform `4/ε` Hessian cap. The target boundary and log-density conditions, and bounded derivatives for each fixed truncation, hold. The cap is independent of the truncation radius.

I checked the uniform coercivity argument, integration identity `E[z·∇φ]=n`, compact Hessian lower bounds from the determinant lower bound and global upper cap, and smooth convergence mechanism. Wang's published 2012 Corollary 2.3 is a real-`Sym(n)` uniformly elliptic concave regularity statement, not a theorem restricted to an even-dimensional complex setting. A concave spectral extension of log-determinant is uniformly elliptic on the local Hessian bounds. Schauder estimates are applied to already smooth truncation solutions; passing a priori estimates to the limit is legitimate. Finite supporting slopes plus the dense gradient image make every tilt coercive and the limit gradient map onto; domination supports the limit normalization and pushforward.

For density of the double-divergence range, local ellipticity and distribution regularity justify smoothing a weak annihilator. I checked the localized fourth-order identity and cutoff coefficients `4,-12,-8`, the absorption estimates, and the separation of the constant/linear obstruction. The graph approximation step uses the compact Hessian identity to avoid an unsupported global second-derivative approximation. Only local Hessian lower bounds are required.

In the tensor step I checked the row-adjoint identities and that the vector-field derivative in moment coordinates is symmetric. The Bochner contraction uses the matrix-square trace, not an unjustified replacement by a Hilbert–Schmidt norm. At a normalized point `τ=I`, with symmetric `S` and `J=hC` symmetric in its last two indices, the crucial remainder is

`2 ||S+Sym J||² + (1/6)||J-J^(12)||²`.

The contractions and coordinate invariance give a nonnegative remainder without assuming a positive Hessian for the test function. The homogeneity identity and Cauchy–Schwarz give the soft-variance inequality with the correct degree factor. The slab limit through even degrees, Gaussian domination, removal of the auxiliary quadratic term, approximation of slab directions, and Hausdorff approximation of symmetric bodies provide the nonsmooth all-body input used in the follow-on note. I found no material gap in this needed analytic chain. The finite exact tensor tests corroborate this general calculation; they cannot establish it on their own.

## Attribution and priority

The stated framing is justified as a checked consequence package. BLZY 2012 supplies the logarithmic and positive-p transfer machinery; Kolesnikov–Milman Proposition 11.1 supports the known mixed/identical-measure connection. He–Liu supplies the smooth endpoint mechanism. The BFR book's precise smooth and general positive-p targets are correctly identified as Conjectures 9.4.3 and 9.4.4. My book verification was of the relevant primary indexed excerpts, not a claimed line-by-line reading of the whole book.

I read the relevant full primary [Stancu 2018 report](https://ems.press/content/serial-article-files/46776), pp. 3262–3264/PDF pp. 45–47. It publicly announces smooth logarithmic uniqueness in Corollary 1 and an all-dimensional inequality in Theorem 2, with flow-asymptotic details deferred. The manuscript expressly acknowledges that announcement; it therefore does not claim first public announcement, a new implication, or a new base-inequality proof. The October 6 public repository release and the September 23 internal manuscript date are distinguished. The pinned commit's local metadata and the public repository identify October 6; a filename date is not public-priority evidence.

The full Stancu IMRN 2022 article (DOI `10.1093/imrn/rnaa103`, online June 3, 2020, volume 2022 issue 2 pp. 1016–1044) remained inaccessible to this review. I inspected the accessible primary metadata/abstract and searched the title/DOI for an accessible primary full text. An abstract about proportional centro-affine curvature cannot establish or refute the complete prior theorem/proof. This is an exact limitation of the priority investigation, not a missing premise in the current analytic proof. A search failure is not novelty evidence. The manuscript/metadata's conservative consequence language and the explicit audit caveat accommodate that limitation.

## Exact package, PDF and reproduction

I independently verified ZIP safety and correspondence: 32 unique regular entries, consisting of 31 payload files plus the internal manifest; no absolute or parent-traversal paths; exact file set, sizes, SHA-256 and MD5 values; fixed timestamps and regular-file `0644` permissions. At the exact-candidate checkpoint, the builder's read-only `--check` with the recorded review paths exactly reproduced the existing three upload bytes. The allowlist omits third-party PDFs and source copies, dependency clones, caches, secret/state files and previews. The formal-scope excerpt removes only the unrelated operational incident and retains the mathematical limitations with original provenance hash. The CC BY 4.0 assertion is explicitly for the owned contribution, not for the excluded external sources.

A closing live-workspace `--check` at 04:32 UTC detected that final assembly work had begun: `publication/build_package.py` alone differed from the reviewed ZIP (`0d970aede1b53c100ea3468e1675bb9d6a7fe2765ea809a9a6f17ddbc1ac4824` in the ZIP; `1a96993505f8f33206668178aeb4035023f510d6856bcc6124db3cf71dfd08c1` in the live workspace). I compared every manifest entry to identify that change. The exact source, PDF, metadata, README and ZIP above remained unchanged. This does not invalidate the fresh extracted-ZIP tests, but it means the old ZIP cannot be described as reproducible from the now-modified author workspace. The new builder and later final assembly are outside this exact-version verdict and must be checked in the announced final-package review.

The intended Zenodo metadata matches the theorem, title, author, ORCID `0009-0001-9320-500X`, preprint type, date, license and exactly three upload filenames. Its disclosures match the manuscript and README. The reviewed README does not infer an external publication or DOI from local success. External staging/publication and spreadsheet actions were not performed or verified in this review.

I rendered the exact exported PDF to five page images and visually inspected every page. The theorem, equation dimensions, p=0 calculation, repaired regularity paragraph, box boundary example, disclosure and all references are present and legible, with no visible clipping or collisions. PDF information reports five letter-size pages, the correct title/author, no JavaScript, no form and no encryption; fonts are embedded. I checked the exact final QA identification. Native preview success was not used as a substitute for examining the exported file.

From a fresh extraction of the exact latest ZIP, I actually ran

`python3 verification/reproduce.py --upstream /Users/alec/Desktop/math --compile --tex-engine /opt/homebrew/bin/tectonic`.

The saved independent output is `review_02_reproduction_final.json`. It passed all 31 payload hashes, 200 upstream tensor cases, 250 separately implemented tensor cases, 200 endpoint-identity cases, 7 box cases in ambient dimensions 2–8, 28 scaling cases, and read-only checks of 23 upstream inventory files against the pinned checkout. Python was 3.14.6 and Tectonic 0.16.9. Compilation from a fresh temporary directory exited zero and produced an actual 79099-byte PDF, SHA-256 `a654442010489037b4b5c3d378fd687c396cd3bedf4f6d33da5d45e4a1ebb3ae`. This is not the separately exported release PDF; differing PDF timestamps/tool output are expressly permitted and no byte-identical cross-environment PDF claim is made.

The revised reproduction instructions correctly distinguish what an extracted ZIP supports from full archive recreation. The public ZIP supports its tests, standalone TeX compilation and optional read-only upstream hash check. The builder also needs the full author workspace's original formal report, separately exported PDF and external package receipt; those are not all duplicated inside the ZIP. I found no remaining claim that the extracted ZIP alone reconstructs the entire upload kit.

## Remaining evidence limits

The actual upstream declaration is `OAI.LogBrunnMinkowski.main`, distinct from the intentionally unfinished comparator. Selected source semantics and the declaration match the required Wulff-volume statement. Independent kernel compilation, theorem-axiom extraction, Comparator reproduction and independent-kernel audit did not complete because dependency installation ran out of available storage. Lexical absence of local placeholders is not imported-axiom closure. The package correctly discloses this, and the follow-on theorem is not formalized. My mathematical verdict rests on the independently scrutinized analytic argument and explicit deductions, not on a claim that those formal checks passed.

Finite calculations do not replace the all-dimensional proof. Automated independent review does not constitute conventional human refereeing. The inaccessible 2022 full text limits priority certainty. The eventual final archive must be checked again after assembly. These are acknowledged limits of the evidence; I found no unresolved substantive concern in the exact repaired candidate reviewed here.
