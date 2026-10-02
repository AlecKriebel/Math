# Independent full-packet review: 30006211

**Verdict: PASS for the exact negative answer, credited prior resolution, and all four scoped preceding partials. No mandatory mathematical correction. Recommended campaign disposition: already_solved, 5/5 author turns consumed. No new discovery or priority claim.**

Review date: 2 October 2026. This is an independent mathematical/source audit of the complete frozen packet, not a sixth author search. The author files were not edited.

## Frozen scope

- Author branch: `math/30006211-multi-affine-wip`.
- Author head: `5c49f126ae66b03b814a3d3c6c51fe01715e70ec`.
- Final author manifest SHA-256: `a73236a49ebd73fe95a12c503dcfa879f333f83f9e63ff61c4ad4a1675bd23e5`.
- Final turn proof SHA-256: `10a3c9b1e23f2e2cf094f04899d8a7fb2e58d4a449bbd99681d5d4a42f7933a8`.
- Reviewed all five complete TURN files, SOURCE_GATE, final result/request, late-prior reconciliation/evidence, all five checker programs and receipts, and all five historical manifests.
- All 26 final-manifest entries and the manifest itself match locally. All 20 historical manifest entries and four predecessor-manifest links verify. Independently read all 28 remote files (the final 27 plus preserved PRIOR_GATE), matching raw contents and Git blob IDs exactly.

## Exact question and source

The complete Basu contribution, joint with Perrucci, at OWR 9/2025 printed 445–446 asks about the common zero set in all real affine space of two polynomials separately of degree at most one in every variable. The degree parameter is total degree. I visually checked printed 446 and read its preceding context. There is no regularity, transversality, compactness, symmetry or bounded-box qualification. The neighboring problem on sums of squares is separate.

Primary PDF: https://ems.press/content/serial-article-files/51353 . A fresh download matches the author's source hash. The publisher page https://ems.press/journals/owr/articles/14299088 dates the report's publication to 29 August 2025; the workshop/report designation is OWR 9/2025. These are compatible dates.

Basu–Perrucci, https://arxiv.org/abs/2204.01595 (published 2023, DOI https://doi.org/10.1016/j.aim.2023.108982 ), Theorem 2 and Examples 2.1–2.2 were checked in the local complete primary manuscript. Their one-equation bound, sharp monomial-minus-one example, and three-equation obstruction remain credited dependencies/context.

## Final negative construction and prior comparison

For m≥2 put f_i=x_i y_i−1 on disjoint pairs, F=Σf_i and H=Σ_(i<j)f_i f_j. Degrees are exactly2 and4, and each variable occurs to degree at most one. The identity F²−2H=Σf_i² proves the real common zero set is exactly the product of m hyperbolas. Each of its 2^m sign classes is homeomorphic to (0,∞)^m, is nonempty, and is relatively open and closed. Consequently those classes are exactly the connected components, for every m, not merely checked dimensions. The optional equal-degree pair H,H+F has the same zero set and degrees4,4.

The smoothness of the real product does not make the two equations transverse: on the product, the H gradient vanishes. This does not violate the actual source. The result settles the source's existence-of-a-degree-only-bound question negatively, while not settling the additional degree≤2 or degree≤3 questions in full generality.

I read the complete retrieved Ferudun preprint, *A Negative Answer to a Question of Basu and Perrucci on Two Multi-Affine Polynomials*, dated 30 September 2026. Its Theorem 1.2 and centered Lemma 3.1 were independently verified, including all degree statements, exact sum-of-squares identities, both zero-set implications, and sign-component topology. His pair P=x0−T, Q=x0T−2E−2T+m satisfies Q=TP+Σ(x_i y_i−1)². The centered lemma has P=x0−F and Q=x0F−2H and forces x0=0. Specializing x0=0 yields exactly the campaign pair up to nonzero scalar factors. Thus removing one auxiliary coordinate is a direct consequence of the prior mechanism and cannot support a new-solution credit.

Primary author page: https://eulersolve.org/papers/owr-14299088-013/ . This review's direct fresh PDF request there returned HTTP 403, and the web indexer could not open the page; the full shared source PDF was nevertheless available, read and hash-checked. Independently retrieved current Zenodo metadata, https://zenodo.org/records/23049180 , corroborates a repository creation timestamp of 30 September 2026 00:18:42.926131 UTC and publication date 30 September 2026. Its PDF byte count/checksum matches the frozen source; a fresh download of the repository PDF also matches its SHA-256 byte-for-byte. Further exact retrieval details are in PRIOR_ARCHIVE_RECONCILIATION.json. This additive evidence strengthens the historical author addendum's then-unverified archive chronology without altering that frozen addendum. Neither the date nor the DOI implies peer review or certifies first priority. The negative conclusion is accepted from its proof, not the website's status label.

