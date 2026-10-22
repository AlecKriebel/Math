# Post-Lie nonexistence with a semisimple target

Current manuscript: `note.tex`; separate paper: `post-lie-note.pdf`. Current metadata is `metadata.json`, copied exactly into `zenodo-deposit.json`. The exact two deposit assets are `post-lie-note.pdf` and `post-lie-verification.zip`. Proposed identity: Alec Kriebel, Independent researcher, ORCID 0009-0001-9320-500X; preprint, 2026-10-16, version 1.0.0, open CC BY 4.0.

The manuscript proves that equal-dimensional finite-dimensional complex Lie algebras `g`, `n`, with `g` unimodular and `n` semisimple, admit homomorphisms `j1,j2: g -> n` with invertible difference only if `g` is semisimple. Consequently no post-Lie product exists for a finite-dimensional complex perfect nonsemisimple source and semisimple target. It credits Burde's OWR 46/2023 formulation with Dekimpe, Burde–Dekimpe–Monadjem's partial results, Burde–Dekimpe's solvable-unimodular predecessor and Baues's determinant method. The priority comparison is bounded by inspected primary passages: it certifies neither firstness, current openness nor exhaustive coverage. The original body of Onishchik's 1969 work was inaccessible; that is an access limit, not an identified competing theorem.

AI systems were used extensively in solving, checking and writing this work, including separate AI-agent adversarial reviews of the arguments. This is an unrefereed preprint. No completed human peer review or formal machine verification is claimed; the finite diagnostic tests do not establish the global proof.

This package preserves the historical PR894 / problem 30005737 packet, current manuscript sources and scoped independent audits. Original effort remains **1/5**. Integrity and finite diagnostics are not formal proof, novelty certification or publication approval. Read the actual manuscript, current parent dispositions and `EDITION_HISTORY.md` together. The tool checks only a PDF header; separate parent compilation/export and visual-QA receipts do not change that contract.

## Authenticate before execution

Use trusted Python >=3.11 and its standard library. Independently obtain/check startup `portable.py`, package-index and current-manifest SHA256 pins. A self-reported hash or adjacent index does not authenticate startup. Reviewed tool SHA256: `a5b5ab7a3b0397e1d21bd70d3637ef1e200a7eba50419c0052e357b46a0e1d9c`; authenticate this through an independent channel as well.

Variables below are independently checked values. Pins are not embedded in their own indexed content. `PACKAGE_ROOT` is the portable directory: the extracted ZIP root, or `verification` in the complete candidate. `CURRENT_ROOT` is the complete candidate. Receipt/output parents must be ordinary nonsymlink directories physically outside every indexed/native/primary input tree; receipt directories and output files themselves must be fresh.

```sh
python3 -I -S -B "$PACKAGE_ROOT/portable.py" verify "$PACKAGE_INDEX_SHA256" --root "$PACKAGE_ROOT" --verify-only
python3 -I -S -B "$PACKAGE_ROOT/portable.py" verify "$PACKAGE_INDEX_SHA256" --root "$PACKAGE_ROOT" --receipt-dir "$FRESH_RECEIPTS"
python3 -I -S -B -O "$PACKAGE_ROOT/portable.py" verify "$PACKAGE_INDEX_SHA256" --root "$PACKAGE_ROOT" --receipt-dir "$ANOTHER_FRESH_RECEIPTS"
python3 -I -S -B "$PACKAGE_ROOT/portable.py" build "$PACKAGE_INDEX_SHA256" "$FRESH_BUILD_DIRECTORY/post-lie-verification.zip" --root "$PACKAGE_ROOT" --receipt-dir "$BUILD_FRESH_RECEIPTS"
python3 -I -S -B "$CURRENT_ROOT/portable.py" current "$CURRENT_MANIFEST_SHA256" --root "$CURRENT_ROOT" --receipt-dir "$CURRENT_FRESH_RECEIPTS"
```

