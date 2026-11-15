# An exact period criterion for focal-distance products in elliptic billiards

Alec Kriebel, independent researcher; ORCID 0009-0001-9320-500X.
Research note, 11 October 2026. Extensive AI assistance; unrefereed and not
conventionally human peer reviewed.

## What is proved

For a noncircular ellipse and a strictly nested nondegenerate confocal
elliptical caustic, each ordinary vertex-to-fixed-focus distance product is
constant along its periodic billiard family exactly when its primitive
least period n is 2 modulo 4. Primitive star turns and both orientations
are covered. Both focal products agree at every phase for even n.
A repeated traversal takes the positive primitive product to an integer
power, so the criterion depends on least period, not listed return length.
Circles are a separate trivial case. Hyperbolic and degenerate caustics
are excluded.

This proves the primitive interpretation of the experimentally recorded
k114 observation in Reznik–Garcia–Koiller's Table 2. The paper also supplies
an exact doubled-triangle counterexample to an unrestricted return-length
interpretation. The parametrization and meromorphic divisor method are
classical; no new-method or exclusive-priority claim is made. See
SOURCES_AND_PRIORITY.md for what was and was not checked.

## Files and use

The PDF is deposited separately. This support archive includes its
standalone LaTeX source, metadata, source/priority notes, exact checks,
supplementary numerical diagnostics and their recorded outputs.
SHA256SUMS.txt also records the separately deposited PDF's digest.

Run the core finite exact controls with Python 3.10 or newer:

    python3 verification/verify_exact.py

It needs only the standard library and prints JSON to standard output.
It writes no files. Explicit checks remain active under Python -O.
The recorded output is verification/exact_results.json.

The optional independently authored theta-series diagnostics also use only
the standard library. Copy the verification folder to a scratch directory
and run:

    python3 check_divisor.py
    python3 check_classification.py

These scripts write independent_results.json and classification_results.json
alongside themselves; they reject optimized Python so checks cannot silently
disappear. Ordinary floating-point agreement is supplementary evidence,
not certified numerical bounds. In some nonconstant cases the variation
is below floating-point resolution; that is reported explicitly.

The universal theorem is the analytic proof in the manuscript. The finite
checker verifies exact cyclic zero/pole inventories, both focal signs,
repeat multiplicities, and physical three- and four-period controls.
It does not independently prove the analytic identities or all-period
claims. The separate theta code checks sampled complex/real values and
chord tangency through a different computational implementation.

Compile the standalone source using a usual LaTeX system supporting
amsmath, amsthm, geometry, lmodern, microtype and hyperref; for example:

    tectonic focal_product_period_criterion.tex

External source PDFs are not redistributed. References and access limits
are in SOURCES_AND_PRIORITY.md. LICENSE.md covers the author's materials;
cited works retain their own rights.
