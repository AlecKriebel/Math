# Independent direct Euclidean geometry audit of PR203 / 5100011 / k203,a

Report checkpoint: 2026-10-16T07:44:44.063036+00:00.

## Verdict and scope

**PARTIAL independent verification; no counterexample to the exact target found.** The direct family proves the universal pedal-area quadratic, primitive-even central pairing, the exact all-M reduction to two scalar phase identities, the complete N=4 theorem, and several decisive exact boundary controls. It does **not** prove the scalar identities for every primitive N=0 mod 4 with N>=8. That route is **BLOCKED at precisely A B_0 and AC**, not complete. This is not a rejection of the submitted proof: its later Jacobi/two-pole argument lies outside the mechanism used here and has not supplied this family's conclusion.

Family audit completion estimate: 100%; universal elementary proof completion estimate: 35%. Percentages are estimates of this effort, not probabilities of mathematical truth.

Independence was frozen in INDEPENDENCE_FREEZE.md at 2026-10-16T07:31:54.278037Z before original PROOF.md or any favorable verdict. The universal quadratic was frozen at 07:33:09.205703Z and the direct central-pairing/N=4 derivation at 07:36:00.472125Z. Original PROOF.md was read afterward. No favorable independent_review or sibling-author checkpoint was read. No Jacobi/two-pole verdict is imported. Source hashes and safe authored hashes accompany this report.

## Exact target and direct primary source check

The outer ellipse is x^2/a^2+y^2/b^2=1, a>b>0. The fixed inner caustic has axes squared a^2-lambda,b^2-lambda, 0<lambda<b^2. The original ordered physical billiard trajectory has primitive least period N divisible by four. For any one fixed finite real M, feet are taken to the original successive SIDE LINES; their ordered signed shoelace area is B_M. The original area is A. The claim is phase independence of A B_M for every primitive winding and reversal, allowing B_M=0 or B_M<0.

Direct arXiv v11 checks: introduction pp.1-2 requires a confocal ellipse pair and physical normal bisection; Eq.(1) p.3 declares all areas signed; Section 3.3 p.4 defines feet from M to trajectory sides; Table 3 p.6 prints k203,a: A A_m, N=0 mod 4, M=all, value=?, proven=?. The distinct journal PDF has matching Eq.(1) p.343, Section 3.3 p.344, Table 3 p.346. Its outer-pedal construction is separately Section 3.4/Table 4 and is not this target. The sources say 'sides'; supporting-line perpendicular projection is the usual all-M pedal convention, without clipping feet to segments.

Neither primary table row prints 'primitive'. The submitted proof's least-period qualification is substantive and necessary for a literal ordered-list interpretation, as the repeated-triangle counterexample below shows. It is consistent with the usual primitive periodic-family convention but should remain explicit in publication. The question marks establish the source's stated proof status there; they are not a present-day novelty certificate.

## Strongest universal results independently proved

For ANY cyclic ordered side-line list L_i: n_i dot X=h_i with unit n_i, set d_i=n_i cross n_(i+1), s_i=n_i dot n_(i+1). The exact identity is

B_M=B_0+ell dot M+C|M|^2,
B_0=(1/2)sum d_i h_i h_(i+1),
ell=-(1/2)sum d_i[h_i n_(i+1)+h_(i+1)n_i],
C=(1/4)sum d_i s_i=(1/8)sum sin(2delta_i).

Projection gives Q_i=M+(h_i-n_i dot M)n_i. Translation invariance of signed shoelace area then gives the formula except radiality. In coordinates M=(r,0), the identity

sin(beta-alpha)cos(alpha)cos(beta)
 =[sin(2beta)-sin(2alpha)+sin(2beta-2alpha)]/4

makes the anisotropic terms telescope. Thus radiality of the quadratic term is universal, not a billiard invariant. For opposite line pairs n_(i+m)=-n_i,h_(i+m)=h_i, the linear term cancels.

Primitive-even central pairing is independently justified by the orientation-preserving Poncelet circle map T and center inversion C_0. The conic porism gives finite order N; C_0 commutes with T, is a fixed-point-free involution, and preserves the chosen tangent branch. If T^(N/2) differed from C_0, they would generate a Klein group of orientation-preserving circle homeomorphisms, contradicting the elementary fact that every finite such group is cyclic. Hence P_(i+N/2)=-P_i. See DIRECT_GEOMETRY.md for the elementary group and branch arguments.