Verify/current replay by default; build always replays. Each replay launches one genuine isolated wrapper plus eight genuine isolated children. The unchanged original root executes **inside** the wrapper, not as another OS process. Its two requested diagnostics run at actual optimization 0 and 1. Six additional children reject invalid R=I, original `require(False)` and corrupt checker bytes in both modes. The 2,896 checks are finite diagnostics, not proof coverage. Actual `-I -S -B` and startup-environment filtering protect children. The selected interpreter/stdlib and OS remain trusted; no OS sandbox or general concurrent-mutation protection is claimed.

Verify-only executes zero archival code and reports `VERIFY_ONLY_BYTE_AUTHENTICATION_NO_ARCHIVAL_EXECUTION`; it rejects a receipt directory. Build has no verify-only option. Replay records actual UTC start/end, PID, return code and raw stdout/stderr hashes before outcome checks, including failures. Omitted receipt paths produce retained system temporary directories. Private process evidence is outside this public archive.

The verification ZIP has sorted regular ASCII-relative members, fixed 2026-10-16 timestamp, 0644 permissions and level-9 DEFLATE. Exact compressed bytes require identical inputs and the same Python ZIP/zlib runtime. The paper PDF is separate. Current mode binds both assets to the external outer-manifest pin and compares the rebuilt ZIP and exact outer/inner tool, TeX, metadata and deposit copies.

## Preserved evidence

The paths `source/`, `audits/`, `root_evidence/` and `history/` below are relative to `PACKAGE_ROOT`, which is `verification/` in the outer candidate.

`source/` preserves exactly 18 original files, 91,564 bytes, including the nine-member author archive. `root_evidence/SOURCE_MANIFEST.json` binds their bytes and original Git blob IDs. Original labels are historical.

`audits/` contains each of eight complete accepted safe payloads plus its unchanged original safe manifest/schema. These are preserved scoped reports, code and curated public evidence, not a newly executed integrated suite. The complete 20-file `publication_tools_01` safe envelope retains explicit **NOT ACTUAL PAPER** TeX/metadata/index fixtures and omits its 18 private source-fixture copies. Its fixtures are historical, not the current manuscript. Scripts requiring original private fixtures/corpora are not self-contained runnable suites here. Default `portable.py` diagnostics are self-contained and need no private input.

Optional `history/note_author_01/` preserves six author snapshot files plus its safe manifest. It is a dated draft snapshot; pending labels there are historical. Current top-level/portable preprint bytes and explicit current parent editorial/PDF/priority dispositions are authoritative. The format review preserves three failed reviewer expectations from a falsified launcher hypothesis, superseded by its corrected launcher disposition. Classical-priority label errata and superseded reports retain their corrections. A render receipt's earlier pending state is qualified by the later explicit visual-QA disposition. See `EDITION_HISTORY.md`.

## Optional original-input authentication

Default diagnostics need no native corpora or primary PDFs. The optional source-only route authenticates **all three complete corpora before the first JSON parse/target extraction**:

```sh
python3 -I -S -B "$PACKAGE_ROOT/portable.py" source-only --catalog "$COMPLETE_CATALOG" --problems "$COMPLETE_PROBLEMS" --reports "$COMPLETE_RESEARCH_RESULTS"
python3 -I -S -B "$PACKAGE_ROOT/portable.py" source-only --catalog "$COMPLETE_CATALOG" --problems "$COMPLETE_PROBLEMS" --reports "$COMPLETE_RESEARCH_RESULTS" --primary-dir "$CLOSED_FIVE_PRIMARY_PDFS"
```

The optional directory contains exactly `owr2023.pdf`, `perfect-v1.pdf`, `perfect-author2024.pdf`, `rigidity-v1.pdf`, `etingof2024.pdf`. This is the five original pinned inputs, **not all manuscript references** or verification of their theorems. Raw corpora and scholarly primary bodies are excluded. Default verification requires no network, install or external communication.

## Published record

Published preprint: [10.5281/zenodo.23414025](https://doi.org/10.5281/zenodo.23414025). Two successive NEW independent whole-package reviews cleared the same253-file package before merge. PUBLICATION_RECEIPT.json records the accepted revision, final review evidence, production deposit and unique tracker row. This later outer README/manifest annotation adds the receipt; the four-page paper, metadata and242-member verification archive remain unchanged. The README inside the ZIP is the frozen pre-publication version.
