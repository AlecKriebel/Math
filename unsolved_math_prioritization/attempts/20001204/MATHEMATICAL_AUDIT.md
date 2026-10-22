# Independent audit: restricted binary hierarchical quartic classifications

Date: 10 October 2026 (UTC).

## Verdict and scope

**Accepted as proved restricted results.** Theorems A, B, and C in the reviewed manuscript are mathematically sound under their stated conventions. They do **not** solve the general AIM Problem 28 / problem 20001204. No priority or global novelty determination is made.

The distributed [mathematical report](MATHEMATICAL_REPORT.md) has 22,059 bytes and SHA-256 `4ed04726c3a48b8006d86592623735abee930a190dab58a57c461e07e0a96328`. This AI-assisted, unrefereed audit is a scoped mathematical review, not external human peer review, journal acceptance or formal proof-assistant certification.

The report explicitly includes analytic circuit certificates, ghost-column reductions and the at-most-two-facet transportation argument. These details make its restricted conclusions self-contained.

The review independently checked:

- The quadratic Graver classification, including all actual/ghost/empty-ground-set cases.
- The four explicit circuit vectors and their indispensable Lawrence lifts.
- The exact Lawrence identity and its big-facet interpretation.
- Both directions of simplex attachment, cone removal, and grouped-state restriction.
- Every branch of the three-facet classification and its exact-degree subfamily.
- Primary attribution and the distinction between established machinery and the manuscript's restricted synthesis.

The accepted proof contains the finite analytic certificates it needs. This proof-only edition retains those authored certificates and the written audit. Supplemental programs and computational outputs are not distributed and are not prerequisites for reading or verifying the proof.

## 1. Conventions and elementary reductions

The empty face is included. Consequently the total-count margin is recorded, every kernel vector has equally large positive and negative parts, and the degree convention is unambiguous. A simplex on its actual ground set has the full table as a margin and therefore has zero kernel. The complex consisting only of the empty face on the empty ground set has matrix `[1]`, also with zero kernel. The void complex is not admitted.

### Induced restriction

Let S be a subset of the specified ground set. Extend a table on S by putting all outside coordinates in state zero. For any ambient face T, its margin either vanishes at an incompatible outside state or equals the margin on T intersect S. This proves the asserted kernel embedding, since every induced face is itself an ambient face. A conformal summand has no support outside the embedded cells. It therefore corresponds to a conformal summand of the original move. Primitivity is preserved.

For Markov degree the manuscript correctly imposes the additional actual-vertex hypothesis. The one-variable margins of the outside vertices can then be fixed with zero count in state one. Nonnegativity forces the entire fiber into the embedded cells. A path within this ambient fiber is exactly a path in the restricted fiber. Thus any ambient degree bound descends. Theorem A only needs the unconditional Graver statement; no unavailable Markov minor theorem is being used there.

### Repeated columns and ghosts

For a repeated-column configuration, a primitive move with opposite signs among copies of one column contains a conformal degree-one transfer; it must equal that transfer. Otherwise aggregation is sign-preserving and nonzero. A proper conformal decomposition of the aggregate can be allocated among the occupied copies, and conversely a conformal summand of a sign-preserving lift aggregates conformally. This proves the manuscript's formula for Graver degree, including an underlying zero kernel.

The corresponding Markov-degree formula also holds:

`md(repeated A) = max(1, md(A))`, when at least one repetition is present.

For the upper bound, lift every base move in every distribution among copies and add unit copy transfers. A feasible projected step lifts by taking its subtracted occurrences from occupied copies. Once the projected target is reached, unit transfers adjust the copy counts. For the lower bound, aggregate paths between arbitrary lifts of any two base-fiber tables; projected moves have no larger degree. A repeated configuration has a nonzero degree-one fiber, so its degree cannot be zero. This argument does not incorrectly treat fixing a ghost state as an exposed fiber face.

These facts settle the empty-ground-set and ghost-only cases: a ghost-only model has Markov and Graver degree one, whereas its ghost-deleted model has degree zero. They preserve the thresholds and exact degrees used in Theorem C.

## 2. Independent verification of the obstructions

The following direct elimination certificates use the report’s displayed cell lists. Each equation is an ordinary facet-state margin. No rank program or enumeration is needed for this argument.

