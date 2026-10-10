# Independent adversarial audit: chip-firing reachability

## Decision and exact scope

**ACCEPTED: complete mathematical proof of polynomial-time many-one coNP-hardness.** Combining the accepted reduction with the cited membership theorem yields coNP-completeness for legal reachability on finite loopless strongly connected directed multigraphs, represented by binary adjacency entries, with nonnegative binary-encoded initial and target configurations.

This decision applies to the complete proof in the distributed mathematical report:

- Report: [MATHEMATICAL_REPORT.md](MATHEMATICAL_REPORT.md)
- Bytes: 9,455
- SHA-256: `46f0c5c582e5775cd05628fa6dc67ede0a2f550248b84403a51bf621cbc5844c`
- Audit date: 2026-10-10 UTC

The public report preserves the full accepted argument. Editorial changes update its title and acceptance wording; no mathematical proof correction was required. This audit is AI-assisted and unrefereed. It is not external human peer review, journal acceptance, or formal proof-assistant certification.

No unresolved mathematical gap was found. This is a substantive many-one reduction, rather than a restatement of the earlier polynomial-hierarchy consequence. Acceptance does not establish first-in-literature priority and does not extend the result to simple graphs or unary edge lists.

## 1. Source-language verification

Farrell and Levine's *CoEulerian graphs*, arXiv:1502.04690v3, defines its halting problem on PDF page 2 for nonnegative configurations on strongly connected adjacency-matrix multigraphs. Loops are allowed. Corollary 3.2 on page 11 states NP-completeness; the immediately preceding proof explicitly identifies a polynomial-time Karp reduction. Page 10 analyzes description length logarithmically in edge multiplicities. These are the conventions required here. The underlying lattice argument can produce a signed intermediate configuration, but the report's optional normalization supplies an exact bridge; its validity is checked below. [Primary source](https://arxiv.org/pdf/1502.04690v3)

Hujter, Kiss, and Tóthmérész's *On the complexity of the chip-firing reachability problem*, arXiv:1507.03209v4, page 2 specifies loopless multigraphs and adjacency encoding whose length depends on logarithms of multiplicities. Page 3 defines configurations to be nonnegative. Theorem 12, pages 8–9, proves coNP membership for precisely this reachability model. Restricting to strongly connected valid inputs preserves membership because validity is polynomial-time testable. Their Theorem 1 on page 3 supplies the halting dichotomy used by the report. [Primary source](https://arxiv.org/pdf/1507.03209v4)

During the independent audit, both PDFs were retrieved and their recorded byte counts and SHA-256 hashes matched those recorded during proof review. The problem definitions, source hardness argument, target membership proof, and relevant preliminary results were read. The cited pages were also visually checked; additional rendered pages confirmed the graph and configuration conventions. [SOURCE_METADATA.json](SOURCE_METADATA.json) records these historical observations. Edition preparation performed no new scholarly-source retrieval, source-file rehash, page inspection, or literature search.

## 2. Source preprocessing survives adversarial cases

### Signed configurations

Given a signed configuration x, add k_v=max(0,-x_v) loops at each vertex v and add k_v chips there. The loop additions leave the net firing matrix unchanged. After any common firing word, transformed and original counts differ by the fixed vector k, while transformed and original firing thresholds also differ by k. Legality is therefore equivalent at each step, not merely at initialization. Stable configurations and infinite legal words correspond. The transformed initial configuration is nonnegative. All additions have polynomial bit length.

This argument is robust to existing loops and to a vertex whose original chip count is negative. It avoids depending on any unstated nonnegativity property of an intermediate lattice representative.

### Removing loops

Replace ell_v positive loops at v by a fresh relay r_v with ell_v parallel edges in each direction between v and r_v, initially empty. The old vertex retains its firing threshold. An original firing can be lifted by firing its relay immediately afterward; this exactly replaces the immediate self-loop returns.

Conversely, let t_v and s_v be old-vertex and relay firing counts in an arbitrary expanded legal word. The relay holds ell_v(t_v-s_v), so s_v<=t_v. The corresponding original configuration exceeds the expanded old-vertex configuration at v by precisely this nonnegative pending-return amount. Every projected old-vertex firing is thus legal. If the expanded word is infinite, its old-vertex subsequence is infinite because each relay count is bounded by its associated old count. Thus nonhalting, and by dichotomy halting, is preserved in both directions. Strong connectivity survives and at most one vertex is added per original vertex.

The explicit one-vertex preprocessing is also correct: with ell loops the chip count never changes, and a firing is legal exactly at count at least ell. This includes ell=0. Replacing such inputs by fixed two-cycle YES/NO examples avoids zero outdegrees in the principal construction.

## 3. Independent derivation of the reduction

Let A be the loopless source adjacency matrix, x>=0, n>=2, C=sum(x), and D the maximum source outdegree. Set

N=(C+1)^n, M=N+1, B=N(MD+1).

All legal source states remain nonnegative and conserve C. At most N states exist. A legal word of length N visits N+1 states and repeats one; the intervening nonempty word can be repeated indefinitely. The halting dichotomy rules out a terminating alternative. Conversely, nonhalting supplies a length-N legal prefix. The cutoff is valid even when its bound is very loose. At C=0 it gives N=1, and the source has no legal move because outdegrees are positive.

In the constructed graph H, each old vertex has threshold Md_v+1. The gate threshold is nB+1, and the marker threshold is 1. All arcs are nonnegative integers, no loops are introduced, and the gate directly links every old vertex. The marker has reciprocal edges with the gate. Hence H is strongly connected.

Before the first gate firing, the marker is zero and cannot fire. After t total old firings, with individual counts t_v and projected source state z, direct subtraction of firing updates gives

H_v = M z_v + N - t_v,
H_g = nB+1-N+t,
H_m = 0.

For t<N, the remainder N-t_v lies between 1 and N=M-1. This gives a clean integer separation:

- z_v>=d_v implies H_v>=Md_v+1;
- z_v<=d_v-1 implies H_v<=M(d_v-1)+N=Md_v-1.

Therefore old-vertex legality agrees exactly at every step of the first N firings, inductively for every possible legal choice. The gate is illegal before N old firings and exactly at threshold after N. There is no simultaneous-firing convention or fairness assumption hidden here.

### Forward direction and cleanup

If the source is nonhalting, lift a length-N source prefix and then fire the gate once. For each old v, t_v<=N and z_v>=0; consequently its pre-gate count Mz_v+N-t_v is nonnegative. It receives B, leaving at least B chips.

It remains to fire v exactly N-t_v times. At any point before its next such firing, at most N-1 of its cleanup firings have occurred, so even discarding all later incoming chips, the budget B>=N(Md_v+1) covers that firing. This argument works for any cleanup order, including blockwise cleanup, and when t_v=N no further firing is requested. The marker and gate may be legal during cleanup but need not be fired. Reachability allows the legal game to stop at its target.

The resulting total firing counts are f_old=N, f_gate=1, f_marker=0. Direct multiplication gives

Y_v = Mx_v + MN(i_v-d_v) + B,
Y_g = (n-1)N,
Y_m = 1.

These formulas agree with the report's Laplacian orientation. Both X and Y conserve the same total, namely MC+(n-1)N+nB+1. Nonnegativity is unconditional: X_g=nB+1-N>=1 and Y_v>=B-MND=N. The marker coordinates ensure X!=Y.

### Reverse direction under arbitrary firing counts

For any legal target-reaching word, let k_g,k_m be its gate and marker counts. The marker equation is k_g-k_m=1, so k_g>=1. This does not assume the word has the designated firing vector f; extra gate firings, marker firings, or full period-vector additions do not evade the argument.

Take the first gate firing. The marker cannot previously have fired because it starts at zero and receives chips only from that gate. The gate therefore needs at least N previous old firings. Their first N moves are exactly source-legal by the preceding induction. The finite cutoff proves source nonhalting. Delaying the first gate beyond its earliest legal time causes no difficulty: the argument uses only the first N preceding old firings.

Thus the exact YES equivalence is NONHALTING(G,x) iff REACHABLE(H,X,Y). No assumption about a unique odometer, recurrent target, or polynomial-time simulation is needed.

## 4. Polynomial-time boundary

Let s be the binary source description length. The values n, the bit lengths of C+1, and the bit length of D are polynomially bounded by s. Exponentiation to N requires polynomially many operations on integers of bit length O(n log(C+1)+1). M, B, every adjacency entry, and every X/Y coordinate also have polynomial bit length. H has n+2 vertices after preprocessing; the relay preprocessing at most doubles the original vertex count. Integer powers, additions, and products can all be computed in polynomial bit time.

As usual, the report's logarithmic estimates should be read as bit-length estimates, with a constant term when N=1; that edge case does not affect the algorithm or theorem. No expansion of B or M into individual edges is performed. This is why binary adjacency encoding is essential to the stated result. The reduction does not prove hardness for simple graphs, unary multiplicities, bounded degrees, or bounded total chip count.

## 5. Recorded supporting checks

The independent audit records separately implemented exact-integer checks. The following aggregate coverage and outcomes are supporting metadata; programs and raw generated outputs are not distributed. The written analytic proof is independent of every omitted executable.

- 400 two-vertex instances: both directed multiplicities independently range from 1 to 4, and both chip coordinates range from 0 to 4. There are 150 halting and 250 nonhalting instances.
- 486 three-vertex instances: all 18 strongly connected loopless simple directed graphs on three labeled vertices, with every initial coordinate from 0 to 2.
- Source classification explores the entire reachable state graph, testing both reachable stable states and reachable directed cycles. Their dichotomy agrees in every case.
- Every nonhalting test is lifted through N firings, checking exact old-vertex legality at every step, then gate activation and varied-order cleanup to Y. For every halting test, an unrestricted target BFS exhausts the reachable target states and rejects Y.
- An additional explicit list of 36 unrestricted target BFS cases includes positive and negative cases, permits arbitrary gate/marker counts, and uses no prescribed-odometer theorem.
- 1,308 signed source instances, with one or two vertices and all adjacency entries from 0 to 2, positive outdegrees, and coordinates from -2 to 3. Exact threshold/update conjugacy, nonhalting preservation after normalization, and preservation after relay removal all pass.
- Two negative controls deliberately break the construction. Taking M=1 admits a target from a halting source; unlocking the gate one move too early also admits a target from a halting source. Both defects are detected.

The recorded result is PASS. Finite tests supplement the proof; they do not establish its universal correctness or complexity classification. Edition preparation did not rerun these mathematical checks.

## 6. Prior-result and novelty boundary

Tóthmérész's *Rotor-routing reachability is easy, chip-firing reachability is hard*, arXiv:2102.11970v2, Theorem 2.3, gives a collapse consequence if strongly connected reachability were polynomial-time decidable. Its argument proceeds through recurrence and certificates for nonhalting; it does not supply the gate/marker many-one reduction accepted here. The relevant proof and theorem were checked directly. [Primary source](https://arxiv.org/pdf/2102.11970v2)

The Egres question explicitly asks for coNP-hardness of general directed reachability. Its survey permits signed configurations, but the nonnegative subclass established here already answers that hardness question. The fetched problem page bears a 2016 modification date, so its open label is not evidence that no subsequent paper exists. [Exact problem](https://lemon.cs.elte.hu/egres/open/Complexity_of_the_chip-firing_reachability_problem_for_general_digraphs) [Conventions](https://lemon.cs.elte.hu/egres/open/Chip-firing)

A bounded search on 2026-10-10 for chip-firing reachability coNP-completeness/coNP-hardness and recent complexity results, together with inspection of the relevant author's public publication list, found no competing many-one result. This is an incomplete literature check, not a priority certificate. [Author publication list](https://tmlilla.web.elte.hu/talks/papers.html)

## Final acceptance

The distributed report is mathematically complete for its expressly stated binary-multigraph/nonnegative language. Source hardness, loop removal, optional signed normalization, both reduction directions, arbitrary target-reaching firing words, and polynomial output size have all been checked. CoNP membership matches this exact language. No additional lemma is required to conclude coNP-completeness within that scope.
