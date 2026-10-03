# Attempt 1: determinant normalization and the residual central scalar

## Mechanism

The matrix-dilogarithm proof of the pentagon identity determines an intertwiner only up to a scalar. Its determinant normalization is the point at which an Nth root of unity remains: see Baseilhac–Benedetti, *Analytic families*, §8A, equations (66)–(68), [published paper](https://msp.org/agt/2015/15-4/agt-v15-n4-p05-s.pdf). We tested whether determinant-one normalization alone, perhaps supplemented by a trace condition, could eliminate this last ambiguity.

## Exact linear-algebra result

Let A and B be invertible d-by-d complex matrices, with A = λB and det(A) = det(B) = 1. Then λ^d = 1, by taking determinants. Conversely, every λ in μ_d preserves determinant one. Thus determinant normalization supplies exactly a μ_d-valued freedom, not a distinguished scalar. If a linear functional ℓ is nonzero on B, the additional condition ℓ(A) = ℓ(B) fixes λ = 1. But this requires ℓ(B) ≠ 0 throughout the family and compatibility of that normalization with every tensor identity. Neither follows from the determinant condition.

This distinction is not remedied by the oddness of N. For any odd N ≥ 3, put ζ = exp(2πi/N), and define operators on the basis e_j, j in Z/NZ, by

    X e_j = e_(j+1),       Z e_j = ζ^j e_j.

Both have determinant one: X is an N-cycle, so det(X)=(-1)^(N-1)=1; and det(Z)=ζ^(N(N-1)/2)=1. Also X^N=Z^N=I and ZX=ζXZ. Consequently the classes of X and Z commute projectively, whereas no scalar changes X'=aX, Z'=bZ can make the two matrices commute: Z'X'=ζX'Z'. Their traces both vanish, so trace normalization is unavailable on these generators.

More fully, define A_(a,b)=X^a Z^b. Direct multiplication gives

    A_(a,b) A_(c,d) = ζ^(bc) A_(a+c,b+d).

Associativity is equivalent to the cocycle identity

    bc + (b+d)e = de + b(c+e)  (mod N).

This determinant-one projective representation of (Z/NZ)^2 cannot be made genuine by scalar changes because the commutator above is unchanged. It is an explicit counterexample to the proposed general inference “all generators have determinant one, so all scalar anomalies disappear.” It is NOT a counterexample to the quantum-hyperbolic problem; we have not identified this projective representation with the complete move calculus of any original triple.

## Verification and outcome

The accompanying exact verifier checks the displayed monomial-matrix relations, determinants, traces, multiplication rule, and cocycle identities for N=3,5,7,9. It uses integer exponents modulo N; no approximate complex phases are used.

The route is blocked. A solution needs additional coherent scalar information specific to the quantum-dilogarithm moves. Determinants and occasional nonzero matrix coefficients provide no global normalization theorem. The known sign correction likewise cannot determine the remaining μ_N factor.

**Result:** rigorous diagnostic obstruction to an insufficient normalization method; no new QHI counterexample and no complete resolution.
