# Independent mathematical falsification checks

This document records this reviewer's deductions, not prior verdicts. Completion at this checkpoint:90% of the assigned whole-package review.

The restricted real equations F=x²−y²−u=0 and G=xy−v/2=0 are jointly equivalent, in both directions and for every real pair (x,y), to (x+iy)²=u+iv. They have exactly two distinct real point solutions for nonzero w and a single real point at w=0, regardless of multiplicity conventions. No additional root can evade the restriction.

A neighborhood U of zero inR6 pulls back through iota to an open neighborhood of zero inC. It contains a positive-radius disk. Choosing a strictly smaller circle in that disk and parametrizing w=ρexp(it) gives q(t)=S(w)/(sqrt(ρ)exp(it/2)). Its square is1, it is continuous, and its denominator never vanishes. Since[0,2π] is connected, q is constant; equal section values at the endpoints force its sign to reverse. This proof independently establishes local failure, rather than only global failure.

The manuscript's polygon supplies the same mechanism without trigonometry. On each closed interval its squared norm has exact minimum1/2 at t=1/2 or3/2 and maximum1 at the endpoints. The seam is i, the root lift starts1 and ends−1, and its square closes. For each r>0 choose c>0 with c²<r; |c²gamma²|=c²|gamma|²≤c²<r. There is no finite-sampling inference and no boundary equality admitted.

Expanding the translated equations gives a1=−2h,a2=2k,a0=h²−k²−u,b1=−k,b2=−h,b0=hk−v/2. All six signs and the factor1/2 are correct. For p(1,0)=(-2,0,1,0,-1,0), a small neighborhood avoids the removed origin but still pulls back to a full translated disk. Thus removing onlyzero does not repair local failure.

The general Jacobian is

J=2x²+2y²+(a1+2b2)x+(2b1−a2)y+a1b2−a2b1.

This follows directly from (2x+a1)(x+b2)−(−2y+a2)(y+b1). On the slice it is2(x²+y²), consistent with simple nonzero roots. Mere Jacobian vanishing is insufficient for no section: x↦x³ has a continuous global inverse. The proof correctly uses the actual square restriction.

An independent route verifies the supplementary invariance-of-domain application: E is globally charted by (a1,a2,b1,b2,x,y), solving the two constants explicitly. The coefficient projection Q has unique preimage atzero. The two chart points with all four linear coefficients zero and roots(±t,0) are distinct but have identical coefficient images and converge tozero. A hypothetical local section is an injection; invariance of domain makes its image an open neighborhood containing both close points, contradicting injectivity of Q on a section image. No fibration assumption is used.

For the harmonic discovery form F+2iG=z²+alpha*z+beta*conjugate(z)+gamma, direct real/imaginary expansion verifies alpha=(a1+2b2+i(2b1−a2))/2, beta=(a1−2b2+i(2b1+a2))/2, gamma=a0+2ib0. This is an equivalent representation for discovery, not a new historical-resolution claim.

On puncturedC, the complements of the two opposite closed rays are open branch domains and cover all nonzero points. Their branch square roots prove the two-domain upper bound; the same loop excludes one global branch. Includingzero changes local sectionability. A closed ray includingzero can support a root when filtered/non-open domains are allowed; that changes admissibility. A homotopy section over contractibleR6 can be constant, since its projection is homotopic to identity; it does not satisfy exact strict selection. No finite-genus repaired problem is computed here.

For fixedε>0, every square root has modulus sqrt(|w|), so zero lies strictly withinε of both roots when|w|<ε². At equality it is on theε boundary. This checks the manuscript's strict inequality and explains why its exact local obstruction does not settle2B. Off-slice approximate claims are not asserted.

The local obstruction excludes the member of any hypothetical open cover that containszero. Hence the admissible-cover class is empty at every cardinality; notation+∞ for no finite cover does not imply an infinite cover exists.

The checker is an exact polynomial/quadratic-range certificate, not a topology checker. The high-degree model's exact commonzero at t=1/128 independently confirms its invalid nonzero-path claim, while rejection occurs on the supported-degree guard before any full high-degree positivity analysis. Extra optimized tests include an interior minimum9801/19801<1/2 with acceptable endpoint values; this confirms why evaluating only endpoints would be insufficient. Removing the lower-bound guard in a private intentional bad mutant makes a zero-crossing lift pass, while the original checker rejects it. A determinant-sign mutant fails the general identity. These strengthen control materiality without promoting computational checks into continuity/topology proofs.
