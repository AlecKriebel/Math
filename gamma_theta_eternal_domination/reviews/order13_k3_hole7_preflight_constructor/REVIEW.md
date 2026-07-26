# Independent constructor preflight: order 13, k=3, hole7

## Verdict

**`ACCEPT_EXACT_HOLE7_PACKAGE_PREFLIGHT`**

The live package `instances/order13_k3_hole7` is accepted as an exact
pre-production input.  It contains exactly the intended `hole7` formula,
complete coloring bank, and constructor manifest.  All three files are
byte-identical to a fresh constructor-A package generated from a private copy
of the exact committed source bytes at
`b9b74a38415dac6ef11bb7cbc55badf224affadd`.  The formula is also
byte-identical to a fresh emission by the separately accepted clean-room
constructor B.

This verdict is deliberately narrow.  No SAT solver or proof checker was
launched.  It makes no SAT, UNSAT, template-exclusion, finite-slice,
counterexample, or conjecture claim, and it is not production initialization.

## Exact package binding

The package contains exactly three nonsymlink, single-link regular files:

| artifact | bytes | SHA-256 |
|---|---:|---|
| `coloring-bank.json` | 505,200 | `efafa89d6096d81bc0ae5a1860be4d0ce69b56f4e4957c8bd307316c121e692d` |
| `constructor-manifest.json` | 5,409 | `a218a21b761754bfaef520d8e98d10963c97a1178966cbfbb68054005ac53bf9` |
| `instance.cnf` | 1,372,338 | `3e1c86ccbcfc1e04b3ec4de29ec5b7d342cf909553655f959b1c35de0a36c340` |

Their total size is 1,882,947 bytes.  Hashing the sorted ASCII records

```text
name SP sha256 SP size_bytes LF
```

gives package-set SHA-256
`0f651f87b1339273776505da9eae50c1fa681623310216ea48d430ca354eb448`.

The package is a newly generated working-tree object and is not asserted to
belong to the bound commit.  The commit binding applies to the exact
constructor sources and accepted C-055 review chain; the table above binds the
live package bytes reviewed here.

## Independent census and parsing

The audit strictly parses all three artifacts.  JSON parsing rejects duplicate
keys, nonfinite constants, malformed UTF-8, and noncanonical serialization.
The DIMACS parser requires an ASCII formula, one valid header, closed nonempty
clauses, in-range nonzero literals, the promised clause count, and a terminal
line feed.

The parsed and independently rederived census is:

| quantity | value |
|---|---:|
| variables | 9,802 |
| full clauses | 34,903 |
| full literals | 349,248 |
| coloring-bank rows | 5,103 |
| coloring-obstruction literals | 122,229 |
| base clauses | 29,800 |
| base literals | 227,019 |

The checker independently enumerates every first-use-canonical proper
three-coloring of the forced positive `hole7` template graph.  The resulting
5,103 sorted unique rows equal the JSON bank exactly.  For each row, it then
rederives the clause consisting of the H-edge variables whose endpoints have
the same color.  These 5,103 clauses equal the DIMACS suffix in order and
literal-for-literal.  Subtracting this independently derived suffix from the
strict full census gives the base counts above.

## Source and commit binding

The audit binds the constructor and accepted C-055 sources to frozen baseline
commit `b9b74a38415dac6ef11bb7cbc55badf224affadd`; it does not require that
baseline to remain the current branch tip. It obtains the committed blobs
with read-only `git show`, compares them with the live source files before
construction, and repeats the live comparison after all private work. This
keeps the exact preflight replayable after later documentation-only commits.

| runtime source | bytes | SHA-256 |
|---|---:|---|
| `src/search/order13_k3/__init__.py` | 584 | `90809fbba9e0fb06998ac910db44ff232849bd5b4ab8f9dfbc4c4e931ca96892` |
| `src/search/order13_k3/__main__.py` | 125 | `6a1a7df4c3919e17d29bbe27ac10c6ba66e18a37bdefac0e0f05af845572b524` |
| `src/search/order13_k3/encoding.py` | 22,581 | `da06a797a29fcefff1eadbea4aa1535fb2ef14c0c64d84236bb3bf9241e1d47d` |
| `src/search/order13_k3/generate.py` | 24,045 | `35c78ecc4802667514c6294ac00558b83c9cfc83a37f9854533aedb9ca1bf1d0` |

