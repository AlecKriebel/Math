# Reproduction and evidence scope

**Pre-review preparation snapshot: 2026-10-07 14:29:16 UTC (07:29:16 America/Los_Angeles).** Status, review counts and unresolved choices below describe this snapshot. Later complete-package review dispositions, license resolution and any publication/tracker outcomes are recorded separately in the repository's review and publication receipts; this snapshot does not predict those outcomes.

Updated 7 October 2026 for the full arbitrary-predual proof candidate. The seven-page downloadable PDF has passed compilation and all-page visual inspection. At this snapshot, the actual supplement's clean extraction/reproduction and complete-package reviews remain outstanding. Historical receipts certify their dated versions only; see `publication/PENDING_ACTIONS.md`.

## Manuscript and downloadable PDF

The standalone source is `manuscript/main.tex`, with an embedded bibliography and no external images. It is the full proof candidate currently open in the Codex LaTeX editor. The built-in compiler confirmed successful compilation of the exact saved source; the editor preview is distinguished from the actual downloadable export.

The downloadable artifact is `output/pdf/paper.pdf`, seven pages, 83,877 bytes. Source SHA-256 is `46a02c0cd03f798459a9cfd8fb1cd5e03c4e599208a2a53750d3b218b7e96dc4`; PDF SHA-256 is `64ef84935aa6b3d327e30d26719927ce603aa75116a6aefa70589342bafe1c0b`. The final-candidate export receipt records successful Tectonic 0.16.9 build, Poppler 26.08.0 inspection, embedded fonts and visual checks of every page. No clipping or formula overflow was found; the bibliography's underfull warning was visually checked and remained legible. The manuscript stayed open in the existing editor.

The deposit will provide `paper.pdf` separately from a source/verification archive preserving the project-relative `manuscript/`, `reproducibility/` and selected supporting paths. The archive's publication README and file/hash manifest define its actual contents. Historical audit/build files not selected into that archive are repository-only evidence, not build dependencies. The former four-page draft and initial morning export receipts do not authenticate the current PDF.

## Clean build of the supplement

Install Python 3, Tectonic and Poppler commands `pdfinfo`, `pdftotext` and `pdftoppm`, or make existing installations available on PATH. Tectonic may fetch its configured TeX bundle on its first run. Keep the separately downloaded, authenticated `paper.pdf` outside the extracted build directory so the script cannot overwrite that reference artifact. Extract the source/verification archive into a fresh temporary directory, change to the extracted project root and run:

```sh
python3 reproducibility/build_paper.py --root . --render
```

The script copies `manuscript/main.tex` to a new project-local `tmp/clean-publication-build-*` directory, rejects compiler failure or an overfull warning, checks that the source did not change, and creates the reproduced `output/pdf/paper.pdf`. It also extracts text and renders every page; it does not itself visually inspect the renders or certify mathematics. With `--receipt PATH`, it writes a JSON receipt at the specified path. The original source remains unchanged.

Verify the extracted source's SHA-256 against the archive manifest and the reviewed source hash above. Compare normalized layout-extracted text from the reproduced PDF with the separately authenticated downloadable paper. PDF byte hashes may differ because of creation timestamps; preserve the actual deposit PDF's exact bytes/hash, and do not mistake a rebuilt hash for the submitted one. Inspect all rendered pages. Before publication, root must run these commands on the actual archive and preserve a clean-package reproduction receipt; this documentation update does not assert that test has already occurred.

## Finite exact checks

Run `python3 research/cohomology_adversary_checks.py` from the project root with Python 3 (tested 3.14.6; standard library only). It writes `research/cohomology_adversary_checks.json` and checks 5,461 exact central-homotopy equations, 16 Catalan leading counts and seven ordered-block endpoint cases. These are falsification checks on finite proof mechanisms, not a computational proof of the infinite-dimensional theorem.

