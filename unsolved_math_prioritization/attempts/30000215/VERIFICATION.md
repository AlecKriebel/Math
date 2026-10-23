# Verification and replay contract

## What is mathematically established

The complete analytic argument is in `PROOF.md`, accepted at its exact SHA-256 by `ACCEPTANCE.md`. It proves the full simultaneous set-assignment statement for every n >= 3 in the two specified families. No finite check below is a premise of that proof. Preparing this reader adds no mathematical pass and no broader mathematical claim.

## Preserved checker and safe entry point

The original `verify_exact.py`, `CHECKS.md`, and `exact_checks.json` are unchanged. The checker contains sixteen Python assertion sites. Python's `-O` and `-OO` options disable assertions when a source file is run normally, so a direct optimized invocation of that original file is not an assertions-enforced verification.

The provided `replay_checks.py` checks the strict packet inventory and source hash, compiles the exact original source with `dont_inherit=True, optimize=0`, and executes it in a temporary directory. This explicit compilation setting is used even when the replay wrapper itself is launched with `-O` or `-OO`. It also checks the sixteen source assertion sites and at least sixteen assertion-failure instructions in the compiled original code. A chained comparison may compile multiple failure instructions; this interpreter produces seventeen. The targeted negative tests below independently confirm each site. Outputs are compared byte for byte with the preserved `exact_checks.json`, and the summary counts are checked explicitly with exceptions rather than wrapper assertions. No preserved file is overwritten.

Run these commands from this directory with Python 3.10 or later:

    python replay_checks.py
    python -O replay_checks.py
    python -OO replay_checks.py

Each complete replay checks 60 drawings (m = 3,4; n = 3,...,32), 1650 induced K(3,3) restrictions, and 1792 deterministic seeded complete assignments. The optional diagnostic enumerates the K(3,3) switching image only: rank 17, 131072 distinct switched vectors, minimum weight 1. This diagnostic is bounded and does not enumerate all original 2^36 incidence assignments or establish an infinite-family result. `REPLAY_REPORT.json` records one complete replay in each of the three interpreter modes and exact output equality.

## Assertion enforcement negative tests

`test_packet.py` runs three positive strict validations, eighteen packet mutations in each of the three interpreter modes, and all sixteen assertion-site probes in each mode. Thus it records 54 rejected tampered packets and 48 confirmed assertion failures. `TEST_REPORT.json` contains the full per-case records.

For each assertion probe, the preserved source is first checked and its unmodified compiled code inspected. The probe then makes a temporary in-memory AST in which the selected original assertion is forced false and the other assertion conditions are forced true to isolate that site's enforcement. The corresponding original function is invoked, and the exact failure marker must be caught. These deliberately modified ASTs never replace the packaged source, and are negative tests of assertion behavior only. They are not independent mathematical checks or new experimental evidence. The three exhaustive-image assertion sites use only the same bounded K(3,3) case.

Run the complete test suite:

    python test_packet.py

For a later restoration inventory-only check, this option explicitly omits assertion probes already recorded above:

    python test_packet.py --skip-assertion-probes

The output accurately marks those probes as skipped. It must not be represented as a fresh assertion-enforcement run.

## Strict manifest and preserved-input checks

`validate_packet.py` uses explicit exceptions, so all its gates remain active under normal, -O, and -OO execution. It rejects missing and unexpected files, unexpected directories, symlinks, malformed or duplicated JSON keys, non-finite numbers, invalid byte counts, unsafe or absolute paths, duplicate or unsorted inventory rows, unrecognized keys, changed target metadata, incorrect hashes or sizes, and altered preservation records.

The validator pins all twelve preserved authored artifacts independently of the editable manifest. Consequently editing the proof or original checker and updating its manifest hash still fails the preserved-input gate. It checks proof-to-audit bindings, source-review pins, and the original source-review public inventory. No source document is fetched or redistributed.

`MANIFEST.json` lists all public files other than itself, with exactly one sorted record per file. Omitting its own hash avoids a circular digest. An external archive/seal record can bind the manifest bytes. Integrity is checked relative to trusted validator and seal bytes; an attacker who replaces the entire packet and its trusted pins is outside this checksum contract. No cryptographic signature or outside mathematical peer review is implied.

## Restoration

The prepared restore archive contains this public directory only. Restore it into a new empty directory, then run all three validator modes and the inventory-only tamper suite. The preparation record separately binds the archive's SHA-256, manifest SHA-256, exact entry list, and restored byte comparison. Archive creation and restoration are packaging checks; neither changes the accepted proof or establishes a new mathematical result.

## Integration-review additions

The reviewed reader binds the complete original PRESERVATION_MAP.json, REPLAY_REPORT.json, and TEST_REPORT.json as immutable historical evidence. The original reports describe the prepared 22-file reader and retain their original validation counts. The final expanded packet is measured separately in INTEGRATION_EVIDENCE.json. This closes metadata relabeling gaps without editing the original proof, checker, or reports.

The added review_checks.py independently compiles the original checker with optimize=0, counts the retained assertion instructions, and isolates all sixteen original assertion sites in each of the three outer interpreter modes. It also records that compiling the original source directly with optimize=1 or optimize=2 leaves zero assertion-failure instructions. Those stripped compilations are negative controls only, never claimed as assertions-enforced tests. It reruns the unchanged wrapper suite and adds resealed-metadata regressions. The probes change an in-memory AST only and do not establish additional mathematical facts.

The top-level manifest covers every public file except itself, including all added review evidence. Historical nested inventories keep their original scope. The final external seal binds the final manifest and archive without a self-referential digest.
