# Version 1.0.1 deployment verification

Verified 2026-09-23T13:51:39.034995+00:00. Requested adversarial review and global-update task: **100% complete**.

- Revision commit: `6c23a59bb95b9ead3afdc7f824c7f9730b29e80c` on main.
- Successful GitHub Pages run: https://github.com/AlecKriebel/Math/actions/runs/35869708450
- Deployed descendant: `cd8714c8055d7957c650f0c8b764c6b602bc665d`.
- Public page: https://aleckriebel.github.io/Math/papers/odd-part-slow-variation/
- All nine tested public files return HTTP 200 and match the local publication files byte for byte: HTML, PDF, LaTeX, both archives, metadata, upload guide, preprint-readiness record and verification report. Exact hashes are in `public-download-checks-v1.0.1.json`.
- Final paper, PDF and verifier match the hashes recorded by the second fresh reviewer. No scientific edits occurred afterward.
- Source and upload archives have validated manifests and reconstruct byte-for-byte from extracted source. Both ordinary and optimized verifier modes pass.
- All three updated PDF pages were visually checked. The Availability URL is a live PDF link, and title/author metadata is present.
- Two fresh adversarial rounds completed. Round 1 found two delivery issues, now fixed; round 2 found no actionable issues. The paper is ready as a preprint of the printed slow-variation question, with priority qualifications preserved.
- No journal-submission work, immutable release, Zenodo deposit, DOI creation or external contact was performed.

This operational record is outside the frozen research ZIP; it does not modify the approved paper or its evidence.
