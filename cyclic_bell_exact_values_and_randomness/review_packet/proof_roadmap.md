# Proof roadmap for a focused specialist review

This is a suggested reading order for the load-bearing chain.  It is deliberately narrower than “check the whole paper.”

## Route 1: exact commuting-operator value

1. Fix the convention in equation `eq:Id` and the value \(M_d=2\csc(\pi/(2d))\).
2. Check Lemma `lem:polar` first, especially
   \(|C^\dagger|^{1/2}V=V|C|^{1/2}\), support projections, and commutation with Bob's algebra.
3. Check Lemma `lem:scalar`, including the equality set \(z^d=(-1)^{d-1}\) for both parities.
4. In Theorem `thm:exact`, verify the placement of \(A_0\) in \(|L_y^\dagger|\), then the two functional-calculus terms.
5. Confirm that the upper bound uses only cross-party commutation.  Separately check that the finite order-\(d\) strategy in Appendix `app:attainment` supplies the lower bound.

Decisive question: is there any step that requires a tensor product or an invertible polar factor?  The audited answer is no.

## Route 2: equality phases without overclassification

1. Read equation `eq:global-certificate` and distinguish operator equality from annihilation on one vector.
2. Confirm that the manuscript does not infer a global polynomial relation from vector annihilation.
3. In Theorem `thm:permutation`, treat the maximizing-label and two product-one assumptions as hypotheses, not conclusions.
4. Verify the weighted-cycle characteristic polynomial and the three symmetric first-harmonic sums.

Decisive question: does this theorem construct a valid permutation orbit, or does it accidentally claim the complete maximizing face?  It should do only the former.

## Route 3: nonuniform first-family maximizers

1. Verify the root and polar-phase products in `eq:cyclic-products`.
2. Derive `eq:target-table` directly from the spectral projectors of the two weighted shifts.
3. Check the final-two-swap autocorrelation `eq:R2`.
4. Check the \(\ell^1\)-to-maximum estimate that yields `eq:guessing-gap`.
5. Replay Appendix `app:d4` independently; it is the shortest exact falsifier of all phase, Fourier, and outcome-label conventions at once.

Decisive question: can the same exact score coexist with the alternating \(d=4\) table?  The certificate says yes.

## Route 4: second family

1. Expand `eq:second-sos`; check \(1/(2d)\), Fourier orthogonality, and \(\sum|\lambda_\ell|^2=1\).
2. Recompute the geometric sum leading to `eq:Fourier-compression`, including \(r_\ell\).
3. Check the parity exponent proving \(D_\ell^d=I\).
4. Confirm \(A_\ell=\overline{D_\ell}\) is the convention that annihilates the SOS on \(|\Phi_d\rangle\).
5. Verify that \(A_1\) is exactly the first-family weighted shift, so the target table transfers.

Decisive question: is global optimality supplied by a complete valid SOS, rather than inferred from a candidate strategy?  The manuscript displays the complete SOS.

## Route 5: randomness scope

1. Compare the definitions of value conditioning and full-behavior conditioning.
2. Confirm that trivial Eve plus a nonuniform table already gives \(G>1/d^2\).
3. Confirm that the root-swapped behavior changes higher Fourier data and need not satisfy canonical full-behavior constraints.
4. Read the endpoint corollary with “deficit at most \(\varepsilon\)” as the quantified tolerance.

Decisive question: does the text ever turn “one canonical behavior is private” into “every maximizer is private,” or vice versa?  It should not.

## Route 6: optional setting appendix

The cyclic results do not depend on this route.  Check Proposition `prop:one-input` as the universal baseline.  For Proposition `prop:mub`, verify the corner-block form and keep the conclusion limited to separately bounded coefficientwise spectral terms.

## Minimal exact replay

```sh
(cd cyclic_bell_exact_values_and_randomness && python3 verification/verify_merged.py)
(cd cyclic_randomness_counterexample && python verify_exact.py)
(cd minimum_bell_randomness && python verify_second_family_d4_exact.py)
```

These two dependency-light exact programs are the shortest checks of the two-family \(d=4\) certificate.  The all-dimensional and commuting-operator conclusions still require the analytic routes above.