All displayed vectors have zero full facet margins. Their supported rational kernels are one-dimensional. Each generator has a unit coordinate, so its supported integer kernel is its integer span. Since no coordinate of the generator is zero, its support is minimally dependent. This proves both the circuit and primitive properties.

For completeness, here is the analytic elimination certificate, independent of a rank program. In each case label the distinct support cells in lexicographic order by z1, ..., zm.

- Three isolated vertices: `z1+z2+z3 = z4+z5 = z1+z2+z4 = z1+z5 = 0`, forcing `t(-1,2,-1,-1,1)`.
- Path: `z1+z2 = z3+z4 = z5+z6 = z3+z5 = z1+z3 = 0`, forcing `t(-1,1,1,-1,-1,1)`.
- Two disjoint edges: `z1+z2 = z3+z4 = z5+z6 = z1+z3 = z2+z5 = 0`, forcing the same coefficient vector.
- Four-cycle: `z1+z2+z3+z4 = z5+z6 = z7+z8 = z1+z2 = z5+z7 = z1+z5 = z3+z6 = 0`, forcing `t(-1,1,1,-1,1,-1,-1,1)`.

Every listed equation is a facet-state margin. Substitution verifies all remaining margin equations. The accompanying report includes these systems and the full ordered cell lists.

The higher boundary obstruction is also valid. For the boundary of a k-vertex simplex, each codimension-one margin sets the sum of the two cells differing in the omitted coordinate to zero. Moving in each coordinate forces every entry to be the zero-cell entry times its parity sign. Hence the integer kernel is generated by the parity vector. It has degree `2^(k-1)` and is primitive.

## 3. Theorem A: quadratic Graver classification

The proof is exhaustive.

1. After removing ghosts, a minimal nonface of size at least three induces a simplex boundary. The preceding obstruction gives Graver degree at least four. Therefore every quadratic-Graver complex must be flag.
2. In a flag complex let H be its missing-edge graph. A triangle in H induces three isolated vertices in the complex, so its Graver degree is at least three.
3. If H is triangle-free and contains two disjoint edges, consider their four endpoints. At most two cross edges are possible. Two cross edges must be disjoint, or they make a triangle. The induced graph is consequently two disjoint edges, a path, or a four-cycle. Its complement is respectively a four-cycle, a path up to relabeling, or two disjoint edges. All three are already obstructed.
4. A triangle-free graph with no two disjoint edges is a star plus isolated vertices. When two edges ab and ac exist, any edge avoiding a must be bc to meet both, which is prohibited by triangle-freeness. A graph with zero or one edge is immediate.

Conversely, the clique complex of the complement of a nonempty star has facets `S union {c}` and `S union L`, where S is the isolated-vertex set of H. Conditioning on S gives independent `2 by 2^|L|` transportation blocks. In one block every kernel vector has column pairs `(a_j,-a_j)` with sum of the a_j equal to zero. A positive and a negative coefficient extract a conformal unit rectangle. Thus a primitive vector is exactly such a rectangle, of degree two. A primitive vector cannot use two independent blocks. The edgeless missing graph yields a simplex and degree zero.

Two incomparable facets with one singleton exclusive side have precisely this star form; their intersection is S and the other exclusive side is L. Both exclusive sides are nonempty because they are distinct facets. Ghost deletion then gives the stated equivalence on a specified ground set.

## 4. Theorem B: big facets and Lawrence fibers

Every face of a big-facet complex either lies in F or contains v. Therefore splitting into the two v-slices gives exactly the link margins separately in each slice and the pointwise sum of the slices. This is the asserted Lawrence matrix, up to redundant rows. Keeping all of F as the link's specified ground set is essential: deleting its ghosts before forming the lift would discard distinct F-cells and would give the wrong model.

For any homogeneous integer configuration A, the binary Lawrence lift has kernel vectors `(g,-g)`. Conformal decomposition of g into primitive moves yields a path coordinatewise between any pair of nonnegative endpoints. Each lifted move has degree twice that of its base move. This proves the upper degree bound.

For the lower bound fix a primitive g. The two tables `(g+,g-)` and `(g-,g+)` share a Lawrence statistic. In any other fiber table z, the pointwise-sum margin forces `z0+z1=|g|`. Set `h=g+-z0`. Coordinatewise, where g is positive, h lies between zero and g; where g is negative, h lies between g and zero; where g vanishes, h vanishes. The slice margins give `Ah=0`. Primitivity leaves only h=0 or h=g. Hence the fiber has exactly those two points. No smaller move or sequence of smaller moves can connect it. This proves the exact identity `md(Lambda(A))=2 gd(A)` and the claimed indispensability.

