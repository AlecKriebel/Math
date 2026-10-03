# Publication change map

Reviewed freeze manifest SHA-256: `327e376b1d14851e89294fbe8a67e1476a14eacbac3ffb3dab35c5f9313a08a9`. Its exact bytes are preserved as REVIEWED_MANIFEST.json. The original frozen directory was not modified.

- SOURCE_CERTIFICATE.md, GATE_REPORT.md, turns.jsonl, verify.py, and verify_results.json are byte-identical to the reviewed originals. No mathematical repair or extension was made.
- README.md records the completed independent review and links the audit and portable controls.
- source_record.json replaces pending review/publication fields with independent PASS and draft-PR metadata.
- RESEARCH_LOG.md records the completed audit and publication checkpoint.
- AUDIT_REPORT.md is the complete unchanged independent report, SHA-256 `d95d0320916c97a499fd53bdae0f543d890b0c79bb987f02cf04c99cae735ecb`.
- independent_controls.py and independent_controls_results.json are the unchanged independent diagnostic implementation and expected output. The script uses only the Python standard library and writes beside itself.
- MANIFEST.json binds the assembled publication files.

The mathematical outcome remains a negative consequence of prior constructions, recorded as already_solved1/5. No paper explicitly resolving the named Morgan–Pansu question was located.
