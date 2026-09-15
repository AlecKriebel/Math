# Cyclic Bell formalization: repair and evaluation

**Final verification: passed.** The repaired companion passes the complete frozen clean build, all controls, every-declaration axiom checks, and source/dependency integrity checks. Independent reviews found no remaining gap in the mapped mathematical result statements. The proof-method and external-result boundaries below remain explicit.

## Manuscript and preserved input

This evaluation concerns the merged v1.1.0 manuscript at `../../main.tex`, not
one of the earlier separate notes. Its SHA-256 is
`82a47d69e43a4a3d18aa8c351b81cfae09c9a06910e85d91ae7daf120f201b71`.
The frozen implementation is Git commit `6648fbca6`; subsequent evidence-only
commits do not change its Lean sources or verification inputs.

The received handoff was not an executable formalization: the first build failed
in foundational matrix, Fourier and scalar modules. Its own coverage report also
identified substantive omissions. All 289 received files remain unchanged in
Downloads; [the input integrity receipt](FINAL_INPUT_INTEGRITY.json) checks their
original hashes. Repairs live in the repository companion.

## What was repaired

The original proofs needed extensive Lean 4.19/Mathlib API, coercion, summation,
inner-product, finite-index, matrix and functional-calculus repairs. One important
parser repair parenthesizes the entire first-SOS summand so both square terms
are actually under the intended sum. Several incomplete proof steps required
explicit algebraic, positivity, support and supremum arguments.

All 1,538 original named declarations remain. Independent reviews compared
original mathematical objects and statement signatures, including a final review
of every module changed after the preliminary audit. They found no narrower
physical model, added target-conclusion premise, weakened endpoint, or deleted
original declaration. See [the final statement reconciliation](FINAL_STATEMENT_RECONCILIATION.md)
and [the declaration inventory comparison](FINAL_DECLARATION_PRESERVATION.json).

The main coverage additions are substantive proofs, not validity assumptions:

- The arbitrary-Hilbert polar positive-factor identity, including singular
  operators, and the arbitrary-Hilbert conditional permutation upper bound.
- Full simple spectra and all required harmonic/local moments for permutation
  strategies, plus the literal computational-MUB spectral obstruction.
- The manuscript's actual source coefficient matrices: exact Weyl/Fourier
  identities, canonical positive-modulus factorization and inverse, unitarity,
  order d, full simple spectra, genuine spectral PVMs, and an actual normalized
  source strategy attaining the claimed first-family value.
- Actual Qqa inclusion in Qqc for finite input alphabets. The proof constructs a
  positive word-moment kernel from varying physical realizations, realizes its
  GNS Hilbert space, extends bounded projection actions to the completion, proves
  every PVM/cross-party relation, and recovers the limiting behavior. It does not
  assume a limiting realization or closedness of the commuting model.

The original exact values, biased maximizers, supported multiplicity rigidity,
binary benchmark/privacy/minimality, one-input construction, adversarial guessing
bounds, finite-POVM maximum/nesting, and settings-table/entropy results are retained.
The complete claim map is [COVERAGE.md](../COVERAGE.md).

## Verification evidence

The frozen source inventory contains 106 Lean files, 1,387 named theorems and
1,852 named declarations in total. The generated axiom-query module explicitly
imports every source module. The normal build also elaborates 100 expanded
statement examples.

All 63 Python tests of the reporting/scanning machinery passed before the frozen
run. All five Lean acceptance and twenty rejection controls passed individually;
their original 49 example statements are preserved. Rejection controls were
repaired to reach the intended proof failure: unknown names/imports, syntax
errors, crashes and resource exhaustion are rejected by the runner. Negative
proof-attempt failure alone is not asserted to prove every target's negation.

The final clean run `20260915T041758190218Z` completed successfully in
1839.3 seconds using `Lean (version 4.19.0, arm64-apple-darwin23.6.0, commit 6caaee842e94, Release)`. All
67 recorded commands had the required exit status. Both the clean
build and the standalone collection produced exactly the same 1,852 axiom
reports, with only `propext`, `Classical.choice`, and `Quot.sound`. No admissions,
custom axioms or native proof-evaluation axioms are present in the audited dependencies.

All five acceptance controls and twenty intended proof rejections passed again
against the clean build. The 100 expanded statement examples elaborated. Compiler
commit, all nine locked dependency revisions, manuscript identity, command-log
hashes and protected source fingerprints passed the final checks.

See [the complete command/log receipt](final_clean_run/run.json),
[the consolidated result](RESULT.json), and [the actual clean build log](final_clean_run/022.log).
Historical root handoff reports and `SOURCE_HASHES.sha256` describe the received
snapshot; use this receipt and `reference/source_inventory.json` for the repaired
snapshot.

## What “full formalization” means here

The coverage goal is the paper's mathematical result statements in its stated
physical models, with explicit witnesses and definitions. It is not a literal
translation of every prose derivation or of all cited literature.

The computational-MUB theorem has an alternative, stronger constant-diagonal
positivity proof; its intermediate Toeplitz/SVD calculation is not separately
translated. The general polar identity starts with a supplied polar decomposition
and its defining properties, as the lemma states. It does not construct arbitrary
polar decompositions or their strong-limit/von Neumann representations. The
specific attaining source pencil's polar factor and inverse are constructed.

External self-testing theorems and an isometry transport from those papers are
outside this companion. Its displayed physical probability tables are proved
directly. Novelty, priority, bibliography, open classifications and unknown
optimal adversarial guessing values are not converted into formal claims.

The distinctions needed for interpreting the results are preserved: a guessing
lower bound is not an exact worst-case optimum; observed entropy is not
adversarial entropy; supported rigidity is not self-testing; finite-Eve POVM
maxima do not assert a maximizing global realization. The Qqa/Qqc closure theorem
uses finite input sets, covering the paper's scenarios, with no finite Hilbert
dimension restriction.

Independent final reviews found no remaining gap in the mapped mathematical
claims. See [source/polar final review](SOURCE_POLAR_FINAL_ADDENDUM.md),
[closure review](CLOSURE_SEMANTIC_AUDIT.md), and
[semantic coverage audit](SEMANTIC_AUDIT.md). Older reports retain their dated
intermediate gap lists; these final reviews and the final clean receipt supersede
those earlier statuses.

## Reproduction

From the companion directory, with Lean 4.19.0 available:

```sh
python3 scripts/check.py --bootstrap --manuscript ../main.tex
```

Omit `--bootstrap` if all exact pinned dependencies and their cache are installed.
The checker removes the companion build directory, verifies the full build,
runs controls, checks every named declaration's transitive axioms, and confirms
the protected inputs and dependency sources did not change. It is not a
from-source bootstrap of Lean itself.

The automated runner deliberately leaves `formal_endpoint_certified` false:
compiler success alone cannot perform the separate manuscript-correspondence
review. The combined evaluation here distinguishes that semantic review from
the machine-checked proof and control receipts.
