# PR239 / 30001321: reproduction and historical-review-package audit

**Disposition: PASS_FINITE_REPRODUCTION_AND_HISTORICAL_BINDING. No mandatory mathematical or package correction found within this family's scope.** This verdict does not certify novelty, infinite-time estimates, the original-source interpretation, historical reviewer independence, or publication readiness by itself.

The reviewed original and current attempt snapshots are bound to the parent-supplied materialization manifest: 65,348 bytes, SHA256 4ddb9e5c9dc2487b9fb5fd8f993e562517b5efe2b4af2c2ae87c1a5c61feefa4, at HEAD 7f17eef77c52b2d9b2ec3ad0803c016267fa6496. I independently rehashed all 64 full materialized bodies and checked their native Git-blob SHA1, SHA256 and lengths against that manifest. This is full-body authentication of the selected original/current attempt snapshots and QUEUE materialization; it is not an independent native-network custody claim.

## 1. Actual reproduction

I fully read check_turn1.py, check_turn2.py, check_turn3.py and independent_review/independent_check.py before executing any of them. They contain finite rational calculations and standard imports; only turn 1 additionally imports the installed SymPy. They contain no network, file-write, shell, dynamic source-loading or external-effect operations.

All four actual executions returned exit code 0, empty stderr, and stdout **byte-identical** to the respective frozen JSON receipt:

| Checker | Exact assertions | Scope actually checked |
|---|---:|---|
| check_turn1.py | 486 | Two elliptic two-point laws, complete reachable environments through time 4; annealed endpoint law, replica overlap, quenched mean variance, interval-layer variance; 31 symbolic resolvent coefficients per law |
| check_turn2.py | 50,324 | Backward hitting profiles through time 40; conditional environment-prefix overlap and occupation moments through time 4; deterministic dyadic blocks, fixed-exponent margins, tail algebra and parity residue inequalities |
| check_turn3.py | 17,148 | Killed lazy reflection, finite quenched coalescing coupling, moving-strip substitutions and nonlinear norm sensitivity, killed-mass loss, within-cell replacement, final exponent margins |
| independent_review/independent_check.py | 31,888 | A polynomial return-resolvent identity, nontrivial old-law replicas, three-valued environments through time 3, direct coalescing-pair propagation, path-sum tubes/strips, real cell widths, parity residues and exponent margins |

Turn 1 ran under Python 3.11.8 with the preinstalled SymPy 1.14.0. The other three ran with Python's site initialization disabled and use only the standard library. No optimized Python flags disabled the scripts' assert statements. Each small ACTUAL_*.json receipt records the exact command, source digest, stdout digest and actual returned output. ALL_FOUR_ACTUAL_REPLAYS.json records their agreement.

These are assertion counts, not counts of independent mathematical propositions or proof branches. Many assertions are parameter or environment instances of the same finite identity. Neither the historical reviewers nor this family may infer a uniform asymptotic estimate merely from the counts.

## 2. Materially different independent finite controls

I authored independent_finite_check.py without importing or calling any historical checker. I had already read those checkers and the historical review, so this is a new mechanism-based cross-check, **not a blinded review**. Its actual archival run returned PASS with 19,340 exact assertions, empty stderr and exit code 0. The source digest is 96f1382b6fb295fc468ec5ef0c903499b3d7894f86c2ac91b711fa62ba0a3486; its 990-byte stdout digest is 10248a73a5956879736eb76d68da24d07eee6dc5deeae6b9d237a56a57848f30.

The additional mechanisms are:

- **Ballot first passage and renewal.** For a homogeneous lazy walk with neighbor probability a, first hitting zero from 1 at time t has exact coefficient
  sum over odd m <= t of binom(t-1,m-1) Catalan((m-1)/2) a^m (1-2a)^(t-m).
  The last step must move, so the holds are inserted into the preceding t-1 slots. This differs from the historical square-root series and squared-polynomial resolvent checks. Using first-return coefficients f_1=1-2delta and f_t=2delta h_(t-1), I compute the sticky return law by renewal and compare it with separate forward propagation and backward profiles. Six parameter pairs include q=1/1000 and q=99/100, delta/a=1/10000, and deterministic elliptic delta=a. Coefficients through time 20 agree. The same first-passage mass gives reflection survival for starting gaps 1 through 4 through time 12.

