# Turn 1: recover modular data from the ordinary torus sector

Timestamp: 2026-10-03T09:28:00Z. Outcome: partial; original problem unresolved.
Completion estimate toward the general converse: 15% (subjective, not a probability).

## Attempt

Try to reconstruct the Drinfeld center from the ordinary TQFT. The first step really is possible: one can recover the center's *based modular data*, not merely its torus representation up to arbitrary conjugacy.

Let C be a unitary fusion category and B=Z(C), equipped with its canonical unitary modular structure. Use the anomaly-free RT normalization corresponding to TV_C. Write A=Z(T^2). The product of a pair of pants with S^1, the product of a disk with S^1, and its reverse make A into a commutative Frobenius algebra (A,mu,eta,epsilon). Fix the standard meridian/longitude parameterizations once and for all. Let s be the torus mapping class represented in the standard simple-core basis x_i by the unitary symmetric normalized S-matrix.

In that basis:

    x_i x_j = sum_k N_ij^k x_k,
    eta(1)=x_0,   epsilon(x_i)=delta_i0.

These formulas follow by cutting P×S^1 into the usual fusion cobordism; equivalently this is the complexified Verlinde algebra. Put D=sqrt(sum_i d_i^2), so S_0j=d_j/D>0. The primitive idempotents are

    p_j = S_0j sum_i conjugate(S_ij) x_i.

Indeed the character x_i -> S_ij/S_0j diagonalizes fusion (Verlinde), and unitarity gives the idempotent equations and sum_j p_j=x_0. Consequently

    epsilon(p_j)=S_0j^2,
    s(p_j)=S_0j x_j.

For the second identity, the coefficient of x_k is S_0j times sum_i S_ki conjugate(S_ij)=S_0j delta_kj, using symmetry and unitarity of S.

Thus the distinguished simple-core basis can be recovered intrinsically, up to permutation, from ordinary closed-surface and 3-cobordism data:

    x_j = s(p_j)/sqrt(epsilon(p_j)),

where the positive square root is unambiguous. In particular, no arbitrary choice of eigenvectors or their phases is being silently made.

## Naturality consequence

An isomorphism alpha between two such ordinary TQFTs preserves mu, eta, epsilon, and s. It permutes primitive idempotents, preserves their positive epsilon-values, and therefore sends x_j exactly to x'_pi(j). It fixes the vacuum label because it preserves eta. Naturality for the torus Dehn twist gives equality of the twist matrices under the same permutation. Naturality for s gives equality of S, and the product gives equality of all N_ij^k. Since S_00=1/D, it also preserves every d_i.

This proves a necessary relation on the centers of the original fusion inputs: their full based S,T,fusion,dimension data agree up to a common vacuum-preserving relabeling.

## Boundary of this attempt

The argument uses positivity to fix square roots and is stated only in the unitary subcase. It does not claim that the underlying input fusion rings agree. Most importantly, S and T do not generally determine the braided tensor category: recovering the associator and compatible multiplicity-space identifications is still missing. No center equivalence, Sato equivalence, or full solution follows from this turn.

Dependencies: the standard RT torus/Verlinde construction, and the TV-to-center comparison in SOURCE_AUDIT.md. The reconstruction calculation is written out above; it is not an independent novelty claim.
