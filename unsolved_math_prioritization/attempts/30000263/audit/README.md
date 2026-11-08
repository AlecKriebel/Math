# Independent Bahri Xu audit package

Verdict: ACCEPT PARTIAL RESULTS; NO GENERAL RESOLUTION.

Read AUDIT_REPORT.md for the complete mathematical audit, the exact external
uniformity dependency, boundary cases, and numerical limitations.
MANDATORY_CORRECTIONS.md records that no mandatory correction was found.

This source-free archive contains only authored audit text, authored verification
code/results, and public verification metadata. It excludes PDFs, extracts,
screenshots, dataset contents, and private coordination material. It neither
includes nor modifies the separate authenticated author archive.

Python 3.10 or newer, standard library only:

    python verify_audit.py
    python -O verify_audit.py
    python audit_controls.py

To authenticate the author ZIP and independently replay its 24 saved outputs:

    python verify_audit.py --author-zip AUTHOR.zip

To recheck the complete external inputs, add:

    --corpora CATALOG.json PROBLEMS.json REPORTS.json --source-dir PDF_DIRECTORY

The PDF directory must contain owr2005_29.pdf, xu2006.pdf, chen2021.pdf,
lan_lu.pdf, and chen2021_journal.pdf. Their public URLs, hashes, and sizes are
recorded in INPUT_SOURCE_CHECKS.json. Missing optional inputs are explicitly
reported as NOT_PROVIDED. An unsupplied source is never reported as verified
by the current run.

audit_controls.py accepts the same optional input flags. With every input
supplied it runs 26 cases, including normal/-O relocation and bit-flipped
external inputs. It does not alter the originals.

The finite identity tests and output replay do not prove the general
conjecture. The report contains the analytic reasoning accepted by this audit.

pack_audit.py is only for an intentional revised copy. It rewrites the internal
manifest and builds a deterministic ZIP outside the package directory:

    python pack_audit.py --output ../AUDIT.zip

An independently supplied ZIP digest authenticates a freeze. Rebuilding a
manifest does not authenticate an arbitrary edit. No validation relies on
Python assert, and the default verifier performs no writes or network calls.
