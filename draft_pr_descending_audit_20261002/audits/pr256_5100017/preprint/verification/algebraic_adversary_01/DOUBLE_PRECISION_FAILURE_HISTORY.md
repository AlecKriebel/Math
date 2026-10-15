# Diagnostic generator failure and repair history

This history records failures of the independent audit's numeric family generator. It does not describe failures of the submitted theorem, submitted proof, or submitted author verifier.

The independent source began with explicit inner-ellipse tangent contacts, a second outer-ellipse intersection, and 60 iterations of double-precision λ bisection for each primitive N,k. The target was total lifted central angle 2πk. Raw Cartesian moment checks used the normalized threshold 2e−8 and multiplied the centroid denominator out, so the diagnostic also tested points on the zero-area locus.

1. First broad run: after the exact checks, `independent_verifier.py` returned exit code 1 with this assertion:

       AssertionError: ('moment', 1.7316632969461483e-07, (1.7, 20, 9, 0.0))

2. Selective repair: 90-digit tangent construction and λ bisection were introduced for families whose inferred b²−λ was below 1e−8 b². A second family outside that selection still used double generation, and the script returned exit code 1 with:

       AssertionError: ('moment', 5.311199719618375e-08, (4.3, 28, 11, 0.317))

3. Final repair: every tested family was tuned and generated with 90 decimal digits and 160 bisection iterations. Projection, signed area, raw moment, reflection, reversal, and scaling diagnostics remained separately evaluated with ordinary floating arithmetic. The original 2e−8 threshold was retained. The complete run returned exit code 0; its normal standard output is `verifier_stdout.json`, and the machine-readable evidence is `INDEPENDENT_EVIDENCE.json`. No additional broad run followed.

The original full first-run and selective-repair script snapshots were not preserved before editing. Their exact failure records above are preserved from the tool results. `double_precision_failure_reproducer.py` is a reconstructed minimal source for both original generator paths, with only those two family cases. It reproduces the observed residuals exactly and returns exit code 0 only after asserting that the original diagnostic fails and its 90-digit replacement passes. Its normal standard output is `double_precision_reproducer_stdout.json`.

| Family | Original maximum residual | 90-digit generated maximum residual |
|---|---:|---:|
| a/b=1.7, N=20, k=9, phase=0 | 1.7316632969461483e−7 | 1.1025968495928332e−14 |
| a/b=4.3, N=28, k=11, phase=0.317 | 5.311199719618375e−8 | 3.52163460817876e−14 |

An earlier symbolic run was manually interrupted because expanding an unnecessarily nested rational expression produced excessive CAS work. Cross multiplying the already-proved nonzero denominator instead of expanding it resolved that runtime issue; the exact checks then completed in well under a second. It did not produce a failed mathematical identity.
