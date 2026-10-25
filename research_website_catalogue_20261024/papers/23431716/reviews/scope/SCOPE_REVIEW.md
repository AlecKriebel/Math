# Acquisition and scope review — Zenodo 23431716

**SCOPE_COMPLETE. Mathematical verdict: not assigned.** This report authenticates the release, reads and maps its claims, and checks the cited problem and theorem interfaces. It is not a correctness promotion, priority clearance or verifier replay.

## Identity, assets and coverage

The fresh public record identifies *A modular-storage proof of NP-completeness for chip-firing halting on simple digraphs*, Alec Kriebel, version 1.0, publication date 16 October 2026, DOI 10.5281/zenodo.23431716. It is explicitly classified as a preprint. The frozen reconciliation queue identifies this direct-paper record as the canonical edition of work Z-23431715, spreadsheet row 59.

Both public assets were freshly downloaded through their record file URLs, checked against API sizes and MD5 checksums, and independently SHA256 hashed:

| Asset | Bytes | MD5 | SHA256 |
|---|---:|---|---|
| `paper.pdf` | 83,409 | `94bc495c73b48a191d7c6ca61f67e1a5` | `52d4355533f5095be83c8799bd148e9927e5c4bef8c2f6a00d534303f0b7ee5c` |
| `pr1098_support_v1_0.zip` | 798,999 | `d965d2ea501f26b9f53fe27fabfd21bb` | `a9606c07600ca9ac60f36f5165c8c09ff3e0c0b42e83e50d006df6f1ee2723fe` |

These match the frozen queue's expected sizes/checksums; the main PDF also matches its expected SHA256. `sources/receipt.json` binds metadata, file URLs, bytes and every extracted ZIP member. All 124 regular ZIP members passed path/type checks, CRC reading and individual hashing. There are no nested archives and no additional PDF. The seven-page public main paper is the entire reader-PDF map. Unlike a named monorepo archive, this record has a real top-level PDF download; no embedded-member workaround is needed.

All seven main pages were read, including the whole proof, preprocessing cases, oriented construction, limitations and references. The current `CLAIM_SCOPE.json`, reproduction README, helper launcher and helper interfaces were read. The complete proof is in the main paper. Historical mathematical reports, acceptance records and review verdict bodies were left opaque; they are not needed to understand the self-contained current proof. The current manuscript source is `sources/published-source/paper.tex`. No archived paper was promoted as an additional publication.

Selected manuscript pages and the scan containing the original prime/clause construction were visually inspected to disambiguate formulas. The full original abstract is saved separately as `ORIGINAL_ABSTRACT.md`. `CONTENT_CANDIDATE.md` is conditional draft copy, not an approved page.

## Exact input model and output claim

The input is an explicitly represented finite directed graph with at least two vertices and a supplied vector of **nonnegative integer chips encoded in binary**. The graph is loopless, strongly connected, and simple in the directed sense: at most one arc for each ordered pair. The main class permits both `u→v` and `v→u`. The separately treated **oriented** class forbids such antiparallel pairs as well. A strongly connected oriented input necessarily has at least three vertices; the theorem's general `N>=2` convention introduces no two-vertex oriented example.

Every vertex follows the same ordinary rule: it may fire if it has at least its outdegree in chips, then sends one chip along every outgoing arc and loses exactly its outdegree. Total chip count is conserved. There is no dissipative sink, programmable threshold different from outdegree, weighted output, or changing rotor state. The distinguished root is an ordinary firing vertex, not a chip-deleting boundary.

HALTING means that **some finite legal firing word reaches a stable configuration**, where every coordinate is below its vertex's outdegree. Voluntarily stopping while a vertex remains active does not count. The paper invokes/proves least action to relate this existence question to arbitrary legal schedules; it does not assume fairness. It is not a target-configuration reachability problem and not the problem of whether a network halts on all possible inputs.

Theorem 1 claims **NP-completeness under deterministic polynomial-time many-one reductions**, including the oriented subclass. The hardness construction additionally supplies a specific root whose deletion leaves an acyclic graph containing **no directed path of two arcs**, and has a numerical total initial chip count polynomial in the explicit 3-CNF input length. Unary chip encoding therefore retains the stated hardness. The graph and chip coordinates may grow polynomially; the result does not impose bounded degree, planarity, a fixed graph, an Eulerian condition, a treewidth bound, or a numerical bound independent of input size.

