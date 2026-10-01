# Versioned deterministic-output correction

Recorded2026-10-01T13:32:00Z, after the initial five-turn freeze. No mathematics or author-turn count changed. All original files and FROZEN_MANIFEST.json remain byte-for-byte unchanged.

The original turn1 checker traverses sets, so JSON dictionary key order varies with the Python hash seed. Its rerun JSON is semantically identical to the saved receipt: the same35 assertions, vertices, distances and scope. The problem is output ordering only.

`check_turn1_v2.py` changes only `json.dumps(..., sort_keys=True)`. `turn1_checks_v2.json` is its deterministic output, verified identical under three different hash seeds and semantically equal to the historical receipt. Use this v2 pair for byte-for-byte replay, or compare parsed JSON for the original pair. This supersedes only the overly broad byte-comparison implication for turn1 in RESULT.md; turns2–5 already replay byte-for-byte.

FROZEN_MANIFEST_v2.json binds every original artifact, the initial freeze and these three versioned additions. All five substantive turns remain exhausted, and independent review is still required. No claimed mathematical result or original status was changed.
