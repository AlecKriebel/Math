# Finite linear hypergraphs of incidence dimension at most three: reductions and a local obstruction

## Status and conventions

This is a partial mathematical investigation, not a proof or counterexample to the intended triangle-representation conjecture. No novelty or current-open-status claim is made. The substantive convention is a finite **simple** hypergraph in the terminology of de Fraysseix, Ossona de Mendez and Rosenstiehl: edges are nonempty, cover the vertex set, have size at least two, and any two distinct edges share at most one vertex. More generally, the elementary reductions below apply to finite Sperner hypergraphs (no edge properly contains another).

The representation is an indexed family of nonempty **closed filled** convex sets in the plane. Its hyperedges are the inclusionwise maximal subfamilies having nonempty common intersection. There is no contact-only, disjoint-interior, one-sidedness, or selected-contact-point requirement. Intersections of every subfamily, rather than merely pairwise intersections, are controlled.

The published starting fact used below is the statement on p. 135 of the 2008 paper that every finite simple hypergraph whose incidence poset has dimension at most three admits a convex-set representation with exactly these maximal-common-intersection hyperedges. The paper credits the general poset representation theorem in Ossona de Mendez (2002). The 2008 paper states the consequence without giving an explicit hull-coordinate formula. We use the stated consequence and do not assert that an arbitrary application of its 2002 separation theorem immediately gives a correct full nerve.

## 1. Witness compression preserves the entire nerve

The empty hypergraph is represented trivially by the empty indexed family; in the arguments below assume V is nonempty. Let H=(V,E) be a finite Sperner hypergraph with union E=V, represented by convex sets C_v. For each e in E choose a point p_e in the common intersection of the C_v for v in e, and put

    K_v = conv{p_e : e in E and v in e}.

Every K_v is nonempty, compact, and contained in C_v. For every nonempty subfamily S of V (the empty face is automatic):

* If S is a face of the original nerve, it is contained in a maximal face e because V is finite. The point p_e belongs to every K_v for v in S.
* If S is not a face of the original nerve, intersection(K_v : v in S) is empty, since K_v is contained in C_v.

Consequently, K and C have exactly the same nerve and hence exactly the same maximal-intersection hypergraph. Distinct maximal edges have distinct chosen witnesses: if p_e=p_f, all sets indexed by e union f contain that point, contradicting maximality when e and f are distinct.

If deg_H(v) <= 3, K_v is a nondegenerate triangle, a nondegenerate segment, or one point. The claim concerns vertex degree (the number of incident hyperedges), not hyperedge cardinality.

## 2. Compact finite nerves are stable under sufficiently small outer perturbations

Let K_v be a finite family of nonempty compact subsets of R^2. For every nonempty S with empty common intersection define

    delta_S = inf over x in R^2 of max_{v in S} dist(x,K_v).

Then delta_S > 0. Otherwise choose x_n for which the maximum distance tends to zero. For any fixed v_0 in S, distance(x_n,K_v0) tends to zero, so compactness of K_v0 makes x_n bounded. A convergent subsequence has a limit in every closed K_v, a contradiction.

There are finitely many subfamilies. If at least one has empty intersection, choose epsilon strictly smaller than the minimum of their positive delta_S. If there are no empty subfamilies, choose any epsilon>0. Whenever

    K_v subset T_v subset {x : dist(x,K_v) < epsilon}

for every v, the whole nerve is unchanged. Old faces survive by containment. If an old nonface S had a point x in all T_v, then max_{v in S} dist(x,K_v) < epsilon < delta_S, a contradiction. This proof controls empty triple intersections even when all three pairs intersect, and also controls all larger subfamilies.

### 2.1 Every point, segment, or triangle has arbitrarily close containing nondegenerate triangles

For a genuine triangle, dilate slightly about its centroid. The original triangle is in the interior of the larger triangle, and its Hausdorff distance tends to zero with the dilation factor.

