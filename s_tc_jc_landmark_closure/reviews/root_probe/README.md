# Root/probe review package

This directory is self-contained except for read-only access to the audited
repository inputs.  The clean verifiers use only the Python standard library
and other files in this directory; they never import `primary` graph code.

Run the complete replay from this directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify_all.py
```

A successful structural replay may report
`hard_cover_contract_satisfied=false`; that reproduces the final
`UNRESOLVED` theorem verdict rather than indicating a verifier failure.

The replay regenerates:

- `root_probe_certificate.json`;
- `probe_coherence_certificate.json`;
- `incoming_coverage_certificate.json`;
- `parameter_submersion_certificate.json`;
- `redstar_partition_certificate.json`; and
- `primary_artifact_audit.json`.

`verify_primary_artifacts.py` is a comparison-stage clean reader: it parses
primary JSON and source text but imports no primary module.  `REVIEW.md` gives
the mathematical verdicts and `counterexamples/` preserves the exact boundary
cases.  `INPUTS.sha256` and `MANIFEST.sha256` bind the final audited inputs and
review outputs.
