# Adversarial audit: problem 30006563

Audit date: 2026-10-03. Verdict: **PASS for the precisely scoped partial-results packet.**

No mathematical or certificate defect requiring a HOLD was found. This is not a solution of the asymptotic problem, a novelty certification, or a claim to have excluded every later result in the literature. The author packet correctly makes none of those claims.

## Frozen input and independence

Audited input: the sibling `author` directory, containing 16 manifest-listed files plus `MANIFEST.json`.

Manifest SHA-256:

`d862a64b69ccfbf06f1c56dee1dcd8aedc86fccee2af0c325fb0897e31894dfc`

The manifest identity, all 16 byte counts and SHA-256 digests, and the absence of unlisted files were checked before and after the independent computations. The frozen input was not modified. No remote writes or additional construction/proof attempt were undertaken.

The audit did not merely rerun the author verifier. `independent_audit.py` imports no author module, executes no author script, reconstructs the coloring from an independent block-palette lookup, evaluates types as color histograms, checks disjointness using vertex masks, rebuilds the Boolean specification, validates every local truth assignment, and checks every proof-tree inference. It also independently reproduces the stated bounded searches and records a violating triangle pair for each of the 24 rejected row pairs.

Run from a disposable copy of this problem directory:

    python3 audit/independent_audit.py

Results are in `independent_results.json`; explicit failed-ansatz witnesses are in `ansatz_failure_witnesses.json`. These files live outside the frozen author directory. The original mathematical review and all of its scoped findings are preserved here; the local absolute execution path was replaced by this portable command.

## 1. Source and interpretation: PASS