For a nondegenerate segment [a,b], put u=b-a and let n be u rotated by 90 degrees. For eta>0 use the triangle with vertices

    a-eta*u-eta*n,  a-eta*u+eta*n,  b+eta*u.

It is nondegenerate, contains the entire original segment in its interior, and every point in the triangle is within sqrt(2)*eta*|u| of the segment. To check interior containment, use longitudinal coordinates along u: the base is at -eta, the tip at 1+eta, and the two original endpoints have longitudinal coordinates 0 and 1, strictly between them and strictly between the two sloping sides. The distance bound holds at the three vertices and then throughout their convex hull by convexity of distance to a convex set.

For a point p, use a sufficiently small nondegenerate triangle with p in its interior, for example p plus the three offsets (-t,-t), (t,-t), (0,t).

Combining these constructions with the preceding stability lemma proves:

**Triangle-only equivalence.** A finite hypergraph has an unrestricted intersection representation by closed filled triangles and closed segments, with points optionally allowed, if and only if it has such a representation by nondegenerate filled triangles only. The replacement can make each original compact set lie in the interior of its replacement, so every original common-intersection witness lies in the interior of all its new sets.

This conclusion is specific to unrestricted intersections and does not preserve contact systems or disjoint interiors. Thus it must not be applied to the different contact-representation results in the 2008 paper.

### 2.2 Degree-three corollary, credited to the published convex-realization fact

**Corollary.** Every finite simple linear hypergraph H with incidence-poset dimension at most three and maximum vertex degree at most three is the maximal-common-intersection hypergraph of a family of nondegenerate filled triangles in the plane.

**Proof.** Apply the convex-realization consequence stated in de Fraysseix–Ossona de Mendez–Rosenstiehl (2008), p. 135. Apply witness compression in Section 1; all resulting sets have at most three witness points. Apply the outer-triangle construction and finite-nerve stability in Section 2. These steps preserve every face and nonface. QED.

The same conclusion holds for Sperner linear hypergraphs with singleton edges: any singleton edge is then an isolated vertex component, since Sperner excludes larger incident edges. Remove those components, apply the preceding argument, and represent the removed vertices by triangles in pairwise disjoint disks sufficiently far from the compact existing family.

Rational coordinates can also be obtained existentially. After the outer perturbation, every desired maximal edge has a witness in the interiors of its finitely many triangles. Small enough independent perturbations of the finitely many triangle vertices preserve these positive interior margins. The empty-subfamily separation lemma preserves all nonfaces under sufficiently small Hausdorff perturbations. Density of the rationals therefore permits rational triangle vertices. This is an existence conclusion, not an asserted complexity bound or explicit construction from a three-order realizer.

## 3. A fixed-geometry obstruction to one-at-a-time triangle replacement

This example is **not a counterexample** to the conjecture. Its hypergraph is the disjoint union of a four-leaf star and a four-cycle, so is planar and admits other triangle representations. It demonstrates that an arbitrary convex representation cannot always be converted by replacing one polygon while holding all other sets fixed, even if the replacement may enlarge the polygon and move all edge witnesses.

Let the central set be

    Q = [-1,1] x [-1,1].

Let the four leaf segments be

    A = {(t,t)       : 1 <= t <= 7/6},
    B = {(-t,t)      : 1 <= t <= 7/6},
    C = {(-t,-t)     : 1 <= t <= 7/6},
    D = {(t,-t)      : 1 <= t <= 7/6}.

Let R,S,T,U be the top, left, bottom, and right closed sides, respectively, of the outer square

    O = [-4/3,4/3] x [-4/3,4/3].

These nine sets have exactly the following eight maximal common-intersection hyperedges:

    {Q,A}, {Q,B}, {Q,C}, {Q,D},
    {R,S}, {S,T}, {T,U}, {U,R}.

