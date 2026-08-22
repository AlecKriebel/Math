# Human Zenodo deposit sequence

These are instructions for the human author.  No command below uploads a file,
publishes a record, chooses a license, or submits a manuscript.

1. Create a Zenodo draft and reserve its DOI.
2. From a clean project checkout, insert that exact DOI:

   ```bash
   python reproducibility/test_finalize_zenodo_doi.py
   python reproducibility/finalize_zenodo_doi.py --doi 10.5281/zenodo.<number>
   ```

3. Review the DOI-only changes, rebuild all article and journal packages, and
   commit the DOI-bearing source state.
4. From that clean commit, build and seal the curated archive.  The complete
   `release_artifacts/` tree is ignored build output.  Sealing independently
   prepares a second payload from the clean commit, requires exact byte and
   executable-mode equality, and archives only that fresh reconstruction:

   ```bash
   python -I -S reproducibility/build_certificate_bundle.py prepare
   python -I -S reproducibility/build_certificate_bundle.py seal
   ```

5. Run, without interruption, from the staged archive root:

   ```bash
   bash release_artifacts/stc_jc_sharp_boundary_atlas_certificates_v1.1.7/verify.sh quick
   bash release_artifacts/stc_jc_sharp_boundary_atlas_certificates_v1.1.7/verify.sh full
   bash release_artifacts/stc_jc_sharp_boundary_atlas_certificates_v1.1.7/verify.sh regenerate-all
   ```

6. Preserve the complete source-commit-bound output of those commands in
   `release_artifacts/certificate_bundle_logs/`.
7. Upload exactly the files listed in `PERSISTENT_ARCHIVE_CHECKLIST.md` to the
   Zenodo draft.  Confirm every filename, byte count, and SHA-256 against
   `CERTIFICATE_BUNDLE_ENVELOPE.json`.
8. Publish the Zenodo record manually, download the public archive, and run
   `reproducibility/verify_certificate_zenodo_release.py` on that download.
9. Only after the public DOI resolves and the download verifies, submit the
   same DOI-bearing article and supplement to bioRxiv.  The small verifier ZIP
   is a navigation capsule, not the proof object.

The older GitHub-release instructions and omnibus development archive are
superseded provenance only; they are not required by the active theorem.
