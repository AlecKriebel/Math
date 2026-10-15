# Source-only target and independent route (frozen before candidate access)

UTC: 2026-10-04T23:01:46.117797+00:00
Source arXiv: https://arxiv.org/abs/2004.12497v11, title Eighty New Invariants of N-Periodics in the Elliptic Billiard, submitted 29 October 2020 v11. PDF Table 7, printed p.9 (PDF page 9), k606.
Source published: https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf, Fifty New Invariants of N-Periodics in the Elliptic Billiard, Arnold Mathematical Journal 7 (2021), 341–355, Table 7 printed p.349 (PDF page 9), k607.
Both PDF page-9 tables have been visually inspected from independently downloaded originals.

## Exact displayed target
ArXiv v11: \(\bar A_1/\bar A_2=\bar A'_1/\bar A'_2\). Published: \(A_1/A_2=A'_1/A'_2\). Both rows: which N = all; value = ?; date = 4/20; proven = ?. ArXiv k607 instead concerns antipedal area ratios and is not this target.

The setting is a one-parameter family of periodic Poncelet trajectories between two confocal **ellipses**, with outer ellipse semiaxes a>b>0 and foci f1,f2=(±sqrt(a²−b²),0). The outer polygon has sides tangent to the outer ellipse at the billiard vertices. The unprimed focal pedal polygon consists of perpendicular feet from a focus to successive billiard side lines; the primed polygon uses successive outer-polygon side lines. All polygon areas are the signed cyclic shoelace sum S=(1/2)Σ Wi×Wi+1. The sources do not state this row for hyperbolic caustics, degenerate conics, arbitrary inscribed polygons, or generic arbitrary Poncelet pairs.

The literal ratio equality requires its displayed denominators nonzero. Its division-free counterpart is A1 A2'−A2 A1'=0. The latter may extend to zero-area cases, but does not automatically define a ratio there. Source does not separately specify primitive-period, repeated traversal, or star-winding conventions in the target row. Do not assert more than the equation; the table's conserved-quantity terminology does not replace a proof of separate phase-constancy.

## Independent derivation/control route
For a real line n·x=h with unit n, focus f=(s c,0), s=±1, its perpendicular foot is Q_s=f+(h−s c n_x)n. For a tangent to a confocal ellipse (α,β) with α²−β²=c², use n=(cosφ/α,sinφ/β)/D, h=1/D, D²=cos²φ/α²+sin²φ/β². Then Q_s is rational in cosφ,sinφ; independently check |Q_s|²=α². This establishes elementary geometry controls but does not prove the ratio identity.

Algebraic alternative: complexify the conic-pair tangent incidence curve, use its two involutions to form the billiard map T, and express each signed pedal area as a rational orbit sum on the resulting genus-one curve. To prove equality, one must establish that the determinant D(z)=A1(z)A2'(z)−A2(z)A1'(z) is identically zero. A pole-based route must enumerate complete principal parts of D, prove all vanish, and evaluate its residual constant at a regular symmetric phase. Matching residues alone is insufficient whenever higher-order poles occur. Torsion/closure must be proved for the same cyclic indexing and lattice; odd/even and nonprimitive repetition must be handled separately.

Exact elementary controls: take outer ellipse (a,b)=(5,3), foci (±4,0), axis diamond P=(5,0),(0,3),(−5,0),(0,−3). Its edge lines are ±x/5±y/3=1, tangent to confocal ellipse with λ=a²b²/(a²+b²)=225/34, α²=625/34, β²=81/34. This is an exact real billiard 4-periodic. Compute rational focal pedal areas for these four side lines and for outer tangents x=±5,y=±3; cover reversal, repetitions, and similarity scaling. In the circular limit c=0 the two focus polygons coincide identically, so the cross-product equation is tautological whenever feet exist. For odd controls, independently construct isosceles billiard triangles by reflection equations before trusting any elliptic parametrization. Numeric tests are independent evidence only and cannot establish all n.

## Early independence
No candidate file, candidate README, author check, source binding, or inherited review has been accessed. This analysis and the independent control program are frozen now.
