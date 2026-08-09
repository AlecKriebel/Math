# Load-bearing claims

The paper's main conclusion survives only if each item below survives.  Each question is intended to admit a concrete yes/no answer.

| Claim ID | Load-bearing statement | Best attempted falsifier | Audited outcome |
|---|---|---|---|
| CBR-003 | The polar positive-factor identity remains valid with kernels and in commuting algebras. | Use a genuinely rank-deficient \(C\); track the canonical partial isometry rather than silently replacing it by a unitary.  Check the cross term and support projection. | PASS analytically; no inverse or unitary extension appears. |
| CBR-004 | The scalar maximum is \(2\csc(\pi/(2d))\), with equality exactly at \(z^d=(-1)^{d-1}\). | Check parity endpoints, \(d=2,3\), and off-root phases; look for extra equality arcs or repeated roots. | PASS; exact equality set has \(d\) points. |
| CBR-005 | The first upper bound holds in the commuting-operator model. | Search for a tensor trace, dimension assumption, order-\(d\) relation, or Bob functional calculus inside the upper-bound proof. | PASS; only cross-party commutation is used. |
| CBR-009 | Permuting paired equality/polar labels preserves admissibility and first-harmonic score data. | Break either product-one condition and check order \(d\); then test reversed and random admissible permutations. | PASS under the displayed hypotheses; broken products fail as expected. |
| CBR-011/012 | The final-two swap is an exact maximizer with a nonuniform designated joint table for every \(d\geq4\). | Reconstruct spectral projectors rather than only correlators; recompute \(R_2\) and the Fourier normalization. | PASS; exact \(d=4\) probabilities alternate \(1/32,3/32\). |
| CBR-014 | The second-family residual is a complete positive SOS with the stated normalization. | Expand every \(P_\ell^\dagger P_\ell\); check the Fourier cross terms and \(1/(2d)\). | PASS. |
| CBR-015 | The permuted second-family strategy annihilates that SOS in every dimension. | Recompute \(\widehat B_\ell\), the coefficient phase, \(D_\ell^d\), and Alice's entrywise conjugation. | PASS analytically and in an independent exact \(d=4\) replay. |
| CBR-016/018 | Maximum scalar value alone does not certify maximal global randomness, without contradicting fixed-canonical-behavior certification. | Ask whether the witness attains the same scalar maximum, whether its target table is genuinely different, and whether a full-behavior constraint would exclude it. | PASS; the distinction is explicit. |
| CBR-017 | A value-only bound cannot converge to \(1/d^2\) at the endpoint when quantified by deficit tolerance. | Interpret \(\varepsilon\) as exact deficit and look for a quantifier gap. | PASS only with the manuscript's explicit “deficit at most \(\varepsilon\)” convention. |
| CBR-019 | One input on either wing precludes private global randomness even for a fixed full behavior. | Reconstruct the local model and ask whether the flagged realization is finite, pure, projective, and compatible. | PASS. |

## Claims deliberately not load-bearing

- No complete maximizing-face classification is claimed.
- The final-two swap is not claimed to maximize guessing probability.
- No result for \(d=2,3\) is inferred from failure of the explicit permutation family there.
- The computational-MUB proposition is not used to prove any cyclic theorem.
- Numerical tests do not prove the all-dimensional or \(q_c\) statements.
