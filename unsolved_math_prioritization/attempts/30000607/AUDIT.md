# Problem 30000607: near-perfect matching codegree threshold

Authored edition: 11 October 2026 (UTC). OWR-1386-014.

AI-assisted, unrefereed authored reconstruction and editorial acceptance. This edition is based on one source/proof reconstruction plus an internal AI review of its three reports; it does not claim a second independent mathematical audit, external human peer review, or formal proof-assistant certification. It is not a computational reproduction package.

## Disposition

**PRIOR RESULT AUDITED; LITERAL ALL-n TARGET NOT CLOSED.**

Jie Han's arXiv:1404.1136v3 proves the sharp threshold for each fixed integer k ≥ 3 and all sufficiently large nondivisible n. This is an existing theorem, not a discovery of this audit. Its proof survives the detailed audit below, with explicit repairs to two displayed inequalities in the extremal argument and explicit justification of its dependencies. Neither the theorem nor its corollary establishes the corpus's unrestricted statement for every n ≥ k ≥ 2.

The lower bound holds for every permitted (n,k). The graph case holds for every n. A separately recorded substantive finite-n attempt establishes the trivial one-edge range and the two-edge endpoint cases n = 3k−2 and n = 3k−1. It does not settle the remaining finite range. The diagnostic MILP searches are not proof certificates and do not reduce that remainder.

Acceptance is therefore split: the existing sufficiently-large-n theorem passes this mathematical audit; mathematical acceptance of the full corpus target remains false. No novelty claim is made for any mathematical statement or proof here.

## 1. Exact target and conventions

The selected mathematical question is problem 30000607, OWR-1386-014. Let H be a finite simple k-uniform hypergraph on n vertices, n ≥ k ≥ 2. Its minimum codegree δ is the minimum number of edges containing S over **all** (k−1)-subsets S of the vertex set, including those contained in no edge. Let ν(H) be the maximum number of pairwise vertex-disjoint edges. Set q = floor(n/k) and r = n−kq.

The target asks whether t_k(n) = q whenever 1 ≤ r ≤ k−1, where t_k(n) is the least integer forcing ν(H) = q. This is an all-n assertion with variable k. It is not the partite problem, a positive-codegree problem, a lower-d-degree problem, or a fractional matching problem. A separate divisible-n decision-complexity question is outside this selected target and is not claimed solved here.

The original problem statement and available prior material were checked in the underlying reconstruction. This is not an exhaustive historical-literature or priority claim.

## 2. Authentication and source identity

The underlying source-inventory manifest SHA-256 is
23ce75bf727d96fb50eee788f263530323ad73ad41efcf7a1fa03d82e9c2e960.
The underlying reconstruction checked this exact pin and independently checked the byte count and SHA-256 of all 104 listed members, with no mismatches. This authenticates the listed members rather than claiming closure of the larger source collection. Source bodies and per-member source contents are not distributed in this edition; the separate closed reconstruction inventory and identities are summarized in VERIFICATION.json.

Primary sources used:

