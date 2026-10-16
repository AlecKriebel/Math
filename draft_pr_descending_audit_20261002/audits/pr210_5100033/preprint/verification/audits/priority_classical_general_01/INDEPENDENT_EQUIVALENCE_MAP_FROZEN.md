# Independent equivalence and obstruction map — frozen before inherited priority reading

UTC: 2026-10-15T12:17:29Z. Audit completion estimate: 10%.
Inputs read: parent INTAKE.json; submitted original PROOF.md and SOURCES.md only. No inherited review, old priority report, current other-shard report, or PR211 report has been read. This document freezes the independently derived approach map; later additions go elsewhere.

## Exact target and boundaries
The target is B_+(w) B_-(w) for signed areas of feet from the original two foci onto the tangent lines at the vertices of a primitive odd-period confocal elliptic billiard. The tangent lines are sides of the outer polygon. The source label is arXiv v11 k605,a / published k606. Chord-pedal, antipedal/inverse, inner-polygon and hyperbolic-caustic results are distinct until an exact bridge is proved. Stars must retain ordered signed area and all coprime turning numbers.

## Independent geometric reduction
Write E: x²/a²+y²/b²=1, c²=a²-b², X=(a cos θ,b sin θ). The plus focal foot is
Q_+(X)=(a²(c+x)/(a²+cx), a²y/(a²+cx)).
It lies on x²+y²=a². Thus it is the restriction of a real projectivity P_+ represented by [[a²,0,a²c],[0,a²,0],[c,0,a²]], with positive real denominator a²+cx. P_- follows by c -> -c. Consequently each focal pedal polygon itself is a Poncelet polygon between the auxiliary circle S and the projective image P_±(C) of the original caustic C. This is a circle/conic Poncelet family. It must not be assumed to be a circle/circle family.
On the unit-circle parameter ζ=exp(iθ), Q_+/a=(ζ+t)/(1+tζ), t=c/(a+b); Q_-/a=(ζ-t)/(1-tζ). This is a real disk Möbius transformation on the boundary and a plane projectivity on the conic. These two extensions have the same restriction on E after normalizing x/a,y/b.
The same-focus signed-area sum is A_+(w)=1/2 sum det(Q_+(w+jδ),Q_+(w+(j+1)δ)); the opposite focus corresponds to w+2K. Odd N turns that shift into half of the reduced real period L=4K/N. A prior theorem would need to prove A(w)A(w+L/2) constant for this special circle/conic pair, or an exactly equivalent expression.

## Approach families and falsification gates
1. General Poncelet area theorem: inspect exact hypotheses and whether a product of paired signed circle-inscribed areas is covered. Constancy of one area, of an outer/inner ratio, or a sum of angle functions does not suffice. A pair of circle/conic Poncelet polygons is a plausible entry point.
2. Inversive/pedal/polarity theorem: derive exactly which points, conics and reference foci transfer. Inversion of a vertex or an antipedal construction is not orthogonal projection of a focus to a tangent. A theorem with a circle as both outer and inner conic needs proof that P_+(C) is a circle; likely false in general, test symbolically/numerically.
3. Jacobi cyclic identities: the area sum is a cyclic rational Jacobi expression. Identify the exact expression, pole locations, shifts and character. A generic product/trace identity might apply, but merely rewriting the invariant as an elliptic identity transfers the central task. Mark blocked unless the published identity actually implies the expression.
4. Classical auxiliary circle: Q_+ lies on radius-a circle; this property alone gives no area product invariant. Preserve classical credit independently of application priority.
5. Two-pole trace/character lemma: the submitted proof reduces to an elementary elliptic-function divisor argument. It is a classical mechanism, not a new general method. Prior application priority still needs an exact older published argument for this focal map or a theorem with hypotheses verified here.
6. Boundary controls: even N should not be silently included; non-confocal caustics/circle-conic Poncelet pairs need testing; signed areas and primitive stars cannot be discarded. A general theorem that predicts too much should be falsified with explicit examples.

## Strongest initial deduction and remaining gap
The circle/conic Poncelet reduction is an exact candidate bridge. It does not establish older coverage. The key open audit task is whether an actual primary general theorem covers the product of the two paired transformed areas for this special pair. Search absence cannot certify novelty.
