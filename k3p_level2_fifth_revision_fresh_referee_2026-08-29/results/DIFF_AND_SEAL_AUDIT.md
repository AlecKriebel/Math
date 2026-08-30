# Fifth-revision seal and immutability audit

## Result

PASS. The fifth package is clean and internally sealed. No change reaches a
mathematical producer or theorem dependency.

## Identities

- proof/package commit:
  `c0894b85a1a6faf08d13bc17f7586de0223081f6`
- outer manifest:
  `97cdf689b27d443179ab03dd4b18022cd8ded9f4a38c5514f69eab35e797d10b`
- outer sums:
  `820380cf7ab9d476723240c6b86df3e27d5e2bcb30042833d7ee69ac802c1aae`
- archive manifest:
  `c81afe66c3d76469898c221d6afc1dc82864471d43157bcf520ddd10f1c6a9c0`
- named canonical archive:
  `7501c52166e7ddcddf5c1a5e60105ba308e84e31f23432c36b5c3328b419b2c5`

Integrity checked 635 outer payload rows and 597 proof-core members. Independent
`SHA256SUMS` verification passed 636/636.

## Changed outer payload paths

Exactly 22 of 635 paths changed; there were no additions, removals, or mode
changes:

1. `RUN_REVIEW.sh`
2. `START_HERE.md`
3. `proof_package/ACTIVE_MANIFEST.json`
4. `proof_package/ARCHIVE_MANIFEST.json`
5. `proof_package/FINAL_CLAIM_LOCK.json`
6. `proof_package/REPRODUCIBILITY_README.txt`
7. `proof_package/SHA256SUMS`
8. `proof_package/release/FINAL_RELEASE_ENGINEERING_REPORT.md`
9. `proof_package/release/dist/k3p_level2_article_source.zip`
10. `proof_package/release/dist/k3p_level2_supplement_source.zip`
11. `proof_package/release/source_reproduction_evidence/article.json`
12. `proof_package/release/source_reproduction_evidence/supplement.json`
13. `proof_package/release/source_reproduction_evidence/
    supplement_transcripts/run1.log`
14. `proof_package/reproducibility/K3P_SAME_CLASSIFICATION_GATE_REPORT.json`
15. `proof_package/reproducibility/
    K3P_SAME_CLASSIFICATION_MUTATION_REPORT.json`
16. `proof_package/reproducibility/RELEASE_WORK_LOG.md`
17. `proof_package/reproducibility/verify_k3p_same_classification.py`
18. `proof_package/source_archives/k3p_level2_article_source.zip`
19. `proof_package/source_archives/k3p_level2_supplement_source.zip`
20. `referee_tools/run_active_verifiers.py`
21. `referee_tools/test_output_mode_preservation.py`
22. `referee_tools/verify_package_integrity.py`

The top-level manifest and checksum file necessarily changed outside the
payload list.

## Mathematical immutability

The inner core has 587/597 identical members. The ten changes are one repaired
report writer, two regenerated reports, binding manifests/checksums/logs, and
two source ZIP containers. The writer diff is exactly one `chmod(0644)` line.

All 34 TeX files, one BibTeX file, the 115-file proof-core Python path set,
PDFs, heavy
certificate data, producer cones, and active command plan were compared. Every
mathematical item is identical except the nonsemantic writer line.


Source ZIP content comparison found identical source/cache members. Only the
embedded archive/build metadata changed in content; all member timestamps were
rebound to the new commit epoch.

The Git path diff from `10bd695c...` through `c0894b85...` agrees with the
package change cone. No long mathematical replay is dependency-justified.
