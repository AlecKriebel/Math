# Attempt log: AMR-039-0010

Date: 2026-10-04 UTC. Five substantive mathematical approaches are recorded below. This count describes distinct approaches, not five independent discoveries or five independently reviewed model responses. No full solution is claimed.

## Initial gate, approximately 06:10--06:19 UTC

Recovered the exact target record after the catalogue page failed; downloaded and checked the original Problem J. Checked actual PR, branch, commit, content, and problem-tree evidence separately from the queued label. Identified the established uniform-local-T1 theorem and read the full relevant proofs in the primary sources listed in SOURCE_GATE.md.

Initial conclusion: the known graph/local-T1 theorem cannot simply be relabeled a solution of every non-Gaussian or pointwise-cost variant.

## Approach 1: uniform-local-T1 semigroup argument

- Mechanism: exponentiate bounded Lipschitz functions, contract their Lipschitz constants, sum a geometric series, and use the entropy variational formula.
- Result: complete proof of `W1^2 <= B H/[kappa(2-kappa)]` under uniform transition T1; the neighbor-walk constant follows from bounded support.
- Status: established prior result, reconstructed with matching constants.
- Exact limitation: uniform one-step T1 excludes the non-Gaussian generality that motivates the source's proposed modifications.

## Approach 2: variable local variance and restricted Laplace transform

- Mechanism: retain actual local Lipschitz variance in Ollivier's nonlinear iteration, control the Lipschitz constant of each iterate, and optimize only over the allowed Laplace window.
- Result: complete proof of `alpha_{A,L}(W1)<=H`, where `A=pi v/[kappa(1-kappa/4)]` and `L=min(1/(3S),1/(2C))`; `alpha` is explicitly quadratic then linear.
- Status: proved conditional formulation, derived from established methods, with no novelty claim.
- Exact limitation: this is a nonlinear function of W1, not the optimal integral cost with alpha inside.

## Approach 3: atomic perturbation of a curvature-one chain

- Mechanism: change the two atom weights by epsilon; transported mass is first order in epsilon while entropy is second order.
- Result: complete counterexample to every correction-free bound `T_c<=K H` with `c(1)>0`, even on the reversible uniform two-point reset chain. For the profile from approach 2, the exact rational violation margin is at least `29/1728` at epsilon `1/16`.
- Status: exact negative result for that strengthened variant only.
- Exact limitation: it does not refute the original source, which explicitly allows additive or other changes.

## Approach 4: defects and a genuine nonlinear transport cost

- Mechanism: optimize the two-point entropy defect exactly; for general spaces, combine exponential integrability, entropy duality, and a product coupling.
- Results: exact minimum two-point defect `K log cosh(c(1)/(2K))`; complete general bound `T_alpha <= H+2 eta pi d(o,.)+A eta^2`, and replacement of the radius by `J(o)/kappa`.
- Status: proved, but deliberately weak.
- Exact limitation: the product-coupling bound discards the quadratic concentration benefit, and its additive term is not shown to be sharp or dimension-free. It is one coarse formulation, not a universal completion of the source's program.

## Approach 5: tail and scaling stress tests

- Mechanism: test independent reset kernels, an explicit Poisson-thinning kernel, and exact lazifications of a three-state reversible chain.
- Results: positive curvature plus bounded local variance alone permits polynomial tails; positive curvature also coexists with failure of every Gaussian T1 bound for a Poisson invariant measure. Conversely, the variance-sensitive constants in the finite-chain example stay finite as the time step decreases, while a diameter-only T1 bound diverges.
- Status: complete proofs for these tests; modest exact arithmetic verifies finite calculations.
- Exact limitation: these checks do not remove the general local hypotheses or prove a full continuous-time limit theorem.

## Checkpoint, approximately 06:29 UTC

The five-route research deliverable is complete, subject to independent audit. Best-guess completion toward that bounded deliverable: 100%. Best-guess progress toward the entire exploratory problem: 20%, a subjective planning estimate rather than a probability or a claim of partial proof of a fixed conjecture. The stronger generally useful nonlinear-cost formulation remains unestablished here.

Verification: original standard-library Python checks passed; exact rational certificates are separated from 70-digit Decimal regressions. No large exhaustive search was used. Full generality and infinite-state assertions rest on the manuscript proofs, not finite tests.

Disposition: unresolved/partial progress after five approaches. Suggested queue accounting is `unsolved`, `5/5`, rather than any exhausted label, solved status, or novelty claim. No remote repository write, merge, release, or external outreach was made in preparing this frozen candidate.
