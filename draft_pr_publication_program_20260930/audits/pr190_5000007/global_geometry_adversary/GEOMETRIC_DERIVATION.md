# Independent analytic derivation of the restricted geometric theorem

This is independently authored verification, not an amendment to the source or the submitted candidate. The theorem below deliberately defines its class rather than asserting that it is the only interpretation of Fuchs's printed definition.

## Precise statement

Let D be the intrinsic surface of a regular dodecahedron. Let gamma:[0,L]->D, L>0, be unit speed, with vertices at its endpoints and no vertex at any interior parameter. It may intersect itself. Fix its initial face and vertex. Fold/unfold it as a regular-pentagon billiard trajectory with N straight face occurrences. Include both initial-face edge trajectories in class C. Include an interior trajectory in C exactly when N is even and the transported Figure8 endpoint angles satisfy beta-alpha=2*pi/5.

**Theorem.** For gamma in C, its endpoint graph distance is neither 0 nor 2. In particular it is not 2. The proof is unbounded in L and N.

## Explicit double pentagon and all endpoint sectors

Put r=exp(2*pi*i/5), p_j=sum_{a=0}^{j-1}r^a, P=conv{p_0,...,p_4}, Q=conjugate(P), and q_j=conjugate(p_j), with indices modulo5. The boundary order p_0,...,p_4 is counterclockwise; q_0,...,q_4 is clockwise. Every reflected odd face occurrence is a translate of P; every reflected even occurrence is a translate of Q. This follows because reflecting across a line with one of the five side directions conjugates the polygon followed by a fifth-root rotation, and the unlabeled regular pentagon is invariant under such rotations.

The side p_j->p_{j+1} has vector r^j. Its parallel, translation-paired side of Q is q_{-j}->q_{1-j}, with the same vector r^j. These pairings form the standard double-pentagon translation surface X. They identify all ten corners to its single cone point of angle6*pi.

Take the initial P corner to be p_0 and alpha in [0,3*pi/5]. The reverse terminal tangent has direction pi+alpha in the developed coordinate. Write angles below in degrees solely to make the sector table readable; all are exact integer multiples of pi/5.

For an odd terminal occurrence (P), the interior corner at p_j is the counterclockwise sector from 72j to 72j+108 degrees. The possible terminal corners and equations are:

| terminal corner | permitted alpha | endpoint equation |
|---|---:|---|
| p_1 | alpha=0 | beta=72 |
| p_2 | 0<=alpha<=72 | alpha+beta=144 |
| p_3 | 36<=alpha<=108 | alpha+beta=216 |
| p_4 | alpha=108 | beta=180 |

For an even terminal occurrence (Q), the corner at q_j is the counterclockwise sector from -72j-108 to -72j degrees. Equivalently, if theta=-72j is its outgoing clockwise side direction, pi-beta is the counterclockwise angle from the reverse terminal tangent to that outgoing ray. Thus theta=alpha-beta modulo2*pi. The possibilities are:

| terminal corner | permitted alpha | endpoint equation |
|---|---:|---|
| q_0 | 72<=alpha<=108 | beta-alpha=0 |
| q_1 | 0<=alpha<=108 | beta-alpha=72 |
| q_2 | 0<=alpha<=36 | beta-alpha=144 |

The remaining corners cannot contain the reversed tangent. These tables follow from the actual corner sectors and include singular endpoint prongs, rather than identifying merely equal planar directions. At the cone point of X, equal planar directions alone do not identify a germ: the cone has angle6*pi.

For every non-edge member of C, the table therefore identifies its terminal corner as exactly q_1.

## The involution and midpoint

The map h(z)=1-z exchanges P and Q, since 1-P=Q as unlabeled polygons. In particular h(p_0)=q_1. It has derivative -I. Under the side gluing above, h maps a P side to its paired Q side with reversed parameter. Hence h is a well-defined isometric involution of X. It fixes exactly the five glued side midpoints in the regular locus; it swaps the two polygon interiors, and on every open glued edge the fixed-parameter equation is s=1-s. The identified singular vertex is its sixth fixed point.

Project the unfolded gamma to X, obtaining sigma. This can be justified by the regular-pentagon covering construction in Athreya–Aulicino–Hooper §4, or directly by analytically continuing the above translation identifications along the face occurrences. Open faces map to open faces, open edges map to open edges, and all preimages of the unique X vertex are physical vertices in the unfolding. Consequently sigma has no interior singularity.

For the non-edge member of C, h applied to the reverse of sigma starts in the P corner p_0. Its tangent is v, because reversal changes v to -v and Dh=-I changes it back to v. It is the same ray in the same corner as sigma's initial germ. Therefore ordinary straight-geodesic uniqueness on the regular locus, continued up to the first singularity, gives
    h(sigma(L-t))=sigma(t), 0<=t<=L.
Both paths have the same length L. This argument concerns parameterized paths and does not require embedded images.

At t=L/2, sigma is a regular fixed point, so it is one of the five side midpoints. Every face map is a translation of congruent unit-side pentagons. Its physical preimage on gamma is therefore a midpoint m of a dodecahedral edge, not an arbitrary point of that edge and not a singularity.

No step asserts that h lifts to the unfolding, nor that an arbitrary affine map of the unfolding descends to D.

## Physical half-turn and graph obstruction

The 180-degree rotation rho around the line through the center of the solid and the midpoint m of its edge preserves the dodecahedron. The line also passes through the midpoint of the opposite edge. It is an orientation-preserving intrinsic isometry. On a locally flattened neighborhood of m it is the half-turn with derivative -I: it reverses the edge coordinate and exchanges the two incident faces.

