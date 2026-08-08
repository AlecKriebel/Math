# Exact clique--pendant audit at fitness three halves

## Status

- **PROVED:** the endpoint normalized-product conjecture is false.
- **PROVED:** the balanced normalized-arithmetic-mean conjecture is false.
- **PROVED:** within the unweighted clique--pendant family below, the first
  product witness by population size is the unique pair `G(31,4)` on 36
  vertices.
- **PROVED:** this witness is *not* a simultaneous amplifier: its normalized
  dB fixation probability is strictly below one.
- **EXACTLY COMPUTED:** the affine crossing for this witness is
  `lambda_0=0.469920183876...`; in particular, the proposed `lambda=1/3`
  separator survives this counterexample with strict slack.
- **OPEN:** whether the `lambda=1/3` separator holds for every weighted graph.

## 1. Graph and exact lumping

Let `G(c,m)` have vertices

\[
 H,\quad C_1,\ldots,C_c,\quad L_1,\ldots,L_m.
\]

All edges have unit weight.  The vertices `H,C_1,...,C_c` induce
`K_{c+1}`, and every `L_j` is adjacent only to `H`.  Thus
`n=c+m+1`.  The group `S_c x S_m` acts by graph automorphisms.  Its orbits
on mutant subsets are indexed by

\[
 (h,i,j),\qquad h\in\{0,1\},\quad 0\le i\le c,\quad 0\le j\le m,
\]

where `h` is the type of `H`, `i` is the number of mutant ordinary clique
vertices, and `j` is the number of mutant leaves.  Graph automorphisms also
preserve fitness and either update rule.  Therefore, for any two labelled
states in one orbit, the total transition probability into every other orbit
is the same.  This proves strong lumpability.

Here are the transition probabilities derived directly from the update
definitions.  Only type-changing transitions are displayed; the remaining
probability is the self-loop.  Put

\[
 F=n+(r-1)(h+i+j),\qquad d_H=c+m.
\]

For Bd updating,

\[
\begin{aligned}
p(i\to i+1)&={r(c-i)\over F}
 \left({h\over c+m}+{i\over c}\right),\\
p(i\to i-1)&={i\over F}
 \left({1-h\over c+m}+{c-i\over c}\right),\\
p(h:0\to1)&={r\over F}\left({i\over c}+j\right),\\
p(h:1\to0)&={1\over F}\left({c-i\over c}+m-j\right),\\
p(j\to j+1)&={rh(m-j)\over(c+m)F},\\
p(j\to j-1)&={(1-h)j\over(c+m)F}.
\end{aligned}                                                    \tag{1}
\]

Terms outside the state space are omitted.  For dB updating, put
`f_H=1+(r-1)h`.  Then

\[
\begin{aligned}
p(i\to i+1)&={c-i\over n}
 {r(h+i)\over f_H+ri+c-i-1},\\
p(i\to i-1)&={i\over n}
 {{1-h+c-i}\over f_H+r(i-1)+c-i},\\
p(h:0\to1)&={1\over n}{r(i+j)\over c+m+(r-1)(i+j)},\\
p(h:1\to0)&={1\over n}{c-i+m-j\over c+m+(r-1)(i+j)},\\
p(j\to j+1)&={h(m-j)\over n},\\
p(j\to j-1)&={(1-h)j\over n}.
\end{aligned}                                                    \tag{2}
\]

The last two lines are fitness-independent because a leaf has exactly one
possible parent.  The verifier aggregates every labelled transition row of
`G(3,2)` and checks it against (1)--(2), for both rules and every subset.
This is independent of the quotient derivation.

## 2. Baselines and absorbing equations

At `r=3/2`, the complete-graph baselines are

\[
 \rho_{Bd}(K_n)={3^{n-1}\over3^n-2^n},\qquad
 \rho_{dB}(K_n)={(n-1)3^{n-2}\over
 n(3^{n-1}-2^{n-1})}.                                  \tag{3}
\]

The first is the standard one-dimensional recurrence, derived because the
Bd down/up ratio is `2/3`.  For dB, the down/up ratio at mutant count `k` is

\[
 \gamma_k={2(2n+k-2)\over3(2n+k-3)},
\]

whose products telescope; summing the resulting one-dimensional absorption
formula gives the second expression in (3).

For either quotient chain, delete the extinction and fixation states.  If
`q_s` is the total changing probability from transient state `s`, solve

\[
 q_s u_s-\sum_{t\text{ transient}}p_{st}u_t=p_{s,V}.     \tag{4}
\]

The uniform-singleton value is

\[
 \rho_U(G(c,m))={u_U(1,0,0)+c u_U(0,1,0)+m u_U(0,0,1)
 \over c+m+1}.                                          \tag{5}
\]

The certificate constructs (4) over `QQ`, solves it with FLINT, and then
substitutes the result back into every row to prove the exact zero residual.

## 3. Smallest unweighted family witness

Set

