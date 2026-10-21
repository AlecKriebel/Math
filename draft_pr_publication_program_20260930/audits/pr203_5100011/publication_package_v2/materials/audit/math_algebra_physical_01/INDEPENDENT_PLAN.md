# Frozen independent plan

UTC: 2026-10-16T07:32:16.212417+00:00

Before reading original PROOF.md, original verify.py, or favorable audit reports.

Hypothesis under adversarial test: For a>b>0 and a fixed proper nested confocal elliptical caustic, a primitive elliptical billiard orbit whose LEAST period N is divisible by four has phase-independent product of (i) signed original trajectory area and (ii) signed area of perpendicular feet from every fixed finite real M to original trajectory side lines. Coprime star windings, reversed orientation, zero and negative pedal areas are included. No parity converse or repetition-based extension is assumed.

Independent mechanism: derive feet and shoelace formula directly, isolate polynomial dependence on M, then generate actual billiards by caustic tangent from each boundary point followed by the second intersection of that line with the outer ellipse. Verify tangency, inward contact, reflection and closure independently. Select caustic parameter by closure rotation, avoiding author Jacobi implementations. Reconstruct an exact 4-period orbit family from reflection/tangency geometry and arbitrary-M formula; test deliberately wrong coefficients/products using explicit exceptions under ordinary and optimized Python.

Plan: (1) inspect primary source claim and source metadata; (2) complete fresh tangent/projection/area/reflection derivation and exact N=4 check; (3) implement direct physical arbitrary-precision checks N=4,8,12,16,20, including stars and near-circle/elongated cases, phases and M=origin/focus/generic/large; (4) probe reversal, zero/negative pedals, odd repetitions, excluded padded primitive periods; (5) freeze independent evidence before reading original proof/code; (6) audit all original proof dependencies and full code without executing original; (7) run inspected originals only in a disposable child directory and count enforced checks/retained stdout/provenance; (8) report strongest verified claim and exact gaps. Numerics are noninterval diagnostics and cannot prove a universal theorem.

Completion estimate: 2%.
