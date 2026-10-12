# Independent audit: local switching frontier and retained max-cut certificates

## Verdict and exact scope

**PASS for the stated mathematical results and the retained finite evidence. No substantive mathematical correction is required.** The packet does not resolve the Weak pentagon conjecture, does not establish that all globally maximum cuts admit the prescribed extension, and does not establish novelty.

The independent review verified the complete original inventory, declared sizes and digests, and the incoming integrity pin before and after replay. Unexpected files, directories, and symlinks were rejected. The original proof and audit arguments are preserved here; the undistributed inventory and its identities are omitted. The public manifest identifies only this edition's distributed files. The source material was neither edited nor published during that audit.

Independent checks established:

- The three-stability/four-stability equivalence and the sharp bound `|M| <= 3n/8` under the stated hypotheses.
- The five-switch forbidden configuration and the necessary bound `|M| <= n/3`, with neither a converse nor sharpness asserted.
- The exact sharpness graph: cut size 18, maximum cut 22, one normalized maximizing cut, and exact maximum gains `-1, 0, -1, 0, 1` for switching sets of sizes 1 through 5.
- The fixed-status 19-edge core obstruction and the impossibility of making a cut globally maximum while retaining this core as an injectively embedded subgraph with its edge statuses.
- All **33,400 positive graph–cut certificates**, including **1,600 independently certified globally maximum prescribed cuts**.
- All four complete construction outputs and all four search logs reproduced byte-for-byte from the frozen C++ sources.
- Runtime validation and adversarial controls remained active under ordinary Python, `-O`, and `-OO`.

## 1. Definitions, quantifiers, and scope of assumptions

Let `G=(V,E)` be a finite simple triangle-free cubic graph. A cut is the edge set `B=delta(S)` for a vertex subset `S`; its complement is `M=E\B`. A switch of a **set of distinct vertices** `X` replaces `S` by `S symmetric-difference X`. The cut gain is exactly

`g(X) = |delta_M(X)| - |delta_B(X)|`.

Thus a cut is globally maximum if and only if `g(X) <= 0` for **every** subset `X` of `V`: every other cut is reached by choosing the symmetric difference of its vertex side with `S`. A cut is `k`-stable when this holds for every `X` with `1 <= |X| <= k`; if `k > |V|`, this simply ranges over the available subsets. Ties are permitted. Empty and full-vertex switches have gain zero. The competing cut after a switch need not retain a matching complement or any prescribed edge types; stability compares against all such vertex-set switches.

For a singleton vertex `v`, the gain is `2 deg_M(v)-3`. Therefore one-stability is equivalent to `deg_M(v) <= 1` for every vertex, so `M` is a matching. In particular, five-stability supplies the matching hypothesis needed below. This is not an assumption that arbitrary cuts have matching complements.

Put `W=V(M)`, `m=|M|`, `U=V\W`, `u=|U|`, and `n=|V|`. For a matching complement, `|W|=2m`. For any switching set put `t=|X|`, `r=|X intersect W|`, `a=e_M(X)`, and `b=e_B(X)`. The exact boundary identities are

`|delta_M(X)| = r-2a`,

`|delta_B(X)| = 3t-r-2b`,

and hence

`g(X)=2r-3t+2b-2a`.

These statements do not require connectedness. If `G` is disconnected, boundary gains add over its components, and the stability statements and density arguments below remain valid. The empty graph is harmless with the convention that the maximum degree of an empty induced graph is zero. Simplicity, triangle-freeness, and cubic degrees must not be dropped from the stated theorem: the proof uses them explicitly.

## 2. Exact three/four-switch theorem

**Claim.** For a matching cut complement in a finite simple triangle-free cubic graph, the following are equivalent:

1. Three-stability.
2. Four-stability.
3. `Delta(B[W]) <= 1`.

**Necessity.** If a vertex of `B[W]` has two distinct neighbors, these give a three-vertex cut-edge path `a-b-c` in `W`. No matching edge can lie inside this triple: the only possible extra pair is `a-c`, which would create a triangle. Each vertex has one matching edge leaving the triple. The triple has two internal cut edges, so its matching and cut boundaries have sizes 3 and 2 respectively. Its gain is 1. Consequently three-stability implies condition 3. Four-stability trivially implies three-stability.

