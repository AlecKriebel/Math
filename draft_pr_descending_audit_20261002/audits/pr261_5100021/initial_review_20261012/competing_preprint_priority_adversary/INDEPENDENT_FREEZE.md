# Independent mathematical freeze

Frozen at 2026-10-12 10:10:13 UTC, before reading our candidate proof or any review verdict. Completion estimate: 75% of this external-proof and priority audit; mathematical reconstruction is complete, provenance comparison remains.

## Verdict

**PASS for the external preprint's stated mathematical scope, conditional only on the correctly identified established Chávez-Caliz theorem.** I found no central proof gap or false displayed identity. This concerns the currently retrieved manuscript, not proof of when these exact bytes were publicly available. This audit does not certify absolute novelty or authorize promotion of our result.

The exact target is the same-focus signed pedal/antipedal product for a primitive ellipse-billiard orbit of least period N divisible by four, with a>b>0 and 0<lambda<b². Stars with coprime winding are covered; arbitrary padded lists and hyperbolic/degenerate caustics are excluded. These restrictions are substantive.

## Check matrix

| Step | Independent result | Exact boundary or dependency |
|---|---|---|
| Reflection velocity components | Verified from confocal tangent chord geometry and ordinary reflection | W>=b²>lambda; positive tangent component follows from orientation with caustic left |
| Velocity-product telescope | Verified; difference divided by 2hj is (2D-sW)/(dW) | Consecutive outgoing/incoming unit velocities coincide; d,lambda>0 permit division |
| Focal pedal single-vertex determinant | Verified by orthogonal projection in the (normal,tangent) frame | Signed determinant, not absolute face area |
| Opposite-vertex pedal pairing | Verified rationally and using 2D S2=s S1 | Requires actual central pairing, supplied by primitive even canonical translation |
| Outer signed-area trace | Verified by pulling tangent intersections back to the unit circle | Half gaps lie in (0,pi/2), because caustic contains center; roots of half-gap quadratic finite |
| Jacobi quarter permutation | Verified against Stachel Theorem 2 and squared quarter identity | gcd(N,tau)=1 and 4 divides N force tau odd; N/4 shift adds an odd multiple of K |
| Pedal factor K | Verified, including reciprocal sqrt(J) in outer trace | K=sqrt(J)(beta-lambda)/beta²; all radicands positive |
| General antipedal edge-area formula | Verified by regrouping adjacent intersection determinants along each oriented defining line | Does not require convexity or divide by total polygon area |
| Opposite-edge antipedal algebra | Verified from distances, chord length and determinant | F is strictly inside caustic, so consecutive normal determinants nonzero |
| Antipedal final telescope | Verified independently from trig endpoint identity | Sum det(Pi,Pi+1)cos(2ti)=0; central pairing reduces full sum to opposite-edge representatives |
| Factor R and signed zeros | Verified | R=[D(3beta-alpha)+lambda(alpha-beta)²]/[2D(beta-lambda)]; no division by A, p, q or R |
| Established AT theorem mapping | Verified in published Theorem 6, p104, area definition p93 | Concentric ellipses in complex projective general position; theorem stated for oriented n-gons, no winding-one restriction |
| General position | Verified explicit four intersections and nonzero gradient determinant | No common infinity point when lambda>0 and alpha>beta; endpoints and circle excluded |
| N4 formula | Verified | lambda=D/s implies R=2, K=D/s²; product=16D²/s² using AT=8D |
| Least-period distinction | Verified logically; independently obtained N6 product variation | Repeating N6 twice cannot create the necessary primitive N12 quarter permutation |

## Reconstruction and falsification checks

Use alpha=a², beta=b², d=alpha-beta, D=alpha beta, s=alpha+beta, L=D-s lambda and J=(alpha-lambda)(beta-lambda). For vertex parameter theta let W=beta cos²theta+alpha sin²theta and Sr=sum sqrt(W-lambda)/W^r.

In the orthonormal frame n=(b cos theta,a sin theta)/sqrt(W), t=(-a sin theta,b cos theta)/sqrt(W), the velocities are ht±jn with h²=(W-lambda)/W and j²=lambda/W. Their xy product difference is 2sqrt(lambda)sqrt(W-lambda)(2D-sW)/(dW²). Summing is a genuine closed-orbit telescope, proving 2D S2=s S1. It imports no area invariant.

