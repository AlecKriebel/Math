# PR411 / 6800014 exact candidate verification

This standalone bundle contains all nineteen original PR-head author files in
`original_packet/` and the corresponding nineteen current candidate files in
`author_packet/`. The original PR head is
`ac8b960bdda61c154cc30d7e3aba70389a9b139e`. Current status remains
`claimed_solved`, with author proof-search turns **2/5**. The current guard repair
adds zero author proof-search turns and makes no mathematical change.

Authenticate the bundle's published seal or archive digest from independent
project custody **before executing it**. This is an unkeyed integrity bundle:
someone able to replace all code, data, whitelist and seal together is outside
its threat model. Hashes bind the exact prose that reviewers inspected; they
do not themselves prove the meaning or truth of arbitrary prose.

Create a private environment outside the delivery folder. These example commands
also work when the bundle path has spaces:

```sh
python3 -m venv /path/to/private-venv
/path/to/private-venv/bin/python -m pip install sympy==1.14.0
/path/to/private-venv/bin/python "/path/to/verification/run_all.py"
/path/to/private-venv/bin/python -O "/path/to/verification/run_all.py"
/path/to/private-venv/bin/python "/path/to/verification/reproduce_controls.py" \
  --private-log-dir "/path/to/private-raw-logs"
```

Current replay uses Python **3.14.6**, SymPy **1.14.0**, and its mpmath dependency
**1.3.0**. No runtime, virtual environment, downloaded data, raw fixture or
third-party source is included. The scripts resolve packet paths relative to
their own location and can run from another working directory. Executing a
direct algebra checker proves only that its guarded identities passed; use
`run_all.py` for full byte and file-set binding.

`run_all.py` checks the exact positive package inventory, every delivered file
hash, all nineteen original receipt sizes/SHA256/Git blob SHA1 values, both
publication manifests, both six-file frozen inventories, unchanged theorem and
historical audit bytes, exact AST guard relations, recorded output SHA256 values,
and all **54** actual mandatory guard evaluations. Original 19/2/18 assertion
nodes correspond to 24/2/28 runtime checks because some guards occur in loops.
The full source AST is unchanged except that each `assert P` becomes
`if not (P): raise AssertionError("mandatory checkpoint …")`. No original
assertion had a message. Predicate truth conversion and Python short circuit
are retained; the constant diagnostic is evaluated only on failure. The current
scripts and bundle entrypoint use explicit exceptions in both normal and `-O`
execution.

`reproduce_controls.py` makes fresh private temporary copies. It checks normal
and optimized foreign-directory baselines and a clean archive extraction with
spaces, false current theorem interval, false current manifest claim, frozen
proof/metadata corruption, original-receipt corruption, checker corruption,
missing/extra files, an unlisted FIFO (POSIX), whitelist tampering, direct false algebra predicates,
direct frozen-hash failure, short-circuit traps, and a changed predicate whose
candidate manifest and custody hashes were all recomputed. That last control
must still fail the exact AST relation. Raw commands, outputs and mutated
fixtures belong outside the bundle. `TEST_RESULTS.json` is summarized evidence;
the controls and actual scripts are the reproducible checks.

## Hash custody and absent history

`PUBLICATION_MANIFEST.json` intentionally omits its own hash. A separate positive
`PUBLICATION_WHITELIST.json` includes **all** current prose, current metadata,
original inputs, checker code, results and runner code. The whitelist omits only
itself and `FINAL_SEAL.json`; these two files are explicitly separately custodied
to avoid impossible self-hash cycles. The final seal names the real SHA256 of
the whitelist. Its own real SHA256 must be carried in the parent package custody
or other independent distribution record. There are no invented self hashes.

The original historical audit and the `frozen_author/` scripts remain intact.
Original optimized `-O` output is **not certified validation**: its assertions
are erased by Python. Two historical metadata references remain **UNATTESTED**:

- Standalone historical source manifest:
  `f5446c816081c5322e4279bcd9a61dca5bfb63cfacf69d105d1587ed9d93b7fb`.
- Pre-path-adjustment historical checker:
  `eccde3c2a903b1fca0f232e7e392d537479ddd3936281a37e87c4f7e7047be97`.

Those byte objects are absent. The bundle validates the included six frozen
objects and actual PR-head checker bytes, and never fabricates attestations for
missing objects. Historical corpus/search claims, original runtime, novelty,
and inaccessible live aggregator wording are outside this software replay.
No mathematical theorem is inferred from a semidefinite Hessian or checker
output alone; analytic coverage remains in the independently reviewed proof.
