Editorial note: The complete authored proof or audit is preserved below. Changes replace only operational artifact identities, byte counts, locations and original replay directions. All mathematical arguments, exact finite scopes and substantive limitations remain. This edition's public manifest identifies the distributed prose.

# Independent acceptance: fourth-pass chordal core-extension obstruction

## Verdict and exact scope

**ACCEPTED, without a mathematical correction.** The supplied all-size proof establishes the stated counterexample to *arbitrary prescribed division extension* from the exact high-incidence core, for every integer k >= 3. The graph itself has a division, so this is not a counterexample to odd-hole-free 2-divisibility. It does not establish a conclusion about an induced-minimal indivisible graph or settle the general target.

This audit independently read the full [family proof](FAMILY_PROOFS.md), the explicit k=4 fixture, the checker, the final control harness, and all scope/expected data. It used the final trust anchors below, not preliminary pins. No source packet bytes were edited. No remote, queue, publication, or new research-round action was taken. No historical credit, novelty, minimality, or comprehensive security claim is made.

## All-size mathematical acceptance

Let A,P,L,M be disjoint (k-1)-cliques and let u,b,c,d,e be five distinct additional vertices. The only inter-block adjacencies join A to u,b,c; P to u,d,e; L to b; and M to b.

1. **Order, size and degrees.** The order is 4(k-1)+5 = 4k+1. The number of edges is 4 binom(k-1,2)+8(k-1) = 2(k-1)(k+2). Each vertex of A or P has degree k+1; each vertex of L or M, and each of c,d,e, has degree k-1. The degrees of u and b are respectively 2(k-1) and 3(k-1). These formulas account for every edge and give the same edge count by the degree sum.

2. **Exactly eight maximal and maximum cliques.** Every clique is contained in one of A+u, A+b, A+c, P+u, P+d, P+e, L+b, M+b. Indeed, a clique meeting L or M has no outside neighbor except b; one containing c,d,e is restricted to its corresponding block; after these cases, a clique meeting P can use only u outside P; one meeting A can use at most one of the nonadjacent u,b. The remaining vertices form a stable set. The eight listed sets are distinct cliques of size k, so they are exactly the maximal cliques as well as the maximum-cardinality cliques, and omega(G_k)=k.

3. **Incidences and the exact core.** The original maximum-clique incidences are three on A and P and on b, two on u, and one everywhere else. Consequently X=A union P union {b}, of order 2k-1, exactly equals the incidence-at-least-three set. Its induced graph is K_k on A+b disjoint from K_(k-1) on P. The only maximum clique of this core is A+b. Every induced subgraph of the core is a disjoint union of at most two cliques, so its clique and chromatic numbers coincide; the perfect-core assertion is elementary and valid.

4. **Connectedness and chordality.** The connections through u join A and P, and those through b join A,L,M; c,d,e attach to their blocks. The order L,M,d,e,c,P,b,u,A, with arbitrary internal block orders, is a perfect elimination order: the later neighbors are successively subsets of L+b, M+b, P, P, A, P+u, A, A, and A. Each is a clique. The earliest vertex on any induced cycle of length at least four would have two adjacent later cycle-neighbors, a contradiction. Thus G_k is connected and chordal, hence odd-hole-free, for every stated k. No imported perfect-graph result is needed.

5. **The obstructed core division.** Coloring A blue and P+b red gives a valid division of the core because A+b is mixed. In the whole graph A+u forces u red and P+u forces u blue. Thus this core division cannot extend. Reversing both colors supplies its complement.

6. **Exact projection, including sufficiency.** A core coloring extends precisely when (a) A+b is mixed and (b) A and P are not monochromatic in opposite colors. Necessity is supplied by A+b and the two bags through u. For sufficiency, every monochromatic A or P requires u to take its opposite color; these requirements are compatible under (b). Choose c opposite a monochromatic A and d,e opposite a monochromatic P, with arbitrary choices when the corresponding block is mixed. Give both colors to each of L,M, possible because k-1>=2. All eight maximum cliques are then mixed.

An equivalent exact Boolean projection, writing x_v=1 for one color, is the conjunction of these four clauses:

- OR over v in A+b of x_v;
- OR over v in A+b of not x_v;
- (OR over v in A of x_v) OR (OR over v in P of not x_v);
- (OR over v in A of not x_v) OR (OR over v in P of x_v).

The last pair excludes respectively (A all 0,P all 1) and (A all 1,P all 0). This projection also follows by ordinary existential Boolean elimination: eliminating the private vertices removes their bag clauses via tautological resolvents, and eliminating u leaves exactly the two cross-block clauses above, alongside the two A+b clauses. The audit implements this alternative, independently of the packet's depth-first extension oracle.

7. **All core colorings and exact counts.** There are 2^(2k-1) core colorings. Precisely 2^k have A+b monochromatic, so 2^(2k-1)-2^k are core divisions. Among the latter, opposite monochromatic A,P force b to have P's color; exactly two such divisions exist. Therefore exactly 2^(2k-1)-2^k-2 divisions extend and exactly two do not. Non-core-divisions are excluded separately; “two failures” refers only to divisions of the core.

8. **The whole graph is divisible.** Give both colors to each of A,P,L,M and color the five other vertices arbitrarily. Every listed maximum clique contains a mixed block. This confirms the limitation of the obstruction and supplies an extension-compatible core division.

