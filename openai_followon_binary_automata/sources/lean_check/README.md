# Pinned minimal family-129 Lean check

Status: **not successfully reproduced**; dependency acquisition exhausted the shared filesystem before proof compilation. See `../../agent_notes/formal_reproduction.md` and `receipts/formal_reproduction_status.json`.

This preserves a byte-identical local-import closure from OpenAI/math commit adc7f1241b42e322a6451854ab7e4b4c146bf78a. It does not formalize the binary follow-on reduction. Original upstream material is retained for local research audit, not licensed here for redistribution. The adapted Lake configuration selects only the pertinent modules.

With adequate storage and installed Lean4 4.34.1, run `python3 bootstrap_and_build.py`. All generated files and downloaded dependencies remain in this folder's `.lake`. No upstream clone writes are performed. No Comparator validation was reproduced.
