# GitHub release checklist

This checklist is not used for the direct Zenodo version 1.0.0 deposit.  Do
not create a GitHub release for that deposit: the project is a subdirectory of
a monorepository, and an integrated GitHub--Zenodo release could create a
duplicate or archive the wrong scope.

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
- For a future deliberately GitHub-integrated release, confirm the automatic
  Zenodo deposition completed before using its DOI.
