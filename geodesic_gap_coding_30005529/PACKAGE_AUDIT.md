# Independent package acceptance audit

Date: 2026-10-21 UTC. Decision: **accept as an unresolved mathematical checkpoint**, subject to regeneration of the root inventory after adding this audit and a final successful verifier run. This is not acceptance of a solution, an impossibility theorem, or a comprehensive claim about the current literature.

## Editorial and mathematical scope

REPORT.md, README.md, CLAIM_LEDGER.json, and MATHEMATICAL_AUDIT.md consistently distinguish the proved arithmetic/geometric partial results from the missing compatible geodesic successor construction. Literal tangency, the limited failure of geodesic-time sliding, local transversality without a global return map, orientation-sensitive endpoint reconstruction, finite collisions, and clock/Palm normalization are presented with the required limits. External horizontal sorting is not represented as intrinsic symbolic dynamics. The finite multiplicity examples are not misrepresented as contradicting the limiting Marklof–Welsh theorem.

The original author's REPORT.md was compared byte-for-byte with the package copy and matched. Its SHA-256 is 134658711b21c05418be33b8108d35081074076920d27e3cdf5e6b8f7f1b5fdb. Arnoux–Schmidt background formulas are explicitly labeled researcher-primary-source-checked, not independently source-certified by this reviewer. They are not dependencies of the newly accepted elementary partial results. The corrected tangent calculation uses g^-1 dg, with no incorrect right-trivialization claim carried forward as an accepted formula.

## Script provenance and optimization-safe guards

All three original authored scripts were independently compared with their declared original byte counts and SHA-256 hashes. Their parsed ASTs, after the documented output-path relocation, exactly match the stored original AST records. The shipped verifier's AST transformation was inspected and executed. It replaces each Assert node by an explicit conditional raise, preserving its test expression rather than deleting the guard. Counts are three guards in exact_gap_checks.py, three in endpoint_decoder_check.py, and eleven in exact_audit.py. The transformed complete ASTs match the shipped scripts, and no Assert nodes remain in them. Output relocation changes the destination, not the arithmetic tests.

This is a reproducibility/provenance check against the supplied original evidence, not a cryptographic attestation of authorship. AST_PROVENANCE.json contains authored Python syntax, not copied scholarly source text.

## Actual verifier and mutation execution

Before this audit file was added, the reviewer independently executed:

- python verify_package.py
- python -O verify_package.py
- python mutation_tests.py

All passed. The verifier checks the exact recursive file inventory, byte counts, hashes, structural script provenance, full result-file bytes, and full stdout. Each script runs in an isolated temporary directory under both normal and optimized Python, leaving the expected files unchanged. It does not merely compare selected summary fields.

The mutation suite was inspected and run. It directly executes changed arithmetic or matrix inputs, bypassing the inventory-hash gate for these tests: the congruence sign, a determinant-one matrix input, and a symbolic matrix scaling. All three mutations were rejected under both normal and optimized Python, for six executions. A mathematical mutant is rejected on execution failure or complete-result mismatch. This tests the actual guarded computations/output validation; it does not claim exhaustive fault detection or prove the mathematical results by testing.

Inventory controls passed for an extra file, a missing file, a corrupted file, and a nested MANIFEST.json. The implementation excludes only the exact root-relative name MANIFEST.json; any nested file with that basename raises an error. Symlinks are rejected. The root-manifest exclusion control passed as an intentional self-hashing exception. This exclusion is not an authentication guarantee for the root manifest itself; its final digest must be recorded externally when freezing or transmitting the package.

## Publication boundary and freeze condition

The inspected package contains authored analysis, authored scripts and generated arithmetic results, plus public bibliographic and verification metadata. No copied source PDF, extracted scholarly text, dataset contents, private-source content, or private coordination file was found. Source and dataset metadata are explicitly metadata; the corpus is described as freshly hashed rather than freshly downloaded. AUTHOR_EVIDENCE_MANIFEST.json is clearly labeled original-evidence provenance, not the current package inventory; its absent original STATUS.md entry is not falsely represented as a shipped file.

Adding this audit changes the package inventory. Regenerate MANIFEST.json to include this file, rerun both verifier commands and the mutation suite, and record the final root-manifest hash outside the self-hashed inventory. Any subsequent edit requires another inventory refresh and verification. No publication was performed by this audit.
