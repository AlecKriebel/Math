# Public release assets

The authoritative external release location is:

- tag: `stc-jc-sharp-boundary-v1.1.4`
- release page: <https://github.com/AlecKriebel/Math/releases/tag/stc-jc-sharp-boundary-v1.1.4>

It is active only when `reproducibility/verify_public_release.py` returns
`PUBLIC_RELEASE_VERIFIED`.  The release page then carries the exact eight
non-Git assets needed for a complete replay:

1. `stc_jc_sharp_boundary_reproducibility.tar.gz`
2. `stc_jc_sharp_boundary_reproducibility.tar.gz.sha256`
3. `RELEASE_ENVELOPE.json`
4. `RELEASE_ASSET_SHA256SUMS`
5. `FINAL_RELEASE_ENGINEERING_REPORT.md`
6. `verify_quick.log`
7. `verify_full.log`
8. `verify_regenerate_all.log`

`RELEASE_ENVELOPE.json` binds the immutable source commit, the deterministic
archive, and all three clean-checkout transcripts.  The flat
`RELEASE_ASSET_SHA256SUMS` covers the other seven downloaded assets by
basename, including the envelope, so this command works from one download
directory:

```bash
shasum -a 256 -c RELEASE_ASSET_SHA256SUMS
```

The manifest cannot contain its own digest and is therefore the downloaded
trust anchor; its hash is recorded in the machine-readable
`PUBLIC_RELEASE_VERIFIED` verdict and final release transcript. A reader can
either verify the annotated tagged source
checkout or download all eight assets and run the extracted-archive verifier
described in the engineering report.

The files formerly stored directly under `release/` certified an older
18-page manuscript. They are historical only and now live under
`history/superseded_release_evidence/outcome_p_2026-08-13/`.
