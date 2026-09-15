# Bounded complex ultralimits

Checkpoint 2026-09-15T04:06Z. Bounded prerequisite completion: 100% compiled. This is a prerequisite for the separate Qqa-to-Qqc reconstruction; it does not by itself prove that inclusion.

## New module

`CyclicBell/GeneralCoverageUltralimit.lean` proves actual convergence of every uniformly bounded complex family along every genuine ultrafilter. It uses compactness of complex closed balls and Hausdorff uniqueness of limits. `naturalUltrafilter` is Mathlib's ultrafilter extension of `Filter.atTop`, rather than an assumed limit functional.

The module preserves constants, addition, negation, subtraction, multiplication, fixed scalar multiplication, conjugation, and finite sums. Eventual equality, norm bounds, nonnegative real parts, and complex-order nonnegativity transfer to the limit. Finite Gram positivity (both complex-order and real-part versions) and Hermitian kernel symmetry also transfer. Ordinary convergent sequences retain their usual limit along the chosen natural ultrafilter.

All laws require the stated actual boundedness or convergence premises. The total definition `ultraLimit` alone makes no assertion about unbounded families. No Hilbert realization, positivity of the limiting Gram form, or containment between quantum models is assumed.

## Verification

`lake build CyclicBell.GeneralCoverageUltralimit` completed successfully, including all three kernel-transfer endpoints. Build output: `coverage_ultralimit_build.log`. Focused axiom probe: `UltralimitAxioms.lean`, output `ultralimit_axioms.log`.

## Remaining integration

The moment-model agent constructs bounded actual PVM word moments. The independent GNS agent constructs the Hilbert space and bounded operators from their positive limiting kernel. The final inclusion must assemble those constructions and identify the limiting behavior. For a sequence-based extraction, finite input alphabets supply the relevant first-countability; an assertion for arbitrary uncountable alphabets would require a net-based argument. The ultralimit module allows arbitrary index types for that reason.

Axiom checkpoint 2026-09-15T04:10Z: all nine probed ultralimit/PSD-transfer endpoints depend only on `propext`, `Classical.choice`, and `Quot.sound`. Probe Lean process exited 0.
