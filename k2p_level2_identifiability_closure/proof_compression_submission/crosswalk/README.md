# Submission crosswalk and referee-bundle recipe

This directory binds each theorem layer to exact authoritative, producer,
replay, mutation, environment, and runtime fields.  The crosswalk is a
submission aid.  It does not modify or supersede the frozen principal-domain
release lock.

The builder always reads the current qualified lock.  Earlier lock hashes in
dated research logs remain historical provenance; the theorem and finite
classification universe were unchanged by the later evidence-qualification
reseal.

From the project root, replay the package with:

```sh
python3 proof_compression_submission/adversarial_review/audit_article_sources.py --check
python3 proof_compression_submission/crosswalk/build_theorem_artifact_crosswalk.py --check
python3 proof_compression_submission/crosswalk/build_revised_referee_bundle.py --check
python3 proof_compression_submission/crosswalk/check_revised_referee_bundle.py
python3 proof_compression_submission/crosswalk/test_crosswalk_bundle_mutations.py --check
```

The revised manifest reconstructs the complete transitive frozen-evidence
ledger from the current promotion-ready release lock and records its exact
file count, byte count, and content root. It also includes the named
clean-replay reports, final PDFs, build logs, and all submission sources. The
archive also copies the portable content ledger, its fail-closed checker,
and its reader README as explicit execution dependencies outside the
`proof_compression_submission/` tree.

No release hash, layer count, runtime, or memory value is hardcoded: the builder
and independent checker derive and cross-check those fields from the final
lock and detached clean-replay telemetry. Any included source edit makes both
checks fail. Reseal only after the release lock, clean replay, PDFs, and
submission sources are final:

```sh
python3 proof_compression_submission/adversarial_review/audit_article_sources.py --write
python3 proof_compression_submission/crosswalk/build_theorem_artifact_crosswalk.py
python3 proof_compression_submission/crosswalk/build_revised_referee_bundle.py --write
python3 proof_compression_submission/crosswalk/check_revised_referee_bundle.py
```

The final archive is requested explicitly after the manifest is sealed. The
builder fixes member order, timestamps, modes, prefix, compression method, and
level:

```sh
python3 proof_compression_submission/crosswalk/build_revised_referee_bundle.py \
  --check --archive \
  proof_compression_submission/output/K2P_Principal_D_Plus_Referee_Package_20260828.zip
```

Run `unzip -t` and compare the external `.sha256` sidecar after construction.
The sidecar is deliberately outside the ZIP, avoiding a self-referential hash.

The final manifest is labelled `SUBMISSION_READY_PC_PARTIAL`. It binds the
approved email, sole-author contribution statement, funding and
competing-interests declarations, CC BY 4.0 paper/data license, MIT code
license, and designated versioned annotated source tag
`k2p-same-biorxiv-v1.0.4`. The tag-object and peeled-commit identifiers are
external release metadata, avoiding a self-referential source binding. The
manifest also records the explicit release boundary: this package neither
creates nor claims a GitHub Release, Zenodo deposit, or DOI; the author will
perform any such release actions separately.
