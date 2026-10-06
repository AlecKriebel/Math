# Final report: source-model adversarial fidelity and physical-resource audit

## Verdict

**PASS. No essential repair was identified.** The pinned complete candidate supplies a valid construction in the historical source model: independent sender messages encoded by local product unitaries; two charged qubit transmissions per resource copy to separate receivers; post-transmission local processing plus classical receiver communication; and asymptotic vanishing average decoding error.

The exact verified claim is
`C_LOCC(W4) >= 3/2 + h2(1/4)`, with an interior independent rate pair `(9/8,9/8)`. This resolves the source's strict comparison with 2 bits per W copy. It neither determines optimal capacity nor proves a one-copy or maximal-error claim.

The first independent reports are [FIRST_SOURCE_ONLY.md](FIRST_SOURCE_ONLY.md) and [FIRST_CANDIDATE_VERDICT.md](FIRST_CANDIDATE_VERDICT.md). Their freeze records keep the pre-candidate conclusions separate from this completed review. No author-review, sibling scientific conclusion, priority clearance, or ROOT scientific conclusion was inspected.

## Falsification attempts and evidence

| Potential failure | Independent check | Finding |
| --- | --- | --- |
| Replacement by a common-message code | Compare explicit sender maps with product priors in PRL 210501-3 and expansion p. 7 | Each sender uses only her own message; Winter's separate codebooks match |
| Quantum receiver communication hidden in a cq decoder | Trace physical ownership of every output register and condition a pinched POVM on J^n | All decoder quantum operations occur at B2; B1 transmits only classical outcomes |
| Bell measurement spans distant parties | Check chronology and post-transmission laboratory cut | Bell measurement acts on A1B1, both already at B1 |
| Filtering or successful branch counted as deterministic | Rebuild every conditional block without normalization | All 64 branches included, each of 16 complete output states has exact trace 1 |
| Asymptotic bound mistaken for achievability | Read primary Winter definition and Theorem 9 | The direct theorem establishes vanishing average-error codes for the computed MAC region |
| Additional qubits or free sender feedback | Count n local Pauli codeword uses and n prescribed transmissions by each sender | Exactly 2n transmitted qubits for n W copies, no encoder feedback or sender–receiver classical channel |
| Entropy calculation or marginal inconsistency | Independent exact Fraction amplitude contraction and sixteen spectral power sums | All asserted channel spectra and relevant W marginals pass |
| Equality at classical threshold | Exact interior witness 27 < 32 | Total rate 9/4 is strictly below the achievable sum bound and strictly above 2 |

The replay is [independent_channel_replay.py](independent_channel_replay.py), with [independent_channel_results.json](independent_channel_results.json). It imports no candidate checker and reads no candidate numerical report. Its successful process receipt, complete stdout, and empty stderr are under `process_evidence/independent_channel_exact_replay/`.

## Decoder locality argument

For every block output, the state has the form
`omega = sum_j |j><j|_J ⊗ sigma_j_R`.
For decoder elements `M_mu >= 0` satisfying `sum_mu M_mu = I`, define
`M'_mu = sum_j P_j M_mu P_j`, `P_j = |j><j|_J ⊗ I_R`.
Then `M'_mu >= 0`, `sum_mu M'_mu = I`, and
`Tr(omega M'_mu) = Tr(omega M_mu)`.
Write `M'_mu = sum_j |j><j| ⊗ N_(mu|j)`; for each j, the N operators form a POVM on R. Reading J and measuring R accordingly at B2 realizes the complete decoder. This remains true when j is the whole n-copy outcome string and R is R^n. No coherent transport of B1's residual systems is needed.

## Rate and source boundary

The effective cq output spectra are:
- each input: `(1/2,1/4,1/4)`;
- average over input 2 holding input 1 fixed: `(1/4)x2, (1/16)x8`;
- average over input 1 holding input 2 fixed: `(1/8)x8`;
- full average: `(3/32)x8, (1/32)x8`.

Thus the two conditional constraints are 3/2 each and the sum constraint is `3/2+h2(1/4)`. [Winter's primary source](https://arxiv.org/pdf/quant-ph/9807019v3), Sec. II p. 2 and Theorem 9 pp. 4–5, uses uniform independent message sets, separate deterministic encoder maps, and average error. Finite alphabets, finite output dimension, and the memoryless tensor product needed by that theorem are all present.

The original source formal gaps retained in FIRST_SOURCE_ONLY remain qualifications about historical precision, not a hidden failure of this construction. The candidate explicitly chooses ordinary asymptotic average error. Its codewords are products across copies, so it does not rely on the source's less explicit treatment of entangled block encoders.

## Repairs, limits, and custody

Essential repairs: **none**. Optional wording: make “average decoding error” explicit in candidate Sec. 1's generic block-code sentence; the candidate already states it elsewhere.

No novelty, prior-art completeness, publication-readiness, optimal-capacity, numerical finite-block simulation, or experimental claim is assessed. The linked priority materials and prior-protocol paper in the candidate were not opened. No fresh central-proof search was performed; the candidate's proposed finite channel was verified and its established theorem dependency checked.

All scientific files were written only inside this exclusive audit folder. No Git/index/main/status command, PR mutation, publication action, external message, upload, or outreach was performed. ENOSPC was handled by removing only four disposable rendered PNG intermediates after visual inspection; the exact cleanup record and required original PDF bytes remain preserved. One unavailable rg executable and the initial ENOSPC directory creation failed before their scientific commands launched; those infrastructure limitations are explicitly recorded, not represented as passed checks.

Assigned audit completeness: **100%**. [VERDICT.json](VERDICT.json), [CANDIDATE_AND_THEOREM_PINS.json](CANDIDATE_AND_THEOREM_PINS.json), and [EVIDENCE_MANIFEST.json](EVIDENCE_MANIFEST.json) provide the machine-readable outcome and byte custody.

