# PR480 finite verification: independent verdict before repair

Recorded 2026-10-12T03:47:56Z (2026-10-11, America/Los_Angeles).
Completion estimate: 100% of the independent finite reproduction and code audit;
this is not an estimate of the open-problem or publication workflow.

**Verdict: normal-mode exact reproduction passes; no contradiction in the finite
mathematical outputs was found. One runtime verification weakness should be
repaired in any promoted verification package.** This verdict does not certify
the unbounded mathematics, target fit, novelty, or priority. Those are outside
this assigned code-only audit.

The inspected source is PR480/problem 30003656, head
`cd9025795f40bd9ebc2b32de50917d73ca0f2bfa`. The author snapshot and its pre-existing
audit packet were inspected. No current reviewer reports were consulted. No
frozen files, Git state, queue entry, or external communications were changed.

## Exact reproduction and custody

`replay.py` checks 31 hashes/size records against `SOURCE_RECEIPT.json`,
`FROZEN_AUTHOR_MANIFEST.json`, `audit/FROZEN_INPUTS.json`, and the portable-file
table in `audit/AUDIT_MANIFEST.json`, before and after isolated execution. All
checks match. Outputs are written only into this review's own copied-run folders.

Under normal Python 3.14.6, both output artifacts reproduce byte-for-byte:

| Artifact | SHA-256 |
| --- | --- |
| `exact_results.json` | `4e33a0884d0de172397e4a5693316508767e14eae1bf7041dd865be562277831` |
| `audit/audit_controls.json` | `7c55d69ea60579949394c0830923f247c6d917a3d46ea234e40d46a013a3b2ff` |

The author run has 1,279 pointed maps and 89 pointed injections on cardinalities
1 through 5, 64 premise subsets on four terms, and 1,024 atomic-consequence
comparisons. The pre-existing audit run has 312,413 passing calls to its explicit
`check` function, 294 finite geometric formulas, and eight equality-premise sets.
Run commands, interpreter information, timestamps, exit codes, output hashes,
and individual manifest checks are in `replay_receipt.json`; output files are
under `runs/normal` and `runs/optimized`.

## Additional independent controls

`independent_controls.py` independently constructs both categories by Cartesian
products and injectivity filtering, checks identities and **860,923** composable
map pairs across bounds 1 through 5, then computes negation as a lattice
complement of natural carrier subobjects. This uses explicit stage fibers and
preimages, rather than recursive formula forcing. The resulting negation,
double-negation, beta, alpha, existential, and decidability values agree with
the author output at bound 5. At bound 1 the injection-category alpha is false,
as the recorded audit correctly expects; bounds at least 2 give alpha true.

Actual modified copies of `audit_controls.py` were run for seven mechanisms:
pointwise universal quantification, replacing alpha by a current-stage
existential, dropping the two negations, deleting transition maps, using
injections for the generic category, eliminating growth, and postulating
classical validity at the singleton. Every modified program raises its explicit
`AssertionError` both normally and with `-O`: **14 actual rejected executions**.
The original audit's seven mutation flags are semantic examples rather than
automated execution of modified source; these new runs supply that additional
evidence. In particular, its flag for removing all proper transitions inspects
only the singleton, whose generic values already agree with the discrete
singleton. The actual category mutation is detected at another finite stage.

`independent_controls_receipt.json` records all commands, source/output hashes,
failure labels, category rows, and finite boundary controls. Frozen-source
hashes still match after these runs.

## Runtime weakness requiring publication repair

The author checker uses Python `assert` at original lines 55–62, 95, 100–101, but
constructs a literal `"status": "PASS"` at line 108. Python optimization strips
the assertions. The unmodified program still exits zero under `-O`; its pointed
injection cache count changes from 85 to 79 because checks no longer execute.
Consequently its optimized output is not byte-equal to the recorded result.

More decisively, an actual copied semantic mutation replaces both categories
by discrete identity-only categories. Normal Python rejects it. Optimized
Python exits zero and reports `PASS` even though, for example, the supposed
all-map beta becomes false at cardinality 2. This is an executable false-PASS
demonstration, recorded under `mutations/author_discrete_category` and in the
independent receipt. It does not refute the correct normal-mode result.

The audit checker uses an explicit `if not condition: raise AssertionError`
instead of `assert`; it remains byte-identical and effective under `-O`.
Recommended repair for promoted supporting materials: replace the author's
assertions by explicit failure checks, preserve computation order, and verify
normal and optimized outputs and both equality and forcing failure detection.
The historical source should remain frozen.

## Meaning and exact gaps

The code has no floating-point arithmetic, numerical stability or tolerance
issues, external dependencies beyond the Python standard library, or network
operations. Both programs deliberately write output beside their program files,
which is why replay used isolated copies. Formula environments and covariance
are consistent with the stated outgoing-arrow semantics. The finite injection
enumeration includes identities and all point-preserving injections, and the
all-map enumeration includes every collapse map.

The strongest independently supported result is agreement of the specified
finite category and quotient calculations, their normal-mode exact
reproducibility, and the audited harness's ability to detect the stated finite
mechanism failures. The matrix closure and union-find checks use distinct
implementations. The large assertion total counts repeated finite instances;
it is not a count of independent proofs or universal coverage. The positive
evaluator shares the positive structural clauses with the forcing evaluator,
so comparisons between them partly mirror implementation.

The witness extractor and its verifier share a supplied equality-closure
relation. The verifier checks a finite derivation-shaped witness against that
relation, without independently validating its derivation from the original
premises. A supplied forged all-true relation accepts an unrelated equality;
the genuine empty-premise closure rejects it. Malformed proof tuples can raise
`IndexError`. Neither fact invalidates the actual internally generated tests,
but the routine is not a standalone trusted proof kernel. The source docstring
already disclaims a formal proof certificate, and that limitation should remain.

No finite run establishes an unbounded classifying-topos claim or conservativity
for all geometric formulas, especially arbitrary small disjunctions. Concrete
truncation artifacts are recorded: for every bound K from 1 through 5, the
universal collision formula on K+1 variables holds in every carrier of the
truncated categories; the explicit K+1-element stage supplies a distinct-tuple
counterexample. Thus even stable finite results cannot simply be extrapolated
to arbitrary formulas. The target alpha's finite values agree with its proposed
mechanism, but the universal proof must be checked separately. Historical
priority and whether the original open problem has already been settled are
entirely outside these computational checks.

## Reproduction

From this directory, run `python3 -B replay.py` and
`python3 -B independent_controls.py`. Both retain the source snapshot intact.
The combined replay receipt intentionally reports that not all four outputs
are byte-equal because the author's optimized run exposes the weakness above;
both normal-mode outputs and the optimized audit output are byte-equal.

No proof search was performed, and no acceptance/merge/publication decision is
implied by this finite-code verdict.
