# Independent proof review: convex reduction and fixed-neighbor obstruction

## Verdict and exact scope

**Accept the elementary reductions, the explicitly exhibited representations, and both local-replacement obstructions, within the conventions below.** The degree-three representation corollary uses a specifically credited published convex-representation statement. This review does not independently fill in the deduction of that published statement from the general poset-separation theorem. Nothing reviewed here proves or refutes the intended general triangle-representation conjecture. No novelty or present literature-status claim is made.

The objects are an indexed finite family of nonempty closed **filled** convex sets in the plane. Hyperedges are precisely the inclusion-maximal index sets with a nonempty common intersection. The intended hypergraphs are finite and covered by their edges; the principal case is loopless and linear. All statements about perturbations concern unrestricted intersections. They do not concern one-sided contacts, disjoint interiors, triangle boundaries alone, or a selected list of incidence points.

The author supplied a convex-reduction report and a separate convention/math supplement. Both have received a full proof review here. The primary-source dependence, the supplement, and the new finite certificates are distinguished below. The distributed edition files are identified by the accompanying [public manifest](PUBLIC_MANIFEST.json). An initial checker that used Python assertions was not accepted as optimization-safe. The author replaced all such gates with explicit exceptions before the accepted replays.

## 1. Source dependence and convention boundary

