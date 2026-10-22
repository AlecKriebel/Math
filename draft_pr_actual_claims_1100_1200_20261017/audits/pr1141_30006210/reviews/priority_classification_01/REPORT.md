# PR 1141: independent adversarial priority classification

## Disposition

**Exact-target prior-resolution evidence: not established.** The inspected prior primary sources do not record the complete inverse-polynomial relative-influence theorem, nor a recorded fully instantiated equivalent deduction covering all of its hypotheses. This is a bounded literature finding, not a certificate of novelty or firstness.

**Mathematical relationship: a short source-dependent corollary/application.** The full exact target follows from Li–Li–Li–Liu's prior arbitrary-real disjoint-support separator and the original OSSS covariance inequality, after the square-weight application detailed below. Calling the separator, the covariance inequality, or the elementary square estimate a new general theorem would overstate the contribution. A new recording of a target-specific corollary is distinct from a new foundational theorem.

Under the requested distinction between an earlier **recorded exact resolution** and generic earlier ingredients plus a present target-specific application, these sources do not justify `already_solved`. They also do not justify `novel`, `first`, or an assertion that this problem remained unresolved everywhere until the PR. If project eligibility requires novelty, that gate is not certified by this review. If it requires a valid exact solution with source credit and no affirmative novelty claim, the priority findings here do not refute that description.

**Attribution correction:** the submitted proof should cite O'Donnell–Saks–Schramm–Servedio, arXiv:cs/0508071v1, Section 3.3, Equation (6), for its Lemma 3. The present PROOF.md proves that special case and disclaims priority, but omits this relevant original source. This is an attribution finding, not a discovered defect in the mathematical implication.

## Exact claim audited

Let d,n be positive integers and f,g nonzero real multilinear polynomials of degree at most d on the uniform {-1,1}^n cube. For every coordinate,

    rho_i(f) = sum_{S containing i} f_hat(S)^2 / sum_{all S} f_hat(S)^2.

The denominator includes the constant Fourier coefficient. The target is that some constants c,C>0, independent of n,d,f,g, make rho_i(f),rho_i(g)<=c*d^(-C) sufficient for a vertex where f*g is nonzero. The submitted constants are c=1/4096, C=8. Its contrapositive is the stronger maximum-influence lower bound 1/(1024*d^8) under disjointness.

Nonzero constant polynomials cause no difficulty; degree-zero pairs overlap immediately. Degree at most d includes n<d. The common zero set may be arbitrarily large. Signed real coefficients and unrestricted nonzero amplitudes are allowed. Scaling either polynomial preserves the relative influence. Bounds for variance-normalized influences, uniformly bounded polynomials alone, Boolean range alone, nonnegative inputs alone, or supports covering the entire cube would leave a gap.

Austrin's [OWR 9/2025 p.445](https://ems.press/content/serial-article-files/51353) is the exact target source. Its exponential sufficient scale does not imply a uniform inverse-polynomial sufficient scale: 2^d/d^(C-1) tends to infinity for every fixed C. Its inverse-quadratic obstruction is a necessary restriction, not a sufficient inverse-polynomial theorem. The degree-one pair 1+x and 1-x has relative influence 1/2 and disjoint supports; it also explains the strict endpoint caveat in the submitted note.

## Strongest prior sources and exact gaps

