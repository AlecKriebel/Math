# Proof roadmap for a focused specialist review

This is a suggested reading order for version 1.1's load-bearing chain. It is
deliberately narrower than “check the whole paper.”

## Route 0: source baseline and normalization

1. Fix the displayed Hermitian convention in `eq:Id`.
2. Confirm the source attribution: Perito et al. proved the general bound
   $d\sqrt2$, supplied a strategy of value
   $M_d=2\csc(\pi/(2d))$, conjectured equality, and reported matching NPA
   bounds through $d=6$.
3. Compare Table `tab:exact-values` with the source's truncated decimals and
   levels: analytic CHSH at $d=2$, $1+AB$ for $d=3,4$, and NPA level 2 for
   $d=5,6$.
4. Keep the isolated printed normalization discrepancy beside Conjecture 2
   separate from the operator definition, whose augmented maximum is $M_d+1$.

Decisive question: does the paper strengthen the source bound without
reclaiming its operator definitions, strategies, NPA evidence, or second SOS?

## Route 1: exact commuting-operator value

1. Check Lemma `lem:polar`, including the strong limits placing the support
   projection and canonical polar partial isometry in Alice's generated von
   Neumann algebra.
2. Verify that $\mathcal B\subseteq\mathcal A'$ implies
   $\mathcal A''\subseteq\mathcal B'$, so every polar/functional-calculus
   factor commutes with Bob.
3. Check the kernel identities and expansion of `eq:polar-factor`; no inverse
   or unitary extension is allowed.
4. Check Lemma `lem:scalar`, including both parities and the exact equality set
   $z^d=(-1)^{d-1}$.
5. In Theorem `thm:exact`, verify the placement of $A_0$ in
   $|L_y^\dagger|$, the two positive functional-calculus terms, and the fact
   that no trace, finite dimension, order relation, or tensor decomposition
   enters the upper bound.
6. Separately verify the finite order-$d$ attaining strategy in Appendix
   `app:attainment`; the inclusions $q\le qa\le qc$ then give equality.

Decisive question: is the $q_c$ statement a genuine operator inequality in
arbitrary commuting representations? The audited answer is yes.

## Route 2: finite-dimensional support rigidity

1. Read `eq:global-certificate` and add the positive augmented residual
   $I-\operatorname{Re}(A_0B_d)$.
2. In Theorem `thm:support-rigidity` and Appendix `app:rigidity-proof`, verify
   that exact saturation annihilates every residual separately.
3. Check the Schmidt-support equivalence `eq:support-cancellation`, including
   nonfaithful $\rho_A$ and the absence of claims on $K^\perp$.
4. Verify the bad-phase exclusion and the cancellation that upgrades
   $P_y|\Psi\rangle=0$ to the polar stabilizer even when $V_y$ is globally
   only a partial isometry.
5. Check that $A_0K=K$, $V_yK=K$, and $S_y^2=\omega^yU$ make $K$ reducing
   for $U$, using finite dimensionality to pass from $U(K)\subseteq K$ to
   $U(K)=K$.
6. Recompute the adjacent half-angle reflection, apply Lemma
   `lem:reflection-rank`, and verify that the rank sum forces every root
   multiplicity to equal $\dim K/d$.

Decisive question: is the conclusion limited to every attained finite-
dimensional tensor-product exact maximizer of the **first augmented** family?
It must not be stated for $qa$, general $qc$, the unaugmented operator, or the
second family.

## Route 3: conditional permutations and nonuniformity

1. In Theorem `thm:permutation`, treat the maximizing-label and both
   product-one conditions as hypotheses, not conclusions.
2. Verify the weighted-cycle characteristic polynomial and that the same
   permutation is applied to roots and every polar-phase row.
3. Check the symmetric first-harmonic formulas; they do not control higher
   Fourier data.
4. Derive `eq:target-table` directly from the weighted-shift projectors.
5. Check the final-two-swap autocorrelation `eq:R2` and the
   $\ell^1$-to-maximum estimate in `eq:guessing-gap`.
