# Independent global-topology/PL reconstruction seal

Sealed before reading historical review artifacts or scripts, running old verification,
or receiving any root/sibling mathematical outcome. The snapshot manifest was read
only for input binding; PROOF.md and primary original problem sources were read.

## Bound input and exact original target

PR 21, problem 30001696 / OWR-4798-013, head
`096aacd71a1dc6dd3a73bea3c1055877dc8c0451`.
Original PROOF.md SHA-256:
`58809f3edaa2930f1111ba823b1ce50c8e328dd8388b2e19323600ede3d04305`.

I read the complete Klee contribution (printed pp. 370–373, question p. 372)
in EMS's full OWR 08/2011 PDF, and Klee–Novik arXiv 1102.0542v1,
Theorem 1.2, Definition 3.1, Lemma 3.2 and relevant context. Q4 asks about
the entire complex B(i,d), not just its boundary. The required claim is:
for every integer d>=2 and 0<=i<=d-2, the finite simplicial complex generated
by length-d sign words with at most i adjacent switches has a PL realization
homeomorphic to the standard PL product S^i x D^(d-i-1).
The d=1 / i=d-1 whole-sphere endpoints may be handled separately.
No outside contact, publishing, priority clearance, classification by homology,
or new attempted solution is part of this family audit.

## Independent acceptance criteria

1. Every zero-coordinate stratum realizes the claimed closed set C on the
round sphere, and its spherical interior is exactly s^+<=i. This must include
arbitrary leading/trailing/intermediate zeros.
2. The given classical TP input has the actual zero-sensitive strict
inequality s^+(Ax)<=s^-(x), so every positive-time image of all of C enters
its spherical interior. A weaker inequality is insufficient.
3. The attracting linear sphere A=S(E) lies in the interior and repelling
sphere B=S(F) misses C. Compactness gives uniform neighborhoods, not merely
orbitwise asymptotics.
4. The algebraic normalized maps psi_a form a genuine invertible action;
R=||F||/||E|| increases from 0 to infinity for every orbit with both components
nonzero. Sigma={R=1} is compact even when disconnected.
5. Gamma:Sigma x (0,infinity)->S^(d-1) minus (A union B) is a continuous
semialgebraic bijection with continuous inverse. Prove inverse continuity by
strict bracketing, without a properness or smoothness assumption.
6. Membership on each orbit is a nonempty finite CLOSED lower interval.
Strict trapping is what makes lower points interior; closedness alone or
non-strict invariance cannot substitute. The boundary meets each orbit once.
7. beta is positive, finite, continuous on all Sigma and semialgebraic.
Continuity must use both interior and exterior persistence. Compactness then
yields uniform positive lower/upper bounds across all components.
8. The straightening fixes an entire ambient neighborhood of A and is a
bijection onto D_E; prove continuity of both directions at A. Uniform epsilon
and the spectral ratio inequalities must actually imply the claimed identity.
9. The full product map S(E) x closed unit ball(F)->D_E is invertible including
v=0 and ||v||=1. No unidentified bundle or isotopy is allowed.
10. The source and target must be COMPACT POLYHEDRA linked by a real
semialgebraic homeomorphism. Check the actual primary semialgebraic
Hauptvermutung theorem and proof hypotheses. A general topological
homeomorphism is insufficient; triangulation of a map alone is not enough.
11. Check every endpoint: i=0 (S^0 and possible disconnected Sigma),
i=d-2 (dim F=1), d=2,i=0 (both spheres S^0), d=1,i=0, i=d-1.
Universal deductions carry the proof; finite exact or numerical tests only
serve as supplementary falsification controls.

## Independent reconstruction of the global mechanism

Abstract the needed data as a closed semialgebraic C subset of a round sphere,
a splitting E+F with both nonzero, projections P_0,...,P_N onto an orthonormal
basis, E=sum_{k<r} P_k, F=sum_{k>=r} P_k, and psi_a(x)=sum a^k P_kx normalized.
Assume A=S(E) is contained in int(C), B=S(F) is disjoint from C, and
psi_b(C) is contained in int(C) for every 0<b<1.
For any orbit, if q=log(a),

d log R(psi_a x) / d q = (weighted mean of F indices) -
(weighted mean of E indices),

which is in [1,N]. At least one weight in each block is positive. Therefore
R increases strictly and obeys a^N<=R(psi_a s)<=a for a<=1, reversed
correspondingly for a>=1 and s in Sigma. This gives a unique Sigma crossing;
local bracket values persist under changing x, proving the inverse continuous.
The graph of the inverse is obtained by swapping graph factors, proving it
semialgebraic without invoking log/exponential definability.

Distance to A tends uniformly to zero as a->0 (because R<=a), and distance
to B tends uniformly to zero as a->infinity (because R>=a). Compactness of
A, B, C supplies uniform interior and exterior thresholds. If a member is
at b, then every a<b equals psi_(a/b) of that member and is interior. The
membership set is thus (0,beta], since it is closed in (0,infinity), bounded
above, nonempty, and downward closed. The endpoint cannot be interior or the
interval would extend; it is the unique boundary point on that orbit.
Interior below and exterior above beta persist in Sigma, so endpoints are
bracketed continuously. The beta graph is Gamma^{-1}(boundary C), a
semialgebraic graph with exactly one point per fiber.

A uniform 0<epsilon<min(1,min beta) allows affine endpoint straightening
above epsilon and identity below. If R(x)<epsilon^N, its orbit parameter must
be <epsilon, so the straightening is exactly the identity there. The same
neighborhood statement holds for the inverse because its output parameter
<=epsilon exactly when its input parameter<=epsilon. This proves genuine
continuity at every core point, without a limit-direction assumption.
Orbit straightening maps C bijectively onto {R<=1} union A. The latter is
exactly the image of S(E) x D(F) under (u,v)->(u+v)/sqrt(1+||v||^2), with
inverse (y+z)->(y/||y||,z/||y||). This is an actual product, not a homology or
boundary inference.

Round models are not polyhedra, so before applying Hauptvermutung use radial
maps from the boundary of an E cross-polytope and the whole F cross-polytope.
Their Cartesian product is a finite polyhedral cell complex with a standard
product subdivision. The original l1 realization of B is also a finite
compact polyhedron. Composition is semialgebraic over real algebraic
coefficients. The outstanding external input at this seal is the exact
primary PL uniqueness theorem; it is not yet presumed checked.

## Initial independent status

No global defect found at this reconstruction stage. The acceptance decision
remains OPEN pending primary-theorem/proof verification and adversarial
controls. Estimated completion of this AUDIT (not discovery or priority): 35%.

Seal timestamp UTC: 2026-10-01T18:28:40.916463+00:00
