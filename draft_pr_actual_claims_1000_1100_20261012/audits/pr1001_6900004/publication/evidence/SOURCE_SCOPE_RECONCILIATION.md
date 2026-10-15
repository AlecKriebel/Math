# Fresh source-scope reconciliation: PR #1001

Checkpoint: 12 October 2026, 20:38 America/Los_Angeles (13 October 2026, 03:38 UTC).

**Correction to provisional eligibility, not a mathematical correction.** Earlier intake preserved the full literal theorem and flagged the source interpretation for reconciliation. Fresh primary-source inspection now supports inclusion. Root has adopted conservative entry into the full workflow for the exact literal equality formulation. The historical intake and the pinned PR's explicit unqualified-interpretation hold are retained; neither is erased or retroactively represented as a broader solution claim.

**Recommendation: enter the full mathematical and priority workflow for the precise literal original formulation.** Do not accept, merge or publish it on this scope finding alone. The pinned PR currently claims a complete literal theorem and explicitly withholds an unqualified interpretation claim; that authored reservation must remain accurately recorded until any wording is deliberately revised.

The fresh source examination supports the literal formulation directly. I found no written competing equivalence relation whose classification is an additional requirement of Problem 4. Keeping a hypothetical alternative author intention as an unresolved mathematical obligation would add a condition that the source does not state. The current scope hold is a prudent editorial reservation, but it is not evidence of a missing case under the source's defined full-partition formulation.

## Source evidence

The primary version of record is Oleg Karpenkov, *Open Problems on Configuration Spaces of Tensegrities*, Arnold Mathematical Journal 4 (2018), 19-25, [DOI 10.1007/s40598-018-0080-7](https://doi.org/10.1007/s40598-018-0080-7). It was freshly downloaded from the [journal's PDF archive](https://armj.math.stonybrook.edu/pdf-Springer-final/018-0080.pdf). The [Liverpool author manuscript](https://livrepository.liverpool.ac.uk/3022838/1/stratum.pdf), dated 13 January 2018, was also freshly obtained. All text of both documents was read; journal pp.20-22 were rendered and inspected visually.

The relevant source facts are these:

- Definitions 1.1-1.3, journal p.20: positive dimension, simple graphs, labelled configurations, the full base `(R^d)^n`, coordinate-sign-preserving fibre equivalence, and connected components defining strata. The following subgraph remark compares actual unions of strata in that common base.
- Examples 1.4-1.5 and Figure 1, p.21, retain vertex collisions and isolated labelled vertices. Problem 5's example, p.22, again retains a collapsed edge in dimension two.
- Section 2, pp.21-22, emphasizes dimensions and adjacency. Problem 4 nevertheless asks: “Which subgraphs of K_n define the same stratifications?” Its preceding sentence discusses coinciding strata. Neither passage defines an abstract-poset or ambient-homeomorphism comparison, restricts to generic/noncollapsed configurations, or replaces the earlier definition of a stratum.
- The author manuscript has the same relevant definitions, examples, context and Problem 4; it supplies no additional comparison convention.

Checkable extraction locations: [journal text](/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/claim_scope_01/sources/pr1001/Karpenkov2018_version_of_record.txt:59), lines 59-102, 122-150, 153-207; [author manuscript text](/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/claim_scope_01/sources/pr1001/Karpenkov2018_author_manuscript.txt:17), lines 17-82, 101-150. The primary PDF pages and extraction hashes are recorded in [SOURCE_RETRIEVAL.json](/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/claim_scope_01/sources/pr1001/SOURCE_RETRIEVAL.json).

## Comparison with the actual PR assertion

Pinned PR head: `f333d06cc161b1b8ae8422bf413ed1ffae31e614`.

The asserted theorem is exactly

`for every n>=1, d>=1, and simple labelled G,H on [n], S_d(G)=S_d(H) iff E(G)=E(H)`.

Here `S_d` is the full connected sign-equivalence partition of the common Cartesian base, and equality is equality of its subsets. Collisions, deficient affine span and isolated vertices remain included. A collinear path is used as a witness inside that full base; it does not restrict the theorem to collinear configurations. Its quantifiers include the planar context and every positive dimension. This is a complete answer under the literal source formulation, subject to the proof and priority audits still to be done.

The report's source discussion and the acceptance document explicitly retain the interpretation hold: [REPORT.md](/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/claim_scope_01/inputs/pr1001/REPORT.md:72), lines 72-95; [ACCEPTANCE.md](/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/intake/pr1001/artifacts/ACCEPTANCE.md:9); [STATUS.json](/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/claim_scope_01/inputs/pr1001/STATUS.json:5). Accordingly, the historical assertion remains **a complete literal theorem with a held interpretation**, not an already-made unqualified assertion of a new solution.

## Exact ambiguity and workflow consequence

There is a semantic reservation: the informal word *same* is not separately defined for two graphs, and the surrounding section is interested in combinatorial structure. That makes a different intention possible. It does not establish such an intention, define the alleged alternative target, or show that the PR leaves an additional written requirement unproved. In particular, coincidence of individual strata is compatible with unequal complete partitions and therefore does not contradict the theorem.

My independent inference is that the source's explicit common-base definition and its subgraph-refinement comparison give sufficient evidence to audit this as a full candidate answer to **Problem 4 read literally as equality of its defined stratifications**. Such a title and claim can remain precise without claiming any unspecified abstract classification. Do not demand author outreach; it is forbidden and unnecessary for this source-grounded disposition.

Thus the next step is the originally authorized complete proof/reproduction/adversarial/priority workflow for that exact claim. If it survives, update the package's claim and scope documents consistently before promotion. The alternative-intention caveat may remain as a short limitation, but should not be used to silently exclude this full literal candidate. If the program instead deliberately selects an abstract-equivalence reformulation as its research target, that would be a separate, newly specified target, and this PR would not resolve it.

## Retrieval and acceptance limits

- The journal PDF is seven pages, 434,961 bytes; the author manuscript is six pages, 85,258 bytes. SHA-256s and extraction hashes are in SOURCE_RETRIEVAL.json.
- The web tool returned HTTP 406 for the author-manuscript URL; a direct fresh download succeeded and was parsed as a valid six-page PDF. This is a retrieval-method limitation, not missing source coverage.
- This narrow reconciliation did not inspect predecessor papers or later literature, certify novelty, prove the theorem, run PR-delivered code, audit the entire package, or communicate externally. No GitHub action or queue change occurred.
- Checkpoint: **100% of this source-scope reconciliation; 0% of fresh whole-result mathematical/priority acceptance.**