For u=P-F, projection gives Q±=P-v±(u·v±). Direct determinants give half det(Q-,Q+)=hj[Pn un-Pt ut+ut²h²-un²j²]. Eliminate cos²theta+sin²theta=1 and c²=a²-b². The normalized single contribution is (alpha-lambda+ac cos theta)/(a+c cos theta)². Pair its value with the opposite vertex. The normalized pair is 2[(alpha+lambda)/W-2alpha lambda/W²]. After the velocity telescope this proves p=sqrt(lambda) alpha(beta-lambda)S1/beta.

The signed tangent-polygon boundary formula on the unit circle is one half the sum of the forward and backward half-gap tangents, then multiplied by ab. The quadratic discriminant is lambda D(W-lambda). Hence T=D sqrt(lambda) sum sqrt(W-lambda)/(L+lambda W).

Stachel's canonical step is 4tau K/N at modulus squared d/(alpha-lambda). The actual N/2 index permutation negates every vertex. When 4 divides N, the actual N/4 permutation shifts by tau K, with tau odd. With sn²(u+K)=cn²u/dn²u, substitution gives W'=(lambda W+L)/(W-lambda), W'-lambda=J/(W-lambda), and L+lambda W'=JW/(W-lambda). Positivity is essential when taking square roots. Evaluating the permuted trace therefore gives **T=D sqrt(lambda) S1/sqrt(J)**. This establishes K. The denominator sqrt(J) is confirmed in the downloaded LaTeX; a text-extraction ambiguity could incorrectly reverse it.

For antipedal sides translated to F, write their unit normal/support form n_i·Z=r_i. If successive normals have angle eta, adjacent intersection coordinates along a side are (r_next-r_i cos eta)/sin eta. Regrouping the shoelace terms yields E(u,v)=[|u|²|v|²-(|u|²+|v|²)(u·v)/2]/det(u,v).

For an original edge with parameters t±delta, let U=alpha-d cos²t, z=c cos t, C=cos delta, S=sin delta. Its focal distances are a-zC±c sin t S and its squared chord length is 4US². Their substitution into E gives numerator 2S²[(2beta-U)(a-zC)²+U(U-beta)S²]. The opposite edge changes z to -z. Their sum divided by det(P,Q) reduces to 2-LU/[D(beta-lambda)]. The exact canceled determinant product is (aC-z)(aC+z)=U(beta-lambda)/beta>0.

The independent trig identity det(P,Q)cos(2t)=ab[sin(2theta_next)-sin(2theta)]/2 telescopes. It makes the det-weighted U sum equal sA/2. Thus q=[2-sL/(2D(beta-lambda))]A=RA, with no assumption that q is nonzero.

For theorem transfer, the complex conic intersections satisfy x²=alpha(alpha-lambda)/d and y²=-beta(beta-lambda)/d. They are four distinct finite points; the gradient determinant is 4xy lambda d/(DJ), nonzero. At infinity a common point would require alpha/(alpha-lambda)=beta/(beta-lambda), contradicted by lambda d>0. The published general-position definition is exactly transversality in CP². This is a checkable hypothesis map, not a limiting argument.

`INDEPENDENT_ALGEBRA.json` records 22 exact symbolic identities checked by an independent script, without importing external checkers. `INDEPENDENT_GEOMETRY.json` records direct projection/intersection/shoelace calculations for 84 cases at 80 decimal digits: N4,8,12,16,20, including winding 3,5,7 and near-circle/eccentric caustics. Maximum target identity residual was 2.59e-79, product phase spread 1.83e-79. These are rounded corroboration, not interval certification. An initial version accidentally used Python binary floating division in the canonical step; it failed precision assertions, was corrected to multiprecision division, and passed. This was a checker defect, not a counterexample to the manuscript.

## Primary sources read

- Current [external PDF](https://eulersolve.org/papers/amr-050-0021/paper.pdf?v=34ff068237a7), obtained as bytes and full text; 6 pages. Equations and proof are now independently reconstructed above.
- [Chávez-Caliz published paper](https://armj.math.stonybrook.edu/pdf-Springer-final/020-0154.pdf), Definition p93, general-position definition p94, Theorem 6 p104.
- [Stachel v2](https://arxiv.org/pdf/2105.03624v2), Theorem 2 pp11–12, canonical modulus and shift.
- [Reznik–Garcia–Koiller v11](https://arxiv.org/pdf/2004.12497v11), k403,b Table 5 and signed/antipedal conventions; target provenance rather than proof authority.

No claims about external author's unpublished work, independence, plagiarism, or human review follow from this audit.
