# Independent adversarial review: PR1132 existing-publication ledger repair

**Ready for one existing external publication record, using the final reviewed plan and helper and the parent's required fresh live checks.** No mathematical-scope or record-identity objection remains. Two operational defects were found and repaired before any live write. This is a bounded AI review of an accounting repair, not a new publication, a complete fresh Floer-foundations audit, human peer review, or worldwide-priority certification.

Final reviewed plan SHA256: `6d550ac55930e294fd2e544efb02510dc052b49852efd65d644add7ca56cad81`.
Final reviewed helper SHA256: `a213f0f14f19bcf94f4cb4396e2d487e8afa1f21ce8131d6af00c6be581f8900`.

## Exact result and attribution

I independently read [Alfieri–Binns v1](https://arxiv.org/html/2404.00490v1), Definition1.6, Question1.10, Section2.1 and Remark2.2. The question concerns the full staircase of cyclic **direct summands** through the U-torsion length, in the total HF-minus module over F2[U], for every rational homology3-sphere. It does not ask only for a submodule or one selected Spin-c structure.

I freshly obtained the actual [Ferudun publication](https://zenodo.org/records/23063072), read its title, abstract, exact Theorem1.3, definitions, module argument, scope/disclosure and source/reproducibility sections, and visually inspected PDF p2. Its example Sigma(30,47,83) is an integral homology sphere, hence has one Spin-c structure. Both orientations have torsion length16 without a length15 cyclic direct summand, including after forgetting the grading. This is exactly the required negative answer. The weaker Lin restriction and the L-space conjecture are not refuted. The proposed row preserves those boundaries.

Authorship belongs to **Alper Ferudun**, with the provider's Mercury Software GmbH affiliation. The record is dated30September2026, version1.0. The source calls itself an unrefereed, AI-assisted, computer-assisted preprint; its manuscript expressly says it has not been peer reviewed. The row does not transfer authorship to Alec Kriebel or announce a new DOI. Its exclusion of exhaustive searches, minimal-product claims, additional examples, population counts and worldwide-priority certification is appropriate. Those unnecessary claims are present in the source but are outside this repair's verification.

This review checks the identity and intended scope of an already published result. I did not rerun historical third-party archive programs, redo the entire numerical proof, or retrieve and independently reprove all analytic plumbing/graded-root foundations. The repository PR contains a separately scoped mathematical audit; its historical computation totals are not certified by hashing or by this accounting review.

## Current publication, supporting materials and duplicate checks

Fresh independent Google Workspace CLI reads show180rows with the exact four-column schema. Searches across every cell found no DOI, numeric problem ID, OWR alias, exact PR reference, author-pair/question match, or broader Floer/geography/Seifert semantic lead. A full authenticated GET-only owned-account enumeration covered197published/draft records over8pages and found no equivalent publication or pending-draft lead. These are dated captured checks, not a promise that the live world cannot change.

The Zenodo API says record23063072 is done/submitted, with DOI10.5281/zenodo.23063072. The DOI independently resolves HTTP200 to the correct record. All three current public attachments have freshly matched provider sizes, MD5 and the reviewed SHA256 values:

- Paper PDF,178682bytes, SHA256`246de76cb53d62629b62ae291bab4aa3e3cb001e7c54f5d8c6b50425e7d53759`.
- Source ZIP,258522bytes, SHA256`36960972d2b2de7eedb9a3e8e794f4b292afeb0143566f5b6feed7ce93a80797`.
- Verification report,20935bytes, SHA256`4ac9deefc93c6509c2a3243638f6227c1c796dbb8888d1966f3d68f56bacb614`.

The ZIP has99unique safe entries and92payloads; every payload was read and inventoried and CRC checks pass. It contains manuscript source, bibliography, reproduction instructions, certificate/checker code and recorded outputs. The two21829byte copies of the1707-pair certificate agree exactly, SHA256`6d7130dbc0ecf948286ed5d2b7e51a2cdad322da0588a97f3c9ddf7a43f72943`. The standalone report matches its archived copy exactly. This third-party source archive has no internal full manifest and no embedded PDF; I did not invent such a guarantee or impose the repository's later packaging format. The separately published PDF supplies the reading copy.

A final independent readback before sealing found the same180rows, provider metadata/files, and OPEN draft PR at head`bab329be46faab9d04bf1664a7183712239f88b2`, base`f6caddda8f8be2cdb3e91494325d8f7f365bc3fc`, bodySHA256`3c32d41522c5943d82865e67e5b3d21fe1b9ee0fac50d704699db992629b443e`.

## Adversarial operational findings and repairs

The initial helper, SHA256`a9a4cf9c499a11256817073667d14e3281a150b18a504d0f3a334aec7aa4a97e`, compared live head/base/body only against mutable inventory. A changed live head paired with refreshed inventory therefore passed the old reviewed plan. I demonstrated that failure with a copied helper and fake services. The final helper directly checks the reviewed plan's head, base and body hash, in addition to inventory equality. It also checks its own bytes against the parent's adoption. Mock changes to any of these reject before append.

The initial intent used an existence precheck followed by replacement. Two simultaneous invocations could both pass and append. A forced concurrent mock reproduced two appends with the old helper. The final helper uses exclusive O_CREAT|O_EXCL creation, mode0600, complete JSON write, flush and fsync before append. With both prechecks deliberately forced stale, exactly one writer appends and the other gets FileExistsError. A partial intent blocks blind retry.

The final helper was tested in new private copies, with all provider, account, PR and spreadsheet calls replaced by explicit fake services. **25cases pass in each of normal, -O and -OO modes**, with identical semantic outcomes. They cover a new append, exact-existing-row idempotency, incomplete/duplicate/semantic rows, account lead, absent adoption, plan/helper/review-pin changes, changed live-and-inventory head/base/body, provider draft/metadata/files, wrong DOI destination, schema change, prior partial intent, unexpected append response, and final duplicate detection. An append that committed before a simulated transport failure leaves an intent; recovery reads the exact existing row and does not append again.

Google Sheets append is not a global compare-and-swap transaction. Another independent agent can append an equivalent record between this helper's final read and append. The tests show that final readback detects that duplicate and refuses a verified receipt; it does not promise to prevent all cross-agent races or automatically delete another process's row. Any such outcome requires reconciliation without a blind retry. This is the remaining service-level concurrency limit, not an unresolved defect in the revised local intent guard.

## Recommendation and artifact boundary

The proposed four cells correctly record this existing external publication with author credit, exact scope, DOI, source links and PR reference. The parent should bind the final plan/helper hashes and this review's sealed evidence in its adoption, then let the helper perform its live account/PR/provider/DOI/schema/semantic-duplicate gates and exact final row/uniqueness readback. If a concurrent incomplete or different row exists, the helper stops for root reconciliation instead of appending.

The read-only custody guard also rejects four malformed packet cases in each of normal/-O/-OO modes (12rejections): wrong external digest, an extra file, a symlink and tampered captured PDF bytes. Those provisional-seal fault runs are retained separately from the final externally anchored replay.

No provider, spreadsheet, PR, Git index/ref or unrelated repository content was modified by this reviewer. No outside individual or other ongoing agent was contacted. The private input inventory and externally anchored manifest establish byte custody only. `verify_artifact.py` is read-only and does not replay writes; `mock_guard_tests.py` can be replayed only in new disposable fixture directories with fake services. The local GWS shared-prerequisite file was absent; no skill generation was attempted, and the CLI's actual read schema was inspected. Review completion100%; overall sweep estimate77% as supplied by the parent.
