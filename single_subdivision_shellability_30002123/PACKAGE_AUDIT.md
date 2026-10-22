# Independent package acceptance audit

21 October 2026. Row 1837; ID 30002123; OWR-12006-004.

## Decision

ACCEPTED for the limited unresolved checkpoint described in ACCEPTANCE_REPORT.md. The packaging transformation preserves the accepted mathematics and independent verification algorithm. The problem remains UNSOLVED; the elementary positive example and failed centroid ordering are not a solution or disproof.

RESEARCH.md remains byte-identical to the accepted artifact, SHA-256 a11d8b56011bc9043f00410b97f29aed7e0084c3487e36df1c02fa0870660d4a. The independent checker reviewed here has SHA-256 0869c5a00dda55049e369552702af76c3ef2e7cbd897d701f4f6aff5235497e7.

## Source-to-package transformation review

Independently compared the original and packaged checker line by line. Changes are limited to using the package directory for inputs; introducing an explicit RuntimeError guard; replacing all original assertions with equivalent guard calls; and additionally enforcing the exact square vertices, fan facets, rational functional slope, and no-tie field. No maximal-chain enumeration, facet-completeness, face-union, intersection-purity, height computation, or geometric identity algorithm was replaced. Explicit guards remain active under Python optimization.

The mathematical audit differs only by its package-local reproduction command. All source/package hashes in PROVENANCE.json were independently recomputed, and entries described as byte-identical were also directly compared byte for byte. SOURCE_METADATA.json and CORPUS_VERIFICATION.json retain public bibliographic and verification information while omitting local source locations. No copied PDFs, source extracts, dataset records, or private coordination material are included.

## Independent replay and corruption results

Reviewed all packaging scripts: run_checks.py, research_controls.py, test_corruption_controls.py, and verify_manifest.py. The replay uses temporary copies, checks complete output bytes rather than selected success fields, and tests both normal and optimized mathematical executions. Its syntax check rejects assertion-dependent guards. The independent results remain byte-identical to the pre-packaging independent audit.

Independently ran run_checks.py successfully. Independently ran the corruption-control orchestrator with optimization enabled; all 34 controls passed, and its complete output matched CORRUPTION_CONTROLS.json byte for byte. These include content corruption, missing/extra inventory, nested manifest inventory, invalid manifest entries, incorrect saved output, incomplete/duplicate/incorrect complete certificate orders, invalid face labels, and altered geometry or sweep inputs.

A separate independent disposable-copy test additionally exercised ten cases in each execution mode: an unchanged mathematical input baseline; missing certificate facet; duplicate facet; wrong complete order; outside-square fan vertex; changed slope; contradictory tie field; broken apex midpoint; flattened apex; and changed ridge vertex. Both baselines passed and all eighteen altered-input runs failed. This confirms that explicit optimized checks, not only manifest detection, reject the selected bad mathematical inputs.

The provisional 25-file manifest passed exact inventory, byte-count and SHA-256 checks before this audit was added. Final manifest regeneration and verification are required after adding this audit and updating the provenance review status. No package content should change after the final manifest is frozen without a corresponding integrity and scope review.

## Limitations

These are selected mathematical and integrity controls, not exhaustive hostile-parser testing or authentication. A manifest cannot authenticate itself against coordinated replacement. Direct research-script calls write generated results beside those scripts; immutable replay should use run_checks.py. Use Python's -B switch to avoid adding bytecode files to the exact inventory.

Source status remains a bounded literature inspection, not a guarantee of exhaustive coverage through 2026. No queue modification or GitHub publication was performed by this audit.
