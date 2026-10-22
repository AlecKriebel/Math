# Closed custody reproduction

Use the externally supplied final MANIFEST.json SHA256 and custody_check.py SHA256 from the parent handoff. The manifest cannot authenticate its own exclusion. No hashes in this recipe are substituted for caller-held pins.

Run with Python bytecode disabled, once normally and once with optimization:

    python3 -B PACKET/custody_check.py --packet PACKET --inputs-root INPUT_ROOT --bodies-root BODY_ROOT --expected-manifest-sha EXTERNAL_MANIFEST_SHA256 --expected-checker-sha EXTERNAL_CHECKER_SHA256
    python3 -B -O PACKET/custody_check.py --packet PACKET --inputs-root INPUT_ROOT --bodies-root BODY_ROOT --expected-manifest-sha EXTERNAL_MANIFEST_SHA256 --expected-checker-sha EXTERNAL_CHECKER_SHA256

At audit time:
- PACKET is this priority_example folder.
- INPUT_ROOT is its RAM-backed parent tmp, containing intake/original, selected-record/identity files and root-receipts.
- BODY_ROOT is sibling priority_example_scratch. These third-party PDFs, extracted texts and four inspected renders are intentionally outside the authored packet and must not be included in its publication package.
- Rehomed copies are supported by explicit input/body roots; hashes and exact original-tree inventory remain mandatory.

The checker requires the exact flat authored inventory and permits only MANIFEST.json as its explicit self-hash exception. It binds all47 received input files, including every one of41 originals, all24 external source-body/text/render files, frozen initial plan/report/position, ledgers and peer provisional input, and replays the finite comparison artifact. It rejects symlinks, missing/unlisted files, invalid or duplicate JSON keys, unsafe paths, altered source/head/claim flags and failed comparison replay. It uses explicit exceptions, with no optimization-sensitive asserts. It reads only; it does not search the web, change sources or mutate Git.

For separate review, comparison_check.py can be run with python3 -B or python3 -B -O; its result is COMPARISON_RESULTS.json. It only checks finite specializations and never certifies a universal proof, novelty, publication priority or search completeness.

CUSTODY_TEST_RESULTS.json records positive/negative tests against an earlier testing manifest, before this receipt was added. The final manifest incorporates that receipt and this recipe. The externally reported final manifest/checker pins and final positive replay are the authoritative closure, avoiding a circular self-receipt.

RAM staging is the actual storage used because global APFS writes failed. No canonical disk persistence is assumed; root handles publication and durable/API preservation. This packet is sealed only after final pins and both final positive checks are returned. Do not alter a sealed packet; add later work as a sibling supplement.
