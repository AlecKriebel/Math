# Integer endpoint discontinuity of normalized uniformization for positively curved surfaces

Alec Kriebel · ORCID [0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X) · preprint version 1.0, 3 October 2026

For every fixed finite integer `r >= 0`, the note constructs smooth complete strictly positive-curvature metrics on both the plane and the sphere that converge in ordinary compact-open `C^r`, while their unique point-normalized uniformizing diffeomorphisms fail compact-open `C^(r+1)` convergence. The critical `r=1` construction controls the full nonlinear inverse-coordinate curvature operator with a small `C^1` convex-radius correction. The theorem is proved in the standalone manuscript.

The normalization fixes `0,1` on the plane and `0,1,infinity` on the sphere, with orientation preserved. The theorem concerns the inverse of this specific conformal metric parametrization. It makes no assertion about abstract homeomorphisms, `RP^2`, the smooth topology or noninteger Hölder topologies. Each finite integer has its own sequence; planar positivity has no prescribed uniform positive lower bound.

AI tools were used extensively in mathematical construction, drafting, adversarial review, source research and verification. This preprint is unrefereed. No human peer review, journal acceptance or formal proof certification is claimed. Classical logarithmic and twisting mechanisms are credited; the bounded search qualification is explained in `SOURCE_QUALIFICATIONS.md`.

## Reproduce the finite exact diagnostics

From the extracted support directory, using Python 3.9 or later:

```sh
python3 -B verify_integer_endpoint.py
```

The checker uses only the Python standard library and explicitly refuses optimized Python (`-O` or a nonzero `PYTHONOPTIMIZE`), because its exact assertion checks must remain enabled. It writes deterministic JSON to stdout, creates no files, imports no manuscript or historical checker, and makes no network requests. A successful run reports `PASS_FINITE_EXACT_DIAGNOSTICS`. A recorded verification run stores its complete successful stdout as `expected_results.json`; compare the two JSON outputs or their exact bytes. `VERIFICATION_RECORD.json` binds the recorded run to the exact manuscript and checker.

Five rational Taylor controls check a nonorthogonal inverse-chart principal matrix, nonlinear inverse-map drift, the negative leading curvature term when the `r=1` correction is omitted, the convex-radius correction and the critical conformal-factor jet. The wrong reversed matrix order produces a different exact value. Further finite controls cover logarithm numerator homogeneity and coefficient bounds for derivative orders 1 through 7, Beltrami numerator homogeneity for `r=1` through 8, and six rational metric-reconstruction examples. These are exact algebraic diagnostics with explicit finite ranges, not a sampled numerical proof of the theorem.

The checker does not establish estimates for every derivative order, global cutoff-annulus curvature, completeness, normalized uniformization, or priority. Those conclusions depend on the written proof and the explicitly cited background results. In particular, the convex correction's universal constant is selected from the analytic bound in the proof; no diagnostic numerical constant replaces it.

## Portable files and archive

The support ZIP contains the standalone `.tex` source, checker, exact results, actual verification record, provenance, source qualifications, this README, mixed licenses, member checksums and archive builder. The final PDF is a separate upload. No third-party article bodies, primary images, administrative audit corpora, credentials or database snapshots are redistributed.

In an extracted copy without an existing archive, run:

```sh
python3 -B build_verification_zip.py
```

The builder checks the exact member set and `SHA256SUMS`, refuses overwrite, then reads every archive member back. Member order, timestamps and permissions are normalized for reproducibility. The normalized archive timestamp is a convention, not a research or execution timestamp; compressed bytes may depend on zlib. Exact member bytes are the portable target.

The manuscript and new documentation are licensed under CC BY 4.0. Python code is licensed under MIT. Cited publications retain their respective licenses and are not redistributed or relicensed.
