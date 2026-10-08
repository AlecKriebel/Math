# KP-4.69 independent audit

**Accepted unchanged as partial/unresolved, with five mathematical approaches completed.**

The audit validates the relative-boundary Casson–Sullivan cancellation and the resulting finite interior-stabilized boundary extension. It does not establish an unstabilized smooth pseudo-isotopy or resolve the original existence question.

- `AUDIT.md`: full mathematical review, with the relative marking and excision arguments made explicit
- `AUDIT_RESULT.json`: machine-readable disposition and scope
- `ORIGINAL_FREEZE.json`: unchanged original candidate metadata
- `SOURCE_AUDIT.json` and `CORPUS_AUDIT.json`: public source/dataset verification metadata only
- `EXECUTION_AUDIT.json`: all 36 genuine UID-1000 read-only normal, `-O`, and `-OO` execution records, including 30 rejected invalid controls
- `independent_checks.py` and `INDEPENDENT_CHECKS.json`: independent exact matrix-ring and cycle-basis computations
- `reproduce_audit.py`: rerun the execution audit against the externally pinned original candidate
- `verify_audit.py` and `AUDIT_PINS.json`: verify this authored bundle with an externally supplied manifest hash

Reproduce the arithmetic and optimization controls:

`python -B reproduce_audit.py /path/to/pseudoisotopy_2945 /path/to/new_execution_audit.json`

Verify this bundle's bytes using the audit-manifest hash delivered separately:

`python -B verify_audit.py /path/to/audit/public EXPECTED_AUDIT_PINS_SHA256`

The original candidate tree hash is `9373856af6e529c088f6df98cc42e147f3b8730e00494a90af7781e62d90cf83`.

This directory contains only authored audit work and verification metadata. Source papers, source text, dataset contents, and private coordination materials are excluded. The unavailable original KS96 full text remains a disclosed dependency boundary. No publication or global queue change was performed by this audit.
