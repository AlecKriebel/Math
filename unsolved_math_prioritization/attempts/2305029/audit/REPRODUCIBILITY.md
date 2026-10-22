# Reproducing the independent boundary zero audit

Use Python 3.10 or newer on POSIX. Obtain the unchanged seven-file original packet, plus this audit's trusted checker and test harness. No package installation or network access is needed.

## Verify the exact reviewed packet

Run from any working directory:

    python3 -B verify_independent.py --packet-dir ORIGINAL_PACKET --expected-manifest-sha256 cf5f178a46b580701522ce59ff4707c4179963ec5d2f8848a759261b1d974206

This checks all seven filenames, sizes and SHA-256 values, including MANIFEST.json, against constants independently fixed in the checker. Any alternative manifest pin is rejected. The strict checker rejects symlink packet/source roots and members, duplicate JSON keys, nonfinite JSON numbers, and incorrect manifest or source-identity schema types. It is the authoritative interface for this audit. The script must itself be trusted or reviewed; an executable cannot establish its own authenticity merely by printing PASS.

The original checker can also be run separately:

    python3 -B ORIGINAL_PACKET/verify_packet.py --packet-dir ORIGINAL_PACKET --expected-manifest-sha256 cf5f178a46b580701522ce59ff4707c4179963ec5d2f8848a759261b1d974206

## Optional source identities

Retrieve the three public PDFs identified in SOURCE_AUDIT.json independently. Add `--source-dir PDF_DIRECTORY` to either verification command. Each expected filename, size and hash must match. These PDFs must not be added to the original packet directory or the audit's publication slice.

## Run the adversarial controls

As a non-root user with a writable temporary directory:

    python3 -B run_audit_tests.py --packet-dir ORIGINAL_PACKET --source-dir PDF_DIRECTORY > audit-results.json

Omit `--source-dir` to omit source-identity cases. The full final recorded run includes the three PDFs and has 337 expected outcomes. The harness resolves input paths before using an unrelated read-only subprocess working directory. It tests both checkers in normal, -O and -OO modes and mutates disposable copies only. Source PDFs are copied solely into disposable test directories; neither their contents nor their pathnames beyond public basenames are emitted in the reusable receipt.

Permission probes establish that the read-only fixture really rejects creation and append attempts by the current non-root user. The script deliberately refuses to run the test suite as root. Any unexpected outcome raises an error; no partial run should be represented as the final all-pass result.

Tests with deliberately replaced manifest pins map parsing and metadata boundaries. They are not attacks under the original external trust anchor. See AUDIT_REPORT.md for the accepted boundary cases and the strict checker's fixed-inventory guarantee.

## Audit slice authenticity

MANIFEST.json lists all seven audit payload files with their lengths and hashes; the audit directory contains exactly those plus the manifest itself. Obtain this audit manifest's SHA-256 from the separate handoff or a trusted version-control commit, compare its raw bytes to that value first, and then compare the listed payload identities and exact inventory. Do not bootstrap trust from a hash stored beside otherwise untrusted bytes.

Finite integrity results neither prove the imported analytic theorem nor establish the absence of future corrections. The mathematical acceptance and its dependencies are explained separately in the audit report.
