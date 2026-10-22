# Verification

Run `python check_exact.py` with pre-existing SymPy 1.14.0. No network,
software installation or floating-point root is used. The deterministic
receipt passes **3,310 exact assertions**.

The checker constructs the rectangle antipedals and verifies every
line incidence, the opposite-focus correspondence, determinant product,
and signed-area formula. It independently verifies the axis-diamond
caustic and contacts through the dual-conic tangency identity, reduces
the two aspect-ratio factors, and distinguishes the finite collapse from
the parallel-line failure. It checks all four collapse intersections
and their exact coordinates. Rational centrally symmetric polygons
provide separate controls of the general equivariance and area identity.

These generic rational polygons are not claimed to be billiard orbits.
The genuine four-orbit certificates are proved analytically and checked
symbolically. The universal symmetry input and geometric argument
remain matters for independent mathematical review; finite assertions
do not substitute for them.
