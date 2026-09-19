# Trust report — local runner update and historical source-only report

## Local runner update — 18 September 2026

Local Lean execution and compiler repairs have now been completed for the
existing source; the sections below preserve
the **historical 17 September source-only status**, not a claim that no local
module has ever compiled. Current audit records determine which modules passed.
The final unconditional group theorem remains absent.

The validation runner now compiles every module in the exact selected project
import closure serially with `lean -j1`. It deletes stale selected objects before
starting, blocks dependents of failed modules, rejects missing compiler outputs,
and checks that project source hashes stay fixed during compilation. Timeouts
kill the complete subprocess group, including children spawned by Lake.

Dependency checks now reject untracked changes and ignored Lean source outside
normal `.lake` artifacts. Ignored build/cache artifacts remain permitted.
Pinned upstream objects are preserved: no full dependency-source rebuild has
been performed. `--fresh-project` explicitly requests the default fresh project
check; the old full-dependency `--fresh` option fails with an explanation.
The rechecker's separate `--fresh` option still means same-kernel replay.

Python negative controls tested stale and partial output removal, failed-import
blocking, missing output and executable rejection, source mutation rejection,
exact selection, process-group timeout termination of a TERM-resistant child,
and dependency source-shadow rejection. These checks test the runner, not
Lean's kernel or the absent theorem. Original source and axiom-parser controls
also continue to pass.

## Historical actual status — 17 September 2026

No Lean source was compiled in this continuation. No Lean installation, remote
CI setup, axiom query, same-kernel recheck, or comparator was attempted. The user
explicitly requested source for offline execution after the previous setup
failure. **Actual axiom dependencies are unknown, not an empty list.** There
are no kernel-checked milestones to report, and the final group theorem is absent.

The previous session's environment failures and C++ reproduction logs are
retained as historical records. They are not new tests or new setup attempts.
See `logs/README.md` for the separation.

## Evidence produced here

Exact Python reconstruction checked the weighted bracket and Lean literals,
all 900 equations of the new 30-by-30 rational inverse witness, all 88 cleared
integer generation nodes and 31 targets, 196 small scalar kernels, and 420
small Dynkin controls. Deliberately incorrect new witnesses were rejected.
The direct-flag checker also reran its 4495 integer Jacobi triples and 12
special identities. These are **external computations**, not formal proofs.

The static inventory recursively scans all source modules, rejects direct
admission/native-proof patterns, checks that all modules belong to the root
import closure, and produces query files for public named declarations. It
is not a Lean parser or an elaborated-environment inventory. Private/generated
names are not guessed; compilation plus the actual transitive dependency
reports must validate the resulting environment.

Python controls exercise rejection of direct proof admissions, project axioms,
compiler-trusting proof evaluation, missing/duplicate/unexpected axiom output,
and unexpected axioms. They test the runner, not the correctness of the Lean
kernel or the mathematical statements.

## Prepared offline checks

The toolchain is Lean 4.19.0; Mathlib commit
`c44e0c8ee63ca166450922a373c7409c5d26b00b`; optional lean4checker commit
`e11f65c651edd58d68ba260015d2bfde5102cd7f`. The Lake manifest is source-derived
from the pinned upstream manifest and has not been validated by running Lake.
Selected actual Mathlib sources were consulted, but not every drafted API use
has been checked or elaborated. See `docs/API_LEDGER.md`.

The offline runner requests a real build, exact elaborated type output, and
actual `#print axioms` output for the selected module closure. It accepts only
`propext`, `Classical.choice`, and `Quot.sound`; no report, a duplicate, an
unexpected name, or an unexpected axiom causes failure. Actual declaration
inventory fidelity still requires an elaborated review. The runner checks
protected source/data/script hashes and dependency revisions across a run.

The PATH executable's recorded hash may be an elan shim. Neither that hash nor
the dependency hashes amount to a verified bootstrap of Lean's compiler. The
optional rechecker is Lean's own kernel replay, not an independent kernel.
Cached upstream oleans may have platform/bignum compatibility limitations.
At that date, `--fresh` and `--cache` were separate proposed options. See the
18 September update above for their revised operational status.

`--milestones` imports and builds **all present draft mathematics**. It never
claims to prove the absent main result. The default final gate exits with
`INCOMPLETE_FINAL_GROUP_THEOREM_ABSENT`. There is no hidden final-proof axiom,
mock BCH group, or assumed certificate acceptance.

## Release conditions still unmet

The complete mathematical construction and both full-automorphism passages must
be closed; the actual Smith witness must be accepted by a proved checker; and
the exact final ordinary-`MulAut` statements must be inspected and rechecked.
The deposited DOI identity also remains unverified. No external human peer
review, new priority claim, or publication action occurred in this continuation.