\[
 x={\rho_{Bd}(G(31,4),3/2)\over\rho_{Bd}(K_{36},3/2)},
 \qquad
 y={\rho_{dB}(G(31,4),3/2)\over\rho_{dB}(K_{36},3/2)}.
\]

Exact rational arithmetic proves

\[
\begin{aligned}
x&=1.1218228992728234\ldots>1,\\
y&=0.8920029824088562\ldots<1,\\
xy-1&=0.000669371885908453\ldots>0,\\
{x+y\over2}-1&=0.006912940840839855\ldots>0.             \tag{6}
\end{aligned}
\]

The decimal displays are not used for signs.  The exact fractions have the
following deterministic fingerprints (the hash input is the ASCII string
`numerator/denominator`):

| quantity | numerator digits | denominator digits | SHA-256 |
|---|---:|---:|---|
| `x` | 1088 | 1087 | `8c31e06d3c9ce3f6484d37d40c83e624b0f21794e23ea4a3e174b912825e9b37` |
| `y` | 866 | 866 | `aad1b6cb857508c503a57dbbb579b6b7f825515018f5b8b674b490401b99864c` |
| `xy-1` | 1950 | 1953 | `2f98042de13f4ab21c93705af3c1ff926b560fb6936219c78aa36a135b7efa9d` |
| `(x+y)/2-1` | 1947 | 1949 | `0da0e05bacda05856fab5e83ce92c72c1ab8808c1e4e48db257df2b79a830106` |

Consequently both the product separator `xy<=1` and the balanced arithmetic
separator `(x+y)/2<=1` are false.  Since `y<1`, (6) does **not** exhibit
simultaneous endpoint amplification and does not determine `R_sim`.

For a compact manuscript certificate, the same exact solve proves the short
rational bounds

\[
 x>{5609\over5000},\qquad y>{223\over250}.
\]

They immediately imply

\[
 xy>{1250807\over1250000}>1,
 \qquad {x+y\over2}>{10069\over10000}>1.                 \tag{6a}
\]

Thus the two refutations do not require printing the large fractions in the
table.

An exhaustive exact run checks all 595 integer pairs `c,m>=1` with
`c+m+1<=36`.  Every pair below 36 vertices has `xy<1`; at 36 vertices the
only positive product gap is `G(31,4)`.  The exact transcript hash is

```
3b6affb2cd06e749c397c9d2342058b1d8947cb4d2e7ea57f0b77d35ca0bd742
```

Thus `G(31,4)`, rather than the initially found `G(32,4)`, is the minimal
product witness by population size **within this unweighted two-parameter
family**.  No claim of minimality over all weighted graphs is made.

## 4. Affine separators and the one-third test

For

\[
 A_\lambda=\lambda x+(1-\lambda)y,
\]

the unique crossing is

\[
 \lambda_0={1-y\over x-y}=0.4699201838762665\ldots .     \tag{7}
\]

Exact arithmetic proves `1/3<lambda_0<1/2`.  The balanced arithmetic mean
fails because `1/2>lambda_0`.  At `lambda=1/3`, however,

\[
 1-A_{1/3}=0.031390378636488026\ldots>0.                 \tag{8}
\]

The sign has the transparent exact factorization

\[
 1-A_\lambda=(x-y)(\lambda_0-\lambda).                  \tag{9}
\]

The exhaustive exact run proves (8)'s analogue for all 595 pairs through
36 vertices.  A floating-point hostile scan through 60 vertices finds no
violation; at each fixed population size in that scan, the closest graph is
`G(n-2,1)`, and its slack approaches zero from above.  This last observation
is **NUMERICAL EVIDENCE**, not an all-parameter theorem.

There is also a useful asymptotic diagnostic.  If the pendant proportion
tends to `alpha`, the early Bd leaf-establishment calculation gives

\[
 \ell(\alpha)=
 {8\alpha-3+\sqrt{9+60\alpha-44\alpha^2}\over18\alpha}.
\]

The numerically observed fixation limits are consistent with

\[
 x_\infty=1-\alpha+3\alpha\ell(\alpha),\qquad
 y_\infty=1-\alpha.                                    \tag{10}
\]

If (10) is established with post-establishment control, the one-third slack
would reduce transparently to

\[
 1-{x_\infty+2y_\infty\over3}
 =\alpha\{1-\ell(\alpha)\}>0.                           \tag{11}
\]

Equation (11) is recorded only as a route: the branching calculation alone
does not prove the fixation limits in (10).

## 5. Replay

From the repository root, run

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  universal_simultaneous_amplification/phase4_landmark_closure/threshold/clique_pendant_product_audit/verify_clique_pendant_product.py \
  --c 31 --m 4 --exact
```

For the exhaustive within-family minimality certificate, run

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  universal_simultaneous_amplification/phase4_landmark_closure/threshold/clique_pendant_product_audit/certify_minimality.py
```

The second command is intentionally slower because it performs 1,190 exact
absorbing solves (Bd and dB for each of 595 graphs).
