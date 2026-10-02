# Reproduction and integrity scope

Use Python 3 and Poppler `pdfinfo`/`pdftotext` for these programs. The workspace's `.venv/bin/python` was used. All paths remain inside this family except the explicitly read-only frozen candidate and two immutable previous family manifests.

From `/Users/alec/Documents/Math`:

```sh
.venv/bin/python draft_pr_publication_program_20260930/audits/pr32_6800007/priority_flag_family/build_evidence_catalog.py
.venv/bin/python draft_pr_publication_program_20260930/audits/pr32_6800007/priority_flag_family/priority_binding_controls.py
```

These generate actual offline catalog/control results within this family, including retained-source size/SHA/PDF format and previous-family integrity. The final closed manifest binds the originally recorded outputs; rerunning programs changes timestamps, so reproduce in a copied family if its final seal must remain byte-exact. Source reading locations and judgments are in `SOURCE_READING_LEDGER.md`; program controls are not automated theorem or novelty checking.

Original URL retrievals were performed by `fetch_priority_sources.py`, `fetch_followups.py` and adaptive direct calls to the same `fetch` function. Their actual successes/failures, timestamps, redirected URLs and hashes are preserved in receipt JSONs. `replay_source_requests.py` consolidates every durable URL from those receipts without overwriting original bytes:

```sh
.venv/bin/python draft_pr_publication_program_20260930/audits/pr32_6800007/priority_flag_family/replay_source_requests.py --output-root tmp/source_replay
```

The replay destination must be a new directory in ignored `tmp/`. Network replay was not needlessly repeated after the inspected source set was recovered. It may return different bytes or access failures; no equality is inferred. Initial retrieval scripts overwrite their own original receipt/source files, so do not rerun them in a closed family. The replay program is the safe reproduction route.

The complete survey source was received only as raw primary PDF bytes from a separate successful root scholarly retrieval after this family's exact URL returned bot HTML. `SURVEY_RECEIVED_BYTE_BINDING.json` binds that read-only input and the ignored copied bytes. This is bounded retrieval independence, with fully independent content assessment; no root or sibling new priority report was read. Verify its PDF magic, 746579 bytes and SHA256 eb83de6334edafdbae8a9bd744fdc8c9abebbb05736bc9694a579203dfdfe81a. Its source URL is recorded alongside the unsuccessful request. Actual received-source conclusions supersede the initial access-gap record, while failed bodies remain preserved.

Borrelli's PS was converted with `ps2pdf` and then `pdftotext -layout`; that derived PDF is identified as a conversion. Other PDF text was extracted with `pdftotext -layout`. Scan-based Forstnerič proof reading reuses this investigator's own earlier complete scan/OCR read and fresh PDF hash rather than misrepresenting sparse fresh text extraction as a complete new read. Duchamp p.2 and Derdzinski–Januszkiewicz proof note were rendered and visually inspected.

The final first-party MANIFEST.json excludes itself, all foreign `sources/`, all `tmp/`, and caches. It binds reports, early seal, research log, actual first-party programs, receipts, control outputs and documentation. The manifest's integrity is not evidence of mathematical correctness, exhaustive bibliography, current openness or novelty. No write, commit, push, merge, release, DOI, tracker, queue change or individual outreach is part of reproduction.

Read-only closure verification:

```sh
.venv/bin/python draft_pr_publication_program_20260930/audits/pr32_6800007/priority_flag_family/seal_manifest.py --verify
```
