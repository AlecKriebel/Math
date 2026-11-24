# Independent acceptance audit: small prescribed Clebsch classes

12 October 2026 UTC. Problem 3209 / OPG434, queue row 1752.

## Verdict

**ACCEPT the restricted mathematical results in the main restricted proofs and their separately frozen high-degree addendum.** No correction to their proofs or stated degree ranges is required. The arbitrary-size one-sided result retains its explicitly cited signed degree-choosability dependency. This acceptance is not a proof of that external theorem, the full fixed-maximum-cut strengthening, or the cubic weak pentagon conjecture, and it makes no novelty claim.

The computational corroboration also passes, subject to an important reproducibility boundary: the submitted program is assert-based and is **not** an optimization-safe acceptance checker. Its normal replay is accepted; its `-O` and `-OO` runs receive no semantic-validation credit. A separately authored, explicit-exception checker supplies fail-closed input, witness, and negative-control validation in all three modes. The original program's optional missing-catalog branch is not accepted as completion of the advertised catalog checks.

No frozen candidate file was changed. No publication or remote mutation was performed by this audit.

## 1. Exact scope reviewed and split freeze

The original review verified the main proof, the separately frozen addendum, and their complete declared inventories before and after independent computation. The split freeze was deliberate and accepted. This prose edition preserves the mathematical and audit arguments; operational file inventories, original proof-file identities, checkers, raw collections, and runtime-artifact identities are excluded. Its own distributed bytes are listed by the public manifest. The original review did not mutate or publish its input.

The public versions are [SMALL_COMPLEMENT_PROOFS.md](SMALL_COMPLEMENT_PROOFS.md) and [HIGH_DEGREE_ADDENDUM.md](HIGH_DEGREE_ADDENDUM.md).

The reviewed claims are:

1. In a finite simple triangle-free graph, any cut complement of at most two edges has the specified cube/antipode extension, with no matching or degree assumption.
2. In a triangle-free subcubic graph, a matching cut complement of at most three edges has that extension.
3. In a triangle-free subcubic graph, an arbitrary-size one-sided matching cut complement has that extension, using the stated external theorem.
4. The authored 15-vertex graph has a unique maximum cut up to side exchange, with a three-edge matching complement, but no such extension.
5. More strongly, that same graph has no homomorphism into any loopless triangle-free target of maximum degree at most seven, hence none into the Clebsch graph.

The last graph has maximum degree eight. Claims 4–5 do not furnish a cubic or subcubic counterexample.

## 2. Cube lemmas and grid extension

### Same-parity sets of at most three

If a common neighbor exists, any two images are at cube distance at most two, so an antipodal pair is impossible. For the converse, translate one chosen image to zero. Every other distinct same-parity, non-antipodal image has weight two. With two such images, their supports must intersect: disjoint weight-two supports in four coordinates are complements and would make those two images antipodal. A unit vector in their intersection is adjacent to zero and both images. One or two distinct images, repeated images, and an empty neighborhood create no additional problem.

The eight vertices of each parity form four antipodal pairs. A cube neighborhood has four elements and never contains an antipodal pair, so it takes exactly one representative from each pair. Antipodal translation exchanges its representatives with the other representatives. These are precisely the facts required later. The proposed four-image limitation is genuine: the images 0, 3, 5, 6 have no common neighbor despite containing no antipodal pair.

### Distance-envelope proof

For terminal coordinates `(a,b)`, set `p=a+b`, `q=a-b`. The identity between Manhattan distance in `(a,b)` and the maximum of the two coordinate differences in `(p,q)` is exact. Thus pairwise terminal distance compatibility makes both terminal scalar assignments 1-Lipschitz.

On each component containing terminals, the distance-envelope minima recover the given scalar values. Each minimum is 1-Lipschitz because graph distance satisfies the triangle inequality. For a vertex `v`, all summands in each envelope have the same parity: terminal-coordinate parity plus the parity of the terminal-to-`v` distance equals the fixed bipartition parity at `v`, with the chosen component offset. Both envelopes consequently have that parity. Across an edge their differences are odd and have absolute value at most one, hence are each exactly `+1` or `-1`.

