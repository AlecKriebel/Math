# Acquisition and scope review — Zenodo 23431676

**Scope complete; independent mathematical decision pending.** This document authenticates sources, identifies the exact claim and its primary interfaces, and supplies a conditional editorial candidate. It is not a mathematical PASS, a verification-program result, or permission to publish a page.

## Edition and authenticated inventory

*CoNP-completeness of binary directed chip-firing reachability*, Alec Kriebel, Zenodo DOI https://doi.org/10.5281/zenodo.23431676. Queue row67, work Z-23431675, inventory index83, version1.0. The six-page manuscript prints “15 October 2026, version1.0”; Zenodo `publication_date` is 2026-10-15. The record's `created` timestamp is 2026-10-17T05:45:36.045033+00:00. These are different facts: a page may label October15 the manuscript/edition date but must not infer an October15 DOI deposit or web publication.

All public assets were freshly retrieved from the Zenodo API. Their byte sizes and MD5s match fresh public metadata and the queue; independent SHA-256 commitments follow.

| Public asset | Bytes | SHA-256 |
|---|---:|---|
| paper.pdf | 77187 | 6ae840e0b2e1df73b204c2c293c3fbcfa39206654e775a75261515c693a6187d |
| pr1097_support_v1_0.zip | 5658794 | 94280d71c41617198e96f1f4b4aca043ff86c3feda3109e0af9a1a18e1db651d |

The ZIP contains198 regular members, safely extracted with path/symlink screening, CRC validation, per-member SHA-256 and original permission bits. Its sole embedded PDF is byte-identical to the current main reader. There are no nested archives or additional reader editions. All member mappings are preserved in `sources/extraction-integrity.json` and `reader-support-map.json`. The current proof is `sources/published-source/pr1097_support_v1_0/paper.tex`. The current finite-check program is `scripts/run_checks.py`; `scripts/common.py` and `scripts/verify.py` concern integrity/custody guards. Other substantial contents are historical provenance and assessments, not extra paper chapters.

I read all six actual PDF pages, the complete current TeX, and these three current support-program bodies. I did not execute any mathematical or package verifier. No claim of a fresh verifier PASS or of replaying historical omitted programs is made.

## Exact language and model

Theorem1 claims **coNP-completeness under deterministic polynomial-time many-one reductions** of the language of valid triples ((G,x,y)) satisfying all of the following:

- (G) is a finite nonempty **loopless strongly connected directed multigraph**. Its vertex count varies with the input.
- Its adjacency entries (a_{uv}\in\mathbb N), including parallel-arc multiplicities, are encoded in binary. One does not expand a multiplicity into a list of individual arcs.
- Both initial and target configurations (x,y\in\mathbb N^V) are nonnegative integer vectors encoded in binary.
- A firing at (v) is legal precisely when its current chips are at least (d_v=\sum_w a_{vw}). It removes (d_v) and sends (a_{vw}) to each (w). Firings are sequential.
- Reachability means **there exists a finite legal word ending at exactly (y)**. The empty word is allowed, and the word may stop even when further moves remain legal. It need not be a maximal game or end at a stable or recurrent target.
- Invalid encodings are NO inputs. The loopless one-vertex graph is explicitly included: all firings have zero effect and reachability is exactly (x=y).

The column firing matrix is (L_{wv}=a_{vw}-d_v\mathbf1_{w=v}), so a firing count (f) gives endpoint (x+Lf). This is the negative of the Laplacian sign convention in Farrell–Levine. A loop cancels from this matrix while still contributing to the legality threshold; the preprocessing therefore cannot simply delete loops. There is **no designated absorbing/nonfiring sink** in the target model. For at least two vertices, strong connectivity implies positive outgoing degrees. The gate and marker are ordinary vertices, not sinks.

The precise exclusion list is material: no corresponding classification is asserted for simple graphs, unary encodings, bounded degree, bounded total chips, fixed vertex count, or every signed-input formulation. The output uses large degrees/multiplicities/chip counts. The result does not classify unrestricted Petri-net reachability, rotor-routing, or halting.

## Claimed proof organization and quantifier obligations

The source is the complement of the credited strongly connected binary directed-multigraph HALTING language for a supplied nonnegative starting configuration. The paper carefully gives two alternative total-string extensions: valid NONHALTING with invalid strings rejected, or the literal complement of HALTING, where invalid strings are accepted. The reduction must use the corresponding fixed NO or YES target for malformed inputs consistently.

