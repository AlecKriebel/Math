# Why the diagonal filter stops at derived subgroups

This is an elementary exact example for DIAGONAL_PARABOLIC_OBSTRUCTION.md, not a further obstruction or a solution.

Let H=F(a,b), A=F(a₁,b₁)×F(a₂,b₂)×⟨z⟩, and P=F(a₁,b₁)×F(a₂,b₂). Define commuting embeddings

    α(a)=(a₁,1,z),   α(b)=(b₁,1,1),
    β(a)=(1,a₂,z⁻¹), β(b)=(1,b₂,1).

The combined map j:H×H→A, (h,k)↦α(h)β(k), is injective because projection to the first two free factors recovers h,k. Write ε_a:H→Z for the exponent sum of a. Then

    j(h,k)=(h₁,k₂,z^{ε_a(h)−ε_a(k)}),

so j(ΔH)≤P, but neither α(H) nor β(H) is contained in P. Therefore the theorem cannot generally strengthen its conclusion from α(H′),β(H′)≤P to the whole images. Every commutator has ε_a=0, so both derived images do lie in P. In particular j([a,b],1) lies in P and is not diagonal.

The exact intersection is

    j(H×H)∩P=j({(h,k):ε_a(h)=ε_a(k)}),

which is strictly larger than the diagonal. This example also shows why cancellations in shared abelian/root coordinates must be allowed in the proof; the nonabelian direct factors alone do not describe every original generator.

For abelian H=Z, the automorphism (x,y)↦(x−y,y) of Z² takes the diagonal onto the second coordinate factor. Thus no analogous obstruction excludes every nontrivial diagonal without the nonabelian hypothesis.