The translation to facets is also exact:

- Since v is actual, its link contains the empty face and is never void.
- If the ghost-deleted link is a simplex on U, its sole facet U is properly contained in F. Otherwise the face `F union {v}` would contradict maximality of F. There is therefore at least one link ghost, and its Graver degree is exactly one. The original complex has exactly two facets and Markov degree exactly two.
- If the link has the two-facet star form, its Graver degree is two, with or without ghosts. The original complex has precisely the displayed three facets and Markov degree exactly four.
- Any other link fails Theorem A and has an explicit primitive move of degree at least three. Its lift requires degree at least six.

A saturated simplex is correctly excluded from the big-facet hypothesis: deleting a vertex does not leave a maximal face. The apparently degenerate case F empty cannot satisfy that hypothesis with v actual. The ghost-only link case is valid for nonempty F and gives two disjoint simplices of Markov degree two. No hidden exception affects the conclusions.

The example with facets `[123][14][24][34]` is the Lawrence lift of the three-isolated-vertices configuration. Its degree-six indispensable move is therefore verified. This demonstrates why a quadratic Markov basis of the link is insufficient: the Lawrence invariant is the Graver degree.

## 5. Theorem C: three facets, attachments, and exact degrees

### Zero, one, or two facets

Under the empty-face convention a finite complex has at least one facet. With one facet it is saturated on its actual vertices. With two facets, conditioning on the full intersection leaves ordinary row-and-column-sum transportation fibers. These are connected by quadratic rectangles. The accepted proof supplies a direct feasible distance-decreasing construction: select a deficit cell and surplus cells in its row and column, subtract from the two surplus cells and add at the deficit and the opposite corner. The l1 distance to the target decreases by at least two. The argument terminates and works independently in each conditioned stratum. Ghost restoration only introduces linear transfers.

### Private-variable attachment: both bounds

The relevant lemma is the following. Let K be a complex on V, let S be a face of K, and let E be a disjoint group of new variables. Adjoin the simplex on `S union E`, and call the result L. Then

`md(K) <= md(L) <= max(2, md(K))`.

For the upper bound, project a table by summing out E. Given a feasible base move, select its removed occurrences from the current expanded table. The positive and negative occurrences have the same S-margin, so pair them within each S-state. Give each added occurrence the E-state of its paired removed occurrence. This preserves the complete `(S,E)` margin, keeps the move feasible, and does not increase its degree. After a base path is followed, two expanded tables with the same base projection differ only in couplings between E-states and remaining base cells at each S-state. The relevant row and column sums are fixed, and quadratic transportation swaps connect the couplings.

For the lower bound, put every E variable in one state. The corresponding one-variable margins set the counts of all other states to zero. Nonnegativity forces the entire expanded fiber into these fixed-state cells. The `(S,E)` margin adds no new constraint to the base fiber, because the S-margin is already recorded in K. This gives an actual fiber isomorphism and a degree-preserving converse.

Consequently every threshold at least two is preserved, and exact degree is preserved whenever the reduced degree is at least two. The possible jump from a zero-kernel base to degree two is not silently excluded.

Each group private to one of the original three facets fits this lemma: its separator is that facet with its private variables deleted, an existing face in the projected complex. The groups can be removed and restored successively. The argument remains valid when projected facets coincide or become nonmaximal.

### Cone and grouping reductions

Variables in all three original facets occur together in every retained facet. Conditioning on their full state splits the model into independent copies. Markov degree is the maximum degree of these identical blocks, hence unchanged. This is valid even when a block has zero kernel.

The remaining pair-only overlap groups are disjoint, with sizes a, b, c. Replacing each group by a supervariable is a bijection on table cells, not a marginal approximation. Its states are full binary strings on that group, and the pairwise supervariable margins are exactly the retained facet margins. The core is therefore the no-three-way-interaction configuration with state counts `2^a, 2^b, 2^c`.

If a group is empty, one core facet contains every remaining variable. Its kernel is zero. Restoring the private groups produces degree at most two, so the first branch of the theorem is correct, including cases with two or three empty groups.

### Quartic and nonquartic cores

