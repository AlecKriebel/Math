# Source-free independent audit

Problem 30001518 / OWR-4412-008 / rank 976. Date: 7 October 2026.

**Decision: accept the five scoped partial approaches; retain unsolved, 5/5.** No mathematical correction patch is required. This is an independent computational/mathematical audit, not human peer review or a full solution.

Read `AUDIT_REPORT.md` for the complete source, geometric, analytic, and verifier review. `ACCEPTANCE.json` records the accepted claims and remaining gaps. `SOURCE_AUDIT_METADATA.json` contains public provenance and inspection scope only. `audit_results.json` records the actual executed tests.

The original author packet and ZIP remain unchanged. This audit directory contains no downloaded papers, extracts, rendered pages, dataset contents, or private coordination material.

## Replay

1. Check this audit's SHA256SUMS against its externally supplied manifest hash.
2. Run `python check_frozen_author.py /path/to/packet --archive /path/to/author_packet.zip` to verify the exact reviewed author freeze.
3. Run `python run_audit.py --author /path/to/packet --archive /path/to/author_packet.zip` for the complete local mathematical, optimization-mode, relocation, and corruption controls. Runtime varies with the machine.
4. Optional complete source/corpus byte checks: additionally supply `--source-dir /path/to/pdfs --corpus-dir /path/to/corpora`. Expected public filenames, lengths, and hashes are retained in source metadata. Omitted external inputs are explicitly NOT_RUN; they are never silently treated as verified.

The new mathematical verifier works under ordinary Python, `-O`, and `-OO`, using explicit checks rather than stripped assertions. The author's own scripts intentionally reject optimized modes. The independent checker was written separately from the author's tracer and tests; common reflection and line-intersection identities are standard mathematics.

A self-consistent rewritten manifest is not an authenticity certificate. The externally fixed author manifest hash is the acceptance anchor. The audit includes a deliberate coordinated-prose-and-rehash control showing this distinction.
