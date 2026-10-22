# Independent adversarial audit: OWR-15957-002 / 30003649

## Verdict: PASS

Audit date: 5 October 2026. The retained proof and independently recomputed finite certificate establish the negative answer to the general rational factorization question, with no restriction on finite factor width. The separate order-two integral question is affirmative by the credited prior theorem and by the complete descent argument in the freeze. No material mathematical gap or required revision was found.

The appropriate outcome is **verified prior resolution / already_solved**, with the qualifications below. This audit is an independent nonauthor AI review, not external human peer review, journal acceptance, or a new formal proof-assistant run. It asserts no novelty, minimum counterexample order, or classification of smaller orders.

## Frozen object and review independence

The audited archive contains 15 files, is 23,238 bytes, and has SHA-256 e07292e0950de7e75576263d9ed69ecbd2b70f0d2d02660521ded791f4c85e8d. Its manifest has SHA-256 a6ddcab54ebcc0111594758c4b1ba5db539599c793116b1858a29a7ab5db60b2. Every manifest entry and archive member was checked against the frozen work. The freeze was not modified.

The reviewer read the entire authored proof interface, reports, programs, and recorded metadata; the entire eleven-page Holden manuscript; the original Berman question and surrounding definitions; and the Laffey–Šmigoc preprint, including its proof. The OWR question page and the manuscript's local-PSD/triangle page were also inspected visually. An optimized replay of the frozen mathematical and integral checkers independently reproduced their stable outputs.

The new verifier imports neither the frozen verifier nor code from the source repository. It uses a different field representation, different root isolation, and a different complete facet algorithm. The previously reported source audit and Lean status are not premises of the proof. Prior repository-search coverage is a bounded provenance assertion in the freeze, not a mathematical dependency or novelty certificate; this audit does not enlarge that search claim.

## Exact target and source status

Berman's contribution to [Oberwolfach Report 52/2017](https://ems.press/content/serial-article-files/46715), printed page 3082, asks about rational factors in arbitrary order and integral factors specifically in order two. Both permit an arbitrary finite number of columns. Neither grants a scaling change or imposes nonsingularity. The report expressly distinguishes the already-known rational interior case.

The rational counterexample is credited to Sidney Holden's [13 September 2026 public manuscript](https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/412489c6c52f49653bf069ac2f85e92034cdbfa5/references/holden-pf03-2026-09-13/proof/PF03_counterexample.pdf). The inspected source identifies informal AI review; journal publication and external human peer review were not verified. Its original manuscript status must remain explicit in any public description.

The current [PF-03 source record](https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/main/nonnegative-and-positive-factorizations/PF-03/README.md), freshly read through GitHub, separately credits George Stepaniants's Lean formalization. Its stated theorem negates the same universal rational assertion, but its witness does not certify order 444, strict entry positivity, or minimal real cp-rank. This audit neither reran nor audited Lean and does not infer those explicit-witness properties from that status.

