# 30000679 / OWR-1453-013

Both original questions have an affirmative prior resolution by Ealy–Krupiński–Pillay (2007 preprint; 2008 journal). This packet records the exact scope, the short connected-case consequence, and source verification. It does not claim novelty.

Start with RESULT.md and SOURCE_GATE.md. PROOF_READING.md records the inspected proof dependencies. ATTEMPT_LOG.md explains why the investigation stopped at 1/5.

## Reproduce the controls

Run:

    python3 verify.py --sources DIRECTORY_CONTAINING_THE_THREE_PDFS

The required basenames and public download links are in SOURCE_BINDINGS.json. Python's standard library and Poppler's pdftotext are required. Exact source bytes are hash-checked before text extraction. Source files are deliberately not distributed in this packet. The script makes no network request.

Without --sources, finite-group controls still run, but the source gate prints NOT_RUN_MISSING_SOURCES and exits 2. That is not a complete verification pass. A byte mismatch or content-check failure exits 1. CHECK_RESULTS.json records the successful author run. The tests are checks on finite algebra and document identity, not formal verification of the infinite model-theoretic theorem.

FROZEN_MANIFEST.json contains SHA-256 digests of every other author file. Review artifacts, if later added, must not be mistaken for part of this original freeze. Independent review is pending in this version.

OpenAI tools assisted research, drafting and controls. No human peer-review or historical-priority certification is claimed.
