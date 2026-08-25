# GitHub release checklist

- Do not create a release until every local acceptance gate passes.
- Confirm `main` is clean, pushed, and identical to the source commit in the
  release envelope.
- Confirm the proposed local tag points exactly at that commit and is recorded
  in the envelope.  Then have Alec push it and verify immutability on the
  remote; the local tooling never creates, moves, pushes, or proves remote tags.
- Attach every asset listed in `RELEASE_ASSET_SHA256SUMS` plus the envelope and
  checksum list.
- Do not announce a DOI before Zenodo has actually minted it.
- Do not select or state a code, data, or manuscript license without explicit
  authorization from Alec.
- After upload, download every asset and compare its SHA-256 locally.
- Confirm the automatic Zenodo deposition completed before using its DOI.