## Claim and proof-interface map

### Least action and NP certificate — p. 2

For the column-action Laplacian, `Delta_(v,v)=d_v` and `Delta_(v,u)=−1` for an arc `u→v`, a count vector `f` sends `x` to `x−Delta f`. Lemma 1 says a nonnegative count vector with stable result bounds all legal firing words coordinatewise. The certificate used by the verifier includes the stronger range check `0 <= x−Delta f < d`. It need not encode a legal word explicitly.

The positive primitive kernel period comes from directed in-arborescence counts. In a simple `N`-vertex graph, the paper bounds its coordinates by `(N−1)^(N−1)`. For an actual terminating word some vertex fires fewer than its period count. A path-to-that-vertex argument with the essential additive-one slack gives

`f_u+1 <= (N−1)^(2N−2)`.

Thus each coordinate of the certificate has `O(N log N)` bits, independently of possibly enormous binary input chip magnitudes. The argument claims polynomial verification, **not polynomial firing time**. The special `N=2` two-cycle case is covered explicitly.

The paper identifies a missing slack term in one intermediate line of the Farrell–Levine preprint's membership discussion. It gives a three-vertex example to distinguish `f_u+1 <= d_v(f_v+1)` from the false stronger line `f_u <= d_v f_v`. This is presented as a local correction in a self-contained proof, not a disproof of the prior NP-membership theorem or a complete re-audit of that primary paper.

### Modular storage — p. 3

For `q>=2` and a **nonempty** allowed subset `A` of residues modulo `q`, use its periodic indicator `h`. The counter multiplicities are

`c_a=1+h(−a−1)−h(−a)`, for `0<=a<q`.

They lie in `{0,1,2}` and sum to `q`. The storage sum of those separate counters has the exact proposed identity

`S_A(k)=K_A+q h(k)`, `K_A=q(q−1)/2−|A|`.

Its maximum `B_A=K_A+q` is attained exactly at allowed residues. Empty `A` is excluded because it would invalidate this attained-maximum statement. Full `A` is permitted and gives constant storage. A negative constant `K_A` in a modulus-two boundary case is not a negative physical chip count. All actual counters begin with an offset in `0..q−1`.

The literal multiplicity formula is expressly credited to the parallel primed-toppler mechanism of Holroyd–Levine–Winkler. The new paper distinguishes that abstract processor construction from a conservative ordinary chip-firing implementation. It does not claim a new modular-counter identity.

### SAT predicates and total preprocessing — pp. 3–4, 6

Inputs are explicit 3-CNF encodings with clauses of length at most three. Malformed strings, repeated literals, tautologies, empty clauses and an empty conjunction are handled. Only variable identifiers actually appearing are relabelled; long binary identifiers or declarations of unused variables are not expanded. After preprocessing, nontrivial inputs have `n>=1`, with `O(L)` variables and clauses.

The construction uses the first `n` primes **starting at 3**. Variable banks allow `{0,1}` modulo their prime. Each clause bank uses the product of the primes for its one to three distinct variables and allows the CRT residues of its satisfying Boolean assignments: `2^t−1` choices, between one and seven. Joint satisfaction of all banks is equivalent to the Boolean formula's satisfaction. CRT supplies a nonnegative common integer when an assignment exists.

This is a complement presentation of Stockmeyer–Meyer's classical invalid-variable/failed-clause union, reconstructed by Gramlich. A local clause complement contains extra non-Boolean residues, but those are already excluded by the variable predicates. The paper does not claim a novel prime/Boolean/three-prime-product encoding or novel avoidance of expanding the global CRT period.

Using the cited prime estimate, the largest prime is bounded by `U<=3(n+1)^2`; each local modulus is at most `U^3`. The global product of all variable primes is a correctness witness only. It is not expanded into an exponentially large graph or traversed by the reduction algorithm.

### Physical simple graph — p. 4

Write `Q=sum_b q_b`, `P=max_b q_b`, and `B=sum_b B_b`. There are exactly `Q` distinct counter vertices, even when two have equal offsets. The main graph has one root, `P−1` return vertices, and arcs:

- root to every counter;
- each modulus-`q_b` counter to the root and to returns `t_1,...,t_(q_b−1)`;
- each return to the root.

