# Uniform full-conflict charging is refuted

Let \(V\) be the 28 normalized \(D_5\) roots outside the fixed 12-point
support.  In scaled coordinates \(z=\sqrt2y\), define the full conflict set
\[
F(z)=\{v\in V:v\mathbin{\cdot}z>1\}.
\]
The strict inequality is essential: a root at \(v\cdot z=1\) is compatible
with \(z\), and hence is not in \(F(z)\).

Consider the proposed fractional rule in which each extension point \(z\)
sends charge \(1/|F(z)|\) to every member of \(F(z)\).  The rule would be
useful only if every center received total charge at most one from every
compatible extension code.  This statement is **REFUTED** by the exact
rational certificate in
`uniform_conflict_charge_counterexample.json`.

## Exact counterexample

The certificate gives four rational scaled points.  Direct exact arithmetic
proves
\[
\|z_i\|^2=2,\qquad r\cdot z_i\le1\quad(r\text{ in the fixed support}),
\qquad z_i\cdot z_j\le1\quad(i\ne j).
\]
Thus they are a compatible extension code.  In the deterministic ordering
returned by `support.completion_roots()`, their full conflict sets are
\[
\begin{aligned}
F(z_0)&=\{0,8,12\},\\
F(z_1)&=\{0,13,16,26\},\\
F(z_2)&=\{0,13,17,27\},\\
F(z_3)&=\{0,12,16,24\}.
\end{aligned}
\]
All four contain center \(0=(-1,-1,0,0,0)\), so its received charge is
\[
\frac13+\frac14+\frac14+\frac14=\frac{13}{12}>1.
\]

The independent verifier recomputes norms, all support inequalities, all six
mutual inequalities, and every strict full conflict from the coordinates.  It
does not trust the listed conflict sets or claimed charge:

```sh
python3 verify_uniform_conflict_charge_counterexample.py
python3 -O verify_uniform_conflict_charge_counterexample.py
python3 -m unittest -v test_verify_uniform_conflict_charge_counterexample.py
python3 -O -m unittest -v test_verify_uniform_conflict_charge_counterexample.py
```

This refutes only the uniform \(1/|F|\) charging rule.  It does not refute
Hall matching for the full conflict hypergraph: the four sets above have
union of size nine.
