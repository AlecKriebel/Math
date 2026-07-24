# Exact nonextension of the frozen K6 distribution

The particular symmetric 51-orbit K6 distribution in
`../direct_k6_triangle_extension.json` is not the K6-face marginal of any
quarter-grid K7 distribution, even before imposing positivity or rank.

Its 51 orbits expand to 26,820 labeled K6 matrices.  Any K7 atom in an exact
extension must have all seven K6 faces in this support, because nonnegative
weights cannot cancel mass outside the prescribed marginal.

Glue the faces deleting vertices 6 and 5 over their common labeled K5 face.
There are 22,677 K5 keys and 39,630 compatible ordered face pairs.  The two
faces determine every K7 edge except \(56\); trying its seven colors gives
277,410 cases and covers every possible supported K7 matrix.  Exact
enumeration finds zero cases whose other five K6 faces remain in support.

Thus the K7 face-count matrix \(A\) has no columns.  If \(w_i\) are the exact
K6 weights, the target is \(b_i=7w_i\).  Since
\[
w_8=\frac{10427428593}{26000000000000}>0,
\]
the Farkas vector \(y=-e_8\) has vacuous
\(A^{\mathsf T}y\geq0\) and
\[
b^{\mathsf T}y
=-\frac{72992000151}{26000000000000}<0.
\]

This excludes only the frozen K6 distribution.  It does not exclude another
K6 distribution with the same triangle marginal, a direct K7 local
distribution, or a global 41-point code.  In this support-specific test the
rank-five null/Schur equations never become active because no combinatorial
K7 support pattern survives.

Reproduce with:

```sh
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/k7/verify_fixed_support_obstruction.py
```
