# Independent audit of the strong-Heegaard Fano diagnostic

Decision: ACCEPT UNCHANGED AS A RESTRICTED PARTIAL RESULT. KP-3.53 / ID 2851 remains unresolved, at 3/5 approaches. No manifold counterexample or novelty claim.

Read INDEPENDENT_AUDIT.md. The unchanged ten-file author package is retained as AUTHOR_SAFE_FREEZE.zip, with its exact original external manifest.

Run the complete pinned computational replay:

    python replay.py
    python -O replay.py

Run only the independent corner-band calculation:

    python independent_check.py

All use Python 3's standard library. The full replay checks exact input pins before extracting the safe archive, runs normal/optimized/relocated checks, exercises fifty explicit negative CLI outcomes, and repeats the independent computation. SOURCE_PIN_RESULTS.json records full-byte corpus and PDF verification; verify_source_pins.py can repeat those checks with locally supplied authorized inputs. No source documents or corpus contents are included.

The outer external manifest, distributed alongside the audit ZIP, is the root file-inventory and ZIP-integrity record. See ACCEPTANCE.json for the precise accepted author archive and status.
