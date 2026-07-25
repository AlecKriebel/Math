# Exact nonextension of the frozen K7 distribution

The particular symmetric 51-orbit K7 distribution in
`../k7/direct_k7_triangle_extension.json` is not the K7-face marginal of any
quarter-grid K8 distribution.

Its 51 orbits expand to 221,340 labeled K7 matrices.  Any K8 atom in an exact
nonnegative extension must have all eight K7 faces in this support: a face
outside the support would give the prescribed K7 marginal positive mass
outside its support, and nonnegative weights cannot cancel it.

Glue the faces deleting vertices 7 and 6 over their common labeled K6 face.
There are 192,045 K6 keys and 298,500 compatible ordered face pairs.  The two
faces determine every K8 edge except \(67\); trying its seven colors gives
2,089,500 cases and covers every possible supported K8 matrix.  Exact
enumeration finds zero cases whose other six K7 faces remain in support.

Thus the K8 face-count matrix \(A\) has no columns.  If \(w_i\) are the exact
K7 weights, the target is \(b_i=8w_i\).  Since
\[
w_{50}=\frac{1142575236831}{520000000000000}>0,
\]
the Farkas vector \(y=-e_{50}\) has vacuous
\(A^{\mathsf T}y\geq0\) and
\[
b^{\mathsf T}y
=-\frac{1142575236831}{65000000000000}<0.
\]

This excludes only the frozen K7 distribution.  It does not exclude another
K7 distribution with the same triangle marginal, a direct K8 local
distribution, or a global 41-point code.  In this support-specific test the
rank-five equations never become active because no combinatorial K8 support
pattern survives.

Reproduce with:

```sh
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/k8/verify_fixed_support_obstruction.py
```
