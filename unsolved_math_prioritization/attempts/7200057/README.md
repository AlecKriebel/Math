# Crossing minimizers and halving-line maximizers

Problem 7200057 / AMR-071-0057, rank 1064. Accepted corrected partial results; exhausted 5/5; general implication unresolved. Start with [the current report](current/REPORT.md), [the independent audit](audit/AUDIT.md), and [acceptance and limitations](ACCEPTANCE.md).

The universal implication is reconstructed for 3 through 7 points. The packet also contains weighted-profile tightness and corrected slack criteria, generic mutation/deletion lemmas, conditional propagation, and exact eight-point equal-crossing/unequal-halving witnesses proved nonoptimal. It does not claim a general resolution, novelty or best-known status.

## Verify

Use standard-library Python under actual UID=EUID=1000. Obtain the expected bootstrap SHA-256 from an independently trusted PR description or acceptance record. Authenticate `BOOTSTRAP.py` before running it; keep a trusted copy outside the candidate directory. Run:

    python -I -S -B /trusted/BOOTSTRAP.py /candidate/7200057 /candidate/unsolved_math_prioritization/QUEUE.md

Repeat with `-O` and `-OO` before the script path. The verifier rebuilds permission-read-only current/audit copies and freshly replays every safe mathematical output, complete stdout/stderr bytes, all ten semantic mutants, path controls and physical denied writes. All replay results are compared against `REPLAY_RESULTS.json` with exact recursive types and no normalization. Hostile-import, schema, inventory and anti-repin controls can be run after bootstrap authentication:

    python -I -S -B /candidate/7200057/mutation_tests.py --root /candidate/7200057 --queue /candidate/unsolved_math_prioritization/QUEUE.md --bootstrap-sha256 EXPECTED_EXTERNAL_SHA256

Run the controls in all three optimization modes. Authenticate the control code through the manifest first; it is not itself the initial trust anchor. `QUEUE_BINDING.json` records exact approved base and new QUEUE byte hashes and counts, and the required separately supplied QUEUE file is authenticated against that fixed binding before and after replay. The verifier also tests actual denied writes on a permission-read-only copy of those exact QUEUE bytes.

`PUBLIC_SCOPE.json` distinguishes historical metadata and the changed audit packaging from fresh computations. Original full replay, complete patch roundtrip, source/PDF/dataset binding and archive reconstruction are NOT_RUN; omitted inputs are not silently substituted. Full historical outer receipts are excluded. `REPLAY_RESULTS.json` is a new public-only receipt, not a transcription of them. Source bodies, corpus contents, private sources and coordination records are excluded.

No merge, release, DOI or outreach is part of this draft publication.