The exact target consequently reduces to

(1) A B_0 is independent of phase;
(2) AC is independent of phase.

Both are necessary and together sufficient for all M. A curvature center at the origin establishes radiality only. Treating either scalar as automatically invariant would transfer the original difficulty to an unsupported claim; this audit does not do so.

For a consistently oriented physical trajectory around a proper elliptical caustic containing O, every chord has the caustic on the same side, so every det(P_i,P_(i+1)) has the same nonzero sign: its magnitude is side length times the positive center-to-line distance. Thus A cannot vanish in the exact target; reversal changes its sign. The universal polygon formulas nevertheless make no division by A or B. The meaningful zero case is a pedal area, exhibited below.

## Complete four-bounce theorem

The elementary derivation in DIRECT_GEOMETRY.md proves that for every primitive 4-family,

A B_M=8a^4 b^4/(a^2+b^2)^2, for every finite real M.

The forced caustic is lambda=a^2 b^2/(a^2+b^2). The central trajectory is a parallelogram, for which C=0. With adjacent side lengths u,v, its pedal area is B_0=A^3/(2u^2v^2), and confocal tangency gives A^2/(uv)=4a^2 b^2/(a^2+b^2). This proves the stated constant. For a=2,b=1 the two exact phases (2,0),(0,1),(-2,0),(0,-1) and (4/sqrt(5),1/sqrt(5)),(-4/sqrt(5),1/sqrt(5)),(-4/sqrt(5),-1/sqrt(5)),(4/sqrt(5),-1/sqrt(5)) both give 128/25.

This is a universal N=4 proof, not an extrapolation to larger N.

## Exact falsification controls

### Nonconfocal Poncelet is insufficient

For outer x^2/4+y^2=1 and inner x^2/2+2y^2=1, affine images of rotating squares form a genuine tangent Poncelet 4-family. The diamond (2,0),(0,1),(-2,0),(0,-1) gives A B_0=128/25; the rectangle (+/-sqrt(2),+/-1/sqrt(2)) gives A B_0=8. Both have C=0, so the difference persists for all M. The second polygon fails physical reflection. Nested Poncelet polygons alone do not suffice; confocality/physical reflection matter.

### Repeated lists make the source's unprinted primitive convention material

Let r=sqrt(13), w=sqrt(2r-5)/3 and E have a=2,b=1. The two exact primitive triangle phases are

U=[(2,0),(2(1-r)/3,w),(2(1-r)/3,-w)],
V=[(0,1),(-4w,(r-4)/3),(4w,(r-4)/3)].

Both are physical trajectories tangent to the same proper confocal ellipse with lambda=4(2r-5)/9. At M=(1,0), their products are

A_U B_U=(11936-3176r)/729,
A_V B_V=(67312-18544r)/729.

Their nonzero difference is (-55376+15368r)/729. Repeating each list four times produces a nominal length 12 and multiplies each area by four, hence the product difference by sixteen. Thus 'listed length divisible by four' is false if primitive parity is ignored. Repeating a trajectory already satisfying the primitive hypothesis simply scales a valid product; these are different statements.

### A primitive even-period extension is false

For the same E with lambda=4/9, set

H=[(2,0),(4/3,sqrt(5)/3),(-4/3,sqrt(5)/3),(-2,0),(-4/3,-sqrt(5)/3),(4/3,-sqrt(5)/3)],
J=[(0,1),(-4sqrt(2)/3,1/3),(-4sqrt(2)/3,-1/3),(0,-1),(4sqrt(2)/3,-1/3),(4sqrt(2)/3,1/3)].

These are two physical primitive 6-family phases. Their centered products are 14000/729 and 14336/729, differing by 112/243. Their AC values are 2000/729 and 2048/729. This directly prevents a parity-blind generalization of the two scalar identities. Repeating each list twice gives nominal length 12 with products 56000/729 and 57344/729, differing by 448/243: an especially simple repeated-list counterexample when least period 6 is mislabeled by listed length 12.