1. Official OWR 48/2006 report, DOI 10.4171/OWR/2006/48, https://ems.press/content/serial-article-files/46078. Relevant contribution: Andrzej Ruciński, “Hamilton cycles and perfect matchings in hypergraphs,” PDF pages 54–56, printed pages 2928–2930. PDF 636,348 bytes, SHA-256 71d0bbd6d20e5fa4e70e4b7c3cc09a8b46ae72c03ea335e607d59b8397c1cef2. The full report was retained, but unrelated contributions were not audited.
2. Jie Han, “Near Perfect Matchings in k-uniform Hypergraphs,” https://arxiv.org/abs/1404.1136v3 and https://arxiv.org/pdf/1404.1136v3. All eight PDF pages were read and rendered pages viewed. The fresh version-specific retrieval is byte-identical to the handoff PDF: 151,855 bytes, SHA-256 db2b9afd5e85eefeef0761514bb67201b9d3ebbed63959239dcaba148f347518. The arXiv record links the journal DOI 10.1017/S0963548314000613; the journal version itself was not retrieved or compared.
3. Rödl–Ruciński–Szemerédi, “Perfect matchings in large uniform hypergraphs with large minimum collective degree,” author-hosted article-in-press PDF at http://rucinski.home.amu.edu.pl/papers/89.pdf. DOI 10.1016/j.jcta.2008.10.002, eventually JCTA 116 (2009), 613–636. This exact file is an article-in-press proof with 24 PDF pages, not a verified byte copy of the final paginated issue: 437,593 bytes, SHA-256 d6747aa2a08e3453e17255504e0c456d1f4bae259d4173ac69bd72f34907e84d. Definition 1.1, Section 2, Facts 2.1–2.3 and their proofs, and the conjecture at the end of PDF page 5 were checked. HTTPS retrieval twice returned 502; the author's ordinary HTTP URL returned the PDF. No credentials or user data were sent.
4. Oleg Pikhurko, “Perfect Matchings and K_4^3-Tilings in Hypergraphs of Large Codegree,” Graphs and Combinatorics 24 (2008), 391–404, DOI 10.1007/s00373-008-0787-7. Author-hosted final paginated PDF: https://pikhurko.github.io/E/Pikhurko08gc.pdf. 209,264 bytes, SHA-256 2a2fea27a35843feca9995c4c4f15dfa98b5d7ebe2938bf20cc03d88b2946afc. Theorem 3, Lemma 1 and Corollary 1, and the proof of Theorem 3 were inspected. Unrelated tiling arguments were not fully audited.

### The two dates in Han's PDF

These are distinguishable metadata, not competing mathematical versions:

- The fresh official abstract page and PDF margin identify **v3, submitted 6 August 2014 at 14:46:47 UTC**.
- The PDF's first-page internal date is **13 August 2021**.
- The freshly retrieved version-specific TeX archive assigns the displayed date dynamically from the compilation date. The archive was only read as data; no TeX or author code was executed.
- The PDF metadata reports creation and modification on 13 August 2021. The source gzip header and tar member timestamps are in August 2014; HTTP last-modified values are separately retained and are not treated as submission dates.

The dynamic source date explains why a generated PDF can display its production date while retaining the 2014 arXiv version label. The evidence supports a 2021-produced PDF of official v3; it does not identify who initiated that production, its institutional cause, or any 2021 mathematical revision. None is guessed. The audit cites the official v3 identity and retains the internal date and metadata separately.

## 3. Original statement and intended scope

OWR PDF page 55 defines t_k(n) for all integers n ≥ k ≥ 2. Conjecture 4 then states the nondivisible equality without an additional large-n qualification. The immediately preceding divisible theorem does explicitly require sufficiently large n. The beginning of Ruciński's contribution on page 54 contains no blanket convention that silently restricts every subsequent n to be large. Thus the corpus's literal all-n reading has direct textual support.

The later RRS article likewise defines t(k,n) for all n ≥ k in Definition 1.1, and its conjecture at the bottom of PDF page 5 has no stated sufficiently-large-n restriction. Both sources develop asymptotic methods nearby. That context explains the emphasis of later work but cannot delete a quantifier from the selected target. We cannot infer the authors' private intent from the literature's use of “confirms” or “resolves.”

Han's Theorem 1.1 is unambiguous:
for each fixed k ≥ 3 there exists N(k) such that for every n ≥ N(k) with k not dividing n, δ ≥ floor(n/k) implies ν(H) = floor(n/k).
Neither a uniform bound independent of k nor a theorem for k growing arbitrarily with n follows. Corollary 1.3 has the same fixed-k, sufficiently-large-n limitation. The wording of an abstract or a later survey does not enlarge these quantified statements.

## 4. Exact lower bound and graph case

### 4.1 Space barrier, with the correct offset

For any integer d with 0 ≤ d < n/k, partition V = A ∪ B with |A| = d and let the edges be precisely the k-subsets meeting A. A (k−1)-set in B has exactly d extensions. A (k−1)-set meeting A has n−k+1 extensions, at least d. Such sets in B exist. Therefore δ = d. Every matching has at most d edges, since distinct edges must use distinct vertices of A. Conversely, there are at least (k−1)d vertices in B, so choose one distinct A vertex and k−1 distinct B vertices per edge to construct a d-matching. Hence ν = d, also for d = 0.