**Sufficiency.** Suppose condition 3 holds. For `t=1`, the gain is at most `-1`. For `t=2`, at most one simple cut edge is internal, so the gain is at most zero. For `t=3`, if `r<=2`, triangle-freeness gives `b<=2`, and the gain is at most `-1`; if `r=3`, `B[W]` being a matching gives `b<=1`, again giving at most `-1`.

For `t=4`, the cut subgraph is bipartite and has at most four edges. If `r<=2`, this makes the gain at most zero. If `r=4`, the matching condition on `B[W]` gives `b<=2`, which suffices. If `r=3`, let `x` be the one vertex outside `W`. There is at most one cut edge among the three vertices in `W`; there can be at most three cut edges at `x`. Achieving four total would require all three edges at `x` and the edge between two of its neighbors, which is impossible. Thus `b<=3`, and the gain is again at most zero. This proves four-stability and the equivalence.

The independent replay also enumerates every internally feasible signed induced pattern on one through four vertices, with cubic boundary stubs and matching-complement saturation statuses. This includes patterns that might not admit a global completion, so it is a conservative superset. Under `Delta(B[W])<=1`, there are respectively **2, 13, 125, and 1,681** such normalized-side patterns; their maximum gains are **-1, 0, -1, and 0**. This finite calculation supplements the proof, rather than replacing its universal quantifiers.

**Density.** Every vertex in `W` has cut degree two, and at most one cut neighbor in `W`. Therefore at least `2m` cut edges join `W` to `U`. Their number is at most `3u`. Hence `2m<=3(n-2m)`, which is `8m<=3n`.

Counting endpoints, not distinct neighbors, is essential: several vertices of `W` can share a neighbor in `U`; the capacity `3u` already handles that. Repeated components cause no problem because the counts add. Equality requires all vertices of `W` to have one cut neighbor in `W`, and every vertex of `U` to send all three incident edges to `W`.

Since the matching covers `W` and `B[W]` is another matching, `G[W]` consists of alternating paths and cycles. A cycle has equally many matching and cut edges. Every cycle crosses any cut an even number of times, so the number of cut edges on such an alternating cycle is even; its total length is divisible by four. This assertion does not mean every component is a cycle.

## 3. The sharp 16-vertex example

The graph has vertices `0,...,15`, cut side `S={8,...,15}`, and these 24 unordered edges:

```
(0,1) (2,3) (4,5) (8,9) (10,11) (12,13)
(1,12) (5,8) (3,10) (4,13) (2,9) (0,11)
(0,14) (1,15) (2,15) (3,14) (4,14) (5,15)
(8,7) (9,6) (10,6) (11,7) (12,6) (13,7)
```

Direct checks establish simplicity, connectedness, triangle-freeness, and cubic degrees. The first six edges are precisely `M`. The next six are `B[W]`, a perfect matching on the twelve saturated vertices. Thus the cut is four-stable, has size 18, and attains `m=6=3n/8`.

Switching `X={0,3,4,10,14}` gains one. Its cut-induced tree has edges `14-0`, `14-3`, `14-4`, `3-10`; the matching and cut boundary sizes are four and three. Direct enumeration of all subsets of each size through five gives maximum gains `-1,0,-1,0,1`.

The cut with vertex side `S*={1,2,5,6,8,11,13,14}` has 22 edges. The two pentagons

`0-11-10-3-14-0` and `2-9-8-5-15-2`

are vertex-disjoint, hence also edge-disjoint. Every cut omits at least one edge from each odd cycle, so every cut has at most `24-2=22` edges. This is a complete human certificate for the global optimum. It applies to `S*`, **not** to the original size-18 cut.

Independently counting crossing edges for each of all `2^15=32,768` normalized cuts confirms maximum 22 and exactly one normalized maximizing mask, **26982**, where vertex 0 is outside the chosen side. The packet's own checker uses a different recurrence; both algorithms agree.

The original cut's fixed-`M` positive witness, in vertex order, is

`(0,15,9,6,3,12,15,0,4,11,7,8,13,2,2,13)`.

Every matching edge has xor difference 15 and every cut edge has difference in `{1,2,4,8}`. This example occurs within the direct stable family at `(n,m)=(16,6)`; displaying its sharpness certificate does not add another sampled record to the 33,400 count.

