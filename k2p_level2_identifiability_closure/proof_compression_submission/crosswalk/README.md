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

The revised manifest includes the complete 370-file transitive frozen
evidence ledger and every current submission source outside build-output and
cache directories.  Any source edit makes both the primary and independent
manifest checks fail.  Reseal only after the submission sources are final:

```sh
python3 proof_compression_submission/crosswalk/build_revised_referee_bundle.py --write
python3 proof_compression_submission/crosswalk/check_revised_referee_bundle.py
```

No large archive was created in this pass.  After the manifest is final, an
archive can be requested explicitly; the builder fixes member order,
timestamps, modes, prefix, compression method, and level:

```sh
python3 proof_compression_submission/crosswalk/build_revised_referee_bundle.py \
  --check --archive /explicit/output/path/k2p_submission_referee.zip
```

The manifest remains labelled
`DRAFT_PC_PARTIAL_PENDING_HUMAN_METADATA`.  Corresponding email, funding,
competing interests, licenses, repository/tag/DOI decisions, and final clean
full-replay performance measurements require human confirmation.
