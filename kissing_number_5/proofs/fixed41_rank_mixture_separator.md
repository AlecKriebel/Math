# An exact separator for the proposed C039--C047 mixture

## Status

**PROVED BARRIER RESULT.**  Convexly mixing the all-harmonic fixed-\(41\)
pseudo-measure C039 with the five-node degree-three/C047 pseudo-measure C056
cannot produce a pseudo-measure satisfying both every Bachoc--Vallentin
block and the rank-five moment inequality C047.

This is not an upper bound for the kissing problem.  It eliminates one
specific synthesis of two pseudo-measures.

## 1. The two endpoints

Let \({\cal A}\) denote the rational pseudo-measure in
`fixed41_bv_fullradial_k16_pseudodistribution.json`, whose all-degree BV
certificate is C039.  Its active support for every positive harmonic degree
is

\[
 X_{\cal A}=
 \left\{-\frac34,-\frac12,-\frac14,0,\frac14,\frac12\right\}. \tag{1}
\]

Let \({\cal B}\) denote the pseudo-measure in
`local_hybrid_degree3_rank_pseudodistribution.json`.  Its support is

\[
 X_{\cal B}=
 \left\{-\frac{77}{100},-\frac7{10},-\frac{11}{25},
              -\frac9{100},\frac{499}{1000}\right\}.          \tag{2}
\]

The two sets (1)--(2) are disjoint.  Normalize the integral counts of
\({\cal B}\) by dividing ordered pair counts by \(41\) and unordered triple
orbit counts by \(41/6\).  Both endpoints then have pair mass \(40\),
triple mass \(40\cdot39\), and the same fixed-cardinality marginal
normalization.

For \(0\leq\theta\leq1\), put

\[
 {\cal M}_\theta=(1-\theta){\cal A}+\theta{\cal B}.             \tag{3}
\]

All fixed-cardinality marginal equations and all BV matrices are linear in
this mixture.

## 2. The rank cut can be repaired by the mixture

Use the fixed-\(41\) normalization

\[
 \delta=A-\frac{36}{5},\qquad
 E=T-\frac{1116}{25}-\frac{108}{5}\delta.                       \tag{4}
\]

The rank-five condition C047 is

\[
 20E^2\leq369\delta^3.                                           \tag{5}
\]

At the all-harmonic endpoint,

\[
\delta_{\cal A}=
\frac{7796592200083}{800000000000000},\qquad
E_{\cal A}=
\frac{416587466342759}{16000000000000000},
\]

and the left side minus the right side in (5) is strictly positive.
At the five-node endpoint,

\[
\delta_{\cal B}=\frac{29759}{820000},\qquad
E_{\cal B}=\frac{9958803}{1025000000},
\]

and (5) holds strictly.

Because \(\delta\) and \(E\) are linear in (3), the rational choice
\(\theta=3/5\) gives

\[
\begin{aligned}
\delta_{3/5}
 &=\frac{2105200280203403}{82000000000000000},\\
E_{3/5}
 &=\frac{26640537000053119}{1640000000000000000},
\end{aligned}
\]

and

\[
20E_{3/5}^2-369\delta_{3/5}^3
=-\frac{
12997910797610647818875415573067981620921786443
}{
13448000000000000000000000000000000000000000000000
}<0.                                                               \tag{6}
\]

Thus the obstruction below is genuinely a higher BV obstruction, not
merely the original C047 failure.

## 3. A finite exact BV separator

Define the degree-six radial polynomial

\[
\begin{aligned}
\phi(u)
 &=\prod_{a\in X_{\cal A}}(u-a)\\
 &=\frac3{256}u+\frac1{64}u^2-\frac{15}{64}u^3
   -\frac5{16}u^4+\frac34u^5+u^6.                    \tag{7}
\end{aligned}
\]

Consider the harmonic-degree-three BV block with radial degree six,
equivalently the total-degree-nine block \(H_{3,9}\).  Its quadratic form in
the radial direction \(\phi\) is linear in the pseudo-measure.

For \({\cal A}\), the value is exactly zero.  Indeed, \(\phi\) vanishes on
all six active nodes (1), while the transverse degree-three kernel vanishes
at the endpoint \(-1\).

For \({\cal B}\), direct exact evaluation from the stored pair and triple
weights gives

\[
\begin{aligned}
\langle\phi,H_{3,9}({\cal B})\phi\rangle
=-\frac{
135784775695227319838686509438758262331745452990857
}{
10250000000000000000000000000000000000000000000000000000
}<0.                                                               \tag{8}
\end{aligned}
\]

It follows from linearity that

\[
\langle\phi,H_{3,9}({\cal M}_\theta)\phi\rangle
=\theta\,
 \langle\phi,H_{3,9}({\cal B})\phi\rangle<0
\qquad(\theta>0).                                                   \tag{9}
\]

Therefore every positive mixture coefficient fails one fixed,
finite-dimensional BV block.  At \(\theta=0\), C047 fails.  No
\(\theta\in[0,1]\) can satisfy C039 and C047 simultaneously along this
convex segment.

The disjoint supports are decisive.  Arbitrary radial degree permits a
polynomial that annihilates the complete active support of \({\cal A}\);
strict positivity of its harmonic blocks cannot rescue a negative
direction supported on the new nodes.

## 4. Reproduction

The standard-library verifier reconstructs both endpoint normalizations,
the C047 values, the polynomial (7), and both degree-nine quadratic forms
directly from the source certificates:

```sh
/usr/bin/python3 verifiers/verify_fixed41_rank_mixture_separator.py
/usr/bin/python3 -m unittest tests.test_fixed41_rank_mixture_separator -v
```

No floating-point eigenvalue or solver status is used.
