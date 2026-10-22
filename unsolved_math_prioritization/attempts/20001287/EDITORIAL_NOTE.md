# Post-audit editorial note

2026-10-03 UTC. Problem 20001287 / AIM-CONVEX_GEOMETRY-0019.

The full independent audit has verdict **PASS_FULL_PRIOR**. The frozen author packet remains byte-for-byte unchanged. Statements in that packet describing review as pending record its earlier freeze state; the full later report is in `audit/AUDIT_REPORT.md`.

Two nonblocking clarifications from that review:

1. The ordinary spherical-volume bound is **sₙ₋₁² / 4ⁿ**, where sₙ₋₁ is the total area of Sⁿ⁻¹. The exponent is 2. Any comma-like spacing artifact in the frozen display has no mathematical meaning.
2. The finite checker runs **18 rational matrix instances, comprising 17 distinct matrices**. Two of its one-dimensional instances coincide. The universal proof does not rely on the number of examples.

To reproduce the complete portable audit from this attempt directory, run:

`python3 audit/audit_controls.py .`

This replays the author checker in a temporary directory and leaves the frozen author files unchanged. Its output matches the included `audit/audit_controls.json`.

The original mathematical target is completely answered by a classical theorem deduction: Fradelizi–Meyer (2007), Proposition 1, and Lehec (2009), Lemma 8 and the dual-cone application. The all-dimensional normalized bound is 4⁻ⁿ and equality holds precisely for orthogonal orthants. Mathematical target completion: **100%**. No novel theorem or first historical explicit resolution is claimed. The appropriate queue disposition is **already_solved, 3/5**.
