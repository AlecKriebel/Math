# Final release status

Problem 20001670 / AIM-GEOMETRY-0008 remains **UNRESOLVED after 5/5 substantive proof attempts**.

The complete full audit passed the stated partial results with two minor rigor clarifications. The correction-only v2 release applied those clarifications; the complete narrow audit now records PASS. No further proof change was made after that review. The original and correction-only freezes are preserved. Pending-review wording in the v2 README, change map, and research log describes the historical pre-review checkpoint; the included NARROW_RELEASE_V2_AUDIT.md and this status supersede that pending status.

The results are p-dependent universal lower comparisons and strict segment comparison for sufficiently thin triangles at each fixed p. They do not settle global segment minimality, provide a p-uniform or explicit numerical thinness threshold, or establish novelty. The audits are independent AI reviews of an AI-assisted, unrefereed package; they are not journal peer review.

Run python3 verify_constants.py for the portable standard-library checks. The exact rational assertions are mathematical checks; floating-point gamma-function output is illustrative and may vary in its last digits across Python/libm platforms. The recorded checks.json was reproduced byte-for-byte in the research and review environment.

Reviewed correction-only manifest SHA-256: 3399f4db86a4dddcbb7ad1c5cf278c164037cf7317b12e4492a58e78900ee328.
Full audit SHA-256: fae43a8e62fb0e6da8c7baaa4c7b166cc7fede134984cc556dabf6081385eac1.
Narrow audit SHA-256: 9b7a86042e4cd69a5f0476e440de5f95f9ae95bb969251381b37db3b433f86f3.
