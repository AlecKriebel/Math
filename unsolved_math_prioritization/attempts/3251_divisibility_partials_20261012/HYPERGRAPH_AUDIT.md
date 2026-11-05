> Edition note: This complete authored text preserves the mathematical arguments and substantive audit findings. Original operational references and identities of material not distributed here have been replaced with descriptive prose. The independent audits are AI mathematical reviews, not human peer review or formal proof verification.

# Independent mathematical audit: maximum-clique hypergraph partials

## Decision and exact scope

**ACCEPTED as scoped partial results. No mathematical correction is required in the frozen authored report. The full odd-hole-free maximum-clique division conjecture is not solved.**

The target is a finite graph with at least one edge and no induced odd cycle of length at least five. A division is a two-coloring of its vertices in which each maximum clique meets both colors. Maximum cliques cannot be replaced by inclusionwise maximal cliques, and graphs of clique number one are excluded.

The review verified the frozen authored hypergraph proof, explicit inputs, result expectations, and supporting programs against a separate external anchor and closed manifest. The complete authored proof is preserved in HYPERGRAPH_PROOFS.md. Original omitted proof, packet, program, and anchor identities and byte counts are intentionally not part of this prose-only distribution.

This audit independently reviews the all-size proofs, independently reconstructs and checks the finite witnesses, independently enumerates the exact finite scope, observes the author's precise visited case set, and exercises fail-closed controls. It makes no novelty claim. It makes no remote or queue changes and does not alter the frozen input packet.

## 1. Shadow realizability: accepted

Let H be a nonempty r-uniform hypergraph, in the surrounding scope r at least two, and S its two-section or shadow. Every graph realizing the edges of H as r-cliques contains all edges of S. Thus a clique of size r+1 in S rules out realization as maximum r-cliques. Conversely, if S has no such clique, nonemptiness of H supplies an r-clique, so S itself has clique number exactly r and realizes every edge of H as a maximum clique.

For exact equality with the maximum-clique family, every r-clique of S is unavoidable in any supergraph realization. Therefore it must already belong to H. This additional condition, together with absence of an (r+1)-clique, is also sufficient by taking G=S. These two directions establish the stated equivalences, not merely necessary conditions.

Vertices in no hyperedge are isolated in S and do not affect either equivalence. Repeated copies of an identical hyperedge, if a multihypergraph convention is used, impose the same constraint; exact equality to a graph's clique family is understood after discarding repetitions. The certificate deliberately uses simple hypergraphs and rejects repeated input edges. The proposition's nonemptiness assumption is essential to its argument that the shadow has clique number at least r.

This proposition does not preserve odd-hole-freeness when passing to S. The report correctly avoids that inference, and its next theorem explicitly refutes it.

## 2. Fano obstruction: accepted

The seven listed triples cover each of the 21 pairs of the seven vertices exactly once. Their shadow is consequently K7. They cannot be a subfamily of maximum triangles in any graph on those vertices, or in any larger graph containing those vertices, because their forced pair edges already produce a seven-clique.

The non-two-colorability proof is also correct. A line-free four-set has six pairs on six different Fano lines. Each such line meets the four-set twice, accounting for all twelve point-line incidences of that set; hence the seventh line lies entirely in its three-point complement. A line-free set of at least five vertices would have at least ten pairs lying on different lines, but only seven lines exist. Therefore every coloring has a monochromatic line. The independent replay checked all 128 colorings and all 35 four-sets, in addition to pair coverage.

The pair-covering generalization is valid: an r-uniform family covering every pair on more than r vertices has a complete shadow with clique number greater than r. None of this produces a graph counterexample to the original conjecture.

## 3. Chordal family and strong odd incidence cycles: accepted

For every odd m at least five and r at least four, attach r-2 private vertices to each perimeter edge of the fan-triangulated m-cycle, making that edge and its private vertices a complete graph of order r.

Every private vertex is simplicial while private vertices are eliminated, since its remaining neighbors lie in its one attached clique. Afterwards c1,c2,...,c(m-1),c0 is a perfect-elimination order of the fan. For the last entries the stated neighbor set is interpreted with the evident endpoint truncation; the remaining neighbors are still a clique. The earliest vertex of any proposed induced cycle of length at least four would have two nonadjacent later neighbors, contradicting this order. Hence the graph is chordal and therefore odd-hole-free.

A clique meeting private vertices stays in one attached r-clique. A core-only clique has size at most three. The requirement r at least four therefore makes the attached cliques precisely all the maximum cliques. Every fan chord is absent from their shadow, whereas each perimeter edge remains. The core induces the desired odd cycle in that shadow.

The explicit red-core/blue-private coloring divides every maximum clique. Thus the family invalidates inheritance of the odd-hole-free property under deletion of edges irrelevant to maximum cliques; it does not invalidate the original division conjecture. At r=3, core triangles can also be maximum, so the report correctly does not extend this argument to that rank.