The official MFO report record and its linked PDF were retrieved independently. Question 14 under David Conlon is on printed page 74, PDF page index 69. The available page image was also visually inspected and agrees with the retrieved text. The question concerns arbitrary edge-colorings, forbids two vertex-disjoint triangles with a color-preserving isomorphism, and imposes no properness requirement. It states the square-root baseline, the displayed upper bound n−4, the linear-growth conjecture, and the stronger possibility n−O(1). It attributes a lower bound c n^(1/2+ε), with ε>0 unspecified, to Conlon, Fox and Pham. The packet faithfully retains the unspecified exponent and distinguishes the announcement from a supplied proof. [Official report record](https://publications.mfo.de/handle/mfo/4435); [report PDF](https://publications.mfo.de/bitstream/handle/mfo/4435/OWR_2026_01.pdf?isAllowed=y&sequence=1).

The Conlon–Tyomkyn paper explicitly makes proper edge-colorings its main setting. Its results cannot simply be substituted for the unrestricted question. The packet handles this distinction correctly. [Primary paper](https://www.its.caltech.edu/~dconlon/repeats.pdf).

The Botler et al. primary-paper search excerpt likewise explicitly describes proper colorings. The direct PDF fetch timed out during this audit. The catalog URL was inaccessible through the available web tool; this audit does not independently assert its exact HTTP status or verify the catalog body. None of those access limitations affects the verified primary problem statement or the mathematical checks. The limited additional searches did not produce a new resolution, but are not proof of universal absence or historical priority.

## 2. Triangle types and deletion bound: PASS

For K3, every permutation of its three edges is induced by a vertex permutation. Consequently, equality of the actual color multiset, including multiplicity, is equivalent to color-isomorphism. It is not enough to compare unordered sets of colors. The independent checker additionally tested all 729 pairs of three-color edge assignments against all six vertex permutations.

There are q monochromatic types and q(q−1) types with one repeated and one singleton color: exactly q² non-rainbow types. Choose one triangle from each realized such type. Their vertex union S has size at most 3q². A non-rainbow triangle outside S would be disjoint from the chosen representative of its exact type, so the remaining clique has only rainbow triangles.

If two incident edges in that clique had equal colors, their completing triangle would be non-rainbow. Thus the induced coloring is proper and its order m is at most q+1. This gives n≤3q²+q+1 and the displayed quadratic-root lower bound. The cases m≤1 are harmless. No unjustified reduction from q² types to q colors appears.

## 3. Intersecting-family and center arguments: PASS

The elementary bound |F|≤9(n−2) for a nonempty intersecting triple family with no common vertex is valid. With T∈F and T_x avoiding x for each x∈T, every U∈F contains some x∈T and some y∈T_x. Since x∉T_x, this is a genuine pair of distinct vertices. At most nine pairs cover F, and each pair lies in n−2 triples.

For the restricted class in Attempt 2, B≤9q²(n−2). Cauchy–Schwarz gives

    W ≥ n(n−1)(n−1−q)/(2q).

A triangle with two colors contributes exactly one monochromatic cherry, a monochromatic triangle contributes three, and a rainbow triangle contributes zero. Thus W≤3B and the constant 54 in the displayed inequality is correct.

The asserted exponent follows without a hidden sign assumption. If n−1≤2q, then n=O(q); otherwise n−1−q>(n−1)/2, so (n−1)²<108q³. Both cases give n=O(q^(3/2)). This theorem is restricted; it does not establish an unrestricted n^(2/3) lower bound.

The center-deletion inequality is also valid: the count for noncentered types may be bounded using their original n-vertex families even after restricting to m surviving vertices. If q=o(n^(2/3)), then q³n=o(n³) and q=o(n). The displayed inequality therefore forces m=o(n); otherwise its left side is Ω(n³). The interpretation |C|=n−o(n) is correct. There is no established O(q) bound on C, and the packet does not pretend otherwise.

## 4. Edge-family, common-neighborhood, cut, and blow-up statements: PASS

A pairwise-intersecting nonempty edge family is a star or exactly the three edges of a triangle. The induction proving q≥s−2 is valid even when deleting a star center removes additional colors: the surviving palette has size at most q−1. If there are no star classes, the edge partition is into triangles, yielding q=binom(s,2)/3≥s−2 for s≥3.

If u and v have a common color-c neighborhood S, disjoint same-colored edges xy and zw in S produce the forbidden pair uxy and vzw of type {c,c,b}. This includes b=c. Hence |S|≤q+2. Small |S| cases are immediate; for |S|≥3 the preceding lemma applies.

For a monochromatic cut A,B, the argument with one side of size two correctly gives q≥n−4. If both sides have size at least three, their internal palettes must be disjoint: equal-colored internal edges can be completed by fresh opposite-side vertices to make disjoint repeats. Summing the two internal palette lower bounds yields n−4. No unsupported extra color is added for the crossing color.

Three doubled blocks in a uniform blow-up immediately give two transversals of the same three original blocks and thus equal-type, vertex-disjoint triangles. This is a universal obstruction to that specific uniform operation, not to arbitrary nonuniform constructions. The packet observes the distinction.

## 5. K7, K9, and private-star extension: PASS

The K7 hand proof correctly separates all four red-edge counts. The exact equality g(6)=g(7)=2 follows from the exhibited K7, restriction to K6, and the obvious impossibility of one color on six vertices.

The K9 construction was rebuilt from its written block rules. The following independent block enumeration explains all 84 triangles; A and B each have three vertices.

| Vertex pattern | Type | Count |
|---|---:|---:|
| AAA | 111 | 1 |
| AAB | 001 | 9 |
| ABB | 000 | 9 |
| BBB | 000 | 1 |
| AAz | 111 | 3 |
| ABz | 011 | 9 |
| BBz | 011 | 3 |
| AAx | 001 | 3 |
| ABx | 002 | 9 |
| BBx | 022 | 3 |
| AAy | 111 | 3 |
| ABy | 012 | 9 |
| BBy | 022 | 3 |
| Azx | 011 | 3 |
| Bzx | 112 | 3 |
| Azy | 011 | 3 |
| Bzy | 012 | 3 |
| Axy | 012 | 3 |
| Bxy | 222 | 3 |
| zxy | 012 | 1 |

This yields the claimed counts 10,12,9,18,16,6,7,3,0,3 in the type order 000,001,002,011,012,022,111,112,122,222. Every stated intersection certificate is correct. In particular, the nonstar families use two vertices from a fixed three-set, and the other families have the stated fixed vertex or fixed pair. Type 122 is absent.

Adding one new vertex with a fresh incident-edge color preserves admissibility: all new triangles contain that vertex and have a type using the new color; old triangles use none of it. Induction proves g(m+t)≤g(m)+t. With the K9 seed, the all-n conclusion g(n)≤n−6 for n≥9 is therefore a hand-proved theorem, not an extrapolation from finite tests.

Direct checks of the extensions at n=10,12,16 respectively cover 2,100, 9,240, and 80,080 disjoint pairs, and pass. These are consistency checks, not replacements for the induction. Stored K6 and K7 Boolean witnesses were independently validated as well.

## 6. K8 Boolean specification and UNSAT certificate: PASS

The lower bound has the advertised complete scope: arbitrary two-color edge assignments on all 28 edges of K8, with no properness restriction.

For each pair of vertex-disjoint triangles, equality of their numbers of color-1 edges is equivalent to color-isomorphism. There are binom(8,6)·10=280 unordered pairs. The 20 equal-count assignments on the six distinct edges of each pair give 20 six-literal clauses, each forbidding precisely that assignment. All 5,600 resulting clauses are distinct.

The audit rebuilt the required clause set independently by selecting equally sized color-1 subsets in each triangle. It verified equality with the certificate-indexed clause set. It also evaluated all 64 local assignments for every pair, totaling 17,920 truth-table checks: the clauses hold exactly when the two counts differ. This addresses missing constraints, sign reversal, spurious constraints, duplicate variables, and lost multiplicity.

Fixing the first edge to color zero is the sole symmetry assumption. It is complete because complementing all edge bits preserves equal-count versus unequal-count status. The independent checker explicitly confirmed closure of the clause set under global bit complement. No vertex normalization, seed restriction, or unproved symmetry reduction is part of this lower bound.

The strict independent proof validator checks each unit reason against the current partial assignment, verifies that its one remaining literal is the requested new assignment, verifies every leaf conflict, and requires both assignments to a previously unassigned branch variable. Its result is:

- 571 total nodes
- 285 branch nodes and 286 conflict leaves
- 3,847 validated unit assignments
- Maximum branch depth 15

A wrong-root-assumption negative control is rejected. The certificate proves conditional UNSAT under edge 0=0; complement symmetry completes the unrestricted two-color argument. Combining this with the K7 one-vertex extension and the K9 construction gives g(8)=g(9)=3. The lower bound remains computer-assisted, as the packet clearly says.

## 7. Bounded searches and failed recursion: PASS

Independent enumeration of the specified K7 extension reproduces 58 individually feasible rows, 26 canonical first rows, and the displayed K9 on the 27th tested combination. Sorting each of the A and B blocks is justified by independent vertex permutations preserving the K7 seed. No completeness of a wider seed search is claimed or needed for an upper witness.

The specified K9-to-K11 ansatz has 64 raw rows for each new vertex. Complete admissibility checks leave eight possible u rows and three possible v rows. All 24 combinations fail. This audit records an explicit forbidden pair for each combination, rather than trusting a status flag or the author's pruning routines.

This rules out only the stated rows to A and B, the fixed mutual color, and the fixed original K9. It supplies no lower bound for arbitrary four-color K11 and no universal obstruction to adding two vertices per color. The packet consistently states this limitation.

## Required repairs, optional clarifications, and remaining gaps

**Mandatory repairs: none. No HOLD condition identified.**

Two optional wording/reproducibility improvements would make the presentation more robust:

1. In the restricted no-common-center hypothesis, write “every realized non-rainbow type family.” This removes any empty-family convention ambiguity without changing the intended proof.
2. Tell readers to run the optional search scripts on a copy of the frozen packet. Those scripts overwrite their output JSON files, including run-time values, and therefore can legitimately invalidate the recorded manifest after a rerun. This is a packaging convenience issue, not a mathematical defect.

The unresolved substantive gaps are exactly the advertised ones: no unrestricted Ω(n) lower bound, no o(n)-color construction, and no proof or disproof that n−g(n) is bounded. A fixed-seed private-star extension preserves its deficit; making deficits unbounded would require further construction or amplification work. Neither the 24-case rejection nor the proper-coloring literature bridges these gaps.

**Final disposition: PASS as five partial attempts with verified scoped results and an unresolved original asymptotic question.**
