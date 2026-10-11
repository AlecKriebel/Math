# Independent AI-assisted challenge audit: finite-force equilibrium and exponent extension

Review date: 11 October 2026 UTC. Problem: AMR-099-0003, dataset ID 10000003.

## Separate verdicts

1. **PASS: the prior theorem.** The proof of Theorem 1.2 in Alper Ferudun's [arXiv:2610.06944v1](https://arxiv.org/abs/2610.06944v1), for `1 < s <= 2`, is mathematically sound under its stated finite-one-sided-force, nontrivial-set hypotheses. The source-proof reconstruction examined in this review correctly handles its essential analytic and probabilistic steps. This is a proof audit, not journal peer review, a formal proof-assistant certification, or a new claim to the inverse-square solution.
2. **PASS: the corrected extension.** The standalone theorem in `CORRECTED_EXPONENT_EXTENSION.md` is accepted for `1 < s <= (3+sqrt(5))/2`. The extra range `2 < s <= (3+sqrt(5))/2` follows from the original mechanism and the stated little-o counting/power-concavity argument, including the upper endpoint.
3. **Scope correction to the original extension prose.** It must explicitly require at least two distinct particles, or state a bi-infinite strictly increasing enumeration. A singleton satisfies finite force and zero net force but is not a positive-spacing bi-infinite arithmetic progression. The earlier proof already uses a bi-infinite increasing enumeration, so this is a standalone-statement correction rather than a substantive failure of the nontrivial-configuration proof. Acceptance here is attached to the separately pinned corrected statement, not an unrestricted reading of the old prose.
4. **No novelty certification.** The prior inverse-square result and the original network/cutoff construction are credited to Ferudun. The exponent extension is a separate deduction; no claim that it is first in the literature has been verified.

## Source identification and review scope

The key primary source PDF is 463,339 bytes, SHA-256 `257be3a3a46dd0fe82b941950ade540f3ade30c0945a1c167cae01d13c390bd9`. Its complete retained TeX was read, including the theorem, Sections 2-4, and Remark 5.3. Fresh local renders of PDF pages 6-8 were visually inspected against the critical energy formulae and range discussion. The previously retained PDF/text files were inspected locally; this review does not claim a second independent download of the PDF bytes.

