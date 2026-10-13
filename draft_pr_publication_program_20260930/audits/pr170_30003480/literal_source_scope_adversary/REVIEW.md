# Independent literal-source and mathematical-scope adversarial review

Verdict: **PASS for the exact binary closed-unit-ball target.** I found no fatal mathematical gap or source-scope mismatch in the permitted candidate. The proof rules out an arbitrary real determinant-coordinate polynomial for every n>=3, even within the displayed determinant convex hull. It therefore negatively resolves the binary conjectural description referred to by problem30003480. The n=4 rational tuple independently refutes the literal proposed Q1>=Q2 condition with all coordinates positive.

This verdict addresses mathematics and literal source scope only. It makes no historical-priority, novelty, operational-publication, or human-peer-review conclusion.

## Source reconstruction and exact claim

Sources independently acquired: [OWR Report20/2017](https://ems.press/content/serial-article-files/46684), [published Seigal paper](https://seigal.github.io/seigal2018gram.pdf), [HSS v2](https://arxiv.org/abs/quant-ph/0209085v2), and [PMC manuscript rendering](https://pmc.ncbi.nlm.nih.gov/articles/PMC6051437/). Complete PDF identities agree with the frozen submission's listed hashes, established by independent downloads. Detailed acquisition timing, HTTP outcomes and coverage are in ACQUISITION_PROVENANCE.json.

The exact source data are:

- OWR printed1226: binary format2x...x2, flattenings2x2^(n-1), determinants det(M_i M_i^T), image of the Frobenius unit ball; pointer to Conjecture1.5.
- Seigal Definition1.2, printed352: n>=2 and sum of squared real entries<=1.
- Seigal printed354: Q1=product_i(sum_(j!=i)d_j-d_i); Q2=(1/2)product_(epsilon in{+-1}^n)(sum_i epsilon_i sqrt(d_i)). All2^n factors, including global-sign partners, are present. Conjecture1.5 has n>=4 and every cube bound0<=d_i<=1/4, with Q1>=Q2.
- HSS v2: normalized smaller eigenvalues obey the polygon inequalities; its three-qubit realization uses real amplitudes.

No positive-rank or positive-determinant exclusion appears in the conjecture. The source's later nonbinary discussion does not broaden this binary statement.

## Adversarial checks

| Attempted failure | Independent result |
| --- | --- |
| Sphere substituted for closed ball | Rejected. The source is explicitly the closed ball; the candidate proves that smaller norms cannot repair a unit-trace eigenvalue-polygon violation. The endpoint s=2sqrt(max d) and zero entries are covered. |
| Complex sufficiency silently used for real tensors | Rejected. HSS's real three-qubit amplitudes, or the independently checked parity-support version, realize every triangle-feasible triple at norm1. |
| Extra feasible zeros destroy the odd boundary multiplicity | Rejected. Exact multiplicity leaves a residual polynomial nonzero at some point of the open boundary patch; a sign crossing there forces odd multiplicity. |
| Reflection carries the factor outside the domain | Rejected. Polynomial invariance holds globally; the reflected plane sum t_i=1 has a separate open patch near(1/3,1/3,1/3) strictly inside the feasible domain. |
| Residual polynomial vanishes on the entire reflected patch | Rejected. That would force another copy of its linear factor, contrary to exact multiplicity. |
| Convex-hull inequalities prevent the crossings | Rejected. Both required patches have strict determinant-polygon inequalities, as derived independently in DERIVATION.md. |
| Zero-slice removal changes norm or other determinants | Rejected. Normalized rank-one factors have unit contraction and preserve all remaining Gram matrices and Frobenius norm. |
| Q2 product halved or duplicates removed | Rejected. Independent exact enumeration uses all16 n=4 factors and prefactor1/2; results match all candidate fractions. |
| Candidate merely invalidates a printed typo | Rejected. The arbitrary-polynomial obstruction is independent of printed Theorem1.4; the n=4 example uses the literal conjecture and HSS necessity. |
| Claimed conclusion improperly covers general dimensions | Rejected within the stated scope. Binary means every factor has dimension2. Larger factor dimensions, auxiliary coordinates, and punctured domains are not covered by the theorem. |

## Printed-source caution

For the unit real GHZ tensor, direct flattening gives d=(1/4,1/4,1/4). Independent full-product evaluation gives Q1=1/64 and Q2=9/512. The secondary pair expression in printed Theorem1.4 is1/4, above its printed upper bound3/16. Thus the literal displayed union excludes a feasible tuple. Printed365 says the corresponding pair polynomials are positive, corroborating a sign discrepancy. This does not justify silently substituting a repaired theorem. The candidate handles the issue correctly by using a separate HSS-based proof.

## Coverage and limits

I read all20 pages of the published Seigal paper and all3 pages of HSS v2, including their qualifications and references. I read the entire Seigal OWR contribution and references at printed1226–1227 and the report identification, within an independently acquired and extracted74-page report. I do not claim to have read the unrelated workshop contributions. All14 retained relevant/contextual page renders were visually inspected. Relevant PMC definitions, formulas, proof and computational passage were read; the full PMC article body was acquired. The web tool returned a recaptcha page for PMC; a separate direct HTTP fetch successfully returned the article. There is no inaccessible primary evidence needed for this verdict.

The source's random-tensor discussion cannot establish sufficiency, which asks whether every allowed determinant tuple is realizable. That is a methodological observation, not an assumption needed in this review. Finite checker cases likewise do not establish the all-polynomial theorem; the written multiplicity proof does.

The strongest verified result is the all-n>=3 impossibility inside C_n or H_n, plus the strictly positive n=4 counterexample to the named formula. Exact remaining mathematical gap in that result: **none identified**. The theorem is not machine-formalized. Historical priority and later literature remain unaudited by this worker. The proof via zero slices does not separately establish higher-n impossibility after deleting every zero-coordinate face; that alternative domain is absent from the literal source conjecture.

## Independence and handling

Only the three permitted original files, independent public sources, and the PDF skill policy were consumed as external file inputs. No author review/verifier/results, ROOT/sibling notes, PR body/comments or scientific reviewer conclusions were read before either freeze or this verdict. The original source_manifest contains incidental operational assertions; none was used as scientific evidence. All writes stayed in this reviewer's assigned directory; there were no Git/index/ref/branch/checkout, MAIN/PR/remote writes and no external communications to individuals.

The public own-output whitelist is explicit in RESULT.json. Source bodies, extractions, renders and private scratch are excluded from that whitelist, while their identities are preserved in the complete file inventory.
