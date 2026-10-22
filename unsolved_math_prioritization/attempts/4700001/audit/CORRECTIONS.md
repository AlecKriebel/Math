# Corrections and hardening record

Audit date: 2026-10-04. Input: the eight files bound by the original external freeze manifest, SHA-256 c1af53c8f215aff4236e2490d01a81d2502c82e36e6f9c36c5779b00df6972f4.

## Frozen packet

No material mathematical correction was found. The original files have not been edited.

One low-severity test-hardening issue was found in `check_numeric.py`: the refinement comparison uses `zip(rr, refined_roots)` without first asserting equal list lengths. If one refined root were absent, the comparison could silently check only the retained root; an empty refined list would instead cause `max()` to fail. In the actual frozen and replayed data, every refined list contains exactly two roots, with the stated stability signs. The independent audit explicitly checks both counts and independently integrates all six refined roots. Suggested future change: assert `len(refined_roots) == len(rr) == 2` before the zip comparison. This is not a correction to the recorded numerical result or the analytic theorem.

The original symbolic checker verifies moments and the displayed return polynomial but does not itself compare every perturbation recurrence through order four. This is a coverage limitation, not a claim failure: the accompanying proof supplies those steps. The audit checker adds the full recurrence and full fourth-order integration independently.

No rigorous finite numerical epsilon cutoff has been supplied for the two-cycle theorem. In particular, the three floating-point controls do not become existence certificates merely because the asymptotic proof is sound. The packet already states this limitation correctly.

## Audit checker development

The first run of the new checker stopped at the reciprocal positivity identity because it used Python/SymPy structural equality between differently factored but algebraically equal expressions. The checker was changed to test the simplified difference against zero. This was a checker representation error; the identity and frozen proof did not change. No result from that incomplete run was reported as a pass.