Lemma2 handles signed intermediate lattice representatives by adding (k_v=\max(0,-x_v)) loops and chips at each vertex, shifting both its current count and threshold by the same amount. Loop removal then replaces each positive loop multiplicity by one fresh relay and binary-weighted arcs in both directions. The relevant claim is preservation of existence of infinite legal play, using arbitrary interleavings and bounded relay counts. Singleton sources are decided separately and replaced by suitable two-cycle inputs. This prepares a loopless, nonnegative source with at least two vertices; it does not extend the target language's membership theorem to arbitrary signed configurations.

The finite-state cutoff is (N=(C+1)^n), with (C=\sum_vx_v); (M=N+1) and (B=N(MD+1)). It is a possibly exponentially large integer, not a polynomial trajectory-length bound. The claimed reduction writes its binary representation and a graph of polynomial vertex count, not the trajectory or unary arcs. It adds a gate and a marker, with target computed explicitly from the original input. The mathematical families should independently check all formulas, nonnegativity/conservation, bit bounds and both implications.

The critical reverse-direction quantifier concerns **every legal target-reaching word**, not merely the displayed forward firing counts. The target marker balance forces at least one gate firing. The first gate requires at least (N) preceding old moves; their first (N) moves must project legally to the source. Extra periods, delayed first gates and later gate/marker firings are allowed and cannot be dismissed by assuming the designated count vector. The forward direction uses a finite legal source prefix, one gate firing and a reserve-funded completion of the old counts, then stops at the target even if other firings remain possible.

Section4 explicitly attributes membership to existing work. It computes the unique reduced nonnegative integer count (g), then uses a proper vector (u\leq g) whose uncompleted coordinates are below their firing thresholds as a certificate of nonreachability. The certificate need not itself be a legal partial trajectory. Its bit length, strict inequalities, properness, period deletion and the integer-image nonmembership branch all matter. This is a claim about concise negative certificates, not an algorithm that efficiently generates the target-reaching word or runs a potentially exponential bounded game.

## Primary-source interface inspection

Five raw primary PDFs were freshly acquired with URL, size, SHA-256 and page counts in `primary-source-receipts.json`. Their adjacent text files are reading derivatives. Exact named statements and the surrounding definitions were inspected; no comprehensive proof review of every upstream reference was attempted.

