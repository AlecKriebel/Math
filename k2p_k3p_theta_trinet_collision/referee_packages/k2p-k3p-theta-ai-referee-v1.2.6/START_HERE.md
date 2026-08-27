# Independent AI referee packet

This folder is a self-contained copy of the manuscript, mathematical
certificates, verifier source, stored reference transcripts, and PDF build
inputs for version 1.2.6 of *Exact Tree--Theta-Trinet Collisions under the
Kimura 2- and 3-Parameter Models*.

The packet is intended for an independent journal-style review. It does not
include prior referee reports, author rebuttals, review dispositions, research
logs, or release commentary. Their exclusion is deliberate: the requested
assessment should not inherit an earlier reviewer's conclusion.

## Suggested use

1. Give the referee the entire folder, or the sibling ZIP archive.
2. Ask the referee to open `AI_REFEREE_PROMPT.md` and follow it without being
   told what verdict is expected.
3. The referee should first read the manuscript and inspect the verifier code.
4. The referee may then run:

   ```bash
   bash ./RUN_REFEREE_REPLAY.sh --with-pdf
   ```

5. `REFEREE_REPORT_TEMPLATE.md` is an optional structure for the resulting
   report.

The replay script fails closed: before and after execution it rejects symbolic
links, checks the exact packet path set, and verifies every manifest-listed
SHA-256 digest. These unsigned digests establish internal packet consistency,
not authorship or external authenticity. The script runs the complete suite
normally and with Python optimization, compares focused outputs with the stored
transcripts, separately replays the strict-JSON/schema suite in both modes,
executes both K2P and K3P semantic-mutation guards, regenerates the compact K2P
certificate in a disposable copy, and optionally rebuilds all PDFs in a
temporary directory. A passing replay is
evidence about the supplied code and data, not by itself proof that the
implementation matches the manuscript; the referee prompt requires that
separate audit.

## Requirements

- Python 3.10 or newer; verifier execution uses only the standard library.
- For `--with-pdf`: `latexmk` or `tectonic`, plus `pdftotext`.
- A POSIX shell and ordinary utilities (`cmp`, `diff`, `mktemp`).

No network connection is required for the mathematical replay. Literature
checking may require external access at the referee's discretion.

## Contents

- `AI_REFEREE_PROMPT.md`: neutral review instructions.
- `REFEREE_REPORT_TEMPLATE.md`: claim-by-claim report structure.
- `RUN_REFEREE_REPLAY.sh`: fail-closed replay driver.
- `PACKET_PROVENANCE.txt`: exact source identity and scope.
- `PACKET_SHA256SUMS`: integrity manifest for every other packet file.
- `materials/combined-paper-clarified.pdf`: manuscript to referee.
- `materials/technical-summary-clarified.pdf`: author-supplied orientation;
  read it after the paper if independence is a concern.
- `materials/k2p_displayed_tree_clarification.pdf`: focused supporting note.
- `materials/*.tex`, `materials/references.bib`, and
  `materials/figures/`: reproducible document sources.
- `materials/strict_json.py`, `materials/verify*.py`, and `materials/src/`:
  strict input handling, verifiers, hostile tests, and certificate-generator
  source.
- `materials/CERTIFICATE_FIELD_COVERAGE.md`: author-supplied map of recomputed,
  consistency-only, informational, and transport fields; independently audit
  it rather than treating it as evidence of its own accuracy.
- `materials/certificate*.json` and
  `materials/*_certificate*.json`: exact certificates.
- `materials/verification_report*.txt`: stored expected transcripts; inspect
  them only after inspecting the code if avoiding anchoring.

All materials are copies. The canonical source files were not moved or
modified while this handoff folder was assembled.
