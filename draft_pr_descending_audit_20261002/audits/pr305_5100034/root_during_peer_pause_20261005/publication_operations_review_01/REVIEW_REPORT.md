# PR305 publication operations independent review

Completed UTC: 2026-10-05T01:37:49.781055+00:00. Outcome: **repairs required before operational clearance**. Review completion: 100%; no publication completion or mathematical result is asserted.

The exact five reviewed operator files, reviewed submission PDF/ZIP/metadata, frozen candidate manifest/payloads and repository Zenodo kit match all specified identities. Two native isolated runs passed 13 and 15 tests respectively; passing tests include reproduced unsafe boundary behavior, so they do not constitute a clean publication verdict. Full native argv/cwd/times/code/stdout/stderr/source hashes are retained in the root test artifacts and `test_run_002/`. All four intentionally absent actual authority files remain absent.

## Mandatory findings

**M1 (P1): optimization removes the safeguards.** The operators rely on `assert`; `/opt/homebrew/bin/python3 -B` still honors `PYTHONOPTIMIZE`. The exact gate source compiled with optimize=1 accepted a paused, revoked, mismatched token/owner/PR/origin fixture. Normal test execution had optimization unset; this is a proved runtime boundary, not evidence that a real launch bypassed authority. Fail explicitly on an optimized interpreter before running gate logic, or replace hardguards with explicit exceptions. A separately checked, bound actual-launch environment is also possible.

**M2 (P1): the lease has no temporal validity.** `window()` requires logical status/token/head/origin but no issue time, expiry or bounded validity. It accepted an explicit expired year-2000 lease and future year-2099 not-before. Require ordered bounded UTC issue/not-before/expiry fields bound across the two actual lease files and ensure the subprocess deadline fits the remaining validity. Missing/stale/future fields must fail closed.

## Optional hardening and bounded prerequisites

Operational clearance accepts an empty closed-evidence map; the future trusted root producer must actually bind closed independent reviews. The tracker mock accepts a locally supplied public verification receipt whose two file entries contain only true success flags, although the genuine reviewed public verifier emits full evidence. Binding exact public receipt file digests/names/bytes, manifest/source identities and capture hashes would remove that reliance on trusted recent local output. Public HTTP traces omit cwd/source identity. These are explicit trust/reproducibility assumptions, not allegations of present unauthorized grants.

## Strongest verified result and exact gap

Normal-mode absent grants and paused/mismatched status reject before mutations. The source binds complete frozen payloads, production kit/manifest, exactly two files and publication confirmation ID. A lost publish response made one mocked POST and read back the same published deposit; a child timeout retained partial streams, exit124 and a permanent attempt marker that blocked retry. Anonymous public code compares all 11 metadata fields, whole bytes of both files, checksums and exact DOI/record resolution. The exact tracker code made one RAW four-cell mocked append, preserved the blank chat cell, checked all 43 columns in FORMULA mode before/after and rejected completion if the original header changed. The actual retained preappend capture contains 23 used row arrays and no target/title duplicate. No individual communication is present.

Live Git/remote account/public-record state was not tested. OS flock coordinates cooperative local writers; arbitrary file replacement and other remote tracker editors remain outside that mechanism. Read-only recovery is mandatory after an uncertain write; the timeout does not prove the service did nothing. The future root must create genuine scientific/operational closure and bounded release/lease artifacts only after actual reviews and reconciliation. No current publication authority is inferred.

A new adversarial review of the **repaired exact source hashes** is required before operational promotion. The separate whole-preprint mathematical review is not adjudicated here. See `REVIEW_REPORT.json` for mechanisms, evidence tests, repair details and complete assumptions; `INPUT_INVENTORY.json` and `OUTPUT_INVENTORY.json` provide measured file inventories.
