# Direct Zenodo release

This directory implements the direct Zenodo release path for version `1.0.0`.
It is separate from `release/build_release.py envelope`, which remains a
journal-package gate and is deliberately unsuitable for this first Zenodo
preprint deposit.

The generated folder has two parts:

- `UPLOAD_THESE_FILES/` contains the exact Zenodo upload allowlist.
- `ZENODO_METADATA_GUIDE.md` stays local and contains fully expanded,
  copy-and-paste metadata and post-upload checks.

The DOI is assigned by Zenodo when the record is published.  It is
authoritative record metadata and is intentionally not predicted or embedded
in the immutable version `1.0.0` bytes.  A later DOI-bearing manuscript would
be a new version, commit, tag, manifest, and checksum set.

The builder requires:

1. a clean K3P project at the exact pushed `main` commit;
2. canonical compact and full archives bound to that commit;
3. both final-commit source-reproduction reports and transcripts;
4. a freshly built, integrity-checked referee folder; and
5. the local annotated tag `k3p-level2-identifiability-v1.0.0` pointing to
   that commit.

It creates no network record, DOI, GitHub release, or Zenodo upload.

```sh
.venv/bin/python release/zenodo/build_zenodo_upload_set.py \
  --referee-package release/dist/K3P_Level2_Independent_Referee_Package_v1.0.0

.venv/bin/python release/zenodo/verify_zenodo_upload_set.py
```

After pushing the annotated tag, the mandatory final prepublication check is:

```sh
.venv/bin/python release/zenodo/verify_zenodo_upload_set.py \
  --require-remote-tag
```

That mode also refuses publication on a date other than the manifest's
Zenodo publication date.  If publication is delayed, update the date and make a
new commit, tag, manifest, and checksum set before publishing.

The generated upload set contains no journal cover letter or journal portal
package.  Those are not mathematical evidence and are not part of the direct
preprint deposit.
