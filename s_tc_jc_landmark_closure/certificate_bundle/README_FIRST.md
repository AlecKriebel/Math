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
primary and separately implemented programs.  `regenerate-all` additionally
rebuilds the complete relation, restoration, and probe streams from the
committed primitive graph and invariant inputs, compares them with the frozen
proof records, and repeats that regeneration in a second isolated copy.  The
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
  row-level checks.
- `atlas/ATLAS_EVIDENCE_BINDINGS.jsonl.gz` is the authoritative row-level
  map.  For every canonical three-outgoing relation and every four-outgoing
  survivor it binds the decorated graph relation, direction, disposition,
  exact evidence, transports when applicable, and replay program.
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

## Scope and licensing

This archive contains only active proof inputs, generated certificates, and
their verifiers. It contains no manuscript, referee report, research log,
superseded theorem, or release-engineering workspace. The code license is in
`LICENSES/`; the depositor separately selects the Zenodo record/data license
at publication.