6. In Appendix `app:d4`, independently verify the $1/32,3/32$ table,
   $G=3/32$, and $H_{\min}=5-\log_2 3$ for the displayed trivial-Eve
   realization.

Decisive question: does the theorem give an inequivalent exact behavior for
every $d\ge4$ without claiming the complete face or worst guessing strategy?

## Route 4: second augmented family

1. Expand `eq:second-sos`; check the source-v3 SOS prefactor $1/(2d)$, Fourier
   orthogonality, and $\sum_\ell|\lambda_\ell|^2=1$.
2. Recompute `eq:Fourier-compression`, including its phase $r_\ell$.
3. Check $D_\ell^d=I$ and that
   $A_\ell=\overline{D_\ell}$ annihilates every SOS factor on
   $|\Phi_d\rangle$.
4. Verify that $A_1$ is the first-family weighted shift, so the target table
   transfers exactly.
5. Keep the conventions separate: the main/SOS convention has $B_y$; the
   source appendix's all-Bob-adjoint convention is outcome inversion
   $b\mapsto-b$, not a termwise mixture.

Decisive question: is global optimality imported from and credited to the
complete source-v3 SOS rather than inferred from annihilating an arbitrary
candidate expression?

## Route 5: precise randomness conclusion

1. Read the model-indexed definition `eq:gval-model` and distinguish scalar
   value, fixed full behavior, and fixed canonical strategy.
2. Check that one finite-dimensional nonuniform exact maximizer with trivial
   Eve embeds in $q,qa,qc$ and already gives the displayed lower bound on
   $G_{\mathrm{val}}^\mu$.
3. Read the Conjecture 2 paragraph literally: in the operator normalization,
   the disproved implication is
   $\langle\overline{\mathcal I}_d\rangle=M_d+1\Rightarrow G=1/d^2$ for
   $d\ge4$.
4. Verify behavior-level nonuniqueness by comparing a uniform target table
   with a nonuniform one; local output relabelings cannot connect them.
5. Check that $5-\log_2 3$ is an upper bound on value-only worst-case
   min-entropy, not the exact optimized value.
6. Read the endpoint corollary with “deficit at most $\varepsilon$” as its
   quantifier.

Decisive question: does any sentence confuse a fixed-full-behavior SDP with
optimization over the scalar maximizing face? It should not.

## Route 6: secondary low-setting benchmarks

These results are not dependencies of the cyclic conclusions.

1. For Theorem `thm:binary-benchmark`, expand the two-square SOS for
   $\mathcal W_2$, check $q=qa=qc=3\sqrt3$, and follow the on-state
   operator-valued Fourier argument to $\sigma_E^{ab}=\rho_E/4$. Keep its
   Wooltorton--Brown--Colbeck prior-art credit visible.
2. For Lemma `lem:private-mub`, verify the $1/d$ sandwich and $1/d^2$
   conditional-state normalization. Treat its hypotheses as sufficient only;
   it neither proves necessity nor constructs a Bell score enforcing them.
3. Keep the one-input theorem and higher-dimensional obstructions at their
   stated narrow scopes.

## Focused replay

```sh
(cd cyclic_bell_exact_values_and_randomness && python3 verification/verify_merged.py)
(cd cyclic_bell_exact_values_and_randomness && python3 verification/verify_rigidity.py)
(cd cyclic_bell_exact_values_and_randomness && python3 verification/verify_exact_benchmarks.py)
(cd cyclic_bell_exact_values_and_randomness && python3 verification/verify_private_mub_binary.py)
(cd cyclic_randomness_counterexample && python3 verify_exact.py)
(cd minimum_bell_randomness && python3 verify_second_family_d4_exact.py)
```

The finite programs catch normalization, phase, support-rank, and transcription
errors. They do not prove the all-dimensional, arbitrary-$q_c$, or arbitrary-
maximizer statements; those require the analytic routes above.
