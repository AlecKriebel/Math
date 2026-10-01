# Sources and exact target

## Original invariant

Dan Reznik, Ronaldo Garcia, and Jair Koiller, *Eighty New Billiard Invariants*, arXiv:2004.12497v11, 29 October 2020. [Original PDF](https://arxiv.org/pdf/2004.12497v11).

The target is Table 7, printed p. 9, **k605,a**: the product of the two primed focal pedal areas, for odd N. Section 3.7 defines the prime as the outer polygon, rather than the original billiard orbit. Section 2 specifies signed cross-product areas and defines the outer polygon from successive tangents. The introduction restricts the billiard setting to an elliptical caustic confocal with the outer ellipse. Primitive self-intersecting orbits are included in the present proof. Hyperbolic caustics are not added to the claim.

The original table page was rendered and visually checked, so the primes, parity and source code do not depend on OCR alone.

## Published edition

The authors' published companion, *Fifty New Invariants of N-Periodics in the Elliptic Billiard*, Arnold Mathematical Journal 7 (2021), 341–355. [Published PDF](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf).

Table 7, printed p. 349, retains the same outer focal-pedal product under **k606**. Its **k605** refers instead to the product of the unprimed, original-orbit focal-pedal areas. This is an edition renumbering, and neither proof nor status may be assigned by matching a code alone. The published table page was separately rendered and visually checked.

## Canonical parametrization

Hellmuth Stachel, *On the motion of billiards in ellipses*, European Journal of Mathematics 8 (2022), 1602–1622, [DOI](https://doi.org/10.1007/s40879-021-00524-2).

Theorem 4.3 and equation (4.9), printed p. 1614, provide the canonical Jacobi phase, the step 2v, and the relation between the outer and caustic semiaxes. The modulus in that paper is denoted m; the proof here calls it k and passes k² as the parameter to mpmath. The turning-number condition is gcd(N,τ)=1. The proof includes every allowed τ after choosing orientation, rather than only τ=1.

## Classical analytic inputs

[NIST DLMF §22.4](https://dlmf.nist.gov/22.4) records the periods, poles and special translations of the Jacobi functions. [§22.8](https://dlmf.nist.gov/22.8) gives addition formulas, from which the displayed quarter-period identities follow. [§22.13](https://dlmf.nist.gov/22.13) gives their derivatives. The proof uses the elementary compact-torus fact that a nonconstant elliptic function has equal total zero and pole multiplicities. It does not invoke an unproved invariant from a neighboring table row.

## Readiness and history

The pinned problem and complete imported research report were read at dataset revision 37e53eabe540fb458758e198be61634bd02ee008. The imported report is open-target triage, not a proof. Its review hash is recorded in readiness.json. The pinned data hashes are 04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf for problems.json and 8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b for research_results.json.

Before the first author turn, live all-state PR searches for 5100033 and k605, a branch search for 5100033, the default-branch history at this attempt path, the recovered prior-work exclusion list, and the related-target groups were checked. None identified an earlier campaign attempt for this exact target. A limited contemporary literature check found the source and related billiard work, but did not verify a general published proof of this exact outer-pedal product. This is not an exhaustive literature review or a novelty certificate.

The two-pole elliptic-function framework was also present in the adjacent k203,b and k804,a campaign candidates independently reviewed by this author. The outer-tangent foot formula and its adjacent-pole collinearity cancellation are derived explicitly here. This dependence in mathematical technique is disclosed, not presented as independent discovery of the framework.

source_manifest.json binds the three PDF reading copies. They are not part of the publication package, which contains links and hashes rather than redistributing the papers.