For the integral result, the [Laffey–Šmigoc primary preprint](https://arxiv.org/abs/1802.04129) states the stronger theorem for every integral doubly nonnegative matrix of order two and cites the original question. The authors' later [2019 journal article](https://doi.org/10.1515/spma-2019-0021), reference 13, confirms the 2018 publication in Pure and Applied Functional Analysis 3(4), 633–638. The publisher's original PDF route timed out in the web tool and returned HTTP 502 on direct retrieval; no successful retrieval of those journal PDF bytes is claimed. This does not affect inspection of the complete primary preprint or the independent proof.

Fresh direct downloads of all five pinned public witness files matched the freeze's sizes and SHA-256 hashes. Fresh downloads of the official OWR PDF and immutable Holden PDF also matched. Downloaded PDFs, extracts, witness contents, and private source-comparison scripts are excluded from this audit package.

## Mathematical dependency audit

### 1. Arithmetic and irrational directions

The field is the real embedding of Q[t]/(t³−2). Irreducibility is supplied by Eisenstein, not a numerical root test. Coefficients in the rational basis 1, α, α² therefore compare exactly. A rational vector on the line through a column of O would force the three rational coefficient columns to have rank at most one: the real proportionality scalar belongs to the cubic field after dividing a nonzero coordinate. Each coefficient matrix has verified rank three. This excludes rational vectors on the entire line, not merely rational unit vectors or a chosen normalization.

Orthogonality, symmetry, trace zero, the Cayley identity, all seven local kernel identities, and the local positive minors were checked independently. Positive definiteness of the leading 2-by-2 block and a kernel vector with nonzero last coordinate give the full local positive-semidefinite rank-two restriction by completing the square. Checking two minors alone, without the kernel identity, would be insufficient; both are present.

Additional source-definition checks confirm the two displayed integer seed matrices, all seven fixed entries, all fourteen defining linear equations, and rank fourteen of their determined-variable system. These construction checks are supplementary. The obstruction itself depends on the verified actual matrices, not a claim that a numerical search generated them.

### 2. The global zero set

The positive barycentric coordinates place every orthogonal column in its corresponding rational three-generator cone. The first coordinate of the coefficient triangle is one, so the local zero line contributes only its positive ray. The common rational functional is strictly positive on every generator; it excludes cancellation to zero and proves pointedness. The contained orthonormal basis proves full dimension.

All 189 cross-block bilinear pairings are strictly positive. Thus any decomposition using nonzero vectors from two distinct blocks has a strictly positive quadratic value, since the local quadratic values are nonnegative. A zero of the form in the total cone must lie on a single distinguished positive ray. By the preceding irrational-line argument, the only rational zero is the origin. No uniqueness of the conic decomposition is required.

### 3. Exhaustive halfspaces, rather than a partial outer approximation

Every facet of the seven-dimensional generated cone contains six independent input generators. Enumeration of every six-subset therefore finds every supporting facet normal. The independent routine computes all relevant six-by-six minors by shared Laplace expansions and obtains signed cofactor normals; it does not call the frozen nullspace/Bareiss routine. Nonzero minors establish independence. Integer dot products establish support, orientation, and incidence.

Exactly 54,264 candidates were checked, none rank deficient; 53,820 were non-supporting and 444 yielded the complete facet list. The rows and incidences agree exactly with the pinned witness and CSV. Standard finite-polyhedral duality then gives equality between the generated cone and the intersection of these halfspaces. This equality is indispensable: merely verifying that the known generators satisfy some inequalities would not restrict all hypothetical factor columns to the required cone.

### 4. All finite factor widths

Let A=RRᵀ and suppose a rational nonnegative C of any finite width satisfied CCᵀ=A. For each y in ker(Rᵀ), the identity yᵀAy=∑(yᵀc_j)² forces every column c_j into range(R). Rank seven provides a rational left inverse L. Therefore X=LC is rational, RX=C≥0, and XXᵀ=I.

The complete halfspace description places every column x_j in the generated cone. Trace zero gives ∑x_jᵀQx_j=0. Every summand is nonnegative, so every column is a rational zero and must vanish, contradicting XXᵀ=I. The number of columns is never bounded. The form Q need only be real symmetric; no unjustified rationality assumption on the exposing form is used.

The real factor RO is nonnegative, and orthogonality gives its Gram matrix A. Independent exact checks find 2,966 positive factor entries and 142 zeros, and verify every one of the 98,790 stored integer Gram entries as strictly positive. Rank seven proves real cp-rank at least seven, and the seven-column factor proves equality. Singularity at order 444 proves boundary membership in the full symmetric-matrix space. Entrywise positivity does not invalidate that argument.

### 5. Integral order two, weights, and scaling

The frozen descent has a valid all-input induction parameter: nonnegative integral trace. A diagonally dominant matrix is a sum of integral nonnegative elementary outer products with integral multiplicities. Otherwise a positive diagonal a<b can be used in an integral nonnegative congruence whose transformed off-diagonal is b−a and other diagonal is c+a−2b. Positive semidefiniteness gives c+a−2b≥(b−a)²/a>0, and the trace strictly decreases. The other case follows by coordinate interchange. Congruence and multiplication by the integral nonnegative transformation preserve the required factor type. Zero and rank-one cases are included. Thus this is a proof for all inputs, not an extrapolation from a test box.

A nonblocking typographical issue was verified visually in the 2018 primary preprint, page 5: equation (5) prints a subtraction inside the square, whereas the preceding factor vector and the expansion in equation (6) require addition. Replacing that sign restores the displayed algebra immediately. The frozen self-contained trace descent does not invoke that line, so this source typo creates no gap in the audited proof.

The known order-three example in the freeze has the stated rational factor. Its all-width integral impossibility follows from squared length two in the first row, then the forced two nonzero entries of the second row, and the incompatible third-row inner product. The finite enumeration of possible row-two pairs is exhaustive because the first-row support has exactly two entries; there is no hidden width bound.

A positive rational p/q is a sum of pq copies of (1/q)². Hence rational nonnegative weights can be absorbed by increasing width. This proves invariance of rational factorability under positive rational scaling. Clearing denominators gives equivalence with an integral factor for some square multiple, but does not give an integral factor for the unscaled matrix. The scalar [2] control correctly distinguishes unrestricted width from minimal real cp-rank. None of these steps uses irrational square roots as rational columns.

## Computational results and adversarial checks

- Independent field arithmetic uses one common positive denominator and explicit cubic multiplication. Sign decisions use a separately generated 192-step rational bisection interval and full Horner interval multiplication.
- All seven local restrictions, 189 strict cross-pairings, complete facets, factor signs, and all Gram entries passed. Full-rank tests use a nonzero modular specialization as a one-way witness for characteristic-zero nonvanishing; no vanishing-modulo-prime conclusion is used.
- 2,000 multiplication comparisons against independent polynomial convolution and 24 cofactor comparisons against permutation determinants passed, including dependent-row cases.
- Eleven deliberate corruptions were rejected, including a consistent negation preserving trace and local kernels, omission of a facet, reversed facet orientation, altered Gram value, duplicate coordinate, and hash mismatch. Mathematical negative tests run separately from hash rejection.
- The quotient-step integral verifier passed all 234,905 positive-semidefinite triples with entries from 0 through 80, 5,000 large generated inputs, twenty additional degenerate/rank-one inputs, and four invalid-input controls. This corroborates the proof, without being its basis.
- The frozen verifier and its controls were replayed with optimization. The new verifier was also replayed under -OO from another working directory. Explicit exceptions, not removable assertions, guard mathematical checks.

One nonblocking hardening observation: the frozen checker reports hashes and its README asks the operator to validate them. The new audit checker makes those same immutable hash pins a mandatory entry gate. The actual frozen replay used matching pinned bytes; there is no proof gap arising from this interface difference.

## Publication boundary and conclusion

PASS applies to the exact frozen package and the quantified prior-resolution claims audited above. It does not convert the Holden manuscript into a peer-reviewed publication, certify the separate Lean project, or authorize distribution of source datasets. Keep the manuscript-status distinction, historical attribution, all-width qualification, and order-two scope in any public summary.

The audit directory contains only independently authored code/report material and allowed public verification metadata. No remote write, commit, push, or PR operation was performed. The authored freeze remains unchanged.
