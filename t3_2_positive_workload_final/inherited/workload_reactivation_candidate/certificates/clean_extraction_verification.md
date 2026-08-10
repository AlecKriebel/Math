# Clean extraction verification

The release archive was extracted to a fresh temporary directory and the
following completed successfully:

- `./verify_release.sh`;
- all 12 pytest tests;
- direct C++ atlas;
- independent Python atlas;
- clean-room third atlas;
- deterministic two-pass PDF build;
- stable two-pass verification report;
- `sha256sum -c certificates/MANIFEST.sha256`.

Released content hashes:

- PDF: `e6498b153702dd1e6689f32470f42c3f8150c0a796c5679cac6114d0f3a2eb18`
- verification report: `ea432bd8507e66543fc0af8995cfdcea33f4f00ab3cdbf4a41903614a9a25aae`
- independent verification: `3027479c169f0acdb320789396008903b0d6d7fdee4b9ad8b393fbdd42f7b503`