The relevant chapter is de Fraysseix, Ossona de Mendez and Rosenstiehl, *Representation of Planar Hypergraphs by Contacts of Triangles*, LNCS 4875, pp. 125–136. Its first section defines finite hypergraphs with nonempty edges covering the vertices and calls loopless linear hypergraphs simple. On p. 135 it states that the incidence-dimension condition gives the required convex-set representation for simple hypergraphs. The following conjecture uses the broader word linear. [Publisher chapter](https://doi.org/10.1007/978-3-540-77537-9_15).

I read the local full text of the 2002 paper, including the proof of Theorem 2.1, and the relevant chapter sections. The 2002 proof constructs a projectively normalized map with a separation property for differences of common lower sets. The chapter credits this theorem for its convex-representation consequence but does not supply that deduction. The present report therefore treats the consequence as a credited dependency; it does not certify the stronger assertion that an arbitrary normalized dual-edge hull construction automatically has the correct entire nerve. The rapidly increasing coordinates can be chosen with base greater than the dimension, which supplies the growth inequality actually used in the separation proof. [Ossona de Mendez, *Realization of Posets*](https://jgaa.info/index.php/jgaa/article/view/paper48).

The reviewed proofs explicitly select filled triangles as their working convention. This is consistent with the preceding convex-set discussion, but the source does not separately formalize boundary-only versus filled triangles in the conjecture. It would be incorrect to attribute an explicit boundary/degeneracy definition to that source.

### Literal nested singleton issue

The maximal intersecting index sets of any family of sets form an antichain under containment. Consequently the linear hypergraph with edges {a} and {a,b} is impossible under maximal-family semantics, independently of geometry. Its incidence poset has the three strict relations a<e, a<f, b<f, where e={a} and f={a,b}. The orders a,e,b,f and b,a,f,e intersect in exactly these relations. The poset is not a chain, so its dimension is exactly two. The independent checker verifies all 12 ordered distinct pairs.

This is a convention mismatch, not a counterexample to the intended loopless problem. In a linear hypergraph, a properly contained edge can only be a singleton. If a linear hypergraph is Sperner, each singleton edge is an isolated component. Removing those components restricts the incidence poset and hence cannot increase its dimension. Conversely, after constructing the remaining finite representation, isolated singleton components can be placed as separate distant triangles. This proves equivalence of the loopless and Sperner-linear versions under the stated semantics. Deleting a nested singleton from a non-Sperner input changes that input and cannot be presented as preserving it.

## 2. Independent verification of witness compression

For every maximal edge e of an existing convex representation choose a common point p_e. Every nonempty face S of its nerve is contained in some maximal face, because the index set is finite. Define K_v as the convex hull of the points p_e for all edges e containing v. Coverage makes K_v nonempty. Finiteness makes it compact, and convexity gives K_v contained in the original object C_v.

If S is a face, a maximal edge e containing S supplies the same point p_e to every K_v with v in S. If S is a nonface, shrinking C_v to K_v cannot produce a common point. Thus every face and every nonface is preserved, not merely the pairwise intersection graph. If two distinct maximal edges had equal selected points, their union would also be a face, contradicting maximality. The empty index face is automatic, and the empty hypergraph is handled by the empty family.

At a vertex incident with at most three maximal edges, K_v has at most three generating points. It is therefore a point, a segment, or a filled triangle. This is a bound on vertex degree, not on the number of vertices in a hyperedge. No step implies such a bound for vertices incident with four or more edges.

## 3. Independent verification of stability and triangle inflation

For a nonempty subfamily S of nonempty compact objects having empty common intersection, put

    delta(S) = inf_x max_{v in S} dist(x,K_v).

This number is strictly positive. If it were zero, choose x_n with all the distances tending to zero. Distance to one fixed compact member bounds x_n; a subsequence converges. Closedness of every member then puts its limit in their common intersection, a contradiction. There are only finitely many S. Choose epsilon smaller than all positive gaps, or arbitrary positive epsilon if no nonface exists.

Every family with K_v contained in T_v and T_v contained in the open epsilon-neighborhood of K_v has the same nerve. Containment preserves faces. A point common to T_v for a nonface S would make every corresponding distance less than epsilon and contradict delta(S)>epsilon. Checking only empty pairs would be insufficient: the three sides of a triangle meet pairwise but have no common point.

For a nondegenerate old triangle, a slight dilation about an interior point contains the old triangle in its interior and is arbitrarily close. For a segment [a,b], let u=b-a and let n be its quarter-turn. Use the three vertices

    a-eta*u-eta*n, b+eta*u, a-eta*u+eta*n.

In the coordinates along u and n the base has longitudinal coordinate -eta and the tip 1+eta. Both old endpoints have zero transverse coordinate and longitudinal coordinates strictly between base and tip, so the entire old segment is strictly interior. Each new vertex is within sqrt(2)*eta*|u| of the old segment. Distance to a convex set is convex, so this bound holds on the whole new triangle. A point is treated by an arbitrarily small surrounding triangle. Choosing the perturbations within the common epsilon gives all nondegenerate triangles and preserves the full nerve.

This proves the triangle-only equivalence for unrestricted finite representations by triangles, segments, and optional points. All original selected witnesses become interior witnesses. Applying this result after witness compression proves the maximum-degree-three corollary **conditional on the credited convex-representation theorem described in Section 1**.

Rationalization also survives review. Interior witnesses have positive margins in finitely many triangles. Perturbing the triangle vertices sufficiently little preserves these margins. The nonface distance gaps persist under sufficiently small Hausdorff perturbations even without containment; containment was needed only for the old-face part of the earlier lemma. Rational coordinates are dense, so all vertices can be chosen rational. This is existential and makes no algorithmic complexity claim.

## 4. Strong fixed-neighbor obstruction

The central square is Q=[-1,1]^2. Its four leaves are the diagonal segments t(1,1), t(-1,1), t(-1,-1), t(1,-1), with 1<=t<=7/6. Four further segments are the sides of O=[-4/3,4/3]^2.

Each leaf meets Q at exactly its inner endpoint. The leaves are disjoint and miss the four outer sides. Q also misses those sides. Adjacent outer sides meet at a corner and all other pairs of sides are disjoint. No triple intersection occurs. Thus the entire maximal-edge family is the disjoint union of a four-leaf star and a four-cycle. An independent half-plane-feasibility implementation checked all 511 nonempty subfamilies and recovered exactly the asserted eight pairs.

Suppose a triangle or segment P replaces only Q. To retain the four leaf edges, it must contain points

    a=(t1,t1), b=(-t2,t2), c=(-t3,-t3), d=(t4,-t4),

where every t_i is at least one. These four points are vertices in the indicated cyclic order. One way to see this is that their two diagonals are on the lines y=x and y=-x and cross at the origin, interior to each diagonal. Their convex hull has area

    t1*t2+t2*t3+t3*t4+t4*t1 = (t1+t3)(t2+t4) >= 4.

Convexity forces this hull into P. Meanwhile preserving the hypergraph forbids P from meeting any outer side. P contains a leaf point in the interior of O. A segment from that point to any point of P outside the interior of O would cross its boundary. Hence P is contained in the interior of O.

For any triangle in a square of side s, its area is at most s^2/2. To prove this, maximize the absolute determinant of its three vertices over the compact product of three copies of the square. With two vertices fixed the objective is convex in the third vertex, so a corner can replace it without reducing the objective. Do this for all three vertices. Every resulting corner triple has area at most half the square. Here the upper bound is 32/9<4, contradicting the lower bound. A segment has area zero and is already excluded. The proof allows moving all four chosen leaf witnesses and allows enlarging the original central square; it only fixes the eight other objects.

The supplied three-order realizer was independently checked on all 272 ordered pairs of its 17 elements. Its dimension is exactly three, since its star component contains the three-leaf star incidence poset, whose dimension-three lower bound is proved in Section 5. No planar representation theorem is needed for this certification.

The hypergraph itself is readily representable by segments: use one horizontal segment crossed by four mutually disjoint vertical leaves, then draw a square boundary far away for the cycle. Thus the example rejects a universal independent local-replacement procedure. It supplies no obstruction to a coordinated global representation.

## 5. Supplementary arbitrary-k shrinking obstruction

For the star with center c and leaves u_i, put p_i=(i,i^2), assign P=conv{p_i} to c, and assign the vertical segment from p_i to (i,i^2-1/4) to u_i. The affine functional y-2ix+i^2 is zero at p_i, strictly positive at every other p_j, and strictly negative below p_i on its leaf. It follows that P meets that leaf exactly at p_i and that p_i is exposed in P. The leaf segments have distinct x-coordinates and are disjoint.

Any replacement T contained in P that preserves all leaf intersections must contain all p_i. Each remains extreme in T: any nontrivial convex expression in T would also express it nontrivially in P. Consequently a triangle or segment cannot do this when k>=4. Unlike Section 4, this argument assumes containment in P. It is correctly presented as the weaker inscribed-replacement obstruction.

The explicit orders place c first with the leaf-edge pairs in forward order, c first with those pairs in reverse order, and all leaves before c before all edges. Required incidences hold in all three. The first two orders reverse leaf pairs, edge pairs, and every nonincident leaf-edge pair; the third reverses each center-leaf pair. For the lower bound when k>=3, any two-order realizer would put every leaf before c in at least one order. Two leaves u_i,u_j must occur before c in the same order. That order has u_i<e_j and u_j<e_i, so the other order must have e_j<u_i and e_i<u_j. Together with the required incidences this gives the cycle e_j<u_i<e_i<u_j<e_j, impossible. Hence dimension equals three. The independent script verifies the displayed realizers and exposing evaluations for k=3,...,8, while the written argument proves all k.

## 6. Pair/triple full-nerve criterion

Let D(H) be the downward closure of a finite covered linear Sperner hypergraph. Suppose a set A has every subset of size at most three in D(H). Sets of size at most three are immediate. Otherwise choose three distinct elements a,b,c in A and an edge e containing them. For any other x in A there is an edge f containing a,b,x. Because e and f share a,b, linearity forces e=f. Thus e contains all of A. Every minimal nonface therefore has size at most three.

For arbitrary nonempty representing sets it suffices to realize each edge with a common point and to prohibit the nonedge pairs and triples. A common point for any unwanted larger subfamily would also give common points for all its pairs and triples, contradicting the preceding combinatorial statement. Conversely realizing every edge realizes every face. The Sperner condition then identifies exactly the maximal edges. This proof does not assume convexity or invoke Helly. The optional further reduction of positive common-intersection checks for planar convex sets uses Helly and is not needed for the acceptance here. Exact exhaustive checks cover all 109 covered linear Sperner hypergraphs on one through four labeled vertices as a regression, not as the general proof.

## 7. Five-vertex nonplanar example

The five supplied integer-coordinate segments lie on x=0, x+y=4, y=0, y=x-2, and y=x/3. Their indicated endpoints give exactly the pair-only maximal edges 12,23,34,14 and the triple maximal edges 135,245. The independent implementation checked all 31 nonempty subfamilies; there are 17 nonempty faces in total.

Every one of the 110 ordered distinct pairs in the supplied three-order certificate has the required incidence-order value. The induced subposet on vertex elements 1,2,3 and edge elements a=12,b=23,e=135 is the standard six-element example S3. Each of its three missing-incidence pairs needs reversal in some extension; two such reversals in the same extension would cycle through the two cross-incidences. This proves a dimension-three lower bound, while the supplied realizer proves the upper bound.

The nine supplied paths between branch classes {1,3,f} and {2,4,e} are incidence-graph paths, have distinct internal vertices, avoid all branch vertices internally, and account for every incidence-graph edge. They therefore prove that the graph is a subdivision of K3,3. This concerns the incidence graph and does not prevent arbitrary crossing segment representations of the hypergraph.

## 8. Computational acceptance and limitations

The independent geometry implementation converts each point, segment, or strictly convex counterclockwise polygon to rational closed half-planes. A nonempty bounded intersection has a vertex, possibly a degenerate endpoint or isolated point, at two independent active boundary lines. Enumerating those line intersections and checking every inequality therefore decides each tested common intersection exactly. This differs from the author's polygon-vertex and segment-intersection implementation.

All gates use explicit exceptions and run unchanged under ordinary Python, -O, and -OO. Each baseline includes six negative controls: an overlong leaf, an invalid realizer, an insufficient area contradiction, a spurious triple invisible in the pairwise graph, an incorrect thin-triangle construction, and a direct explicit-gate check. An additional harness alters only temporary copies and requires twelve mutation rejections, comprising four mutations under all three interpreter modes. The author's repaired harness was separately replayed. A final audit replay also caught nondeterministic ordering in an independent rejection diagnostic; the diagnostic was sorted before final acceptance, and the earlier sealed audit edition was retained as superseded. No timeout is treated as rejection, and no canonical input is mutated to produce a control.

The numerical certificates are finite checks. The compactness theorem, arbitrary-k lower bound, rationalization, and universal combinatorial statements rely on the written proofs above. The normalized realizer-coordinate experiment is not used for acceptance. The remaining general gap is real: witness compression may leave polygons with at least four exposed witnesses, and the fixed-neighbor example prevents a universal one-object conversion of an arbitrary initial representation. No conclusion about the general conjecture follows beyond the stated subclass and local obstructions.
