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

`quick` authenticates every byte and checks the frozen theorem summaries.
`full` replays every load-bearing exact component certificate with the
primary and clean-room implementations.  `regenerate-all` additionally
rebuilds the theorem-forced normalized relation, restoration, and probe
records from the committed primitive inputs.  Every mode works in a temporary
copy so the extracted proof object remains immutable.

The scripts create a local virtual environment on first use.  They do not
contact an editor, upload data, choose a license, create a DOI, or alter files
outside the extracted directory and a temporary work directory.

## What is authoritative

- `ACTIVE_MANIFEST.json` and `SHA256SUMS` authenticate the complete bundle.
- `atlas/ATLAS_INDEX.csv.gz` gives one row for every canonical
  three-outgoing relation and every four-outgoing survivor.
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