The stated outdegrees are `Q`, `q_b` and one, respectively. It is loopless and simple but has root/counter antiparallel arcs. A largest-modulus bank reaches every return; all vertices reach the root and the root reaches the others. Removing the root leaves only counter-to-return arcs. Exact counts are `N=Q+P` and `|E|=Q+sum_b q_b^2+P−1`.

Returns start empty; counters start at their assigned offsets; the root starts with

`R=Q+B−1−S(0) >= Q−1 >=0`.

The conserved total is `C=Q+B−1`. Return vertices are ordinary degree-one vertices that send their chips back; they do not absorb chips. Numerical multiplicities in the bank become distinct vertices, not parallel arcs.

### Legal checkpoints and schedule implication — p. 5

The analysis chooses a legal order: fire the root once when legal, then all ready counters, then clear all returns before another root firing. At a checkpoint after `k` root firings, a counter's state is its offset plus `k`, reduced modulo its bank modulus; returns are empty; the root has `Q+B−1−S(k)` chips.

The proposed exact checkpoint equivalence is

`root stable <=> S(k)=B <=> every bank accepts k`.

A failed predicate creates a strictly positive storage deficit, so deficits cannot cancel. A satisfying assignment therefore gives a reachable stable checkpoint, unless the process already stopped at an earlier accepting checkpoint. An unsatisfiable formula produces an infinite legal word; least action rules out a terminating legal word under any other schedule. These phases are a proof device, not a modified firing rule or a polynomial-time simulation claim. The `k=0` accepting case is allowed.

### Polynomial bounds and oriented graph — pp. 5–6

With `H=O(L)`, `P<=U^3` and `Q<=HP`, the claimed construction has `N=O(HP)` and `|E|=O(HP^2)`, and the numerical chip total is also polynomial in `L`. Local residue enumeration and at most three-prime CRT computations are polynomial. The stable-capacity expression `(|E|−N)−C=sum_b[q_b(q_b−3)/2+|A_b|]` is nonnegative because the actual reduction uses moduli at least three. The capacity bound is an a-priori check, not a SAT algorithm.

The oriented version has `P` returns, omits counter-to-root arcs, and sends each counter to `q_b` distinct returns instead. Arcs follow the three-part cycle root–counter–return–root. The root and counter outdegrees, offsets, initial root mass and checkpoint equation are unchanged; the vertex and edge counts each increase by one. All conservation, legality and SAT claims are re-stated for this actual graph, not inferred merely by relabelling the main graph.

Preprocessing uses directed two-cycles for the main class and directed three-cycles for the oriented class, with zero chips for YES and one circulating chip for NO. Both cases preserve the appropriate strong-connectivity and root-deletion restrictions. The seven-page proof covers these totality cases explicitly.

## Fresh primary-source inspection

Ten primary PDFs were freshly fetched and hashed; all match the published bibliography ledger's stated PDF hashes. The raw files and text are under `cache/primary-sources`, with receipts in `primary_source_receipts.json`. These are raw sources, not another reviewer's conclusions. Exact reading scopes are in `primary_interfaces.json`; no source is represented as fully read unless it was.

