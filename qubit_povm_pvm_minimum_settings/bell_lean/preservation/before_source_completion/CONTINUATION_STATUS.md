# Continuation status — 10 September 2026

## Actual result

**The full Lean proof is not complete. Zero project theorems have been kernel-
checked.** The new runtime executes local commands and files correctly, but Lean
and Lake are absent and direct external downloads fail. The project build wrapper
was executed and returned **127 before invoking Lean**. Its current report is
`reports/kernel_report.json`; the actual log is
`reports/session_20260910/build.log`.

GitHub branch creation was attempted through the connected integration and denied
with HTTP 403. No branch, commit, PR, workflow, or manuscript change was made
remotely. A fresh chat alone does not supply the missing compiler or dependencies.

## Source work preserved

The complete input preservation archive is retained at
`preservation/input_recovery_20260910.zip`. All 23 preexisting mathematical Lean
modules remain byte-identical. The aggregate import and generated audit were
updated for one new source module, `Bell/DeterministicGap.lean`.

That module reconstructs the earlier deterministic-replacement shortcut. Its
eight theorem declarations are uncompiled attempts. Stationarity, null incidence,
positive pairings, and strict deterministic gaps remain explicit hypotheses;
they are not smuggled in as axioms. The module proves no unconditional statement
about all physical two-input strategies. See `docs/DETERMINISTIC_GAP.md` for the
argument and its remaining physical obligations.

The static inventory now reports 286 theorem/lemma declarations in 25 source
files excluding the generated audit. This is a text count, not proof coverage.
The formerly missing `Bell/Assembly.lean` and other recovery gaps were not
silently recreated or labelled recovered.

## Checks actually executed

| Check | Result |
| --- | --- |
| Original exact algebra/finite checks | 122 passed |
| Rational transportation regressions | 1,215 passed; 43,740 entry comparisons |
| Rational operator SOS certificate | Passed; corrupt-certificate mutations rejected |
| Independent integer Bareiss positivity checker | Passed all 12 principal determinants |
| Deterministic-gap/table symbolic identities | 230 passed; transpose mutation rejected |
| Offline handoff integrity/safety/syntax tests | 21 passed |
| Lean compiler build | Not invoked: wrapper exited 127 at toolchain discovery |

These rows are different kinds of evidence. Only the last could provide Lean
verification, and it did not run. Polynomial and finite regression checks do not
prove the remaining physical or analytic arguments.

## Concrete environment handoff

`environment/bell-lean-offline.yml` is a self-contained workflow intended for
`.github/workflows/bell-lean-offline.yml` in `AlecKriebel/Math`. It embeds all exact
pins and helper code, so the Lean sources need not already be on GitHub. On an
online GitHub-hosted Linux runner it is designed to prepare Lean 4.19.0 and this
project's exact Mathlib cache, check positive/negative Lean smoke examples before
and after relocation, and export separate parts of at most 400 MiB each.

The paired restorer accepts raw parts or GitHub artifact ZIPs, verifies hashes,
rejects unsafe archive paths, checks exact revisions, reruns compiler smoke tests,
and can invoke the actual project build/axiom audit. It refuses overwrites.

**That workflow has not been installed or executed. No offline compiler bundle
was produced in this chat.** Only its local transfer/safety/syntax tests have
run. Read `environment/README.md`; the next build begins after the real compiler
and matching cache are supplied, not after another chat restart.

## Still missing from the full mathematical formalization

The compiler is only one blocker. The universal equality still needs compactness
and extremal reductions; the cone/common-span residual reduction; physical
Lorentz coordinates and local reconstruction; derivation of stationarity from
physical maximality; tangent integration and the actual second-variation curve;
and the rank-trichotomy assembly with physical hypotheses supplied. Strengthened
physical attainment remains separate. The deterministic-gap shortcut removes
a duality argument from the positivity implication, not these obligations.

A future clean build of the existing subset must not be relabelled a full proof.

## Machine-readable continuation

`reports/session_20260910/progress.json` records actual checks, source provenance,
missing work, and the first unfinished operation. `SHA256SUMS.txt` authenticates
this snapshot. `scripts/package_continuation.py` recreates the source archive
without including toolchain caches or pretending that packaging verifies proofs.
