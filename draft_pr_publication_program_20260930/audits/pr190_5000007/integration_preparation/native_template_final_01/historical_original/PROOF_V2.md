# A parity-aware proof for Fuchs's dodecahedral conjecture

Frozen revision 2, 2026-10-01. Read the independent review for the verdict. This is a mathematical result for the precisely stated parity-aware type below, not a novelty or publication claim.

## 1. Scope must come first

Fuchs's Conjecture 3.2 concerns vertex-to-first-vertex geodesics on the regular dodecahedron. “Short” has no metric length bound, and the path need not be simple or closed. The graph distance is distance in the one-skeleton.

There is a source-formulation caveat. Figure 8 and the paragraph immediately preceding Definition 2.1 distinguish the difference relation for an even number N of straight face segments from the sum relation for odd N. Under this parity-selected classification, type A0 in a pentagon consists of:

- the two edge trajectories leaving the initial vertex; and
- interior trajectories with N even and beta−alpha=2pi/5.

This agrees with the source's Figure 9 calibration: edges are A0, while the two proper pentagon diagonals are A1 and A2. We call this the **parity-aware type A0** throughout.

The isolated p.506 statement “beta−alpha=2pi/5” is not a sufficient definition at every exceptional direction if detached from parity. The imported dataset sentence makes precisely that detachment. Under the literal angle test alone, the two direct face diagonals are additional qualifying geodesics, and their endpoints have graph distance 2. Therefore the literal extracted sentence is false. We do not silently replace it with the theorem below or claim the unqualified shorthand has been proved.

**Theorem.** Every short dodecahedral geodesic of parity-aware type A0 has endpoints at graph distance different from 2.

**Literal-angle clarification.** With a fixed initial face and initial vertex, the bare condition beta−alpha=2pi/5 admits exactly two extra short geodesics beyond that type: the two direct face diagonals. Thus the formulation defect is explicit and finite.

## 2. The endpoint angles and the odd-N exceptions

Use a unit-side regular pentagon above the horizontal initial edge. Set

r = exp(2pi i/5),
p0 = 0, p1 = 1, p2 = 1+r,
p3 = 1+r+r^2, p4 = 1+r+r^2+r^3.

The initial direction is alpha in [0,3pi/5]. The polygon's initial boundary ordering is counterclockwise. The terminal boundary ordering is transported by reflecting the labeled billiard polygon at each crossing; it is not the fixed outward orientation of the physical dodecahedron's faces. Figure 8 defines pi−beta as the terminal interior angle between the reversed terminal tangent and the outgoing transported boundary ray.

For odd N, the sum relation alpha+beta is an integer multiple of 2pi/5. If the bare difference condition beta−alpha=2pi/5 also holds, then alpha is an integer multiple of pi/5. In the permitted initial sector this leaves alpha=0, pi/5, 2pi/5, or 3pi/5. Each such ray already hits a vertex of the initial pentagon, so the vertex-to-first-vertex trajectory has N=1. The endpoint angles are:

- p0 to p1: alpha=0, beta=2pi/5, an edge of type A0
- p0 to p2: alpha=pi/5, beta=3pi/5, a proper diagonal of type A2
- p0 to p3: alpha=2pi/5, beta=4pi/5, a proper diagonal of type A1
- p0 to p4: alpha=3pi/5, beta=pi, an edge of type A0

The A1/A2 labels use Fuchs's clockwise Figure 9 labeling and interchange under reflection; both are non-A0. The sum branches for A0=A3 in the n=5 instance of Definition 2.1 reduce to alpha=0 or alpha=3pi/5. These facts prove the literal-angle clarification. The edge cases also prove the theorem when N is odd. It remains to treat N even.

## 3. An even-N A0 connection has an edge midpoint as its midpoint

Every odd developed face occurrence is a translate of the unlabeled pentagon P above; every even occurrence is a translate of Q=conjugate(P). Write qj=conjugate(pj). Identify parallel sides by translations to obtain the standard double pentagon X. Equivalently Q=1−P as an unlabeled polygon. The involution h of X interchanges the two polygons via z↦1−z. This is the hyperelliptic involution, though only its explicit polygon action is needed here.

The translation unfolding of the dodecahedron maps by translations to X, with vertices over the common singular vertex, face interiors over polygon interiors, and open edges over open edges. Therefore a short geodesic lifts and projects to a saddle connection sigma on X without interior singularities. It starts in the P corner p0.

Because N is even, its terminal corner is in Q, with clockwise transported boundary orientation. Let theta be the direction of that corner's outgoing boundary ray. The terminal-angle convention gives, modulo 2pi,

pi−beta = theta−(pi+alpha),
so theta = alpha−beta.

The A0 relation forces theta=−2pi/5=8pi/5 modulo 2pi. In Q there is exactly one clockwise outgoing edge with that direction: q1 to q2, whose vector is r^4. Thus the terminal corner of sigma is q1=h(p0).