- **Farrell–Levine, CoEulerian graphs, arXiv:1502.04690v3:** definitions, capacity, period/least-action context, membership passage and Section 3.1/Table 1 were inspected. Page 13 expressly distinguishes simple directed graphs from the binary multigraph hardness construction and poses the simple-graph hardness question. Page 10 contains the membership argument and intermediate inequality discussed by the present paper. The question is authenticated as historical, not certified to have remained open in October 2026. [Primary edition](https://arxiv.org/pdf/1502.04690v3).
- **Holroyd–Levine–Winkler, arXiv:1511.00422v2, Lemma 4.1 p. 15 and Section 8.3 p. 32:** the increments of a unary periodic-linear function determine multiplicities of parallel primed topplers. Substitution of `F(k)=k+h(0)−h(k)` gives the displayed bank priming; the source expressly distinguishes conservative sandpile nodes from nonconservative abstract splitters/topplers. [Primary edition](https://arxiv.org/pdf/1511.00422v2).
- **Stockmeyer–Meyer, STOC 1973 preliminary report, Theorem 6.1 and proof, retained PDF pp. 7–8:** inspected text and visual scan confirm the prime Boolean residues, invalid-residue union and clause products. [Primary scan](https://esp.mit.edu/download/827dcf47cbc9cf4a3b04dbf773ea54fb/M3175_meyer-stockmeyer-word-probs.pdf). **Gregor Gramlich alone**, MFCS 2003, Fact 3 on PDF pp. 5–6 reconstructs the same unary-automaton reduction. [Author manuscript](https://ggramlich.github.io/Publications/unaryMFCS03.pdf).
- **Farrell's 2014 thesis, Sections 1.1 and 4.1:** the root-last/nonroot-stabilization procedure and conserved-total comparison appear explicitly. Levine is the advisor, not a coauthor. [Author thesis](https://pi.math.cornell.edu/files/Research/SeniorTheses/farrellMatthewThesis.pdf).
- **Eriksson (1991):** all three pages read; its simple directed family has an exponentially long terminating game with linearly many initial chips. That historical phenomenon is separate from decision-problem NP-hardness. [Primary paper](https://www.ams.org/journals/proc/1991-112-04/S0002-9939-1991-1065944-3/S0002-9939-1991-1065944-3.pdf).
- **Dusart, arXiv:1002.0442v1, Eq. 4.2 and proof on p. 4:** the logarithmic prime estimate and `p_k<e k log k` corollary have the stated `k>=2` range, supporting the polynomial local-modulus bound. [Primary edition](https://arxiv.org/pdf/1002.0442v1).
- **Bond–Levine, Abelian networks II, Definition 6.5 and Corollary 6.6, pp. 17–18:** sandpilization preserves **halting on all inputs** under finite/local-irreducibility hypotheses. That statement is not a supplied-input reduction by itself. [Author manuscript](https://lionellevine.github.io/abelian-networks-II-halting.pdf).
- **Auger–Coucheney–Etse, actual 2026 journal PDF:** title page and pp. 39–40 confirm that Theorem 21 is legal reachability between specified rotor/chip configurations in generalized rotor multigraphs. It is not the identical decision interface as ordinary fixed-output halting. The complete 53-page construction was not re-audited here. [Journal PDF](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v33i2p5/pdf).
- **Esparza's sole-author survey:** selected pp. 31–32 distinguish conflict-free/free-choice 1-safe net hypotheses and several decision questions. Those passages do not establish a direct ordinary-chip-firing transfer. Garbled text extraction in formulas limits this inspection; no comprehensive weighted-net exclusion or theorem transfer is claimed. [Author survey](https://lsv.ens-paris-saclay.fr/~demri/Esparza98.pdf).

The primary mechanisms and historical question are therefore accurately delimited for the independent mathematical reviewers. The paper's full-result, simple/oriented realization and remaining-method priority stay **unknown**. This scope assignment did not inspect every potentially relevant weighted-net proof, conduct an exhaustive forward-citation search or establish immediate prepublication worldwide openness.

## Verification and status boundaries

The current package provides standard-library diagnostics through `code/run_checks.py` and `code/checks.py`. Their described coverage includes bank/antecedent substitutions, actual main/oriented graphs, legal conservation, small full successor graphs, tree periods, certificate slack and damaged variants. The launcher is stdout-only, and its guards use explicit exceptions. A separate `verify_kit.py` binds assets and historical workflow states. This scope reviewer read interfaces but did **not execute those checks**, rebuild the PDF or adopt their historical outcomes. Mathematical reviewers must test the proof and relevant executable claims independently.

Incidental status exposure was unavoidable in the fresh record metadata and current README, which recount prior internal acceptance, whole-package reviews and administrative publication holds; the current source-ledger schema/first entry also exposed one historical consequence summary. These are disclosed as author-supplied history and not evidence of a new mathematical verdict. Historical report/verdict/acceptance bodies, including those in `history/` and `terminal/evidence/`, were not read. The fresh publicly downloadable Zenodo record establishes present release existence; stale workflow fields must not be repeated as the current paper's publication state.

The strongest completed scope result is an authenticated seven-page preprint with the exact ordinary conservative model, both graph classes, restricted hardness and NP-certificate claims mapped against their cited sources. The remaining gate is independent mathematical review of the universal storage identity, graph dynamics, total reduction, polynomial bounds and NP-certificate argument. No mathematical promotion follows from this report.

Follow-up recommendation: **null**. Bounded-degree or other restricted-model questions would need a separate novelty and feasibility case; this report supplies none and recommends no speculative list. No website, spreadsheet, Git, deployment, UI or outreach action was performed.