## 4. Five-switch restriction and density

**Claim.** In a five-stable cut, if an unsaturated vertex `x` has three neighbors `a,b,c` in `W`, none of these neighbors can have a cut neighbor `d` in `W`.

Five-stability first gives the matching complement and the three/four-switch theorem. Suppose `a-d` is such a cut edge. The five vertices `x,a,b,c,d` are distinct: simplicity distinguishes `a,b,c`; `d` is saturated while `x` is not; and `d=b` or `d=c` would create a triangle through `x`. The four edges `xa,xb,xc,ad` are cut edges. Further cut edges from `d` to `b` or `c` violate the matching condition on `B[W]`; the remaining possible cut edges are excluded by the cut sides. There is no internal matching edge: among `a,b,c` such an edge would form a triangle with `x`, `d` lies on the opposite cut side from these three vertices, and `x` is unsaturated. Thus `r=4`, `t=5`, `b=4`, and `a=0`, yielding gain one, a contradiction.

For the density argument let `a0=e(B[W])`, and let `n_i` count vertices in `U` with exactly `i` neighbors in `W`, for `i=0,1,2,3`. Every one of the `2a0` endpoints of `B[W]` has exactly one cut neighbor in `U`. The forbidden configuration shows this neighbor cannot be counted by `n_3`. Counting these incident edges gives

`2a0 <= n_1+2n_2`.

All cut edges from `W` to `U` are counted by

`4m-2a0 = n_1+2n_2+3n_3`.

Adding yields

`4m <= 2n_1+4n_2+3n_3 <= 4u`.

Since `u=n-2m`, this gives `m<=n/3`. Shared unsaturated neighbors and disconnected graphs are handled by these edge-incidence counts. The argument does not show a characterization of five-stability or sharpness of `n/3`, and neither is claimed. Additional five-vertex induced subgraphs can have positive gain.

The known global bound `m<=3n/10` is numerically stronger but concerns globally maximum cuts. It cannot be used as a replacement for this local-stability theorem without supplying global optimality.

For a connected graph, every globally maximum cut spans a connected subgraph: if the cut subgraph were disconnected, some one of its components would have an edge to another component because the original graph is connected. All such boundary edges belong to `M`, while no cut edge leaves the component. Switching that component would improve the cut. For disconnected `G`, the proper statement is connectivity of the cut subgraph within each connected component of `G`.

## 5. The fixed-status 19-edge core

The core has vertices `0,...,13` and edges

```
(0,1) (0,4) (0,11) (1,2) (1,8) (2,6) (2,12)
(3,5) (3,12) (4,7) (5,9) (5,13) (6,7) (6,10)
(7,9) (8,9) (8,10) (11,12) (11,13)
```

Its cut side is `{1,3,6,7,8,11,13}` and its matching edges are

`{(0,4),(1,8),(2,12),(5,9),(6,7),(11,13)}`.

It is exactly the first-round 21-edge graph with cut edges `(3,10)` and `(4,13)` removed, as independently checked against the retained authored first-round graph. All vertices have degree three except `3,4,10,13`, which have degree two. These are the only available ports in any cubic supergraph preserving the existing vertices and edges.

### Prescribed-extension obstruction

A fixed-`M` extension has labels in the four-dimensional binary cube, uses xor 15 on matching edges, and a unit direction on cut edges. On the pentagon `0-1-2-12-11-0`, exactly one edge has difference 15. The four unit directions therefore xor to 15. With four unit terms, each coordinate must occur once. Translation and coordinate permutation normalize the labels to

`f(0)=0, f(1)=1, f(2)=3, f(11)=4, f(12)=12`.

The audit verifies all `16*24=384` pentagon translation/direction-order normalizations. The matching edges then force `f(4)=15`, `f(8)=14`, `f(13)=11`.

Write `N(z)={z xor 1,z xor 2,z xor 4,z xor 8}`. Edges `2-6`, `6-7`, and `4-7` give

`f(6) in N(3) intersect N(0) = {1,2}`.

If `f(6)=1`, the unit two-edge path `6-10-8` would join labels 1 and 14, whose Hamming distance is four. This is impossible, so `f(6)=2`.

