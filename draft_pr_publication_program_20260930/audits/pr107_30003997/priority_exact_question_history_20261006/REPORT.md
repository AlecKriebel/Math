# Independent priority audit: exact OWR question and history

Initial report UTC: 2026-10-06 04:24:06 UTC; final cross-family incorporation: 2026-10-06 04:29 UTC. Target: PR107 / 30003997 / OWR-16633-014. Cutoff requested: 2026-10-06. This is a bounded literature audit, not a new proof attempt.

**Verdict: novel-resolution clearance is false.** Earlier accessible theorem proofs have objectives that embed exactly in unrestricted Problem2. After the independent initial comparison was frozen, root supplied a 2022 published construction that also implies the complete graph/cost restriction bundle. This family independently retrieved and checked that proof and the comparison. No substantive new hardness theorem or resolution is established by the candidate.

## Exact question and historical wording

The pinned source was read completely for Kaibel's contribution: printed3014–3015 / PDF46–47. The contribution is headed *Open Problem: Arborescences and NP-hardness*. Both numbered problems ask “(Why) is the following problem NP-hard?” The text supplies no proof, named solver, citation, or explanation of the parenthetical. It documents a workshop question; it does not authenticate an already known proof or establish later open status. Inferring the author's private knowledge or intent would exceed the evidence. [Official report](https://ems.press/content/serial-article-files/46772).

Problem2 is fixed-root, directed, and permits an arbitrary arc-cost vector for each nonroot destination. Its objective is the sum of each destination's vector along its own root path. Problem1 instead concerns an undirected tree and all root orientations. The curation background confuses these in one sentence; its 2026 “open” label is a triage hypothesis, not a priority certificate.

The workshop was 4–10 November2018; the MFO record gives institutional DOI10.14760/OWR-2018-50 and publisher DOI10.4171/OWR/2018/50. EMS identifies report volume15(2018),no.4,pp2969–3023, submission4November2018 and publication17December2019. Thus “2018 question, report published2019” is precise. [MFO record](https://publications.mfo.de/handle/mfo/3672), [EMS dates](https://ems.press/journals/owr/articles/16633).

## Checkable objective comparison

This algebraic identity is an audit deduction, rather than a claim quoted from a paper. Let an undirected rooted spanning-tree problem minimize

\[
F(S)=\alpha\sum_{e\in S}a_e+\beta\sum_{v\ne r}b_v\sum_{e\in P_S(v)}d_e.
\]

Replace each undirected edge by both directed versions. Every rooted out-arborescence corresponds bijectively to the undirected spanning tree oriented away from the root. For the directed arc \(h\to k\) from edge \(e\), define

\[
c^v_{h\to k}=\beta b_vd_e+\alpha a_e\mathbf1_{k=v}.
\]

Then the source objective is exactly \(F(S)\): the first summand is the weighted path part; the indicator part charges a selected arc once, for the destination at its head, where it is the final path arc. All other destinations contribute zero for that indicator. The table is polynomial in graph size and retains rational encoding and nonnegative costs. Feasibility is preserved, since a connected undirected graph becomes root-reachable. No polyhedral equivalence is needed.

This identity subsumes a linear tree-edge cost plus SUMROOTEDFLOW/cost-distance objective. It is sufficient for comparison to earlier theorem proofs. It does **not** preserve acyclicity, the candidate's four consecutive layers, indegree bound, binary/positive1–2 alphabet, or zero threshold.

## Earlier proof evidence

| Source and version | What was actually inspected | Priority implication |
|---|---|---|
| Dell'Amico–Maffioli, institutional preprint *Combining Linear and Non-Linear Objectives in Spanning Tree Problems*, cover August1997, report186; journal metadata June2000, JCO4,253–269, DOI10.1023/A:1009854922371 | Full PDF retrieved. Definitions pp2–3, X3C setup, theorem4.1 construction, and theorem4.3 proof/printedp13 read. Theorem4.3 visually checked against the scan. | NP-complete minimization of a linear tree cost plus SUMROOTEDFLOW, nonnegative integer weights, λ=1/2. Embeds in general Problem2. Journal typeset theorem text and first archival posting date were not checked. |
| Khazraei–Held, author preprint *An Improved Approximation Algorithm for the Uniform Cost-Distance Steiner Tree Problem*; WAOA2020, LNCS12806,189–203, first online6July2021, DOI10.1007/978-3-030-80879-2_13 | Full author PDF retrieved; equation1, section2/theorem1, entire 3SAT construction and proof read. Publisher metadata checked. | NP-hard spanning-tree case with undirected lengths1/2 and clause delay weights positive, remaining weights0. Embeds in general Problem2. The typeset paywalled chapter was not read. |

Primary links: [1997 author/institutional preprint](https://iris.unimore.it/retrieve/bcf0f9f5-acc8-4d58-b733-f27ac638a63a/0186.pdf), [2000 publisher record](https://link.springer.com/article/10.1023/A:1009854922371), [2021 author proof](https://www.or.uni-bonn.de/~held/publications/ucdg_preprint.pdf), [2021 publisher dates](https://link.springer.com/chapter/10.1007/978-3-030-80879-2_13).

A further audit deduction from the 2021 proof is that choosing the allowed constant clause weight1 gives destination table entries in {0,1,2,4} under the identity above, and a polynomial integer threshold. Hence even generic strong hardness with a bounded cost alphabet cannot safely be claimed new. This does not establish a prior {0,1}/zero-threshold theorem.

The dated preprint and published metadata are normal priority evidence, not a forensic proof of the date its current PDF became publicly available. The conservative publication anchor is the independently confirmed2021 proceedings record and its accessible matching author proof; no novelty clearance relies solely on a server's crawl date.

## Published construction covering the complete restriction bundle

This lead was supplied by root after the independent first16-query checkpoint and first58-query search were complete. Romain Chapoullié–Zoltán Szigeti, *On packing time-respecting arborescences*, Discrete Optimization45(2022),100702, DOI10.1016/j.disopt.2022.100702, theorem13, proves NP-completeness of a spanning rooted arborescence with monochromatic paths on a two-colored DAG. This family independently downloaded the full author-hosted journal PDF, read the entire theorem/construction/proof on printedpp11–12, and visually checked those pages/Figure2. It also retrieved arXiv2203.01096v1 and read the corresponding proof on pp10–11. The arXiv primary history dates v1 to2March2022 13:32:07UTC; publisher metadata gives August2022. The author-hosted journal PDF says accepted28March2022 but leaves its available-online field as “xxxx”; no precise first-online journal date is inferred. [Author-hosted primary proof](https://pagesperso.g-scop.grenoble-inp.fr/~szigetiz/OCG/13.C-Szigeti.pdf), [arXiv version history](https://arxiv.org/abs/2203.01096), [publisher record](https://www.sciencedirect.com/science/article/pii/S1572528622000147).

The published RXC3 instance has h elements and h three-element hyperedges, each element occurring in three hyperedges. Its graph has root s, hyperedge vertices u_i, element vertices v_j, and overlap vertices w_ij for distinct intersecting pairs i<j. Root-to-u_i has two parallel options, black and gray. Membership arcs u_i→v_j are black; u_i/u_j→w_ij arcs are gray. The display omits i<j, but Figure2, the bound |W|≤3h and the converse's explicit j<k fix that convention. The forward proof's displayed nonroot sets omit s while their intersection is written s; interpreting their root augmentations, or using the argument below, avoids importing that notation defect.

The following is an explicit audit inference, not the literal theorem statement. Subdivide each black root option as s→t_i→u_i and each gray option as s→f_i→u_i. Both selector root arcs are forced in any spanning tree; each u_i chooses one parent. Retain all terminal arcs. Set every coefficient to zero except that destination v_j charges every s→f_i arc1, and destination w_ij charges every s→t_k arc1. A cost-zero tree means each element chooses a black-selected hyperedge and each overlap chooses a gray-selected hyperedge. The black-selected hyperedges therefore cover all elements and are pairwise disjoint: an intersecting black pair would force its overlap destination to pay1. Conversely an exact cover selects its hyperedges black and all others gray, giving every element a black parent and every overlap a gray parent. These are exactly the published monochromatic choices after selector compression.

This graph is simple and reachable, with consecutive layers {s}, {t_i,f_i}, {u_i}, {v_j,w_ij}; all root paths have depth at most3. Nonroot indegrees are respectively1,2,3 and2. There are 1+3h+m vertices with m=h+|W|, and the dense binary table is polynomial. The nonzero costs lie solely on first-layer root arcs, as in the candidate. Adding1 to every destination/arc coefficient gives {1,2} and increases every tree cost by the same 2h+2h+3m=4h+3m. Thus the complete restricted hardness bundle follows from the prior published construction through a straightforward model translation. The published paper does not print the destination-cost-table theorem verbatim, and it uses RXC3 rather than the candidate's direct3SAT gadget; those distinctions are retained.

## Restriction-by-restriction comparison

| Claim/restriction | Current verified candidate | Earlier accessible constructions inspected |
|---|---|---|
| Literal destination-specific objective | Exactly source Problem2 | Present after the explicit identity above; original terminology differs |
| Fixed root; spans every vertex; feasibility guaranteed | Yes | Yes in the relevant spanning-tree theorem cases |
| Simple graph | Simple directed DAG | Simple undirected source constructions can be bidirected |
| Four layers; consecutive-layer arcs; depth3 | Yes, for every feasible tree | Not supplied by the bidirected embedding; source digraph contains directed cycles |
| Nonroot indegree≤3 | Yes | Not a theorem restriction in the examined earlier constructions; literal/set nodes can have unbounded degree |
| Destination costs{0,1}; threshold0 | Yes | Not established in the earlier sources examined |
| All destination costs{1,2}; constant4n+3m offset | Yes | Undirected edge lengths1/2 in2021 are a different claim: converted destination table also has0 and4 |
| Direct3SAT consistency mechanism | Variable-parent choice shared by clauses |2021 has truth/literal–clause selection with an undirected literal-pair edge;1997 uses X3C/set selection |
| Generic NP-hardness | Verified | Already follows from earlier source proofs |
| Generic strong NP-hardness | Verified |2021 constant-weight construction plus comparison yields bounded destination numbers |
| Same complete restricted theorem or same directed gadget | Verified here | Complete theorem bundle follows from2022 construction as above; identical direct3SAT gadget not claimed |

The table's older bidirected constructions explain general prior hardness; the2022 transformation supplies every graph and cost restriction that they do not. The2021 proof and current candidate share a consistent literal assignment/true-literal witness idea. A direct3SAT derivation differs from the RXC3 derivation, but this does not establish a new theorem or conceptual discovery.

The candidate's equation7, optimum equals the minimum number of unsatisfied clauses of the cleaned formula, is accurate objective accounting: once variable choices are fixed, every clause independently chooses a parent and contributes0 or1. It is useful exposition and checker evidence. No independent approximation, gap, parameterized, or quantitative theorem beyond that accounting is stated and established in the candidate. It does not restore a substantive novel-result claim. Any proposed separate theorem would need its exact claim and a fresh source-bound priority audit; none is promoted here.

## Citation chain and later literature

Löhken–Stiglmayr's *A multi-objective perspective on the cable-trench problem*, arXiv2312.13810v1 (21December2023 13:03:59UTC), journal49,article55,26April2025, DOI10.1007/s10878-025-01289-0, was retrieved in both versions. Journal section2.2/pp9–11 and references were read. It attributes mixed arborescence/routed-flow hardness to Dell'Amico–Maffioli1996, and identifies a flaw in the older Vasko2002 hardness argument; it points to Khazraei–Held2021 and Benedito–Pedrosa–Rosado2023 for later valid proofs. This attribution is not used as a substitute for the earlier accessible proofs above. [Journal text](https://link.springer.com/article/10.1007/s10878-025-01289-0), [arXiv version history](https://arxiv.org/abs/2312.13810).

The original1996 directed article is *On some multicriteria arborescence problems: complexity and algorithms*, DAM65(1–3),191–206,7March1996, DOI10.1016/0166-218X(95)00035-P. Its institutional record explicitly reports no associated files; direct publisher retrieval returned403, and the DOI route returned a small HTML page rather than the article. Its theorem, exact restrictions and gadget remain unread. [Repository](https://iris.unimore.it/handle/11380/451178), [publisher metadata](https://doi.org/10.1016/0166-218X(95)00035-P).

Benedito–Pedrosa–Rosado's later sources were located: Procedia Computer Science195,39–48(2021), DOI10.1016/j.procs.2021.11.009, and DAM340,272–285,15December2023, DOI10.1016/j.dam.2023.07.010. Publisher previews and author bibliography were checked, but their full proofs were not retrieved/read in this family. They are recorded leads, not independent theorem verification. [2023 publisher preview](https://www.sciencedirect.com/science/article/pii/S0166218X23002743), [author bibliography](https://www.ic.unicamp.br/en/~lehilton/).

Foos–Held–Spitzley2023, DOI10.4230/LIPIcs.APPROX/RANDOM.2023.19, published4September2023, full PDF retrieved: its problem definition and references confirm continuing cost-distance terminology and the2021 citation. Its approximation analysis was not audited and does not settle the candidate's restricted priority. [Primary proceedings](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.APPROX/RANDOM.2023.19).

No paper in this chain was verified to say that it explicitly answered Kaibel's named2018 question. That bibliographic attribution gap does not make the unrestricted mathematical conclusion new.

## Subsequent Kaibel record and bounded-search coverage

The institutional publication list and research portrait were inspected; the former lists work through2024 and the latter through2025. Their incompleteness is visible (for example, one omits *Source detection on graphs*). They cannot authenticate absence of a2026 paper or an unpublished solution. [Group list](https://discopt.ovgu.de/publications/), [institutional portrait](https://www.ovgu.de/Kaibel.html?rewrite_engine=fast).

Accessible full text was obtained for plausible nearby works: scale-free spanning trees (arXiv2005.13703v1,27May2020; journal2021 DOI10.1089/cmb.2020.0500), source detection (22July2022 preprint; journal2024 DOI10.1007/s11081-023-09869-x), Steiner cut dominants (arXiv2209.14802, retrieved revision dated13March2024), and rock extensions (arXiv2307.05246v3,24September2024; journal DOI10.1137/23M1585878). Their concrete objective/definition sections were read and full texts searched for the target terminology and report citation. The first maximizes degree indices, the second minimizes oracle queries, the third studies cut polyhedra, and the fourth studies polytope diameters. None supplies a verified matching path-cost theorem in the examined sections. Remaining proofs were not read; they are not asserted irrelevant on title alone.

Kaibel's2011 extended-formulation survey (arXiv1104.1023v1,6April2011 07:22:45UTC) and Optima85 were retrieved; the spanning-tree and Wong formulation discussion was read. The arXiv PDF's generated26November2024 title date was not treated as a submission/revision date. These sections give context but no verified answer to the later question. [Survey history](https://arxiv.org/abs/1104.1023), [Optima85](https://mathopt.zib.de/Optima-Issues/optima85.pdf).

The exact-title/author/report/“Wong integer optimization” searches and later talks/preprints searches surfaced no attributable exact-question resolution in this family. Broader aliases searched included destination-dependent/specific costs, path-cost arborescence, rooted-flow, mixed arborescence and cost-distance/cable-trench. Results with only a common arc vector, robust regret, local changeover costs, or additional Steiner constraints were not silently equated with the target. These findings are bounded to the returned results, not all literature.

The query log records59 search queries in16 batches:58 independent queries before reading another family's findings, then one exact-title primary-metadata search for the root-supplied2022 lead. Raw search excerpts, source PDFs, text extracts, web pages and the visual theorem checks are all private. The final search batch is preserved as a selected-result note, not misrepresented as full raw output. First independent comparison was checkpointed after16 queries, before any other priority family's work was read. Root's comparison and finite-control summaries were read only after the independent search. Those finite controls were not rerun by this family. No external communication, prepared outreach, authentication bypass, Git/PR/tracker/native-editor/Zenodo mutation or new central proof search occurred.

A guessed arXiv2011.02446 lead was fetched and then excluded: its title/author record concerns a discrete time-cost tradeoff problem, not Khazraei–Held's cost-distance theorem. Its local filename was corrected and its receipt explicitly records the mismatch; it supplies no priority evidence. Direct publisher retrieval of the2022 article returned403; the complete author-hosted and arXiv proofs were legitimately accessible. Failed retrievals and unread source portions remain in the receipts/reading ledger.

## Required corrections and remaining gaps

1. Replace any claim that the unrestricted general NP-hardness result is novel or newly resolves an open2018 problem. Cite earlier mixed tree/path-cost and cost-distance hardness with the explicit comparison.
2. Describe the candidate as an independently verified direct3SAT proof/exposition. Its complete restricted hardness theorem is a straightforward consequence of a prior2022 construction; no novel strengthening is established.
3. Preserve the2018 workshop/2019 publication distinction and literal Problem2 scope. The dataset's “open” label cannot survive as an independently validated literature conclusion.
4. Do not claim the original1996 theorem/construction has been inspected. It remains an important unread gap.
5. Earliest priority, unpublished/oral knowledge, omitted author records, the full2000 typeset version, and unread2021/2023 cable-trench proofs remain unresolved. They do not undermine the verified2022 obstruction to novelty, and no amount of no-hit searching closes these historical gaps.

Bounded audit deliverables:100% complete. Discovery/novelty assessment: no established novelty; novel-resolution clearance false; restricted-strengthening clearance false, with a positive prior-construction obstruction. This percentage denotes completion of this assigned bounded audit, not probability that a theorem is novel. Original attempt budget1/5; added central proof-search turns0.
