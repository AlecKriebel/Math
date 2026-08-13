# The minimal gate disjunction and its exact convexification

Date: 2026-08-13 (America/Los_Angeles)

No external communication or graph search was used.

## Status

**PROVED ALGEBRAIC REDUCTION.**  For one bounded module at one gate scale,
the exact obstruction to simultaneous gain is the stationary singleton
product inequality, not the stronger Hellinger form BDM.  At the hybrid
endpoint, however, BDM is exactly the half-space condition needed after
positive mixtures with the two known boundary rays are admitted.  Thus BDM
is not an arbitrary strengthening: every strict BDM violation produces a
strictly positive response after adding either leaves or the tangent strong
pair.

This note does not prove the stationary singleton product inequality or BDM.
It separates their two logical roles and identifies the smallest theorem at
each stage.

## 1. One module and one gate

Fix `r>1`, put

\[
 c=r-1,\qquad p={c\over r},
\]

and use the bounded-module notation

\[
 b=\rho_{Bd}(H,r),\qquad d=\rho_{dB}(H,r),\qquad
 q=q_Bq_D,qquad K={rc^2\over q}.
\]

At Bd gate odds `z>0`, the two normalized responses are

\[
 {B(z)\over s}={rb\over c}{z\over1+z}-1,
 \qquad
 {D(z)\over s}={rd\over c}{K\over K+z}-1.             \tag{1}
\]

Direct solution of the two strict inequalities gives

\[
 B(z)>0
 \iff b>p\ \hbox{ and }\
 z>{c\over r(b-p)},                                    \tag{2}
\]

\[
 D(z)>0
 \iff d>p\ \hbox{ and }\
 z<{r^2c(d-p)\over q}.                                 \tag{3}
\]

Consequently, some positive gate scale amplifies both rules if and only if

\[
 \boxed{q<r^3[b-p]_+[d-p]_+.}                          \tag{4}
\]

Equivalently, the exact all-gate disjunction for this one module is

\[
 \boxed{
 q_Bq_D\ge r^3[\rho_{Bd}(H,r)-p]_+
                  [\rho_{dB}(H,r)-p]_+.}               \tag{5}
\]

For the uniform Bd portal and inverse-degree dB portal, (5) is exactly the
stationary singleton-product inequality previously numbered (65).  Formula
(5) is portal-general and is the minimal local theorem: no affine separator
is needed to exclude a single module at a single gate.

## 2. Why the stronger BDM half-space is still necessary

At `r=R_hyb`, write the leaf-annihilating functional

\[
                         L(B,D)=D+cB.                   \tag{6}
\]

The ordinary leaf response is

\[
                         \ell=(1/c,-1),\qquad L(\ell)=0. \tag{7}
\]

The optimized strong-pair response at the hybrid tangency has the form

\[
                         k=(-\eta/c,\eta),\qquad
                         \eta>0,\qquad L(k)=0.           \tag{8}
\]

Indeed, the exact pair formula at the hybrid optimizer has negative Bd and
positive dB coordinates, while the hybrid sextic makes their `L`-score
zero.

Let `v=(B,D)` be any bounded-module response with

\[
                              L(v)>0.                   \tag{9}
\]

There are three cases.

1. If `B>=0` and `D>0`, the response is already in the open positive
   quadrant.
2. If `B<0`, then `D>0`.  At `lambda_0=-cB`,

   \[
    v+\lambda_0\ell=(0,L(v)).                           \tag{10}
   \]

   Replacing `lambda_0` by `lambda_0+epsilon`, for sufficiently small
   positive `epsilon`, makes both coordinates strictly positive.
3. If `B>=0` and `D<=0`, then at `lambda_0=-D/eta`,

   \[
    v+\lambda_0 k=(L(v)/c,0).                           \tag{11}
   \]

   Replacing `lambda_0` by `lambda_0+epsilon`, for sufficiently small
   positive `epsilon`, again makes both coordinates strictly positive.

Thus

\[
 \boxed{L(v)>0\quad\Longrightarrow\quad
 \text{a positive mixture of }v\text{ with }\ell\text{ or }k
 \text{ lies in }(0,\infty)^2.}                        \tag{12}
\]

Conversely, if every admitted response satisfies `L<=0`, then every common
positive-measure mixture does too and therefore cannot have both coordinates
positive.  Hence `L<=0` is the exact closed-cone condition in the presence of
the two boundary rays.

## 3. Relation to BDM

The Hellinger-form bounded dual-moment lemma is algebraically equivalent to

\[
                           L(B(z),D(z))\le0
             \qquad\hbox{for every }z>0.               \tag{13}
\]

Equation (5) is weaker: it says only that `(B(z),D(z))` never itself enters
the positive quadrant.  Equations (7)--(12) explain why (13) is nevertheless
the correct local obligation for a matching upper theorem over separated
mixtures.  If (13) fails strictly for any realizable module and scale, the
known leaf or tangent-pair ray converts that failure into a simultaneous
leading response.

This gives a useful proof order:

1. prove the minimal stationary product inequality (5), which is the first
   genuine cross-rule stationary statement;
2. prove the additional convexification slack needed to upgrade (5) to
   (13), or apply (5) to a weakly connected compound module realizing the
   boundary-ray mixture;
3. use the paired first-exit trace theorem to integrate (13) at the actual
   response scale.

Failure at either of the first two steps is not merely failure of a proof
architecture: by (12), a strict physical failure identifies a mechanism for
raising the lower threshold beyond `R_hyb`.

## 4. Exact replay

Run

```text
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B \
  universal_simultaneous_amplification/phase5_exact_threshold/\
rhyb_compactness_reduction/verify_local_disjunction_convexification.py
```

The replay verifies (2)--(5), both boundary-ray convexifications, and the
strong-pair sign/tangency identities over the exact symbolic field modulo
the hybrid sextic.
