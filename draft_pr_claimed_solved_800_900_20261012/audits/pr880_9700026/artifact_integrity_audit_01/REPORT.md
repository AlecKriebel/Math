# PR880 problem 9700026: independent artifact and reproduction audit

Timestamp: 2026-10-15T09:41:28.252670+00:00

**Decision: the exact frozen artifacts are authentic and their finite diagnostics and optional complete-input provenance are reproducible, with explicit limitations in the older wrapper's assurance model.** This family does not issue a mathematical validity, source-interpretation or priority verdict. Successful hashes, acceptance strings and finite computations cannot supply one.

## Target and authentication

The target is frozen PR head `fba74a301786f9648e48722e76f440097b0746c2`, source prefix `unsolved_math_prioritization/attempts/9700026/`. The independent threat-scope memo was written before any supplied program executed. All four unique Python bodies (five paths, including the duplicate author checker) were read in full first.

The externally supplied outer source-manifest digest is `b0b0cdc72798cfcffc5fefeec1de30ff422f54bde83d0f8a91fd2e6a87311d8b`. Against it, the audit verifies a closed inventory of **40 ordinary 100644 files / 276581 bytes**, every byte count and SHA-256 digest, and every Git blob identity. All original JSON is parsed with duplicate-key rejection, nonstandard-number rejection and floating overflow rejection. All Python bodies are parsed before execution.

The original publication manifest is **6446 bytes**, SHA-256 `379efdd8506bb5f28c80ece66fc5b9e130a9668c5605343443cb811b84a23081`. Its 39 listed members plus itself are exactly those 40 files. The author proof is **5736 bytes**, SHA-256 `8b0922482116df0b6510b4d5a6c089c3478765d4fecf2c151fd04c50a6814767`.

The original author ZIP (**11844 bytes**, SHA-256 `adc58ab6c2b52963f303582261ee603470dbf2728eee8b4546c04ba7cf9b201d`) has exactly eight members. The audit ZIP (**43131 bytes**, SHA-256 `c4cab38294bbc44310811056fcfe6c2f83ad8b5ab8690ff45438184d368f64fc`) has exactly 19 members. The audit ZIP's nested author ZIP is byte-identical to the original author ZIP and its eight members are independently authenticated again. Both external manifests, all inner manifests, all readable duplicates, and all five review-B files match. Author ZIP entries use ordinary-file mode 100444; audit ZIP entries use ordinary-file mode 100644. There are no directory entries, duplicate names, unsafe paths, unexpected types, executable entries or inconsistent declared sizes in the real archives. The receipts list every member's bytes, digest, CRC and mode.

## Actual fresh replay

`RESULTS_WITH_PROVENANCE.json` records **56 fresh top-level positive processes**, all passing:

| Entry point | Cases | Modes and locations |
|---|---:|---|
| Author witness and author self-test | 16 | Normal, optimized, isolated, isolated optimized; frozen and relocated |
| Audit-A witness and audit-A self-test | 16 | Same |
| Complete original source checker | 8 | Same |
| Source-free original publication wrapper | 8 | Same |
| Complete-input original publication wrapper | 8 | Same |

Every run starts from an unrelated working directory. `-B` prevents bytecode writes. Original wrapper invocations additionally spawn 72 child-checker processes in total; those nested executions are not counted again among the 56 top-level positives. The author witness reports 216 exact influence comparisons and four scalar algebra checks. The independent audit witness reports 600 influence comparisons, five scalar algebra checks and 27 gradient identity checks. Both original self-tests reproduce their 16/13 negative and two positive controls under all modes and locations.

The original source checker and full wrapper match all three complete unchanged corpus inputs and both freshly retrieved primary PDFs. The corpus is not reduced to the target row for these positive runs. Independently strict parsing selects exactly one canonical int/string ID `9700026` in each relevant full corpus, and the complete record/report canonical pair matches **4409 bytes / SHA-256 `7b18458d71482e2c4e1c62601be1824eba6ad6243c78135d90d1b75223e8e193`**. The imported statement's hash and catalog review hash also match. The exact five input pins appear in the receipt; no private record, report, full corpus, PDF, extracted text or render is retained here.

A separate final invocation executes the independent harness itself under optimized isolated Python. `RESULTS_SOURCE_FREE.json` records **40 positive processes**, all passing, and its external-input status is explicitly **NOT_RUN**. It does not inherit the provenance PASS from another invocation. The two successful final invocations use the same harness digest, recorded in each receipt.

## Adversarial scope and classification

The complete-input invocation records **110 in-process helper/gate evaluations**: **85 intended rejections observed**, **22 legacy limitations accepted**, **three valid acceptance controls**, and **zero unexpected rejections**. Separately, **10 fresh normal/optimized original source-checker processes** reject malformed replacements of each of the five input files at that file's literal pin check. Thus these are 95 observed rejection evaluations across these two categories, not a claimed reconstruction of the historical 106 tests.

All **49 fixed-pin attacks** are rejected: independent mutations of each of the 40 source files; unlisted ordinary file, empty directory, FIFO and symlink; listed symlink and FIFO; wrong mode; missing file; and a malicious startup-marker replacement. The marker is absent after the gate, and the mutated program is never executed. Fixed-pin probes authenticate against the externally fixed outer manifest. Every test uses known-good independently pinned startup code.

