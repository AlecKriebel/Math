# PR397: independent original-source and priority review

**Verdict: qualified PASS for source fidelity of the precise existence construction and for a bounded priority search.** I found no authenticated earlier occurrence of the exact cross-root random-demand model and joint outer-phase theorem in the inspected primary corpus. This is not a certificate of worldwide novelty, continued openness of a canonical problem, or mathematical correctness of every proof step. The fresh flow and probability reviewers have separate mathematical responsibilities. No other fresh review was read in producing this report.

The appropriate contribution is a rigorous, explicitly specialized example of the phenomenon motivating Aldous's conceptual request. It should not be promoted as the definitive or universally accepted resolution of the wider modeling program. The original packet's historical refusal to claim novelty does not establish that its construction is old. Conversely, this search does not justify broad first-discovery language.

## 1. Bound input and exact proposed contribution

The inputs are the 24 original files at PR397 head `3705c5102b58c48e29991c61771978bf756a62e7`, preserved by the root's `SOURCE_SNAPSHOT.json`. The independently rechecked input receipt binds every file by byte count, SHA256 and Git-blob identity. The PR's actual 25-path comparison also contains its own claimed_solved QUEUE edit. The root's initial live GWS CLI query on 21 October 2026 at 05:35:27 UTC found no matching row for the identifier, source alias, PR or congestion term. This review performs no spreadsheet or publication mutation.

The theorem under examination concerns the complete binary tree with `k` leaves on each root side, `k^2` cross-root commodities, cheapest fixed-topology doubled-demand capacities `C_e=2k k_e`, and fixed-law independent `X_ij~Exp(1)` with `d_ij(t)=1+(t-1)X_ij`. Its finite min-cut formula and right derivative are exact. With high probability, at all times below `2-delta_k` every optimizer has the entire physical tree spare, while above `2+delta_k` every optimizer saturates every physical edge; `delta_k=8 sqrt(log(k)/k)`. The resulting throughput limit is `min(t,2)`. The claim does not identify the exact critical scaling, the critical derivative, or an optimizer-independent critical spare graph.

## 2. Original problem and source fidelity

