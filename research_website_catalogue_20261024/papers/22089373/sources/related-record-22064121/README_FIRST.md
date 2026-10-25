# Computer-assisted proof certificate bundle

This is the reviewer-facing proof object for **Strong Tree-Childness Is a
Sharp Generic-Identifiability Boundary for Level-2 Jukes--Cantor Networks**.
It contains the active mathematical inputs, the frozen finite atlases, every
exact certificate used by the paper, and both the primary and separately
implemented replay programs.  It deliberately excludes development history,
superseded claims, referee prose, manuscript build products, and release
engineering.

The finite decorated-relation theorem (Theorem 6.3) is the sole finite
machine-certified dependency in the positive classification proof.  This
bundle exposes its complete chain:

```text
primitive graph and invariant inputs
  -> primary generators
  -> frozen canonical directed-relation atlases
  -> exact pullback/sign/rank/restoration/probe certificates
  -> separately implemented replay verifiers
```

## One entry point

After extracting the archive, run:

```bash
bash verify.sh quick
bash verify.sh full
bash verify.sh regenerate-all
```

The archive's external SHA-256 authenticates the complete compressed object.
After extraction, `quick` authenticates every proof-payload file, checks that
`SHA256SUMS` is the exact projection of `ACTIVE_MANIFEST.json`, and checks the
frozen theorem summaries.
`full` replays every load-bearing exact component certificate with the
primary and separately implemented programs, including the complete
arbitrary-word cut reduction and a clean-room graph/switching replay of its
reduced palette.  `regenerate-all` additionally
rebuilds the complete relation, restoration, and probe streams from the
committed primitive graph and invariant inputs, compares them with the frozen
proof records, and repeats that regeneration in a second isolated copy.
Before running their producers it also deletes all three independent n=3
generator outputs and all six four-port signature/crosswalk/quotient outputs;
no-op, partial, or stale-output producers therefore fail closed.  The
mathematical gates work in temporary copies.  On first use `verify.sh` adds
only a local `.venv` alongside the authenticated payload; it does not alter
any authenticated proof-payload file.

The scripts create a local `.venv` on first use.  That first installation
requires either access to the Python package index or a local wheel cache;
after the pinned dependencies are installed, the mathematical checks make no
network requests.  The scripts do not contact an editor, upload data, choose
a license, create a DOI, or alter files outside the extracted directory and a
temporary work directory.

## What is authoritative

- `ACTIVE_MANIFEST.json` inventories and authenticates every proof-payload
  file, and `SHA256SUMS` is checked as its exact projection.  The external
  archive SHA-256 authenticates those two metadata files and the archive
  container.  None of these integrity checks replaces the mathematical
  row-level checks.  The manifest also records the exact 40-hex source commit,
  certifies that the builder observed a clean project tree, and records the
  SHA-256 commitment of the complete pre-seal payload.  During sealing the
  builder independently re-prepares that payload from the clean commit,
  rejects any byte or executable-mode difference from the requested stage,
  and archives only the fresh reconstruction.  The extracted verifier
  recomputes the payload commitment and checks every recorded byte and mode;
  the external clean-checkout sealing transcript is what attests the source
  commit named in the manifest.  The extracted verifier alone checks the
  commit's syntax and internal binding, not existence in a remote Git
  repository; the repository-level release gate checks that Git object and
  cross-checks it against the external envelope.
  Both preparation invocations use Python isolated mode with `site` startup
  disabled, and the detached child receives no inherited Python startup path,
  user-site configuration, or global `sitecustomize` hook.
- `atlas/ATLAS_EVIDENCE_BINDINGS.jsonl.gz` is the authoritative theorem-row
  map.  Every restoration row points to
  `RESTORATION_CLOSURE_BINDINGS.jsonl.gz`; every direct residual equality row
  points to `DIRECT_ANCHOR_CLOSURE_BINDINGS.jsonl.gz`; and every equality
  terminal in a restoration tree points onward to
  `COMPACT_PATH_CLOSURE_BINDINGS.jsonl.gz`.  Those content-addressed closure
  rows name every restoration state, compact path, transport, witness,
  polynomial, and direct one-/two-port relation used to discharge the theorem
  row.  The verifier reconstructs all four streams independently of the
  frozen index.
- `atlas/ATLAS_INDEX.csv.gz` is a human-readable projection of that evidence
  map.  The verifier regenerates both and checks the projection exactly.
- `THEOREM_CERTIFICATE_CROSSWALK.md` is the minimal theorem-to-file map.
- `REGENERATION_MAP.md` states exactly which program reconstructs each
  logical proof object.
- `PROOF_BOUNDARY.md` separates human proofs from finite computations.
- `expected_outputs/expected_counts.json` records the exact finite-universe
  commitments. Complete run transcripts are distributed beside the archive
  so they do not become self-referential proof inputs.

The broader development snapshot is useful for provenance, but it is not
needed to check the theorem and is not part of this bundle.

The active sharpness material is isolated under `sharpness/omega/` and
`sharpness/theta/`.  Each contains only the immutable machine-readable input,
the producer engine needed for exact replay, and a separately implemented
clean-room verifier.  No development audit directory or superseded sharpness
claim is part of the bundle.

## Scope and licensing

This archive contains only active proof inputs, generated certificates, and
their verifiers. It contains no manuscript, referee report, research log,
superseded theorem, or release-engineering workspace. The code license is in
`LICENSES/`; the depositor separately selects the Zenodo record/data license
at publication.