Apply h to sigma with its parameter reversed. The resulting initial germ lies at p0 in the original P corner, and its tangent is exactly the initial tangent of sigma, since Dh=−I. Straight-line continuation from a regular germ is unique up to the first singularity. Both connections stop at their first singularity, so

h(sigma(L−t))=sigma(t), for 0≤t≤L.

In particular the midpoint is a regular fixed point of h. No polygon-interior point can be fixed, since h swaps the polygons. On every glued edge, h acts by reversing its edge parameter; hence its only regular fixed points are the five edge midpoints. The common vertex is singular and cannot be the midpoint of sigma. The original dodecahedral geodesic therefore has its midpoint at a physical edge midpoint.

This is exactly the virtual-Weierstrass mechanism of Athreya–Aulicino–Hooper, Section 5. Their all-saddle-connection result for triangular and square cases is not being assumed for pentagons. The local endpoint-germ calculation above establishes precisely the symmetry needed for A0.

## 4. Lift the midpoint symmetry to the solid

Let m be this physical edge midpoint. The half-turn rho about the line joining the center of the regular dodecahedron to m preserves its surface and intrinsic metric. On the locally flat intrinsic tangent plane at m it acts by −I. It therefore reverses the geodesic germ at m. Unique continuation to the first vertex in either direction implies

rho(gamma(t))=gamma(L−t).

Thus rho exchanges the two endpoint vertices. Self-intersections cause no difficulty: the assertion concerns the parameterized geodesic and its uniquely continued germ, not global embeddedness.

## 5. A half-turn cannot exchange distance-two vertices

The dodecahedral graph has girth 5. Any two vertices at graph distance 2 therefore have a unique common neighbor; two common neighbors would make a 4-cycle. Any graph automorphism exchanging those vertices must fix that common neighbor.

But a nonidentity rotational half-turn of a regular dodecahedron fixes no vertex. The rotational stabilizer of a vertex has order 3: a rotation fixing it preserves its axis through the center and cyclically permutes its three incident edges. In particular an element of order 2 cannot occur in that stabilizer. This contradicts the fixed common neighbor. Hence the two endpoints of gamma cannot have graph distance 2, proving the theorem.

An independent exact check in standard Q(sqrt5) coordinates corroborates this elementary argument for all 30 edge-axis half-turns. Their vertex-distance histograms are always {1:4, 3:8, 4:4, 5:4}. The enumeration is not needed as a logical premise of the proof.

## 6. Relation to the public 16-face witness

The independent reconstruction verifies that the public witness is a legal short geodesic of graph distance 2, with squared unit-edge length (307+137sqrt5)/2. This geometry is not disputed by the checks.

In the normalized development, alpha≈5.041282 degrees. Its terminal transported billiard ray is 2→16, with direction 216 degrees, so beta=144 degrees+alpha and beta−alpha=144 degrees exactly. With N=16 and alpha<36 degrees, the parity-aware source classification is A1. The outward physical-face ray 2→10 used in the public certificate instead has direction 108 degrees. Its interior angle with the reversed tangent is 72 degrees+alpha; that is the angle producing the public 72-degree subtraction. The distinction is specifically about the transported boundary ray and the Figure 8 supplement, not about length, self-intersections, or closedness.

These statements apply to the identified literal witness and the stated angle calculation. They do not make claims about the authors or authorize any contact or publication.

## References and reproducibility

- D. Fuchs, *Billiard Trajectories in Regular Polygons and Geodesics on Regular Polyhedra*, Arnold Mathematical Journal 7 (2021), 493–517, https://amj.math.stonybrook.edu/pdf-Springer-final/020-0170.pdf. Relevant source locations: pp.501–506, especially Figure 8, Definition 2.1, Figure 9, and the shorthand on p.506; pp.514–515 for Conjecture 3.2
- J. S. Athreya, D. Aulicino, W. P. Hooper, *Platonic solids and high genus covers of lattice surfaces*, https://arxiv.org/html/1811.04131v2, Sections 4–5. The virtual-Weierstrass definitions and half-turn argument are classical inputs, not new claims of this note
- Public literal certificate pinned to commit 7b403decdc9317f6ba3dc2c4a91243a0bf0c9ff9: https://github.com/DannyExperiments/dodecahedron-short-geodesic-counterexample/blob/7b403decdc9317f6ba3dc2c4a91243a0bf0c9ff9/proof/PROBLEM_AND_PROOF.md

Local original checkers: `python check_certificate.py`, `python check_half_turn.py`, and `python -m unittest discover -s . -p 'test_*.py' -v`. No downloaded external software was executed. The independently written review checker and its verdict are separate artifacts.

Historical attempt counts remain unknown but nonzero; this recovery does not reset the five-turn allowance. Current literature and historical priority require a separate review before any novelty claim or publication decision.
