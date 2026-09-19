# Remaining mathematical obligations — local audit edition

The local audit runs and repairs the existing proof bodies. Its verification
report records actual compiler and axiom results. The distinction below is
between **existing ingredients** and **mathematics that is still missing**.
Compiler acceptance of the ingredients does not close these four gaps.

## 1. Complete the arbitrary finite-quotient lifting theorem

Written: automatic residue-ring linearity; all Lie-ring automorphisms versus
invertible bracket-preserving matrices; p-adic quotient coordinates; explicit
p-adic generation; the `i-6` bilinear error estimate in a torsion-free common
module; word-induction preservation; weighted-flag reduction; full and
infinitesimal flag rigidity; two-lattice power bounds.

Missing: assemble the concrete common rational vector space, A and B lattice
models and all their inclusions; construct representatives of **arbitrary**
finite-quotient automorphisms and derivation solutions; establish the needed
unit determinant/invertibility assertions and residue identifications; combine
the written lemmas into the theorem that every representative lies in `1+J`
or `J`. The generic lemmas' hypotheses have not all been instantiated and
discharged. Do not assume an exact infinite-Lie-algebra automorphism lift.

## 2. Finish exact exponential/logarithm equivalence

Written: explicit near-identity power gains in the two coordinate lattices,
finite geometric inverses, the three commuting differential tensor actions,
the actual nonlinear tensor action, and the exact conditional factor-to-kernel
argument when an integral invertible factor is supplied.

Missing: define the applicable exponential and logarithm; prove convergence or
a sound finite specialization; integrality, inverse identities, and precision
preservation on the actual lattices; identify the tensor exponential; prove
integrality and invertibility of the actual `U(X)` series; obtain a bijection
between the **entire** finite Lie automorphism set and the **entire** derivation
kernel. `fixed_iff_derivation_of_factor` has an explicit factorization
hypothesis; it is not a substitute for proving that factorization.

In particular `J` is not silently identified with `p End(A)`. The written
power estimate retains its actual two-power coordinate loss. Do not divide in
`ZMod(p^i)` by arbitrary nonzero elements.

## 3. Certify the actual Smith computation and final kernel count

Written: the actual bracket-derived matrix and row/column indexing; complete
kernel versus derivation equivalence; a 30-dimensional injective inner-
derivation witness, with its rational left inverse transported to every
characteristic-zero field; scalar kernels over composite residue rings;
diagonal and padded kernel counts; kernel transport under invertible maps;
a soundness proof draft for a **generic** elementary-operation circuit checker.

Missing: a practical local-Smith certificate algorithm with the required exact
p-power divisions, and a proof that the **actual** 931-pivot plan is accepted for
the **actual** 14415-by-961 matrix. The generic circuit checker has not been
connected to that plan. Its acceptance hypothesis is not discharged. No complete
matrices for a Smith transformation have been materialized or benchmarked.

Combine the accepted lower-rank/invariant data with
`characteristic_zero_rank_upper`, not a zero finite-precision residual alone.
Then instantiate the scalar/diagonal kernel theorems to obtain the actual
`1009^(30*i+1689)` count. The full count for K is still absent.

## 4. Validate BCH and recover all group automorphisms

Written: actual finite Lie-ring definitions and a length-847 monomial-vanishing
proof draft leading to mathlib's 846th lower-central term being zero; a
Dynkin-Specht-Wever reconstruction proof for Lie words; collected-coefficient
soundness for integer homogeneous Lie-polynomial identities with an explicit
injective-degree-scalar hypothesis.

Missing: construct the finite BCH product, prove its coefficients meaningful,
associativity, identity and inverses; prove its agreement with the paper's
construction; prove **both directions** of the full group/Lie-ring automorphism
correspondence. The Dynkin helpers do not provide a completed BCH polynomial,
formal primitive/free-algebra infrastructure, or a Lazard theorem. Counting
only Lie maps which induce group maps is insufficient.

Only after these steps can the group cardinality, ordinary `MulAut` cardinality
and notebook corollary be closed. They are intentionally absent rather than
hidden behind an axiom or a theorem with the desired result as a hypothesis.

## Cross-cutting validation

Consult the local verification report for actual source compilation, axiom
queries, statement review, and finite-check measurements. Future mathematical
extensions require fresh compiler checks and review of their exact hypotheses.
The ordinary kernel path remains the reproduction standard.

Check the deposited DOI archive identity. Inspect actual elaborated statements
and instance choices after compilation, including `LieRing`/`LieAlgebra`
structure values and the final ordinary group automorphism type. Re-run actual
axiom queries and a fresh same-kernel recheck. Novelty and external mathematical
review are separate from those checks.
