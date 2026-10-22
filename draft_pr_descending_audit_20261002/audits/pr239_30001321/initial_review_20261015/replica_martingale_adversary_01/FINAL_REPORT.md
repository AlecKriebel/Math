# Replica, overlap, and martingale adversary: final lane report

UTC checkpoint: 2026-10-15 04:24:46 UTC. Assigned-lane completion estimate: **100%**. Whole-PR completion is not assessed by this lane.

**Lane verdict: no mathematical defect found in the earlier-turn inputs (B)–(G) of current PROOF.md.** The proof has been independently reconstructed from the original TURN_1 and TURN_2 documents. No inherited `independent_review` verdict was consulted, and no whole-PR clearance or priority claim is made.

The strongest verified results in this lane are the full restricted-scale theorem: for every fixed γ>1/4, fixed u>0 and K>0, the coarse quenched-vs-annealed L1 discrepancy has O(N^(−K)) environmental tail uniformly over all integer M≥N^γ and all deterministic alignments; and the all-diverging-scale expectation convergence (F). These apply to every fixed iid law on (0,1), including biased and merely elliptic laws.

## Mechanism, evidence, and exact status

| Input/family | Independently checked mechanism | Status and limits |
|---|---|---|
| Replica half-difference | Direct joint local coin probabilities yield a symmetric lazy nearest-neighbor chain with rate a away from zero and δ at zero; exact E I_s=g_s | Verified, with same-parity scaling explicit |
| Defect return bound | First-return transform plus reversible positive-spectrum monotonicity gives g_s≤C/√(s+1) | Verified; transform bounds alone were not substituted for a pointwise coefficient proof |
| Backward profile | Radial-difference recurrence has nonnegative coefficients, including the origin defect coefficient 1−2δ−a | Verified for all times and all starting gaps; backward and forward profiles distinguished |
| B and C | Fresh future layers and ordered-index conditional occupation moments | Verified, including repeated indices and deterministic s,L; no instantaneous high-moment theorem asserted |
| D | Exact layer increment, within-layer independence, semigroup Lipschitz preservation | Verified for bounded terminal tests and smoothed terminal laws |
| E | Explicit exponential-supermartingale proof on the joint event {deviation>u,Q≤w} | Verified with the stated constant 4; no conditioning on a future good event |
| F | Independent Fourier binomial-gradient argument, parity telescoping, sum of cell variances, window Cauchy–Schwarz and annealed tails | Verified uniformly in deterministic alignment and for arbitrarily slowly diverging M |
| G | Common dyadic overlap event, deterministic sign tests, entropy margin, tail truncation, periodic boundary majorant and last-segment coupling | Verified for fixed γ>1/4; does not itself cover arbitrary slow scales |

The detailed independent proof is `INDEPENDENT_RECONSTRUCTION.md`. It was saved before any inherited-verdict access; those verdicts remained unread through completion.

## Reproduction and independent controls

The two original checker sources were inspected before execution and run unchanged. Their complete scientific outputs reproduce the frozen receipts **byte-for-byte**, not merely the assertion totals:

- `check_turn1.py`: PASS, 486 exact assertions, empty stderr.
- `check_turn2.py`: PASS, 50,324 exact assertions, empty stderr.

`replay_comparison.json` preserves both full original and replay JSON objects, equality results, and the actual read-only runtime identity (Python 3.14.6, SymPy 1.14.0, mpmath 1.3.0).

The separately authored `independent_controls.py` passes **42,965 exact assertions**. It imports neither original checker and uses deterministic biased, strongly biased near-arrow, and skew three-point laws different from the original two checker laws. Controls include direct two-coin replica transitions, forward/backward return agreement, radial ordering through time 64, parity-aware gradients over every tested cell alignment, arbitrary nontrivial old same-parity initial distributions, exact smoothed martingale increments and variances, occupation moments through order 6, and rational exponent margins. These finite checks corroborate identities and boundary handling; they do not certify the asymptotic theorems.

An independent development failure and correction are preserved in the research log: the alternate gradient reindexing in my new checker initially used x−1+y instead of x+1+y. This indexing error was confined to the new diagnostic script and was corrected by direct change of summation variable. The original packet was unchanged.

## Adversarial boundaries and source use

At the excluded random-arrow boundary δ=0, quenched endpoints are point masses and the coarse L1 discrepancy tends to 2 when M=o(√N). Near that boundary, preferred-arrow paths have quenched mass (1−ε)^N, proving that no constants or onset threshold can be uniform over laws as ε→0. The exact finite diagnostic at N=128, M=8, ε=10^(−6), q=1/2 gives a lower bound greater than 1.4656 for every environment. This is consistent with the candidate's explicit fixed-law scope and is not an admissible asymptotic counterexample.

Berger's original Theorem1 and following Conjecture1 were directly consulted for the surrounding quantitative claim, without importing an estimate. [Primary OWR report](https://ems.press/content/serial-article-files/46239), printed p.2151. The origin-perturbed replica mechanism was compared with [Balázs–Rassoul-Agha–Seppäläinen](https://www.math.utah.edu/~firas/Papers/rap.pdf), Section4. That manuscript imposes span1 in its general walk preliminaries, whereas the raw ±1 walk has span2. The candidate supplies its own same-parity half-difference and binomial proofs, so it does not silently import the paper's span1 theorem. This is an attribution/adaptation caution, not a missing premise in B–G. Actual source URLs, retrieved PDF hashes and sections used are in `source_manifest.json`; the full private third-party PDFs are excluded from the authored manifest.

## Exact remaining gap

No unresolved analytic gap remains in this assigned B–G family. The whole-PR claim (A), including the novel small-scale closure, still requires the separately assigned coalescence, conditional final-strip concentration, source-scope and closure lanes. This report does not certify those steps, novelty, priority, or publication readiness.
