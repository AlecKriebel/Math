# Exact-checker validation

Completed 8 October 2026 at 18:01:27 UTC. Python 3.12.14; effective UID 1000.

## Recorded execution

The authored checker was run three ways:

- `python check_counting.py`
- `python -O check_counting.py`
- `python -OO check_counting.py`

During all three runs, the working directory had permission mode 0555, its input files had mode 0444, and `PYTHONDONTWRITEBYTECODE=1` was set. A real attempt to create a file in that directory raised `PermissionError`. Each process exited 0, wrote no stderr, and returned exactly the same 7,683-byte stdout. Input hashes were identical before and after the runs. Output capture was performed outside the read-only directory. Permission bits were restored afterward for packaging.

Common stdout SHA-256:

`bceedd5fd3210423942f9001d7e75ab0c8c1c15225917e2f2f2845ec82711959`

This equals the hash of `EXPECTED_RESULTS.json`. `EXECUTION_RESULTS.json` records the execution details. These are observed permission-bit and write-probe checks; they do not claim a separate container or mount-level sandbox.

## Coverage

- 12 synthetic point-set fixtures, including convex, one-interior, two-interior, collinear and straight-boundary cases
- Exact polygon counts compared with connected degree-two edge-subset enumeration for fixtures up to six points
- Inclusion–exclusion and hull-gap counts compared where their explicit limits permit
- All 1,096 forced-edge subsets of K3, K4 and K5 compared with canonical cycle enumeration
- The same-state continuation witness: 0 versus 1 completion
- The five-point triangulation example: 8 polygons, 2 triangulations, 12 incidences, multiplicities 1 and 2
- Convex-five comparison: 1 polygon and 5 triangulations
- Three metamorphic tests: nonsingular affine map, rational rescaling, vertex relabeling
- Eight rejection tests: duplicates, floating point, Boolean coordinates, oversized coordinates, excessive point count, collinear inclusion–exclusion input, excessive crossing events and excessive edge-subset input
- Empty and singleton input boundary checks

All validation conditions use explicit exceptions, not Python assertions. Optimized modes therefore execute the same checks. Geometric routines use integer/Fraction predicates without floating-point tolerance.

## Limits

The checker is deliberately factorial/exponential and capped. It is not an implementation of the cited subexponential algorithms. The checked fixtures do not establish behavior for all point sets. The two direct enumeration schemes share their segment predicates; the independently stated determinant certificates and proofs remain important.

The public report, source metadata and package manifest were assembled around the validated checker. No source PDFs or imported datasets are required to run it. All fixtures in the output are authored mathematical examples.
