# Independent audit: exact (p,q) transversals, record 30001895

Date: 2026-10-03 UTC. Review of five frozen author attempts only.

## Disposition

**PASS for the stated partial mathematical and computational claims. HOLD for any claim that the full original record is solved.** No mathematical repair to the frozen partial conclusions was found. The package correctly ends `exhausted_unfinished`, with five substantive author responses used and no complete result for the r-element component. This review did not undertake a sixth author search or resume an unresolved case.

The accepted partial conclusions are:

- The hyperplane assertion is false by credited prior work on actual affine lines. It is not an original result of this attempt and does not settle the separate r-element assertion.
- The finite r-set problem has the claimed exact bounded-degree packing formulation. The private-padding and finite-obstruction reductions, elementary maximal-packing bound, and critical-counterexample deductions are valid.
- The r=2 case follows from the cited existing graph theorem, with the stated reductions and explicit nonvacuity convention.
- Every rank-at-most-three family H with τ(H)≥3 satisfies ν₃(H)≥min(|H|,5). Therefore the original rank-three bound holds for p=q+1, q≥4; the p=q boundary holds in every rank. The arbitrary-family extension is valid.
- The critical edge/degree equality cases force complete uniform families and yield the stated strict bounds on a minimal counterexample.
- A rank-three, τ=4 minimal counterexample has maximum degree at most seven. Degrees ten, nine and eight are excluded by the stated extremal/link arguments and complete finite certificates.
- The counting restriction has exactly twenty surviving (edge-count, maximum-degree) pairs. Nine are excluded by complete trees; eleven remain unresolved. Nothing in this review excludes larger τ at rank three or general ranks at least four.

## 1. Frozen input and scope

Reviewed author files: the 54 files in this directory’s parent bound by `../FINAL_AUDIT_MANIFEST.json` (53 payloads plus the manifest).

Frozen final-manifest SHA-256:

`32c1dc88b5e6457ab78f98c88aaf82231190601e3cb5f3f6043c8a40613ed79e`

All 53 manifest-listed files match both their recorded byte lengths and SHA-256 hashes. The manifest, final report, T1–T5 mathematical notes, all claimed complete certificates, checkers, generators, result files and per-turn records were inspected. The review is bound to these bytes. The reviewed WIP reference is branch `research/30001895-r-set-transversals`, commit `7f029a9d7deebfc523a1ccc9fdcb83220edf0990`; the mathematical audit does not depend on a remote or perform a remote write.

The original source separates Dol’nikov Problem 8 parts 2 and 2′. The standard nonvacuous interpretation |F|≥p, distinct members, nonempty sets, common intersection of q members, and rank/exact-uniform conventions are essential and are explicitly retained. No claim is made for a vacuous |F|<p reading, for multisets, for empty member sets, or for a pairwise-intersection substitute.

## 2. T1–T2 and credited sources

The separate reviewer report `REVIEW_T1_T2_T4_SECTION1.md` records the source checks and detailed algebraic audit. The core reasoning was also reviewed here:

1. A p-edge subfamily with no q-fold common point is exactly a (q−1)-packing. Adding any edge to an s-packing increases every degree by at most one, giving the claimed packing-growth inequality. Choosing p=ν_r+1 and q=r+1 proves necessity of C_r; growth proves sufficiency for all larger q.
2. Private padding preserves every common intersection of two or more distinct members and preserves τ by replacing private points with points of their original nonempty edges. It also preserves all ν_s, s≥1, since a new point has degree one.
3. The finite-obstruction induction is valid, including its size bound 1+r+…+r^t. Enlarging a witness to at least p members proves the arbitrary-family extension without a hidden finiteness hypothesis.
4. A maximal r-packing's saturated vertices cover every unselected edge. Counting saturated incidences shows |S|≤|N|, and covering the residual selected edges proves τ≤|M|. The Fano extension correctly disproves completeness of the proposed surplus method, not the original conjecture.
5. Minimal-counterexample edge deletion cannot leave maximum degree ≤r: the deleted edge would otherwise give an (h−1)-packing and a degree-(r+1) vertex would give a cover of size h−r. The resulting chain of inequalities forces τ-criticality, packing deletion-stability and τ=ν_r−r+2. Additivity plus τ≤ν_r forces incidence-connectedness. The τ=1 and τ=2 cases are correctly eliminated.

