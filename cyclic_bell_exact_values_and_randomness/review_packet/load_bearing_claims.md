# Load-bearing claims

Version 1.1's central conclusion survives only if each core item below
survives. Each proposed falsifier is concrete and bounded.

## Core cyclic claims

| Manuscript item | Load-bearing statement | Best attempted falsifier | Audited outcome |
|---|---|---|---|
| Source baseline and Table `tab:exact-values` | Perito et al. proved $\beta_q\le d\sqrt2$, supplied the $M_d=2\csc(\pi/(2d))$ strategy, conjectured equality, and reported matching NPA values through $d=6$. These are source contributions. | Compare the source theorem, conjecture, NPA levels, and truncated decimals against $M_d$; look for a reversed attribution or normalization mix. | PASS. The source's analytic $d\sqrt2$ bound is tight only at $d=2$; its reported numerics agree with the exact radicals for $d=2,\ldots,6$. |
| Lemma `lem:polar` | The polar positive-factor identity remains valid with kernels and in arbitrary commuting algebras. | Use a genuinely rank-deficient $C$; track the canonical partial isometry and show, by strong limits, that it belongs to Alice's generated von Neumann algebra and commutes with Bob. | PASS analytically; no inverse, tensor factor, trace, or unitary extension appears. |
| Lemma `lem:scalar` | The scalar maximum is $2\csc(\pi/(2d))$, with equality exactly at $z^d=(-1)^{d-1}$. | Check both parity endpoints, $d=2,3$, and strict off-root phases; search for equality arcs or repeated roots. | PASS; the equality set has exactly $d$ roots. |
| Theorem `thm:exact` | The first reduced upper bound holds in the commuting-operator model and the source strategy makes $q=qa=qc=M_d$. | Search the upper bound for finite dimension, a tensor trace, normalized trace, order-$d$ use, or functional calculus outside Alice's von Neumann algebra. | PASS. The upper inequality uses only cross-party commutation; finite-dimensional attainment closes all three values. |
| Theorem `thm:support-rigidity` | Every attained finite-dimensional tensor-product exact maximizer of the **first augmented** family has all equality roots with equal multiplicity on $K=\operatorname{supp}\rho_A$, so $d\mid\dim K$. | Use nonfaithful $\rho_A$, a globally nonunitary polar factor, zero root multiplicity, or unequal multiplicities; test every support/invariance and reflection-rank step. | PASS at the stated scope. No claim is proved on $K^\perp$, for the unaugmented/second family, or for approximate/general commuting maximizers. |
| Theorem `thm:permutation` | Permuting **paired** equality-root and polar-phase labels preserves order, full spectrum, maximum score, local first moments, and the complex first-harmonic matrix under the displayed product hypotheses. | Break either product-one hypothesis or mismatch the row permutations; then test reversed and random admissible orders. | PASS as a sufficient theorem; hostile mismatches fail as expected. It is not a face classification. |
| Theorem `thm:biased` and `eq:target-table` | The final-two swap is an exact first-family maximizer with uniform marginals but a nonuniform target table for every $d\ge4$. | Reconstruct projectors instead of only correlators; recompute the target DFT, lag-two autocorrelation, and max-versus-$\ell^1$ estimate. | PASS. |
| Appendix `app:d4` and `eq:d4-entropy` | At $d=4$, the exact table alternates $1/32,3/32$, so $G=3/32$ and the displayed trivial-Eve min-entropy is $5-\log_2 3$. | Replay the cyclotomic projectors and an independent Fourier calculation; check that entropy is not mislabeled as the optimized worst case. | PASS. It supplies an upper bound on value-only worst-case min-entropy, not its exact value. |
| `eq:second-sos` and Theorem `thm:second` | The credited source-v3 SOS has prefactor $1/(2d)$; the permuted strategy obeys $\widehat B_\ell=d\lambda_\ell D_\ell$, $D_\ell^d=I$, and annihilates every factor. | Expand the full SOS, check the Fourier phase and Alice conjugation, and compare the main convention with the all-Bob-adjoint appendix convention. | PASS. The latter is consistently Bob outcome inversion $b\mapsto-b$, not a termwise hybrid. |
| Conjecture 2 paragraph and `eq:value-conditioned` | For $d\ge4$, the displayed strategy disproves precisely $\langle\overline{\mathcal I}_d\rangle=M_d+1\Rightarrow G(AB\mid1,d,E)=1/d^2$. | Ask whether the witness has the exact same normalized scalar maximum, whether trivial Eve suffices, and whether the text accidentally extends the conclusion to the fixed canonical full behavior. | PASS. The paper neither attacks the complete-behavior SDP nor computes the exact worst-case guessing probability. |
| Corollary `cor:behavior-nonunique` | The maximum fails to determine one behavior even modulo local output relabelings. | Try to map the canonical uniform target table to the swapped nonuniform table by output permutations. | PASS; relabelings preserve the multiset of table entries. No broader classification under all strategy-level equivalences is claimed. |
| Endpoint-robustness corollary | A value-only bound cannot approach $1/d^2$ when quantified over strategies with deficit **at most** $\varepsilon$. | Read $\varepsilon$ as exact deficit and look for a quantifier gap. | PASS only under the explicit tolerance convention in the statement. |

## Secondary, non-load-bearing benchmarks

These are mathematically substantive but not dependencies of the cyclic
counterexample.

| Manuscript item | Exact scope | Audited outcome |
|---|---|---|
| Proposition `prop:one-input` | One input on either wing cannot force private global randomness against all compatible realizations, even from a fixed complete behavior. | PASS by an explicit local model and finite pure projective Eve-flag realization. |
| Theorem `thm:binary-benchmark` | The prior-art binary score has $q=qa=qc=3\sqrt3$; every attaining finite-dimensional tensor-product strategy gives $\sigma_E^{ab}=\rho_E/4$ at $(0,0)$. | PASS by a two-square commuting SOS and on-state operator-valued Fourier proof. The privacy part is not extended to arbitrary commuting maximizers. |
| Lemma `lem:private-mub` | A private reference PVM, perfect Bob matching, and supported MUB sandwich are sufficient for $\sigma_E^{a,\pi(b)}=\rho_E/d^2$. | PASS with the $1/d$ and $1/d^2$ normalizations. It is neither necessary nor a low-setting existence theorem. |
| Higher-dimensional setting observations | The stated ideal tables are nonuniform, and one separately bounded computational-MUB exposure route fails. | PASS only at those stated scopes; no general $2\times2$ or $2\times3$ no-go is claimed. |

## Claims deliberately excluded

- No complete maximizing-face classification is claimed.
- Equal supported multiplicities do not imply a Weyl representation,
  uniqueness, or self-testing.
- The final-two swap is not claimed to maximize Eve's guessing probability.
- The permutation family does not resolve the first-family $d=2,3$ faces.
- The second-family SOS, $d\sqrt2$ bound, canonical strategies, and source
  NPA evidence are credited prior contributions.
- Numerical tests do not prove all-dimensional or $q_c$ statements.
