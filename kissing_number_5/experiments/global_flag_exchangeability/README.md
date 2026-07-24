# Global rooted-flag exchangeability obstruction

## Result

There is a continuous polynomial flag-square inequality, valid for every
real symmetric \(41\times41\) array, that rejects all eight stored exact
rank-five local pseudodistributions built over the fixed centered
pair/triple marginal:

- the direct \(K_6,K_7,\ldots,K_{11}\) extensions;
- the 74-atom \(K_6\) product witness; and
- the 53-atom \(K_7\) product witness.

No finite inner-product alphabet, positivity, rank, kissing constraint, or
rigidity assumption is used in deriving the inequality.  The alphabet is
used only to evaluate the named rational certificates.

This is a genuine global-overlap obstruction.  It is not a proof that the
fixed pair/triple marginal has no other \(K_6\) lift, and it is not an upper
bound on the kissing number.

## Exact finite-exchangeability identity

Let \(N\ge k\ge6\), fix an ordered root \((i,j)\), and let
\[
 f_{ij}(\{p,q\})
\]
be any real feature of the rooted four-vertex array on
\((i,j,p,q)\), symmetric in \(p,q\).  Put
\[
 S_{ij}=\sum_{\{p,q\}\subset[N]\setminus\{i,j\}}f_{ij}(\{p,q\}).
\]
For a uniformly sampled \(k\)-set \(T\) containing \(i,j\), define
\[
 \widehat Q_{ij,T}
 =
 \sum_{\substack{A,B\in\binom{T\setminus\{i,j\}}2}}
 \frac{\binom{N-2}{|A\cup B|}}
      {\binom{k-2}{|A\cup B|}}
 f_{ij}(A)f_{ij}(B).                              \tag{1}
\]
For a fixed ordered pair \(A,B\), with \(u=|A\cup B|\), the probability
that \(A\cup B\subset T\setminus\{i,j\}\) is
\[
 \frac{\binom{k-2}{u}}{\binom{N-2}{u}}.
\]
It cancels the coefficient in (1), term by term.  Hence
\[
 \mathbb E[\widehat Q_{ij,T}\mid i,j\in T]
 =S_{ij}^{\,2}.                                    \tag{2}
\]
Now average over the root and over a uniform \(k\)-subset:
\[
 \mathbb E_T\sum_{\substack{i,j\in T\\i\ne j}}
 \widehat Q_{ij,T}
 =
 \frac{k(k-1)}{N(N-1)}
 \sum_{i\ne j}S_{ij}^{\,2}\ge0.                    \tag{3}
\]
This proves the identity, including all finite-population coefficients and
all overlap cases.  For \(N=41\), the three coefficients in (1) are
\[
 \lambda_u=\frac{\binom{39}{u}}{\binom{k-2}{u}},
 \qquad u=2,3,4.                                   \tag{4}
\]

At root size three and \(k=7\), the analogous extension-pair coefficients
are
\[
 \frac{\binom{38}{2}}{\binom42}=\frac{703}{6},
 \qquad
 \frac{\binom{38}{3}}{\binom43}=2109,
 \qquad
 \frac{\binom{38}{4}}{\binom44}=73815.             \tag{5}
\]
Thus the integer \(2109\) found independently in the factorial Farkas ray
is exactly the one-vertex-overlap coefficient for rooted \(K_5\) flags.

## One continuous polynomial row

Use
\[
 \boxed{\quad
 f_{ij}(\{p,q\})
 =
 g_{pq}\bigl(2-3(g_{ip}+g_{iq})\bigr).
 \quad}                                             \tag{6}
\]
This polynomial is continuous on the full Gram domain.  It does not mention
the quarter grid or select an equality stratum.

The verifier symmetrizes (1) over every ordered root of every stored atom.
It evaluates all quantities as exact fractions.  Every value is strictly
negative.  Approximate decimal values are shown only for readability:

