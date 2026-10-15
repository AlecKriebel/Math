# Root postvalidation filename-case repair

2026-10-02T08:50:09.577839+00:00 — source-only one-line repair: Path.exists on this case-insensitive filesystem resolves the lowercase acceptance.json when asked for ACCEPTANCE.json. Verify actual literal directory entry names instead. Original helper and its actual failure receipt are preserved. No canonical/science/queue/state/history bytes are changed; original1/5,new0. Rerun the full postvalidation under identical gate pins.