Resealed diagnostics are deliberately a different trust model: the good old helper is called with a newly computed manifest digest, or with minimal private source payload PINS replaced in its namespace while the hardcoded canonical-pair and statement pins remain unchanged. They measure parser and inventory behavior, not a way through the unchanged external fixed pin. Every intended rejection has an explicit classification in the raw receipts, including accepted limitations:

- Legacy publication JSON accepts a duplicate top-level identity key and irrelevant NaN, positive/negative Infinity and `1e999` fields under a resealed manifest. The strict independent parser rejects each.
- Legacy publication inventory accepts an unlisted empty directory and FIFO. It rejects symlinks. The independent gate rejects all nonregular entries and extra directories before opening them.
- Legacy author JSON can hide an invalid first alpha field with a duplicate valid last field. Its standalone witness also accepts a dictionary of rational-string keys as the weight iterable. Audit A rejects that malformed container. These probes do not change the fixed certificate.
- Synthetic resealed ZIPs carrying matching `x` bytes with symlink, FIFO or executable mode metadata pass the legacy archive helper. It reads bytes and does not extract them, so this is a missing metadata assurance, not demonstrated file-system exploitation. The independent archive guard rejects all three, plus absolute/parent/dot/backslash/drive-like paths, duplicates, directory metadata and mismatched declared sizes. A plain ordinary-file ZIP passes as a control.
- The legacy POSIX path helper accepts backslash and colon spellings. They do not escape the real current POSIX root in these probes, but the helper is not a portable ZIP-safe-name policy.
- The standalone audit checker accepts changed audit-report metadata when its own optional manifest is removed. The complete fixed publication inventory rejects this alteration.
- Minimal resealed source diagnostics accept duplicate catalog ID, record ID and report keys, plus irrelevant NaN/overflow catalog fields; the strict parser rejects those forms. Duplicate exact rows, missing reports, wrong rank/title and changed statement are rejected by the known-good source checker. Its PDF input reader follows a symlink; the independent regular-file guard rejects the symlink and a FIFO before opening either.

The current frozen ordinary files and ZIPs contain none of the malformed diagnostic payloads. Hashes protect their present bytes even where a standalone parser is permissive. None of these diagnostic limitations alone contradicts the analytic result.

## Startup trust and remaining gaps

The original wrapper hashes a manifest which lists the wrapper itself **after Python has begun executing that wrapper**. An external publication-manifest digest does not by itself authenticate initial code execution. The independent harness first authenticates the outer manifest and closed complete payload, then launches original code. The harness is itself a trusted caller requiring independent inspection or a separately pinned public-manifest entry before reuse. Accepted legacy behaviors are an explicit allowlist: any newly accepted intended-rejection probe fails the audit, including every strict-parser or strict-ZIP regression.

This is not a hostile concurrent-file-replacement sandbox: the interpreter/standard library and inspected harness are trusted, and the audit assumes no adversary mutates authenticated files between checks and child launch. Receipt capture is not a general redactor: its present publication safety depends on the inspected fixed checker bodies, which emit only verification metadata and diagnostic paths. TemporaryDirectory cleanup covers normal and exception exits, not an uncatchable crash or SIGKILL. Acceptance strings are checked only as frozen metadata. Their truth is not inferred. This family does not renew the PR's 41-remote-file/QUEUE whole-file publication provenance; its authenticated source scope is the supplied 40-file frozen subtree. The artifact family does not certify the universal geometric/comparison proof, current problem-page contents, corrected intended conjecture, primary-source interpretation, literature completeness, novelty, human peer review, formal proof-assistant status, historical HTTP retrieval events or GitHub CI.

The PR advertises 56 positive executions and 106 adversarial rejections. This independent audit freshly reproduces an explicit 56-case positive matrix. It cannot infer that the historical processes occurred, and it does **not** reassert that its differently enumerated rejection observations reproduce the exact historical 106 cases. Historical `AUDIT_TEST_RESULTS`, source receipts and review-B receipts remain authenticated historical objects, not fresh evidence.

## Operational record and reproduction

The initial large-copy optional provenance attempt failed with ENOSPC and cleaned its disposable directory. A second invocation exposed an integer-only assumption in this audit harness; the canonical ID selector was corrected to admit exact int/string forms, and that failed invocation also auto-cleaned. Neither failed invocation was promoted as a passing result.

The successful full replay uses exact independently verified ordinary-file **hardlinks** with the original checker's required basenames. Full code inspection confirms supplied source code only reads those paths. No hardlinked input is written, truncated or chmodded. Each malformed-input test first unlinks its temporary name, then writes a new independent malformed file. All disposable links and malformed fixtures are removed. Only this assigned audit folder was written; frozen source, corpus/PDF contents, Git, PRs, releases, sheets and outside contacts were not mutated. The branch remained `main`.

From this directory, run `python3 -I -B audit_harness.py` for the source-free audit; optional provenance requires `--provenance` and the existing complete unchanged local corpora plus the two separately held PDFs. Python's standard library suffices. Results are metadata-only JSON. `STATIC_CODE_REVIEW.md` documents exact code coverage and limits. `PUBLIC_MANIFEST.json` lists every authored public file, byte count and SHA-256, excluding itself to avoid self-reference; it redistributes no primary sources or private data.

Assigned artifact/reproduction audit completion estimate: **100%**. Research-wide mathematical acceptance remains the parent audit's separate decision.
