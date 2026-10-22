# PR 781 priority adversary packet

Read REPORT.md, COMPARISON.md and PEER_CHALLENGE.md. The independent report/verdict were frozen before peer access; their immutable copies and hashes are in INDEPENDENCE_FREEZE.json. POSITION_FROZEN.json refers to that independent stage; FINAL_POSITION.json refers to the completed stage.

This is a bounded inconclusive priority audit. No inspected full predecessor was verified; firstness, originality and global openness are not established. Source-body and version gaps remain explicit.

The flat packet is closed by MANIFEST.json. Its only explicit exception is MANIFEST.json itself, whose hash must come from root's independent receipt. The custody verifier's own SHA256 must also be obtained independently. Do not manufacture either trust input by reading an untrusted convenience pin file.

Reproduce in this packet directory, substituting the two externally recorded hashes:

    python3 -B verify_custody.py --expected-manifest-sha256 MANIFEST_PIN --expected-checker-sha256 CHECKER_PIN
    python3 -O -B verify_custody.py --expected-manifest-sha256 MANIFEST_PIN --expected-checker-sha256 CHECKER_PIN
    python3 -B test_custody.py --expected-manifest-sha256 MANIFEST_PIN --expected-checker-sha256 CHECKER_PIN

The source root defaults to the parent workspace; pass --source-root when the exact original/ snapshot and SELECTED_PUBLIC_RECORD.json live elsewhere. No network, Git operation or write is performed by verify_custody.py. The separate tamper tester writes disposable copies inside an owned temporary child directory and removes it before returning. It prints a receipt without updating any artifact.

CUSTODY_TEST_RESULTS.json records a pre-seal rehearsal. That rehearsal's manifest hash differs after its receipt is included; the final external pin authenticates the final packet. The same checker and tamper cases can be rerun with the final pin. Final ordinary/optimized checks are independently recorded by root/tool execution, avoiding circular receipt hashing.

The packet is in root-provided RAM staging because APFS allocation failed. It is not durable storage. Root must preserve these exact authored bytes and pinned inputs before temporary storage is detached. The stale canonical partial folder is not a final packet. No third-party full source bodies, extracts or screenshots remain here.