Run `python3 research/draft_whole_review_1_checks.py` for the independent noncommutative central-homotopy check on M_2(C) direct-sum C. Its 260,416 exact scalar equations passed on independent root replay. It uses only the Python standard library. As additional repository-only evidence, the 1,022-equation symbolic check through degrees one to nine has an independent replay receipt in `research/revised_checkpoint_review_symbolic_central_homotopy/independent_replay_receipt.json` and a root replay in `receipts/root_symbolic_central_homotopy_replay.json`. These historical files need not be included in the publication archive or run to build the paper. Each receipt describes its exact finite scope. New source-level correction/carrier/rank arguments are proofs, not claims established by those older finite tests.

## Exact primary versions and audit records

OpenAI family 295 is pinned to commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. Included upstream files are unchanged and retain Apache-2.0 terms and OpenAI attribution. Their repository authentication is in `receipts/pinned_sources.json`; the actual archive manifest separately hashes its included source files. The manuscript-specific README supplies the citation metadata. Fresh 7 October public-source checks found the same advertised main version and matched the primary PDF/source hashes; that does not establish that no later or unadvertised correction exists.

The complete user-supplied Roydor artifact has SHA-256 `2320e92723841bd9414c4d846a489bbe78d01a03403b8078ca43354407cfacb4`, size 431,430 bytes and 26 internally numbered pages. It is the December 2020 publisher-formatted “2nd Reading” version with DOI `10.1142/S1793525321500151`, not a byte-certified copy of the final 2022 issue layout. The full text was read, with pivotal pages visually checked; the repository-only identity/provenance record is `receipts/roydor_user_supplied_source_20261007.json` and is not an archive dependency. Its PDF, text extraction and renders are local-only and excluded from the deposit. To independently inspect it, obtain the corresponding complete primary article legitimately; the source hash authenticates the artifact actually used rather than promising that every available layout has identical bytes.

Current proof/audit records are `research/roydor_full_conventions_20261007.md`, `research/roydor_full_proof_scope_attack_20261007.md`, `research/nonseparable_typei_extension_20261007.md` and `research/involutive_deformation_adversary_20261007.md`. They identify their own source coverage and limits. The morning priority report `research/priority_audit_20261007.md` preserves its initial restriction finding and includes a separately timestamped completed final-candidate follow-up. These are dependency/mechanism/priority records, not complete-package review certificates. Locally retrieved third-party PDFs/text without identified redistribution rights must not enter the supplement.

## Repository-only static Lean evidence and unverified kernel reproduction

These historical Lean audit files are repository-only evidence; they are not required to build the paper and the publication archive does not promise to include them. For an optional static reproduction from the repository, acquire the pinned upstream commit and preserve the 372 paths/hashes in `research/lean_audit/import_closure.json`. `research/lean_audit/static_audit.py` reads that manifest's source paths; adjust only a local copy of its checkout-prefix paths on another machine. It ignores nested comments and strings before scanning source tokens. Root independently checked every source hash in `receipts/root_lean_source_hash_check.json`. Neither scan executes Lean or determines proof-term axiom dependencies.

The aborted setup used Lean 4.34.1 and mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612`. Small setup/probe/failure records are under `receipts/lean_attempt_*`; the exact OAI source build copy is ignored/local-only under `research/lean_audit/build`. Read `research/lean_audit/kernel_build_report.md` and `research/lean_audit/selective_retry_report.md` before another attempt. Dependency setup ran out of disk before successful `MainResult` compilation/import or a `#print axioms` result. The present evidence is static authentication, not reproduced kernel verification. The formal statement's direct scope is abstract Banach-predual algebras, and the general concrete-to-abstract bridge is unfinished in the pinned mathlib.

Formal reproduction is optional additional validation when relying on the independently audited mathematical proof; it is required before asserting reproduced formal verification. The full consequence itself is not formalized. At this snapshot, license selection for the new paper/prose supplement is pending; unchanged third-party source retains its original terms. No complete final package has yet been reviewed or published at this snapshot.