[Aldous's primary page](https://www.stat.berkeley.edu/~aldous/Research/OP/congestion.html) introduces maximum admitted simultaneous demand and its marginal response, then asks for an analytically tractable toy model exhibiting coincident marginal collapse and spare-edge fragmentation. It proposes cheapest capacity enlargement for doubled demand as one design scenario. The example of random growth with mean and variance linear in time is introduced permissively. The page dates the question to May 2003 and contains a February 2018 literature-status remark. That dated remark is not evidence that no relevant work appeared later.

[The primary index](https://www.stat.berkeley.edu/~aldous/Research/OP/index.html) classifies this item at 0.7 on its conceptual-to-technical scale, whose conceptual end concerns finding a useful precise mathematical formulation. The index warns that historical pages are retained and updates are incomplete. There is no unique theorem with a universal graph quantifier to certify as resolved.

My source-fidelity judgment is therefore conditional and precise: **the construction supplies an existence example with the requested two observables, assuming its stated mathematical proof passes independent verification.** Its exact phase theorem is a full theorem about its defined model. This is an adequate specialized response to the permissive existence reading of the primary page. It does not establish that the model is the uniquely “right” one, explain all networks, or finish a general research program.

The following qualifications are material rather than grounds for silently strengthening the source:

- Each finite network is fixed after design. The asymptotic theorem concerns a sequence of networks; it does not increase capacities during post-design traffic growth.
- The physical tree is sparse, but the OD demand set is dense. Terminal capacities grow as `2k`, and top-edge capacities as `2k^2`. A claim of fixed per-terminal resources would be false.
- Affine random slopes give variance `(t-1)^2`, not the primary page's illustrative linear-variance process. This specialization must be stated.
- Exact `r_k=1` below the window uses normalization by the actual offered slope `S_k`. With the deterministic initial-total denominator `k^2`, the finite value is `S_k/k^2`; its limit remains one. Both conventions give zero in the saturated outer phase.
- The phase transition is a statement about a marginal derivative. Total admitted throughput increases and then saturates; it does not collapse to zero.
- The proof gives an upper bound for a transition window. It does not prove an optimal critical exponent or a limiting critical curve.
- “Every optimizer” is supported only in the two outer phases. No critical-region invariant spare graph should be inferred.

### Additional primary context supplied during this review

[Aldous's June 2005 Ottawa talk](https://www.stat.berkeley.edu/~aldous/Talks/Ottawa.pdf), slides 4–6, explicitly contrasts an easy but unrealistic tree analysis with preferred mean-field models. The rest of the 21-slide talk develops layered-network, random-distance and oriented-lattice examples, not the present cross-root HOT construction or joint shrinking-window theorem. This source should be acknowledged in contextual discussion: the paper offers a tractable tree example, not the broader rerouting model the talk prefers.

[Bhamidi's 2022 interview with Aldous](https://doi.org/10.1214/22-STS849), printed 617, advocates studying qualitative process behavior on general networks. The relevant discussion does not state a congestion theorem or formal admissibility restriction. It reinforces a limitation of explanatory scope, without making the candidate's existence theorem false. Neither source authenticates an earlier exact joint-observable example.

## 3. The two closest random-transport antecedents

### Hassin–Zemel: actual 1988 published theorem

The complete [author-hosted final paper](https://www.tau.ac.il/~hassin/transportation_88.pdf), *Mathematics of Operations Research* 13(1), 80–89 (1988), was read, including its proofs and bibliography. Printed 81–82 were visually checked against OCR. Theorem 1 requires exponent separation

`gamma > alpha+beta+chi`, with `chi=max(0,2 epsilon/3,(beta+epsilon)/2)`.

The natural candidate transportation problem, after dividing flows and capacities by two, has row and column totals `k`, total mass `k^2`, and `k` rows/columns. The exponents are `(alpha,beta,gamma,delta,epsilon)=(1,1,2,1,1)`, giving `chi=1`; the strict condition would be `2>3`. Thus this theorem is not a direct proof of the candidate's near-capacity regime. The max-flow application in Theorem 2 has a different complete/random graph topology and bounded terminal capacities. It does not assert the physical spare-tree conclusion. The old work must be credited, but these actual hypotheses do not establish an exact duplicate. [Published DOI](https://doi.org/10.1287/moor.13.1.80).

### Karp–Motwani–Nisan: edition-qualified comparison

I read the actual [December 1988 Berkeley report CSD-88-392](https://www2.eecs.berkeley.edu/Pubs/TechRpts/1988/CSD-88-392.pdf), including its probabilistic formulations, directed/undirected transport theorems, max-flow applications, and further-work section. Its directed theorem fixes bounded integer capacity support `K`, positive mean surplus `epsilon`, and a fixed realizability parameter. Section 5 specifically identifies growing `K(n)` and vanishing `epsilon(n)` as extensions to study. Those fixed-parameter hypotheses do not directly give the stated vanishing-window result for continuous unbounded capacities. The candidate's optimization reduction uses classical transport mathematics and cannot claim that mechanism as new.

The [1993 publisher record](https://doi.org/10.1287/moor.18.1.71) authenticates the journal publication, 18(1), 71–97. The final journal body was unavailable: the direct public PDF request returned HTTP403. This report does **not** equate the 1988 report with a verified final edition or rule out a relevant change in that edition. That is an explicit bounded-search limitation.

`PRIOR_THEOREM_COMPARISON.md` gives independently checkable nonapplication calculations and their limits. They refute particular overbroad equivalence inferences; they do not prove that every possible derivation from old literature is impossible.

## 4. Other close primary sources

| Primary source actually inspected | Mechanism and comparison with the exact candidate |
|---|---|
| [Aldous–McDiarmid–Scott, 2009](https://www.stat.berkeley.edu/~aldous/Papers/me122.pdf), actual journal-layout body, main theorem and constructions | Maximum **uniform** flow on a complete graph with random edge capacities; the limiting value depends on the capacity law and one/two-hop rerouting. Different objective, topology and randomness; no HOT design followed by the candidate's marginal/spare-tree theorem. |
| [Khandwawala–Sundaresan, author preprint dated 1 October 2009](https://ece.iisc.ac.in/~rajeshs/reprints/201003JAPpreprint_KhaSun.pdf), definitions, main results and linear-utility theorem; journal publication 2010 | Concave utility of simultaneous complete-graph commodity flows under random edge capacities. Even its linear-utility result is not a capped offered-demand derivative or a physical spare-edge transition. The final journal body was not separately compared. |
| [Carlson–Doyle, *Complexity and robustness*, 2002](https://pmc.ncbi.nlm.nih.gov/articles/PMC128573/), HOT/SOC and forest-fire sections | Prior design/robustness paradigm, optimized forest firebreaks and fragile responses. This is important historical context, not an occurrence of the candidate's bipartite demand formula and joint theorem. HOT itself is old. |
| [Moreno–Pastor-Satorras–Vázquez–Vespignani, arXiv v1, 2002](https://arxiv.org/abs/cond-mat/0209474), actual four-page body and model variants | Congested failures redistribute load and trigger cascades on scale-free networks. Its fragmentation phenomenon predates this candidate, but its dynamic failure mechanism is not simultaneous maximum admitted demand under frozen tree capacities. Journal DOI: [10.1209/epl/i2003-00140-7](https://doi.org/10.1209/epl/i2003-00140-7). |
| [Hamedmoghadam et al., 2021](https://doi.org/10.1038/s41467-021-21483-y), complete archival XML; unaffected-demand and reliability definitions | Thresholding observed edge quality unpacks connectivity and demand within a snapshot. “Unaffected demand” is a reachability quantity, not the constrained maximum-admitted-flow objective or its marginal derivative. |
| [Di Meco et al., arXiv v1, 2024](https://arxiv.org/html/2405.16100v1), node-dynamics definitions, stationary analysis and congestion/percolation section | Random-walk/node-occupation traffic, analytic stationary approximations and numerical congested-cluster behavior. It establishes related prior modeling, not the candidate's static exact max-flow identity and all-optimizer outer phases. |
| [Kim–Radicchi, 2024 published PRL](https://homes.luddy.indiana.edu/filiradi/Mypapers/PhysRevLett.133.047402.pdf), actual published model/algorithm, parameters, finite-size analysis and conclusions | Sequential OD requests consume all edges of a shortest path, with a path-length budget. Fragmentation is closely related conceptually, but no simultaneous optimal admitted matrix, doubled-demand capacity design, or candidate right-derivative theorem occurs. Publication: 26 July 2024, DOI [10.1103/PhysRevLett.133.047402](https://doi.org/10.1103/PhysRevLett.133.047402). |
| [Lampo et al., 2021 publisher body](https://doi.org/10.1007/s41109-021-00383-6), graph construction and congestion-onset definitions | A Delaunay core/MST periphery and a critical injection rate determined by maximum betweenness; transitions concern congestion **location** as spatial regions grow. This related tree/backbone work is not the candidate's joint marginal/fragmentation theorem. |
| [Kwok–Lau–Ramachandran, 2021 published SIAM body](https://cs.uwaterloo.ca/~lapchi/papers/spectral-scaling.pdf), Theorems1.5/1.7, §4.1.4–5 and AppendixB.7 | Near-balanced random matrices can be scaled with controlled diagonal factors. This is another established route toward regular flow feasibility. The stated near-identity estimates have an extra logarithmic factor; no exact HOT application or the candidate's particular window was located. No claim that matrix scaling or random near-regular feasibility is new is warranted. |

These comparisons are deliberately about actual mathematical objects and conclusions. Mere overlap in congestion, abrupt fragmentation, trees, or random transportation is not result identity. Equally, the manuscript should not claim to introduce those broader phenomena.

## 5. Publication and external-corpus checks

- The complete current [EulerSolve papers index](https://eulersolve.org/papers/) was downloaded. Exact source alias, numeric identifier, percolation-fragmentation and binary-tree terms have no target entry. The congestion hit is a different bounded-congestion fare-zone problem. This is an index coverage check, not an examination of every unrelated paper's full text or a claim about all external repositories.
- The recorded web searches include exact identifiers, the primary problem's terminology, source/author combinations, physical spare edges, random transportation and equivalent matrix-scaling vocabulary. No authenticated exact earlier construction/application emerged from the inspected primary sources.
- Public Zenodo searches are separately recorded with their result counts and limits. Initial requests using unauthenticated page size100 returned a validation error; the documented maximum25 was used for read-only corrected requests. No failed request is treated as negative publication evidence. Public search is not complete authenticated deposit/draft enumeration.
- The root must repeat live spreadsheet, DOI, local publication-package and complete own-account/draft checks immediately before any upload/append. This review authorizes no publication action.

## 6. Required manuscript qualifications and remaining limits

The manuscript should lead with a precise model theorem and a modest interpretation: an analytically tractable designed-tree example of the coincident phenomenon discussed by Aldous. Retain dense OD growth, increasing terminal capacities, quadratic variance, actual-slope normalization, the two outer phases and the upper-bound status of the window. Credit classical max-flow/min-cut, Chernoff bounds, random transportation, HOT, existing congestion/percolation modeling, and Aldous's earlier reservations about tree realism.

Suitable scope wording is: “We give a rigorous specialized example motivated by Aldous's toy-model question.” A claim to have found the canonical model, to have solved general network congestion, to have established the first occurrence of a congestion-fragmentation transition, or to have exhausted the historical literature is unsupported.

No exact earlier equivalent mathematical result was authenticated in this bounded review. The final KMN journal body, unpublished work, incomplete indexing, and uninspected versions remain coverage limits. These limits are not converted into either a global novelty certificate or a categorical priority failure. A concise note can describe the exact construction as its contribution, with a dated bounded-search statement. Any later authenticated exact predecessor would require reconciliation rather than a second novelty claim.

No outside individuals were contacted; no outreach was prepared. No PR, spreadsheet, Zenodo record, Git ref, branch or index was changed. All downloaded third-party bodies and rendered pages remain in the ignored private source directory; only evidence summaries and hashes belong in a public checkpoint.
