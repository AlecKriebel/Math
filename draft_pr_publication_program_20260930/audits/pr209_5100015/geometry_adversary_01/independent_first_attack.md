# Sealed independent first attack

Timestamp: 2026-10-17 01:25:41 UTC. Completion estimate: 10% of this assigned mathematical assessment.

This file was written before reading the manuscript, inherited review reports, root mathematical assessments, or native custody. The only inputs are the assigned claim and the project instructions. No inherited code has been executed.

## Claim to attack

For a closed elliptic billiard in the outer ellipse x²/A+y²/B=1, A>B>0, with inner confocal elliptic caustic diag(A−λ,B−λ), 0<λ<B, the product of signed shoelace areas of the successive intersections of outer boundary tangents and the perpendicular feet of the origin on those same tangents is phase independent when the least period N≥3 is not divisible by 4. Include coprime winding stars, reversals, and displayed repetitions of shorter admitted orbits; do not infer anything for hyperbolic or focal caustics.

## Independent local derivations

Write D=diag(A,B), n_j=D⁻¹P_j, and v_j=(P_{j+1}−P_j)/|P_{j+1}−P_j|. The boundary tangent is n_j·x=1. Consequently the actual foot is Q_j=n_j/(n_j·n_j). A competing normalization n_j, or P_j, is generally wrong.

Tangency of the chord in direction v to the inner confocal ellipse gives

λ=A v_y²+B v_x²−det(P,v)²=AB(n·v)².

The second equality follows algebraically from x²/A+y²/B=1 and |v|=1. For a consistently oriented physical orbit, put κ=√(λ/(AB)); then n_j·v_{j−1}=κ and n_j·v_j=−κ. Specular reflection yields

v_{j−1}−v_j=2κ n_j/(n_j·n_j)=2κ Q_j.

This supplies an independent check on the foot formula, reflection, and common-caustic condition. It also reduces pedal area to determinants of unit velocity differences, independently of any elliptic-function parametrization.

The intersection R_j of boundary tangents at P_j and P_{j+1} is the pole, with respect to D, of their chord. If that chord is u_j·x=h_j with |u_j|=1, then R_j=D u_j/h_j and h_j²=u_jᵀ(D−λI)u_j. This is an exact linear-algebra identity, and identifies a likely dual-conic normalization trap.

## Exact excluded-period falsification benchmark

For A=4, B=1, λ=4/5, the axis diamond P=(2,0),(0,1),(−2,0),(0,−1) has all four chords tangent to C: x²/(16/5)+y²/(1/5)=1 and obeys reflection by symmetry. Its boundary-tangent intersection polygon is the rectangle (±2,±1), with area 8; its foot polygon is the original diamond, with area 4. Product=32.

The rectangle P=(4/√5,1/√5),(−4/√5,1/√5),(−4/√5,−1/√5),(4/√5,−1/√5) is another physical orbit with the same caustic. Its horizontal/vertical sides are tangent to C. Boundary tangents are ±x±y=√5, so their intersections form an axis diamond of area 10; their feet form a square of area 5. Product=50.

Thus period 4 must be excluded. Any derivation accidentally proving all periods has a detectable flaw.

## Planned falsification

1. Derive and implement the billiard step directly by selecting the inner-conic tangent from each boundary point, then intersecting its line with the outer ellipse; check reflection independently. Do not use author sample data or author parametrization.
2. Locate closing caustics by the rotation of a physical orbit; test multiple phases and coprime winding stars, including close-to-degenerate examples and denominator control. Confirm signed shoelace areas on self-intersecting lists.
3. Check exact diamonds/rectangles above, actual orthogonal feet, tangent intersections, chord tangency, reversal, repetitions, and indexing.
4. Read the full manuscript only after this first attack is sealed. Audit every claimed reduction against the independent formulas above. Distinguish verified local geometry, validated computations, and any unsupported global invariant mechanism.
5. Record a precise remaining gap if a global proof simply transfers the difficulty to another unproved phase-invariance assertion. No novelty or priority claim is part of this review.