If all three groups are positive and at least two have size one, choose one of the two-state supervariables as the Lawrence coordinate. The base is `2 by t` independence. Its primitive moves are only quadratic rectangles, so the core has Markov degree exactly four. The attachment and cone bounds preserve that exact degree.

If at least two groups have size at least two, retain three states from each of those groups and two from the third. This is a valid face restriction of fibers. The full margin of each individual group is recorded, since the group is a face of the core. Setting its excluded state counts to zero forces all cells using those states to vanish. The restricted configuration is exactly `2 by 3 by 3`, with no extra constraints.

The `3 by 3` independence configuration has an alternating simple six-edge cycle. Its supported kernel is its integer span: balance at successive vertices forces equal alternating coefficients. It is primitive. Its binary Lawrence lift has a two-point fiber of degree six. The restricted fiber is an actual ambient fiber face, so every Markov basis of the core requires degree at least six. Private-variable and cone restoration cannot lower the bound.

This proves both directions of the three-facet threshold classification.

### Exact degree when one overlap group is binary

For an `r by s` independence configuration with r,s at least two, orient the bipartite edges according to the sign of a nonzero zero-margin table. Row and column balance gives a nonnegative integral circulation. It contains a directed simple cycle, whose signed unit vector is conformal to the table. A primitive table must equal that cycle vector. Conversely a unit simple cycle is primitive, since balance around its support forces a constant coefficient.

The longest simple cycle in the complete bipartite graph uses `min(r,s)` vertices on each side, and one exists. Its move degree is `min(r,s)`. Taking the binary Lawrence lift gives exact Markov degree `2 min(r,s)`. Substituting `r=2^b`, `s=2^c` proves `2^(1+min(b,c))`. Here b,c are positive, so no one-state transportation exception is invoked. The remaining attachment and cone operations preserve this value because it is at least four.

## 6. Primary sources and novelty boundary

The original [AIM problem document](https://aimath.org/WWN/compalgstat/compalgstat.pdf), version 27 March 2004, places Problem 28 on page 8 after the Seth Sullivant heading on page 7 and before the Elizabeth Allman heading. The manuscript's corrected attribution and unrestricted problem scope are accurate.

The attribution of the main existing mechanisms is also supported:

- [Bernstein and O'Neill, arXiv 1704.09018v2](https://arxiv.org/abs/1704.09018v2), Section 5, supplies the nucleus cycle description and explicit ghost, cone, and binary Lawrence Graver operations. Proposition 5.3 covers the transportation-cycle interpretation.
- [Bernstein and Sullivant, arXiv 1508.05461v2](https://arxiv.org/abs/1508.05461v2), Definition 3.4 and Proposition 3.5, identify big-facet models with Lawrence liftings. Their normality theorem is a different classification and cannot by itself serve as the claimed quartic criterion.
- [Engström, Kahle, and Sullivant, arXiv 1102.2601v5](https://arxiv.org/abs/1102.2601v5), Theorem 4.3, gives the codimension-zero Lift/Quad construction. A simplex intersection has the required independent separator grading. Lemma 5.3(2) gives the block-diagonal cone reduction. The manuscript also gives direct arguments adequate for the particular uses here.
- [Petrović and Stokes, arXiv 0910.1610v4](https://arxiv.org/abs/0910.1610v4), Section 4, invokes the classical Lawrence theorem. Example 6.1 demonstrates that its homological degree predictions do not give a converse classification.
- [Král', Norine, and Pangrác, arXiv 0810.1979](https://arxiv.org/abs/0810.1979), already establish the at-most-four criterion for binary graph models in terms of exclusion of a K4 minor. The manuscript does not claim this known graphical result as new.
- [The 25-year Markov bases survey, arXiv 2306.06270v3](https://arxiv.org/abs/2306.06270v3), has a 9 January 2024 revision, matching the version recorded in the manuscript.

The audit does not infer a graph-minor result for arbitrary complexes, does not replace Graver degree by Markov degree in the Lawrence identity, and does not replace quartic generation by normality or unimodularity. Theorems A/B/C may be direct consequences or short syntheses of established literature. The manuscript's explicit disclaimer of a global novelty claim is appropriate.

A bounded literature search and source check cannot establish universal novelty or certify that the general AIM problem remains open in all current literature. The operative conclusion is narrower and fully supported: **the reviewed manuscript proves its three restricted statements and does not provide the requested unrestricted characterization.**