## Explicit k=4 witness

The fixture has A={0,1,2}, P={3,4,5}, L={6,7,8}, M={9,10,11}, and (u,b,c,d,e)=(12,13,14,15,16). Its full 36-edge list equals the independent adjacency construction, and its eight bags and complete elimination order agree exactly. Vertices 0..5 have degree five; 6..11 and 14..16 have degree three; u has degree six and b degree nine. The high-incidence set is {0,1,2,3,4,5,13}.

The fixture coloring sets A to 0 and P+b to 1, forcing contradictory colors on u. Of its 128 core colorings, 112 are core divisions, 110 extend, and two fail. The two failing core masks are 7 and 120 in the ordered core [0,1,2,3,4,5,13]. These are color complements, not two structurally distinct obstruction types.

## Bounded computation and independent cross-checks

The source's exact bounded universe is the six specifically labeled family members k=3,4,5,6,7,8, not all graphs of any order. Their core-coloring counts are 32,128,512,2048,8192,32768, totaling **43,680**. Their counts of core divisions are 24,112,480,1984,8064,32512, and extendible counts are 22,110,478,1982,8062,32510.

The separate exhaustive odd-hole check inspects only the k=3 and k=4 fixtures: every odd vertex subset of size at least five, respectively 3,797 and 64,839 subsets, totaling **68,636**. For odd order n these counts equal 2^(n-1)-n-binom(n,3). Connected induced degree-two subgraphs in that scope are exactly induced odd cycles of length at least five. Larger k use the checked elimination certificates plus the all-size proof; no larger exhaustive odd-subset search is claimed.

The audit's standalone independent checker imports no packet code and reconstructs edges by adjacency rules rather than clique bags. It enumerates every nonempty clique by increasing-label recursion (not the source's Bron-Kerbosch algorithm), checks all degrees and all maximal/maximum cliques, checks core/incidences/PEOs, and obtains the exact four-clause core projection by Davis-Putnam elimination (not the source's depth-first extension algorithm). It checks every one of the same 43,680 core colorings. Its case-stream hash matches the original exactly. The undistributed case-stream identity is omitted from this prose edition.

As an additional finite independence check, it exhausts all 8,192 full colorings at k=3 and all 131,072 at k=4, totaling 139,264 whole-graph colorings. Their restrictions give exactly the independently projected extendible core sets. The full graph has respectively 1,458 and 61,250 labeled two-color divisions. These additional finite counts are audit cross-checks, not new all-size claims. Independent results agree byte-for-byte under normal Python, -O, and -OO.

## Frozen evidence and fail-closed controls

The final supplied original manifest, external pin, complete proof and external terminal receipt all match the actual regular nonsymlink source files. Their identities were verified before this prose edition was prepared. The public manifest identifies the actual distributed prose; omitted original operational identities remain outside this edition.

The final control harness adjusts write permissions only on disposable copied packets and copied pins. Its final bytes are covered by the original final manifest and external pin. The original source root is mode 0555 and its seven files are mode 0444. The exact original inventory consists of the manifest, complete proof, control harness, expected-results record, mandatory-input record, verifier and explicit k=4 fixture. All native source paths and their checked directory ancestors are nonsymlinks. The externally pinned terminal's nine evidence records also match in byte size and SHA-256.

The audit reran the sealed verifier under normal Python, -O, and -OO. Each returned PASS with exactly the stored expected bytes and an empty stderr. It also reran the final sealed control harness separately in all three modes: **42 required rejection controls per mode, 126 total, all rejected**, with two positive controls per mode and empty stderr for each successful harness run. The replayed control JSON matches the corresponding terminal-pinned source receipt byte-for-byte.

The 42 controls comprise missing, tampered, and native-symlink versions of each of all seven packet files, including the manifest; extra file/directory/symlink inventory entries; root and ancestor symlinks; missing, changed, or symlinked external pins; an interior pin; wrong checker origin; missing CLI arguments; duplicate pin/manifest JSON keys; changed scope and scope types; altered expected counts and stream hash; altered explicit witness edges and coloring; and deliberately false order/PEO obligations. Semantic mutants are re-manifested and re-pinned where needed, so their rejection exercises semantic gates instead of stopping only on byte-integrity mismatches. The scripts contain no Python assert acceptance gates.

The source snapshot was independently rehashed after all runs, with original byte lengths, hashes, file modes and inventory preserved. This audit's separate deliverables and replay evidence are sealed by their own audit manifest and external audit seal. These checks support the stated finite failure modes and the supplied trust anchors; they do not claim protection against hostile concurrent filesystem races, arbitrary replacement of the checker and every trust anchor, or every imaginable path-alias attack.

## Acceptance boundary

Mathematical acceptance is complete for the claimed all-k family and its exact projection/count formulas. The independent finite checks are supplementary evidence with the explicit limits above. The scope cautions in the proof are correct: every graph in the family is divisible, the general odd-hole-free 2-divisibility question remains unresolved, and neither an extension-existence theorem nor a perfect-core divisibility theorem is refuted. The sufficiency condition forbidding monochromatic (k-1)-cliques in the prescribed core is not contradicted, because both A and P are monochromatic in the obstructed prescription. No prior theorem's provenance or novelty was investigated or credited.