The independent finite checks reproduce all seven T1 cases, totaling 1,116,240 labelled families, with a new direct vertex-cover computation and a feasible-subset maximum transform. Both T2 examples reproduce exactly, including the Fano extension's two maximum packings and Q-values 0 and 1. Independent mixed-rank controls cover 128 families, 672 (p,q) instances, 576 padding/packing comparisons, 448 growth comparisons, 233 finite-witness instances and 195 maximal-packing cover checks.

The primary sources checked by the reviewer support the cited parameter definitions and theorem applications: [Dol’nikov original scope](https://ems.press/content/serial-article-files/46358), [proposer-authored nonvacuous convention](https://arxiv.org/abs/1312.4110), [Keller–Smorodinsky line theorem](https://arxiv.org/pdf/1809.06451v2), [published r=2 graph theorem](https://pisrt.org/psrpress/j/odam/2024/1/covering-and-2-degree-packing-numbers-in-graphs.pdf), [Bollobás original](https://web.vu.lt/mif/s.jukna/EC_Book_2nd/Bollobas.pdf), and [uniform equality statement](https://www.renyi.hu/~gerbner/papers/glpps2.pdf). Credited results remain credited; no novelty determination or fresh exhaustive literature search was attempted. “Unresolved” here describes what this five-turn package establishes, not an independent certification that no later theorem exists anywhere.

## 3. Complete incidence encoding and tree proof

### 3.1 Why the encoding loses no counterexample

For h labelled triples, represent each ground vertex by the set of incident edge labels. If no five-edge (T3) or six-edge (T5) 3-packing exists, every target subset of that size meets some support in at least four labels. Supports of size ≤3 cannot witness this condition and may be omitted.

Identical high supports may be collapsed. This preserves all target witnesses and reduces row occupancy. If a row still belongs to three distinct retained supports, its three actual vertices must be exactly their unique representatives: there is no room for a repeated support type or a further low-degree point. Consequently, two saturated identical retained rows would have been identical original triples. Forbidding them is a valid simplicity constraint after collapsing duplicates.

For transversal number at least t, any k retained supports, 1≤k<t, have union of size at most h−t+k. Otherwise their k vertices and one representative from each missed edge form a cover of at most t−1 points. This gives exactly:

- T3: support size ≤h−2 and no pair union equal to all h rows;
- T5: support size ≤h−3, pair union size ≤h−2 and no triple union equal to all h rows.

Row capacity is three. All these failures persist when additional supports are selected. A largest support of size D can be relabelled to {0,…,D−1}; all other supports have size at most D. Collapsing equal supports preserves D. This symmetry reduction is exhaustive.

At T3, a minimal subfamily with τ≥3 is τ-critical with τ=3, hence has at most ten edges by the credited Bollobás bound. The arguments for at most five edges are correct. The remaining h=6,…,10, D=4,…,h−2 domain contains exactly fifteen cases. At T5, the degree, critical-edge and counting arguments supply the twenty-case finite domain without asserting that these cases exhaust larger τ.

### 3.2 Why every saved tree is an impossibility proof

Each internal node selects a currently uncovered target and lists every admissible remaining support that covers it. Any completing family must contain one of those supports. Partition completions by the first listed support they contain: child i selects support i and forbids the earlier listed supports. This is an exhaustive, non-overlapping partition. A leaf with no admissible support cannot be completed. Well-founded child indices and a once-only traversal bind the entire finite tree.

The fresh replay in `independent_certificate_audit.py` is separate from the author generators and checkers. It uses immutable sets of row labels; recomputes admissibility from the entire selected family, including all relevant unions; and carries explicit excluded supports. It does not import author code, use a solver status, trust author pruning counters, or rely on the generator's target heuristic.

It accepts exactly the fifteen claimed T3 pairs and exactly the nine claimed completed T5 pairs, rather than interpreting a partial domain as complete. Results:

- T3: 15 trees; 7,116 nodes; 6,172 impossibility leaves.
- T5: 9 trees; 6,521 nodes; 5,774 impossibility leaves.

Wrong targets, omitted required branches, forged impossible leaves and cycles are independently rejected for both parameter regimes. A planted nearby covering system formed by complements of the five edges of K₁,₅ passes the positive capacity-four control, covers every five-row target, and fails the capacity-three control. This tests the essential capacity boundary rather than only feeding malformed files to a parser.

All four supplied checkers were rerun successfully as secondary checks. `reproduce_turn3.py` and `reproduce_turn5.py` were then run only on already completed cases. The exact compressed certificates were reproduced byte for byte; the degree-eight certificate and counting table also reproduced. No unfinished case was resumed.

## 4. Extremal and link arguments

### 4.1 Equality cases

For each critical hyperedge e through v, the pair (e\{v},T_e) has disjoint parts of sizes r−1 and t−1, and cross-intersects every other pair in the required direction. Both directions hold because all distinct ordered pairs occur. The uniform equality theorem therefore gives one common (r+t−2)-set W and all complementary partitions.

Every edge avoiding v meets every (t−1)-subset of W, forcing all of its r points into W. If any r-subset of W∪{v} were missing, its complement would cover H using t−1 points. Thus H is the complete r-uniform family on r+t−1 points. Its cyclic r-intervals are distinct and form an r-packing of that size, while incidence counting gives the matching upper bound. The analogous critical-edge equality argument is valid. These applications justify both strict bounds used later.

### 4.2 Exhaustive graph normal forms

A private transversal for a star triple {v,x,y} avoids v,x,y and restricts to a graph cover of G\{xy}. Thus every link edge has a private cover of size at most three avoiding its endpoints. The neighbor argument forces graph maximum degree ≤4. A degree-four graph vertex forces all edges onto its five-point closed neighborhood: an outside edge touching neighbor b misses the forced cover N(a)\{b}, and an entirely outside edge misses every such cover.

For graph maximum degree ≤3, fix uv and pad a private cover to a triple T disjoint from uv. There are enough graph vertices to do this. All other graph edges meet T. The degree sum over T is (|E|−1)+|E(T)|≤9, giving 0 or 1 internal edges for a nine-edge graph, and 0, 1 or 2 for an eight-edge graph. The one-edge and two-edge cases each have the single stated isomorphism type on three vertices.

The only edge entirely outside T is uv. Vertices u and v have at most two neighbors in T; every other nonisolated outside vertex has one of the seven nonempty neighborhoods in T. Each neighborhood multiplicity is at most three. This proves the normal-form coverage without a bound on the total original ground set, a connectedness assumption on G, or an assumption that equal neighborhoods represent the same vertex.

The fresh checker enumerates neighborhood multisets with `combinations_with_replacement`, independently of the author's residual-capacity recursion and original checker's Cartesian product. It reconstructs the graphs and checks offending edges against all avoiding covers of sizes 0,1,2,3, not just padded triples:

- Nine-edge links: exactly 1,691 normal forms, all rejected; 115,616 candidate small covers tested.
- Eight-edge links: exactly 2,107 forms, 2,097 rejected and 10 explicitly verified diamond-path isomorphisms; 111,546 candidate small covers tested for the rejected forms.

The diamond-path graph passes a positive private-cover control; a degree-five star fails the required private-three-cover test. Both original and fresh checkers reject missing normal forms and a false diamond isomorphism.

### 4.3 Degree nine

The maximum-degree-four case is K₅ minus one edge ab. In G\{f}, the avoiding private cover must have size three within W and equal W\f; two points cannot cover it because an independent triple would require three missing pairs. Hence a non-v hyperedge is either wholly in W or has W-trace exactly ab. If no external abz occurs, W\{a,b} is a three-cover. A missing triple B⊂W not containing ab would similarly yield the three-cover {v}∪(W\B). The needed acd, bce and one abz therefore exist, and the six claimed edges have degrees (3,3,3,2,3,3,1). All six are distinct and present. This excludes degree nine without an assumption about the external point z beyond its stated location.

### 4.4 Degree eight and external vertices

The maximum-degree-four alternatives are precisely K₅ minus two adjacent or two disjoint edges. The normal-form computation leaves only the six-point diamond-path graph when the link maximum degree is at most three.

A link edge with no avoiding two-cover forces its actual private three-transversal wholly into W. A link edge admitting a two-cover need impose no constraint. This is particularly important for edge 12 in K₅ with missing pairs 01 and 02, whose private transversal may contain an external point. The certificate correctly omits that constraint.

The fresh checker recomputes all six private-cover systems, all 12/13 eligible nonempty traces, and all 28,672 trace subfamilies. Exactly 1,290 subfamilies have no two-cover and each supplied witness is verified. Selected trace indices and star-edge indices are required to be distinct. The actual family of traces has no two-cover in W, since otherwise those two points and v cover H. Choosing one actual non-v hyperedge for each of the three distinct selected traces gives distinct edges. External vertices occur in at most these three edges; v occurs in exactly the three star edges; all W-degrees are checked. This establishes the six-edge 3-packing without splitting shared external vertices or imposing artificial private padding.

Both the author and fresh checkers reject an omitted private-cover system, a missing trace-family witness, repeated nonstar trace indices and repeated star-edge indices.

## 5. Counting, array repair and unresolved scope

The function F_h(d) counts six-edge targets containing at least four incident edges at a vertex of degree d. Taking the union bound over vertices is valid even with multiple witnesses. The bound by 3h times the maximum witness-per-incidence ratio uses only the exact total of 3h incidences; vertices of degree ≤3 contribute zero. Flooring the rational upper bound is legitimate because the target count is an integer.

The fresh audit recomputed each F_h(d) by directly enumerating six-element subsets and compared all 46 arithmetic rows, rational ratios, bounds and dispositions. Exactly twenty pairs survive, as stated. The complete-tree pairs are:

(7,4), (8,4), (8,5), (9,5), (10,5), (9,6), (10,6), (10,7), (11,7).

The eleven unresolved pairs are exactly:

(11,5);
(11,6), (12,6), (13,6), (14,6);
(12,7), (13,7), (14,7), (15,7), (16,7), (17,7).

The frozen τ=4 source has seventeen-row arrays. Its target bitset has 194 words, enough for C(17,6)=12,376 targets; at most floor(3h/4)≤12 selected high supports keep its 32-bit row tags within bounds. Its CLI prevents a larger h. An aborted search does not write an impossibility tree. The final aggregate certificate includes exactly the nine completed corrected runs, and all reproduce byte for byte. Independently replaying their full trees means no retained mathematical exclusion depends on the discarded ten-row pilot, its counters or its reported status.

Historical pilot data outside the frozen manifest is not evidence for any conclusion. The reported unsuccessful cases remain unresolved whether stopped by 25,000 nodes or by 45 seconds. The `satisfiable:false` field accompanying `aborted:true` is correctly not interpreted as unsatisfiability. The current code and proof checks support the retained results; they cannot verify the historical claim that every discarded scratch copy ceased to exist, nor is that necessary for this package's validity.

## 6. Required disposition and optional hardening

No mathematical repair is required for the frozen partial claims. The following scope restrictions are mandatory:

1. Preserve the distinct source components and credit the published hyperplane negative result and graph positive result.
2. Preserve |F|≥p and all stated set-family conventions.
3. Treat the nine τ=4 trees as a partial parameter-domain proof, with exactly the eleven unresolved pairs listed above.
4. Do not mark the full r-element component or bundled original record solved. Preserve the five-turn exhaustion status.
5. Run the original Python checkers with assertions enabled. Their documented `python -O` limitation is real. The fresh audit checker instead raises explicit exceptions for its core validations.

Optional software hardening, not a repair to these verified mathematical conclusions: have the original partial-domain checker offer an explicit expected-case list or pinned-manifest mode, and replace correctness-critical Python assertions with unconditional validation exceptions. The review already enforces the exact nine-case list and the manifest; these suggestions are not grounds to infer an unverified gap.

## 7. Reviewer evidence

- `independent_certificate_audit.py` / `.json`: fresh tree replay, multiset link enumeration, all small covers, trace witnesses and direct counting.
- `adversarial_controls.py` / `.json`: seven graph/trace mutations rejected by both checker implementations.
- `verify_tau3_certificate.json`, `verify_link_certificate.json`, `verify_degree8_certificate.json`, `verify_tau4_certificate.json`: rerun original checkers.
- `reviewer_reproduce_turn3.json`, `reviewer_reproduce_turn5.json`: byte-for-byte completed-certificate reproduction.
- `REVIEW_T1_T2_T4_SECTION1.md` and its listed scripts/results: independent T1–T2/source/T4-equality review.
- `AUDIT_SOURCE_MANIFEST.json`: original review identity and original hashes; `../PUBLIC_MANIFEST.json` binds this portable projection.

Final status: **accepted partial results; full original still unresolved, 5/5 author turns used.**
