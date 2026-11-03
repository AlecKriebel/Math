# Independent mathematical review

Reviewed 2026-10-21 UTC.

Target: AUDIT.md
SHA-256: fb7c9e575ab599630c234e1ecbb6ee11154101b50937624728bba9167cbbaf9d
Byte count: 16247

Decision: ACCEPT the explicitly limited mathematical claims in this exact version. This is not an acceptance of a full solution to the original AIM question, a novelty claim, or unrestricted mock-weight coverage.

## Checks performed

1. Recomputed the h derivative elimination: the sixth-power identity and order-two equation are correct, with h rather than raw E4 h as unknown.
2. Checked the polynomial weight-cancellation formula for integral nonnegative weight. The symmetric-power construction gives a genuine finite-dimensional weight-zero composition representation and the stated dimension bound.
3. Checked the cusp repair. The stipulated finite-cover logarithmic Laurent expansions imply unipotence on the realized span of component functions. Wronskian and numerator determinant characters agree; after that cover their punctured-disk scalar functions have finite-power growth and extend meromorphically. Their quotients therefore extend. This proof does not confuse finite-dimensional with finite-image monodromy. Derivatives with respect to a nonconstant meromorphic modular function preserve finite principal-part/logarithmic control, since its reciprocal local derivative is meromorphic of finite order.
4. Checked finite field descent. The derivation extends to K=C(X_Gamma), and restriction of scalars gives the factor [K:C(t)]. This works for higher-genus modular curves and for algebraic-coefficient linear equations.
5. Checked Bol operator leading coefficient, weights, invariant right-hand side, and the dimension 1+sum n_i. Direct calculation confirms B_3=delta^3+2{tau,t}delta+delta{tau,t}.
6. Checked the negative-weight obstruction. Bol covariance gives the stated period-polynomial orientation. Nonconstant periodic f is not rational in tau. The rational coefficient A in a proposed branch relation has distinct poles, forcing every coefficient to vanish. A finite-index intersection still contains a power of the lower unipotent matrix. Paths avoiding the discrete bad locus project to loops realizing the required branches, contradicting a finite-dimensional ODE solution space.
7. Independently inspected Mertens--Raum's public v3 HTML, Section 3.2, Example 3.10, and its preceding definitions. The weight -10, level-one f_Delta example, its Delta shadow, its T-periodicity, and its explicit polynomial cocycle support the stated example. Its displayed internal-degree cocycle terms cannot arise from a constant function. Multiplying by E4 gives total weight -6; factoring out E4 leaves the same rational-pole obstruction. This does not require a weakly holomorphic modular factor. The report correctly isolates the cuspidal-shadow / Bol-image condition rather than assuming it for every moderate-shadow convention.
8. Independently checked the h/Delta alternative. The derivative differential has residue zero at elliptic poles because of its nontrivial stabilizer character, so the affine primitive transformation is legitimate. The raw E4 h/Delta obstruction is correct within the stated weak-factor convention.
9. Checked the differential-algebraic conclusion. v=Dt is a weight-two meromorphic modular form with the required cusp control, hence D-finite by the nonnegative-weight theorem. Differential-algebraic functions form a differential field, so v^(W/2)U is differentially algebraic for the even integral weights under discussion, including negative W. This does not imply D-finiteness.
10. Checked the completion anomaly formula and the double-exponential counterexample. The xi-operator sign is correct. A rational-coefficient companion system has only polynomial coefficient growth along a sufficiently far positive real ray, so Gronwall excludes exp(exp(t)).

## Scope and minor editorial observations

- Coefficients are in C(t), not necessarily Q(t).
- The negative-weight argument excludes linear ODEs, not nonlinear differential-algebraic equations.
- The finite-cover cusp expansion assumption is stronger than necessary. One can instead permit arbitrary complex cusp exponents and untwist the common determinant character, but this generalization is not required for the accepted report.
- In Approach 2, selecting nonconstant t in K before first mentioning its delta-Wronskian would improve exposition without changing the proof.
- “Re-verification of the existing result” in Approach 1 should be understood as verification of the prior proposed equation for Guerzhoy's existing example, not as an independently verified claim that Guerzhoy printed this exact j-equation.

No changes were made to AUDIT.md. No queue edits or publication actions were taken.
