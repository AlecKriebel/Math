# Independent audit: Function Theory Problem 3.30

## Decision

Accept the unchanged author packet as a literature-based resolution of the exact smooth-Jordan-curve problem. The appropriate classification is `already_solved`, equivalent here to the author's `LITERATURE_RESOLVED`. Finite rank occurs precisely for circles; the rank is one over the scalar field of the density space. No mathematical correction patch is required.

The accepted result depends on the classical planar finite-rank rigidity theorem. This audit verifies the cited statements and independently checks the operator, regularity, and function-space reduction. It does not reproduce or independently certify the classical theorem's original proof, assert historical priority, or claim a new rigidity theorem.

## 1. Immutable object and complete problem identity

The reviewed author archive is `FUNCTION_THEORY_2303030_AUTHOR_SAFE_FREEZE.zip`, 8,729 bytes, SHA-256 `cbaa2568baecdd3466a78007d186aae0b23fc35a859cd6273656ebc19cd9070f`. Its six exact members and every internal/external manifest binding were independently checked. All six members were read. The separate author validation receipt was inspected as historical evidence, not adopted in place of new tests.

The selected catalog entry uniquely identifies problem 2303030, AMR-022-3030, rank 854. The complete selected problem object and complete inherited research-result object were read, including all background/status fields; the latter did not contain a proof or counterexample. The inherited open-status inference is not evidence against an explicit earlier theorem. No corpus contents or private coordination records are reproduced here.

The review hash was independently recomputed on the two complete objects in the order `[problem, inherited_result]`, using `json.dumps(..., sort_keys=True)` with all other Python JSON defaults, then UTF-8 encoding. It is `92121b21d4c4a8be8f33021ac02a86ede5f32b0213e0c09338885f89e28a37e4`. Sorting keys is essential: completely default serialization without `sort_keys=True` gives a different hash. The statement-only SHA-256 is `83ab90febdc719e13a811b0cf14d6dd03af505400c299bbab910ab0f3d379060`. See CORPUS_VERIFICATION.json for byte counts and match results.

## 2. Original scope, not a restricted substitute

