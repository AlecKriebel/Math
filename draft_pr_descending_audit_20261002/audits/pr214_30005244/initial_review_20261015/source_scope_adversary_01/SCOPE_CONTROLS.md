# Exact scope-falsification controls

These are review controls of implications used to interpret the source, not repairs or additional author proof attempts.

## Boundary-null geometry implies (G)

Let Ω be bounded with |∂Ω|=0. Consider any cubic cell centered at xₘ, and classify the entire cell by xₘ∈Ω. If a point x in that cell is classified differently from xₘ, the segment between them meets ∂Ω, so dist(x,∂Ω)≤√3h (a harmless bound larger than the cell radius). Thus Ω_h△Ω lies, up to cell boundaries, inside the √3h neighborhood of ∂Ω. The boundary is compact and null, so these bounded neighborhoods have measure tending to zero. The estimate does not depend on the grid translation. This verifies the candidate's stated physical-particle coverage.

## Bounded openness alone does not imply (G)

Take C=(0,1)³. Enumerate Q³∩C as qₖ. Choose positive radii rₖ so that the sum of volumes of their balls is at most ε<1/2, and put U=C∩⋃ₖB(qₖ,rₖ). Then U is bounded open, contains every rational point in C, and has volume at most ε. On xₘ=m/n, membership in U is exactly membership in C: all grid centers are rational, and U⊂C. Consequently U_(1/n) is the same voxel union as for C and converges in volume to C. The inequality

    |U_(1/n) △ U| ≥ ||U_(1/n)|−|U||

therefore gives liminf |U_(1/n)△U|≥1−ε>0. This falsifies the automatic implication “bounded open ⇒ (G)” for arbitrary point-membership meshes. It does not establish off-interval spectral failure for this U and is not claimed to do so.

## What these controls adjudicate

The positive theorem's explicit regular classes really are covered. Its general hypothesis is an added precise consistency condition, not a theorem of topology alone. Nothing in the imported descriptive question requires classifying all failures of that condition. The author TURN_2 construction supplies its own separate spectral obstruction for an unrestricted compact interpretation.
