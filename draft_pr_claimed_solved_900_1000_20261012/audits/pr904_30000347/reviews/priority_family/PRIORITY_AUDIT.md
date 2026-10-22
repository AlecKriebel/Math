# Independent priority audit: PR #904 / problem 30000347

Checkpoint: 2026-10-12 20:25 PDT (2026-10-13 03:25 UTC).

Reviewer role: independent literature/priority adversary, restricted to this eligible claimed_solved result. Only this review directory was written. Original packet and main were not edited. No external communications were initiated. This is an AI-assisted audit, not human peer review.

## Finding and status

**No exact preceding theorem was identified in the inspected literature. This is a bounded finding, not proof of first priority or of continued open status through 2026.** The exact historical problem/model is supported by primary full text. Two methodological attribution omissions need repair: the subdivision identity is already in Poljak (1974), and the tripartite spoke attachment has a close antecedent in Khachiyan et al. (2008). Neither inspected source states the exact target theorem.

Estimated completion: 100% of the bounded priority audit; approximately 65% confidence toward establishing first priority, which remains unverified. The exact remaining gap is inaccessible original Bienstock–Diaz full text, inaccessible final Dvořák–Knop journal text, incomplete citation indexing, and the unavoidable possibility of overlooked differently named literature. The report supports publishing a precise independently proved theorem with careful attribution and a historical source claim. It does **not** support a categorical statement that this is the first resolution or that no one solved the problem between 2006 and 2026.

## Exact claim being tested

For finite simple undirected graphs with unit traversal length and unit edge-deletion cost, decide whether at most B edges can be deleted so that all three distances between three specified distinct terminals increase strictly from their original values. The claimed hardness holds even when all three original distances equal 3. Every edge is deletable. Terminal disconnection is allowed; the optional variant supplies intact four-edge backup paths.

To falsify priority, a prior theorem or explicit construction must imply hardness for this restriction, not merely for a larger class. In particular, arbitrary thresholds, one-pair interdiction, directed demand cycles, full multiway disconnection, and vertex deletion are different restrictions. “A problem contains this one” is insufficient: hardness need not survive restriction.

## Historical model, independently verified

Krause's publisher contribution in Oberwolfach Report 50/2005, printed pp. 2856–2858, defines unit-traversal undirected BSP by hitting original shortest paths. It expressly lists the three unordered demand pairs on three terminals as an unresolved complexity case. The same contribution says directed triangle instances are already NP-hard. The workshop took place 6–12 November 2005; the report is associated with 2006 publication metadata. This establishes a historical question, not its current open status. [Publisher primary PDF](https://ems.press/content/serial-article-files/46024?nt=1)

Krause's dissertation, dated 24 February 2006, printed p. 2, permits terminal disconnection through its observation that ordinary multicut solutions are BSP solutions. Section 4.3, printed pp. 34–36, explicitly leaves undirected triangle complexity unresolved. Theorem 9.3, printed pp. 83–84, is directed. Its construction uses orientations and cannot be treated as an undirected hardness theorem. The “triangle” is the demand pattern, not adjacency of the three terminals. [Institutional-library primary mirror](https://webdoc.sub.gwdg.de/ebook/dissts/Braunschweig/Krause2006.pdf)

## Closest theorem/construction comparisons

### Poljak (1974): exact antecedent of Lemma 1

