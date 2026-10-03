# Independent adversarial audit of the PR 373 memory-coupling route

The candidate's Turn 3 coupling theorem passes the mathematical audit within
its explicit assumptions. It does not establish the unrestricted
probability-only method requested in Steif's Question C, and the candidate
correctly says so. This is an internal AI-assisted audit of that route and its
reproduction. It is not an external peer review, a novelty certification, or
an overall PR disposition.

The input is the parent-specified frozen head
`4e635c77d7399d671ea58700e41bbd92cbdeeb46`, at the snapshot's
`unsolved_math_prioritization/attempts/30004435`. No author files were edited.
No external individual was contacted, no service was written to, no install
was performed, and no Git operation was performed. All new files are in this
audit folder. Root and sibling proofs remained unread.

## Source-first order and checkable proofs

The baseline was sealed at **2026-10-03T08:51:00Z**, before candidate prose or
code. Its SHA256 is
`0fa5ab0dd0f105bc2fa6a816f9e85d267179f6eb82149b9131b1139752bb71f1`.
Only the candidate's source-locator/hash metadata was used before that seal.
Fresh EMS, BFG, and Al-Najjar/Shmaya PDFs were downloaded and hashed; the
critical pages were rendered and inspected privately.

`SOURCE_FIRST_BASELINE.md` independently proves an agreement-length domination
by an auxiliary Markov chain. Its infinite product gives a positive chance of
never returning to zero; stopping-time renewals give finitely many returns
almost surely. This produces a uniform full-infinite-future total-variation
bound. Stationarity and covariance symmetry then give both one-sided-tail
zero-one laws. It also proves that the auxiliary last-return expectation
requires **weighted** summability; a geometric number of excursions does not
make their durations integrable.

Candidate `TURN_3.md` and `RESULT.md` were then read. The mathematical verdict
was sealed at **2026-10-03T08:55:56Z**, before any candidate program, receipt,
or old-review content was read. `MATHEMATICAL_VERDICT.md` checks the candidate's
distinct forcing-block/stopping-time proof, the quantitative indices, the
conditional future version, uniqueness, and the continuous infinite-memory
example's existence construction. There is no mandatory mathematical revision
to that route. Completed-field statements use equality modulo ambient null
sets, equivalently the usual ambient null augmentation, rather than claiming
literal equality of uncompleted raw sigma-fields.

The primary target is for **all stationary finite-alphabet processes**. The
source states the tail identity is known and asks for a proof without entropy;
it also separates bilateral tails. The new overlap/continuity assumptions are
therefore restrictions on the target. [Steif Question C, printed 632](https://ems.press/content/serial-article-files/46847).
The entropy identity is independently corroborated by [Al-Najjar/Shmaya,
pages 13-14](https://arxiv.org/pdf/1406.6670).
The reconstructed coupling mechanism credits the normalized chains, maximal
couplings, and agreement lengths in [Bressaud/Fernandez/Galves](https://arxiv.org/pdf/math/9806132).

## Independent controls and preserved erratum

`independent_controls.py` preceded the candidate mathematics. Its exact
controls check 225 rational maximal-coupling pairs, 213 monotone domination
transitions, and renewal recursions through 96 times. The triangle of three
probability vectors distinguishes uniform pairwise overlap from a global
minorizing measure. Other controls separate coordinate convergence from
full-future convergence, and finite last-return time from finite expectation.

One hand-entered comparison in its first execution was wrong: the exact
last-return expectation is **19/7**, while the assertion contained 47/21. The
assertion alone was corrected. `artifacts/independent_controls_initial.py`
and its initial stdout/stderr preserve the failed run. This did not change a
universal proof or a candidate file.

`block_bound_controls.py` was written after candidate mathematics and before
candidate program inspection. It calculates the full infinite-future
disagreement event in finite-memory approximations, using permanent agreement
once both finite histories coincide. All 5,520 comparisons to the displayed
candidate bound pass. These are finite supplementary controls, with the
universal proof kept separately.

## Original programs, exact replay, and old-review coverage

All 366 lines in the eight top-level invoked author programs/helpers were read
before running the full replay. All programs are standard-library finite
computations and local integrity checks. Bytecode writes were disabled; the
candidate snapshot remained read-only.

The complete author replay with source checks passes:

| Receipt | Result |
|---|---:|
| Total author assertions | 210,974 |
| Per-turn assertions | 5,527; 25,404; 25,455; 123,026; 31,562 |
| Historical/final manifest entries verified | 166 |
| Fresh primary-source hashes verified | 4 |
| Author replay exit code | 0 |

The fourth source, Lemańczyk's thesis, was fresh-fetched after the mathematical
seal solely for the full replay's optional source-integrity check. It was not
used to establish this route's mathematical verdict.

`replay_harness.py` separately preserves stdout and stderr for each of the five
author checkers. Each stdout equals the frozen receipt byte for byte. It also
replays the old review's verifier and 9,334-control script after both were
read in full. All exit codes are zero and all stderr streams are empty.
`artifacts/REPLAY_REPORT.json` records commands, actual UTC times, output
hashes, and receipt equality results; the whole author replay's streams are
also retained.

The author's Turn 3 program uses finite horizons and truncations. Its checks
do not empirically prove an infinite-future theorem, and its prose correctly
does not claim that they do. The new independent controls check full future
events in finite approximations while the separate proof handles general
infinite histories.

The old review's Turn 3 assessment agrees with the independently sealed
assessment, including the stronger-than-target assumptions and the absence
of a bilateral conclusion. Its verifier checks **recorded historical local
blob bindings**; passing it is not verification of the live PR's current head.
Live metadata gates and the ordering of PR dispositions remain with the root
audit. No result from the old review was imported into the earlier verdict.

## Strongest result and exact remaining gap

The strongest verified coupling result is: a history-uniform normalized
kernel with TV overlap bounded away from zero and summable agreement
continuity has a unique stationary compatible law if one exists; that law
has uniform remote-future total-variation convergence and trivial equal
completed one-sided tails. The displayed binary infinite-memory example
realizes these assumptions. Neither a bilateral-tail theorem nor finite
expected last-coupling time is inferred.

The exact remaining target gap is an entropy-free argument for arbitrary
stationary finite-alphabet laws, including conditional kernels with no
uniform overlap or summable continuity. No valid reduction to this subclass
is supplied or presumed. The review task is complete; the unrestricted method
question remains unresolved by this route. No current-openness claim is made.

## Public package and reproduction

`PUBLIC_MANIFEST.json` is an explicit whitelist of authored reports, seals,
independent code, and freshly generated replay streams. It excludes private
PDFs, extracted text, rendered pages, and raw author-packet copies. Fresh
source hashes are metadata only. The seal records the final public manifest.

Reproduce the original independent controls with Python 3:

```text
python3 independent_controls.py
python3 block_bound_controls.py
python3 verify_public_manifest.py
```

`replay_harness.py` additionally requires the frozen candidate at its existing
relative snapshot path. The whole author's optional source replay requires
the four locally available primary PDFs; public distribution intentionally
does not include them.
