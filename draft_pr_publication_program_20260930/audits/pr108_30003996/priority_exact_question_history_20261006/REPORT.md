# PR108 priority audit: exact question, history and follow-up

**Disposition: priority unestablished.** This family found no exact earlier hardness theorem or exact-question follow-up in the inspected primary literature. That is a bounded retrieval result, not evidence that the submitted result is novel. Priority clearance remains **0%**, and no publication, novelty, queue-closure or theorem-promotion authority is exercised here.

The parent granted the mathematical gate before this audit. The checked claim is strong NP-completeness of the finite, explicitly encoded, nonnegative integer threshold formulation and consequently hardness of the source optimization problem. This audit does not reopen central proof search. The authenticated original author effort is **2/5** from QUEUE plus prose at head `3526d46bf143b08e5055ffa7728c6278e9f958ea`; no original structured turn ledger was submitted. This audit used **0 extra central proof-search turns**.

## Exact target and historical wording

The full primary Kaibel contribution was read before candidate or old-review material: printed pp. 3014–3015, PDF pages 46–47. Its heading is “Open Problem: Arborescences and NP-hardness”; Problem 1 begins “(Why) is the following problem NP-hard?” The literal object is one undirected spanning tree, evaluated through every root's induced whole-tree orientation with a separately supplied arc-cost vector. The source motivates integer optimization over Martin's extension. Problem 2 instead fixes a directed root and sums destination-specific root-to-destination paths; its motivation is Wong's extension. [Primary report](https://ems.press/content/serial-article-files/46772).

