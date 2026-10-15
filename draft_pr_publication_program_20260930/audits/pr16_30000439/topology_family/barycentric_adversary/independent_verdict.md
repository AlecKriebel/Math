# Independent adversarial check of the barycentric construction

Audit started: 2026-10-01 15:06:22 UTC.

Final checkpoint: 2026-10-01 15:17:37 UTC. Completion estimate toward this
independent audit: 100%. This percentage concerns the assigned lemma audit,
not a surrounding research program or probabilistic theorem.

Verdict: the stated construction proves the precise embedding claim, provided
the finite-separation choices are made with positive margins as below. I found
no counterexample or missing topological assumption. The proof is independent
of root/sibling reports and historical reviews. A message subsequently received
from the assigning agent says its proof uses the same trimmed-star clearance;
that report has not been read.

## Exact claim and assumptions

Let K be a finite simplicial complex whose two-dimensional facets are the
triples of a linear 3-uniform hypergraph: distinct triples share at most one
original vertex. K consists of their faces and possibly isolated original
vertices. Then the abstract first barycentric subdivision sd(K) has a geometric
realization in R^3 in which every simplex is a straight simplex and every pair
of simplices meets exactly in the image of its common face.

The positions named "edge barycenter" and "facet barycenter" are freely chosen
positions for vertices of the abstract barycentric subdivision. They are not
required to be Euclidean averages of the original vertex positions. This
qualification is essential to interpreting the claim correctly. No initial
embedding is prescribed. No assertion of historical novelty is audited here,
and no original literature source has been supplied to this subaudit.

## 1. The incidence graph really is straight embedded

Put every original vertex v and every facet vertex c_F at a different parameter
of the moment curve p(t)=(t,t^2,t^3). Any at most four distinct such points are
affinely independent: this follows from the Vandermonde determinant (or its
appropriate lower-degree minor). Distinct segments [v,c_F] and [u,c_G] with
four different endpoints cannot intersect, since an intersection would give
an affine dependence of the four endpoints. Segments with one shared endpoint
have no further intersection, since their three endpoints are not collinear.
An unused original vertex cannot lie on a graph edge, by the same three-point
argument. Thus the straight incidence graph, including isolated vertices, is
embedded. Cycles cause no additional constraint in this argument.

For each F={v_1,v_2,v_3}, the vectors a_i=v_i-c_F are linearly independent.
Every original edge belongs to just one facet. Assign its barycentric vertex

    w_ij = c_F + epsilon (a_i + a_j),  i<j.

The six maximal triangles of sd(F) have images

    T_ij = conv(c_F,v_i,w_ij),  i!=j.

Here w_ij=w_ji, and the six choices are the six vertex-edge-facet chains.

## 2. All within-facet intersections are exact

In the independent basis a_1,a_2,a_3, write c_F=0, v_i=e_i, and
w_ij=epsilon(e_i+e_j), where epsilon>0. Then

    T_ij = { (lambda+mu epsilon)e_i + mu epsilon e_j :
             lambda,mu>=0, lambda+mu<=1 }.

It lies in the nonnegative ij-coordinate plane. Its intersection with the
i-axis is [0,e_i], and with the j-axis is {0}.

For the reversed pair T_ij,T_ji, membership in T_ij implies x_i>=x_j,
while membership in T_ji implies x_j>=x_i. Equality forces lambda=0 in
each triangle, so the intersection is exactly [0,w_ij].

For two different coordinate planes, their intersection is their common
coordinate axis. If both triangles are rooted at the common index i, their
intersection is exactly [0,e_i]. Otherwise at least one has intersection {0}
with that axis, so the two triangles meet only at 0. These are precisely the
three types of intersections of different maximal barycentric triangles:
facet-edge segment, facet-vertex segment, and facet vertex. Their faces inherit
the required intersections. Every maximal triangle is nondegenerate since
epsilon>0 and e_i,e_j are independent.

## 3. Explicit global separation choices

Assume there is at least one facet; otherwise the isolated-vertex claim is
immediate. Let

    L   = max_F,i |v_i-c_F|,
    ell = min_F,i |v_i-c_F| > 0,
    S_F = union_i [c_F,v_i].

For each original vertex v, let N_v be the union of incidence-graph edges not
incident to v. This compact set omits v. Choose a uniform radius r>0 so that
the radius-r original-vertex balls are pairwise disjoint and

    dist(v,N_v) > 3r

whenever N_v is nonempty. Finiteness and the embedded-graph property guarantee
this choice. Facet centers also lie outside all these balls: each center is
on an edge not incident to any specified original vertex, since a facet has
three distinct vertices.

Define the trimmed compact stars

    S_F^- = S_F \ union_v B(v,r/2),

