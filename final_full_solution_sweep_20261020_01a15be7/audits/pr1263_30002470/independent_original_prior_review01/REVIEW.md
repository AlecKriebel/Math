# Independent original/prior-result review: PR1263 / 30002470

**Verdict: full credited prior negative coverage of the original universal question.** The nine-vertex host `K4,4,1` has the required minimum degree and excludes every subgraph obtained from `C9²` with the stated degree sequence. The proof is for ordinary spanning containment. It does not depend on identifying the intended “periphery.” I found no mathematical or original-target coverage gap in the pinned PR's negative conclusion.

The existing result is credited to Alper Ferudun, *Dirac Graphs Without a Spanning Near-Square of an Odd Cycle: A Negative Answer to a Question of Heinig*, v1.0, 2026-09-28, [version DOI 10.5281/zenodo.23004012](https://doi.org/10.5281/zenodo.23004012), [canonical publisher page](https://eulersolve.org/papers/owr-12861-021/). This is a publicly posted, extensively AI-assisted, unrefereed preprint. Neither its posting nor this independent AI review constitutes conventional human peer review. The nine-vertex claim is already in the paper's Remark 3.5; the complete elementary argument in the PR and this review verifies that credited claim rather than claiming a newly discovered counterexample.

## Pinned inputs and actual original question

The reviewed head is `fe2a6ee824ccd3d68c9c1d0ec755660c571ddcfb`, base `4b27092a448d53b61408355ce44ec38d103a1ce4`. The full fresh live PR body and all three actual head files were read: `MATHEMATICAL_AUDIT.md`, `ACCEPTANCE_REPORT.json`, and `SOURCE_MANIFEST.json`. The exact diff has only these three additions; no eight-file pattern is assumed, and no QUEUE change is present. A read-only cached original-record recovery and the pinned catalog establish the same problem and statement hash; the cached research report is empty. Its older “partially solved” triage does not supersede an actual counterexample.

I freshly downloaded [the official original OWR report](https://ems.press/content/serial-article-files/46491), 774,443 bytes, SHA-256 `90e086e07098a23768ea07c6f8ed4924c04bd7480bd05fbad3f158edcde9f531`. Text read: PDF pp.77–79; visual inspection: PDF p.78 / printed p.82. Heinig's Question 1 begins on printed p.81 and continues onto p.82. His separate Question 2 is wholly on printed p.82 and asks the universal assertion for every odd `n≥7` at minimum degree at least `ceil(n/2)`.

The target starts with the square of an `n`-circuit and deletes alternate peripheral edges until three consecutive vertices have degree four; the page explicitly states that all other `n−3` vertices have degree three. It asks for a spanning copy, not an induced copy. There is no target drawing on that page. An affirmative answer to Question 2 is said to imply an affirmative answer to the distinct Hamilton-cycle-space Question 1. A counterexample to the former does not negate the latter. No audit of the entire later cycle-space literature is needed for this negative implication, and none is claimed here.

## Independent complete nine-vertex proof

Let `S=C9²`, with vertices `0,…,8` in cyclic order. Since `S` is four-regular, any deletion producing exactly six degree-three and three degree-four vertices removes exactly one edge at each of six vertices and none at the other three. The deleted edges therefore form a matching `M` of size three. This follows solely from the printed degree requirement. Alternate edges, a chosen periphery, and consecutivity can only restrict this class further.

The complete tripartite host `K4,4,1` has degree five at the eight vertices in its two four-vertex parts, and degree eight at its singleton, so its minimum degree is `5=ceil(9/2)`. If `S−M` had an ordinary spanning embedding into this host, remove the preimage `v` of the singleton. The remaining graph would embed into the bipartite graph `K4,4`, hence would be bipartite. A rotation of the nine-cycle lets us suppose `v=0`, with no assumption on `M`.

Inside `S−0` are six triangles `Ti={i,i+1,i+2}`, `i=1,…,6`. Every one must lose an edge if `(S−M)−0` is bipartite. Any edge hits at most two of these six triangles. The edges hitting two are exactly `23,34,45,56,67`: a distance-two edge hits at most one, and edges incident to zero hit none. Three deletions can cover all six triangles only by three disjoint double hits. In `T1`, the only double-hit edge is `23`, which also hits `T2`. To cover `T3` without wasting a hit on `T2`, the next edge must be `45`; similarly the last must be `67`. Thus the only possible deletion set after normalization is

`M={23,45,67}`.

However `1,3,5,7,8,1` is then a surviving five-cycle: `13,35,57,78,81` all belong to the square of the nine-cycle and none is deleted. The edge `81` is a wrap-around distance-two edge and must be retained. This contradicts bipartiteness. Therefore no singleton preimage and no three-edge matching can yield a spanning copy in the host.

This proves the original universal assertion false at the admissible order nine, for every target satisfying the stated degrees, regardless of its peripheral interpretation. It would be an artificial additional condition to withhold this negative answer until the intended periphery is uniquely reconstructed. Conversely, the proof does not assert that a fixed all-order host excludes every broad matching deletion for every odd order; that stronger assertion is false at seven.

The argument uses only elementary graph facts: a bipartite graph has no odd cycle, ordinary subgraph containment preserves that obstruction, and a spanning embedding is a vertex bijection taking required edges to host edges. No numerical feasibility oracle or unverified SAT output enters the proof.

## Separate all-odd-order theorem under the two explicit readings

I independently checked the full proof of Ferudun's Theorem 1.1 and the PR's reconstruction. Write `n=2s+1`, `s≥3`. The host has parts `|A|=s+1, |B|=s`, all cross edges, and `B` independent. If `s` is odd, put a perfect matching inside `A`. If `s` is even, put a two-edge path on three `A` vertices and a perfect matching on the remaining `s−2` vertices. Every `B` vertex has degree `s+1`. Every `A` vertex has degree `s+1`, except the middle of that path, which has degree `s+2`. Thus the minimum degree is exactly `ceil(n/2)` in every permitted case.

For either target `H`, a spanning embedding forces `J`, the preimage of `B`, to be an independent `s`-set. The leftover graph `H−J` must embed ordinarily into the host on `A`. If `F` is the target's set of three degree-four vertices, then independent-set edge counting gives `e(H−J)=3−|J∩F|`. Independence is essential here: it prevents an edge inside `J` being counted twice. No nonedge-preservation requirement is introduced.

For reading R2, keep the original cycle and delete a matching of distance-two edges along the cycle `Q` with vertex order `0,2,4,…` modulo `n`. An independent `s`-set in the retained odd cycle has exactly one gap containing two unchosen vertices and all other gaps containing one. Hence it has the form `{i,i+2,…,i+2(s−1)}`. Between these chosen vertices lie `s−1≥2` consecutive edges of `Q`. Since two consecutive `Q` edges share a vertex, a deletion matching cannot contain both. One survives, contradicting independence. This proves R2 impossible for every odd `n≥7`, without needing the degree-four vertices' additional placement condition.

For reading R1, delete the edges `{2j,2j+1}`, `0≤j≤s−2`, from the original cycle; retain all distance-two edges. Any independent `s`-set has cyclic runs of length at most two. A double run must be one of those deleted pairs. Each gap after a run has at least two unchosen vertices, since the second one is joined to the last chosen vertex by a retained distance-two edge. If there are `r1` single and `r2` double runs, then

`s=r1+2r2`, `2s+1≥s+2(r1+r2)`, and `r2≤ceil((s−1)/2)`.

The last inequality follows because distinct selected pair indices in `0,…,s−2` differ by at least two.

If `s=2t+1` is odd, these bounds force `r2=t`, `r1=1`, and every gap length two. Pair starts are even and lie between zero and `2s−4`. Successive pair starts are four apart except for a single seven-step across the singleton block. Since `n` is odd, only the seven-step can wrap around while preserving even starts. The smallest start is therefore zero or two. This argument includes `t=1`, where the seven-step returns to the same pair around the seven-cycle. Exactly the two independent sets are

`J0={4k,4k+1:0≤k<t}∪{n−3}`,

`J2={4k+2,4k+3:0≤k<t}∪{n−1}`.

Their complements contain respectively the paths `(n−4,n−2,n−1)` and `(n−3,n−2,0)`, whose two edges are retained. The second path explicitly uses the wrap-around distance-two edge. The host inside `A` is a matching and cannot contain either two-edge path.

If `s=2t` is even, the bounds force `r2=t`, `r1=0`. There are `t` pair indices in `0,…,2t−2`, separated by at least two, so they must be `0,2,…,2t−2`. The unique independent set is `{4k,4k+1:0≤k<t}`. It avoids all of `n−3,n−2,n−1`, which form a retained triangle. The host inside `A` is a forest and cannot contain that triangle. This completes both all-order cases. The one spare gap vertex in this parity is consistent with the unique chosen pattern and causes no wrap-around exception.

These all-order statements use the two specified R1/R2 definitions. The original universal negative answer separately follows from the broader order-nine obstruction and does not require claiming that those definitions exhaust authorial intent.

## Seven-vertex controls and the separate source graph

The host `G7` is `K4,3` plus two matching edges on the four-vertex side. It does contain the broad target `C7²−{01,35}`. An explicit target-to-host vertex permutation returned and checked independently is `(6,5,0,1,4,3,2)`, using the canonical host labeling in the checker. The cycle `(2,4,6,1,0,5,3,2)` is also an actual Hamilton periphery in `C7²`; deleting its edges `10` and `53` alternately leaves the consecutive degree-four vertices `2,4,6`. Thus this is a real foil even for that broadened peripheral convention. It confirms that the all-order theorem cannot be inflated to all matching deletions. It is an ordinary, non-induced spanning embedding: the target has twelve edges and the host fourteen.

I freshly recovered [Heinig arXiv:1112.5101v1](https://arxiv.org/pdf/1112.5101v1), 727,223 bytes, SHA-256 `9abbc94ec9f9ef98cd3981e5ae3e3727d2a579cb86027f583324a4f295274f7f`, and read pp.30–31 with visual inspection of p.30. Definition 28's explicit edge list for `X` gives `G7` under `(v1,v2,v4,v5)` as the larger part and `(v3,v6,v7)` as the smaller. The checker verifies the full graph isomorphism, rather than interpreting the picture as a near-square target.

Figure 4 and Proposition 30 concern a Hamilton-cycle basis for the cycle space. As an additional exact positive foil, I transcribed the eight displayed Hamilton cycles, verified their edges in `X`, and checked their binary rank is eight, equal to `14−7+1`. Thus this same small host is a positive example for the distinct cycle-space conclusion while excluding R1 and R2. No general cycle-space theorem or journal-version proof is being imported or re-audited.

## Actual prior-paper, DOI and archive inspection

All five pages of the fresh canonical publisher PDF were read as text and visually inspected. Its SHA-256 is `02ea0f37da91ece4bf3dcab399ef2dbe52f891b5cddc649ab3845ce3efed6824`, length 86,693 bytes. Section 2 states both target readings and the host; Lemmas 3.1–3.3 and Theorem 1.1 provide the all-order proof checked above. Remark 3.5 explicitly states the stronger `K4,4,1` obstruction for all 177 labeled matchings but supports that particular statement computationally. The elementary triangle/five-cycle proof independently certifies precisely that prior claim. Remark 3.6's optimal-threshold enumeration and the manuscript's reported SAT/auditor runs are not needed for full target coverage and are not adopted as reproduced evidence.

The fresh canonical verification report was read in full as author-reported history. The paper and publisher disclose extensive AI involvement and unrefereed status. Statements there about an “independent referee,” proof checking, searches, SAT runs or priority are not converted into external human peer review or newly verified execution records here.

The canonical source ZIP was actually downloaded: 35,881 bytes, SHA-256 `22ea85f687d9a2ea27d8a2f26a7c6c23586b24843ce997bc2ed139a426149c95`. Every one of its 17 entries (16 files and one directory) was read for CRC validation and hashed individually. The archive contains the TeX manuscript, bibliography, license, verification report, reproducibility programs and their recorded outputs. The separately downloaded report equals the archived report bytes. No archive program was imported, executed, compiled or treated as an independent computation. Full archive CRC integrity is a byte-level fact, not a proof of its source programs or claimed runs.

The publisher metadata's complete PDF, ZIP and report hashes agree with the three actual fresh payloads. DataCite freshly authenticates the version DOI, exact title, author, v1.0 and issued date 2026-09-28. Its `IsVersionOf` relation points to concept DOI `10.5281/zenodo.23004011`; the concept record reciprocally lists version `23004012`, and the fresh bounded related-version query returns that one version. These are one publication family, not two independent solutions. The canonical website and its file URLs are reading/source aliases of that family. The original OWR DOI/PDF and Heinig's arXiv paper are source references, not alternative DOI credits for this negative result.

Direct Zenodo record, DOI and file endpoints returned 403 in this review. Thus I do not claim a new successful Zenodo file retrieval or fresh deposited-file MD5 comparison. The primary publisher's actual payloads and their metadata were recovered, and the existing Zenodo DOI identity and concept relations were independently authenticated through DataCite. This access limit is recorded rather than silently borrowing the historical PR's successful Zenodo retrievals. The current publisher page is explicit that this is an unrefereed preprint. Neither a DOI issue date nor the bounded family query certifies earliest disclosure, exhaustive priority or historical exact-byte visibility.

## Independent finite checks and attempted falsification

The fresh standard-library checker `verify_independent.py` was authored after the mathematical sources were read, before inspection of any source-author program. It builds the squared cycle from circular distances, rather than using the source's two row-generating edge loops. It enumerates independent sets by a cached binary circular-word transfer whose state records only the last two bits, remaining cardinality and first two bits for closure. It checks the actual wrap edges at closure and does not assume the claimed run/gap classification. The all-order proof remains the certificate; finite orders alone would not establish it.

Ordinary spanning containment is checked separately by generic bijective backtracking with required-edge constraints. Candidate twin pruning only uses an exact host transposition automorphism fixing other vertices; it does not use the independent-side reduction. Relabeled target witnesses and complete-host searches are positive controls. The induced-embedding setting is tested explicitly as a false replacement for the original semantics.

The actual normal, `-O`, and `-OO` runs produce byte-identical passing outputs. In each mode they establish:

- Correct host and target degrees, edge counts, complete R1/R2 independent-set classifications, and residual obstructions at every odd order 7 through 51.
- Eight generic ordinary noncontainment checks at orders 7,9,11,13 for both readings, with positive controls.
- All 177 labeled three-edge matchings and all 1,593 choices of singleton preimage at order nine. Exactly 1,584 cases have an explicit surviving triangle and nine use the forced-matching/five-cycle certificate. A separate bipartiteness traversal agrees in every case.
- The order-seven broad-matching positive embedding, the full `X≅G7` identification, and the eight-cycle binary-rank positive control.
- Fourteen rejected mathematical corruptions or boundary misclaims per mode, 42 rejections total: wrong parity/order, malformed edge, overlapping or too few deletions, a false five-cycle, an order-seven broad-negative claim, induced semantics, a nonbijective embedding, a missing wrap edge, a missing R1 independent set, adjacent R2 deletions, deficient host degrees, and a false Hamilton-cycle edge.

One initially selected “bad” five-cycle in the new checker was in fact another valid surviving five-cycle. The checker correctly refused to reject it. I replaced that control with a cycle using both a deleted edge and a nonedge; it is rejected in all modes. This is recorded as a correction to a test input, not a defect in the claimed theorem or a suppressed failure. No floating-point computation, downloaded source-author program or removable `assert` serves as authority.

## Ledger, proposal, remaining limits and closure

The fresh numeric-gid GWS duplicate check preceded substantive mathematics at 2026-10-22 09:15:34 UTC. It returned 191 nonempty rows in the 43-column range `A1:AQ1178` for gid `1254632077`. No problem, original code, exact paper-title or version/concept DOI lead matches this result. Twenty-four rows mention Ferudun; their problem/DOI contexts were inspected and concern other results. The current repository releases were checked separately. These bounded observations do not establish worldwide package absence or priority. Raw ledger bodies remain private.

The four-literal-string row proposal is local only. B is exactly blank. C is the already-existing version DOI `10.5281/zenodo.23004012`. D credits Ferudun and the unrefereed, AI-assisted status, describes the original universal negative answer and the independent analytic certification of Remark 3.5, distinguishes the two all-order readings, and preserves current source-access and priority limits. The proposal neither credits Alec Kriebel with the counterexample nor implies a new project publication or DOI.

The exact remaining mathematical gap for the literal original negative answer is **none**. Optimal minimum-degree thresholds, the full cycle-space literature, source-author SAT/program execution, exhaustive historical priority and independent human peer review remain outside the accepted conclusion. Direct current Zenodo byte comparison remains an access limit. None is a reason to weaken the proved universal negative into a merely partial or interpretation-dependent result.

All work is in this dedicated review directory. Previous PR1235/1239/1253/1260 sealed directories are preserved and checked read-only at closure. No external contacts, service writes, uploads, Git mutations, CASE/cursor edits, release, DOI reservation or merge occurred. The complete seal covers every file, including private inputs and nested manifests, excluding only its own exact path. A public artifact manifest does not authorize redistribution of private source or ledger bodies.
