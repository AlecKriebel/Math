# Realized D5 extension attack

This folder studies the exact continuous problem obtained after imposing the
projection-membership equalities on extension profiles.

The fixed support consists of 12 normalized \(D_5\) roots \(x_i=r_i/\sqrt2\)
with positive weights \(p_i\in\{1/10,1/20\}\).  An extension point is a unit
vector \(y\in S^4\) satisfying
\[
\langle x_i,y\rangle\le\frac12\quad\text{for every support point }i.
\]
Equivalently, with \(z=\sqrt2y\), it satisfies
\[
\|z\|^2=2,\qquad r_i\cdot z\le1.
\]
An extension code is a family of such vectors with \(z_a\cdot z_b\le1\).

Exact derivations and exact verification belong in the proof/verifier files.
Continuous optimization is discovery evidence only and is kept in separately
labelled scripts and artifacts.
