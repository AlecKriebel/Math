# PR 108 source, model, and complexity adversarial audit

Target: **30003996 / OWR-16633-013**, frozen submitted head **3526d46bf143b08e5055ffa7728c6278e9f958ea**. Verdict: **PASS for exact source scope and the stated strong NP-completeness theorem.** No substantive mathematical defect was found in this audit. Two small preprocessing clarifications improve presentation. Historical priority, current openness, and publication clearance remain unassessed.

The source reading was frozen at **2026-10-06T04:47:10.841159Z**, before candidate or old-review reading. `SOURCE_FREEZE.json` records the quantifiers and input hashes. The complete Kaibel contribution was read on printed pages 3014–3015, PDF pages 46–47, first from the PDF text and then from rendered pages. Old review conclusions and other proof families were not used to reach this verdict.

## Exact source model

[Kaibel, OWR 50/2018](https://doi.org/10.4171/owr/2018/50), Problem 1, supplies one undirected graph, both directed copies of each undirected edge, and an entire independently specified real coefficient vector for every vertex root. The solution is one common undirected spanning tree. Its induced rooted orientations determine all root costs; each root's cost sums coefficients over the entire rooted tree. Thus there are exactly N(N−1) selected root/arc pairs for every feasible tree on N vertices.

The reduction uses precisely this model. It does not select independent minimum arborescences. Its clause-root vector is evaluated on every arc, even though the structural lemma proves that only one possibly nonzero coefficient is selected. The remaining roots are still included in the input and objective; their vectors happen to vanish. A connected simple graph and nonnegative integer coefficients are permitted restrictions inside the source's more general graph/real-coefficient model.

The source does not explicitly spell out inward versus outward orientation. The candidate fixes outward orientation. For inward convention define c'_r(u,v)=c_r(v,u). Every outward induced orientation reverses to the inward induced orientation of the same T, and the transposed objective is identical for every T. This handles the convention without modifying the source problem.

The entire neighboring Problem 2 was checked. It instead has a directed graph, a single fixed root, destination-specific vectors, and root-to-destination paths. Its objective and feasible model differ. The source's Martin/Wong motivations are contextual assertions in the source; no equivalence of extended formulations, transfer between the two problems, or new formulation theorem is established here.

## Imported complexity dependency and preprocessing

The local complete primary scan of [Karp, *Reducibility among Combinatorial Problems*](https://doi.org/10.1007/978-1-4684-2001-2_9) has 19 pages, printed 85–103. Its ordinary text extraction is empty because it is scanned. All pages were rendered and OCR read; the relevant dependency pages 88–89, 92–95, 98, and 103 were also inspected visually. The Main Theorem on page 94 and item 11 on page 95 include satisfiability with **at most** three literals per clause. Page 98 supplies its reduction from unrestricted satisfiability. Appendix I on page 103 treats clauses as literal sets containing no complementary pair. The imported theorem therefore supports one-, two-, and three-literal clauses, exactly as needed. No exact-three-only or bounded-occurrence assumption is being imported. This is the standard complexity theorem used as an external proved dependency, not a claim that this audit reproves Cook's theorem from first principles.

Removing duplicate literals preserves a clause, and removing tautological clauses preserves the conjunction. An empty clause makes the formula false; a conjunction with no clauses is true. After these cases, there is at least one nonempty clause and at least one occurring variable. The proof's n≥1,m≥1 hypothesis is therefore justified.

Two useful exposition additions are available without changing the reduction:

1. Delete unused variable declarations and relabel the actual distinct occurring variable names densely as x_1,…,x_n. In particular n denotes the number of variables, not the maximum numeric label. This makes polynomial output size explicit for sparse labels such as x_(2^80).
2. Specify fixed endpoints. On the graph consisting of two vertices and their one edge, give both roots all-zero arc vectors and K=0 for a yes-instance. Give both roots all-one arc vectors and K=1 for a no-instance; its unique tree costs 2. Both instances are finite, connected, simple, and include every root and both arc directions.

These clarify routine details already covered by the proof's elementary preprocessing assertion; they are not central-proof repairs. Independently written `check_boundaries.py` verified preprocessing pointwise on 331 formula cases and 1,466 assignments, including repetitions, tautologies, empty clauses/formulas, contradictory units, and sparse IDs. All passed. These checks supplement the elementary logical argument; they are not a replacement for the reduction proof.

## Reduction and root-dependent objective

For the nontrivial input, let n be its variable count and m its clause count. The graph has hubs t,f, variable vertices v_i, and clause vertices q_j. The hub edge and both variable/hub edges connect the core; every nonempty clause has an incidence edge to the core. Thus G is connected and simple. Duplicate literals have been removed, so each clause/variable incidence edge is specified once. It has N=n+m+2 vertices and M≤1+2n+3m edges.

The construction defines every root/arc coefficient. At t, both directions of the hub edge cost 0, both directions of each variable/hub edge cost 1, and both directions of each clause/variable edge cost B=n+1. For each clause root q_j, variable-to-hub directions encode the sign of variables present in that clause. Reverse hub-to-variable arcs and every otherwise unspecified coefficient are explicitly zero. The f-root and variable-root vectors are zero. Consequently no cost depends on the future choice of tree, and no root vector or reverse arc is missing.

For an arbitrary spanning tree, let h∈{0,1} indicate the hub edge, p count variable/hub edges, and q count clause/variable edges. Clause connectivity gives q≥m, and the edge count gives p+q+h=n+m+1. The t-root contribution is

    p+Bq = (n+1)m+n + (1−h)+n(q−m) = K+(1−h)+n(q−m).

This is an exact identity for every spanning tree, including unstructured trees. Because every other root contribution is nonnegative and n≥1, total cost at most K forces h=1 and q=m. Each clause then has degree one. Removing clause leaves leaves the hub core: every variable must meet a hub, and meeting both would form a triangle with tf. Hence each variable has exactly one hub attachment and defines one truth value. This argument does not assume the desired structure in advance.

Root a structured tree at clause q_j, whose selected neighbor is v_i. Its v_i/hub edge points from v_i toward the hub and tests that selected literal. Every other variable/hub edge points from its hub toward that variable and has zero coefficient in c_(q_j). Thus the clause-root cost on its entire rooted orientation is exactly 0 for a selected true literal and 1 for a selected false literal. The full objective for structured trees is K plus the number of selected false literals.

A satisfying assignment attaches each variable to its truth hub and each clause to a true literal; the resulting connected N−1-edge graph is a spanning tree of cost K. Conversely every tree of cost at most K yields a structure and an assignment with every selected literal true. The SAT/decision equivalence holds in both directions. The structured-tree formula is not asserted for unstructured trees, and the proof does not require an exact formula for the optimum on unsatisfiable inputs.

## Explicit input size, verifier, and strong hardness

The coefficient table contains **2NM** entries, including zeros. Here M=O(N), so the table has O(N²) entries. A polynomial algorithm initializes that table to zero and sets the listed coefficients; there is no succinct/oracle representation. Coefficients are at most B=n+1≤N and have O(log N) bits. The binary output therefore has O(N² log N) coefficient bits, plus polynomial graph/root labeling and threshold encoding. After dense relabeling N is bounded polynomially in the original formula length.

K=(n+1)m+n=nm+m+n is at most N². If coefficients and K are written in unary, even the crude bound of O(N) symbols per coefficient gives O(N³) total coefficient output; K contributes O(N²). The reduction stays polynomial under unary encoding. This verifies strong NP-hardness, rather than merely a weak hardness result using exponentially large numerical penalties.

For NP membership, a certificate lists N−1 edge IDs. Check that they are distinct input edges and form a connected acyclic tree. Traverse that tree once from each of the N roots, orient its N−1 edges, and add the corresponding explicit input coefficients. There are exactly N(N−1) summands. If the largest coefficient uses b bits, the sum needs at most b+ceil(log2(max(1,N(N−1)))) bits, with the zero/single-vertex case treated directly. Certificate length, traversals, additions, and comparison with the encoded K are polynomial in the finite input length. No machine arithmetic overflow is assumed.

The precise strongly NP-complete language is the candidate's explicitly encoded nonnegative-integer decision problem. The source's arbitrary real notation alone does not define a Turing input encoding or an NP language. The proved finite integer subclass is enough to establish the requested optimization NP-hardness: an algorithm returning an optimal tree for that source model would decide the constructed integer instances by evaluating and comparing their objective. The candidate already distinguishes these statements correctly.

The optional strictly positive version is also valid. Adding 1 to **every coefficient for every root**, including formerly zero root vectors, adds N(N−1) to every tree objective. Replacing K by K+N(N−1) preserves all answers. Coefficients and the new threshold remain polynomially bounded. Independent controls used all 16 spanning trees of K_4 with fully explicit arbitrary 4,097-bit coefficients to verify orientation transposition, the uniform positive shift, and the stated addition bit-length bound. All passed. The all-size argument is the fixed count of selected root/arc pairs, not those finite controls.

The first audit scripts used executable `assert` statements, which Python can disable with `-O`. Those original scripts, normal-run results, and the first pinned manifest are preserved under `historical_pre_explicit_guards/`. Both current checkers now use explicit `require` calls that raise on failure. `run_guard_controls.py` confirmed zero executable assert nodes, successful normal and `-O` runs for both checkers, and identical semantic results after removing only the timestamps. Four known-false guard controls (normal and `-O` for each checker) exited unsuccessfully with the intended guard diagnostic. `GUARD_CONTROL_RECEIPTS.json` and its byte-pinned stdout/stderr/result snapshots record actual process IDs, argument lists, UTC start/end times, exit codes, and hashes. This repaired diagnostic trust; it changed no central reduction or source input and spent no new central proof-search turn.


## Source pair, duplicate semantics, and effort provenance

`inspect_sourcepair.py` rechecked the source inputs without writes. It opened SQLite with `mode=ro&immutable=1`, verified dataset revision 37e53eabe540fb458758e198be61634bd02ee008, and matched all five preexisting raw/catalog/SQL input byte and SHA-256 pins. The submitted source record equals the selected raw record and SQL payload exactly.

There is no imported report under OWR-16633-013 or its numeric ID in the raw reports. The correctly normalized selected report is `{}`, which matches SQL. No native prior-report file was submitted. Therefore the preexisting authentication field indicating that a *submitted* prior report does not match raw/SQL is not rewritten into a fictitious submitted report; absent native material and normalized source-pair semantics are different facts.

Exact-statement, exact-title, and a narrowly defined all-root arborescence/spanning-tree filter found only this target record. This is a limited source-duplicate check, not a complete equivalence search over all mathematics. The adjacent source record 30003997 / OWR-16633-014 matches its raw/SQL payload but remains the distinct fixed-root directed path-cost problem. Its science or status was not adjudicated. A shared gadget mechanism reported in the author log does not establish problem equivalence or two independent discoveries.

The authenticated original QUEUE projection says **claimed_solved, 2/5**. The original author log describes two substantive approaches, with the first failing to establish a valid transfer and the second producing the direct SAT reduction. The original native file inventory contains no structured status or turns file. No effort ledger was fabricated, no counter reset, and no new central proof-search turn was spent in this audit. The recorded effort is supported by QUEUE and the prose log; it is not an independently recoverable runtime event ledger.

## Exact clearance and remaining gaps

This audit clears source fidelity, the finite decision formulation, the reduction's encoding and boundary handling, strong/unary hardness, and the positivity corollary. The strongest checked claim is strong NP-completeness on connected simple undirected graphs with all vertex roots and an explicitly encoded nonnegative integer root/arc table; this establishes Kaibel Problem 1's requested optimization hardness.

No result on bounded degree, planarity, a fixed number of roots, approximation, the adjacent directed path problem, or an extended-formulation equivalence is inferred. The record's open status and 2026-08-21 literature triage are dated curation rather than a theorem about present-day priority. The candidate's statement that an earlier source search found no exact resolution is historical author prose; this audit neither authenticates an exhaustive priority search nor promotes it into novelty clearance. Priority has not been searched here and remains the exact publication-related gap.

All writes are confined to this audit's folder. Original sources, candidate files, Git/index, services, editor state, and publication state were not changed. No external person was contacted. Primary PDFs and their extracts/rendered images remain private and are excluded from public audit artifacts. `INPUT_OUTPUT_MANIFEST.json` records byte counts and SHA-256 hashes, including private derivative hashes without publishing their content.
