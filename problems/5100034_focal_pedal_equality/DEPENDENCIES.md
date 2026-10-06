# Credited dependencies and review inputs

This candidate combines parity-free local arguments already present in two reviewed campaign proofs. It does not count their original development as independent new work.

## PR210: outer focal-pedal trace

- PR: https://github.com/AlecKriebel/Math/pull/210
- Commit:2180d64b648b81ac660a792f7823d0b715f9cf12
- Proof: https://github.com/AlecKriebel/Math/blob/2180d64b648b81ac660a792f7823d0b715f9cf12/unsolved_math_prioritization/attempts/5100033/PROOF.md
- Proof SHA256:5a78b9d2fb1f7a0a80e556f2e2b759875bdbba055a454c148524eb44879add7e
- Review: https://github.com/AlecKriebel/Math/blob/2180d64b648b81ac660a792f7823d0b715f9cf12/unsolved_math_prioritization/attempts/5100033/independent_review/INDEPENDENT_REVIEW.md
- Review SHA256:176e087962884e5d58c43bf133dc77844817c60ba6ec30ca7a62d1400418ae6a

Its final odd-period product theorem is a different target. The actual tangent-foot formula, exhaustive complex pole locations and adjacent collinear-residue cancellation in its §§2–4 hold without that final parity step. Those local arguments are reproduced in TURN_1.md, with all-period lattice bookkeeping made explicit.

## PR261: original focal-pedal local cancellation

- PR: https://github.com/AlecKriebel/Math/pull/261
- Commit:7b7fcd63d5ea83df3a4c29853c4ba34b93d16f07
- Proof: https://github.com/AlecKriebel/Math/blob/7b7fcd63d5ea83df3a4c29853c4ba34b93d16f07/unsolved_math_prioritization/attempts/5100021/PROOF.md
- Proof SHA256:f7aada9e28e92c6fab920f1330366acd6eaba8006b4cd0ce52e2dbd58e7ef5b9
- Review: https://github.com/AlecKriebel/Math/blob/7b7fcd63d5ea83df3a4c29853c4ba34b93d16f07/unsolved_math_prioritization/attempts/5100021/independent_review/INDEPENDENT_REVIEW.md
- Review SHA256:c7cc49d934eca5090e17d70c821552fd1e995f3ae1f25f645caf868cb4361630

Its final pedal–antipedal product for period divisible by four is a different target. Its §5 original focal-foot formula, even local double-pole germ and odd neighbor-difference cancellation, and §7 strict pedal positivity are parity-free. The even-period reduced trace and final product conclusion are not imported into odd period. TURN_1.md redoes the exact common-lattice step and uses residue subtraction, not unproved division.

## Classical inputs

Stachel's canonical parametrization and midpoint contact geometry are existing theorems, with published DOI10.1007/s40879-021-00524-2. Classical Jacobi periods/addition/quarter shifts and compact-torus residue uniqueness are credited. The derivation is a source-specific companion consequence, not a historical-first claim.

All six dependency proof/review/manifest files are available as local review inputs in sources/. SOURCE_HASHES.json binds their bytes; DEPENDENCY_REVIEW_INPUTS.json records public commit paths. They need not be duplicated in a public target packet. The new proof needs its own separate full audit, since the two earlier verdicts do not automatically cover the all-period equality or the imported-constancy correction.