Selecting the m attached clique rows and the m core vertex columns in the incidence matrix produces exactly two entries per selected row and column, cyclically arranged. Since m is odd, this is the asserted strong odd incidence cycle and disproves balancedness of maximum-clique hypergraphs even for chordal graphs. The separate three-sun illustration is correct: its central triangle and three attached triangles are its four maximum cliques, and the three attached rows alone yield the strong incidence triangle on the core.

Independent finite checks reconstructed the exact G(5,4) input graph, examined all 32,767 nonempty vertex subsets, found clique number four and exactly five maximum cliques, and found no induced cycle of length at least four. Its 32 graph edges reduce to 30 shadow edges, whose five core vertices induce C5. Its supplied elimination order, coloring, and incidence cycle all pass. The three-sun's exact four maximum triangles, elimination order, and strong incidence triangle also pass independent checks.

## 4. Incidence at most two: accepted, including Euler parity cases

Treat hyperedges as distinct labelled real vertices in a loopless multigraph D. A hypergraph vertex in two edges becomes a dual edge joining those real vertices. A vertex in one edge becomes a dual edge to the auxiliary vertex z. Incidence-zero vertices are omitted from D and can be colored arbitrarily. Multiple dual edges are permitted, so no simplicity assumption is needed. Each real degree equals the size of its hyperedge.

Adding one z-edge for every odd real degree makes every real degree even. The degree sum parity also makes the degree of z even. Each nontrivial component thus has an Euler circuit. Starting the z-component at z is important: if a circuit has odd length, the sole possible same-colored arrival/departure pair is at its start. Every other vertex retains exactly half its incident edges of each color under alternating traversal colors.

Every augmented real degree is at least four. In a component containing z, each real vertex therefore sees at least two edges of each color before removing its at most one added edge, and at least one of each afterwards. A component not containing z has no added edges, and all its real degrees were already even and at least four. At a real start vertex of an odd-length circuit, the two color counts are d/2+1 and d/2-1, whose smaller value is at least one. All other real vertices are balanced. This verifies the nontrivial parity corner case rather than presuming that every Euler circuit has even length.

Transferring original dual-edge colors back to hypergraph vertices makes each hyperedge bichromatic. The construction works for nonuniform hypergraphs, isolates, an empty hyperedge family, and repeated labelled hyperedges when incidence is counted with multiplicity. Alternatively, duplicate hyperedges may first be removed without changing colorability or increasing incidence. Empty or size-one hyperedges are excluded, as are size-two edges: the three two-element edges of a triangle already give an incidence-two non-two-colorable example. The Fano plane shows that increasing the incidence bound to three is not valid in general at rank three.

Besides the exact uniform enumeration, the audit exhaustively checked all 2,921 multisets of subsets of size at least three on labelled vertex sets of size at most six, subject to maximum incidence two. These include 94 cases with duplicate edges and 1,785 nonuniform cases, as well as empty families and isolates. Both independently implemented and authored Euler colorings were checked against a separate brute-force oracle. A separate seven-edge dual component with degrees 4,4,6, no z-incidence, and an extra isolated hypergraph vertex specifically exercises the odd-length real-start branch. It passes.

## 5. Hall criterion and incidence corollary: accepted

For every hyperedge create two labelled left-side copies, adjacent to its contained vertices. If a subset of copies represents t distinct original hyperedges, it has at most 2t copies, and its neighborhood is exactly the union of those original edges. The hypothesis gives at least 2t neighbors, proving Hall's condition for every subset of copies, including those with only one copy of some edges. A matching covering all copies gives distinct red and blue representatives in each hyperedge; since the representatives are globally distinct, their prescribed colors cannot conflict. The alternating-path justification of Hall's theorem included in the report is valid.

If all edges have size at least r and maximum vertex incidence is at most floor(r/2), any edge subfamily F satisfies r|F| at most the number of its incidences, at most floor(r/2) times the size of its union, at most r/2 times that union size. Dividing by positive r gives the required union bound. Combining this condition with the incidence-two theorem yields the stated necessary maximum incidence of at least max(3,floor(r/2)+1) for a non-two-colorable r-uniform hypergraph, r at least three.

The union condition is sufficient, not necessary. The four three-element stars of K4 on its six edges violate it for the full family while remaining two-colorable by incidence two; the independent oracle verifies this illustration. For the separate six-uniform witness, all twelve vertices have incidence three, and all 64 edge subfamilies satisfy the union criterion. An independent breadth-first matching construction covers both labelled copies of every edge. Duplicate hyperedges, if retained as labelled family members, can only make this sufficient criterion stronger; the proof still applies.

## 6. Exact computational coverage and implementation audit

