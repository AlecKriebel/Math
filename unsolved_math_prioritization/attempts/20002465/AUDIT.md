# Editorial audit and dependency record

This is an AI-assisted, unrefereed mathematical draft. Acceptance means one independent internal AI mathematical reconstruction accepted the stated partial result with a correction and explicit standard imports. It is not human peer review or formal proof-assistant certification. This is a prose proof-and-audit edition, not a computational reproduction package. No novelty, priority, or worldwide-current-openness claim is made.

## What this document checks

PROOF.md preserves the full accepted authored mathematical reconstruction from one independent internal AI audit. This document records its logical checkpoints, exact scope and public-edition integrity. It is an editorial acceptance record of that same reconstruction, not a second independent audit or a new proof search. The original accepted proof is identified by SHA-256 9cd99c95efa8d5ce02d8f886111c4b1ac7d383da7afcbc0645b922dc61da86e2 (18,019 bytes).

## 1. Definitions and signs

The accepted setting is nonempty compact connected smooth M without boundary, with smooth Riemannian metric and vector field f. Compactness ensures completeness of the flow, finite derivative bounds on bounded time intervals, and minimizing geodesics. Connectedness is used for the single-constant conclusion in the viscosity criterion.

The action is nonnegative and has critical value zero. Its Legendre transform is H_f(x,p) = |p|²/2 + p(f(x)). The tangent zero-action graph is Graph(f); its Legendre image is the cotangent zero section. The original AIM wording's tangent-zero-section and minus-sign defects are identified, rather than inherited. Additive normalization is indispensable because constants solve either sign of the equation.

The quadratic-chain definition quantifies over every positive lower time bound and every positive squared-jump budget. It uses sum e_i², not maximum e_i or sum e_i. Changing a smooth metric on compact M preserves the resulting set because the distances are bi-Lipschitz equivalent.

## 2. Both action–chain directions

For a controlled curve of duration at most R, the pullback z(r) = phi^{-r}(gamma(r)) gives a uniform estimate with C_R = R K_R^4. The constant depends on the fixed block horizon, not the total duration of a long loop. The factor of two arising from L_f = |dot gamma-f|²/2 is retained.

For the Aubry-to-chain direction, arbitrarily long loops with arbitrarily small action are partitioned into equal blocks in [T,2T). Summing the fixed-horizon estimate controls the total squared jump cost. The construction uses near-minimizers of the action infimum and does not assume an action minimizer exists.

For the converse, a minimizing geodesic eta from y to z produces beta(s) = phi^s(eta(s)), with endpoint phi^1 z and action at most K_1² d(y,z)²/2. That endpoint is essential. A chain at phi^{-1}x yields a loop at x: each block follows the orbit for t_i-1 and then uses the unit-time bridge, for total duration t_i. Taking lower time bounds to infinity and budgets to zero proves the zero diagonal Peierls value. The proof does not hide a long-time derivative estimate.

The two implications establish A_f = R_2(f). The conventional tangent Aubry graph identification is then imported from standard weak-KAM graph and common-derivative facts, using the constant zero critical subsolution and its flow-calibrated graph.

## 3. Recurrence bounds and normalized uniqueness

The elementary cost comparisons give SCR(f) subset R_2(f) subset CR(f). The smooth circle example with a fixed semicircle has SCR equal to that semicircle while R_2 = CR equals the full circle. Subdividing the fixed arc reduces its squared-jump cost to pi²/N. The Lipschitz Lyapunov function supplies a positive lower bound on the total unsquared cost for each nonfixed starting point. This proves strictness of the strong-chain inclusion; it does not disprove CR subset R_2.

For uniqueness, A_f = M makes every critical viscosity solution differentiable everywhere with the same zero derivative as the constant solution. Connectedness yields constancy. Conversely, the pointed Peierls function h_f(x,.) is a critical solution for every x, not just Aubry points. If every critical solution is constant, a subsequential forward-orbit limit and the same shifted unit bridge show h_f(x,y) = 0 for some y. Constancy then gives h_f(x,x) = 0 for every x. This is exactly the constants-only criterion, or uniqueness of zero after a base-point normalization.

## 4. Rejected step and complete repair

The original blanket assertion that negation takes viscosity solutions to reversed-drift viscosity solutions is false. Negation swaps upper and lower touching tests without reversing the Hamiltonian inequality. The full smooth-circle counterexample in PROOF.md retains both downward-corner slope intervals, the lack of lower tests there, and the explicit bad lower test for -u at pi/2, where H_{-f}(pi/2,1) = -1/2.

The repair is independent of that false bijection. Reversing every absolutely continuous path preserves the corresponding action after changing f to -f. Hence the finite-time action kernels transpose, the Peierls kernels transpose, and the projected Aubry sets agree. Apply the already proved characterization and uniqueness result separately to -f. This establishes R_2(-f) = R_2(f) and equivalence of the constants-only criteria for both signs. It does not assert an identification of their full viscosity-solution spaces.

## 5. External dependencies and unresolved target

The argument imports three standard weak-KAM facts: finiteness and the pointed-Peierls critical-solution property; the bijective tangent-Aubry projection; and differentiability/common derivative of critical subsolutions on the Aubry set. PROOF.md identifies their locations in Fathi–Figalli–Rifford preprint v1. These facts and the cited dimension estimates are not reproved from first principles here.

FFR's low-dimensional and Mather-disconnectedness results are credited as established conditional results. Cheng–Wei's inspected introductory pages are contextual only. No unqualified higher-dimensional implication is inferred from them.

The remaining unrestricted target is CR(f) subset R_2(f). Ordinary chain recurrence controls each jump but gives no bound on the number N of jumps as their maximum delta tends to zero; the estimate N delta² therefore does not establish the missing implication. Repetition worsens the cost. This failure of an argument is not a counterexample.

## 6. Editorial and verification boundary

All mathematical sections 1–9 and all references of the original accepted proof are retained verbatim. The opening discloses the internal AI review status. Section 10's phrase implying human mathematical acceptance is replaced with “The mathematical argument is in Sections 3–8”; its finite-check description is adapted to this prose-only edition. The final distribution paragraph is updated. No theorem, hypothesis, witness, dependency or unresolved boundary is removed.

The original audit's public-named 10-file input subset, consisting of nine listed members and its manifest, was authenticated as closed; the larger audit parent directory was not claimed closed. The original handoff's 40 listed files were authenticated without claiming that their shared parent directory was a closed inventory. Those original inputs remain unchanged. Byte hashes prove identity, not mathematical truth.

The original audit ran 1,974 exact regression checks per optimization mode and 16 adverse controls per mode, for 48 adverse rejections across normal, -O and -OO. Its authored checker can be rerun privately after authenticating it; neither checker code nor raw outputs are distributed here. Public-edition verification checks exact editorial replay, file membership, an additions-only patch and native Git object identities. These checks are not a formal proof of a continuum theorem and create no additional independent mathematical review.