### A genuine primitive 3/8 star has zero and negative pedal areas

Let a=4sqrt(2), b=3sqrt(3), lambda=864/35, with caustic axes squared 256/35 and 81/35. Take the convex cyclic list

W=[(a,0),(4a/5,3b/5),(0,b),(-4a/5,3b/5),(-a,0),(-4a/5,-3b/5),(0,-b),(4a/5,-3b/5)]

and order the trajectory as Z_i=W_(3i mod 8). Exact tangency and the physical reflection law hold at all eight distinct vertices, establishing least period 8 and winding 3. Its exact areas are

A=168sqrt(6)/5,
B_M=(96sqrt(6)/245)(13-|M|^2),
A B_M=(13824/175)(13-|M|^2).

Thus B_M=0 for |M|^2=13 and B_M<0 for |M|^2>13. Reversal negates both signed areas and preserves their product. At M=(sqrt(13),0), the eight feet are distinct and no two edge supporting lines coincide. The first three feet have nonzero wedge (2304sqrt(6)-1152sqrt(39))/1225, although total signed area is zero. The closed edge graph has a bounded face of positive area. Hence replacing signed area by ordinary unsigned face/lobe area changes the quantity. Taking the absolute value of the total signed area is a separate operation; if both factors are replaced by absolute signed areas, constancy follows trivially from a constant signed product and is not a counterexample.

This star is one exactly checked orbit. It validates boundary conventions and does not prove phase independence for all 8-orbits.

## Submitted-proof scope audit and independently checked contact geometry

The original statement precisely retains noncircularity, 0<lambda<b^2, primitive least N=0 mod 4, arbitrary fixed real M, original SIDE LINES, signed stars, and zero/negative coefficients. It explicitly excludes hyperbolic and degenerate caustics. Its radial lemma agrees with the stronger independently derived universal formula. Its warning that radiality alone leaves two outstanding coefficients is correct.

The contact/outer polarity identity can also be checked without analytic machinery. If R_i is the intersection of the outer ellipse tangents at P_i and P_(i+1), D_E=diag(1/a^2,1/b^2), and D_C=diag(1/alpha^2,1/beta^2), both P_i and P_(i+1) satisfy (D_E R_i) dot X=1. Their chord is also the caustic tangent (D_C B_i) dot X=1. Hence B_i=D_C^-1 D_E R_i and signed shoelace areas scale by alpha^2 beta^2/(a^2 b^2). This is independently derived linear conic geometry and is checked exactly on the 3/8 star. R_i is finite, since an antipodal chord would pass through O and could not touch a proper caustic containing O.

This transfer does not establish the needed even-period outer-area theorem or pedal/contact proportionality. Neither is silently credited as independently proved by this family. In particular, the author's disclosed sibling input is not independent review, and it has not been used here. The submitted later analytic steps require another approach family's actual verification.

## Reproducibility and limits

Run verify_exact_controls.py with the prescribed Python using -B and again -B -O. It reads only the authorized existing SymPy 1.14.0 runtime and writes its own CHECK_RESULTS*.json files. Checks use explicit exceptions, not removable assertions. They verify outer incidence, each original side's confocal tangency, nondegeneracy, distinct vertices, exact physical reflection and its inward/outward sign, direct projected-foot shoelace areas, radial coefficient identities, repeated-list scaling, reversals, and reversal products. The saved script is exactly the 282-check revision whose SHA-256 is present in both passing result files. The separate unsigned-face and contact-polarity derivations above were also checked by exact algebra; an expanded combined run reached result serialization only to fail with Errno 28 (disk full), so it is not presented as an additional completed normal/-O run.

No finite computation is represented as a universal proof. No random numerical tolerance is used. There are no installations, copied dependencies/fulltexts, source modifications, Git/index/ref operations, PR/UI mutations, releases, or external-person communication. All authored work remains inside this family's assigned folder.

**Remaining universal gap:** supply an independent direct Euclidean mechanism proving A B_0 and AC phase-independent for all primitive N=0 mod 4, N>=8; or provide an exact target counterexample. Repeating the reduction, invoking an unsupported invariant, or importing a favorable analytic verdict does not close this gap.