Edges `5-13`, `5-9`, and `8-9` give

`f(5) in N(11) intersect N(1) = {3,9}`.

Because `6-7` and `5-9` are matching edges, the unit edge `7-9` says `f(6) xor f(5)` is a unit. With `f(6)=2`, only `f(5)=3` remains. But the unit two-edge path `5-3-12` would join labels 3 and 12, again at Hamming distance four. Contradiction.

A separate finite backtracking calculation after the justified normalization tests 304 candidate labels and finds no fixed-`M` completion; it imports no packet solver. The hand argument already proves impossibility, so there is no dependence on solver timeout or exhaustion claims.

### Why cubic amplification preserving the core fails

For `X={1,2,6}`, the matching boundary is `{(1,8),(2,12),(6,7)}` and the cut boundary is `{(0,1),(6,10)}`. For `Y={7,8,9}`, the matching boundary is `{(1,8),(5,9),(6,7)}` and the cut boundary is `{(4,7),(8,10)}`. Each gain is one.

Every vertex in both triples already has degree three in the core. In any cubic completion retaining this **injectively embedded** core, no new edge can meet any of these six vertices. Their entire boundaries and prescribed edge statuses are therefore unchanged. Either triple remains an improving switch. Hence no such completion can make the prescribed cut globally maximum, even if arbitrarily large gadgets are attached at the four ports. The two gains are used separately; no gain for the union is assumed.

This conclusion does not cover identifying core vertices, subdividing/replacing edges, changing their cut statuses, or simulating constraints by another gadget. Those operations change the specified core. Nor does it say every completion is homomorphic to the Clebsch graph.

The core itself has the unrestricted positive witness

`(0,1,3,9,1,8,2,3,5,7,13,4,11,0)`.

All 19 differences belong to `{1,2,4,8,15}`. Thus the contradiction concerns the prescribed matching, not an unrestricted Clebsch homomorphism.

## 6. Complete retained finite scope

All records were read individually and independently checked for simple edges, connectedness, cubic degrees, triangle-freeness, the actual cut complement, matching incidence, vertex-label domain, and every unit/antipodal edge difference. Generator-specific matching placement, cut-side parameters, per-group indices, stability flags, group counts, and endpoint identities were checked as applicable.

### Pentagon construction

Exactly 200 records occur for each `k` in `{6,8,10,12,16,20,30,40}`, at order `n=5k`: **1,600 records, all distinct as labeled graph–cut pairs**. Every graph consists of the declared vertex-disjoint pentagons plus a cross-cut perfect matching, whose edges join different pentagons. There is exactly one omitted edge per pentagon. The cycles prove at least `k` omissions for every cut, and the prescribed cut omits exactly `k`, certifying its global optimality. All 1,600 prescribed cuts extend. These are selected cuts of constructed graphs, not all maximum cuts of those graphs.

### Small defects

Exactly 1,000 records occur for every pair with `n` in `{14,16,18,20,22,24,28,32,40}` and `m` in `{4,5}`: **18,000 records and 17,999 distinct labeled graph–cut pairs**. The matching splits as `2+2` across the sides for `m=4`, and `4+1` for `m=5`. The cut-side sizes satisfy the stated cubic side-degree identity. Exactly **9,184** retained records satisfy the three/four-stability invariant. All records extend; global optimality is not asserted.

### Rejection-based stable construction

Exactly 1,000 records occur at `m=6` for each `n` in `{16,18,20,22,24,28,32,40,48}`: **9,000 records and 8,989 distinct labeled graph–cut pairs**. Every record is three/four-stable and extends. The excluded interrupted `m=8` attempt contributes no records, no coverage, and no negative conclusion. The final frozen generator contains only the nine retained groups.

### Direct stable construction

Exactly 200 records occur for each of these 24 `(n,m)` pairs:

`(16,6), (20,6), (28,6);`

`(22,8), (26,8), (34,8);`

`(28,10), (32,10), (40,10);`

`(32,12), (36,12), (44,12);`

`(44,16), (48,16), (56,16);`

`(54,20), (58,20), (66,20);`

`(80,30), (84,30), (92,30);`

`(108,40), (112,40), (120,40)`.

