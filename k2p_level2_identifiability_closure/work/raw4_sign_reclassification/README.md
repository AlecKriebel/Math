# Corrected raw-four full-map terminal overlay

This package replaces the revoked rooted `tree_sunlet` classification of
16,974 raw four-port rows.  The historical label is used only to select the
affected rows from the immutable raw ledger.  Every selected row is re-proved
directly on the original K2P Fourier maps by a transported three-leaf
invariant:

\[
T_i=V^2X_g-X_s^2Y_gZ_g.
\]

For each row, the target pullback is coefficientwise zero and the source
pullback is strictly negative.  Strict negativity is certified by exact
tensor-product Bernstein coefficients on the open parameter cube, which is
stronger than negativity on the principal positive K2P domain.

## Frozen result

- 16,974 historical rows selected exactly once;
- 16,974 corrected exact exclusions;
- 122 exact ordered labelled graph-pair classes;
- 678 exact K2P descriptor-pair classes;
- 8 exact polynomial relation classes;
- zero labelled-isomorphism or ordinary-triangle conflicts;
- zero unresolved rows and zero new restoration obligations; and
- corrected restoration-parent total: 997.

The earlier `raw4_sign_reclassification.json` is deliberately retained as an
`INCOMPLETE` diagnostic checkpoint.  Its point-rank labels are not promotion
claims.  The authoritative replacement is
`raw4_corrected_terminal_ledger.json`.

## Reproduction

From the repository root, using the supplied Python environment:

```sh
.venv/bin/python work/raw4_sign_reclassification/build_raw4_corrected_terminal_ledger.py
.venv/bin/python work/raw4_sign_reclassification/verify_raw4_corrected_terminal_ledger.py
.venv/bin/python -B work/raw4_sign_reclassification/mutation_tests.py \
  --output /tmp/k2p-raw4-full-map-mutations.json
```

The builder searches all triples and orientations and does not import the
adversarial review implementation.  The verifier independently recomputes the
primitive rows, exact semi-directed relations, canonical graph and descriptor
classes, transported full-map pullbacks, and Bernstein tensors.  Its
Bernstein replay uses the closed multivariate coefficient formula rather than
the builder's successive axis transforms.

## Artifacts

- `raw4_corrected_terminal_ledger.json`: authoritative corrected overlay;
- `raw4_corrected_replay_certificate.json`: independent exact replay report;
- `raw4_mutation_certificate.json`: fail-closed mutation report;
- `build_raw4_corrected_terminal_ledger.py`: graph-derived builder;
- `verify_raw4_corrected_terminal_ledger.py`: independent verifier; and
- `mutation_tests.py`: omission, reassignment, transport, polynomial,
  Bernstein, descriptor, and optimized-mode mutations.  The suite requires a
  clean production-verifier baseline, exact per-case diagnostics and exit
  status, no failure report, and caller-owned output outside the source tree.
  It also contains negative controls for unrelated crashes, imports, timeouts,
  signals, wrong exits, wrong diagnostics, and stale success artifacts.
