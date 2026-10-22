# Independent acceptance packet for problem 30005994

Read ACCEPTANCE.md for the complete mathematical audit, exact source scope, acceptance limits, and the original verifier's non-blocking membership weakness.

The original author report is accepted as UNSOLVED for the general convex-potential question after five substantive approaches. No full solution, genuine counterexample, or novelty claim is certified. No publication is performed by this packet.

Run from any working directory:

`python -I -B verify_audit.py /absolute/path/to/author/public /absolute/path/to/author_frozen.zip`

The strict gate checks its own manifested files, all seven pinned author files, original ZIP bytes and membership, and normal/optimized replays of both 43-check suites. Python 3 and SymPy 1.14.0 are needed for the author's replay. The independent verifier itself uses only the Python standard library:

`python -I -B verify_independent.py`

AUTHOR_BASELINE.json identifies the unmodified reviewed object. AUDIT_MANIFEST.json identifies this audit's payload. CONTROL_RESULTS.json records positive and deliberately failing controls. BYTE_AND_REPLAY_AUDIT.json records the initial byte and membership findings; its original subdirectory PASS is a documented verifier weakness, not a mathematical acceptance or a failure of the new strict gate. SOURCE_REVIEW.json distinguishes local byte verification from public-web inspection. No source document, dataset content, or private coordination file belongs to this public directory.

Keep the separately supplied audit ZIP hash as the external freeze anchor. The manifest excludes itself and is not a digital signature. A changed payload needs a new review, even if its manifest has been recomputed.