For the threshold lower bound take **d = q−1**, not d = q. Then δ = q−1 and ν = q−1 < q, so t_k(n) ≥ q for every n ≥ k. Taking |A| = q gives a q-matching and is not a counterexample to threshold q.

### 4.2 Graphs

Let k = 2 and δ(G) ≥ q = floor(n/2). If a maximum matching M had m < q edges, there would be at least two unmatched vertices u,v. No unmatched vertices are adjacent. For each matched edge xy, at most two of ux,uy,vx,vy can be edges: any three include a pair giving an augmenting replacement of xy by two disjoint edges. Thus deg(u)+deg(v) ≤ 2m < 2q, contrary to minimum degree. Therefore ν = q. Together with the space barrier this proves t_2(n) = floor(n/2) for all n ≥ 2, including every nondivisible n.

## 5. Proof architecture and dependency coverage

Han's Theorem 1.1 splits at a large independent set. A hypergraph is η-extremal when it contains an independent set of size at least (1−η)(k−1)n/k. The nonextremal result is Theorem 1.4, the extremal result is Theorem 1.5.

Choose the small ε from the extremal theorem, then γ = ε/(5k), and finally n large enough for both branches and γn ≥ 1. Since floor(n/k) ≥ n/k−γn, Theorem 1.4 applies when H is not ε-extremal; Theorem 1.5 applies otherwise. The order “fix k, choose constants, then choose n” is essential.

### 5.1 RRS Fact 2.1 / Han Theorem 1.2

This is an all-n auxiliary bound ν(H) ≥ min{q−k+2,δ}; a negative right side is harmless. Here is the proof in a form that makes the augmentation step explicit. If the positive minimum d were at least 2 and a maximum matching had at most d−1 edges, at least k(k−1) vertices would remain unmatched. Select k pairwise disjoint (k−1)-sets among them. Their neighbors all lie in matched edges. There are at least kδ incidences, so some matching edge has at least k+1 incidences with these k sets. The associated bipartite graph, with k vertices on each side, contains a two-edge matching: a bipartite graph with no two disjoint edges is a star and has at most k edges. Two disjoint incidences replace the old matching edge by two new edges, a contradiction. Cases d ≤ 1 are immediate.

This bound is not itself the desired near-perfect result for k ≥ 3: q−k+2 falls short of q.

### 5.2 Absorption: audited statement and constant amplification

RRS Facts 2.2–2.3, checked in their source, establish the absorption device that Han uses. For a (k+1)-set S, an absorbing edge e disjoint from S can be replaced by two disjoint edges covering S and all but one vertex of e. Thus each use reduces the uncovered vertex count by exactly k.

For completeness the needed amplification to any fixed number L of available absorbers follows directly. Fix a partition S = S_1 ∪ S_2 of sizes k−1 and 2. Choose distinct outside vertices v_1,...,v_{k−3} freely. Choose v_{k−2} to complete S_2∪{v_1,...,v_{k−3}}, v_{k−1} to complete S_1, and v_k to complete {v_1,...,v_{k−1}}. With δ ≥ cn and fixed c>0, exclusion of previously used vertices leaves at least a constant times n choices at each constrained step. Dividing the ordered count by k! gives at least βn^k absorbing edges for some β>0 depending only on k,c. For example β = c^3/(2^k k!) works once n is sufficiently large and 0<c≤1.

Select every edge independently with probability p = C log(n)/n^k. The expected total size is at most C log(n)/k!, while the expected number of intersecting selected edge pairs is O(log(n)^2/n). For each S the absorber count is binomial with mean at least βC log n. Choose βC > 8(k+2). The usual binomial lower-tail estimate gives failure probability at most n^{−βC/8}; summing over at most n^{k+1} sets gives o(1). For large n the half-mean exceeds any prescribed fixed L. Markov's inequality simultaneously gives a selected matching of size at most C log n with positive probability. This proves Han's version with L = ceil(k/γ).

