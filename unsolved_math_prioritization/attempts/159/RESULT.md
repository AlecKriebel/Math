# Uniform independent summands: five-turn partial results

Problem 159 / GREEN-071, currently Problem 28 in Ben Green's maintained list. **Original arbitrary-support question remains unresolved after five substantive turns.** No full-solution or novelty claim is made. Independent review of this frozen packet is pending.

## Exact target

X and Y are independent, integer-valued random variables with finite positive-probability supports and arbitrary real probabilities. If X+Y is uniform on its support, must both summands be uniform? The support need not be a consecutive interval. Translating to zero minima and normalizing by leading coefficients gives monic nonnegative-real factors A,B of a Boolean polynomial C with C(0)=1. Endpoint and coefficient bounds force A(0)=B(0)=1 and every factor coefficient into [0,1].

## Scoped deductions

1. Any rational-probability summand forces both summands uniform, in all degrees. A counterexample requires irrational algebraic coefficients in both normalized factors, with a shared coefficient field. First fractional coefficients from either end must be complementary at matching distances. An admissible factorization positive under every field embedding is fair; the sign-preservation hypothesis is not automatic.
2. Uniquely represented sums force unit coefficients. A colliding forced-unit pair is an exact support obstruction. Residue classes exclude the entire family 1+a x^d+x^(rd), 0<a<1, r≥2, and its reversed variants. The bounded support scan covers both factor degrees at most 8; it is not a theorem for all total degrees or supports.
3. If the product matches its reversal through half the smaller factor degree, both factors are Boolean. This localizes the credited classical inward argument. Every unfair factorization must have an asymmetry in that outer window. Generic multiplication or reflected padding does not reduce arbitrary products to this case.
4. A seven-equation integer polynomial identity gives an exact contradiction for a credited degree-20 residual system. It excludes all common dilations and translations of one explicit support pair that the simple unique-sum criterion cannot reject.
5. Every fixed product has finitely many monic divisor/cofactor pairs, giving exact finite-degree decidability and a counterexample semidecision search. Fixed-degree compactness yields qualitative stability near exact factors; for a known fair product these limits are fair. Neither supplies a universal degree bound. Infinite formal series and signed epsilon-unfair factors do not meet the original hypotheses.

Proofs, boundaries and failed inferences are in TURN_1.md through TURN_5.md. The literature-derived ingredients, current-source updates and reading limitations are explicit in the source files. Finite controls supplement, rather than replace, the written all-degree arguments.

## Current literature boundaries

Ghidelli and Hare supply established partial cases and algorithms. Dvorsky's 2026 trinomial result has a separate finite-degree companion dependency that was not retrieved; its long analytic proof is not certified here. The September 2026 epsilon-unfair theorem explicitly permits negative coefficients. Zhang's current primary report states a total-degree-66 computational bound, while its linked repository README states degree 45. Neither computation was replayed here and neither solves arbitrary degree.

## Remaining gap

Exclude every asymmetric irrational algebraic nonnegative factorization in arbitrary degree, or exhibit one exact finite counterexample. A uniform degree bound or uniform algebraic obstruction theorem would suffice but has not been proved. No sixth author search is included.