Indeed Q meets each leaf only at its inner endpoint. The four leaves occupy distinct diagonal rays, are mutually disjoint, and lie strictly inside O because 7/6 < 4/3. Neither Q nor a leaf meets a blocker side. Neighboring blocker sides meet at their shared outer corner, opposite sides are disjoint, and no three blocker sides share a point. This verifies the full maximal-edge family, not only its graph.

Suppose a triangle or a segment P could replace Q with all eight other sets held fixed, preserving that hypergraph. It must meet each leaf, so it contains points

    a=(t1,t1), b=(-t2,t2), c=(-t3,-t3), d=(t4,-t4)

with every ti in [1,7/6]. Convexity makes P contain conv{a,b,c,d}. These points are in convex cyclic order: a and c are on opposite sides of line b-d (the line y=-x), and b and d are on opposite sides of line a-c (the line y=x). The shoelace formula gives

    area(conv{a,b,c,d}) = t1*t2 + t2*t3 + t3*t4 + t4*t1 >= 4.

On the other hand P must avoid R union S union T union U, the entire boundary of O. It contains at least one point strictly inside O. If P also contained a point outside the interior of O, its segment to that interior point would cross the boundary of O, contradicting avoidance. Therefore P lies inside O.

Every triangle contained in a square of side length s has area at most s^2/2. One elementary proof maximizes the absolute determinant giving twice the triangle area over the three vertices in the square: with the other two vertices fixed, this is an absolute affine function of the remaining vertex, so its maximum is attained at a corner. Applying this to each vertex reduces the global maximum to triples of square corners, all of area at most half the square. Here s=8/3, so the upper bound is

    area(P) <= (8/3)^2 / 2 = 32/9 < 4.

A segment has area zero, and is ruled out already by the four-point lower bound. This contradiction proves that no such local replacement exists.

### 3.1 Explicit three-order certificate for the obstruction's incidence poset

Write alpha,beta,gamma,delta for the edges QA,QB,QC,QD; write rho,sigma,tau,upsilon for RS,ST,TU,UR. Three linear extensions of the star component are

    Q A alpha B beta C gamma D delta
    Q D delta C gamma B beta A alpha
    A B C D Q alpha beta gamma delta

Three linear extensions of the cycle component are

    R S rho T sigma U tau upsilon
    R U upsilon S rho T sigma tau
    T U tau S sigma R rho upsilon

For the full disjoint union, concatenate star order 1 then cycle order 1; cycle order 2 then star order 2; and star order 3 then cycle order 3. Within each component these orders intersect in exactly the incidence order. Across components orders 1 and 2 reverse every pair, so introduce no cross-component comparison. The exact verifier enumerates every ordered pair of the 17 elements and confirms this certificate.

## 4. The source's nonplanar five-vertex example has an explicit segment realization

The 2008 paper gives the linear hypergraph on vertices 1,...,5 with edges

    12, 23, 34, 14, 135, 245

as an example whose incidence poset has dimension three although its incidence graph is nonplanar. Its incidence graph is a subdivision of K3,3; this is a statement about that incidence graph and does not forbid arbitrary crossing segment intersections.

An integer-coordinate realization by five closed nondegenerate segments is

    C1 = [(0,-2),(0,4)],
    C2 = [(0,4),(4,0)],
    C3 = [(0,0),(4,0)],
    C4 = [(0,-2),(4,2)],
    C5 = [(0,0),(3,1)].

The maximal common intersections are

    12 at (0,4), 23 at (4,0), 34 at (2,0), 14 at (0,-2),
    135 at (0,0), and 245 at (3,1).

All ten pairs intersect. The only intersecting triples are 135 and 245; no fourfold or fivefold intersection exists. This can be checked directly from the supporting lines x=0, x+y=4, y=0, y=x-2, and y=x/3, together with the specified segment endpoints. The supplied exact rational verifier also checks all 31 nonempty subfamilies and recovers precisely the six desired maximal faces.

An independently verified three-order realizer uses edge labels a=12,b=23,c=34,d=14,e=135,f=245:

    1 2 a 3 b 5 e 4 c d f
    1 4 d 3 c 5 e 2 a b f
    2 4 5 f 3 b c 1 a d e

