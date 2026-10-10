# Zenodo paper discoverability metadata audit

## 2026-10-10 21:03 UTC — inventory checkpoint (5% complete)

Goal: review the contents of Alec Kriebel's published paper deposits and improve accurate, field-specific discovery metadata in place. Success requires unchanged record IDs, version DOIs, concept DOIs, version labels, publication dates, deposited filenames, sizes and checksums. Exclude software/codebase deposits and unpublished drafts. No new deposit, new version, DOI reservation, GitHub release, outreach, or curator submission is authorized.

Metadata improvements are hypotheses about better findability, not measured increases in readership or search rank. Prefer precise descriptions and specialist search terms, consistent ORCID, language, resource classification, and verified related resources. Preserve qualifications, AI assistance disclosures, uncertainty, and all authors. Read deposited manuscripts rather than infer results from titles alone.

The existing metadata client has durable snapshots, separate edit/publication, native metadata preservation, and unchanged DOI/file checks. An independent agent is auditing this route. Scope and paper-content reviews will receive independent adversarial checks before publication. Work remains on main, with commits restricted to this dedicated folder because unrelated parallel changes already exist.

## 2026-10-10 21:07 UTC — source and proposal checkpoint (40% complete)

Authenticated inventory found 78 deposits. Exact published PDF checksums bound 71 manuscript deposits to local or verified public-download content (366,239 extracted words, including technical supplements). Specialist independent agents read and prepared content-grounded proposals in five batches. Most original scientific descriptions are accurate and should be retained. Identified resource misclassification for the Knudson paper, reversed creator name on the odd-order p-group paper, missing ORCID/keywords on the qubit paper, and stale no-DOI notes.

One additional published qubit record 21699069 has a public manuscript although its pre-existing pending edit reports no files; it must be investigated separately without publishing or discarding that unrelated edit. Two rich native records need a preserving native route instead of the conservative legacy editor. Initial account reads hit Zenodo's 133-per-minute API quota; no mutation occurred. Reads are now paced and checkpointed for resumption. Metadata edits remain unpublished pending cross-review and full baseline/invariance verification.

2026-10-10T21:19:23.306406+00:00 — Group 3 final offline native audit checkpoint: 100% complete for four scoped rich-record translations and preservation implementation. Current native source ae11b798de60ce749ab9fbde0c262f11e5336bf74d65d5fd64e5a17f21d3ca6d passes 62/62 fake-API checks; exact draft-only OAI omission tested, public PIDs remain exact, second-snapshot rich-state bug repaired. Artifacts: reviews/NATIVE_FINAL_AUDIT.json and reviews/NATIVE_FINAL_ADDENDUM.md. No auditor remote mutation or credential loading; live preservation read-back remains root-owned.

## 2026-10-10T21:21:18.016207+00:00 — publication readiness checkpoint (55% complete)

All 71 initial manuscript proposals passed independent content cross-review and hash binding. Four records contain native-only author roles, custom repository metadata, submitted date or technical scope descriptions; those will use the preserving native route. Existing DOI/concept/version-history and full file baselines are saved for every record. Offline native publication probes pass 62/62 checks.

The first staged legacy edit remains unpublished while representation guards are reconciled: only the required OAI PID and generated per-file links are absent from its draft view, with exact DOI/content/settings preserved. Audited draft exceptions retain exact public read-back requirements. No new version/record/PID routes are allowed. The user authorized discarding older qubit record 21699069’s pre-existing unfinished edit; the discard returned an empty body, and GET read-back confirms done state with identical published metadata, PDF, DOI and version history. The native draft did contain the PDF despite the older legacy API reporting no files. Exact deposited review-edition source is undergoing independent cross-review. Expected final scope is 72 papers and six exclusions.