using open balls. Different S_F^- are disjoint, because different untrimmed
stars share at most original vertices and those vertices have been removed.
Each trimmed star is nonempty, containing c_F. Thus the minimum distance Delta
between different trimmed stars is positive if there are at least two facets;
take Delta=+infinity if there is only one.

For every vertex v shared by facets F,G, their unit ray directions

    u_vF = (c_F-v)/|c_F-v|,  u_vG = (c_G-v)/|c_G-v|

are distinct, since v,c_F,c_G are not collinear. Let m>0 be the finite minimum
of |u_vF-u_vG| over such pairs; if there are no such pairs, take m=1.

Choose one uniform epsilon satisfying

    0 < epsilon < 1/2,
    epsilon L < min(r/2, Delta/3),
    delta := epsilon L / ((1-epsilon) ell) < m/(6+m).

Such a positive epsilon exists, since all fixed constants are positive and
delta tends to zero with epsilon.

## 4. Every possible cross-facet intersection is excluded

For x=lambda v_i+mu w_ij+(1-lambda-mu)c_F in T_ij, define

    y=(lambda+mu epsilon)v_i + (1-lambda-mu epsilon)c_F.

Because 0<epsilon<1 and lambda+mu<=1, y belongs to the incidence edge
[c_F,v_i]. Also

    x-y=mu epsilon(v_j-c_F),  so |x-y|<=epsilon L.

If x lies outside every open radius-r original-vertex ball, then y lies
outside every radius-r/2 ball, because |y-v|>=r-epsilon L>r/2. Hence y is
in S_F^-. If x also belonged to a triangle of a different facet G, the same
construction would give z in S_G^- with |x-z|<=epsilon L. Therefore

    Delta <= |y-z| <= 2 epsilon L < Delta,

a contradiction (the displayed strict inequality follows even from
epsilon L<Delta/3).

If x lies in B(v,r), a triangle rooted at any vertex other than v cannot
contain x: its approximating y is on N_v, yet

    |v-y| <= |v-x|+|x-y| < r+epsilon L < 3r.

Consequently every triangle entering B(v,r) is rooted at v and belongs to a
facet incident to v. For x in T_ij rooted at v_i=v, put

    alpha=1-lambda-mu epsilon >= mu(1-epsilon).

Then

    x-v = alpha(c_F-v) + mu epsilon(v_j-c_F).

Except at x=v, alpha>0. The second term has norm at most delta times the
norm of the first. If q=(x-v)/|x-v|, the elementary normalization bound gives

    |q-u_vF| <= 2 delta/(1-delta) < m/3.

The direction neighborhoods of radius m/3 for two distinct incident facets
are disjoint: a common q would imply |u_vF-u_vG|<2m/3, contradicting its
lower bound m. Hence different facets meet within this ball only at v.

These two cases cover every point. Thus distinct facet surfaces intersect
exactly at their common original vertex, if present, and otherwise are disjoint.
The same ball argument excludes intersection of an isolated original vertex
with any facet image. Together with the local calculation this is an injective
simplexwise affine realization of sd(K). Compactness of the finite complex
makes it an embedding.

## Adversarial conclusions and limits

- No forbidden graph cycle, link singularity, or higher-dimensional obstruction
  survives the stated linearity assumption: triangle facets glue only at points.
- A shared edge would break the construction as written, because its single
  barycentric vertex could not independently be placed close to two facet
  centers. The linearity hypothesis is used essentially for this formula.
- The claim does not concern geometric barycentric subdivision with prescribed
  arithmetic barycenters, nor does it establish a straight embedding of K itself.
- Finiteness is used for positive clearance, a positive minimum ray separation,
  and a single uniform epsilon. An infinite version needs a different argument.
- Merely saying that triangle images are epsilon-close to stars is not sufficient
  without the trimmed-star and vertex-ball margins. The explicit inequalities
  above supply those margins.

The strongest result verified by this audit is the full finite universal claim
under the exact assumptions stated here. There is no remaining mathematical
gap in this construction identified by this audit. Historical attribution,
publication novelty, and broader claims are outside its scope. In particular,
any probability conclusion in the surrounding candidate is a separate gate.

## Reproducible finite stress check

`verify_exact.py` uses only Python's standard library and Fraction arithmetic.
It enumerates basic feasible solutions of each triangle-intersection polytope
and checks that their image points belong to the expected common face. This
validates a finite example independently of floating-point tolerances; it is
supporting evidence, not a substitute for the universal proof above.

The Fano-plane test has seven original nonisolated vertices, seven facets,
42 maximal barycentric triangles, and an incidence graph with cycle rank 8.
At epsilon=1/10^10, all 861 unordered triangle pairs pass, with 231 exact
intersection vertices checked. Two isolated original moment-curve vertices
also pass all 84 point-triangle exclusion checks. These results explicitly
exercise an incidence graph with cycles and unused original vertices.

Reproduce with `python3 verify_exact.py`; the recorded JSON is
`exact_stress_result.json`.
