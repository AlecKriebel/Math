# Five substantive approaches

Research date: 3 October 2026. Final outcome: **unsolved, 5/5**.

1. **Galois detection and dimension.** Proved the field inclusion and separated the odd-prime conductor test from the stronger binary field-equality requirement. Gave a full proof for ordinary characters of positive degree less than p. Generalization stops when complete p-orbits can occur among the high-order constituents.
2. **Clifford homogeneity.** Recovered the known normal-Sylow result via a fixed point in the p′-sized homogeneous constituent orbit. Proved faithful-quotient and direct-product reductions. Nonnormal Sylow restrictions lose the required homogeneity.
3. **Modular top-order multiplicity.** Proved that a nonzero-mod-p order-p^a linear-constituent count suffices. Constructed an exact reducible family whose global top conductor disappears on P, exposing the gap in a proof that does not use irreducibility. Also recorded the p=2 conductor-only obstruction.
4. **Mackey induction.** Proved the high-order multiplicity congruence for induction from proper p-subgroups and for p′-index subgroups. Derived the monomial p′-degree case, within the published Isaacs–Navarro/Hung–Schaeffer Fry mechanism. Primitive nonlinear characters and the conductor-to-multiplicity implication remain outside this argument.
5. **Generalized decomposition numbers.** Tested whether the 2026 conductor-detection theorem closes the gap. It detects individual coordinates rather than their degree-weighted sums. The reducible family provides explicit cancellation, so an additional irreducibility-based theorem is still needed. Identified a limited odd-prime sufficient condition with p-group centralizer, without asserting that it always occurs.

## Exact checks

The standard-library verifier compares multisets of character exponents under the unit group of a cyclotomic modulus. By linear independence of irreducible characters, this computes the field's Galois stabilizer exactly. Conductor is computed by testing which cyclotomic subfield kernels lie in that stabilizer.

- Five reducible examples: p=2,3,5,7,11; index p in each case; character norm p+1 verifies reducibility.
- Binary warning: the field of 1+λ+λ^(-1) on C_8 has conductor 8 and index 2.
- 7,229 bounded positive-degree<p cyclic-character cases satisfy the target.
- 748 high-order multiplicity congruences for proper cyclic p-subgroup induction satisfy the proved congruence.

Finite tests support and audit the displayed examples; the proofs in the attempt notes establish their stated general special cases. No test is promoted to an all-finite-groups conclusion.

## Remaining mathematical gap

For an arbitrary irreducible p′-degree χ, one needs to show that the top p-power irrationality of its global field survives in χ_P, with full cyclotomic field generation when p=2. Proving that the maximal nonzero-mod-p linear-constituent level equals the global conductor level would suffice. No proof of that assertion, or irreducible obstruction to it, was obtained.