Printed p. 308 replaces every edge of a graph by a path of three edges and states α(F)=α(G)+m, with |V(F)|=|V(G)|+2m. Since τ(J)=|V(J)|−α(J), this is exactly τ(F)=τ(G)+m. I rendered the original scanned page and visually checked the equation. The explicit three-part partition is immediate from this construction. Therefore Lemma 1 should be presented as the classical two-subdivision identity, with a self-contained proof and citation, not as a new lemma in priority language. This paper is about stable sets and coloring; it contains no BSP terminal construction. [Poljak primary paper](https://dml.cz/bitstream/handle/10338.dmlcz/105554/CommentatMathUnivCarol_015-1974-2_9.pdf?sequence=2)

### Khachiyan et al. (2008): close tripartite spoke mechanism

Section 6, Theorem 11 and Claim 5, printed pp. 226–227, attach each part of a tripartite graph to a different one of u1,u2,u3 on a single s–t path. All spokes and original graph edges have traversal length 0; the two internal path edges have length 1. Three interior vertices are protected, vertices of the original graph are removed, and the objective distinguishes residual s–t distance 2 from 0/1. Sections 7–8 remove protection and obtain bipartite instances without turning the theorem into unit-traversal triangle BSP. The edge counterpart uses additional splitting constructions.

This is an important antecedent deserving explicit methodological credit. Its stated theorem does not classify three unit-length terminal geodesic families with unrestricted edge deletion. That last correspondence is precisely the remaining step in the PR. The obvious one-pair shortest-geodesic specialization is polynomial, so simply treating this old distance threshold as “the initial distance plus one” is invalid. [Primary publisher PDF](https://link.springer.com/content/pdf/10.1007/s00224-007-9025-6.pdf)

### Baier et al. (2006/2010): length-bounded cut

The inspected full author manuscript's Theorem 3.11 proves edge-cut inapproximability for one terminal pair and length bound L≥4. Its construction hits paths up to an externally set threshold; it does not impose L=d_G(s,t). Theorem 3.13 explicitly says the one-pair problem with L equal to original distance is polynomial. Thus the hardness theorem is not an exact predecessor of triangle BSP. Removing the difference between threshold and original distance would contradict the stated polynomial special case. The ICALP 2006 full text has the same scope distinction. [Full primary author manuscript](https://kam.mff.cuni.cz/~kolman/papers/acmlcuts.pdf), [ICALP primary author PDF](https://page.math.tu-berlin.de/~skutella/ICALP06-final.pdf)

### Dvořák–Knop (2015 preprint / 2018 journal): all-pair bounded multicut

The inspected arXiv full text defines a length lower bound for every pair in a terminal set; it therefore includes the PR's instances, by setting all three required residual distances to 4. Theorems 4 and 7 give algorithms parameterized by treewidth, the length limit, and number of terminals. The hardness portions concern single-pair structural parameterization and use thresholds that grow in their constructions. There is no identified exact three-terminal distance-three hardness result in this inspected version. General bounded-multicut inclusion is not itself a hardness implication for the PR's restriction. The final journal PDF retrieval returned a security page, so no claim is made that the final version was completely inspected. [Primary arXiv full text](https://arxiv.org/pdf/1511.02801), [final journal DOI](https://doi.org/10.1007/s00453-018-0408-7)

### Lee (2016 preprint / 2017 ICALP): arbitrary-threshold interdiction

The inspected full preprint's Theorems 1.3–1.4 establish UGC-based hardness for single-pair short-path cut/interdiction for infinitely many values of the length target. Directed multicut is discussed separately. These theorems neither fix three undirected demand pairs forming a triangle nor restrict the hit family to original geodesics at distance 3. Threshold conventions also differ: Lee cuts paths of length strictly less than l. This is related hardness, not a preceding exact theorem. [Primary arXiv full text](https://arxiv.org/pdf/1607.05133), [published ICALP DOI](https://doi.org/10.4230/LIPIcs.ICALP.2017.92)

### Kuhnle–Crawford–Thai (2018): bounded multicut with many directed pairs

The primary paper's text was inspected through its author-uploaded full text; the ACM PDF endpoint returned 403. Section 2.2, Theorem 2.2, assumes T≥16 and reduces directed edge cycle transversal to directed length-bounded multicut. Its target pair set is {(v_out,v_in):v∈V(G)}, with a distinct pair for each source vertex. Neither demand number nor topology is the fixed triangle, and T is not constrained to the original distance. The detailed construction therefore does not establish the PR's restriction T=3. This source must not be excluded merely because its abstract says “multicut”; the exact theorem/construction differences are what exclude the inspected result. [Primary paper, author-uploaded full text](https://www.researchgate.net/publication/324235769_Network_Resilience_and_the_Length-Bounded_Multicut_Problem_Reaching_the_Dynamic_Billion-Scale_with_Guarantees), [publisher DOI](https://doi.org/10.1145/3179407)

### Miller et al. (2023): Force Path Cut

The primary author PDF's Theorem 3.1 proves APX-hardness for making a prescribed path the unique shortest path for one terminal pair, including unit costs and lengths. Its reduction attaches paths of length N and a prescribed path of length 2N−1 to a full three-terminal cut instance. It relies on destroying arbitrary original terminal connectivity. This is not hitting only the original distance-three geodesics of three demands. The prescribed path and its length threshold are extra input, and protection of its survival is part of the model. [Primary author PDF](https://salfeld.github.io/Pubs/TKDD2023.pdf)

## Bienstock–Diaz and later citation follow-ups

The verified bibliographic year is **1993**, not 1992: SIAM J. Comput. 22(3), 482–499; the publisher records acceptance in January 1992. The primary publisher abstract concerns selecting protected edges that meet small cuts, not deleting shortest paths. Krause expressly attributes the general BSP proposal to this paper. Full text could not be retrieved (403), so the “related problems” portion is not independently excluded. Cite original proposal through Krause unless that text is obtained. [Primary publisher record](https://epubs.siam.org/doi/10.1137/0222034)

OpenAlex's exact-title thesis record W2147325817 reports zero citing works. Its Bienstock–Diaz DOI record W2082296423 reports four: Krause (2006); Goemans et al. (1994), network design; Zhang–Modiano–Hay (2017), shielding; and Tao et al. (2026), region-based shielding. These counts are conspicuously sparse and are explicitly **not** interpreted as completeness. Public title/DOI lists and query endpoints are saved in CITING_KRAUSE.json and CITING_BIENSTOCK.json. No full third-party text is in public artifacts.

The 2017 shielding full primary author text was inspected. Its definition chooses edges made immune to failure and seeks connectivity after bounded failures; it does not delete original terminal geodesics. [Primary author full text](https://jianan-z.github.io/papers/shieldingFull4.pdf)

The 1994 network-design source has an inspected primary author bibliographic record, but its Cornell repository PDF was not retrieved; it is not claimed to have been fully ruled out. [Primary author publication record](https://davidpwilliamson.net/work/publication/goemans-gpstw-94/)

The 2026 shielding article's publisher DOI was inaccessible; secondary indexing describes region-based connectivity and protection, but this is only a triage lead, not an independently checked mathematical exclusion. Its full text remains a stated access gap. [Publisher DOI](https://doi.org/10.1109/TON.2026.3665595)

A recent primary 2024 blocker/interdiction research manuscript was also inspected at Chapter 3, §§3.1–3.1.1. Its shortest-path blocker model is single-pair vertex removal in directed graphs with general lengths and prescribed threshold. It does not state the exact target theorem and cites Khachiyan et al. for the model. [Primary arXiv manuscript](https://arxiv.org/pdf/2412.08256)

## Mechanism ledger and exact gaps

| Family | Mechanism checked | Evidence/status | Exact gap to target |
| --- | --- | --- | --- |
| Historical BSP | Original-geodesic hitting, undirected demand triangle | Exact source match verified | No established continued-open status after 2006 |
| Subdivision VC | Two subdivisions per edge preserve cover optimum up to m | Classical antecedent verified; attribution repair required | Does not introduce terminal demands |
| Tripartite interdiction | Attach three color classes to three internal path vertices | Close construction antecedent verified; cite it | One pair, 0/1 lengths, vertex removal, prescribed target |
| Length-bounded cut | Delete paths up to a chosen length | Related theorem inspected; direct priority route blocked | Its hard threshold is not original geodesic length |
| Bounded multicut | All-pair residual lower bounds | Includes target model, but inclusion alone insufficient | No identified hardness for distance-three fixed triangle |
| Multiway cut / Force Path | Destroy all original terminal connectivity | Different hit family; no valid direct implication | Longer routes need removal there but are allowed here |
| Cut shielding | Protect edges to survive failures | 2017 definition verified; 2026 access gap | Protecting cuts differs from deleting original geodesics |
| Citation indexes | Follow records citing historical works | Bounded search completed | Index coverage is incomplete |

No family is reopened by appealing to general hardness without an additional model-preserving construction. As a concrete distinction, intact four-edge backup routes are harmless for distance-three BSP but must be destroyed for full multiway disconnection.

## Required publication framing

1. Credit Poljak for the subdivision identity and Khachiyan et al. for the earlier tripartite attachment mechanism. Keep both proofs self-contained.
2. Cite Krause for the exact question and say it was left unresolved in those sources.
3. State the exact theorem decisively; avoid “first,” “previously unsolved through 2026,” or “priority cleared.”
4. Distinguish the theorem's verified mathematical proof from the bounded nature of its literature audit. Include extensive AI-use and unrefereed disclosure as required by the human user.

Suggested factual wording: “We give a direct proof that the undirected triangle case of Blocking Shortest Paths posed by Krause is NP-complete, even when all three original terminal distances are three and every edge has unit length and unit deletion cost. The subdivision identity is classical, and a related tripartite attachment was used earlier in shortest-path interdiction. We make no claim of first bibliographic priority.”

## Reproducibility and scope

Searches and retrievals were conducted 2026-10-12 PDT. QUERY_LOG.md records exact query strings and the citation API checks. SOURCE_MANIFEST.json records primary PDF retrieval URLs, UTC timestamps, SHA-256 hashes, and failed endpoints. PDFs, extracted source text, raw citation-index data, and rendered source pages are kept only in ignored private_sources/. This audit is independent of finite computation verification and does not replace the mathematical proof adversaries.
