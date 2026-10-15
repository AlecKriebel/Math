# FIRST_CANDIDATE_VERDICT

Independent verdict on the exact original candidate, fixed before reading ROOT, sibling, author-review, or priority conclusions.

**Verdict: PASS for source-model fidelity, physical resource accounting, decoder locality, and the stated asymptotic average-error coding bridge.** No essential repair or gap was found within this audit's scope. The candidate addresses the original W-state question under its historical unitary-encoding/asymptotic interpretation, rather than only an easier zero-error or common-message variant.

Candidate pin: 11679 bytes, SHA-256 `fb8646bbe3cd8512ec7736fc180fa08a76740ac8b0dbb60b539a0320328c6404`, supplied Git blob `7adfc78adb9561d2fdaaa091559de190cf13f673`. The SHA-256 and size were independently checked; no Git command was used. The prior FIRST_SOURCE_ONLY report remains unchanged at SHA-256 `5334739a2e5d9e440da8e1308625f4920b18354b8818f9b7630c0dda83071e86`.

The verified lower bound is `C_LOCC(W4) >= 3/2 + h2(1/4) > 2`, as a supremum of asymptotically achievable sum rates. In particular `(R1,R2)=(9/8,9/8)` is an admissible independent-message rate pair with vanishing average error, using one W copy and two charged transmitted qubits per channel use.

## Checks that matter

- **Independent senders:** the encoders are separate predetermined maps `m1 -> x^n(m1)`, `m2 -> y^n(m2)`, implemented by products of local Pauli unitaries. Sender 1 never needs message 2, measurement outcomes, shared message randomness, or feedback. Codebooks can be publicly agreed and fixed. Their joint codeword prior factors across senders even though a codebook need not have an iid distribution across positions.

- **Resources and timing:** one qubit per sender per W copy goes to the prescribed different receiver. The Bell measurement is performed by B1 only after she owns A1B1. There is no sender–receiver classical channel or state-conversion stage, no extra shared entanglement, no added quantum receiver channel, and no hidden qubit cost. B1's outcome string is receiver-to-receiver classical communication of an allowed decoder, not sender communication. Receiver classical communication is available without a stated bit budget in the historical LOCC task.

- **All branches counted:** direct amplitude contraction independently verified all 16 input pairs and 64 conditional blocks, every output trace exactly 1, and the full outcome spectra. Zero-probability branches are retained as zeros; positive branch probabilities are already carried by the unnormalized vectors. No successful branch is renormalized into a rate gain.

- **Exact channel algebra:** a separate standard-library Fraction implementation, built from the original four-qubit computational basis rather than the candidate checker, verifies the candidate's four relevant cq spectra and one-/two-qubit marginals. First sixteen exact spectral power sums fix each 16-dimensional characteristic polynomial. The entropies are `3/2, 3, 3, 3+h2(1/4)`, respectively. This yields conditional rate bounds `3/2,3/2` and sum bound `3/2+h2(1/4)`. The exact witness `27<32` proves the selected total `9/4` is strictly interior; no numerical tolerance is needed.

- **Theorem hypotheses:** [Winter, quant-ph/9807019v3](https://arxiv.org/pdf/quant-ph/9807019v3), Sec. II p. 2, defines separate encoder maps and average error over independent uniform message sets. Theorem 9, pp. 4–5, explicitly gives codes for all nonnegative tuples satisfying the conditional subset mutual-information inequalities for product input priors. The proof fixes independently drawn codebooks with low average error. The candidate's finite memoryless cq channel has precisely those hypotheses. The full-rate statement is not merely an application of an entropy upper bound.

- **Decoder is physically LOCC:** after B1's local measurement and classical transmission, every system on which the cq theorem's POVM acts is at B2. The classical outcome string J^n has a block-diagonal state. For any decoder element M, pinching it as `sum_j P_j M P_j` preserves positivity, completeness of the POVM, and every decoding probability. Its j-sector is a POVM on R^n, implementable locally by B2 conditioned on the received classical string. Optional transmission of the decoded message pair back to B1 is classical LOCC. The protocol therefore does not call an inaccessible global quantum decoder on B1:B2.

## Scope and residual qualifications

The original short sources leave block/error definitions less formal than the cited coding theorem; this ambiguity was identified before seeing the candidate. The candidate explicitly states the standard asymptotic **average-error** interpretation and supplies its coding theorem. It does not prove maximal-error, one-shot, zero-error, optimal-capacity, finite-block performance, or priority claims.

The no-communication source expression `2h2(1/4)<2` is consistent with the independently checked marginals, so the positive lower bound establishes the stated LOCC-DC shell membership. The “classical fallback” aside changes neither strict comparison nor the proof.

**Essential repairs required: none.** Editorial hardening, if desired: replace the generic phrase “asymptotic vanishing-error block code” in candidate Sec. 1 with “asymptotic vanishing average decoding error,” consistent with the explicit statement already in Sec. 1 and with Winter's definition. This is a precision edit, not a mathematical gap. No priority or current-literature clearance was undertaken; the candidate's attribution section was read only as part of its pinned full text, and its linked priority materials were not opened.

Review completeness: **100% for the assigned source-model/physical-resource audit**. Candidate truth beyond the checked construction, publication readiness, and novelty are outside this verdict.

