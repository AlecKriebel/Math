# Final adversarial promotion audit

Checkpoint: **2026-09-15 04:32 UTC**. Bounded adversarial audit completion: **100%**.

## Verdict

**Pass for the mathematical claim.** I found no unresolved mathematical gap or counterexample in the current proof that the specified BCH group satisfies

    |G| = |Aut(G)| = 1009^52359.

This was a fresh adversarial review of the manuscript and verifier source, followed by review of the two specialist reports. It includes a new direct comparison of the portable group export against a reconstruction from the manuscript formulas. This is an AI audit of a computer-assisted proof; it is neither external human peer review nor a proof-assistant formalization.

The mathematical claim is stronger than a matching numerical prediction: the lifting and logarithm arguments bound and count every finite Lie-ring automorphism, and the Lazard equivalence preserves every group automorphism.

## Attempts to falsify the chain

### Missing finite-field components

I specifically tested whether repeated radical summands, central shears, nonsquare determinant classes in PGL2, or a disconnected equivariant component could evade the proposed classification. The characteristic radical N and its characteristic commutator N′ prohibit mixing a radical V2 into the Levi quotient and prohibit W → U. Equivariance excludes central shears from all nontrivial simple summands. After conjugating the Levi complement using the two explicit H1 steps, the only possible additional blocks are exactly the U → W coefficient and the V/R matrix in the paper.

The U → W coefficient is killed by the nonzero P5 cross term. Invertibility gives both MᵀM = a³I and MMᵀ = a³I. Applying the latter to the nonisotropic vector (1,1) forces a=1. The residual orthogonal action on its one-dimensional orthogonal complement has exactly two possibilities, even though 1009 has many roots of unity. The involution τ supplies and accounts for the second possibility. PGL2 already includes both square and nonsquare determinant representatives; the field F1009 has no nontrivial field automorphism. Thus there is no uncounted finite component.

The flag obstruction for s=diag(−1,1) uses the U component and remains valid with τ present. The τ-only obstruction uses disjoint weight supports. Therefore the proof does not accidentally check the connected or inner subgroup alone.

### Invalid passage from approximate finite maps to integral maps

The error estimate E_Q(B,B) ⊆ p^(i−6)B is valid before Q is known to preserve B: all maps and brackets extend to the common rational vector space. Starting from Qx,Qy ∈ A ⊆ B, word induction proves integrality on B. Integral generation is supported by a unit determinant modulo p, rather than rational generation alone. A unit determinant of Q in the A basis is the same determinant in the B basis. These facts establish Q(B)=B and validate reduction modulo p.

The derivation version does not need invertibility; its Leibniz-error induction supplies integrality, after which infinitesimal flag rigidity applies. Every finite additive endomorphism is linear over Z/p^i, so there is no omitted nonlinear additive case.

### Logarithms admitting or losing solutions

J is contained in p End(B), but need not equal p End(A). The proof correctly uses both lattices: J^r ⊆ p^(r−2)End(A). Consequently even large-degree denominator terms remain integral and converge. The telescoping estimate for differences uses noncommuting products and yields p^(i+r−5)End(A), enough at every degree with a nonunit denominator. It gives a bijection at the same modulus p^i, not at a weaker modulus.

For the tensor action, X^7 ∈ p End(T) makes U(X) invertible modulo p; the tail with factorial denominators is strictly p-divisible because p=1009 is far larger than the lattice loss of six. Thus exp(X)ν−ν and Xν have exactly equivalent divisibility. This avoids the common invalid inference that a finite-level bracket-preserving exponential must arise from a derivation merely by formal differentiation. Here it follows from a proved invertible operator factor.

### Rank deficiency hidden above the computation precision

A zero residual matrix modulo p^6 alone would not establish rational nullity. The independent rank bound repairs precisely that possible gap. Integer Jacobi and the rank-30 inner subspace give 30 independent rational derivations of B. Rational scaling and the basis change identify the rational Lie algebra of L with B, carrying those independent kernel vectors to L. Hence the scaled matrix has rank at most 931. The 931 nonzero local pivots prove the reverse bound. There can be no hidden additional nonzero invariant at valuation six or above.

I inspected the C++ local elimination source. Unit normalization and exact division by pivot powers implement legitimate operations over Z/(p^6). Conceptually clearing a pivot row by column operations affects no other active row because the pivot column has already been cleared. Checking global divisibility at each new valuation level suffices: all subsequent row operations preserve that divisibility. Products of residues below 1009^6 fit the declared unsigned 128-bit arithmetic. The integer bracket and Jacobi stages are far inside their integer bounds.

A fresh replay of the available compiled verifier completed with `ALL_CHECKS_PASSED`, rank 931, nullity 30, and valuation multiplicities 87,55,758,6,25 at valuations 0,1,2,3,4. This replay used the existing compiled verifier; compilation and full Python regeneration belong to the separate computational reproduction audit.

### Wrong group exported or wrong Lazard range

I reconstructed the original integer transvectants directly with factorial derivatives in a fresh standard-library Python check, then performed the displayed adapted basis change and scaling. I did not import supplied coefficient-generation code or read a precomputed coefficient archive for this check. All **199** exported nonzero bracket terms matched exactly, including signs, basis indices and integer coefficients. All **4,495** distinct Jacobi triples of the exported scaled bracket then vanished over the integers. The exported prime, rank, weights, depth, order exponents and BCH truncation length agree with the manuscript.

The exact order is additive rank times depth, 31·1689=52359. The bound γ_847(L) ⊆ p^1694 B ⊆ p^1689 L establishes class at most 846, strictly below 1009. BCH denominators at degree at most 846 have no factor 1009, including the Dynkin conversion denominator. The cited correspondence is for finite p-power Lie rings of class below p, and does not require additive exponent p. Thus this construction is within its actual range.

## Artifacts examined

- `report/kourovka_16_63.tex`
- `scripts/independent_verify.cpp`, `smith_local.py`, and `export_presentation.py`
- `data/smith_pivot_plan.txt` and `data/group_lie_presentation.json`
- `audit/finite_flag_audit.md` and `audit/padic_count_audit.md`
- Current successful `logs/resume_cpp_verify.log`, plus a fresh verifier replay

The manuscript SHA-256 at the direct comparison checkpoint was
`c82ce52c34928e87fda3d31a2bfd6cad33616f79434956fcdab7c090fe5ccdd3`.
The portable JSON SHA-256 was
`d060acc6eb31c106ab31f64b139c07c9eb1ef978c648cdbbc5d1ee1a9987e22e`.
Later purely editorial changes to the manuscript may change its hash; mathematical changes require renewed review.

## Strongest verified statement and exact remaining boundary

The explicitly specified Lie ring and its BCH group satisfy the stated full-automorphism equality by the combination of the proof and exact checked Smith certificate. **No central mathematical gap remains identified in this audit.**

This audit does not certify historical novelty, the truth of an attribution about who originally solved the problem, visual publication quality, successful deployment, or the reproducibility agent’s still-running full regeneration. Those are separate factual or publication checks. Before promoting the final package, finish that regeneration and ensure the paper distinguishes the supplied software environment from the environment of the new reproduction. No external individual was contacted and no commit, push, or release was made by this reviewer.
