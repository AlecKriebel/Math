# Exact barrier to the pure-BV anchored local-energy route

## Proposed route

For a hypothetical 41-point code, anchor one point \(e=x_i\), and write
\(u_j=\langle e,x_j\rangle\) for the other 40 points.  A proposed
classification-free argument seeks an axisymmetric Bachoc--Vallentin
polynomial \(F\), built from PSD blocks, and a number \(A\) such that

\[
F(u,v,t)\leq0                                             \tag{1}
\]
whenever
\[
-1\leq u,v\leq\frac12,\qquad -1\leq t\leq\frac12,\qquad
1+2uvt-u^2-v^2-t^2\geq0,                                  \tag{2}
\]
and
\[
D(u):=F(u,u,1)+2F(1,u,u)\leq A-u^2
\quad\left(-1\leq u\leq\frac12\right).                     \tag{3}
\]

Kernel positivity and (1)--(3) would imply
\[
\sum_{j\ne i}\langle x_i,x_j\rangle^2
\leq F(1,1,1)+40A.                                        \tag{4}
\]
If the right side were strictly below \(36/5\), summing (4) over anchors,
adding the 41 diagonal squares, and using
\(\operatorname{tr}(G^2)\geq(\operatorname{tr}G)^2/5\) would contradict
\[
\operatorname{tr}(G^2)\geq\frac{41^2}{5}.
\]

The following exact obstruction shows that the strict target in this
*pure BV-kernel formulation* is impossible.

## Barrier theorem

Let \(F\) be any finite-degree axisymmetric BV polynomial whose coefficient
blocks are PSD, and suppose (1)--(3) hold.  Then necessarily
\[
\boxed{
F(1,1,1)+40A
\geq
\frac{5767796592200083}{800000000000000}
>
\frac{36}{5}.}                                             \tag{5}
\]

Thus no increase of harmonic or radial degree, and no finer sampling of
(1)--(3), can make this proposed objective strictly less than \(36/5\).
A successful local-energy argument must add a constraint not respected by
the all-harmonic pseudo-distribution described below.

## Proof

Use the exact mass-41 pair/triple pseudo-distribution
[`../certificates/fixed41_bv_fullradial_k16_pseudodistribution.json`](../certificates/fixed41_bv_fullradial_k16_pseudodistribution.json).
Its all-degree BV positivity is separately certified by
`verify_fixed41_bv_all_harmonics.py`.  Denote its seven-node pair weights by
\(\alpha_q\) and its positive ordered-triple weights collectively by
\(\nu\).  They satisfy
\[
\sum_q\alpha_q=40,\qquad \sum\nu=40\cdot39.                 \tag{6}
\]
Every pair node lies in \([-1,1/2]\).  Every triple support point and each of
its permutations satisfies (2).  The exact marginal identities are
\[
\operatorname{marginal}_q(\nu)=39\alpha_q.                 \tag{7}
\]

Apply the pseudo-distribution's positive BV functional to \(F\).  In the
anchored decomposition it has the form
\[
\mathcal L(F)
=F(1,1,1)
+\sum_q\alpha_q\bigl(F(q,q,1)+2F(1,q,q)\bigr)
+T_\nu(F)\geq0.                                            \tag{8}
\]
Here \(T_\nu(F)\) is a positive weighted sum of values
\(F(u,v,t)\) at distinct-other triple support points.  The exact
all-harmonic BV certificate gives the last inequality in (8) for every
finite collection of PSD BV blocks.

All weights in \(T_\nu\) are positive, and all their support points satisfy
(2).  Therefore (1) gives
\[
T_\nu(F)\leq0.                                             \tag{9}
\]
Using (3), (6), and (9) in (8) yields
\[
0\leq\mathcal L(F)
\leq F(1,1,1)+40A-\sum_q\alpha_q q^2.
\]
Consequently
\[
F(1,1,1)+40A\geq\sum_q\alpha_q q^2.                        \tag{10}
\]

The small exact verifier computes
\[
\sum_q\alpha_q q^2
=\frac{5767796592200083}{800000000000000}
=\frac{36}{5}
 +\frac{7796592200083}{800000000000000}.                   \tag{11}
\]
The final numerator in (11) is strictly positive.  Equations (10)--(11)
prove (5).

## Scope of the obstruction

This does **not** construct a spherical code, disprove the desired
rank-five inequality, or rule out all anchored arguments.  The
pseudo-distribution is not a Gram matrix.  It shows only that any proof
using:

1. positivity of the fixed-cardinality BV blocks;
2. the pointwise distinct-other inequality (1); and
3. the one-variable diagonal/pole inequality (3)

cannot cross the \(36/5\) threshold.

The first-harmonic frame/rank inequality does not repair this particular
relaxation: the same exact excess in (11) is
\[
\left(1+\sum_q\alpha_q q^2\right)-\frac{41}{5}>0,
\]
consistent with the independently certified C067 frame barrier.  An
additional common-source, four-cycle, or stronger rank-five constraint is
therefore genuinely necessary.

## Reproduction

Run

```sh
python3 verifiers/verify_anchored_local_energy_bv_barrier.py
python3 -m unittest tests.test_anchored_local_energy_bv_barrier -v
```

The verifier uses only SHA-256, JSON parsing, and exact rational arithmetic.
It pins the imported all-harmonic pseudo-object by hash and checks the mass,
support, marginals, second moment, and strict \(36/5\) excess.  Rechecking
all BV blocks is delegated explicitly to
`verifiers/verify_fixed41_bv_all_harmonics.py`.
