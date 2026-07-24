# Exact continuum audit of pair-conditioned robust depth

## Result and scope

The exact centered quarter-grid pseudodistribution in
`certificates/centered_quarter_bv_pseudodistribution.json` satisfies every
pair/triple-measure inequality obtained by conditioning the strict
\(\pm1/300\) depth theorem on a base inner product and summing over that
stratum.

This is a relaxation barrier, not a code.  The audit does not supply local
data for individual base edges of the same color.  Such edge-resolved
counts, their products, and their covariances require a four-point or
common-source formulation.

## The conditioned rows

Fix an ordered code pair \(y,z\), put \(q=\langle y,z\rangle\), and take
\[
e=\frac{\lambda y+\mu z}
        {\sqrt{\lambda^2+\mu^2+2q\lambda\mu}}.
\]
The robust cap theorem says that at least seven code points have projection
strictly greater than \(1/300\) on \(e\).  After removing the base
endpoints, the required number of third points is
\[
r^+_{q,\lambda,\mu}
=7-\mathbf1_{\{\lambda+\mu q>L/300\}}
  -\mathbf1_{\{\lambda q+\mu>L/300\}},
\quad
L^2=\lambda^2+\mu^2+2q\lambda\mu.
\]
There is an analogous negative-tail row.

Let \(c^+_{q,\lambda,\mu}(T)\) count the qualifying **oriented** base-edge
incidences in an unordered triangle orbit \(T\).  In the certificate
normalization
\[
\alpha_q=\frac{2E_q}{41},\qquad
\nu_T=\frac{6n_T}{41}.
\]
Consequently the exact necessary row is
\[
\sum_T c^+_{q,\lambda,\mu}(T)\nu_T
\ge 6r^+_{q,\lambda,\mu}\alpha_q.                     \tag{1}
\]

## Why the continuum audit is finite

After positive scaling, every direction with \(\lambda\ne0\) is
\(\pm(1,r)\).  For a fixed ordered incident-correlation pair \((u,v)\),
membership changes only at
\[
(u+rv)^2=\frac1{300^2}(1+r^2+2qr).                   \tag{2}
\]
Thus every critical slope is rational or quadratic over \(\mathbb Q\).

The standard-library verifier represents an irrational root by its
canonical irreducible monic quadratic and its lower or upper branch.
Dyadic bounds for its square root are produced with integer `isqrt`.
Distinct roots are ordered by refining these exact rational intervals until
they separate.  It then checks:

- one rational sample in every open cell;
- both signs at every algebraic boundary, with equality excluded;
- both directions at the projective point \(\lambda=0\); and
- the antipodal base \(q=-1\) separately.

At a boundary, signs of all other event polynomials are evaluated exactly
by reducing them modulo the boundary root's minimal quadratic.  No
floating-point number, sampled angular mesh, or numerical tolerance is
used.

The numbers of distinct finite critical slopes are
\[
\begin{array}{c|rrrrrr}
q&-3/4&-1/2&-1/4&0&1/4&1/2\\ \hline
\#&30&40&44&48&46&42.
\end{array}
\]
For \(q=-1\), \(z=-y\), so every nonzero
\(\lambda y+\mu z\) reduces to one of the two directions on the \(y\)-axis.

## Exact minimum

Every checked slack is positive.  The global minimum is
\[
\boxed{
\frac{9426027066077596589}{342712500000000000}>0
}.
\]
It is attained already for
\[
q=\frac14,\qquad(\lambda,\mu)=(1,-1).
\]
For this row the exact sides of (1) are
\[
\mathrm{LHS}
=\frac{11197706977392614317}{252525000000000000},
\qquad
\mathrm{RHS}
=\frac{26930684548457773259}{1599325000000000000}.
\]

Hence adding every exact base-color-conditioned half-plane consequence of
robust depth does not eliminate this pair/triple pseudodistribution.
The unresolved information is the distribution of these local counts
among individual base edges inside one color stratum.

## Reproduction

From the repository root:

```sh
/usr/bin/python3 \
  experiments/four_point_depth_projection/centered_quarter_pair_depth/verify.py

/usr/bin/python3 -m unittest \
  experiments.four_point_depth_projection.centered_quarter_pair_depth.test_verify \
  -v
```
