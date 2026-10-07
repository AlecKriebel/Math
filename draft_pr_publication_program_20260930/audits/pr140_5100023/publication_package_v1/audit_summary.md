# Mathematical audit and reproducibility limits

Audits completed October 7, 2026 verified the theorem with the explicit even-least-period, strictly nested confocal-ellipse scope. The proof was tested through distinct algebraic/orbit and geometric/variational approaches before convergence. The following are actual completed checks, not prospective test plans.

| Check family | Evidence | Scope and limit |
| --- | --- | --- |
| Rational line-system reproduction | 686,292 explicit checks; 19,543 rational chords; 1,036 finite-rotation cases | Supports local formulas and parity controls, not numerical proof of billiard closure. |
| Separate symbolic/rational verifier | 12,846 explicit checks; 1,004 endpoint chords; three exact six-bounce orbits; 662 finite-rotation cases | Checks the local and sampled closed-orbit formulas independently. |
| Algebraic/orbit adversary | Seven unspecialized exact symbolic certificates; 594 rational chords; 65 physical orbits in 13 families; 39,761 explicit conditions per interpreter mode | Symbolic identities cover their stated algebraic relations; sampled orbits do not by themselves prove the all-period theorem. |
| Geometric/variational adversary | Four generic symbolic identities, 246 rational chords and 120 genuine periodic phases in 30 axis/period/winding cases; 6,553 conditions per mode | Independently generated positive-quadratic tangent-map orbits, including stars through period16/winding7 and a near-circle case. Numerical closure discrepancy at 75 digits was at most 1.71e-67, with tolerance1e-48 relative to the specified unit/axis scale. This is supplementary numerical evidence. |
| Repeated odd-period boundary | Exact 19-condition reflection/tangency/centroid witness for the triangle shown in the paper | Falsifies an even-list-length extension; does not contradict the least-period theorem. |

Both normal and optimized Python modes were used. The portable supplement replays the first two exact families and the 19-condition boundary witness, with eight deliberately false controls. Every false control was rejected; explicit exception guards remain effective under optimization. The positive portable replay counts agree in both modes. Runtime: CPython3.14.6; SymPy1.14.0 for the independent and boundary programs; the author program uses the standard library. Commands and actual replay outputs are under `verification/`.

The proof, rather than these finite runs, supplies the general circle-action symmetry, perimeter stationarity, and all-period averaging. Nonzero denominators follow from the strictly nested caustic; lambda=0, lambda=b², hyperbolic caustics and the noncircular coefficient at c=0 are not claimed.

The original verifiers contained assertion-based guards that could disappear under optimization. The publication versions use explicit exceptions. The original submitted mathematics was preserved; a source-attribution paragraph was qualified to avoid assigning a formal least-period definition to the source. These repairs were independently reviewed.

The bounded priority audit and its limits are in `priority_and_provenance.md`. Original imported review labels and finite computational counts are not represented as conventional human peer review. AI tools were used extensively; this note is unrefereed.
