> Editorial scope: This is the complete authored text of the accepted third-round source document, with operational identities and reproduction directions editorially removed or relabeled. Mathematical arguments and finite-scope counts are preserved. References to candidate status, packet contents, or narrower review scope record the original stage; the final combined decision is in [ACCEPTANCE_REPORT.md](ACCEPTANCE_REPORT.md). This public edition contains prose and public verification metadata only. It contains no programs, raw certificates, dataset contents, source documents, or runnable bundle. Original and distributed identities are different; [PUBLIC_MANIFEST.json](PUBLIC_MANIFEST.json) identifies only the files actually distributed.

# Candidate elementary one-versus-four extension lemma

Authored 12 October 2026. This is a proof originally submitted for independent mathematical review. The complete independent acceptance is reproduced in ONE_VERSUS_FOUR_AUDIT.md.

## Statement

Let G be finite, simple, triangle-free and subcubic. Let X,Y be a cut whose complement M is a matching. Suppose M has exactly one edge rs in Y and at most four edges in X. Then the prescribed M-class extends to the Clebsch graph: cut edges have unit-vector differences in F_2^4 and M-edges have difference J=1111. Global maximality is unnecessary.

This extends the second-round elementary construction for at most two X-demands. Combined with the authored one-versus-five obstruction, if both are accepted, the bound four is sharp for the number of demands opposite one prescribed edge.

## Cube facts and signed notation

Each cube parity has four antipodal pairs. Fix an odd cube vertex h. Label the even vertices by signed colors ±1,...,±4 so that +i is a neighbor of h and −i is its antipode, a neighbor of h+J. Any at most three same-parity cube vertices without an antipodal pair have a common cube neighbor. For the common-neighbor fact, translate one listed vertex to0. Each other distinct vertex has weight2; if two remain, their two-element supports intersect because disjoint supports would be antipodal. A unit vector in their intersection is a common neighbor; lists of size0,1,2 are immediate. The four neighbors of h occupy distinct antipodal pairs because two such neighbors have difference of weight2, never4. These are also Lemmas2.1–2.2 of the preceding round's candidate proof.

Write R=N_B(r) and T=N_B(s), where B is the cut. Triangle-freeness gives R∩T=∅ and prevents either R or T from containing both endpoints of an X-demand. Both sets have size at most two.

Assign each of the k≤4 X-demands a distinct magnitude in {1,2,3,4}. Its two endpoints receive opposite signs. Orient any demand touching R or T so that its R endpoint is positive and its T endpoint is negative. The restrictions just noted guarantee consistency. A demand touching neither set has a free orientation, to be chosen below. All constraints between already colored demand endpoints are automatically satisfied: different magnitudes cannot be antipodal, and two endpoints of the same demand cannot share a B-neighbor by triangle-freeness.

## Boundary singletons

Let U be the unmatched X-vertices in R∪T, and b=|U|≤4. Put ε_u=+1 for u∈R and −1 for u∈T. We will color u by ε_u l(u), with l(u)∈{1,2,3,4}.

Create an ordinary simple graph H on U. Join u,v exactly when they belong to opposite sets R,T and share some ordinary Y-vertex y∉{r,s}. Same-set pairs can never receive antipodal colors and impose no constraint. Duplicate occurrences give just one H-edge.

For a fixed orientation of the X-demands, let A(u) contain a magnitude i exactly when an endpoint p of the demand of magnitude i shares an ordinary Y-neighbor with u and has color −ε_u i. Let L(u)={1,2,3,4}\A(u). Thus the needed boundary coloring is precisely an ordinary proper list coloring of H from L.

Vertex u has at most two ordinary Y-neighbors. Each supplies at most two other X-neighbor incidences, giving at most four slots in total. Each distinct H-neighbor and each distinct forbidden magnitude in A(u) uses at least one separate slot. Consequently

|A(u)|+d_H(u)≤4, hence |L(u)|≥d_H(u).

Moreover, each nontrivial component of H has a vertex with strict inequality. To see this, choose any H-edge uv, witnessed by an ordinary Y-vertex y, with u∈R and v∈T. If y has no third X-neighbor, both endpoints have fewer than four possible slots in total. Otherwise let w be that third neighbor. If w is a colored demand endpoint, its sign is opposite to only one of ε_u,ε_v, so its slot contributes no forbidden magnitude at the other endpoint. If w∈U, it is on the same boundary side as one endpoint, so that slot contributes neither an H-neighbor nor a forbidden magnitude there. If w is another unmatched X-vertex, it is still uncolored and contributes to neither quantity. Thus at one endpoint |A|+d_H≤3, yielding |L|≥d_H+1.

A connected graph with lists of size at least degree and one strict surplus vertex is list-colorable by a direct greedy argument: root a spanning tree at the surplus vertex, color vertices in reverse tree order, and color the root last. Every nonroot vertex has an uncolored parent, so fewer than its degree many colors can have been forbidden when it is processed; the root has a surplus color. Therefore every nontrivial H-component is colorable for every orientation of the demands.

## Ensuring the isolated lists are nonempty

If k≤3, every L(u) contains an unused magnitude. Suppose k=4. An isolated u could have L(u)=∅ only if its four ordinary-neighbor slots are four demand endpoints, one from each of the four distinct demands. Let Z be the set of isolated vertices with this structural property, regardless of the present signs. Then |Z|≤b.

There are at most |R∪T|−b≤4−b boundary vertices lying on demand edges, and hence at most 4−b demands whose orientation is forced by R or T. Therefore at least b of the four demand orientations are free. Inject Z into these free demands. For each u∈Z, orient its assigned free demand so that the unique endpoint of that demand occurring in u's four slots has sign ε_u. Its magnitude then remains available in L(u). Different u receive different free demands, so these requirements are independent. An isolated u∉Z cannot have all four magnitudes forbidden. All isolated lists are therefore nonempty, while the preceding degree and surplus bounds remain valid for nontrivial components.

Choose the orientations just described and properly color H from L. This assigns all boundary singletons while preserving the hemispheres needed at r and s.

## Completing the map

Color each remaining unmatched X-vertex in any order. It has at most three ordinary Y-neighbors, each with at most two other X-neighbors. Thus at most six already assigned X-colors can forbid their antipodes. At least two of the eight signed colors remain available. Choose any one. There are no remaining hemisphere restrictions because every R∪T vertex is already assigned.

Now no ordinary Y-neighborhood contains an antipodal pair, and every such neighborhood has at most three vertices. Choose its common odd cube neighbor independently. Set f(r)=h and f(s)=h+J. Their neighbor images lie in the prescribed positive and negative hemispheres. All X-demands are antipodal by construction, as is rs. This gives the required fixed-M extension.

## Scope

The argument covers all finite subcubic triangle-free graphs with this matching-cut distribution, not merely cubic graphs or a finite catalog. For a cubic graph, degree summation gives 3(|X|−|Y|)=2(|M∩E(X)|−|M∩E(Y)|). With five total demands this forces the distribution4+1, so the lemma covers every cubic matching cut complement of size5. With exactly one demand on the smaller side, the allowed larger-side counts are1,4,7,...; consequently the authored cubic1+7 obstruction has the smallest possible number of demands within that one-versus-many cubic subclass, conditional on acceptance of this lemma and that obstruction. It does not cover the mixed2+2 distribution with four total demands. No signed degree-choosability theorem is used here. The only external background is the Clebsch/cube formulation; all coloring steps are elementary.