Undoing the coordinate change gives integral coordinates. The four possible pairs of scalar increments map to `(1,0)`, `(-1,0)`, `(0,1)`, `(0,-1)`, so no edge is collapsed or sent to a diagonal. The sawtooth map on the integer path fixes its target interval and takes consecutive integers to consecutive integers, including across folds and for negative inputs. Applying it separately to the two coordinates preserves a grid edge. Terminal coordinates remain fixed. Terminal-free components map to one grid edge, including the harmless one-vertex case.

There is therefore no hidden connectivity, injectivity, terminal-distinctness, or nonnegative-envelope assumption. The candidate's grid lemma is a complete proof and uses no retract theorem.

## 3. Degree-free complements of size at most two

The empty-complement case is the ordinary two-color map to a cube edge. For one internal edge, its endpoints lie on the same cut side. If connected in the cut graph, they have even distance at least four: distance two would create a triangle with the internal edge. The specified distance map follows a length-four cube path and then alternates its final two vertices. In a bipartite component adjacent distance levels differ by exactly one, so this is a homomorphism and the two demand endpoints receive antipodes. If the endpoints are in different cut components, those components can be oriented independently.

When two demand edges share an endpoint, the same root-distance construction puts each reachable opposite endpoint at the antipode. Every other component containing an opposite endpoint can send their common cut side to that same antipode. Multiple such endpoints in one component cause no conflict. These are all nonmatching possibilities with two edges in a simple graph.

For two disjoint demands on the same cut side, the four assigned corners of a `2 by 2` grid require distance four only for the demand pairs and distance two for the other pairs. Triangle-freeness supplies the former bound, distinct same-side vertices the latter. Parity agrees.

For demands on opposite cut sides, the two possible kinds of short cross edge require one or the other grid dimension to be one. A requirement of both kinds would select two cross edges sharing an endpoint; together with one of the internal demands they form a triangle. Thus the requirements are consistent. Choosing dimensions `(1,3)` or `(3,1)` satisfies every actual cross edge, while every cross pair without an edge has either infinite distance or odd finite distance at least three. Same-side demand distances are at least four. Separate components impose no distance conditions, and coordinate parities have the required component offsets.

The prefix-bit embedding of this rectangle in four cube coordinates is edge preserving, and its opposite corners are antipodal. This completes every case without a degree bound.

## 4. Three matching demands in subcubic graphs

For one-sided demands, give each demand a distinct even antipodal pair. With at most three demands one pair remains available for all unmatched vertices on that side. The only antipodal image pairs then come from demanded adjacent endpoints. Such endpoints cannot share a cut neighbor, by triangle-freeness. Each opposite-side vertex has at most three neighbor images, so the cube lemma applies independently.

The genuinely mixed case has side distribution `2+1` or `1+1`. Put the single opposite-side demand at `r,s`, choose desired images `h,h+J`, and use the four antipodal pairs indexed by the neighborhood of `h`. The cut neighborhoods `R=N_B(r)` and `T=N_B(s)` are disjoint. Neither can contain both ends of an internal demand, since that would make a triangle.

For each of the at most two demands on the first side, its own unused pair can therefore be oriented so that members of `R` take the representative adjacent to `h` and members of `T` the antipodal representative adjacent to `h+J`. The only potentially conflicting requirements would be the prohibited common membership or both endpoints in the same neighborhood. Reserve the third pair's first representative for remaining `R` vertices and ordinary vertices, and the fourth pair's second representative for remaining `T` vertices. These two background images are not antipodal, nor antipodal to any demand image.

Consequently all first-side antipodal image pairs still correspond exactly to internal demands. The degree-three cube lemma handles every other opposite-side vertex. At `r,s`, the explicit images `h,h+J` work by construction. This argument permits repeated non-antipodal colors and disconnected graphs. It does not claim the four-image common-neighbor implication that fails at higher degree.