1. **[Farrell–Levine, CoEulerian graphs, arXiv v3](https://arxiv.org/pdf/1502.04690v3)**,15pages. Its introduction allows loops and multiple edges, assumes strong connectivity, gives signed configurations generally, and formulates the halting input with nonnegative chips and an adjacency matrix. Section3 contains Theorem3.1's polynomial-time **total-Laplacian** realization, its determinant entry bounds, the signed intermediate (sigma_{max}-sigma), and Corollary3.2's NP-completeness. I read the theorem's construction through its strong-connectivity and polynomial-size conclusions. The present manuscript must supply its stated threshold normalization to reconcile signed intermediate representatives with its nonnegative source. A reduced Laplacian with a fixed sink is not a substitute for this interface. This is the credited source hardness, not newly proved hardness here.

2. **[Hujter–Kiss–Tóthmérész, arXiv v4](https://arxiv.org/pdf/1507.03209v4)**,14pages. Sections2.1–2.3 define loopless multigraphs, adjacency-matrix logarithmic input size, nonnegative `Chip(G)`, sequential legal games and reachability. Theorem1 is the halting dichotomy; Lemmas4–5 are period deletion/reduced realizations. Theorem12 and its proof give coNP membership on general digraphs. Theorem14 requires a **recurrent target** in addition to linear equivalence. Problem19 on printed page12 asks the general reachability complexity, and the following sentence conjectures coNP-hardness. This original problem body authenticates the historical question without requiring a current web-page open label.

3. **[Björner–Lovász, revised July1992 author manuscript](https://www.cs.elte.hu/~lovasz/morepapers/abacus.pdf)**,23pages, redirected by the author host to `https://lovasz.web.elte.hu//morepapers/abacus.pdf`. I inspected graph/loop conventions, game-language/halting and bounded-game statements in Section1, primitive periods in Proposition4.1, the full period-deletion Lemma4.3 argument, reduced-count Lemma5.2, and the binary input-length discussion surrounding Theorem5.1. These predate and are credited by the present membership exposition.

4. **[Tóthmérész, arXiv v2](https://arxiv.org/pdf/2102.11970v2)**,16pages. Its chip configurations can be signed, and graphs allow multiple arcs but no loops. Claim2.4 and its proof deterministically convert recurrence to a return-reachability query after one chosen legal firing. Proposition2.8 uses an **existential recurrent representative** of a nonhalting linear-equivalence class as a certificate; it does not give a deterministic polynomial construction of that representative as a specified output. Theorem2.3 gives the earlier polynomial-hierarchy barrier to a polynomial-time reachability algorithm. This is close antecedent work and must be credited; it is not identical on its face to the claimed deterministic many-one completeness result.

5. **[Kiss–Tóthmérész, arXiv v3](https://arxiv.org/pdf/1407.6958v3)**,16pages. Section4, including Definitions4.1–4.2, Lemma4.3 and Claim4.4, already uses large parallel multiplicities/reserves and bounded-drift finite-horizon simulation for distance to nontermination and divisor-rank hardness. The current paper does not originate reserve simulation or scaling as a general method. The question here is the specific explicitly computed target and the gate/marker equivalence, whose correctness and novelty are separate questions.

The live [Egres survey](https://lemon.cs.elte.hu/egres/open/Chip-firing) timed out in direct acquisition and was inaccessible through direct browsing. Web search returned an indexed survey body identifying oldid2470: signed distributions, separate simple/multigraph rows, and a historical general-digraph coNP-hardness conjecture. That indexed historical text corroborates context but is not a fresh hash-authenticated live page and does not establish current openness. The exact question is already available in the fresh HKT primary PDF. No broad novelty search, comparison with all old Petri-net originals, or confirmation of the manuscript's historical “22 bodies/60 queries” audit was performed.

## Attribution and editorial boundary

A faithful eventual page should give the complete original abstract and exact theorem restriction, describe the finite-state gate/marker mechanism, and credit Farrell–Levine for the halting hardness, Björner–Lovász for periods/reduced counts, HKT for membership and recurrent-target reachability, Tóthmérész for recurrence conversion/hierarchy barrier, and Kiss–Tóthmérész for reserve simulation. The candidate supplies those credits with primary links.

“Halting” here concerns a **given graph and given starting configuration**: whether its maximal legal games terminate. This differs both from reaching a designated target and from a property quantifying over all configurations or all chip totals on a graph. A statement that a graph is Eulerian/coEulerian or that all configurations in some class terminate cannot replace the precise source decision problem. The target reduction is an existence-of-finite-word problem even on inputs from which continued play is possible indefinitely.

Do not label the result a first solution, a new general simulation method, peer-reviewed, accepted by a journal, formally certified, or independently human-verified. The manuscript declares extensive AI assistance and unrefereed status. Its own bounded audit leaves exact-result/gadget/method priority, independent discovery and present worldwide openness unknown. This scope task does not improve those labels.

## Necessary support inspection and independence

The current `run_checks.py` describes finite source state exploration, all-order prefix/cleanup controls, some unrestricted target states and alternate period counts, two-vertex certificates, signed/relay/singleton interfaces, deliberate faults and large binary samples. This is useful replay material for the independent mathematical families. I inspected it but did not run it or adopt its embedded `PASS` string. The current integrity modules were also inspected to identify output rules and replay boundaries.

`verify.py` contains literal assertions about historical review counts, finding-free verdicts, adoption statuses and administrative holds. Those inline assertions were incidentally exposed during necessary current-support inspection. Their truth was not evaluated or used as mathematical evidence. I did not open any dedicated historical assessment/report/verdict body under `provenance/`, nor current package `SOURCE_AUDIT.md` or status reports. Main-PDF and fresh metadata retrospective audit claims were unavoidable source content and remain attributed claims. No sibling review was read. All historical filenames are preserved as inventory data only.

The full source originals are unchanged. No mathematical verifier was run, no source repair was made, and no website, sheet, Git, deployment, UI or external communication was performed. `candidate.json` is a conditional local draft only; independent review and root clearance remain necessary. Follow-up questions are null under the high-bar policy.
