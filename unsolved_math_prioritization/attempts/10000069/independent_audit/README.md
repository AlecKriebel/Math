# Independent audit packet

Target: rank 711, problem 10000069 / AMR-099-0069.

Verdict: qualified credited spectral characterization accepted with one minor reconstruction erratum; no unqualified full-shape or closed-form resolution.

- AUDIT.md: full analytical review and exact acceptance boundary.
- ERRATA_AND_SCOPE.md: the second-moment equality correction and required qualifiers.
- EXACT_BINDING.json: immutable input binding, fresh source hashes, and replay evidence.
- INDEPENDENT_CONTROLS.json and independent_controls.py: 156,596 exact independent assertions.
- NEGATIVE_CONTROLS.md: rejected shortcuts and analytical safeguards.
- SOURCE_UPDATE.md: newly found primary preprint and explicit limits of inspection.
- PUBLIC_SOURCE_VERIFICATION.json: public source titles, URLs, hashes, sizes, and inspection metadata.
- RESULTS.json: machine-readable disposition.
- verify_audit.py: replay and binding checker.
- MANIFEST.sha256: hashes of this packet's other files.

Replay: python3 verify_audit.py /path/to/original/safe_output

The original ten-file directory is untouched. This separate packet contains authored audit material, reproducible verification code, and public verification metadata only. Downloaded PDFs, source extracts, images, raw service records, and private coordination are excluded. No remote changes were performed.