The verifier tests every ordered pair of the 11 elements. These orders are supplied as a certificate, not claimed to be the particular orders printed in the paper. The dimension is exactly three: the induced subposet on minimal elements 1,2,3 and maximal elements a=12,b=23,e=135 is the standard example S3. Its three incomparable missing-incidence pairs cannot have two of them reversed in the same linear extension (the two cross-incidences together with the two reversals would form a directed cycle), so at least three extensions are needed.

For completeness, suppress the degree-two incidence-graph nodes a,b,c,d and the degree-two vertex-node 5. The remaining branch nodes are 1,2,3,4,e,f. A K3,3 bipartition is {1,3,f} and {2,4,e}: its nine links are 1-a-2, 1-d-4, 1-e, 3-b-2, 3-c-4, 3-e, f-2, f-4, and f-5-e. This explicitly certifies the claimed subdivision.

## 5. Remaining gap and limits of the computations

The published convex-realization consequence plus witness compression leaves polygons at vertices incident with four or more maximal edges. Sections 1–2 do not bound those polygons by three sides. Section 3 shows that a universal independent local-replacement step is false, even for an elementary planar hypergraph of incidence dimension at most three. A successful general construction must exploit more freedom, for example a suitable globally chosen convex realization or coordinated changes of several sets.

The normalized rapid-growth realizer formula from the 2002 poset paper was explored on the five-vertex example, with base values 2,3,4,5,10,100 after dualizing the realizer. In this one example the convex hulls of incident normalized edge points have the correct nerve, as checked exactly. This is only a finite sanity check. No general full-nerve theorem, no universal triangle bound, and no counterexample follow from it. The public accepted certificates do not depend on this exploratory formula.

### Exact-checker scope and rejection controls

The canonical checker uses Fraction arithmetic and explicit VerificationError gates, so Python optimization cannot disable its checks. It enumerates every nonempty subfamily and every ordered pair in both incidence posets; polygon intersections include degenerate point/segment cases. A separate control harness runs the canonical checker under ordinary Python, -O, and -OO and requires identical successful output. It then makes four temporary source mutations (a missing triple witness, an incidence-invalid linear order, an overlong leaf touching a blocker, and a false numerical area inequality); all twelve mutation/mode runs must reject with VerificationError. These are controls of the supplied finite certificates, not a computational proof of the infinite conjecture or of the analytic compactness argument.

## Sources and provenance

* H. de Fraysseix, P. Ossona de Mendez and P. Rosenstiehl, **Representation of Planar Hypergraphs by Contacts of Triangles**, Graph Drawing 2007, LNCS 4875 (2008), pp. 125–136. Section 1.1 gives conventions; Section 4, p. 135 gives the convex-realization consequence, the five-vertex nonplanar example, and Conjecture 2. DOI: https://doi.org/10.1007/978-3-540-77537-9_15 . Publisher PDF: https://link.springer.com/content/pdf/10.1007/978-3-540-77537-9_15.pdf .
* Patrice Ossona de Mendez, **Realization of Posets**, Journal of Graph Algorithms and Applications 6(1) (2002), pp. 149–153. General separation theorem 2.1, not an explicit hypergraph full-nerve formula. PDF: https://jgaa.info/index.php/jgaa/article/download/paper48/2922 .
* **Linear Hypergraphs with Dimension 3**, Open Problem Garden, https://www.openproblemgarden.org/op/linear_hypergraphs_with_dimension_3 . Problem identity and historical statement; its presence does not certify current literature status.

The degree-three reduction, compactness proof, triangle-only equivalence, fixed-geometry obstruction, and explicit coordinate certificates above are authored mathematical deductions documented in this investigation. Their novelty has not been assessed. Source documents are not included in this edition; the public scholarly PDF hashes and byte counts appear in [SOURCE_IDENTITIES.json](SOURCE_IDENTITIES.json).
