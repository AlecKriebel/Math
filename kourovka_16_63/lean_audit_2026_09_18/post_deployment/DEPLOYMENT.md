# Verified public deployment

Timestamp: 2026-09-19T05:01:14.100265+00:00.

Checkpoint: **100% of the repair/build/audit/publication task**. The complete
finite-group formalization remains unfinished; the four missing mathematical
developments are listed in the verification report. This percentage does not
measure completeness of the mathematical formalization.

- Publication commit: `e0e3be1325a627a3ee15948ab43a9c2e1c464b12` on `main`.
- GitHub Pages workflow: [https://github.com/AlecKriebel/Math/actions/runs/35422707150](https://github.com/AlecKriebel/Math/actions/runs/35422707150); completed successfully.
- The plain public webpage, ZIP, and checksum URL all returned HTTP200 and
  matched their local SHA-256 hashes exactly; see `live_checks.json`.
- Download SHA-256: `b45e3e798c6b599d429ebb4e0807fcebe85fdb46bce56b86ac936c0b9734bcdc`.
- The paper, original source-and-certificates archive, Zenodo kit and version1.1.0
  tag remain unchanged. No release or new DOI was created.
- All142 production/root modules compile;1262 named declarations passed actual
  type/axiom inspection, with only propext, Classical.choice and Quot.sound.

This deployment record is intentionally outside the downloadable ZIP, avoiding
a circular archive hash. The ZIP remains the frozen verified publication asset.
