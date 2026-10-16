# Separate PR204 original-verifier repair supplement

**Both repaired derivatives enforce their original mathematical predicates in ordinary and optimized Python.** All four valid executions preserve the original archived JSON byte-for-byte. All four genuine false-identity executions fail with the intended mathematical AssertionError. These derivatives do not change or replace the historical original archive or the sealed original-behavior audit.

## Exact change and provenance

The derivatives replace all2 correctness-assertion sites in original verify.py (SHA256 20319857fe6100f817738dfeed82a6a9e925a264c372b1b94eb936ad193ed6db) and all8 sites in original independent_review/independent_check.py (SHA256 804c995cd0f5b481eebc0a3d1831cffcc6e8ab7c594758c2411c41a134df65af). Each `assert test,message` becomes `if not test: raise AssertionError(message)`; no-message assertions raise AssertionError without an argument. Python AST reformatting changes layout; it does not change any other expression, loop, counter or computation.

DERIVATION_PROVENANCE.json lists each original predicate, its line and message, original/derivative SHA256, and the exact false mutations. SEMANTIC_PATCH_RECEIPT.json independently reverses only the explicit exception nodes and recovers the complete original/documented-mutant AST exactly for all4 derivative files. No Assert nodes remain. Four valid derivative-source files are not claimed: there are2 valid and2 deliberately false derivative files, one of each per original program.

The author derivative retains the historical `proof_sha256` calculation. Its copied PROOF.md has the exact original hash d1e04cf42d4358243365969487348887f3451f9b3fcef63b5215e7389af0e039. This is the historical submitted proof associated with the original audit, **not a current manuscript**. These finite computations do not independently establish that analytic proof. Copied historical proof inputs are documented and pinned but excluded from the proposed authored repair allowlist; the preparation script reconstructs them from the preserved original archive when reproducing the runs.

## Required postrepair executions

| Program | Valid ordinary | Valid -O | False ordinary | False -O |
|---|---|---|---|---|
| Author |exit0, exact archived JSON|exit0, exact archived JSON|exit1, expected chord identity failure|exit1, expected chord identity failure|
| Reviewer |exit0, exact archived JSON|exit0, exact archived JSON|exit1, expected physical-product failure|exit1, expected physical-product failure|

The author false mutation changes its first exact chord-contact identity from0 to1. The reviewer false mutation compares actual target products against the reference product plus1; the failing3-orbit discrepancy is.132359743979568... . These are the same genuine mathematical mutations used to demonstrate the historical original defects, followed by the exception repair. FINAL_REPAIR_VALIDATION.json confirms every failure ended in the intended AssertionError and matching identity label, rather than merely observing a nonzero exit.

Valid counts remain37393 exact and4092 numerical controls for the author, and13712 exact and348 diagnostics for the reviewer. With explicit predicates, ordinary and optimized execution enforce41485 author conditions and14061 reviewer conditions; the latter includes the additional final existential wrong-parity check. The original12 residue_nonzero metadata flags remain computed metadata rather than newly added assertions. The repair preserves original scope and counts; it does not strengthen their finite mathematical coverage or turn numerics into interval certificates.

Every run uses the identified existing readonly SymPy1.14.0/mpmath1.3.0 runtime with PYTHONDONTWRITEBYTECODE=1 and no package download, install, copy or cleanup. Independent author/reviewer program groups run concurrently; a program's ordinary/optimized output-writing executions run sequentially. REPAIR_EXECUTION_RECEIPTS.json binds all8 argv/environments/times, derivative code hashes, exact stdout/stderr hashes, and author writable-result hashes. No additional broad tests were run beyond these required8 executions and structural/binding checks.

## Custody, sealing and limits

Original20 files remain59343 bytes and unchanged by SHA256. All46 files in the earlier sealed SAFE_AUTHORED_ALLOWLIST.json were rechecked unchanged. Its SHA256 remains a5c809d4a94bafd3773764f063ce23aa79a86a15058a487500768f38ddf0fea8 and original FINAL_REPORT.md remains713fb7b74e6c3f5f34813868ad88d6d01c714b4500296c9af83f74cc127eaae7. The original audit correctly continues to report the historical -O defects; it was not rewritten after repairs.

The repair supplement is complete. It supplies robust executable finite controls, not universal proof or priority clearance. REPAIR_SAFE_AUTHORED_ALLOWLIST.json is the exact separate proposed repair evidence allowlist. Original archives, dependencies, primary PDFs, and copied historical PROOF.md inputs are excluded. No Git/index/ref/branch/native/PR/UI/tracker/publication or external-person communication occurred.
