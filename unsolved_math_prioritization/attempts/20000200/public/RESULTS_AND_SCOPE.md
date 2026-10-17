# Accepted criterion and precise limits

**Status: scoped_resolved1/5**, row 1793, ID 20000200. Independent acceptance is for the [adopted contract](CONTRACT.md).

Reject every one-dimensional target with u constant or v identically zero. Otherwise put K=C(D)=C(u,v) on the smooth projective normalization and define

    ω=(i du/v−du/u)/2,    ρ=du/(2v),    σ=du/(2uv).

The target is realizable if and only if:

1. Nω=df/f for some positive integer N and f∈K*, decided by the finite residue/divisor/holomorphic-comparison test.
2. Both dA+ωA=ρ and dB−ωB=σ have solutions A,B∈K, decided in explicitly bounded Riemann–Roch spaces.

For the least logarithmic exponent n, take a^n=f and set z=aA, w=a⁻¹B, x=(z+w)/2, y=(z−w)/(2i). Their reduced affine image closure is an allowed source with function field exactly K(a), prescribed signature image S and signature degree n. Every other source is SE(2,C)-congruent. A nonminimal exponent also supplies a positive certificate after factoring its Kummer polynomial and choosing a component; minimality is only required for the immediate degree claim.

The multiplicative test requires simple poles, rational residues, torsion of the cleared residue divisor, and vanishing of the residual holomorphic differential. Neither rational residues alone nor the two rational ODEs alone suffice. Norm and trace eliminate unbounded searches over further covers. The effectivity proof uses two good reductions over an explicitly represented finitely generated characteristic-zero coefficient field, with classical credit to Risch (1970). It does not bound all of J(C)_tors.

Point boundary: exactly (a,0) for a≠0 occurs for allowed constant-signature circles. The point (0,0) belongs only to excluded nonisotropic lines. These points do not enlarge the one-dimensional target claim.

The four frozen exact suites contain 49+67+12+30=158 named checks. The independent suite includes 108 additional slope comparisons within one aggregate check. Tests support conventions and examples; acceptance of the general proof is separately documented. No full normalization, Jacobian arithmetic, Riemann–Roch or inverse-signature solver is provided, and no practical complexity, priority, or unqualified AIM resolution is claimed.
