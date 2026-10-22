# 5000007: candidate proof for the source-defined type A0

Status: recovered candidate, **not independently reviewed**. No verified-resolution or novelty claim is made. The load-bearing convention is the even/odd sign choice in Fuchs, Section 2.2; review this together with Figure 8 and the diagonal calibration in Figure 9. The isolated shorthand “beta minus alpha equals 2 pi/5” must not be detached from that convention at exceptional directions.

## Target and conventions

Fuchs, *Billiard Trajectories in Regular Polygons and Geodesics on Regular Polyhedra*, Arnold Mathematical Journal 7 (2021), 493–517, Conjecture 3.2, p.515. The target excludes graph-distance-two endpoints of every type-A0 geodesic starting at a vertex and stopping at its first subsequent vertex. There is no length bound, simplicity requirement, or requirement that the endpoints coincide. The length120 restriction belongs only to a preceding experiment.

Take the initial developed pentagon above a horizontal edge, with the start at its left endpoint. Let alpha be the initial direction in [0,3pi/5]. As in Figure8, the terminal interior angle between the reversed tangent and the outgoing **billiard-polygon** boundary ray is pi−beta. Its ordering is the labeling obtained by successive reflections of the original oriented polygon, not the fixed outward face orientation of the physical dodecahedron.

Fuchs states immediately before Definition2.1 that the difference relation is used for an even number N of segments, and the sum relation for odd N. For a genuine interior trajectory of typeA0, N is even and beta−alpha=2pi/5. On the odd-N branches of the n=5 definition, A0=A3 occurs only at alpha=0 or alpha=3pi/5; these are edge trajectories and already have graph-distance-one endpoints. This parity interpretation is independently supported by the source's calibration that the two non-edge diagonals have typesA1 andA2. Ignoring parity makes some direct diagonals satisfy the numerical difference relation accidentally, contradicting that calibration. This is a source-convention issue to review explicitly, not an additional geometric hypothesis being silently imposed.

## Lemma1: an interior A0 trajectory is virtual-Weierstrass

Put r=exp(2pi i/5), and let the unit-side pentagon P have vertices

p0=0, p1=1, p2=1+r, p3=1+r+r^2, p4=1+r+r^2+r^3.

All developed odd occurrences are translates of P as unlabeled polygons; all even occurrences are translates of Q=conjugate(P). Let qj=conjugate(pj). The standard double pentagon consists of P and Q, with corresponding parallel sides glued by translations. Its hyperelliptic involution h interchanges the polygons by z↦1−z. In particular h(p0)=q1. The outgoing clockwise ray at q1 is q2−q1=r^4, whose direction is8pi/5.

A geodesic on the dodecahedron lifts to the translation unfolding and projects to a saddle connection sigma on this double pentagon. No interior vertex of the double pentagon is encountered because the original geodesic has no interior dodecahedral vertex; the projection maps face interiors to face interiors and open edges to open edges.

For even N the terminal occurrence is a translate of Q and its billiard orientation is clockwise. Write theta for the direction, modulo2pi, of its outgoing boundary ray. Figure8 gives

pi−beta = theta−(pi+alpha), modulo2pi,

and therefore theta = alpha−beta, modulo2pi. For typeA0 this is −2pi/5 =8pi/5, so the terminal corner projects precisely to q1. Its outgoing **reversed** geodesic germ lies in that Q corner. Applying h maps it to the P corner at p0, and Dh=−I changes its tangent back to the initial tangent. Thus h applied to the reverse of sigma and sigma have the same initial nonsingular germ. Uniqueness of straight-line continuation up to the first singularity yields

h(sigma(L−t))=sigma(t), 0≤t≤L.

The midpoint sigma(L/2) is therefore a regular fixed point of h. The only regular fixed points are the five glued edge midpoints: h swaps polygon interiors, and on each glued side it acts as reflection in that side's midpoint. The remaining fixed point is the common vertex, which cannot occur in the interior of sigma. Hence the original dodecahedral geodesic has its midpoint at the midpoint of a physical edge.

This is the virtual-Weierstrass mechanism defined by Athreya–Aulicino–Hooper, Section5. It does **not** assert that every saddle connection on the double pentagon is hyperelliptic-invariant. Their Proposition5.3 asserts that stronger property only for triangular and square Platonic surfaces; it is not being used for pentagons here. Their Proposition5.1/its proof supplies the same midpoint half-turn argument for closed virtual-Weierstrass saddle connections, but its published conclusion concerns equal endpoints. The extension below to the graph-distance of distinct endpoints is proved explicitly.

## Lemma2: the physical edge-axis half-turn exchanges the endpoints

Let m be the midpoint just found. The 180-degree rotation rho about the line from the center of the regular dodecahedron through m preserves the solid and its intrinsic metric. Its differential on the developed tangent plane at m is −I, since it is the nonidentity orientation-preserving involution fixing this regular point. Consequently rho reverses the geodesic germ at m. By unique geodesic continuation in both directions until the first vertex,

rho(gamma(t))=gamma(L−t).

The endpoint vertices are exchanged by rho. This argument does not require the projected geodesic to be globally embedded; equality follows from the local germ and its parameterized continuation.

## Lemma3: an edge-axis half-turn never exchanges graph-distance-two vertices

The finite assertion is independently checked by `check_half_turn.py`, with exact arithmetic in Q(sqrt5). It builds the standard regular-dodecahedron coordinates

(±1,±1,±1), (0,±1/phi,±phi), (±1/phi,±phi,0), (±phi,0,±1/phi),

where phi=(1+sqrt5)/2. Graph edges have squared length4/phi^2. For each of all30edges {a,b}, the rotation is computed exactly as

rho(x)=2〈x,a+b〉(a+b)/〈a+b,a+b〉−x.

The script verifies that rho permutes all20vertices, squares to the identity, has no fixed vertex, exchanges a,b, and preserves every graph edge. Breadth-first search on the exact graph gives the same vertex-distance histogram for every such rho:

- distance1:4vertices
- distance3:8vertices
- distance4:4vertices
- distance5:4vertices

Thus distance2 never occurs. This is a finite, exact certificate, not numerical evidence about long trajectories.

## Candidate conclusion

For edge trajectories the endpoints have distance1. Every other source-defined A0 trajectory is covered by Lemmas1–3 and cannot end at graph distance2. Subject to an independent audit of the conventions and lemmas, this resolves Fuchs Conjecture3.2 affirmatively, rather than by a counterexample. Novelty is undetermined; no claim of historical priority or publication readiness is made.

## Sources and remaining review gates

- Fuchs source: https://amj.math.stonybrook.edu/pdf-Springer-final/020-0170.pdf, pp.501–506 (orientation, Figure8, Definition2.1, diagonal calibration) and pp.514–515 (target)
- Athreya–Aulicino–Hooper: https://arxiv.org/html/1811.04131v2, Section5, especially the definition preceding Proposition5.1; Section4 for the double-pentagon cover
- External conflicting certificate: https://github.com/DannyExperiments/dodecahedron-short-geodesic-counterexample/blob/7b403decdc9317f6ba3dc2c4a91243a0bf0c9ff9/proof/PROBLEM_AND_PROOF.md

Review gates: (1) exact Fuchs angle/parity convention, particularly its exceptional-direction shorthand; (2) double-pentagon local-germ identification; (3) lift/projection preserving the first-vertex condition; (4) physical half-turn argument for possibly self-intersecting trajectories; (5) exact computational certificate; (6) current literature and novelty; (7) reconcile unknown lost historical turn count before formal queue promotion.
