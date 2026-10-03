# PR384 source and Banach audit

Start with REPORT.md. The original problem remains unsolved5/5; scoped source/Turn1–2 disposition PASS with no mandatory corrections.

Reproduce the standalone independent controls from this folder:

    python3 -B independent_controls.py

Output must match independent_controls_receipt.json. The code imports no author programs. The snapshot and source binding receipts identify the exact frozen head and retrieved primary editions. Raw sources and private copied author replay files are ignored and excluded from MANIFEST.json.

MANIFEST.json binds every public audit artifact except itself. Verify its SHA256/byte entries before relying on this report.
