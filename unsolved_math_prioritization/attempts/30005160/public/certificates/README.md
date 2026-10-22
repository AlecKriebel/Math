# Computational proof dependencies

The 15 original program and result files are byte-identical copies of accepted authored dependencies. Initial assembly did not rerun them; the separate reader reproducibility review subsequently replayed all certificates in scratch copies. A separately authored checker is also included, bringing this directory to 16 program/result/checker files plus this guide. The mathematical acceptances reviewed the algorithms, analytic errors and tail bounds. Exact source hashes are in the [inventory](../CONTENT_AND_DEPENDENCIES.md).

## Integer and rational arithmetic

These computations use Python 3 standard-library integer arithmetic or fractions. The original programs require ordinary Python execution: do not use -O, -OO, or PYTHONOPTIMIZE. Some acceptance gates are assertions, so optimized execution is not validation. Displayed decimal values and elapsed times do not affect their verdicts.

- [certify_uniform_027.py](certify_uniform_027.py) and [certify_uniform_027.json](certify_uniform_027.json): the fixed K=7 triple in [Proof 19](../proofs/19_uniform_027.md).
- [certify_uniform_odd_family.py](certify_uniform_odd_family.py), [uniform_029.json](uniform_029.json), and [uniform_0211.json](uniform_0211.json): the fixed K=9 and K=11 triples in [Proof 20](../proofs/20_uniform_029_0211.md).
- [certify_four_circuit.py](certify_four_circuit.py) and [certify_four_circuit.json](certify_four_circuit.json): the uniform noncollinear mass-seven witness in [Proof 32](../proofs/32_uniform_noncollinear_k7.md).
- [check_middle_exact.py](check_middle_exact.py) and [check_middle_exact.json](check_middle_exact.json): the finite rational coefficient sum used in the corrected cubic middle-cone proof, [Proof 34](../proofs/34_cubic_middle_cone.md).

To reproduce, copy this entire certificates directory to a scratch directory, enter it, and run:

    python certify_uniform_027.py
    python certify_uniform_odd_family.py --K 9 --N 512 --bins 1024
    python certify_uniform_odd_family.py --K 11 --N 1024 --bins 2048
    python certify_four_circuit.py
    python check_middle_exact.py > check_middle_exact_reproduced.json

Several programs overwrite their adjacent output files. Run scratch copies if the packaged bytes are to remain unchanged. Elapsed-time fields need not reproduce byte-for-byte; the exact arithmetic verdicts and bounds are the relevant comparisons.

## Validated quadrature with a disclosed interval dependency

The following additionally require mpmath's real interval module. The original calculations use 45 decimal digits, exact rational coefficient inputs, outward rational output rounding, and the proved global quadrature errors. The real interval elementary primitives are a trusted numerical dependency; this is not a formal verification of the library.

- [certify_entropy_quadrature.py](certify_entropy_quadrature.py) and [quadrature_certificates.json](quadrature_certificates.json), with the one-phase error proof in [Proof 42](../proofs/42_validated_entropy_quadrature.md)
- [certify_green_quadrature.py](certify_green_quadrature.py) and [green_rational_certificate.json](green_rational_certificate.json), with the positive-radius error proof in [Proof 43](../proofs/43_validated_green_quadrature.md)
- [certify_rational_boxes.py](certify_rational_boxes.py) and [rational_box_certificates.json](rational_box_certificates.json), establishing all nontrivial sign vertices of the two boxes in [Proof 44](../proofs/44_rational_boxes.md)

Keep the programs together because the Green and box programs import helpers from the entropy program. From a scratch copy with mpmath available, run:

    python certify_entropy_quadrature.py --N 256
    python certify_green_quadrature.py --N 128
    python certify_rational_boxes.py

These certificates prove only the recorded individual comparisons and coefficient boxes. They do not prove positivity over an optimizer's search domain or at all additional circle-noise radii. The analytic strong-center full-cone theorem is separate and has no interval-library dependency.

## Portable replay checker

The separately authored [replay_reader_certificates.py](replay_reader_certificates.py) verifies all 15 original file hashes, replays all eight jobs in a new scratch directory, retains each original assertion as an explicit conditional exception in memory, and independently checks exact result predicates and equality to pinned output payloads. Only elapsed-time fields are ignored. It requires freshly generated results and never rewrites the accepted source files.

From the package root:

    python certificates/replay_reader_certificates.py

The checker itself supports Python optimization. For a specified new, nonexistent scratch path:

    python -O certificates/replay_reader_certificates.py --output-dir /a/new/scratch/path

Its --self-test option checks pins and ten rejection controls only; it does not replay certificate calculations. No quick replay mode is provided. The testing environment is Python 3.12.14 with mpmath 1.3.0. The interval-library trust boundary remains as described above.