The standard binomial Chernoff bound, Markov's inequality and the union bound are the probabilistic foundations here. No uninspected RRS matching theorem is needed beyond these elementary estimates and the checked counting argument. RRS's much larger divisible-case proof is irrelevant to this dependency and was not audited.

### 5.3 Han Lemma 1.7: almost-perfect matching

Let M be maximum, U unmatched, and suppose |U| > k^2/γ. The nonextremality assumption is nonvacuous only for small γ; in the actual application γ < 1/(5k). Partition all but at most k−2 vertices of U into t disjoint (k−1)-sets A_i. Then t > k/γ.

Let D be the matched vertices adjacent to at least k of the A_i. A matching edge contains at most one D vertex, since two such vertices have distinct adjacent A_i and yield a two-edge augmentation. Counting incidences gives
 t(n/k−γn) ≤ |D|t + nk,
so |D| > (1/k−2γ)n.

Let V_D be the union of matching edges meeting D. Then |V_D\D| = (k−1)|D|. Non-2kγ-extremality gives an edge e_0 inside V_D\D. It meets between two and k original matching edges. Each corresponding D vertex has at least k available A_i, so one can greedily assign distinct A_i to all of them. Replace those original edges by e_0 and these extensions. This increases the matching by one, contradiction. The argument is complete, including disjointness and the strict threshold. It does not make the conclusion near-perfect by itself.

### 5.4 Han Theorem 1.4: nonextremal branch

Reserve the absorbing matching M' of size at most C log n with c = 1/(2k), and let n' = n−k|M'|. For fixed γ and sufficiently large n, deleting at most kC log n vertices leaves minimum codegree at least (1/k−2γ)n'. A 4kγ-extremal independent set in the remainder would have size at least (1−5kγ)(k−1)n/k in H, contradiction. Apply the preceding lemma with parameter 2γ to leave at most k^2/(2γ) vertices uncovered.

While at least k+1 are uncovered, use an unused original absorbing edge. There are at most k/(2γ) such uses, fewer than the reserved k/γ absorbers for any current S. An unused original absorber remains an edge of the current matching, so it is disjoint from the current uncovered S even if earlier absorption exposed an old absorber vertex. Stop with at most k uncovered vertices. The count is congruent to n modulo k; since r is nonzero it is actually r < k. This proves the branch and identifies exactly where nondivisibility is used.

### 5.5 Extremal branch: two displayed errors and their repairs

The constructive partition and Steps 1–3 are valid after supplying the following bookkeeping repairs. Full replacement details are in the extremal reconstruction in PROOF.md.

**Repair A, PDF page 7, first display.** The inequality subtracting only |M_3| from |A| is not justified: an M_3 edge can contain several A vertices. Use instead the exact post-balancing identity
 m = |A_3'| = (n_3−r)/k = q−|M_1∪M_2|−|M_3| ≥ q−3αn,
where α = sqrt(ε). This is stronger than the lower bound the subsequent argument needs and does not charge a multi-A edge as a one-A edge.

**Repair B, PDF page 7, non-neighbor display.** The step |C| ≤ (k−1)n/k is not furnished by Proposition 3.2, which only gives |C| ≤ ceil((k−1)n/k). Keep the rounding, or simply use |C| ≤ n and m ≥ n/(2k). Then the number of missing crossing (k−1)-tuples at any surviving a is at most
 α binom(|C|,k−1) ≤ α c_k m^{k−1}, with c_k = (2k)^{k−1}/(k−1)!.
Taking ε smaller makes this just as useful. The proof does not require the specific constant printed in that display.

The earlier inequalities replacing n/k−q by a small εn are valid for sufficiently large n, for example n ≥ k/ε; they should not be used as all-n inequalities. The matching construction also needs a linear reserve of unused C vertices; this follows when α is chosen small before n is made large. These are genuine asymptotic choices, not finite-range coverage.

After repairs, the balanced k-partite remainder has both a high vertex degree in its A part and a high extension degree for crossing tuples from its C parts. This is precisely the input to Han's Theorem 3.1.

### 5.6 Pikhurko's dependency and an elementary replacement