These are **4,800 distinct labeled graph–cut pairs**, all three/four-stable and extending. Global optimality is not asserted.

### Cross-family duplicates and non-global examples

The total is **33,400 records and 33,386 distinct labeled graph–cut pairs across the four families**. Summing within-family distinct counts gives 33,388, but there are two cross-family overlaps, both at `(n,m)=(16,6)`:

Both overlaps are between the rejection-based stable family and the direct stable family. Their operational record identifiers are omitted; the overlap count and its effect on the aggregate distinct count are retained.

These counts use the actual labeled edge set and cut-side vector, not graph isomorphism classes. No nonisomorphism claim is made.

The remaining 31,800 records are not automatically global-maxcut certificates. Direct checks give explicit non-global examples from each other family:

- An authored small-defect example `(14,4)`: prescribed cut 17, actual maximum 19. Switching `{2,7,9}` gains one.
- An authored rejection-based stable example `(16,6)`: prescribed cut 18, actual maximum 22. Switching `{0,2,6,8,13}` gains one.
- The authored direct stable example `(16,6)`: the sharpness example, prescribed cut 18 and actual maximum 22.

The first two graphs and their positive witnesses are explicitly displayed in [ADDITIONAL_EXAMPLES.md](ADDITIONAL_EXAMPLES.md), while the third is displayed above. The reported exact maxima in these examples were obtained by counting every normalized cut. They are scoped to these three records. No assertion is made about the global optimality of every other record in these families.

All four sets are deterministic constructed samples. They are not exhaustive graph catalogs, uniform random samples, nonisomorphic catalogs, or exhaustive sets of cuts. Certificate multiplicity is not extra coverage. No inference about untested inputs follows.

## 7. Independent implementation, replay, and adversarial controls

The independent mathematical replay imported no submitted code, CSP solver, or external graph library. It uses explicit runtime exceptions, never correctness-critical `assert` statements. The original mathematical checker was also run separately in all three optimization modes; its output matched the retained reference byte for byte.

The independent replay checks the incoming root manifest pin, complete payload inventory, individual sizes and hashes, all 33,400 witnesses, group indices/counts, duplicate counts, the sharp graph, the core, and the abstract small induced patterns. Missing or truncated inputs cannot be silently skipped. It verifies the input packet again after completing the calculations.

The independently authored control suite supplied positive controls plus **18 negative controls**: wrong witness, out-of-domain label, false extension flag, duplicated edge, missing edge, loop, changed cut side, wrong pentagon count, changed stability flag, wrong defect, changed cut breakpoint, missing declared file, extra file, extra empty directory, modified payload bytes, altered manifest count, truncated certificate file, and symlink substitution. Mutations are confined to disposable copies or in-memory records. All controls reject as intended in ordinary Python, `-O`, and `-OO`; their serialized outcomes agree byte-for-byte. The frozen source packet is unaffected.

A separate reproduction process independently compiled all four sources with `g++ (Debian 14.2.0-19) 14.2.0`, flags `-std=c++17 -O2`, then ran their full retained default scopes. All compiler diagnostics are empty. Every output certificate file and every corresponding search log agrees byte-for-byte with the frozen input. This establishes deterministic reproducibility on the tested compiler/runtime; it is not a claim of cross-platform byte identity for standard-library shuffle implementations.

No solver negative result is needed to accept a retained positive witness. No timeout, interrupted process, partial group, or unretained sample was treated as unsatisfiability or exhaustiveness.

## 8. Scholarly-source scope and provenance

The inspected arXiv-v2 background PDF is 284,638 bytes with SHA-256 `aaefc77c1421e5c56d733d12561e198333b73e612c10135aa1361bf462d2ccf2`, identified on its first page as arXiv:math/0602580v2, 23 October 2009. Its abstract/introduction states the `4/5` cut bound for triangle-free graphs of maximum degree three, and attributes the historical results to Hopkins–Staton and Bondy–Locke. The latter is the cited source for the maximum-degree-three formulation in the introduction. No connectedness or bridgelessness restriction is introduced there.

For a cubic graph, `|E|=3n/2`, so the cited theorem gives a globally maximum cut complement of size at most `(1/5)|E|=3n/10`. This algebraic consequence is correct. It does not constrain every locally stable cut, and the 16-vertex example demonstrates why that distinction matters.