Under the constructor's documented sorted-record convention, the source-set
SHA-256 is
`6dc5f770c792dfcc3ebaa8dd74485220832005e8c8026b030883356af38fcf64`.
The manifest records exactly these four sources, in this order, with the same
sizes and hashes.

## Private regeneration

The audit creates a fresh directory under canonical `/private/tmp`, copies
only exact committed constructor blobs into the expected private source tree,
and executes the allowlisted `generate --template hole7 --validation-gate`
entry point with bytecode disabled and warnings fatal.  It compares the
generated formula, bank, and manifest directly with the live files.  All three
comparisons are byte-identical, including the manifest's Python 3.14.6
environment and normalized command.

It separately copies the exact committed clean-room constructor-B source and
runs only its `emit --hole 7` action under isolated Python.  Constructor B's
1,372,338-byte formula equals both constructor A's fresh formula and the live
formula byte-for-byte.

The only child processes used are read-only Git queries and those two
constructor emissions.  No constructor audit that could dispatch a solver,
production runner, SAT solver, proof conversion, or proof checker is invoked.

## C-055 acceptance chain and symmetry boundary

Thirteen exact artifacts bind the accepted C-055 chain: the current theorem
note, both independent-constructor records, the constructor integration
review, the original hostile mathematical review, and its revised-byte
addendum, including their audit sources and human review files.  Every bound
artifact equals its exact committed blob.

The machine-checked verdicts are:

- `ACCEPT_EXACT_CLEAN_ROOM_RECONSTRUCTION`;
- `ACCEPT_CONSTRUCTOR_A_FOR_PROOF_PRODUCTION_INPUTS`;
- `ACCEPT_MATHEMATICS_WITH_NONMATHEMATICAL_WORDING_GAPS`; and
- `ACCEPT_REVISED_BYTES_MATHEMATICS_UNCHANGED`.

Both accepted constructor records contain the exact live `hole7` census and
hashes.  Constructor B records complete coloring coverage, exact semantic
clause multisets, only justified template relabeling, and
`no_unproved_symmetry_breaker: true`.

The live manifest fixes only the justified independent triple `[0,1,7]` in G
and has `heuristic_symmetry_breakers: []`.  Since the live formula is
byte-identical to the accepted clean-room formula, the preflight found no
DoubleLex, unrelated anchor, signature, reflection, or other unsafe heuristic
symmetry restriction.

This finding concerns construction soundness only.  It does not independently
reprove the full C-055 mathematical theorem in this review.

## Hostile mutations

Ten isolated mutations were exercised, and all ten were rejected:

1. an extra package file;
2. a formula bit flip;
3. a coloring-bank bit flip;
4. a manifest bit flip;
5. a manifest relabeled to the wrong `hole9` template;
6. a symlinked formula artifact;
7. a symlinked package directory;
8. drift in `encoding.py`;
9. a symlinked constructor source; and
10. a multiply linked formula artifact.

The mutations run only on private temporary fixtures.  The live package and
constructor sources are read-only throughout the audit.

## Replay

From the campaign directory:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONWARNINGS=error \
  python3 -I -B -W error \
  reviews/order13_k3_hole7_preflight_constructor/audit.py |
  cmp - reviews/order13_k3_hole7_preflight_constructor/evidence.json
```

The replay output is deterministic and byte-identical to `evidence.json`.
The review directory contains only `REVIEW.md`, `audit.py`, and
`evidence.json`; it contains no bytecode cache.

| review artifact | bytes | SHA-256 |
|---|---:|---|
| `audit.py` | 46,081 | `49fd41ea1c94c86a8cf172b2a0890d82c803a0ee926022e2a84566d97e9ece79` |
| `evidence.json` | 8,058 | `0ac51dd6b084d54be2a9f3f403c6d2c6b096d25ca6d6f380853fe755fc17cf28` |

## Final disposition

The exact live `hole7` package is suitable for a separately authorized,
fail-closed production initialization that preserves these input bindings.
Any change to the four runtime sources, the accepted C-055 chain, or any of
the three package bytes requires a fresh preflight. A change to unrelated
repository bytes does not. A later production result requires its own
solver-output and proof-certificate audits before any mathematical promotion.
