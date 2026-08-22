# Version 1.2.4 reproduction record

**Release date:** 22 August 2026
**Canonical tag:** `bimolecular-positive-recurrence-v1.2.4`
**Verifier component:** unchanged Version 1.2.0

This record deliberately does not embed a supposedly final commit hash inside
that same commit. The annotated tag is the immutable identifier, and the exact
commit is obtained without ambiguity by:

```bash
git rev-parse bimolecular-positive-recurrence-v1.2.4^{commit}
```

The complete replay is executable:

```bash
git clone https://github.com/AlecKriebel/Math.git
cd Math
git checkout --detach bimolecular-positive-recurrence-v1.2.4
bimolecular_positive_recurrence_submission_v1_2_4/validation/replay_release.sh
```

The replay prints the resolved commit and exact tag, Python/Tectonic/platform
versions, and SHA-256 values for the canonical report, manifest, four PDFs,
and release ZIP. It then requires:

- all 57 verifier tests and seven release-tool safety/provenance tests to pass;
- two regenerated reports and all three committed report copies to be
  byte-identical;
- every durable package file to match both manifest copies;
- all four rebuilt PDFs to match their committed bytes;
- a newly generated release archive to match the committed archive; and
- the package/archive Git status to remain clean.

Before those checks begin, the replay fails unless the checked-out commit is
identified by the literal annotated tag
`bimolecular-positive-recurrence-v1.2.4`. Regression tests cover an untagged
HEAD, a wrong exact tag, and a lightweight tag with the expected name.

Continuous integration repeats the verifier on CPython 3.11, 3.12, 3.13, and
3.14; manifest/archive checks on 3.11 and 3.14; and the four-PDF build twice
with Tectonic 0.16.9. The tagged-release job retains its console output as a
GitHub Actions artifact. The canonical inputs, tool versions, bundle URL and
digest, timestamp, and ZIP format are recorded in `REPRODUCIBILITY.env`.

The Version 1.2.3 tag, archive, manifests, PDFs, and hosted replay remain
unchanged. This patch release carries the verifier component byte-for-byte and
changes reader-facing exposition, current literature and AI-use dates,
submission and preservation guidance, tag-provenance enforcement, and outer
release records. The theorem and proof dependencies are unchanged.