The public [DeVos–Šámal author manuscript](https://iuuk.mff.cuni.cz/~samal/papers/clebsch/clebsch.pdf) and [publisher abstract](https://onlinelibrary.wiley.com/doi/abs/10.1002/jgt.20580) were also inspected on 12 October 2026. The source supports the target formulation and bound attribution. The currently served author PDF is not claimed byte-identical to the retained arXiv-v2 file; reference numbering differs between versions. No original proof of the Hopkins–Staton/Bondy–Locke cut theorem or the paper's high-girth homomorphism theorem was independently audited here.

The bibliographic entry checked is J. Adrian Bondy and Stephen C. Locke, *Largest bipartite subgraphs in triangle-free graphs with maximum degree three*, Journal of Graph Theory 10 (1986), no. 4, 477–504. This report does not reproduce the paper's source text.

A separate lineage check rejected missing or changed archival inputs and verified the original authored search implementation, the original 14-vertex graph, and the public arXiv-v2 source PDF. The operational identities of the first two inputs are excluded from this edition. The public PDF metadata is retained above. This lineage check was distinct from mathematical certificate checking; missing provenance must not be reported as verified provenance.

The original independent replay was self-contained relative to its retained complete computational inputs. Those programs, raw collections, and runtime artifacts are not distributed here. The full mathematical arguments, small authored examples, reported counts, and substantive acceptance limits remain available in this edition.

## 9. Corrections and acceptance conditions

There is no required correction to the mathematical conclusions in [SWITCHING_PROOFS.md](SWITCHING_PROOFS.md). The following qualifications must be preserved whenever the result is summarized or reused:

1. Keep the original computational inventory distinct from the prose edition. Do not imply excluded programs or samples are distributed or directly replayable here. The public manifest is a closed list of only the distributed prose and permitted metadata.
2. Say “33,400 graph–cut records,” not “33,400 distinct graphs.” If giving aggregate distinctness, use **33,386 labeled graph–cut pairs** after cross-family deduplication.
3. Attribute global optimality to the 1,600 pentagon-family prescribed cuts and the separately identified maximizing cut of the sharpness graph; do not transfer it to all other samples or to the sharpness graph's original cut.
4. State the core barrier for an injectively retained core with all its cut/matching statuses preserved. It does not rule out a redesigned or simulated core.
5. Keep five-stability's condition necessary only, make no sharpness claim for `n/3`, and retain the stronger cited global bound's distinct hypotheses and unaudited-proof status.
6. The original mathematical verifier checked record counts and mathematics but did **not** itself enforce the incoming manifest or full file inventory. Use the independent fail-closed wrapper when making an integrity-verified replay claim. The original command remains a valid mathematical replay on the pinned packet; it alone is not an integrity attestation.
7. Treat normal/optimized runtime verification, deterministic generation replay, and the hand proofs as distinct evidence. No finite sample or successful solver run establishes the open universal statements.

No remote change, branch update, publication, or modification of the input packet was performed. The audit deliverables are frozen separately with an exact manifest and an external hash pin. Read-only filesystem modes supplement the cryptographic pin; they are not claimed to make the files immune to an authorized owner changing permissions.

## 10. Reproduction boundary for this prose edition

The original independent replay and its positive and negative controls were run under normal Python, -O, and -OO, with explicit runtime exceptions active in every mode. A separate process regenerated the full deterministic constructed samples, and an additional check verified archival input lineage. The source material remained unchanged. These are prior audited results, not commands runnable from this edition.

The distributed proofs, finite small examples, exact parameter lists, aggregate counts, negative-control descriptions, and public source metadata permit independent mathematical review and reimplementation of the specified checks. They do not include the retained raw samples, generator implementations, random seeds, runtime artifacts, or their identifiers. Exact byte-for-byte reproduction of those original runs requires material outside this public edition. No claim that the complete finite runs can be independently replayed from these files alone is made.

The edition's own manifest records actual distributed file hashes and byte counts. Its editorial acceptance process separately tests closed inventory, preservation of proof and audit text, privacy boundaries, and explicit small certificates. Those edition checks should not be confused with rerunning all original finite experiments or reproving the external signed theorem.
