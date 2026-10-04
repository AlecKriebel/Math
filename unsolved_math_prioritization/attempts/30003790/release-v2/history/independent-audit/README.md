# Portable independent audit

Problem 30003790 / OWR-16161-003, rank 618. This folder is a separate audit of the frozen author packet, not an edit of it.

Read `AUDIT.md` for the verdict, source scope, proof review, and exact corrections. Read `AUXILIARY_CANDIDATE.md` only as a newly developed, not-yet-independently-reviewed extension. `VERDICT.json` makes this distinction explicit.

Run the new checks independently from any working directory:

    python3 /path/to/independent-audit/verification/audit_check.py

To additionally verify the frozen input hashes and reproduce its recorded output:

    python3 /path/to/independent-audit/verification/audit_check.py /path/to/frozen/public

The second form should reproduce `verification/audit-result.json` under the same Python floating-point implementation. All exact rational assertions are platform-independent. Tiny floating-point differences in numerical quadratures can vary across platforms; the mathematical assertions use tolerances. `verification/author-replay.json` is the byte-identical original replay captured during this audit.

No external Python packages, network access, source PDFs, private coordination files, or repository access are needed for the independent controls. The optional frozen directory is needed only for binding/replay. `MANIFEST.json` binds the audit files and lists the exact author input hashes. It excludes itself from its file list.

No novelty, global openness, or dimension-efficient solution is certified. The auxiliary proof must receive a fresh review before being used to change publication claims.
