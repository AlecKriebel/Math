# Research log and attempt accounting

Target 30004609 / OWR-4990374-015. All timestamps UTC on 2026-10-04. Completion percentages are provisional research estimates toward a reviewed full resolution, not probabilities of correctness.

- 15:41: Began catalogue-first source check. Catalogue retrieval unavailable; verified the pinned corpus hash and matched the numeric record to the exact Oberwolfach source. Checked the live own row, state, existing attempt, branches and PR duplicates. Completion estimate: 5%.
- 15:43: Found the January 2022 withdrawal notice. Reclassified older claims about rank 4/5 and inductively-free arrangements as affected historical claims. Retrieved v3 explicitly and inspected the failed inference. Completion estimate: 5%.
- 15:44, substantive approach 1: Explored deletion/product induction and the direct rank-two counting route. The earlier inference that irreducibility forces one deleted product factor to have a single hyperplane is false. The withdrawal arrangement gives factor sizes 4 and 3. Counting u+3v=r+1 alone does not supply a modular coatom, so that route has a precise missing structural step. A counterexample to an inference does not refute the conjecture. Completion estimate: 15%.
- 15:45, substantive approach 2: Added the dimension of the full relation space, using formality: r<=u+2v=r+1-v. This forces v<=1. Identified the incidence tree cases and the remaining cycle-rank-3 case. A minimal dependency among triple relations is forced to have four triples and six points, giving a K4 core. Completion estimate: 65%.
- 15:49: Saved the complete all-ranks candidate, including connectedness, products, essentialization, the rank-two bound, the K4 support argument, and a direct modular-extension proof for terminal pencils. A complete candidate was obtained within the second substantive approach, so the five-approach maximum was not exhausted. No additional independent proof-search attempts are claimed. Completion estimate: 85%; independent mathematical review still needed.
- 15:55: Exact diagnostics passed: 11 fixtures through rank 6, full-flat modular-chain searches, an explicit Saito certificate and degree-one calculation for the withdrawal example, 1,716 rational rank-three subsets, and 4,845 four-triple supports. The non-Fano arrangement with two cubic exponents correctly fails supersolvability. The tests are finite diagnostics, not a substitute for the proof. Completion estimate: 90%; independent audit and novelty assessment remain external to the author's claim.

## Exact remaining verification tasks

- Independently challenge every implication of PROOF.md, especially connectedness from formality, the dimension inequality, the minimal-dependent-support argument, and global modularity after pruning.
- Reproduce check.py and compare RESULTS.json.
- Confirm source scope and the withdrawal status; do not restore the withdrawn partial results as premises.
- Perform an independent novelty check before promoting the result beyond a candidate.

No queue-management script was run. No main-branch change, remote publication, merge, release, DOI, or external outreach was performed in preparing this packet. Repository workflow instructions were read; the bounded draft-only campaign governs this attempt's publication and status handling.
