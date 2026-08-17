# Publish the exact v1.1.2 replay assets

This is a human-authorized release-engineering step, not journal submission.
The release tag and source commit must already be public before these commands
are run.

From the monorepository root, stage the seven manifest-covered assets in one
flat temporary directory and verify them exactly as a public downloader will:

```bash
stage_dir=$(mktemp -d)
cp s_tc_jc_landmark_closure/release_artifacts/stc_jc_sharp_boundary_reproducibility.tar.gz "$stage_dir/"
cp s_tc_jc_landmark_closure/release_artifacts/stc_jc_sharp_boundary_reproducibility.tar.gz.sha256 "$stage_dir/"
cp s_tc_jc_landmark_closure/release_artifacts/RELEASE_ENVELOPE.json "$stage_dir/"
cp s_tc_jc_landmark_closure/release_artifacts/FINAL_RELEASE_ENGINEERING_REPORT.md "$stage_dir/"
cp s_tc_jc_landmark_closure/release_artifacts/clean_clone_transcripts/*.log "$stage_dir/"
cp s_tc_jc_landmark_closure/release_artifacts/RELEASE_ASSET_SHA256SUMS "$stage_dir/"
(cd "$stage_dir" && shasum -a 256 -c RELEASE_ASSET_SHA256SUMS)
```

Create the GitHub Release and upload the exact assets:

```bash
gh release create stc-jc-sharp-boundary-v1.1.2 \
  --repo AlecKriebel/Math \
  --title "STC/JC sharp-boundary reproducibility v1.1.2" \
  --notes-file s_tc_jc_landmark_closure/release/PUBLIC_RELEASE_ASSETS.md \
  s_tc_jc_landmark_closure/release_artifacts/stc_jc_sharp_boundary_reproducibility.tar.gz \
  s_tc_jc_landmark_closure/release_artifacts/stc_jc_sharp_boundary_reproducibility.tar.gz.sha256 \
  s_tc_jc_landmark_closure/release_artifacts/RELEASE_ENVELOPE.json \
  s_tc_jc_landmark_closure/release_artifacts/RELEASE_ASSET_SHA256SUMS \
  s_tc_jc_landmark_closure/release_artifacts/FINAL_RELEASE_ENGINEERING_REPORT.md \
  s_tc_jc_landmark_closure/release_artifacts/clean_clone_transcripts/verify_quick.log \
  s_tc_jc_landmark_closure/release_artifacts/clean_clone_transcripts/verify_full.log \
  s_tc_jc_landmark_closure/release_artifacts/clean_clone_transcripts/verify_regenerate_all.log
```

Then run the bounded post-upload verifier, which resolves the annotated tag,
downloads all eight assets, checks the exact asset set and flat manifest,
opens the archive, validates its metadata and source marker, and checks every
clean transcript:

```bash
python s_tc_jc_landmark_closure/reproducibility/verify_public_release.py
```

Capture its `PUBLIC_RELEASE_VERIFIED` output in the final release transcript.

If the release already exists, use `gh release upload ... --clobber` only
after checking that the tag still peels to the exact sealed source commit.
