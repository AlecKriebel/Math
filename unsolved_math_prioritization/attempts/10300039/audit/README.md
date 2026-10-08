# Source-free independent audit

Read AUDIT.md and ACCEPTANCE.json first. The author packet itself is not modified or recopied here. This audit accepts only its corrected v2 partial mathematics, with status unsolved, 5/5 and explicit unresolved source-depth limits.

The audit ZIP and external manifest are separately pinned by AUDIT_PINS.json. Authenticate those pins through the trusted sender; the pins file does not authenticate itself.

The independent script requires the original pinned author distribution, its outer packet and external manifest, both complete private corpora, the original five PDFs, and their already inspected text extractions. Inputs remain local. Example:

    python3 -I -S -B audit_replay.py --delivery /path/to/frozen_delivery --packet /path/to/HYPERBOLIC_SEPARATION_10300039_AUTHOR_PACKET.zip --manifest /path/to/AUTHOR_PACKET_EXTERNAL_MANIFEST.json --problems /path/to/problems.json --reports /path/to/research_results.json --sources /path/to/source

Repeat with -O and -OO if desired. Run unprivileged. Keep the actual author distribution read-only. Python 3 and pdftotext are required. The script writes only disposable copies in a temporary directory and prints a JSON receipt; it does not modify the author release or transmit source data.

The three independent receipts are for the final audit script. The author-control receipt records a separate replay of the supplied frozen controls.py. Mathematical diagnostics are finite controls, not a formal proof checker.