| Prior primary source | What is recorded | Relation to exact target |
| --- | --- | --- |
| [OSSS, arXiv:cs/0508071v1](https://arxiv.org/abs/cs/0508071v1), Section 3.3 Eq.(6) | A decision-tree covariance bound with a bounded first function and arbitrary real second function, using L1 resampling influence | Already contains the submitted Lemma 3 after an affine rescaling and sign reversal; contains no polynomial-support separator or degree-to-relative-influence compatibility conclusion |
| [Lee, Theory of Computing 6 (2010)](https://theoryofcomputing.org/articles/v006a004/), Theorem 1.2 | Boolean/Boolean covariance inequality and an inductive proof | Corroborates classical provenance, but its displayed range hypotheses alone do not cover unbounded square weights; the stronger original OSSS source does |
| [Austrin et al., CRYPTO 2022](https://crypto.iacr.org/2022/papers/538804_1_En_6_Chapter_OnlinePDF.pdf), Conjectures 1.2/5.5, Theorem 4.4, Section 5.2 | Distribution-average polynomial compatibility is conjectured; an exponential threshold is proved | Point masses on normalized f,g include the exact target as a special case of the conjecture. An unproved conjecture and the exponential theorem are not an earlier proof of the target |
| [Kovacs-Deak–Wang–Yang, arXiv:2601.08727v1](https://arxiv.org/abs/2601.08727v1); [Kothari et al., v3](https://arxiv.org/abs/2601.08727v3) | Rational/nondeterministic degree bounds, decision trees for total Boolean functions, and a Hypercube Nullstellensatz with no common zeros | The total-function statements need complementary support coverage. The arbitrary-hole target does not satisfy that assumption automatically. Their Markov/symmetrization input is older material to credit, not the target resolution |
| [Li–Li–Li–Liu, arXiv:2608.03824v1](https://arxiv.org/abs/2608.03824v1), Lemma 3.5 | Depth O(d^4) separator for arbitrary real disjoint-support degree-d pairs under the nonzero-union promise | Its proof labels empty-promise subcubes arbitrarily and therefore supplies a total Boolean separator. This is the decisive prior structural theorem. No relative-influence threshold or square-weight instantiation is recorded in the body |
| [Li et al., arXiv:2504.05710v2](https://arxiv.org/abs/2504.05710v2) | Unconditional attacks replacing earlier conjectural cryptographic routes | Removing a dependency on PCC in a cryptographic conclusion does not establish PCC itself. No exact low-influence support theorem was located in its polynomial or theorem statements |
| [Bouaziz–Ermann et al., arXiv:2311.03512v1](https://arxiv.org/abs/2311.03512v1) | A conditional quantum-public-key-encryption separation; Section 1.2 still describes polynomial compatibility as open, and Conjecture 2.16 assumes it | A conditional application, not a target proof |
| [Iyer et al., arXiv:2310.08004v2](https://arxiv.org/abs/2310.08004v2) | Rational-degree results and unbounded separations for partial functions | No full-target influence theorem; a general partial-to-total rational-degree substitution cannot be assumed |
| [Kitagawa et al., arXiv:2608.17610v2](https://arxiv.org/abs/2608.17610v2) | Restricted unconditional attacks for imperfect completeness; primary version dated 1 October 2026 | Followed as a late chronological lead. Its theorem statements and full-body term scan contain no influence, OSSS, separator, or rational-degree target theorem |

The [official ePrint 2023/570 abstract](https://eprint.iacr.org/2023/570) and indexed primary PDF excerpts were also inspected: the work conditions its separations on PCC and states its polynomial form as Conjecture 2.8. Direct PDF retrieval returned HTTP 403. I do not claim a full-body negative exclusion for that unavailable body. The primary abstract already establishes that the advertised separation assumes the conjecture.

## Complete bridge and what it establishes

This derivation is included so that the classification does not rest on a vague claim that the old tools are related.

Assume f*g=0 on the entire cube. Li Lemma 3.5 supplies a total Boolean separator h with h=1 on supp(f), h=0 on supp(g), and depth T=O(d^4). On a common-zero input either label is allowed. The submitted reconstruction obtains T<=16*d^4 from a block count <=8*d^2, a query set <=8*d^3 per stage, and at most 2d degree decreases. That numerical reconstruction is an explicit-constant form of the prior mechanism.

Let r_i be the probability that the separator tree reads coordinate i, so sum_i r_i<=T. Original OSSS Eq.(6) states

    Cov(a,b) <= sum_i r_i E|b(X)-b(X_resample_i)|

for a computed by the tree with range [-1,1] and arbitrary real b. Apply it to a=2h-1 and a=1-2h. Their trees query the same coordinates, and Cov(2h-1,b)=2Cov(h,b). Thus

    |Cov(h,b)| <= (1/2) sum_i r_i A_i(b),
    A_i(b)=E|b(X)-b(X_resample_i)|.

This is exactly submitted Lemma 3. The resampling here includes leaving the sign unchanged with probability 1/2; it is not a forced flip.

Normalize u=f^2/||f||_2^2 and v=g^2/||g||_2^2. They are real nonnegative functions with expectation 1, even if f or g has mean zero. Parseval and Cauchy–Schwarz, applied to a forced flip and then multiplied by its resampling probability 1/2, give

    A_i(u) <= 2 sqrt(rho_i(f)*(1-rho_i(f))) <= 2 sqrt(rho_i(f)),
    A_i(v) <= 2 sqrt(rho_i(g)).

No L-infinity bound is required. The full norm is essential in the identity involving 1-rho_i.

Pointwise hu=u and hv=0. If mu=E h, then Cov(h,u)=1-mu and Cov(h,v)=-mu, so their absolute values sum to 1. The arbitrary common-zero hole disappears from this sum without any full-coverage assumption. Consequently, with delta the maximum relative influence,

    1 <= (1/2) sum_i r_i (A_i(u)+A_i(v))
      <= 2T sqrt(delta),
    delta >= 1/(4T^2) >= 1/(1024*d^8).

This proves the claimed sufficient threshold 1/(4096*d^8). It identifies the target-specific work precisely: select normalized square weights, apply the prior covariance inequality to both sides of the prior separator, and add their covariances. It does **not** exhibit an earlier primary document recording that instantiation. It also does not support a claim of a new covariance or separator theorem.

## Why rational degree alone is not a complete earlier target resolution

Kothari v3 Definition 2 requires a rational denominator nonzero at every cube point. Fact 3 represents a total Boolean function and its complement by polynomials with complementary nonzero supports. Theorem 10 expressly assumes no common zeros as well as a zero product. None of these assumptions follows from f*g=0 alone.

For a concrete hole, on {0,1}^2 let p(z)=z1*z2 and q(z)=(1-z1)*z2. Their supports are disjoint but both vanish whenever z2=0. The putative denominator p+q=z2 is zero on that half of the cube, as is p^2+q^2. Assigning the hole to either side does not make the other original polynomial a nondeterministic representation of the complement. This example falsifies the automatic bridge; it is not a counterexample to the target influence theorem.

Li's separate promise-separator theorem repairs the support hole by allowing an arbitrary total extension. A proof that simply invokes the total rational-degree theorem for p/(p+q) without resolving the hole is blocked. The present Li-plus-OSSS route explicitly resolves it and is therefore materially different from such an unsupported reduction. This check prevents an incorrect `already_solved` classification based only on the total-function literature.

## Chronology and authentication

The primary arXiv histories give OSSS v1: 16 August 2005 01:00:05 UTC; Kothari-family v1: 13 January 2026 16:57:02 UTC, v2: 8 April 2026 16:30:00 UTC, v3: 28 September 2026 16:05:17 UTC; Li v1: 4 August 2026 15:33:42 UTC. Lee's official journal page gives publication on 17 August 2010. The CRYPTO paper is the 2022 conference version; the ePrint record was received 25 February 2022. The OWR source is Report 9/2025 and records the February 2025 workshop; I do not infer an exact PDF upload timestamp from that report number.

The independently fetched GitHub PR API gives creation/update at 10 October 2026 12:23:19 UTC and head b1d6bc6ceb66e9c9c98cfae229ee86e5720799e2. The raw PROOF.md retrieved from that commit is 13,567 bytes with SHA-256 20bf5956520b2b53bb4b415d7d5683a6ae1cf1273bd36372accbc49fab482da1, identical to the local input. It fully asserts the exact theorem and expressly disclaims novelty and priority. A priority review cannot use those disclaimers as a substitute for literature checking, but it should not attribute an affirmative firstness claim to this PR.

All principal prior mathematical inputs above predate the PR. The authenticated OSSS PDF is 186,342 bytes, SHA-256 fe6aa25ccf79b38b9d9490bc6d7e55260321b5dae2413dd712332c451e45db3b. Its internal title page prints September 24, 2018 while the arXiv version history labels the single v1 as submitted in 2005. Both facts are preserved rather than silently reconciled; either date precedes this target application by years, so the classification does not depend on resolving that typesetting-date discrepancy. The authenticated official CRYPTO PDF is 524,674 bytes, SHA-256 05967cbf844369eec7e0c5509346f7cde7fafb65ab8e65072fd2cf04a602942c. Remaining body/HTML identities and version evidence are in the fetch receipts and CHRONOLOGY_METADATA.json.

## Search scope, independence, and limits

QUERY_LOG.json records 39 exact queries in ten ordered batches, domain filters, batch-level returned primary leads, empty results, failed retrievals, and excluded secondary material. Primary bodies were inspected at relevant definitions/results/proofs and searched throughout for compatibility, influences, support separation, covariance, and related theorem statements. BODY_SCOPE.json records the precise files, term positions, and inspection limits. A negative term scan can miss an equivalent statement in unfamiliar language; these checks do not exhaust all published and unpublished mathematics.

The initial independent classification was recorded before reading submitted PROOF.md or source metadata. The root supplied the proposed mathematical ingredients as leads; I independently checked the pertinent primary sources and did not read other reviewers' files or root decisions in forming that record. After the record and source comparison, opening PR_FILES.json for file metadata unexpectedly exposed the old AUDIT.md patch included in that JSON payload. That accidental post-core exposure was immediately disclosed to the parent and is logged. No conclusion in this report uses the old audit. This report is therefore disclosed corroboration with a separately preserved independent initial record, not a claim of complete blindness through the end of the task. A later parent message reported other checks' agreement; it was received only after the substantive findings above had been recorded and communicated.

No external individual was contacted. No Git, PR, paper, Zenodo, or tracker mutation was performed. All authored output is confined to this review directory. Optional formulations involving general distributions, other groups, or approximate disjointness are outside this disposition; they must not be promoted from the present bounded classification.

## Recommended publication framing

Describe the result as an explicit source-credited corollary/application of Li–Li–Li–Liu's separator and the OSSS two-function inequality, with the square-weight deduction supplied in full. Add the original OSSS citation and explain its exact specialization. Preserve the no-priority/no-novelty boundary. Do not call it `already_solved` on the basis of these ingredients alone under the requested recorded-resolution criterion, and do not turn this bounded negative search into a firstness certificate.

## Distribution-only custody repair

On 2026-10-17T22:52:10.589615+00:00, the initial public BODY_SCOPE.json was found to include copied source result-heading strings. Its complete original is preserved only under the ignored sources/private/historical_seal_v1/ directory. The public version now retains all 249 heading line positions and exact source-line byte lengths/SHA-256 hashes, with authored scope, primary URLs, whole-body hashes, keyword positions and inspection limits unchanged. Extracted chronology-history text was likewise privately preserved and replaced publicly by structured factual version dates and sizes. Other public artifacts were reviewed for source excerpts. This repair changes distribution and custody only; it does not change the mathematics, classification, query coverage, or independence disclosure. DISTRIBUTION_REPAIR.json records the old external receipt identity and exact preservation checks; the superseding receipt pins the current public package.
