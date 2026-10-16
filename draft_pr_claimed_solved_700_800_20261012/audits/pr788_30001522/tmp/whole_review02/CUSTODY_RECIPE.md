# Portable review custody

Obtain the external manifest and checker SHA256 pins from the parent review record. Do not bootstrap trust from a digest stored only inside this packet. From any copied flat packet directory, run:

    python3 -I -B custody_check.py --packet /absolute/copied/packet --expected-manifest-sha256 MANIFEST_PIN --expected-checker-sha256 CHECKER_PIN --replay

The checker authenticates its own externally pinned bytes, the external manifest pin, exact flat closure and every authored byte before executing diagnostics. Both ordinary and optimized diagnostics are compared with the sealed results. This is custody, not formal proof verification.

Optional `--preprint-root /path/to/preprint` verifies all 202 bound inputs: the six release outputs, PACKAGE_INVENTORY.json, and every one of the 195 closed source members. Optional `--primary-root /path/to/scratch_whole_review02` rehashes exactly 19 locally listed fresh-evidence files (eight PDFs, eight independently extracted texts, three selected source-page renders). Neither option silently claims recovery of the historical 76-file evidence bank. Primary bodies stay outside this authored packet.

`custody_controls.py` requires the external pins, a separate scratch directory, both optional evidence roots and a second Python interpreter; its help lists the arguments. It runs four relocated positives across Python 3.14/3.12 and ordinary/optimized modes, plus twenty nonvacuous rejection controls. The deterministic receipt omits the manifest digest to avoid circularly hashing its own containing seal. The same controls are rerun against the final seal and must reproduce this receipt byte for byte. Final terminal receipts with the final manifest/checker pins are kept outside this flat packet in scratch.

The source's own verifier and deterministic builder were separately reproduced; see REPRODUCTION.json, SOURCE_CONTROLS.json and REPORT.md. They authenticate current source/artifacts and finite diagnostics, not all external literature or mathematical truth. No publication, merge, release, Git-index update or external communication is performed by this packet.
