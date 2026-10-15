# Independent primary-source priority and attribution report

Review date: 2026-10-07 UTC. Current manuscript reviewed: `manuscript/main.tex`, SHA-256 `25a9b9e5df03ea50c24812f5107bf3913ab352296faf6d5170e0372c4be8b9f4`.

## Verdict

No substantive priority or attribution defect was found in this manuscript's current title, abstract, scope discussion, or bibliography. The rational FPRAS and TV sampler should be credited as consequences of the public unweighted theorem and classical machinery. The manuscript does so explicitly. It establishes no independent approximation breakthrough or new complexity classification, and its own wording correctly declines those claims.

The evidence does not establish a public standalone source containing this exact full Horner-DAG proof, fixed-bit sampler specification, boundary treatment and reproducibility package. Nor does it establish that these details are novel. The mathematical existence of the target algorithms is already implicit in the public sources once the upstream theorem is available. The current note is honestly framed as an implementation/proof/exposition note about that consequence. I found no evidence requiring the user's prohibition against a duplicate preprint **advertised as a new solution** to block this framing. Publication materials must preserve that modest framing. A claim that this paper newly resolves weighted hafnian approximation would be false attribution; the paper's current explicit disclaimer avoids it.

This is a priority and source-scope review, not an independent certification of the lengthy upstream FPRAS proof, a full mathematical review of the wrappers, or a package reproduction. Any publication decision also depends on those other checks.

## Independence and scope

Read the supplied workspace AGENTS.md, project research/USER_REQUEST.txt, current manuscript, primary reading copies, bibliography and download manifest. Inspected the pinned source clone read-only. Preserved initial findings in `INDEPENDENT_FINDINGS_INITIAL.md` before any prior audit conclusions could be read. I did not read previous reviews, PRIORITY_AUDIT or SOURCE_STATEMENTS. An auxiliary independent agent performed additional fresh competing-result searches; its report is kept separately under `fresh_search/`.

All writes from this subreview are confined to this review directory. No individual was contacted; no source/candidate was edited; no commit, publication, or tracker action was performed.

## Source statements and attribution

### McQuillan: the rational general-graph equivalence is established

