# Ueno rationality independent audit

Verdict: qualified pass after the mandatory domain and dominant-component corrections in `CONTROLLING_CORRECTIONS.md`. The original target remains unfinished after five approaches. No proof, counterexample, novelty claim, or global-current-openness claim is supplied.

Read `AUDIT.md` for the full mathematical review and `CONTROLLING_CORRECTIONS.md` for the exact counterexample, corrected dense open, two inverse compositions, vertical components, and downstream rechecks. The corrections control interpretation of the frozen original; the originals were not modified.

The author replay passes 32 checks. The independent script passes 115 controls, including 11 explicitly labeled negative controls. Counts are reproducibility information, not a research-proof certificate. Standard geometric results and the cited diagonal-cubic classification are reviewed in the written audit, not formalized by the script.

Run this folder's read-only portable replay with Python 3 and SymPy 1.14.0:

    python replay_audit.py

To additionally bind and rerun the original frozen packet, pass its safe directory:

    python replay_audit.py --original-safe /path/to/original/safe

`input_bindings.json` binds the seven original payloads and original manifest. `source_bindings.json` records inspected public primary sources, independently recomputed byte hashes, and retrieval limitations. `negative_controls.json` and `audit_status.json` summarize the controlling outcome.

The safe manifest contains authored audit text, exact scripts/results, and verification metadata only. PDFs, screenshots, extracted source text, raw dataset content, raw connector responses, and private coordination are excluded. No remote write or queue change was performed. The neighboring ID 30002830 was assessed only for overlap; its method-specific question remains only partially covered and its budget is unchanged.
