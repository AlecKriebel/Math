# Priority audit bundle

Read REPORT.md and VERDICT.json first. Exact scope: PR781/4600024 at head4a38c3ccc4cac918fb75fd4b97449f3ebd2e0f7f, claimed_solved3/5. This is a bounded priority audit; mathematical correctness is supplied by the separate gate.

The52-query ledger records exact queries and batch-level discovery outcomes. SOURCE_REVIEW_LEDGER.json records actual body locators and unread/version gaps. SOURCE_FETCH_RECEIPTS.json records body hashes and sizes; no third-party body is saved. Metadata-only citation/access results are distinct files.

Verify with a manifest hash obtained from the coordinator's independent receipt, not by trusting the convenience EXTERNAL_PIN.txt:
```
python3 -B verify_custody.py --expected-manifest-sha256 <external hash>
python3 -O -B verify_custody.py --expected-manifest-sha256 <external hash>
```
The input root defaults to the parent workspace. Supply --input-root if the pinned input layout is elsewhere. The entire flat bundle inventory is checked, including verifier/test code. The only exceptions are the manifest itself and the exact convenience pin content; there are no directory, bytecode, or generic scratch exceptions. Pinned input files are checked individually; unrelated files elsewhere in the input workspace are outside this bundle's inventory claim.

For adversarial custody replay:
```
python3 -B test_custody.py --expected-manifest-sha256 <external hash>
```
It tests ordinary and optimized child interpreters, using disposable copies inside an owned temporary directory and removing them before returning. It changes only those copies. fetch_primary.py can replay source retrieval in a copied bundle, but intentionally updates receipts there and thereby invalidates the old freeze.

The completed bundle is staged on temporary storage under this audit's tmp/priority-audit-workspace/priority_audit because canonical APFS allocation failed. Preserve the exact bundle plus pinned inputs in durable storage before that temporary volume is removed. No durable publication or canonical preservation is claimed here.
