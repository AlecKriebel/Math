# Independent adversarial audit of the acceptance queue correction

UTC: 2026-10-02T02:40:33.103391+00:00. Completion estimate: 100% of this bounded metadata audit. Verdict: PASS_EXACT_BOUNDED_QUEUE_CORRECTION. The main application and additive historical qualification remain root-owned subsequent actions.

The approved candidate is SHA256 `2ab8d870f672a1f3c326aa51326dc27d34f83a8b37e81499d7657d10c38c8858`. Its exact preimage is the immutable cab3546c2 queue SHA256 `2a8afda44a3e9bc1c4d348fd40fd6c260d13d70950e1b5f17677372c628be980`. This approval cannot be transferred to changed queue bytes or a changed program.

## Independent initial finding

Before reading root reconstruction, postmerge claims, mirror implementation or candidate, I read the literal header and all 21 completed primary rows from PR9–17, PR19 and PR21–31, plus PR22's shared duplicate. The initial finding was sealed at 2026-10-02T02:31:28.089410+00:00. The initial JSON records contain all 22 actual complete records, and their identities were subsequently verified against the accepted state and completed inventory. I did not borrow root indexing assumptions.

The literal header has twelve names: Rank; ID / code; Problem; EV; Impact (/10); Difficulty; Proposed; Status; Turns; Chat; Findings; DOI. Raw pipe splitting includes two empty edge cells: raw index10 is Chat and index11 is Findings. Removing the edges gives logical Chat9 and Findings10. The error comes from mixing these conventions.

Eight accepted rows, PR24–31, place their complete accepted-result prose in Chat with Findings blank. These are 10000062, 2800102, 10400115, 30003713, 7000019, 30004186, 30003955 and10000043. All eight rows have twelve actual cells. Structural cell-count assertions therefore pass while column meaning fails. The other thirteen completed primary records and the accepted duplicate already have their notes correctly in Findings. Both published DOI cells, for PR9 and PR16, are correct and distinct.

## Exact correction and historical scope

I read the complete repair_queue.py, its root plan and both full queue tables. I independently reproduce the pure candidate function. It moves the exact complete existing Chat cell, including spacing, to Findings and moves the prior blank Findings cell to Chat for those eight IDs only. Every other selected cell and every unrelated line, including all genuine Chat links and DOI links, remains byte-exact. The literal header and all numeric row identities remain unchanged.

All eight actual acceptance merge commits were resolved locally and their first-parent queues independently inspected. Every affected record's genuine premerge Chat and Findings were blank. Restoring Chat to blank is therefore established by Git evidence rather than assumed. PREMERGE_AND_MIRROR_INSPECTION.json preserves the exact eight first parents and full records. Status and original budgets remain: PR24 unsolved1/5; PR25 already_solved0/5; PR26 unsolved1/5; PR27 unsolved1/5; PR28 unsolved2/5; PR29 unsolved1/5; PR30 unsolved2/5; PR31 unsolved2/5. No affected DOI exists or is introduced.

Historical integration claims that only selected status/budget/findings changed are mislabelled: the integration actually modified Status, Turns and Chat, leaving Findings blank. Their numerical raw8/9/10 assertions may describe the actual changed offsets, but they do not certify named Findings placement. This specifically qualifies integration material/checks for PR24–26, MERGE_CANONICAL_PRECHECK and ROOT_POSTMERGE_VERIFICATION for PR27–28, ROOT_POST_MERGE_VERIFICATION for PR29–31, and corresponding accepted prose/logs. PR30's prior vertical-bar repair correctly repaired a malformed cell count, but left its prose in Chat; its receipt is not evidence that the semantic column had been corrected.

These dated receipts, acceptance records and closed manifests should remain exact. Add a central current qualification explicitly applying to all eight canonical/audit records and their earlier body/log claims. Do not rewrite old sealed assertions to manufacture historical success, rebind their old queue hashes to new bytes or infer that old receipts remain current reusable preconditions. Their original dated queues remain reproducible through Git and this initial queue archive. Future updates should derive positions from actual unique header names and check Chat/Findings meaning, not merely row length.

## Accepted mathematics and mirror accounting