## Turn 1: signed affine section

PASS. The full-support tangent argument is valid even for odd highest degree. On the hyperplane, the leading homogeneous part is nonnegative by positive-ray limits. At a point supported on d−1 active coordinates summing to zero it vanishes; differentiating along the specified tangent isolates exactly one degree-d coefficient. The nonzero product factor proves that coefficient vanishes, contradicting degree≥3.

For inactive variables, global one-sidedness of each affine coordinate restriction forces independence on the hyperplane. Divisibility by its nonconstant affine equation is valid, and the degree-in-an-active-variable argument forces the quotient to depend only on inactive variables. Its zero set is an affine subspace or empty by positive-semidefinite quadratic completion. The proof correctly allows zero-dimensional active hyperplanes, zero restriction, and unbounded degree in the off-hyperplane multiple. The sign-free two-component control is correctly limited in scope.

## Turn 2: disjoint product blocks

PASS. The balanced sections are continuous at zero, including block size1. Nonzero-product fiber branches are path connected; zero-product fibers attach through the origin. For an affine base, every coordinate not fixed nonzero hits zero, allowing exactly that block's sign labels to connect. Fixed-nonzero blocks retain sign invariants on every connected subset. This proves the exact formula, rather than inferring connected total space from connected fibers.

The row-space argument proves the number of fixed coordinates is at most the matrix rank. Independence of their columns gives a nonzero minor and therefore a matching into distinct equation rows. Disjoint supports prevent the corresponding leading monomial from cancelling, validating the finer sum-of-row-degrees exponent. Zero/constant/inconsistent rows and unused coordinates are handled.

## Turn 3: regular square pencils

PASS. An invertible pencil combination with a nonzero level can be chosen because an open nonempty set in coefficient space is not contained in the annihilating line. The normalization preserves the real set. For rank≥2, compatible rank-one fibers over nonzero kernel vectors attach via a direction whose image is not parallel to that vector; the local two-row section is well defined and gives actual solution paths on both nearby sides. Within each eigen-hyperplane chamber, finite codimension≥2 linear subspaces do not disconnect the base, by the generic two-segment construction. Kernel attachment creates no extra components or bridges across forbidden hyperplanes.

The scalar cases and both rank-one normal forms are checked separately. In particular, a rank-one nilpotent 2×2 example genuinely has four total-space components despite connected base and fibers; this exception is not incorrectly covered by the rank≥2 attachment argument. The rank-one nilpotent branches intersect nontrivially from dimension 3 onward, giving the stated connectedness. Sharpness examples and the stronger bound of two for m≥3 are correct.

## Turn 4: all rectangular bilinear pairs

PASS. I read and visually checked Iwata–Takamatsu Theorem 2.1, printed 2137, in the freshly retrieved primary PDF https://www.opt.mist.i.u-tokyo.ac.jp/~iwata/papers/KCF.pdf . Its strict equivalence uses constant invertible matrices over an arbitrary field; taking the real field is valid. The additional complex Jordan statement is not being substituted. Collecting all square blocks gives the regular part; zero-index singular blocks are unused variables.

For a positive singular block the two shifted short-vector rows are independent whenever the short vector is nonzero, giving a global Gram section for any residual levels and all other variables. At short-vector zero, first moving the free long variable to zero and then moving the short vector supplies a valid zero-contribution attachment. This joins both signs when its dimension is one and a zero stratum exists. The transpose argument and zero-size regular case are complete. The resulting four-component bound applies to arbitrary bilinear pairs, not arbitrary quadratic multi-affine pairs with no bipartition or simultaneous translation.

## Reproducibility and limits

All five author outputs replay byte-for-byte: 7,447+3,108+1,879+4,421+4,216=21,071 exact assertions. The independent checker imports no author code and passes 28,060 exact integer/rational assertions, including 234 independently solved linear systems, 150 rational rank-drop sections, 1,086 singular-block vectors, full sparse campaign/prior identities through m=20, exact specialization to the campaign pair, and all sign classes through m=9. SymPy 1.14.0 is used for independent rational linear algebra; no downloaded programs are executed.

Finite controls check the implementation and concrete algebra. General nonnegativity, connectedness, topology, and the all-m counterexample are justified by the reviewed arguments above. Earlier unresolved checkpoint labels are historically correct at those turns and remain frozen; the current wrapper should supersede them with already_solved 5/5 and explicit Ferudun/Basu–Perrucci credit. No raw source PDF, source image, import or private coordination is included in this portable review packet.
