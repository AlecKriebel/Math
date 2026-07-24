# Exact nonextension of the frozen K8 distribution

The particular symmetric 51-orbit K8 distribution in
`../k8/direct_k8_triangle_extension.json` is not the K8-face marginal of any
quarter-grid K9 distribution.

Its 51 orbits expand to 1,824,480 labeled K8 matrices.  Any K9 atom in an
exact nonnegative extension must have all nine K8 faces in this support: a
face outside the support would give the prescribed K8 marginal positive
mass outside its support, and nonnegative weights cannot cancel it.

Glue the faces deleting vertices 8 and 7 over their common labeled K7 face.
There are 1,635,480 K7 keys and 2,502,360 compatible ordered face pairs.
The two faces determine every K9 edge except \(78\); trying its seven colors
gives 17,516,520 cases and covers every possible supported K9 matrix.  Exact
enumeration finds zero cases whose other seven K8 faces remain in support.

The exhaustive core stores each color in three bits.  For a candidate face
deleting one of vertices \(0,\ldots,6\), the missing edge \(78\) is the last
edge in the induced K8 ordering.  The verifier therefore indexes the exact
set of supported 27-edge prefixes by the seven-bit mask of allowed last
colors, intersects the seven masks, and counts every surviving color.  This
is exactly equivalent to testing every one of the 17,516,520 trials
individually.  It does not hash or round geometric data: equality of packed
integers is equality of all 28 grid colors.

Thus the K9 face-count matrix \(A\) has no columns.  If \(w_i\) are the exact
K8 weights, the target is \(b_i=9w_i\).  Since
\[
w_{26}=
\frac{255486062818504206996978464985143047480098887}
{47175701418398322017174301773892000000000000000}>0,
\]
the Farkas vector \(y=-e_{26}\) has vacuous
\(A^{\mathsf T}y\geq0\) and a strictly negative target pairing, stored
exactly in `fixed_support_obstruction.json`.

This excludes only the frozen K8 distribution.  It does not exclude another
K8 distribution with the same triangle marginal, a direct K9 local
distribution, or a global 41-point code.  Rank-five equations never become
active because no combinatorial K9 support pattern survives.

Reproduce with:

```sh
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/k9/verify_fixed_support_obstruction.py
```
