# A universal five-bin integer row facet

## Statement

Fix a point \(x\) in a hypothetical 41-point code in \(S^4\), and partition
the other 40 points according to \(u=\langle x,y\rangle\):

\[
\begin{array}{c|c}
A&[-1,-3/4]\\
B&(-3/4,-1/300)\\
C&[-1/300,1/300]\\
D&(1/300,1/2)\\
E&\{1/2\}.
\end{array}
\]

Write the five bin counts as \(d=(A,B,C,D,E)\).  Every such row obeys

\[
A+B+C+D+E=40,\quad A\le5,\quad A+B\ge7,\quad
D+E\ge6,\quad E\le15.                                    \tag{1}
\]

For \(0\le i\le j<5\), in lexicographic order, define

\[
\begin{split}
(c_{ij})={}&(178581,357162,349742,4892,-779258,\\
&178581,349742,4892,-779258,176761,42272,-775478,\\
&3511,-18728,854161).
\end{split}
\]

Then the following discontinuous but universal row inequality holds:

\[
P(d):=\sum_{0\le i\le j<5}c_{ij}d_i d_j\ge0.              \tag{2}
\]

It is legitimate to average (2) over all 41 anchors.  The resulting
pair/triple inequality is valid without assuming a lattice, antipodality,
centering, rigidity, a finite inner-product alphabet, or any symmetry.

## Proof of the row bounds

The enlarged-cap theorem proved elsewhere in this repository gives at least
seven other points with inner product strictly below \(-1/300\), and at
least six with inner product strictly above \(1/300\).  With the displayed
half-open endpoint conventions these are exactly \(A+B\ge7\) and
\(D+E\ge6\).

If \(y_1,\ldots,y_A\) lie in the deep bin, put
\(u_i=\langle x,y_i\rangle\le-3/4\).  If some \(u_i=-1\), then
\(y_i=-x\), and no second point can be in this bin: otherwise
\(\langle -x,y_j\rangle=-u_j\ge3/4>1/2\).  Thus assume \(u_i>-1\).
Normalize the orthogonal projections

\[
z_i=\frac{y_i-u_i x}{\sqrt{1-u_i^2}}\in S^3.
\]

For distinct \(i,j\),

\[
\langle z_i,z_j\rangle
=\frac{\langle y_i,y_j\rangle-u_i u_j}
       {\sqrt{(1-u_i^2)(1-u_j^2)}}
\le
\frac{1/2-u_i u_j}
       {\sqrt{(1-u_i^2)(1-u_j^2)}}<0,
\]

because \(u_i u_j\ge9/16>1/2\).  A set of unit vectors with all
off-diagonal inner products strictly negative in \(\mathbb R^4\) has at
most five elements.  Indeed, its positive semidefinite Gram matrix has
nullity at most one: after subtracting it from a sufficiently large scalar
matrix, Perron--Frobenius makes the top eigenvalue simple.  Rank at most four
then gives \(A\le5\).

Finally, projecting the contact neighbors \(u=1/2\) into \(x^\perp\)
produces an \(S^3\) code with maximum inner product \(1/3\).  The exact bound
\(A(4,1/3)\le15\), proved in `local_link_geometry.md`, gives \(E\le15\).
This proves (1), including all boundary cases.

## Exhaustive exact proof of the facet

There are exactly 32,136 nonnegative integer five-tuples satisfying (1).
Direct integer evaluation of \(P\) on the complete enumeration gives

\[
\min P=0,\qquad
\#\{P=0\}=54,\qquad
\min\{P:P>0\}=11200,\qquad
\max P=210890400.
\]

The standard-library verifier reconstructs this enumeration and every
integer evaluation from the certificate.  Hence (2) follows with no
floating-point or solver assumption.

## Exact separation of the old all-harmonic witness

On the seven-node quarter grid, the bin map is

\[
(-1,-3/4,-1/2,-1/4,0,1/4,1/2)
\longmapsto(A,A,B,B,C,D,E).
\]

The verifier reconstructs the exact first and second row moments from
`fixed41_bv_fullradial_k16_pseudodistribution.json`, aggregates them through
this map, and obtains

\[
\mathbb E P(d)
=-\frac{3914305419977117}{23437500000}<0.
\]

Therefore that pair/triple pseudodistribution violates the universal
five-bin facet.  This destroys the old pure-BV barrier witness, but does not
yet prove that every repaired BV pseudodistribution has average squared
row energy below \(36/5\).

## Reproduction and hardening

```sh
python3 verifiers/verify_fixed41_coarse_bin_integer_degree_obstruction.py
python3 -m unittest \
  tests.test_fixed41_coarse_bin_integer_degree_obstruction
```

Both this verifier and the seven-bin verifier use explicit exceptions, not
Python `assert`, for every proof-critical check, so optimization mode
(`python -O`) cannot disable verification.
