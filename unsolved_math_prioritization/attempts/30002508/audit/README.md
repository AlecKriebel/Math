# Portable independent audit

Verdict: correct partial-results packet, with a minor source-provenance clarification; full target unsolved.

- AUDIT.md: independent source/scope review, line-by-line mathematical audit, additional endpoint proof, and exact remaining gaps.
- CORRECTIONS.md: source qualification and optional endpoint strengthening. Frozen originals are unchanged.
- independent_controls.py: standard-library reproduction and independently constructed controls.
- independent_results.json: test outputs.
- frozen_inputs/: byte-for-byte copies bound to the original SHA256SUMS.
- AUDITED_INPUTS.json: input identity and hash bindings.
- AUDIT_RESULT.json: machine-readable disposition.
- MANIFEST.sha256: hashes of all audit files except this manifest itself.

Run:

`python3 independent_controls.py`

Then verify:

`sha256sum -c MANIFEST.sha256`

The first command produces deterministic output and runs the author replay in temporary storage. It never writes to frozen original inputs. No external packages, network access, private absolute paths, or downloaded third-party papers are required. Source citations are links, not redistributed source documents.
