# Independent source audit: problem 30005030

Audit date: 7 October 2026. Problem: OWR-9790360-001, “Spatial Regularity Versus Time Integrability for Fractional SDEs.”

## Disposition

**Accepted as a source-scoped negative prior-result, conditional on the cited preprint theorem.** The proposed dimension-uniform strong/pathwise-uniqueness criterion based solely on the scaling inequality is refuted by the cited theorem for ordinary, bounded spatially Hölder drifts. The elementary implication and the deterministic-drift/joint-compatibility reduction are valid. This is not a new counterexample construction, a complete independent proof of Hess-Childs–Rowan, or a resolution of every interpretation or special case of the original question.

Acceptance applies to these exact files **together**:

- REPORT.md, 7,763 bytes, SHA-256 `441611b3a286a813d2684af06a09886c754e67a9d53f425205cbf31750bc8738`.
- SCOPE_ADDENDUM.md, 4,348 bytes, SHA-256 `9137ab45499acf2b1899c16aa824b6e952ff6ce2cf54cfe8a434b1b7e6af9fc8`.

The addendum is required: it supplies the solution-class qualifier for the nearby positive result and addresses common-noise compatibility. No blocking mathematical gap was found in this combined, explicitly limited claim.

## Original target and quantifiers

The source was checked against the primary OWR PDF, including printed pages 469–471 and visual inspection of pages 470–471. Equation (2) is alpha > 1 - 1/(q' H), equivalently alpha > S(H,q) = 1 - 1/H + 1/(Hq). Theorem 1 concerns L²-time drifts above A(H) = 1 - 1/(2H), with strong existence, pathwise uniqueness and path-by-path uniqueness in arbitrary dimension. The final paragraph explicitly asks whether higher temporal integrability can lower that spatial threshold in agreement with equation (2). The isolated question A on page 470 omits the “1 -” present in the theorem and final question; the report correctly flags, rather than silently relies on, that discrepancy. [OWR]

The source allows general dimension and also discusses integrated fractional noise beyond ordinary H in (0,1). A counterexample for d=2 and H in (1/2,1) therefore defeats the universal criterion. It does not turn the open-ended word “can” into a claim that no improvement is possible under additional hypotheses.

## Invoked theorem and its status

The frozen HR PDF is arXiv:2604.23883v1, internally marked 26 April 2026 and dated 28 April 2026 on its title page. Corollary 1.11, page 5, applies for d=2, H in (1/2,1), and 0 <= alpha < A(H), with a sure spatial C^alpha bound of 2 at every time in [0,1]. For each fixed deterministic initial point, almost every drift realization gives stochastic pathwise nonuniqueness. The noise and drift randomness are independent. Definitions 1.1 and 1.14 give the ordinary integral equation and a nonanticipation condition. [HR]

The current arXiv record lists v1, and the author’s current research page lists this work under preprints. The experimental HTML displays 24 August 2026, while the version-specific PDF opened during this audit retains the April date. The frozen PDF is the authority for the cited theorem; the HTML date is not silently treated as a new version. Peer-reviewed publication has not been verified. [HR, Author]

## Deterministic selection and common filtration

Fix x0=0 first. The theorem’s full-measure set of drift realizations can depend on this point; choosing one member is sufficient. Neither a drift depending on the realized noise path nor a simultaneous assertion for all uncountably many initial points is needed.

The cited proof dependencies were checked: Theorem 2.5, Lemma 6.1, Lemma 6.2, its Appendix A nonanticipation identity, and the proof’s two-point limit with the drift already fixed. Those dependencies support the addendum’s reading. The full single-scale and multiscale probabilistic construction was not independently verified. [HR]

Independently, the addendum’s measure-theoretic argument is correct. If the law of a compatible weak solution disintegrates as K(W,dX)P_H(dW), then its past-projected kernel K_t depends only on W up to t, up to the usual completion. The conditional-product law

nu(dX1,dX2,dW) = K(W,dX1)K(W,dX2)P_H(dW)

has joint past kernel K_t tensor K_t. Products of bounded past test functions establish its past measurability, and a monotone-class argument extends this to all bounded joint-past functionals. Thus the pair retains nonanticipation with a common canonical filtration. This is stronger than merely verifying the two marginal solutions separately. In the usual filtered-fBm formulation, the resulting immersion of the natural noise filtration also preserves its Brownian innovation representation.

For each fixed epsilon>0, the cited non-Dirac property of K_epsilon implies that the diagonal mass of K_epsilon tensor K_epsilon is strictly below one. Indeed that mass is the sum of squared atom masses; it equals one only for a Dirac probability measure. Integration therefore gives positive probability that the two solutions differ before epsilon. This suffices for failure of pathwise uniqueness. It does not establish that no strong solution can exist.

## Threshold reduction and dimension extension

For H in (1/2,1) and q in (2,infinity], with 1/infinity=0,

A(H) - S(H,q) = (1/2 - 1/q)/H > 0, and 0 < A(H) < 1/2.

Let M=max(0,S(H,q)) and alpha=(M+A(H))/2. If S>=0, then S<alpha<A. If S<0, then 0<alpha=A/2<A and alpha>S. Thus all hypotheses of the invoked corollary are satisfied with strictly positive ordinary Hölder regularity. This also avoids every negative-regularity solution-definition issue.

On [0,1], a bounded time-dependent C^alpha norm gives L^q_t C^alpha_x membership for every finite q with norm no greater than the L^infinity norm; q=infinity is immediate. Consequently, for each H in this interval and each q>2, there is a deterministic drift satisfying the proposed scaling condition while pathwise uniqueness fails. Path-by-path uniqueness would imply equality of any such pair of Carathéodory solutions with the same forcing path, so that stronger property fails too.

The explicit values H=3/4, q=4, alpha=1/6 give S=0, A=1/3 and scaling exponent 1-H-1/q+H alpha=1/8>0. The report does not misrepresent this existence-based selection as an explicit formula for the selected deterministic drift.

For d>2, projection onto the first two coordinates is 1-Lipschitz. Therefore extending the drift by zero in the remaining components preserves its bounded Hölder norm. On an independent product probability space, append the same remaining fBm coordinates to both solutions. Their joint compatibility is preserved by independence; their first two coordinates still disagree with positive probability. This proves the asserted extension, without any spatial integrability assumption beyond the bounded Hölder norm.

## Nearby positive results and exclusions

The GG primary PDF’s assumption (A) restricts q to (1,2], with alpha>S and alpha<1. Using it at q=2 for a more time-integrable drift recovers the old threshold A, not S for q>2. Theorem 1.5 instead gives weak existence under alpha>max(1/2-1/(2H),S), H in (0,1); it does not give the missing uniqueness. [GG]

BM v2, Definitions 2.7–2.8 and Theorems 2.9 and 2.12, confirm the addendum. For autonomous b, H in (0,1/2], alpha>1/2-1/(2H), weak uniqueness is in V((1+H)/2), whose drift part has uniformly controlled L^m Hölder increments for every m>=2. In d=1, strong existence and pathwise uniqueness in that class additionally hold under the displayed product condition or for a nonnegative measure. At H=1/4 and alpha=-11/10, the product is 261/400>1/2, genuinely below A=-1 while above -3/2. These restricted positive results must not be omitted from a broad status summary. [BM]

GY v2’s Theorem 1.1 assumes an L^q_t L^p_x drift, H<1/2, p>=2, Hq>=1 and 1/q+Hd/p<1-H. It does not imply a result for arbitrary negative Hölder/Besov drifts: the relevant L^p-to-Besov embedding cannot be reversed. [GY]

No conclusion is accepted here for d=1 in general, the endpoint alpha=A(H), autonomous drifts in general, integrated H>1 noise, or all solution notions. HR’s H<1/2 explosive-separation statement is not upgraded to actual time-zero stochastic nonuniqueness. No weak-uniqueness or absence-of-all-strong-solutions conclusion is inferred for its non-Brownian examples.

## Provenance and executable checks

All six original public files remain byte-identical. The original verify.py and CHECK_RESULTS.json are retained as historical artifacts. The original checker silently skips missing PDFs and does not verify report/addendum pins, corpus files, or the additional web captures. Its PASS must not be advertised as complete provenance verification or a portable check of absent sources.

The separate audit_verify.py has two explicit modes:

- `python audit_verify.py`: checks all six frozen public-file pins, 6,960 exact rational parameter cases, the explicit negative witness and the BM arithmetic example. All eight external-input checks are explicitly marked skipped. Its success status is PASS_ARITHMETIC_AND_PAYLOAD_ONLY.
- `python audit_verify.py --mode source-backed --source-dir SOURCE_DIRECTORY --corpus-dir CORPUS_DIRECTORY`: additionally requires all three pinned PDFs, two historical web captures and three corpus files. A missing input gives exit code 2 and INCOMPLETE_REQUIRED_SOURCES. Any mismatched source gives exit code 1. A complete run checks corpus counts and the specified term-search gate, without outputting source or dataset contents.

Both modes were run. The source-backed run matched every supplied byte count and SHA-256, reproduced 15,458 problem records and 6,701 reports, and reproduced six matched problem records, four matched reports, and the absence of an exact report for this problem. The matched candidate lists were also separately compared with the historical screening and agreed; their subject matter does not answer this threshold question. This is a reproducible bounded search, not an exhaustive semantic or worldwide novelty guarantee.

AUDIT_PORTABLE_CHECK_RESULTS.json and AUDIT_SOURCE_CHECK_RESULTS.json record the two outcomes. Six checker regression tests passed: explicit portable skips, missing required sources, modified report, modified addendum, absent report, and a corrupt source fixture. The regression script and results are supplied separately.

Hash matches establish identity against the declared frozen inputs, not the authenticity of an unavailable retrieval log. The historical provenance addendum correctly clarifies that HR was originally downloaded from the unversioned PDF URL and identified internally as v1 after a version-specific retry timed out. During this audit, the version-specific public PDF opened successfully and its title date and theorem were checked. No fresh byte-for-byte network-download hash comparison is claimed. BM and GY were inspected in primary versioned HTML; they are not represented as local PDF-hash-verified sources.

## References

- [OWR] L. Galeati, “Some recent advances on SDEs with fractional noise,” OWR 9/2022, pp. 469–471. [Primary PDF](https://publications.mfo.de/bitstream/handle/mfo/3948/OWR_2022_09.pdf?isAllowed=y&sequence=4).
- [HR] E. Hess-Childs and K. Rowan, “Sharp pathwise nonuniqueness for additive SDEs,” arXiv:2604.23883v1. [Versioned PDF](https://arxiv.org/pdf/2604.23883v1), [version record](https://arxiv.org/abs/2604.23883v1).
- [Author] [Keefer Rowan’s research list](https://keeferrowan.github.io/), inspected 7 October 2026.
- [GG] L. Galeati and M. Gerencsér, “Solution theory of fractional SDEs in complete subcritical regimes,” Forum of Mathematics, Sigma 13 (2025), e12. [Published article](https://doi.org/10.1017/fms.2024.136).
- [BM] O. Butkovsky and L. Mytnik, “Weak uniqueness for singular stochastic equations,” arXiv:2405.13780v2. [Primary versioned text](https://arxiv.org/html/2405.13780v2).
- [GY] J. Gu and Q. Yu, “Strong solutions to SDEs with singular drifts driven by fractional Brownian motions,” arXiv:2602.04303v2. [Primary versioned text](https://arxiv.org/html/2602.04303v2).
