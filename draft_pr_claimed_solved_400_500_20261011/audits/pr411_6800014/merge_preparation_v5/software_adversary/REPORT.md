# Independent V5 software adversary — blocked source snapshot

**Verdict: one blocking retry-safety defect at the reviewed V5 source.** This finite review is complete. It does not assess or endorse any later repair, live merge, scientific result, or fresh native verification.

The reviewed helper SHA256 is `942924177712fcf7c6211df84298a423f8397cc985c81fb05a6696c06ca8b7f8`; accepted V4 is `e4c9bd76594127b23cf6439df0b2c7a965f39b8f027d6debdb7cdf8e393aaa14`. Independent syntax-tree comparison finds exactly 82 unchanged original top-level nodes, one new `pre_intent_continuation` validator, and changes only to `Journal` and `main`. Within Journal, only `__init__` and `add` changed; `finish` and `close` remain exact. Existing execute, mutate, prepare, evidence, freshness, approval, claimed-scope, preservation and recovery guards remain exact V4.

## Blocking finding: the already-open successor can emit a second merge request

The new exclusive continuation guard prevents constructing a second successor journal. It does not consume the first successor's permission to append a remote mutation intent. After one `execute` call loses its response and writes a terminal STOP receipt, a deliberate second `execute` call with the same already-open Journal object, unchanged approved plan and unchanged original custody appends another intent and sends another synthetic PUT. The existing receipt file then raises `FileExistsError`, after the second request was sent.

The preserved trace is `exclusive_intent → intent → outcome_unconfirmed → intent → response_received → response_confirmed`, with **two fake API PUT calls**. Neither a second Journal constructor nor modified custody or plan is needed. The ordinary merge route and request body remain those of unchanged execute. This falsifies an unconditional no-retry guarantee for the continuation's live journal interface.

The reviewed `main` contains one execute call site, one Journal construction site and no retry/iteration statements; the counterexample deliberately exercises its reusable implementation interface outside that one-shot command path. That narrower command-path observation does not resolve the requested journal-level one-attempt property. The old route is blocked until a materially new durable remote-intent fence rejects reuse before any second remote call. A later repair requires a new independent review.

## Strongest independently checked results

- Fresh, independently generated synthetic fixtures pass **71/71 controls in normal Python and 71/71 under `-O`**, including seven real subprocess CLI controls in each mode. These are separate from the producer's controls.
- Structural custody controls reject mismatched original claim/run/head/phase/plan; every extra original journal event, including remote intent, response/ACK and unknown events; torn, blank, noncanonical or future journals; altered terminal STOP, completed CLI options/return code/helper hash, unjoined acceptance labels, wrong root and symlinks.
- A real eight-contender exclusive-file race produces exactly one successor. The original synthetic claim, journal and STOP bytes remain unchanged. Guard creation/write failures leave the successor guard consumed, and later plan/descriptor/claim/journal/STOP/CLI/acceptance/guard drift rejects intent append.
- Unchanged execute makes one fake ordinary merge PUT in its positive control. Expired Sheet evidence, stale approval, unclean PR and claimed-scope drift reject the write. Response loss rejects a second *constructed successor*, but the blocking direct-object probe demonstrates why that alone is insufficient.
- The root-owned descriptor pinned at `7bc150a109e2ad48edafe5669e57d261944f5eeaad8de31526a4cfae2a417c48` passed a read-only historical ADMIN replay. API and Journal construction were explicitly forbidden. Original input pins were rechecked and no actual successor guard was allocated. Its prior canonical plan is `9b710bf7f64bed0f06527856587df2c3a806196643ce07dc824bd596a7854c53`; root acceptance is `9fb0dd59e9686f39dde730622e69211486fea3c3d9d6fa78d4dd4d5305f64291`.
- The corrected compact producer public summary was inspected at SHA256 `ce303b199004f75716adab4fb07117afa11ea1d1ffcb035487c8deb0b5ad2887`: plans, QUEUE payloads, requests, responses and captures are absent; capture fields contain hashes with private references. This is a historical packaging observation, not a seal of later producer changes.

## Trust boundary and reproducibility

The synthetic fixture code, source snapshots, results, subprocess stdout/stderr, initial failed harness runs, and direct-object counterexample are private under `private_sources/merge_preparation_v5/software_adversary/`. `PRIVATE_PINMAP.json` positively inventories regular bytes and symlink targets; `FINAL_SEAL_SHA256.json` provides the external digest of the public seal. The public seal binds the other four public files and the private pinmap.

Fixtures are generated from scratch and expressly synthetic. Fake API calls and replaced native verification guards prove only control flow and structural joins. The root-pinned historical acceptance supplies authenticity for genuine custody; matching enum labels alone do not. No API/native/network request, live mutation, actual Journal construction, actual receipt/claim mutation, scientific file or asset-byte read, Git command, or external communication occurred in this review.

Initial independent harness errors are retained and excluded from passed evidence: relative synthetic CLI paths were corrected to absolute paths, and the read-only replay's case-directory depth was corrected. The candidate source was unchanged by either correction. All observed findings and unresolved boundaries are preserved; no scientific claim is promoted.