The original Theorem 3 (PDF page 4 / printed 394) requires, for balanced parts of size m,
 δ_L m^{|L|} + δ_[k]\L m^{k−|L|} ≥ m^k + k sqrt(257 k m log m) m^{k−1},
with fixed k,L and sufficiently large m. For |L|=1 this follows from Han's 3m^k/2 condition once k sqrt(257 k m log m) ≤ m/2. Thus Han's cited special case is legitimate and asymptotic.

The proof of Pikhurko Theorem 3 was checked through its random bipartite matchings, the induction controlling accumulated errors, and the final Hall condition. Its Corollary 1 follows from its stated permutation concentration Lemma 1; that lemma is attributed to McDiarmid (2002), with Talagrand (1995) also cited. Those underlying papers were not independently retrieved or re-proved here. This is the explicit transitive dependency boundary for auditing the published route. Pikhurko's separate random-partition Proposition 2 and Corollary 2 are not dependencies of Theorem 3 and were not imported into the near-perfect proof.

The extremal reconstruction in PROOF.md additionally gives a complete elementary replacement tailored to the much denser remainder actually constructed by Han. It uses a second-moment bound for independent random permutations and Hall's theorem, rather than the full Pikhurko concentration theorem. Consequently the reconstructed extremal branch here does not need to assume the uninspected McDiarmid/Talagrand results. This is an audit reconstruction, not a claimed new theorem.

### 5.7 Corollary 1.3

Write δ=q−c. The all-n auxiliary bound handles c≥k−2. Theorem 1.1 handles c=0 when r>0. For 1≤c≤k−3, if r+c<k, add c universal vertices; the enlarged order is nondivisible with floor quotient q and codegree at least q. If r+c≥k, add c+1 universal vertices; its remainder is between 1 and k−3 and its floor quotient is q+1, with codegree at least q+1. Removing at most the number of added vertices' matching edges gives at least q−c edges in the original H. The new vertices may be used together, so “at most” is the correct loss estimate. These are applications of the large-n theorem to a slightly larger graph, not a way of lifting arbitrary small n beyond its threshold.

## 6. Finite-n partial coverage and precise remainder

The finite-n report in PROOF.md records the incomplete elementary approach to the uncovered literal target. The existing-theorem audit is not relabeled as a solution of that target.

Rigorously covered parameter families are:

- k=2, all n≥2;
- any k≥3, k<n<2k (q=1);
- any k≥3, n∈{3k−2,3k−1} (q=2);
- for each fixed k≥3, every nondivisible n≥N(k), for an appropriately sufficiently large N(k) supplied by the audited proof.

The uniform lower bound t_k(n)≥q holds on the entire target domain.

The part not established by this audit is exactly the following residual upper-bound family relative to these coverage statements:

 k≥3, n=kq+r, q≥2, 1≤r≤k−1, n<N(k),
 excluding the cases q=2 and r∈{k−2,k−1}.

Equivalently, the uncovered q=2 range has 1≤r≤k−3, and the uncovered q≥3 range has every nonzero remainder, whenever n lies below the sufficiently-large-n threshold. For k=3 the q=2 gap is empty. The paper does not provide a numerical N(k), and this audit does not claim an enumerated finite list or the smallest valid threshold. For each fixed k the residual range is finite; over unbounded k it is not a single finite set. “Uncovered here” is not an assertion that every such instance is currently open in the worldwide literature. Targeted searches found no authenticated all-n resolution, but were not an exhaustive literature census.

## 7. Evidentiary and distribution limits

No source-author mathematical code or TeX was executed in the underlying reconstruction. Its executed tools were authored finite checks, PDF text extraction, safe archive reads and rendering. This edition distributes complete authored mathematical arguments and bounded verification metadata. Source documents, source code, datasets, raw search output, and private coordination material are excluded.

The mathematical conclusions are supported by the written arguments, not by file hashes. Hashes establish retained-byte identity, not source authority, truth, priority or novelty. The full source PDFs were retrieved; actual passage-reading and rendered-page inspection scopes are recorded separately in SOURCES.json. The closed inventory and adversarial controls establish that missing, extra, modified and linked files or a modified manifest cannot silently pass the pinned verification workflow. They are not theorem-prover certificates.