## 5. Arbitrary-size one-sided matching: dependency and independent reduction audit

### External contract

The external result is Schweser–Stiebitz, *Degree choosable signed graphs*, [arXiv:1507.04569v1](https://arxiv.org/html/1507.04569v1), Theorem 2.1(a),(e). For a connected loopless signed multigraph uncolorable from lists of at least the vertex degrees, it forces equality of list sizes with degrees and brick blocks. The relevant brick classes are balanced complete graphs, balanced odd cycles, unbalanced even cycles, doubled complete graphs, and doubled odd cycles; doubled edges have opposite signs. Colors are integers with inequality `c(u) != sign(uv)c(v)`, and degrees count multiplicities.

Those exact conventions and clauses were rechecked in the primary manuscript, including the definition of an uncolorable pair. The prior dependency/application audit was read as additional evidence, not substituted for checking this reduction. The locally available 21-page primary PDF has 202,056 bytes and SHA-256 `727b9d254300f36b91c7ff2e02e1538c259ff0075316da2dfffb454ee2da960e`. The current audit does not independently re-prove the external theorem or certify the journal-version numbering. The manuscript dependency remains explicit.

### Auxiliary graph and palette

Collapse each matching edge on the demand side to an entity; unmatched vertices remain singleton entities. Assign opposite signs to the two members of each pair. For two neighbors `x,z` of a vertex on the other side, put an auxiliary edge with sign `-epsilon_x epsilon_z`. Its signed inequality is exactly the prohibition against the original signed colors being negatives, which is exactly non-antipodality after the fixed bijection to even cube vertices.

No loop can be generated: two neighbors in the same entity would form a triangle with that entity's matching edge. Same-sign duplicate constraints are redundant and may be removed. Opposite-sign parallel edges encode distinct conditions and both must stay. The palette is explicitly the eight nonzero colors `{+/-1,+/-2,+/-3,+/-4}`, so there is no inference from an odd palette containing zero.

A singleton contributes at most three cut incidences, each generating at most two auxiliary edges, hence degree at most six. A pair contributes at most two incidences per member and at most two constraints per incidence, hence degree at most eight. These are multiplicity-counted degrees after only same-sign deduplication.

### Saturation and obstruction exclusions

If a component cannot be colored from the fixed eight-color lists, the external theorem makes every auxiliary degree exactly eight and every block a brick. All listed bricks are regular. In an end block of a component with a cut vertex, a non-cut vertex has its full degree eight inside that block, so the block is eight-regular. Its cut vertex would then have degree at least nine in the component. This contradiction leaves a single eight-regular brick, necessarily balanced `K9` or `2K5`.

At any degree-eight entity every prior bound must be tight. It is a pair, both original members have cut degree two, each neighboring opposite-side vertex has cut degree three, and no same-sign deduplication incident with it has reduced the count. Its neighboring degree-three vertex gives three distinct entities and three constraint signs whose product is negative. All three generated pairwise constraints survive at least once. In a supposed balanced `K9` they are its unique triangle edges, contradicting balance. This sign-product argument is invariant under switching and does not assume a particular orientation of the matching pairs.

For a supposed `2K5` component, its five entities represent ten original vertices, each of cut degree two. Every adjacent opposite-side vertex has three neighbors among those ten: its constraints connect its three entities to the same auxiliary component. Thus the twenty original cut incidences must equal three times the number of those opposite-side vertices. The equation is impossible. This count is in the original cut graph, not in the signed multigraph, and it does not assume distinct neighborhoods.

Every auxiliary component is consequently colorable from the required palette. Map back to even cube vertices. Matching endpoints become antipodes, and each opposite-side neighborhood has no antipodal pair. Its size is at most three, so a common odd neighbor exists. These choices are independent precisely because that side has no internal demand edges. This proves the stated one-sided result and explains why it does not silently cover mixed-side complements.

## 6. Authored high-degree graph and unrestricted addendum

The graph consists of the three adjacent terminal pairs, a vertex `t`, and eight vertices representing all binary transversals of the pairs. Every transversal vertex sees `t` and its chosen endpoint from each pair. The cut graph has 32 edges; adding the three pair edges gives 35 edges on 15 vertices. Its degree sequence is eight fours, six fives, and one eight. Triangle-freeness follows because no transversal takes both endpoints of an internal edge.

For the exact maximum-cut certificate, orient any nontrivial switched set away from `t` and let `k` be its number of transversal vertices. If `k>=4`, their edges to `t` give at least four crossing cut edges. If `k<=3` and the set contains a terminal, that terminal has at least `4-k` neighbors outside; these edges and the `k` edges to `t` are distinct and give at least four. If there is no terminal, the nonempty set consists of transversal vertices and has at least four crossing cut edges. Thus every nontrivial cut of the bipartite part has size at least four.

Switching changes the displayed cut's size by the number of crossed demand edges minus the number of crossed bipartite edges. The first number is at most three and the second at least four. Every nontrivial switch therefore makes the cut strictly smaller. The displayed 32-edge cut is the unique maximum up to exchanging sides, and its complement really is a matching of size three.

For the fixed-class obstruction, translation can normalize `f(t)=0`. All terminals are then even. Different demand pairs must occupy different antipodal cube pairs because any selected endpoints from two different pairs share a transversal neighbor. The image of `t` must occupy the fourth pair because it shares a neighbor with every terminal. Each neighbor of `f(t)` selects exactly one representative of every terminal pair. Each such cube neighbor therefore serves exactly one of the eight distinct requested transversals; only four neighbors are available. At least four of the transversal vertices cannot be mapped. Collapsing two demand pairs into the same antipodal pair or identifying a terminal with `f(t)` does not evade the argument: both are already excluded by the common-neighbor constraints.

The addendum is stronger and independent of cube parity. Any two different transversal vertices select opposite endpoints of some adjacent terminal pair. If their images coincide in a loopless target, their common image and the two terminal images are three distinct, mutually adjacent vertices. A triangle-free target forbids this. All eight transversal images are thus distinct neighbors of `f(t)`, requiring degree at least eight. The conclusion for every loopless triangle-free target of maximum degree seven follows. The Clebsch target is loopless, 5-regular and triangle-free under the five-generator description, so its unrestricted specialization is valid.

## 7. Scope and residual problem

The switching identity holds for every cut. A global maximum satisfies every switching inequality. In a subcubic graph, even singleton-switch optimality forces the complement to be a matching, but this necessary condition does not imply global optimality.

For a cubic graph, counting total degrees on the two cut sides gives `3(|X|-|Y|)=2(m_X-m_Y)`. At total complement size four, divisibility leaves only `2+2`; at total size five it leaves only `4+1` up to reversal. These statements in the candidate are correct. The established results do not handle every mixed complement of four or more edges, and the one-sided signed reduction does not coordinate the two common-neighbor choices across a demand on the other side.

The high-degree counterexample remains outside the cubic target even with the stronger addendum. Its sharpness concerns the degree-free universal guarantee at demand counts two versus three, not a proof that any degree threshold or order is optimal. Neither the finite catalogs nor the source check establishes a full literature-status or novelty claim.

## 8. Independent computation and fail-closed controls

The submitted normal program was executed from a temporary copy against already available catalog inputs. Regenerated results and the authored example matched the retained references byte for byte, as did the addendum check. Catalog records and primary source documents were excluded from the audit deliverables and remain excluded here.

The separate independent checker did not import the submitted verifier. It rebuilds the grid construction, small-complement constructions, signed reduction, positive signed coloring, graph6 parser, high-degree graph, cut enumeration, and terminal obstruction checks. Every acceptance check uses an explicit exception rather than `assert`. Its expected counts, graph properties, and stream digests are compared to pinned metadata or the frozen report.

Reproduced totals:

- 186 same-parity cube subsets, of which 130 have a common neighbor; all neighborhood antipodal-pair identities.
- 15,758 valid degree-free instances: 6,561 same-side disjoint-demand cases, 9,072 opposite-side cases, and 125 shared-endpoint cases.
- 4,000 seeded mixed `2+1` subcubic cases, with every edge histogram reproduced.
- Every normalized cut of all 141 supplied through-14 records: 949,536 cuts; 372 small matching complements and 136 one-sided matching complements, with independently checked witnesses.
- 300 authored one-sided cubic cases, from 20 to 100 vertices, demands up to size 30. All six regenerated construction streams matched their retained references. The tests exercise auxiliary degree eight, same-sign duplicate removal and opposite-sign parallel constraints.
- All 16,384 normalized cuts of the 15-vertex example. The sole maximizing normalized mask is 127, its score is 32, and the bipartite edge connectivity is four. All 16,383 nontrivial normalized switching inequalities are strict.
- All 512 normalized terminal assignments. None supports all eight transversals; the maximum is four. Exactly 48 assignments satisfy all pairwise non-antipodality restrictions.
- All 28 unrestricted pair-separation witnesses; the stated Clebsch target properties.

Additional independent coverage:

- 600 authored grid-extension cases over six rectangle shapes, all with terminal-free components; 4,020 fold adjacency checks over dimensions 1 through 20 and integer inputs -100 through 100. The negative-input fold tests are explicit; the generated compatible envelopes happened not to produce negative final coordinates.
- 81 extra zero-/one-demand cases, including long paths and swapped cut sides.
- All 49 valid mixed cases with side sizes `(4,2)` and all 2,070 with side sizes `(5,3)`, plus a separate witness after every side swap.
- 256 signed-color/cube equivalences, all eight negative-triangle sign identities, and targeted same-sign and opposite-sign parallel fixtures.

Each of the normal, `-O`, and `-OO` runs rejects the same 32 negative controls. These include missing inputs; wrong bytes and hashes; missing/tampered main or addendum content; unexpected inventory entries; malformed graph6 length, bytes and padding; loops, duplicate edges and bad endpoints; invalid cut labels; triangles; degree overflow; nonmatching or wrong-side one-sided demands; invalid cube witnesses; incompatible terminal parity or distances; out-of-rectangle terminals; invalid dimensions; and a supplied cut graph inconsistent with its cut labels. Valid restored split-freeze content is also accepted.

The independent outcomes in the three modes were byte-identical. An AST check confirms the independent checker has no `assert` statements. Its optimization safety is supported by active negative controls, not merely by three zero exit codes.

For contrast, an intentionally invalid cube witness is rejected by the submitted verifier in normal mode but accepted in `-O` and `-OO`, because its assertions disappear. Those optimized candidate runs are explicitly not counted as verification. The normal candidate parser also lacks the strict graph6 byte/padding checks and mandatory input pins supplied by this audit. These are acceptance-process limitations, not discovered counterexamples to the written mathematics.

## 9. Final disposition

**All five precisely scoped claims are accepted.** No frozen mathematical correction is requested. The external dependency and the original verifier's input/optimization limits must remain visible in any acceptance summary. Reproduction of the complete advertised computational suite should use the explicit independent checker and require the exact inputs; the submitted normal checker is corroboration, not a standalone fail-closed certificate.

This prose edition retains authored mathematical analysis, full audit reasoning, counts, negative-control descriptions, and permitted public dataset/PDF metadata. It excludes programs, raw collections, runtime artifacts, copied sources, and their operational identities. The retained programs and exact authored samples are not distributed here; therefore this edition alone does not support byte-for-byte replay of the original runs. The audit does not certify catalog generation completeness or nonisomorphism, and no prior packet's pending acceptance was treated as a premise.