| exact local marginal | \(k\) | row value |
|---|---:|---:|
| direct extension | 6 | \(-293916.60\) |
| direct extension | 7 | \(-91026.34\) |
| direct extension | 8 | \(-387168.95\) |
| direct extension | 9 | \(-114518.94\) |
| direct extension | 10 | \(-351362.94\) |
| direct extension | 11 | \(-392470.58\) |
| 74-atom product witness | 6 | \(-183959.31\) |
| 53-atom product witness | 7 | \(-418446.68\) |

The exact values are in
[`global_flag_exchangeability_certificate.json`](global_flag_exchangeability_certificate.json).
By (3), none of these eight measures is the indicated local marginal of
any 41-vertex real symmetric array.  This conclusion is stronger than
failure to be the marginal of a spherical code.

The normalized \(D_5\) configuration provides a positive control.  Directly
summing the right side of (3) on its 40 vertices gives
\[
 \sum_{i\ne j}S_{ij}^{\,2}=646060>0.                \tag{7}
\]

## The exact \(h=4,\ g=1\) counteratom

The rank-five continuous \(K_7\) Gram matrix in
`../continuous_four_point_moment/CONTINUOUS_FARKAS_COUNTEREXAMPLE.md`
has, at its distinguished base, four negative-depth points \(H\) and one
common-cap point \(G\).

For an unordered residual pair use the coarse feature
\[
 \psi(A)=
 \begin{cases}
  1,&A\text{ has one }H\text{ and one }G,\\
 -3,&A\text{ has two }H\text{ points},\\
  0,&\text{otherwise}.
 \end{cases}                                        \tag{8}
\]
Globally,
\[
 \sum_A\psi(A)=H\Gamma-3\binom H2,
\]
so its full contribution is the nonnegative square
\[
 \left(H\Gamma-3\binom H2\right)^2.                 \tag{9}
\]
The unbiased \(K_7\) estimator (1) on the exact local state
\((h,g)=(4,1)\) is nevertheless
\[
 -\frac{746187}{5}<0.                               \tag{10}
\]
This explains exactly how the locally valid rank-five counteratom fails
global exchangeability when used as a pure \(K_7\) orbit.  The continuous
polynomial choice \(f_{ij}(A)=g_{ij}g_A\), summed over every root of that
same pure orbit, also gives
\[
 -\frac{180485617}{2160}<0.                         \tag{11}
\]

Equation (9) is already implied if one imposes a complete representing
measure for the global integer pair \((H,\Gamma)\) through degree four.
It is therefore a useful exact interpretation and audit of the factorial
mechanism, but not an independent strengthening of that complete count
model.  Row (6), by contrast, uses the residual-residual inner product and
endpoint-specific incidences, and is not a function only of \(H,\Gamma\).

The negative local values in (10) and (11) do **not** show that the
seven-point configuration cannot occur inside a global code.  Other local
flags can contribute positive mass to (3).

## Exact scope and remaining gap

The theorem-strength conclusions are:

1. equations (1)--(4) are universal exact identities;
2. all eight named rational local marginals fail the single polynomial row
   (6);
3. the pure orbit of the continuous \(h=4,g=1\) atom fails (8) and
   \(g_{ij}g_{pq}\); and
4. \(D_5\) passes the direct global square nontrivially.

The unresolved step is to show that **every** rank-five \(K_6\) marginal
matching the fixed pair/triple data violates some finite family of such
rows, or to find a feasible replacement.  The stored discovery pools are
incomplete, so their rejection cannot be promoted to a continuous
nonexistence proof.

## Reproduction

Only Python 3.10 or later and the standard library are required:

```sh
PYTHONPATH=. python3 \
  experiments/global_flag_exchangeability/verify_global_flag_exchangeability.py

PYTHONPATH=. python3 \
  experiments/global_flag_exchangeability/independent_flag_audit.py

PYTHONPATH=. python3 -m unittest \
  experiments.global_flag_exchangeability.test_global_flag_exchangeability \
  -v
```

Both proof checkers use always-on verification exceptions rather than
Python `assert`.  The test suite runs each checker under `python -O` and
also verifies that optimized mode rejects a deliberately tampered input.