The live [arXiv HTML](https://arxiv.org/html/2610.06944v1) and [author's public record](https://eulersolve.org/papers/amr-099-0003/) were also read during the review. The arXiv abstract page was intermittently retrievable; the retained landing-page metadata records v1 submitted 3 October 2026, 09:46:28 UTC. The public author record describes the manuscript as an unrefereed, AI-assisted preprint. That disclosure neither establishes nor invalidates the mathematics.

This packet contains authored mathematical exposition and public verification metadata. Third-party source documents and diagnostic programs are not reproduced.

## 1. Source and problem conventions

The [Benjamini note](https://arquivo.pt/wayback/20201231041612id_/https://www.wisdom.weizmann.ac.il/~itai/equilibrium.pdf), Question 0.1, and the [Warwick problem list](https://warwick.ac.uk/fac/sci/maths/research/events/2014-15/nonsymposium/random/Openprobs.pdf), section 4, Question 5, ask for arithmetic-progression rigidity. Their short wording does not specify the series convention or explicitly require increasing labels.

The [Georgakopoulos-Kolountzakis arXiv v1](https://arxiv.org/abs/1604.01649v1), PDF page 2, explicitly requires each one-sided force to be finite. Its Theorem 1 proves rigidity when an extremal gap is attained. Definition 3.1 and Theorem 4 impose both positive lower and finite upper gap bounds for their continuation theorem. The introductory shorthand about bounded distances must not replace that precise hypothesis. This review checked those relevant portions, not every result in the older paper, and does not claim inspection of its publisher PDF.

The corrected theorem is a set statement for at least two distinct points with absolutely convergent signed forces. Finiteness gives local finiteness and countability. A largest or smallest point would feel forces of one strict sign, so equilibrium forces a bi-infinite increasing enumeration. Arbitrary relabeling does not preserve affine dependence on the labels. None of these results addresses cancellation of separately infinite one-sided forces under a principal-value convention.

## 2. Common network mechanism: every fixed s > 1

Each of the following steps was challenged separately and found valid:

- **Adjacent ratios:** all force comparisons are between positive finite sums. The inequality `1 <= 2(v/u)^(-s)+(1+v/u)^(-s)` and reflection provide both ratio directions. The unique root `r_s>1` exists for every fixed positive `s`, hence throughout the needed range.
- **Shifted force subtraction:** both shifted series converge absolutely. For `j<n`, the force sign and the distance-difference sign reverse together. Thus every summand is `c(n,j)(g_j-g_n)` with the claimed positive symmetric divided difference, including its continuous diagonal-in-distance definition when `D=D'`.
- **Finite conductance rows:** the comparison `min(D,D')>=D/(1+r_s)` uses an adjacent-pair case and a nonadjacent-pair case; symmetry genuinely allows `j>n`. A pointwise minimum gap at the fixed row, not a uniform global lower gap, bounds the row by `K_s delta_n^(-1)` times that row's finite force.
- **Harmonic transform:** adding the finite row sum to the absolutely convergent difference identity gives `sum_j c(n,j)g_j=pi(n)g_n`. Consequently `pi^*(n)=pi(n)g_n^2<infinity`, and the calculation of `P^*(1/g)=1/g` supplies rowwise absolute integrability because all terms are positive.
- **No circular recurrence claim:** transformed row finiteness follows before recurrence. The energy estimate proves recurrence rather than inferring it merely from one-dimensional indexing. The equality of return probabilities under the harmonic transform is valid but is not needed to repair any missing step.

Sections 1-3 of the corrected note give a complete proof of these facts without restricting `s` to be at most two.

## 3. Infinite-degree recurrence is justified

Finite row mass suffices for the displayed finite-support Green identity: its absolute double sum is bounded by a finite sum of integrable rows. The finite-support hitting-probability function minimizes energy with origin value one and zero boundary values. Its energy is the origin row mass times the probability of leaving the finite set before returning.

The event of avoiding the origin forever while staying in the remaining finite set has probability zero. This follows from finitely many positive-probability simple exit paths and a uniform positive lower bound on their probabilities, followed by the Markov property. It does not require bounded degree or uniform control over the entire infinite state space. Therefore arbitrarily small finitely supported energies imply recurrence. Positive harmonic functions are constant by nonnegative-martingale convergence and recurrent visits, without a boundedness hypothesis. These arguments apply directly to `c^*`.

No explosive continuous-time process is being used: the argument concerns a discrete-time stochastic kernel with finite row normalization.

## 4. Original energy proof: prior theorem accepted

Every nonzero cutoff-difference pair has an endpoint in the support interval. A near pair then has both endpoints in the larger interval and an initial gap at most `R`. The integration intervals are ordered and have disjoint interiors; their last endpoint extends only to `(1+r_s)R` relative to the left particle. The integral comparison on the left tail needs the extra factor `r_s`, and the source includes it.

For `1<s<2`, the near energy is bounded by `7(1+r_s)R^(1-s)/(2-s)` before multiplying by `K_s`.

For `s=2`, the logarithmic sum is controlled by concavity. The further substitution of `7R` for the total gap length is not assumed unconditionally: splitting at the maximum point of `z log(Lambda/z)` gives the stated `max(1,log(...))` expression. The finite-force quadratic point count then yields `O(log(R)/R)`, even when gaps tend to zero.

Both infinite far tails are dominated by convergent integrals of `t^(-s-1)`. The total gap weight at supported endpoints includes the outgoing right boundary gap; that gap is controlled by the preceding supported gap because there are at least two supported points. The complete far bound is `4(1+r_s)^(s+3) R^(1-s)/s`. Charging a pair twice is harmless for an upper bound, and the unordered-pair energy convention has no missing factor of two.

Combining these bounds with recurrence proves exactly the source theorem. No substantive gap or additional density/discreteness assumption was found.

## 5. Extension: endpoint and all inherited premises accepted

The source's Remark 5.3 explicitly observes that the ordering, ratio, harmonicity, comparison, and far-tail bounds survive for all `s>1`, but stops short of claiming a theorem there. Direct inspection confirms that the near bound before evaluating its integral also survives.

For `2<s<3`, evaluation at the positive lower limit gives

`S_near <= (1+r_s)^(s-1)/(s-2) * R^(-2) * sum_{I_R} g_n^(3-s)`.

The exponent `3-s` lies in `(0,1)`, so concavity, together with disjoint gap lengths summing to at most `7R`, gives

`sum_{I_R} g_n^(3-s) <= N_R^(s-2) (7R)^(3-s)`.

An empty index set contributes zero; no division by its cardinality is made. This step neither reverses Jensen's inequality nor assumes a lower gap bound.

A convergent positive force series gives `A(L)=o(L^s)`: separate a fixed finite inner region from the arbitrarily small force tail, then take the two limits in that order. Since `N_R<=A(3R)`, set `epsilon_R=N_R/R^s -> 0`. The near bound becomes

`S_near <= C_s epsilon_R^(s-2) R^(s^2-3s+1)`.

The exponent is strictly negative for `2<s<s_*`. At `s_*=(3+sqrt(5))/2`, it is exactly zero; `s_*-2>0` still makes the little-o factor tend to zero. The endpoint remains strictly below three, so every use of concavity stays valid. The far bound tends to zero as before. Recurrence and harmonic rigidity complete the theorem for the corrected statement.

Above `s_*`, this estimate alone no longer proves decay, because `epsilon_R->0` has no specified rate. That is an obstruction to this upper-bound argument, not a counterexample to the theorem for a larger exponent.

## 6. Diagnostics and limits

The independent diagnostic program imports no code from the original audit or the source paper. It checks exact shifted-force identities for integer exponents 2, 3, and 4; exact distance/conductance inequalities; high-precision one-sided integral and cutoff inequalities across the old and extended ranges; the exact algebraic endpoint; and an exactly summed infinite-degree Green-identity control with every tail edge accounted for. It also checks the singleton scope issue and the failure of power concavity past exponent three. These supplemental checks are not a formal certification.

Finite profiles in that program are not claimed to be equilibrium configurations. Their successful tests are supplemental diagnostics; the universal mathematical and infinite-tail claims are established by the proofs in this report and the corrected note.

A limited public search did not supply a priority certification. Neither the current audit nor the corrected note claims that the exponent extension has never appeared elsewhere, that the prior preprint has passed journal peer review, or that principal-value or all-force-law problems are settled.

The acceptance report binds separate verdicts for the prior theorem and the corrected extension to the identified source and the exact public proof and audit hashes. The editorial map records the changes for this public edition.