[Approximating Holant problems by winding](https://arxiv.org/abs/1301.2880), Section 7.2 (printed pp. 26–28), defines `#FugacityWeightedPM` using nonnegative rational edge weights and fugacities whose numerators and denominators are in binary. Lemma 25 constructs a polynomial-size all-unit-weight, zero-fugacity two-external-edge circuit with matrix signature diag(p,q). Lemma 27 explicitly constructs a simple unweighted graph with perfect-matching count C times the original closed-circuit partition function, for an easily computed positive integer C. It removes loops and makes the multigraph simple by subdividing each edge into a length-three path.

Thus a binary rational hafnian is already an exact scaled special case of unweighted general-graph perfect-matching counting. Lemma 27 is stronger scope than the note needs because it permits vertex fugacities too. It supplies an approximation-preserving equivalence independently of the upstream 2026 algorithm. The manuscript's Section 1 credit is accurate. McQuillan's specific binary-sum path construction has O(log^2 p) size in the worst case; the note does not attribute its linear-in-bitlength constant to that exact construction.

### Dell: logarithmic positive integer weights are established

[Dell–Husfeldt–Wahlén, ECCC TR10-078](https://eccc.weizmann.ac.il/report/2010/078/), Section 3, Figure 3 (printed pp. 7–8), already uses binary digits to simulate a positive integer a with O(log a) graph size in the permanent/directed-cycle-cover model. The proof explicitly uses parallel paths for addition and serial edges for multiplication. The [expanded five-author version](https://arxiv.org/abs/1206.1775), Section 3, Figure 3 (printed p. 12), retains this mechanism; it was later published in ACM Transactions on Algorithms in 2014.

This is not itself a theorem about arbitrary nonbipartite rational hafnians. The candidate carefully cites it for permanent gadgets and McQuillan for the relevant general-graph rational equivalence. That division of credit is correct. The Horner DAG and identity-edge conversion can be presented self-contained, but no invention of logarithmic weight removal is supportable.

### JVV: count-to-sample is established

Jerrum–Valiant–Vazirani, *Random generation of combinatorial structures from a uniform distribution*, Theoretical Computer Science 43 (1986), 169–188, Section 6, Theorem 6.3, proves that a fully polynomial randomized approximation scheme for a self-reducible p-relation's count yields a fully polynomial almost-uniform generator. It explicitly discusses graph 1-factors after the theorem. The paper's self-reduction framework attribution is accurate. Its direct fixed-bit TV analysis is useful specification detail, with no claim of a new equivalence.

### Upstream family 113: new base FPRAS; unweighted stated applications

Pinned commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`; local read-only clone and fresh current remote main both match it. In the primary `build/main.tex`, Theorem 1.1 states a uniform FPRAS for finite simple undirected graphs, rational accuracies, nonnegative rational output, exact zero on infeasible input, and every-execution polynomial bit time in input length, inverse relative accuracy and log inverse failure. Its final applications (source lines 3080–3127) expressly use an explicitly listed simple unweighted host and exclude compressed multiplicities/weights. Source lines 3195 onward give an unweighted deletion sampler using self-reduction.

The candidate's direct theorem attribution, bit-model assumptions and description of the source's application scope agree with this source. The main proof uses internal weighted intermediate models; that fact does not silently enlarge the stated input theorem to arbitrary external binary rational weights.

### Entropy companion: weighted scope is broader but accuracy is coarse

The pinned *Entropy and Face Dimension of the Perfect-Matching Polytope* source, `sections/05-weighted.tex`, proves brackets for arbitrary finite real log-weights. Its introduction, deterministic counting theorem (source lines 190–214), gives a uniform polynomial-bit algorithm on binary nonnegative integer pair multiplicities with N/512^n <= A <= N and exact zero; the algorithm is detailed in Section 9. It does not assert a relative-epsilon FPRAS or the requested weighted approximate sampler. The current manuscript's comparison is fair. The 2^(18n) factor mentioned elsewhere concerns its separate singleton-loop convention, not the loopless perfect-matching model of this note.

### Restricted hafnian comparisons

[RSZ](https://arxiv.org/abs/1409.3905), Theorem 1.2, assumes strong expansion of a dense regular graph and gives subexponential multiplicative determinant-estimator accuracy; its improved bound also assumes a spectral gap. The broader statements still require expansion/scaling promises. [Barvinok](https://arxiv.org/abs/1601.07518), Theorem 2.1, has entries in a fixed positive interval and deterministic quasipolynomial relative approximation; the related complex statements rely on zero-free regions. [Yi](https://arxiv.org/abs/2609.04079), current v1, Theorem 1.1(a), fixes gamma,theta, assumes nonzero entries in [theta,1] and support minimum degree at least (1/2+gamma)n, and gives deterministic polynomial relative approximation with exponents depending on those fixed parameters.

None of those precise primary statements is the unrestricted binary rational target. The candidate's brief scope descriptions and bibliographic volume/page/article information agree with their records. Yi's current source contains additional promised pseudorandom-support results, but that does not invalidate describing its dense bounded-weight theorem; it still does not give the arbitrary-support/arbitrary-positive-weight rational target.

## Public chronology

| Source | Public evidence inspected | Scope relevant here |
| --- | --- | --- |
| JVV | Journal volume 43 (1986); received July 1985, revised November 1985 on article front page | Count/sample equivalence; receipt dates are not claimed as public priority |
| Dell–Husfeldt–Wahlén | ECCC original report 27 April 2010; expanded arXiv v1 8 June 2012; journal 2014 | Logarithmic binary positive-integer permanent gadget |
| McQuillan | arXiv v1 14 January 2013 08:02:59 UTC; only version presently listed | Binary rational weighted/fugacity to simple unweighted matching exact scaling |
| RSZ | arXiv v1 13 September 2014 03:13:06 UTC; v2 2 September 2016 | Restricted estimator |
| Barvinok | arXiv v1 27 January 2016 19:46:45 UTC; v5 13 January 2017 | Restricted deterministic relative approximation |
| Yi | arXiv v1 3 September 2026 16:47:58 UTC; only version presently listed | Dense bounded-positive-weight FPTAS |
| OpenAI main and entropy companion | Official release announcement dated 6 October 2026 links repository; pinned initial commit author/committer time 6 October 2026 21:58:50 UTC in saved API record | The new unweighted general-graph FPRAS and coarse weighted entropy consequence |

Both upstream papers are internally dated 23 September 2026. That is accurate citation metadata, not evidence they were public on that date. The [official announcement](https://openai.com/index/sharing-ai-progress-in-mathematics/) establishes public release by 6 October. Neither an author's manuscript date nor a Git commit timestamp establishes an exact first disclosure instant. I found no earlier primary public disclosure in this bounded audit. An optional clarification in the bibliography or scope paragraph could call 23 September the manuscript date and 6 October the public release date; the current wording does not falsely assert September public priority.

## Already public implications and duplication boundary

The composition McQuillan + the upstream FPRAS already implies a binary rational hafnian FPRAS. Classical self-reducibility plus feasibility testing yields the requested TV sampling consequence, and uniform sampling after an exact weighted lift also pushes forward to the weighted matching law. Therefore the existence/classification of both algorithms cannot be honestly claimed as this note's new theorem discovery, even if nobody has yet written a single paper stating the combined corollary.

The note adds an explicit selected gadget, accounting, bounded-bit wrapper, boundary cases and finite checks. These are concrete expository/implementation artifacts; this audit does not establish their first public priority. Current title and abstract identify an exact reduction and consequences, and Section 1 states that the consequence was implicit once the base theorem became available and disclaims both first publication and a new classification. This satisfies the user's requested framing and avoids advertising a duplicate as a new solution. No known exact public duplicate of the whole account was found. Search failure must not be promoted to a novelty certificate.

If publication metadata were changed to claim an independently solved hafnian problem, the attribution verdict would change. If a requirement is interpreted as demanding a mathematically novel theorem beyond the inherited composition, that demand is not certified by this package; it should be described as a credited research note/consequence, as it currently is.

## Evidence limits and disposition

The auxiliary fresh-search report confirms that Cai–Liu explicitly credits McQuillan for the approximation equivalence. Its initial allegation that the corresponding 2019 arXiv text lacked that citation was false and was subsequently falsified by direct versioned-PDF, HTML and source inspection, documented in `CAI_RECONCILIATION.md`. Both the actual v1 arXiv account and ICALP proceedings support the attribution. The auxiliary search also traces earlier path machinery to Ben-Dor–Halevi and identifies Zankó's paper as an inaccessible original-source lead. The exact linear-size Horner construction's priority remains unresolved; no first-gadget claim is justified. Recent Anand et al. Gaussian-boson graph sampling concerns a different subset law and does not supply the fixed weighted-perfect-matching target by arbitrary conditioning; Lim et al. has a special matrix/parameter promise. Details and exact queries are preserved in `fresh_search/REPORT.txt` and `fresh_search/search_queries.json`.

The fresh queries and retrieval limitations are recorded in `SEARCH_LOG.md`. A fresh unauthenticated GitHub API read hit the rate limit; the remote main hash and official announcement succeeded. This report does not establish exhaustive priority, certify upstream correctness, or decide whether a journal would value the exposition. No substantive priority repair is required for the current manuscript. Preserve the present credit/disclaimers consistently in metadata, README and final claims.

Third-party reading-only downloads made by the auxiliary reviewer are confined to `fresh_search/primary_reading/`; my follow-up Cai–Liu reconciliation downloads and extracted source text are confined to `primary_reading/cai_reconciliation/`. Both reading directories should be excluded from owned Git commits/public payloads. All remaining files in this subreview are authored reports, source-reference metadata or query records.

Priority/source audit completion: 100% of the assigned checks, subject to the stated bounded-search limits. Mathematical resolution and publication-package completion percentages are not assessed by this subreview.
