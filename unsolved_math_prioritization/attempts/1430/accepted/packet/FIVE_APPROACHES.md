# Five mathematical approaches and exact stopping gaps

These are distinct mathematical routes within this investigation, not claims of five independently scheduled model interactions. Source lookup, duplicate reconciliation, file packaging, and testing are not counted as proof turns. The mathematical claims are elaborated in PROOFS.md.

## 1. Transfer the extremum through orders and an apex

Target: use the extremal dimension theorem for finite posets to prove the proposed half-order bound, or use large-dimensional posets to exceed it.

Work: recover the exact equality between representations of an apex extension and concatenations of permutations of its base; relate the latter to realizers. Apply Hiraguchi's theorem to prove the half-order bound for all comparability graphs on N>=4, and the stronger floor((N-1)/2) bound for an apex extension when N>=5. Reconstruct the standard-example realizer and lower-bound obstruction, with the actual vertex count 2m+1. Test seven explicit apex witnesses, m=2,...,8. Analyze why replacing a general semi-transitive orientation by its reachability poset loses nonedges, already on the three-vertex path.

Result: the familiar extremal construction cannot cross the threshold, and a counterexample must be noncomparability. Gap: an arbitrary word-representable graph need not be the comparability graph of its reachability poset. No valid transfer of Hiraguchi's bound across that difference is established.

## 2. Induction using components and twin deletion

Target: extend a half-order inductive hypothesis by recovering deleted vertices without increasing multiplicity.

Work: prove uniform padding; prove the disjoint-union formula with its necessary lower floor of 2; give explicit true-twin and false-twin insertion maps, handling 1-uniform inputs correctly. Combine these with the exact small-order checks to restrict a smallest counterexample to a connected, twin-free, noncomparability graph with no universal vertex. Test 570 twin insertions, 121 component combinations and 75 padding cases.

Result: a rigorous reduction of the candidate class. Gap: these reductions do not ensure that every candidate has a removable twin, disconnected component, or apex. General vertex insertion does not inherit the twin construction, because prescribed neighborhoods may differ.

## 3. Compress compatible nonedge-cover blocks

Target: improve the known 2(N-omega) upper bound by covering many nonedges with fewer compatible words.

Work: prove the concatenation criterion with orientation compatibility. Define the finite set-cover parameter c2(D) for 2-uniform compatible supergraph words and prove R(G)<=2c2(D) for noncomplete graphs (complete graphs have R=1 and need no nonedge-cover blocks). The known star-cover lemma gives c2(D)<=N-omega(G), yielding the half-order bound whenever omega(G)>=ceil(3N/4). Test the arithmetic. A pure 2-block construction has an intrinsic parity/expressiveness obstruction to attaining the proposed exact target at N=6: the triangular prism has R=3 but any successful pure 2-block construction uses at least two blocks, hence multiplicity at least 4. Give an explicit 3-word and an exhaustive 10,395-normalized-word obstruction to a 2-word.

Result: a valid dense-clique case and a concrete limitation of this particular proof architecture. Gap: no universal small cover bound is proved, and adding permutations, overlap, or other block types changes the architecture and requires new compatibility arguments.

## 4. Force a larger example by entropy counting

Target: force some bipartite graph beyond the half-order bound by comparing graph counts with uniform word counts.

Work: count graphs on fixed part sizes a,b and bound their representations by N^(kN), obtaining examples with R on the order of N/log N. Then test the sharper exact multiset-word count (kN)!/(k!)^N at k=floor(N/2). It is already at least (N!)^k, which is at least 2^(ab) in the relevant range. Thus counting all words without quotienting their many-to-one map to graphs cannot give the desired contradiction at the target multiplicity. Derive the barrier analytically and check its integer inequality through N=500.

Result: a self-contained weak lower-bound route and a precise limitation of the naive pigeonhole method. Gap: useful control of representation fibers or a different candidate ensemble would be needed; this analysis does not rule out refined counting arguments. The September 2026 bipartite theorem independently shows that the bipartite class cannot supply the desired large-order counterexample.

## 5. Exact occurrence-order constraints and small instances

Target: turn the full definition into a finite constraint system and search small candidates for a lower-bound obstruction.

Work: give an exact occurrence-order encoding for k-uniform representations, including the nonedge constraints. Enumerate first-occurrence-normalized double words, relabel to produce all graph masks through N=5, and retain a directly checkable witness for each of 1,099 labeled graphs. Independently exhaust the 10,395 normalized double words on six letters to exclude the triangular prism, while directly checking its 3-uniform word. This distinguishes a positive representation witness from a proof of minimal multiplicity.

Result: all graphs on N=4,5 meet the proposed bound; the prism attains it at N=6 and demonstrates the block obstruction in route 3. Gap: finite checks at these orders do not yield a structure theorem or any conclusion at untested orders. No exhaustive search of all larger graphs or uniformities was attempted.

## What would close the problem

Either (i) construct a connected, twin-free, noncomparability, nonbipartite word-representable graph without an apex, of order N>=6, and prove R(G)>floor(N/2), or (ii) prove an extension or compression theorem covering that remaining class. A smallest counterexample must also have omega(G)<ceil(3N/4). These are necessary restrictions, not a characterization, and they do not prove nonexistence.