The independently inspected [Hayman-Lingham source, Problem 3.30, printed p.69 / PDF p.70](https://arxiv.org/pdf/1809.07200v2#page=70) concerns a smooth Jordan curve in the plane and the double-layer boundary operator on continuous densities. The normal and arclength integration are at the first kernel argument, which is the source/integration point. The question is whether a noncircular example can have finite-dimensional range. Its update describes a lack of reports received by the compilers, not a theorem establishing continuing openness.

A Jordan curve is simple and closed. Its bounded interior is simply connected, and the curve is its single boundary component. The audit therefore does not replace an arbitrary multiply connected domain by a simply connected one: that restriction is already forced by the original curve hypothesis. No analytic-boundary hypothesis is present or needed. Here smooth has its usual differential-geometric meaning of a regular smooth embedded curve; in particular it is C-infinity, hence C^{2,alpha} for, say, alpha=1/2 on the compact boundary. The conclusion is not extended to a reinterpretation of smooth as merely C^1 or to rough/self-intersecting curves.

Rank means algebraic dimension of the operator's range. It is not the number of distinct eigenvalues, the count of nonzero eigenvalues without multiplicity, or numerical rank of a discretization. No numerical experiment or spectral-equivalence shortcut is used.

## 3. Decisive prior theorem and attribution

The following source checks were made against freshly retrieved PDFs, with the decisive pages visually inspected. All four fresh files matched the author's recorded byte counts and hashes.

- [Miyanishi, arXiv:1806.03657v1, Corollary 5.1, p.11](https://arxiv.org/pdf/1806.03657v1#page=11), gives the finite-rank implication for bounded C^{2,alpha} regions, alpha>0, in dimensions two or three: only a planar circular boundary can occur. Its preceding discussion identifies the planar ingredient as already known. This is a direct finite-rank statement with sufficient regularity scope, not an inference from the paper's three-dimensional asymptotic formula. The [arXiv record](https://arxiv.org/abs/1806.03657v1) dates v1 to 10 June 2018.
- [Miyanishi-Suzuki, arXiv:1501.03627v1, p.6](https://arxiv.org/pdf/1501.03627v1#page=6), explicitly records the general finite-rank planar characterization after Corollary 2.8. The nearby singular-value/rank-one criterion by itself would not suffice. Pages 1 and 3 define the operator on L² of a bounded C² boundary, page 4 discusses diagonal continuity, and reference [S] on page 19 identifies Shapiro's book. The [arXiv submission record](https://arxiv.org/abs/1501.03627v1) gives 15 January 2015 and labels the work preliminary. The served PDF's title page also displays 22 September 2021; this audit records that discrepancy without guessing its production history. It uses the explicit arXiv version and pinned bytes, not an inferred PDF creation date, to identify the inspected object.
- [Khavinson-Putinar-Shapiro, author manuscript, §8.2, p.75](https://web.math.ucsb.edu/~mputinar/poincare.pdf#page=75), independently records the disk-only finite-rank planar result and cites [39]. That reference, inspected on p.88, identifies the 1992 Shapiro monograph. These are manuscript page numbers, not journal page numbers. The [journal DOI](https://doi.org/10.1007/s00205-006-0045-1) is bibliographic context; this audit's source inspection was of the author manuscript.
- The [publisher's book listing](https://www.wiley-vch.de/en/areas-interest/mathematics-statistics/the-schwarz-function-and-its-generalization-to-higher-dimensions-978-0-471-57127-8) corroborates Harold S. Shapiro's title and 1992 publication. Neither that listing nor the two bibliographies constitutes inspection of the book proof. The original book proof remains uninspected.

These sources support classification as previously resolved within the exact scope. The audit does not infer that the cited papers supply mutually independent proofs; they point to the same classical dependency. Nor does it establish the first date at which every part of the result was proved.

## 4. Independent operator and normalization check

Let y be the source and x the target, let n(y) be the outward unit normal, and put nu(y)=-n(y). Under the signed double-layer convention in the original question, its kernel is

    k(y,x) = nu(y) dot (x-y) / |x-y|²
           = n(y) dot (y-x) / |x-y|².

This signed convention follows the stated double-layer operator; replacing the angle by an unsigned acute angle would define a different kernel. With T f(x)=integral k(y,x) f(y) ds_y, differentiation at the source yields

    partial_{n(y)} log(1/|x-y|)
      = - n(y) dot (y-x) / |x-y|²
      = -k(y,x).

The explicit planar Miyanishi-Suzuki operator therefore satisfies K_MS=-T/pi. Both the derivative and normal are at y. There is no unnoticed adjoint, transpose, target-normal substitution, or boundary jump term. Multiplication by the nonzero scalar -1/pi leaves rank unchanged. This check also predicts K_MS 1=-1 on a circle, agreeing with the source normalization.

The modern corollary uses the standard Neumann-Poincare boundary operator; it is not necessary to extrapolate its displayed three-dimensional kernel into dimension two. The planar operator is explicitly specified in Miyanishi-Suzuki, whose p.6 finite-rank statement and the corollary express the same classical characterization.

A translation and positive dilation of the curve scale k by the reciprocal dilation and ds by the dilation. Pullback consequently conjugates the integral operators. Thus the circular conclusion includes arbitrary centers and positive radii. A literal restriction to the unit circle at the origin would contradict this elementary invariance and is not the geometric meaning of the cited S¹ notation.

## 5. Removable diagonal and bounded mapping property

Choose a local arclength parametrization gamma, so |gamma'|=1 and nu(gamma(s)) dot gamma'(s)=0. Compact C² regularity gives the uniform expansion

    gamma(s+h)-gamma(s)
      = h gamma'(s) + (h²/2) gamma''(s) + o(h²).

The numerator defining k is therefore (h²/2) nu(gamma(s)) dot gamma''(s)+o(h²), while the denominator is h²+o(h²). The limit is

    k(gamma(s),gamma(s)) = (1/2) nu(gamma(s)) dot gamma''(s).

It varies continuously in s. Uniform remainders on compact coordinate neighborhoods establish joint continuity at the diagonal; off-diagonal continuity is immediate. Simplicity of the compact curve ensures the diagonal has no other geometric self-intersections. The extension is thus a continuous kernel on Gamma x Gamma. Assigning its diagonal value does not change any of the integrals, since each diagonal section is an arclength-null singleton. No principal value or singular boundary trace needs to be added.

For finite arclength measure and this continuous kernel, define

    M = sup_x ||k(.,x)||_{L²} < infinity.

Cauchy-Schwarz gives ||T_2 f||_infinity <= M ||f||_2. Moreover x -> k(.,x) is continuous in L² (indeed uniformly pointwise on the compact product), so T_2 f has a continuous representative. This independently verifies the smoothing property used in the author's range argument.

## 6. Finite-rank transfer and scalar fields

Let T_C and T_2 denote the continuous-density and L²-density operators over the same scalar field. Continuous functions are dense in L² on the compact smooth curve with arclength measure. If F=T_C(C(Gamma)) is finite dimensional, then F is closed in the uniform norm. For f in L², choose f_j in C with f_j -> f in L². The preceding estimate yields T_C f_j -> T_2 f uniformly, hence T_2 f belongs to F. The reverse inclusion is immediate from C being a subspace of L². Thus the two finite-dimensional ranges coincide as continuous functions.

Conversely, finite rank of T_2 implies finite rank after restriction to C. Applying the same argument then gives equality of the finite ranks. The embedding C -> L² is injective: a nonzero continuous function is bounded away from zero on some nonempty open arc, and that arc has positive arclength. Passing to almost-everywhere equivalence classes loses no dimension.

The kernel is real. If the question is read with real-valued densities, its complex-linear extension is the complexification: T_C(u+iv)=T_R u+i T_R v. A real basis of the real range remains complex-linearly independent, and spans the complex range. Hence finite real rank and finite complex rank are equivalent, with equal numerical ranks on the respective real-valued and complex-valued density spaces. If instead the whole complex-valued space is merely regarded as a real vector space, its finite rank doubles; this does not change the finite-versus-infinite classification. The usual rank-one assertion for C(Gamma) is over C, and it is also rank one on C(Gamma;R) over R.

It follows that the exact operator in Problem 3.30 has finite rank if and only if the planar classical operator does. The cited rigidity theorem applies without a spectral or scalar-field gap.

## 7. Circle converse checked directly

Write y=c+Ru and x=c+Rv with |u|=|v|=1 and R>0. For distinct u,v,

    nu(y) dot (x-y) = R(1-u dot v),
    |x-y|² = 2R²(1-u dot v).

Therefore k=1/(2R), including the diagonal by continuity. The output is the constant function

    T f = (1/(2R)) integral_Gamma f ds,

and T 1=pi. The range is precisely the one-dimensional constant subspace. This checks the converse, nonzeroness, and the rank normalization independently of the literature.

## 8. Validation, privacy boundary, and limits

The independent external validator reads the ZIP as data without extracting or executing any member. It enforces exact allowlists, duplicate rejection, safe flat paths, regular non-executable files, UTF-8 text, strict JSON parsing, size limits, and internal/external hash and byte-count bindings. The unchanged author archive passed four runs: isolated normal Python, isolated optimized Python, and both modes after relocation to unrelated paths with hostile current-directory/script-directory imports and environment variables. Each run rejected 21 hostile controls. A deliberately fully rebound harmless edit was accepted as a positive control, emphasizing that consistent hashes certify identity and structure, not truth.

The hostile import fixture was first shown to fire without isolation; under -I -S it did not fire. The validator uses explicit exceptions rather than assertions, and caller-supplied paths rather than repository-root discovery. Payload import/cache/entrypoint tests are inapplicable because the packet contains no executable payload. See VALIDATION_RESULTS.json for actual run details and validator identity.

The audit bundle contains only authored Markdown/JSON and public verification metadata. Source PDFs, screenshots, source extracts, raw corpus records, and private coordination files are excluded. Fresh retrieval and source hashes identify the examined bytes but do not replace mathematical review. The unchanged author archive remains separately pinned; this audit does not rewrite its historical pending-audit statements.

There is no formal proof-assistant certificate, claim of human peer review, proof of the original book theorem, exhaustive literature search, or novel theorem claim. This is one literature-verification approach. No repository write, publication, merge, release, or external submission was performed by this audit.
