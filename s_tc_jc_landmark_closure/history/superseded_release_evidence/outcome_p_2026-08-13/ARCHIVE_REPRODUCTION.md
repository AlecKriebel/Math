# Deterministic Outcome-P archive

Status: **VERIFIED**

The release archive contains the sealed positive-classification project and
the frozen weak-class sharpness package at exact commit
`35291bba72f52ac800e99ea797ddad20d9852a67`.

From the repository root, regenerate it with:

```bash
mkdir -p s_tc_jc_landmark_closure/release
git archive --format=tar \
  35291bba72f52ac800e99ea797ddad20d9852a67 \
  s_tc_jc_landmark_closure s_tc_jc_sharp_boundary \
  | gzip -n \
  > s_tc_jc_landmark_closure/release/stc_jc_landmark_closure_outcome_p.tar.gz
shasum -a 256 \
  s_tc_jc_landmark_closure/release/stc_jc_landmark_closure_outcome_p.tar.gz
```

Expected output:

```text
db481d35c1393827b2ea010509e551fcfe64845413f2f9c87ca3dc559a2d0ce8
```

The resulting archive is 336,143,114 bytes.  It is deliberately ignored as
an ordinary Git blob because of its size and is intended to be attached as a
repository release asset.  The checksum sidecar, this recipe, and the clean
replay transcripts are tracked.
