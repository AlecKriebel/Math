# First candidate assessment: renewal/probability family

Frozen 2026-10-04T14:16:41.343679+00:00, after explicit root release of `TURN_1.md` only. No author code or inherited review read. First source-stage held files remain unchanged. Original author turn count **1/5** preserved.

Candidate input: `TURN_1.md`; SHA256 **996947d8d995699411499b3bbdb781f25ae9a729900fb33074104cbf9e411cab**.

| Candidate claim | Initial assessment and adversarial attack | Exact remaining verification |
|---|---|---|
| Equations (1)–(3): a normalized strictly positive finite, non-lattice, infinite-mean law | The uniform component supplies non-lattice status; infinite mean follows from individual weighted atoms diverging, despite summable masses. Test mass indexing from n=1, uniform support below first atom, and finiteness of each possible value. | Independently prove the infinite series estimate and support/non-lattice claims literally. |
| Equations (4)–(6): first-large interval and its preceding sum | My source-only mechanism applies with `H=[a_n,infinity)`. Direct expectation decomposition avoids Wald and dependence assumptions; test the event `K_n>j` carefully because it includes the current draw being small. | Derive the full infinite identity, conditional law, exact hit probabilities, and crossing index from original independent variables. |
| Equation (7): transfer to inspected renewal total life | The event uses `T_n<=t_n`, which correctly includes a renewal epoch because the crossing is strict. Test whether any earlier partial sum can exceed `t_n` when `T_n<=t_n`. | Formal containment proof, endpoint examples, and control when `T_n>t_n` or the hit jump is too short. |
| Equations (8)–(9): asymptotically deterministic total life | Both bounds appear valid with the stated powers. Need independently derive geometric tail comparisons, the coarse `M_n<=a_{n-1}`, and the vanishing exponent. | Check base n=2, exact recurrence indexing, series tail, and a quantitative symbolic vanishing bound; preserve any computational failure. |
| Section 4: exclusion of all deterministic positive scales | The concentration input is sufficient if correct. Tightness/point-mass lemma appears applicable to all positive eventual scales. This family's role is to certify the renewal input, with any hidden domain assumptions flagged. | Other family's universal proof remains independent; I will check local assumptions and scope rather than adopt its result. |
| Equations (12)–(14): suggested truncated mean | Exact split at `t_n` should hold since all lower support is below `t_n` and all tail support exceeds it. | Reconstruct exact identity, monotonicity/positivity/finiteness, coefficient/exponent bounds, and divergence in probability for each fixed real threshold. |

## Independent proof and meaningful-control plan

Write a fresh complete probability derivation based on the first-success variables, not a paraphrase of the submitted proof. Use independence/Tonelli directly, and separately derive the negative-geometric distribution and failed-draw conditional law to expose any hidden conditioning. Derive exact two-sided bounds on the tail `q_n`, exact rational values for finite symbolic controls, and prove all infinite limits analytically.

An independent checker will use alternative exponent indexing and exact rational arithmetic to test base cases, candidate displayed inequalities, tail controls, and finite first-success identities. It should include meaningful stress controls: failure of concentration bounds for equal tail masses, failure when the preceding-sum term is large, and an explicit too-short-success endpoint example demonstrating that the crossing hypothesis is essential. Such controls corroborate proof obligations without proving the infinite theorem. Candidate code and inherited reviews stay unread until their separate release.

## Preliminary scope and checkpoint

No mathematical rejection identified on first reading; this is **not acceptance**. Mathematical verification toward assigned probability mechanism **20%**; overall assigned workflow **30%**. Unresolved: independent complete derivation, computational controls and reproduction, submitted code/read scope after release, all-family/root acceptance, and source binary authentication. No historical-priority or publication claim; no Git mutations.
