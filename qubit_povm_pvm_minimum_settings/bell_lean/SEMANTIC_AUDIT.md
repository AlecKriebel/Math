# Mathematical-interface audit — 10 September 2026

**Status: the additional exact tests passed. The Lean source is still uncompiled
and not kernel-verified.** No Lean/Lake invocation or remote repository change
was made during this pass. Compiler-free tests cannot establish the complete
formal proof or faithful statement correspondence.

## Deliverable and preservation

This pass adds an independent checker, exact physical fixtures and certificates,
a focused correspondence-review note, and an explicit rank-three coupled-path
stress test. The combined compiler-free preflight now runs the new checker too.

**All 58 mathematical Lean modules, the aggregate import file, and the 14
anonymous statement contracts are byte-for-byte unchanged from the incoming
preflight ZIP.** The source still has 681 theorem/lemma proof attempts (672
public) by static inventory. No definition was weakened, no proof premise was
added, and no Lean proof body was altered to make these tests pass.

`reports/semantic_audit/summary.json` contains per-module hashes and the incoming
archive SHA-256. The prior changed documentation/harness and reports are retained
under `preservation/semantic_audit_baseline/`; another complete nested copy of
the already-nested input ZIP was deliberately not added.

## New exact tests

The final `scripts/semantic_audit.py --suite all` run passed **1,387 exact
checks**, with no numerical comparison tolerances. A matrix identity is counted
as one check, not inflated by counting every scalar matrix entry.

| Suite | Passed exact checks | What was exercised |
|---|---:|---|
| Complex physical conventions | 390 | Six full complex rational strategies; direct Born traces, null/future conditions, whole tables, local unitaries, conjugation and party exchange |
| Common-span filtering | 351 | Three nontrivial exact complex filters; both physical branches and correct state-dependent common weights |
| Incidence and Gram differentials | 115 | Full normalization derivative including the metric term, radial correction, derivative right inverses and finite score-gap identities |
| Degenerate cone circuits | 299 | All 31 vertices of four specified finite rational balanced-ray polytopes, including repeated rays and singular common sums |
| Whole-strategy relabeling | 72 | A genuinely nonlocal PVM strategy, heterogeneous labels, 16 complete branches per scenario and zero-weight boundaries |
| Rank-three coupled physical path | 160 | Exact stationarity, positive multipliers, all single-block dual certificates, an increasing physical interval, and direct/incidence score agreement |

The **27 exact controls** comprise 24 incorrect-formula mutations, one incorrect
interface mutation, and two scope controls. They catch or distinguish missing
transposes, adjoint/transpose confusion, incorrect filter weights, a missing
metric term, sign mistakes, zero-coefficient padding, unrelated input-pair
mixtures, and reliance on individual-block optimization instead of coordinated
physical variation. **They do not mutate or execute Lean source.**

The finite cone catalogue is exhaustive for its four recorded input sets only:
31 vertices in total, 13 with nonsingular common sums and 18 with rank-one common
sums. It is not an enumeration of all qubit measurements or arbitrary Lorentz
circuits. The six complex strategy fixtures likewise do not certify an
arbitrary-input theorem.

## Most informative result: an actual coupled uphill curve

An exact heterogeneous (2,3)-by-(2,3) physical strategy has metric-row rank three
and strictly positive determinant multipliers. With its measurements fixed, its
state attains the global state-only maximum. With the state and all other
measurements fixed, each of its four measurements attains its individual global
maximum, certified by explicit positive dual slacks and complementary slackness.

Nevertheless an explicit coordinated physical path increases the Bell score.
Its direct Born score is

```
f(t) = t²(850000-955000t²-58595t⁴+252t⁶)
       / [40(4-t²)(100+t²)²(100+9t²)],
f(0)=0, f′(0)=0, f″(0)=17/1600>0.
```

A symbolic positive-factor certificate proves `f(t)>0` for `0<|t|≤1/2`. The path
has normalized positive qubit states and measurements throughout that interval.
Six exact finite evaluations independently reproduce the source's incidence-gap
formula from the physical matrices.

**This is not a POVM–PVM separation.** A deterministic PVM strategy on the same
functional already scores 3/10, above the entire certified path. Its value is a
stress test of the coupled-direction step, not a counterexample to the main
claim. See `docs/RANK_THREE_STRESS_TEST.md` and
`reports/semantic_audit/rank_three_saddle_certificate.json` for full formulas.

## A convention explicitly tested

Zero *effects* are legitimate when padding output labels. Assigning an added
label a free zero *Bell coefficient* can instead change an optimization problem.
The inspected residual recoding correctly composes the full Bell functional
with the coarsening map. A negative-functional control rejects the incorrect
alternative. No Lean source correction was needed for that convention.

## Retained checks rerun

The combined compiler-free preflight completed successfully, including all
**92** existing software/runner/package/environment tests, 122 original exact
checks, 1,215 transportation regressions comparing 43,740 probability entries,
the rational SOS and independent positivity checkers, 230 deterministic-gap
identities, and the expanded-source checker's 69 symbolic checks and 474 rational
regressions. Those counts retain their original narrow scopes.

Runner/dependency-parser tests use explicitly mocked outputs in temporary
folders. They are tests of verification machinery, not reports of a Lean run.

## Reproduce

Verify a freshly extracted shipment before any check regenerates its reports:

```bash
python3 scripts/verify_files.py
```

With the Python dependencies already available:

```bash
python3 scripts/preflight_all.py
```

To run only the new independent tests:

```bash
python3 scripts/semantic_audit.py --suite all
```

`all.json` and the aggregate log in `reports/preflight/physical_interface_audit.log`
are the authoritative final execution evidence. Earlier individual-suite reports
are retained with their real earlier checker hashes; their counts are not added
to the final aggregate. Optional numerical discovery is isolated in `research/`
and is not used to certify any reported exact result.

The later real Lean commands remain those in `OFFLINE_RUN.md`, including
`bash scripts/check.sh --serial` for an already prepared environment and
`bash scripts/check.sh --bootstrap --serial` when acquiring dependencies online.
The archive still contains neither the compiler nor compiled Mathlib caches.

## Limits and next verification boundary

No new mathematical blocker or counterexample was identified in the inspected
interfaces. That is not a claim that the complete draft is correct. The general
rank-one exceptional geometry and rank-zero reconstruction were not independently
re-proved in this pass. Compactness, extremality, openness, curve/limit arguments,
and the actual implicit-function API applications remain uncompiled source.

`docs/STATEMENT_CORRESPONDENCE_REVIEW.md` lists what was inspected and what was
not established. The first decisive formal validation remains the actual Lean
build, statement-contract check, and real declaration-level dependency audit.