- **A genuine finite maximum event.** Enumerating all 128 Bernoulli paths through time 7, I check the rational nonnegative martingale z^B_t/(1-q+qz)^t for three biased/unbiased q values and three rational z values. Its exact means equal one, and the maximum-event probability obeys the finite Doob bound at four thresholds. An explicit strict difference between maximum and terminal events is required to pass. This catches the endpoint-only substitution that would be insufficient for the proof's tube-escape estimate. It does not numerically certify the Gaussian Hoeffding exponent; the analytic exponential-supermartingale argument must establish that.

- **Formal path read-variable sets.** Across 360 parameter/start/horizon cases and 7,560 individual nearest-neighbor paths, I collect exactly which environment sites can be consulted before killing. I verify every consulted site lies in the alive tube and that its deterministic strip has the starting point in the stated enlarged influence interval. I check the worst overlap bound of six directly. Five drifts include -99/100 and 99/100; integer radii are 1, 2, 3 and 5; horizons are 1 through 6. An exit-and-return path must exist, so killing is not replaced by an endpoint test. This mechanism tests read-variable geometry, rather than relying on two selected numerical environment substitutions.

The historical tests separately and exactly verify weighted subprobability mixtures, the 2w_k oscillation, coarse nonlinear norms and mass replacement; the new path-set checks complement that coverage. Irrational drift, arbitrary horizons, all environment laws and limiting claims remain analytic obligations. The excluded delta=0 random-arrow boundary is not smuggled into the positive elliptic grid.

## 3. Historical bindings and scope

All entries in TURN_1_MANIFEST.json (9 files), TURN_2_MANIFEST.json (5 files), FROZEN_MANIFEST.json (24 author files), and independent_review/REVIEW_MANIFEST.json (6 review files) match their full current bodies. The turn-2 earlier-manifest pointer, reviewed_hashes.json's exact author-file list and author-manifest digest, and the review's proof/manifest references are consistent.

The preserved progression is coherent:

- Turn 1 is a historical unreviewed partial: ordinary coarse L1 convergence, explicitly no superpolynomial conclusion.
- Turn 2 is a historical unreviewed partial at fixed polynomial scales gamma>1/4. It explicitly refuses choosing gamma depending on N to cover arbitrary slowly growing target scales.
- Turn 3 is the frozen all-scale candidate, explicitly pending separate review and with no novelty claim.
- The subsequently dated review binds that exact proof and returns PASS_COMPLETE_SOURCE_TARGET, while expressly excluding novelty and priority.

The recorded 25%, 40% and 90% completion estimates and pending-review wording are historical snapshots; their retention is not an unpropagated mathematical correction. A final publication should identify them as history and provide its own dated current disposition. Do not silently rewrite those frozen manifests or portray the old pending-review file as the final current assessment.

I read PROOF.md, the complete TURN_1.md and TURN_2.md, the full historical independent review, the source-review/addendum, status/budget/continuity records and verification notes. I found no correction supplied by the historical reviewer that was omitted from the frozen proof. The review expressly says no mandatory correction was needed and does not claim the finite checkers establish asymptotics. The candidate proves the affirmative theorem, and the records consistently state that this would refute the source's negative conjecture, rather than prove that negative conjecture.

**Evidence limit:** The internally ordered timestamps and manifests authenticate the bytes and their self-reported sequence, not the physical creation times, original number of model turns, distinct reviewer identity, absence of pre-freeze proof assistance, or historical PDF reading. The historical statement “the reviewer did not supply an ingredient before freeze” is preserved testimony, not independently established by this package. Four primary PDF hashes are recorded, but their bodies are outside these selected attempt snapshots; this family did not reopen or hash those PDFs and does not adopt the old “four primary PDFs verified” statement as a fresh observation. The parent's separate original-source and priority family must decide the source/priority questions.

## 4. Mathematical limits and disposition

The finite checks are consistent with the claimed mechanisms: biased annealed increments, a sticky difference chain with a radially maximal backward hitting profile, same-parity coalescing reflection, full-segment killing, and independent deterministic strip inputs. The written proof explicitly retains fixed-law constants, deterministic alignments, parity, merely elliptic 0<p<1 a.s., and a qualitative rho(ell,M_N)->0 without a polynomial lower rate on the target scale.

In the written dependencies I found no circular appeal from the finite checks to an asymptotic assertion, no use of a future-conditioned martingale law, no independence assumption on interval masses or overlapping starting cones, and no claim of a uniform bound near delta=0. These analytic observations support but do not replace the parent's independent proof audit.

No source edit or mathematical repair is requested by this family. There was no Git use, original global lock acquisition, PR/ref/provider/tracker mutation, network access, external communication, chat coordination or cleanup. All authored outputs are small, finite files in this dedicated folder. This family's task is complete; the full PR/publication goal remains open.