The event took place 4–10 November 2018. The report is cited as volume 15 (2018), but EMS records publication on 17 December 2019. The publisher and institution DOIs are respectively `10.4171/OWR/2018/50` and `10.14760/OWR-2018-50`. These dates must not be flattened into a claim of a 2018 journal publication. [EMS metadata](https://ems.press/journals/owr/articles/16633), [MFO metadata](https://publications.mfo.de/handle/mfo/3672).

The dated heading and parenthesized “Why” authenticate a question. They neither exhibit a proof nor establish its present open status. The preceding Dadush bibliography belongs to the preceding contribution, not to Kaibel's question. Searches that cite the entire workshop report can refer to another contribution: the retrieved Earth Mover Distance paper cites Basu's assignment question. A report-level DOI match is therefore not a Kaibel follow-up by itself.

## Independent reconstruction and audit boundary

The initial independent reconstruction and search freeze is `INITIAL_FREEZE.md`, recorded at 05:00:40 UTC on 6 October 2026. Three search batches and the full source reading preceded candidate and old-review reads. No other current priority-family output or root priority conclusion was read. The later mathematical gate was read only to bind the already permitted mathematical scope.

For outward orientation, deleting an edge uv of T gives components U containing u and W containing v. Its whole-root contribution is

```text
sum_{r in U} c^r(u,v) + sum_{r in W} c^r(v,u).
```

This is a bookkeeping reconstruction of the literal model, not an earlier-hardness theorem or a new central proof route. Reversing all arc costs handles the opposite orientation convention. It also makes the gap in routing analogies checkable: a root-to-every-destination path objective normally charges an edge once per destination on the far side, whereas the target charges each selected oriented edge once per root. A path formulation requires an explicit transformation that removes that tree-dependent multiplicity; this family has not supplied one.

PR107 addresses the other source problem. Its closure cannot by itself establish either mathematical or historical priority for Problem 1. The original PR108 log acknowledges a shared literal-selector mechanism with the adjacent author's different model, so two entirely unrelated inventions are not asserted.

## What was actually searched and read

`SEARCH_RECEIPT.json` records **58 exact queries in 17 web calls**, their UTC times and returned result URLs. Sixteen raw responses are retained privately; the directly printed response of search15 has no retained raw hash, and its public receipt explicitly limits the result list to selected primary metadata. Search requests are retained exactly for the final two batches. Earlier query arguments were retained exactly, while historical open/click/find scopes are separately listed in `SOURCE_LEDGER.json`.

The search families covered the exact contribution title, Kaibel plus Problem 1, both workshop DOIs, full-tree/all-root/root-dependent/root-specific/source-dependent terminology, rooted orientations, “Martin” integer optimization, common underlying trees, two-hub SAT gadget wording, post-2018 author publications, explicit 2025–2026 terms, German NP-Härte/Spannbaum/Arboreszenzen and French arbres couvrants. Result snippets and mirrors were discovery aids only. Technical conclusions below rely on primary full texts.

The official author and research-group publication pages were followed before inspecting two material near matches. The author page points to a publication list with post-2018 entries; that is not a complete live citation graph. Source-to-follow-up chaining was attempted through the exact title and report DOI. No direct theorem-citation chain was located. Old author/source-search and old independent review material was read only after the freeze; it contains no independently checkable exact-prior-hardness theorem. Imported “open” and literature-check date fields cite the workshop report and do not establish continued openness.

## Full-text near matches and explicit gaps

**Orlovich, Kukharenko, Kaibel and Skums, arXiv:2005.13703v1 (2020), 27 pages.** The full author preprint, including proof, formulations and references, was read. It optimizes degree-square and degree-product indices of a tree and proves hardness on restricted graphs. Section 6 uses Martin variables to describe trees but adds Boolean edge-product variables to linearize its objective. Its linear objective on those added variables is not an objective on the bare all-root orientation coordinates. Merely citing Martin or placing an NP-hard tree objective in a larger extension does not transfer hardness to this target. No objective-preserving translation, inherited exact restriction or Kaibel-question follow-up was established. [Primary preprint](https://arxiv.org/abs/2005.13703).

**Pignolet, Schmid and Trédan, “On the Implications of Routing Models on Network Optimization” (2021), 14 pages.** The full author-hosted paper was read; one page was reread to resolve output truncation. Section VI scores source–destination routes with source-dependent edge costs. It has the destination multiplicity described above. Its hardness statements concern monitoring placement or constrained multicommodity routing, not the literal whole-tree all-root objective. This family found no exact translation or exact-question citation in it. [Primary author copy](https://schmiste.github.io/tnsm21routing.pdf).

Other retrieved items concerning Steiner orientations, tree packings, geometric Steiner arborescences, polytope diameter, popularity, Markov-tree sums or general quadratic trees were not promoted to exact-model antecedents. Except for the two full-text studies above, no complete-theorem exclusion is claimed for those items. Their presence in search metadata is not evidence that they were fully read.

Martin's 1991 paper is identified in the scale-free paper's bibliography. This family did not retrieve and fully adjudicate the original Martin/Wong papers or every classical routing/tree-optimization theorem; materially different current families are tasked with those translations. This report must not be used to preempt their results.

## Comparative novelty matrix

| Submitted or audited feature | Strongest checked comparison in this family | Priority conclusion |
| --- | --- | --- |
| One tree, all roots, entire induced orientation cost | Primary Kaibel Problem 1 authenticated; no later exact theorem located | Exact target authenticated; novelty unresolved |
| Finite explicit integer decision version, strong NP-completeness | Parent mathematical gate granted; no inspected exact antecedent | Mathematically cleared, historically uncleared |
| Costs in {0,1,n+1}, hence polynomially bounded | Original proof read; degree-index and source-path papers do not state this target | Strong restriction is part of claim; no priority clearance |
| Positive integer costs via uniform +1 shift | Each of N roots contributes N−1 arcs; fixed additive shift N(N−1) | Consequence of the same result; not a separately cleared novelty |
| Two hubs, variable vertices, clause vertices, clauses incident to at most three variables | Full candidate construction read; targeted gadget-wording search located no exact prior construction | Common SAT gadget appearance alone establishes neither priority nor novelty |
| Unbounded number of active root vectors | Candidate uses the structural root plus clause roots | No fixed-root-count result claimed |
| Symmetric structural-root costs, asymmetric clause-root tests | Candidate mechanism preserved; source-path objective has a distinct multiplicity | No inherited exact prior restriction established |
| Audited B=2 / costs {0,1,2} robustness | Already identified by parent as same-mechanism robustness | Not an original standalone priority claim; no clearance |
| Planarity, bounded overall degree, approximation hardness, global OPT=K+minunsat | Not claimed; the last identity is false globally | Must not be added to result or novelty claim |
| Problem 2 / PR107 literal selector | Different directed destination-path model | Neither closure nor priority automatically transfers |

The effective proof's structural identity, already checked by the mathematical audit, is
`F_t = K + (1-h) + n(q-m)`, where K=(n+1)m+n, h marks the hub edge and q counts clause-variable edges. At threshold it forces clause leaves and one hub edge per variable. Only on that structured subset does total cost equal K plus false selected literals. This report records the candidate's comparison object; it does not add a global optimization identity.

No full prior theorem in this family was found whose hypotheses admit an explicit exact reduction to every claimed restriction above. Therefore no claim is made that this family has proved the candidate a rediscovery. Conversely, the absence of such a theorem in the inspected corpus does not clear even the general hardness claim, and cannot clear the small-cost or graph-family refinements.

## Concrete publication recommendation and material obstructions

This family identified **no concrete exact antecedent or unread theorem plausibly covering this result**. The original Martin formulation paper is a citation lead, not a located hardness theorem. The two fully read material near matches do not supply the necessary objective translation. Generic incomplete indexing is an epistemic qualification, not an affirmative material obstruction and not a demand for a logically impossible exhaustive-novelty guarantee.

This family is favorable to publication of a carefully attributed proof note answering the literal question **if the pending independent objective/translation families also find no material antecedent**. The concrete pending work is their adjudication of classical/general tree and extended-formulation hardness translations. Final publication should wait for that joint assessment. This recommendation is not a priority-gate waiver and does not authorize a first-solution claim. Historical wording should say the question appeared in the November2018 workshop report published December2019; any current-status statement should be qualified as “no earlier proof located in the audited literature” with the search date, rather than “still open” or “first solution.”

## Exact remaining gaps

1. No concrete unevaluated exact antecedent was located. An earlier exact/equivalent whole-root orientation theorem could still occur under an unsearched name or in nonindexed material. This is a bounded-search qualification, not an affirmative obstruction by itself.
2. The concrete pending independent-family check is whether a general earlier hardness theorem has a checkable translation. Such a theorem would settle general-priority questions even if it does not preserve the two-hub or cost-alphabet restrictions. No particular such theorem or transfer is established here.
3. The author publication list and search-engine results do not provide exhaustive cited-by coverage. “No follow-up located” is the strongest search conclusion.
4. The initial pilot inventory and one failed sparse-checkout read were not fully instrumented; a later inventory/gate read also lacks retained stdout hashing. Known gaps are disclosed in the execution ledger. Primary PDF retrieval/extraction and complete near-match reads have actual process receipts.
5. PMC returned a challenge page after an initial partial rendering. The scale-free paper was recovered from its primary arXiv preprint. The old author URL and the MFO event view returned internal errors; working primary metadata pages were used. No download or communication request was made to another person.

Further independent bibliographic evidence could change the disposition. No outside input was solicited or prepared.

## Custody, reproducibility and permitted interpretation

All writes remain within this family's dedicated folder. No Git, branch, index, service, editor, publication, queue mutation, external message or outreach operation was performed. The two downloaded PDFs total about 1.51 MB. Third-party PDFs, extracted text and raw web results are under `private/` and excluded by `.gitignore`. The primary MFO license expressly restricts redistribution; no source text is offered as a public artifact.

`INPUT_BINDINGS.json` binds the relevant source, effective proof, original proof, original provenance and gate by bytes and SHA-256. `EXECUTION_LEDGER.json` exposes only execution metadata. `PRIVATE_CUSTODY_MANIFEST.json` binds private custody without publishing contents. `PUBLIC_OUTPUT_MANIFEST.json` and `SHA256SUMS` bind the public audit artifacts. Hashes attest the artifacts inspected or emitted, not mathematical priority.

This family's strongest checked result is source fidelity plus exclusion of two specific false-positive follow-up mechanisms after full-text reading. Its final priority result is **unestablished**, original effort **2/5**, audit extra central proof turns **0**. Parent adjudication is required before any promotion.
