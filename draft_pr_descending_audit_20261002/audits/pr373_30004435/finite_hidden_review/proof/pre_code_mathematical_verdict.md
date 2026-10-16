# Mathematical verdict sealed before candidate-code inspection

Read after the source-first baseline and original controls were sealed: candidate TURN_1.md, TURN_2.md, and RESULT.md only. No candidate code, assertion receipts, old review, root/sibling proof, or comparison result was used. Candidate frozen head: 4e635c77d7399d671ea58700e41bbd92cbdeeb46. This verdict concerns the finite Markov / finite HMM route only.

## Verdict

The universal finite Markov and finite HMM mathematical claims in Turns 1-2 are correct under their stated stationary finite-model assumptions. The candidate expressly leaves the full Steif method target unresolved and does not mistake the scoped theorem for the universal target. The proofs do not import the general entropy theorem. No mathematical blocker was found in these two routes. Finite-model correctness gives no positive completion estimate for the unrestricted probability-only target.

## Additional bilateral reconstruction

The independent baseline established one-sided tails. The candidate also claims the bilateral tail, which requires an additional check rather than following merely from equality of the one-sided tails. Independently derive the central-block conditional law from the stationary path density. For a central hidden path y_a,...,y_b, and endpoint states i at -m and j at m, factor the joint probability of the endpoints and central path as

 pi(i) P^(m+a)(i,y_a) [product_(t=a)^(b-1) P(y_t,y_(t+1))] P^(m-b)(y_b,j).

The endpoint marginal is pi(i)P^(2m)(i,j). Cancelling gives the bridge quotient. Conditional on endpoint states, adding any finite earlier or later outside observations contributes factors that cancel identically. Taking the increasing outside-window martingale limit gives the same bridge for the full outside field. For m on a cofinal common-period multiple and fixed class/phase l, the left matrix factor tends to d_C pi_C(y_a) on the appropriate phase, the right one to d_C pi_C(j), and the denominator to d_C pi_C(j)>0. The quotient therefore tends to the class/phase-conditioned central-path probability. Finitely many supported endpoints make this uniform; incompatible central paths have probability zero. Reverse martingale convergence plus cylinder density yields the bilateral tail upper bound sigma(L). Every endpoint recovers L, so equality follows. This derivation checks the stronger bilateral theorem directly without assuming a generally invalid one-sided-to-bilateral implication.

For observations the bilateral tail is a subset of the joint hidden/output bilateral tail. Hence it is a function of L. Equal conditional full observation laws force that function to be constant on the observable quotient, while the frequency reconstruction in the baseline places the quotient in each one-sided tail. Thus all three observed tails equal that quotient for this finite model class. The conclusion does not extend to arbitrary stationary finite-alphabet processes without additional work.

## Adversarial boundaries checked against candidate proofs

- Transient/zero-mass states: zero stationary mass makes removal legitimate; no reverse kernel divides by zero after support restriction. Zero-mass recurrent classes are also excluded, not accidentally treated as latent positive-mass atoms.
- Periodicity: the class/phase label is retained; the conditioned law is stationary under the common D-step shift and need not be one-step stationary. Candidate handles this correctly.
- Nonergodic mixtures and nonreversibility: finitely many classes yield finitely many positive lower bounds; reverse-time mixing or bridge factorization requires no detailed balance.
- Bilateral tails: independently rederived above. General bilaterally deterministic examples show why this required a separate finite Markov proof.
- Emission degeneracy: constant or identical emissions can erase all class/phase information; zero symbols merely create null joint states. Candidate quotient is law-based, not label-based or one-letter-based.
- Observable-law quotient: equality of forward prefix-word laws extends to every full observed cylinder because each conditioned label law has the same shift-D invariance. One-letter equality alone fails in the independently constructed period-2 four-state model.
- Dimension bound: V_0 has dimension one, strict growth stops by s-1, and the first stable space is invariant under every M_a. Thus no off-by-one or unsupported finite-word extrapolation occurs. For stochastic emissions candidate uses a safe larger count of supported joint states, which is valid; the independent hidden-state calculation permits a sharper bound but candidate does not need it.
- Completion: the decreasing-field representative liminf construction and finite-label positive weights make null-set transfers valid. Cylinder density applies to the canonical process space, as candidate assumes explicitly.
- Excluded cases: nonstationary initial hidden laws, infinitely many hidden states, infinite coordinate alphabet, and arbitrary infinite-memory observed laws are outside this theorem. No finite scan proves their tail claims.

## Exact remaining gap and publication interpretation

Both approaches depend on finite class/phase structure and geometric forgetting within a skeleton. Neither feature holds for arbitrary stationary finite-alphabet processes. Finite-model approximation does not provide tail continuity, and a hypothetical finite-label reduction would replace the core problem with an unsupported statement. The finite Markov classification is already identified in the primary thesis; no novelty determination is made for the HMM reconstruction or certificate. This is independently checkable scoped mathematical validation, not independent human peer review or a solution to the original target.
