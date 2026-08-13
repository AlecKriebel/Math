# Adversarial release review

## Verdict

**VERIFIED.** The tracked compact n3 and theta2-n4 probe shards now have a
compact-only semantic verifier.  The release no longer needs any untracked
verbose `probe_extension_*` stream for these families.

## What was checked

- Every external runtime input is git-tracked and byte-locked (50 files).
- Both four-shard ranges are gapless and exhaustive: `[0,144)` and `[0,132)`.
- All 276 path records and 269,730 packed relation cells are decoded exactly.
- Parent graphs, admissible arcs, deterministic insertions, and exact
  deletion to parents are regenerated.
- Displayed switchings, descendant masks, zero-sum JC descriptors, invariant
  pullbacks, sparse polynomial bodies, and strict open-cube signs are
  regenerated from graphs.
- Labelled isomorphism and ordinary-`T` transports are independently solved;
  every child transport restricts to its parent transport.
- All witness, transport, and polynomial libraries are orphan-free.
- All four compact classes are exercised by n3.
- The largest relation has ten ports, exactly the advertised bound.

The semantic implementation imports no module under `primary`.  It reuses
only the already committed clean-room graph/Fourier engine in
`reviews/compact_probe_format/final_n4_cleanroom/engine.py` and its independent
triangle/sign extension in `final_n3_cleanroom/engine_n3.py`.  Frozen invariant
coefficient data are vendored in this package and every use is regenerated
against the bound graph.

## Mutation sensitivity

Outer file hashes are deliberately bypassed for the mutation suite.  The
semantic checks reject all nine mutations:

1. delete a path;
2. duplicate a path;
3. alter an admissible arc;
4. alter arc order;
5. move a valid witness to the wrong relation;
6. move a valid transport to the wrong relation;
7. change a relation class;
8. make an ordinary-`T` child transport inconsistent with its parent;
9. alter path/root provenance.

The exact first rejection categories are in `certificates/mutation_tests.json`.

## Reproduction

From the project directory:

```bash
PYTHON_BIN=../.venv/bin/python \
  bash reviews/compact_probe_clean_clone_gate/verify_quick.sh

PYTHON_BIN=../.venv/bin/python \
  bash reviews/compact_probe_clean_clone_gate/verify_full.sh
```

After this package is committed, the following extracts `git archive HEAD`
to a fresh temporary directory and executes both gates there:

```bash
PYTHON_BIN=/absolute/path/to/python-with-networkx-and-sympy \
  bash reviews/compact_probe_clean_clone_gate/verify_archive_clean.sh
```

The full replay is sequential to stay within the 16 GB host limit.