I fully read the applicable acceptance-mirror builder, validator and guarded-writer implementation plus the PR31 incremental wrapper. The v2 parser derives named columns correctly, but the builder validates selected Status, Turns, DOI and bound acceptance evidence; it does not check whether the acceptance synopsis is in Chat versus Findings. Neither Chat nor Findings is included in the acceptance event core. Thus this queue defect is a real presentation/schema error while being separate from the accepted proof and source-bound state. Both defective and corrected queue versions pass the existing mirror, demonstrating the precise blind spot.

I independently hash-checked 460 distinct actual protected files before and after the checks: the latest acceptance plan has519 binding records and460 unique paths; its historical queue and inventory bindings are exempt from reusing dated hashes, and current state/history replace those two exclusions in the460-file check set. All458 other exact protected acceptance/package/source/ledger/publication bindings and both actual state/history files are unchanged. Actual builder/validator execution also checks every canonical manifest member and its byte length, accepted-source/prior context against read-only pinned SQLite, unique accepted scope, saved exact remote-merge receipts and original budget ledgers. No source, proof, canonical package, accepted DOI, publication record or original attempt ledger was modified. Git independently reports no changes sincecab3546c2 in the eight old audit folders or eight canonical accepted attempt folders.

Using the actual unmodified v2 builder and validator with PR23's same explicit zero-source ledger adapter, I run two nonmutating preflights. Only QUEUE bytes are substituted in memory; the current inventory hash is refreshed because pending PR33 metadata has advanced, without altering completed scope. Both preflights verify519 binding records,22 targets,21 primary acceptances plusone duplicate. Every acceptance decision/event ID remains exact, state bytes remain SHA256 `7ce88bb56b9c8394d641fc4cfcb78057b5d9e0b9ca252a1bf3e5a522ccf231f9`, history bytes remain SHA256 `5825a64a826b7df02be3edadbb880953e96f6261d97f2548cbda15eb2fb2e535`. History appends arezero; the original consumed-turn sum is26 and new proof turns arezero.

The two runs do not call any writer, queue generator, network API, commit, branch switch, DOI tool or tracker operation. Saved remote receipts are checked offline; this audit does not claim a fresh independent GitHub network authentication. Hash continuity preserves the accepted scientific inputs; it is not a new universal-proof review of21 problems.

## Adversarial controls and reproducibility

check_correction.py is runnable and writes no files. It derives fields from the actual header and checks the full candidate against the immutable independent preimage, exact premerge Chat support, protected bindings and both actual source-bound mirror preflights. Ten in-memory negative controls are rejected: unrepaired displaced notes, altered selected Status, reset budget, invented selected DOI, erased Findings, retained prose in Chat, altered unrelated published DOI, altered unrelated genuine Chat link, changed header, and an extra malformed selected duplicate. The duplicate control is rejected at the line-count boundary before any inference from the malformed row.

check_root_pure_candidate.py imports only the pure function and never runs the root main writer. It independently reproduces the exact candidate and exercises five actual-helper rejections: genuine Chat URL, occupied Findings, duplicated selected wellformed row, duplicated literal header and missing selected identity. All fifteen controls are metadata falsification checks; none consumes an original proof attempt or claims to certify mathematics.

Run from the repository with a Python version supporting the existing v2 helper:

    /usr/bin/python3 draft_pr_publication_program_20260930/infrastructure/queue_schema_correction_20261002/adversary/check_correction.py
    /usr/bin/python3 draft_pr_publication_program_20260930/infrastructure/queue_schema_correction_20261002/adversary/check_root_pure_candidate.py

For a post-application check, supply the actual main QUEUE.md path as check_correction.py's single argument. It must still match the sealed candidate hash. Future acceptances changing protected state or historical inputs should correctly invalidate this dated check rather than silently update the approval.

## Exact remaining action

No concern remains with the sealed bounded candidate. Root should publish the additive scope qualification, perform the exact-preimage guarded single-file application, rerun the independent check against the actual applied queue and preserve an additive application receipt. Approval does not authorize changes to science, state/history, budget, DOI, genuine Chat links, source records, old receipts or closed manifests.
