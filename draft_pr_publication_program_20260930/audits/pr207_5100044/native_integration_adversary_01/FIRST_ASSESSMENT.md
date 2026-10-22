# Independent operational first assessment

UTC: 2026-10-17T00:12:49.897521+00:00
Estimated completion of this operational audit: 15%.
State: independent requirements fixed before reading any preparer implementation, tests, or results. No clearance of the future helper is implied.

## Exact claim and limits

The proposed bounded helper must construct and verify an exact native overlay and then, only after actual Root acceptance and actual native readback, install the exact five current views under the stable existing cooperating-writer lock. The two phases are merge95 (parents fresh MAIN then original HEAD; 49 complete, 34 published, last 206, cursor 207, advance false) and completion100 (one fresh MAIN parent after actual PR207 merge; 50 complete, 34 published, last 207, cursor 208, advance true). Goal remains false. Literal submitted claimed_solved 1 and effort 1/5 remain the only eligible submitted interpretation; model and effort are unverified. A successful fake-service test establishes implementation behavior, never an actual publication, tracker, merge, acceptance, or permission event.

## Independently chosen failure targets

1. Scope escape: native path aliases, leaf/ancestor collision, mode/type mismatch, unexpected old tuple, deletion or change of foreign trees, executable blobs, symlinks, gitlinks, empty trees, or a foreign QUEUE line. Test native tuples and raw QUEUE bytes, not flattened file inventories.
2. Wrong native identity: unauthenticated tree order/SHA, truncated trees, corrupt base64/size/blob SHA, wrong commit parent order/count, wrong tree, wrong original HEAD/tree, stale parent lease at each mutation boundary. Candidate identity and fresh reader verification must bind the exact selected bodies and full changed tuple scope.
3. Fact drift: bool/int alias acceptance; duplicate/nonfinite JSON; missing/extra phase fact keys; incoherent counter aliases; JSON/Markdown disagreement; phase advancement without actual merge event. Goal complete must remain strictly false.
4. Preparation laundering: a candidate or preparation envelope cannot stand in for actual Root phase gates, actual role-selected event files, actual publication/tracker readback, or actual post-CAS acceptance. Every selected receipt requires byte pin binding and event-specific actual semantics.
5. Source and authority drift: pinned helper/core and manifest, canonical regular 0444 owned sources, finite bounded input shape, exact manifest totals and byte/blob identities. Reject symlinks, unsafe paths, booleans as byte counts, mutable source modes and stale pins.
6. Mutation escape and uncertainty: dry is offline, plan/verify GET-only; candidate POST only to native trees/blobs/commits, without refs or other services. No hidden Git/ref command or automatic mutation retry. A journal collision/uncertain POST prevents retry and must never generate a local actual pointer.
7. Local sync races: stable lock inode/payload/ownership, all exact preimages, postimage-only resumability, per-file rechecks and atomic fsynced install; final exact-five plus current MAIN recheck before actual receipt/pointer. This is a cooperating-writer per-file protocol, not a five-file atomic transaction or protection against an arbitrary same-UID writer.
8. Historical fidelity: original 20-file 61131-byte archive immutable; frozen package and proposal seals remain fixed; operational finalization cannot silently change mathematics, code, runs, credit, source, novelty, or prior receipts.

## Checkable control plan

Use small independently authored in-memory native trees and fake API transcripts. Include untouched native empty tree, symlink, gitlink and executable; compute SHA1 natively without local Git. Mutate one dimension at a time with explicit failure expectations and record calls to distinguish validation from side effects. Execute safe owned fixtures using Python -E -S -B -P; require optimization refusal separately. Test local installation only in an owned miniature repository with a real temporary stable lock, never in the shared views. Keep fixture trees/private input copies outside the public allowlist.

## Verified references and remaining gap

Read-only verification matched archive206_verified_reference.py (22049 bytes, SHA256 8a61aee886e7a19bba6c7369944d778614b4099cbe1a060cf7e8acf2f52ec4d5), checkpoint207_v3_public.py (22360 bytes, SHA256 b448d2671fe27ca1bee624602cc1a8de5ef6e95126bef6a79b24fc9ce50bd256), and FACTUAL_FINALIZATION_RULES.json (2647 bytes, SHA256 9028ea071ee69bfcbf6c37fd4f7ec91c72cebd744ce7f5f8aa7e4316efde863e). Only the two source references and factual rules were read. The new preparer helper, manifests, tests and results remain unread pending Root-frozen pins. The exact gap is validation of that frozen implementation, followed by Root's separate actual operations.