The advertised 11,390 count means simple, labelled, rank-tagged hypergraphs with 0 at most n at most seven, 3 at most r at most n, and maximum vertex incidence two. There are no admissible (n,r) pairs for n below three. An empty family is counted once for each admissible (n,r), so rank-tagged empty cases must not silently be deduplicated across ranks. Isolated vertices are allowed. These tests do not enumerate all graphs of those orders and do not test all hypergraphs without the incidence restriction.

The independent enumerator uses increasing edge-index extension with per-vertex capacity pruning. Each eligible family has exactly one increasing index sequence; every prefix of that sequence meets the capacity bound. Therefore recursion visits every eligible family once and cannot lose a case through pruning. Unlike the authored loop, this enumeration does not depend on a separately imposed edge-count bound. The authored bound itself is valid because r times the number of edges is at most 2n.

Instrumentation records the author's exact (n,r,edge-family) arguments, checks that none is repeated, and compares the resulting set with the independently generated set. Exact equality holds for all 11,390 cases, not merely equality of aggregate counts. The exact serialized case set was checked as part of the original audit but is not distributed here. Counts in every (n,r) cell match the mandatory expected-results file. Exactly 6,170 cases satisfy the Hall union criterion; independent exhaustive subfamily checks and independent breadth-first matching agree on each case.

The audit independently validates every returned authored Euler coloring, runs its own Euler construction, and checks existence using a brute-force oracle that fixes one color by complement symmetry. Three independent audit replays under normal Python, -O, and -OO return identical JSON results. The authored executable also independently passes under all three modes with byte-identical output. Assertions are not used as an acceptance gate.

## 7. Integrity and hostile controls

Native lstat checks reject symlink components in the original packet and external-pin paths. The independent audit verifies exactly five payload files plus the manifest, verifies regular-file types, checks both the fixed external-pin identity and fixed manifest identity, and verifies every payload hash and byte count. The frozen inputs are byte-identical before and after all tests.

There are 42 independently authored negative cases in each of normal, -O, and -OO, for 126 successful rejections. For every packet member, including the manifest and executable, controls cover removal, symlink substitution, and tampering. Additional controls cover missing or modified external pin, pin symlink, root and ancestor symlinks, unexpected file/directory/symlink, a pin improperly placed inside the packet, a checker launched from a different packet, duplicate JSON keys, missing mandatory sections, repeated or nonuniform Fano input, wrong graph edges, incomplete maximum-clique list, invalid elimination order, wrong hole, monochromatic division, wrong Hall incidences, changed enumeration scope, altered expected count, and missing required command-line arguments. Semantic mutants are repinned in isolated copies where appropriate, proving rejection beyond hash mismatch alone. No hostile mutation touches the frozen originals.

The author's separately completed 36-control record and terminal receipt were also independently rehashed and all receipt members verified. These original records are not distributed in this prose-only edition.

These checks certify this pinned static packet and the specified tested failure modes. They are not a claim of protection against concurrent hostile filesystem races, every possible malformed JSON representation, or a replacement of both trusted external anchors. Finite testing supplements the mathematical proofs; it does not replace them.

## 8. External theorem boundary

The structural proofs above are self-contained and do not depend on the four-colorability theorem cited in the literature paragraph. That citation was independently checked against the public author PDF: Maria Chudnovsky, Neil Robertson, Paul Seymour, and Robin Thomas, *K4-free graphs with no odd holes*, Journal of Combinatorial Theory, Series B 100 (2010), 313-331, https://thomas.math.gatech.edu/PAP/k4free.pdf . The exact PDF has 217,207 bytes and SHA-256 `2e57b496d24fbc04db44d9efc900f3eb5af4843c9f42adadc5e376837be4b504`.

On internal page one, PDF page three, Theorem 1.3 states the four-colorability result, and the paragraph following Conjecture 1.4 explicitly identifies the corresponding division consequence. With clique number three, any maximum triangle uses three distinct proper colors; splitting four colors into two pairs prevents it from being monochromatic. The clique-number-two case needs its own bipartiteness argument: a shortest odd cycle in a triangle-free graph would be an induced odd hole. The at-least-one-edge condition must be retained, because singleton maximum cliques cannot meet both parts. The source's broader wording involving at least two vertices is not imported into the target without this correction.

The theorem statement, local context, and public metadata are verified. No independent audit of the entire external 24-page proof is claimed. The packet's acceptance does not rely on such a claim.

## Conclusion

All five requested mathematical components and the finite computational claims are accepted at their stated scope. The exact coverage, authored and independent algorithms, graph witnesses, optimization-resistant checks, mandatory-input failures, native inventory and symlink checks, and separate author terminal evidence all pass. The unrestricted odd-hole-free division conjecture remains open within this work, and no classification or novelty claim follows from this audit.
