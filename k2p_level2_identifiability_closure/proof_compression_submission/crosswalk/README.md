# Submission crosswalk and referee-bundle recipe

This directory binds each theorem layer to exact authoritative, producer,
replay, mutation, environment, and runtime fields.  The crosswalk is a
submission aid.  It does not modify or supersede the frozen principal-domain
release lock.

From the project root, replay the package with:

```sh
python3 proof_compression_submission/crosswalk/build_theorem_artifact_crosswalk.py --check
python3 proof_compression_submission/crosswalk/build_revised_referee_bundle.py --check
python3 proof_compression_submission/crosswalk/check_revised_referee_bundle.py
python3 proof_compression_submission/crosswalk/test_crosswalk_bundle_mutations.py --check
```

The revised manifest includes the complete 374-file transitive frozen
evidence ledger and 73 submission artifacts, including the named clean-replay
reports, final PDFs, and build logs. Any included source edit makes both the
primary and independent manifest checks fail. Reseal only after the submission
sources are final:

```sh
python3 proof_compression_submission/crosswalk/build_revised_referee_bundle.py --write
python3 proof_compression_submission/crosswalk/check_revised_referee_bundle.py
```

The final archive is requested explicitly after the manifest is sealed. The
builder fixes member order, timestamps, modes, prefix, compression method, and
level:

```sh
python3 proof_compression_submission/crosswalk/build_revised_referee_bundle.py \
  --check --archive \
  proof_compression_submission/output/K2P_Principal_D_Plus_Referee_Package_20260822.zip
```

Run `unzip -t` and compare the external `.sha256` sidecar after construction.
The sidecar is deliberately outside the ZIP, avoiding a self-referential hash.

The manifest remains labelled
`DRAFT_PC_PARTIAL_PENDING_HUMAN_METADATA`. The detached clean full replay is
already measured and bound: 35 layers passed in 5,172.89 seconds. Corresponding
email, contribution approval, funding, competing interests, licenses,
immutable-tag, and DOI decisions require human confirmation.