Thus rho(gamma) has, at its midpoint, exactly the germ of the reversed gamma. Uniqueness on D minus its vertices gives
    rho(gamma(t))=gamma(L-t).
There is no choice of continuation through a vertex: both directions stop at their first vertex. Self-intersections at regular points do not obstruct uniqueness of a specified tangent germ.

A nonidentity half-turn of the regular dodecahedron fixes no vertex. Indeed, a rotation fixing a vertex fixes the radial line through it and cyclically permutes its three incident edges, so its vertex stabilizer is cyclic of order3. An element of order2 cannot belong to it. This already excludes equal endpoints.

The dodecahedral graph has girth5. For an elementary model, use the generalized Petersen graph with u_i,v_i, i mod10, and edges u_i-u_{i+1}, u_i-v_i, v_i-v_{i+2}. With no spokes a cycle has length at least5. A cycle with two spokes of length<=4 would require one outer step of index difference1 and one inner step of index difference2 to join the same index pair, which is impossible. A cycle with four spokes requires an additional non-spoke edge between consecutive spokes and cannot have length4. Thus no 3- or 4-cycle exists.

Two vertices at graph distance2 have a common neighbor. If there were two common neighbors they would form a 4-cycle, so the common neighbor is unique. An automorphism exchanging the two endpoints must fix that neighbor. Since rho fixes no vertex, it cannot exchange a distance2 pair. This proves the theorem.

The edge trajectories omitted from the midpoint derivation have graph-distance-one endpoints directly.

## Exceptional directions and the exact interpretation gap

For odd N, intersect beta-alpha=72 with the odd table. At p_2 this gives alpha=36, beta=108; at p_3 it gives alpha=72, beta=144. At the boundary corners it gives the two edges alpha=0 or108. Each of these four directions already hits another vertex of the initial pentagon. The first subsequent vertex condition forces N=1.

The two non-edge paths are exactly the two direct face diagonals. They have graph-distance-two endpoints: there is a two-edge boundary route and there is no joining graph edge (equivalently, otherwise the face would yield a triangle). Their angle pairs satisfy the bare beta-alpha=72 test. In the clockwise Fig.9 calibration they are A2 and A1 respectively. They also satisfy the printed difference branch for A0; the source's non-strict branch conditions do not explicitly remove that overlap.

Consequently:
- The parity-selected class C has a complete geometric proof.
- The bare difference-angle statement is false, with exactly those two additional trajectories per fixed initial face and vertex.
- Geometry cannot authenticate a correction to Fuchs's printed definition or prove that an unstated priority convention is uniquely forced. The source's diagonal calibration supports the parity interpretation, while its literal displayed branches and p.506 shorthand still overlap at the two exceptional directions.

## Cover bookkeeping and classical dependency audit

The physical dodecahedron has cone angle9*pi/5 at every vertex. Its linear holonomy has order10. The minimal translation unfolding has degree10, with one point over each physical vertex and angle18*pi there; Euler/stratum bookkeeping gives H(8^20) and genus81. It has120 pentagonal faces. Mapping to the two-faced double pentagon has degree60. The twenty cone points map to the unique angle6*pi cone with local degree3, accounting for 20*3=60. Thus there are no additional regular preimages of that singularity. This is consistent with the explicit face/edge map used above.

The regular degree60 cover and the virtual-Weierstrass vocabulary come from Athreya–Aulicino–Hooper §§4–5. Their Proposition5.3 is only about triangular or square faces and is not used for pentagons. Their no-closed-virtual-Weierstrass theorem excludes distance0; the unique-neighbor argument above supplies distance2 explicitly.

There are15 distinct edge-axis half-turns because the30 edges are paired oppositely. Enumerating one rotation for each of the30 edges repeats each distinct map twice. The candidate's phrase about30 edge-axis half-turns is harmless if understood as an edge-indexed enumeration.

## Reproducible auxiliary public-witness check

EXACT_WITNESS_REPLAY.py uses only Python's standard library and the explicit public face lists/itinerary pinned by the candidate. It constructs the sixteen developed face occurrences in Q(r), without importing or executing any source checker. It tests all face boundary intersections, all potential vertex hits, ordered strict interior crossings, graph distance, and squared length exactly. It also derives the initial angle sector and both terminal boundary rays.

This replay validates the literal face word and its own reconstructed coordinates. It does not validate every coordinate expression or every other claim in the external repository; in particular the external displayed A+B*eta expression was not used as an input or checked by this replay. Its exact result is:
- Z=5+r-7*r^2-8*r^3;
- length squared=(307+137*sqrt(5))/2;
- N=16;15 strict, ordered interior edge crossings; no interior vertex;
- endpoint graph distance2;
- 0<alpha<pi/5 proved by exact determinants;
- terminal outward physical ray108 degrees, transported clockwise ray216 degrees;
- beta-alpha=144 degrees in the source's even-N endpoint convention, hence parity-selected A1.

The approximate alpha=5.041282036470806 degrees is explanatory only. Exact sector tests, not floating-point angle rounding, choose the branch. This supports candidate §6 and does not enter the unbounded analytic theorem.

## Primary references

- D. Fuchs, Arnold Math. J.7 (2021),493–517, DOI10.1007/s40598-020-00170-8, https://amj.math.stonybrook.edu/pdf-Springer-final/020-0170.pdf, especially pp.501–506 and514–515.
- J. S. Athreya, D. Aulicino, W. P. Hooper, https://arxiv.org/html/1811.04131v2, §§2,4–5.
- Public pinned construction: https://github.com/DannyExperiments/dodecahedron-short-geodesic-counterexample/blob/7b403decdc9317f6ba3dc2c4a91243a0bf0c9ff9/proof/PROBLEM_AND_PROOF.md.
