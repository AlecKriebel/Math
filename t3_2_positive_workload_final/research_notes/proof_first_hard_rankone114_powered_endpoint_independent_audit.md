# Independent proof audit of the powered hard rank-one 114

**Verdict (2026-08-12 PDT): PASS at the stated local-row scope.**  The
fourth-power endpoint is a consequence of the corrected-factorial carrier
and the positive-shell-overshoot strengthening.  This audit does not promote
an incidence, a support pair, or the global T3-2 claim.

The frozen targets are

```text
note    8802e901d501494bbdbc2e33acf5a0b0df44d12218acdd9ad5ed72c0abfb4a33
source  725ab17abb7295b3a0e2feb79b1d4d4d43336d31d9d614fc40a8314f81a60974
tests   a5822e09cf18f3f62d4b5e938ea50faa1000d90b6bc6714e3a6ea8d652b39136
```

The upstream proof texts replayed in this audit have hashes

```text
corrected-factorial carrier  4aa0297c6236eb80d565e2bdf76289ec23e34d79b137c3d484880a988230a615
all-channel carrier          af5516b5169047b0de069a5a49b8986875cc40926e1bf92d0d4abd2bbd35b110
powered overshoot theorem    4764849b05915b9005d68ac885c512a906af439430e8db8a7131f04645224e29
powered theorem audit        c07f9d9d79574d1c590b03d552de574882c141c84f35fdf452508689e46743f6
```

No orientation or trajectory space was enumerated.  The finite replay below
is used only to check membership, shell shape, activation geometry, and the
common-correction menu.

## 1. Exact finite scope

The 114 rows are a literal subset of the 930 closed rank-one rows to which
the audited carrier theorem applies.  They consist of 38 pairs, with exactly
three rows per pair.  Each pair has one whole-top mask in all three rows and
one correction family.  The independent support histogram is

\[
\begin{array}{c|r|c}
\text{whole-top support}&\text{rows}&\text{correction}\\ \hline
\{2A,B+C\}&36&\text{reversible}\\
\{2A,A+B\}&24&\text{reversible}\\
\{2B,A+B\}&24&\text{reversible}\\
\{2A,2B\}&6&\text{reversible}\\
\{2A,A+B,2B\}&21&\text{directed triple}\\
\{2A,A+C,2C\}&3&\text{directed triple}.
\end{array}
\]

Thus the correction count is exactly 90 reversible rows and 24 directed
triple rows, equivalently 30 and eight pairs.  No pair has two competing
top corrections.  None of the 38 pairs is an $H_w$ rank-two switch.  On an
overlap with an all-active rank-one phase, the whole-top mask is identical;
the twelve curvature-seam pairs use the separately audited common
rate-adjusted factorial stopped block.  Hence the displayed $\ell$ is a
single physical correction on every endpoint of this local menu.

The activation split is

\[
110\ \text{lower-top seeded},\qquad
2\ \text{top-phase activated},\qquad
2\ \text{lower-layer activated}.
\]

The two top-activation rows have top $\{2A,B+C\}$.  At inactive cap zero,
$2A$ fires at order $N^2$, whereas every enabled lower source has weight
zero and total rate $O(1)$.  The two lower-layer rows are, up to swapping
$A,B$,

\[
 \{2A,A+B\}\quad\text{paired with}\quad\{0,C,2C,A+C\},
 \qquad w=(1,1,0),\quad C=0.
\]

These are two of the audited 25 finite activation blocks, not new support
geometries.

## 2. Positive moments at the actual carrier endpoint

For a direct carrier, only a bounded number of top windows and lower
reactions occur.  The positive factorial cost has all fixed moments for
the following analytic reasons.

1. On a homogeneous reversible shell or an arbitrary strongly connected
   directed triple, the exact inward fluid sign, discrete convexity, and
   the top carré estimate give an exponential Lyapunov bound for the shell
   displacement $Z=G_\ell-\min G_\ell$.  The directed case uses the unique
   sign-changing zero of the fluid polynomial; it does not require
   reversibility or an orientation list.
2. For the exceptional shell $\{2A,R+I\}$, write
   $J=A+2I$, $K=R-I$, and use $i=I$ as shell coordinate.  Exact-tier
   compactness gives $J\asymp N$, $K\asymp N^2$.  For $i\le J/4$,
   \[
   G_\ell(i)-G_\ell(i_0)
     =(i-i_0)c_*+\log(i!/i_0!)+O((1+i+i_0)^2/J).
   \]
   The birth rate is $O(N^2)$ and the death rate is at least $cN^2i$, so
   the audited exponential cofactor estimate, after reducing its exponent,
   controls every power of the positive expression above.  The event
   $i>J/4$ has exponentially small probability, while the full shell
   oscillation is polynomial.  This proves every fixed positive moment,
   including on the two rows initially activated from $i=0$.
3. Killing at a lower clock polynomially size-biases these shell laws.
   Every lower source in this rank-one menu has active weight at most one;
   in the exceptional shell the normalized killing density is bounded by
   a fixed polynomial in $I$.  Reducing the exponential parameter absorbs
   that bias.
4. If a submaximal lower source has relative propensity $r_n\to0$, its
   $q$-th positive endpoint contribution is bounded by a constant times
   \[
      r_n\{1+\log(1/r_n)\}^q\longrightarrow0.
   \]
   Maximal-to-maximal reactions have bounded positive moments by the exact
   factorial-ratio identity.  The terminal maximal-to-lower reaction is
   retained and supplies the negative gap.  Thus a killed window is not
   mistaken for its pre-jump state.

The initial race in either top-activation row adds only
$O(N^{-2}\log^q N)$ to a positive $q$-moment if an $O(1)$-rate lower clock
wins.  Conditional on the top reaction winning, the cofactor equals one and
the preceding exceptional-shell argument applies.  Hence for every direct
row one may choose a nonnegative $Y_n$, with
$\sup_n\mathbb E Y_n^q<\infty$ for each fixed $q$, such that

\[
 \Delta G_\ell\le-I_ng_n+Y_n,
 \qquad \mathbb P(I_n=1)\ge p_0>0,
 \qquad g_n\longrightarrow\infty.                  \tag{2.1}
\]

All stops are physical: word completion includes its actual terminal
reaction, a competing reaction is the endpoint when it fires, and an
unsuccessful top window stops at its physical window end.  Top reactions
are retained throughout.

The population endpoint estimates also survive this replay.  Homogeneous
shells conserve their active total.  On $B\rightleftarrows2A$, the invariant
$A+2B$ and the audited polynomial comparison give all moments of $A/N$.
On $2A\rightleftarrows R+I$, one has $A\le J\asymp N$, $R=K+I$ with
$K\asymp N^2$, and every fixed moment of $I$.  A bounded number of lower
jumps changes only the constants.  These are precisely the scaled
population endpoint moments stated by the parent carrier theorem; no claim
of uniformly bounded unscaled shell displacement is being made.

## 3. Fourth-power lift on the 112 direct rows

Let $G=G_\ell(x_n)$ and set $Z_n=-I_ng_n+Y_n$.  Because
$g_n=O(\log(2+|x_n|))=o(G)$, $G+Z_n>0$ for all large $n$.  Since the
endpoint potential is positive and $\Delta G_\ell\le Z_n$, monotonicity
gives

\[
 W_\ell(X_\tau)-W_\ell(x_n)
 \le (G+Z_n)^4-G^4.
\]

Now

\[
 \mathbb EZ_n\le-p_0g_n+O(1),\qquad
 \mathbb E|Z_n|^j=O(g_n^j+1)\quad(2\le j\le4).
\]

The exact binomial identity therefore yields

\[
 \mathbb E\Delta W_\ell
 \le-4p_0G^3g_n
   +O(G^3+G^2g_n^2+Gg_n^3+g_n^4)
 \le-cG^3g_n.                                      \tag{3.1}
\]

This argument does not require moments of a possibly large beneficial
negative shell displacement; clipping it by the upper surrogate $Z_n$ is
enough.

The direct stopping time is bounded by a fixed sum of windows of length
$O(a_n^{-1})$; the top-activation prelude has exponential moments on the
$N^{-2}$ scale.  Consequently it has every required physical-duration
moment and its mean is negligible in (3.1).

## 4. The two lower-layer activation rows

The finite activation block has a deterministically bounded number of
constant-rate zero-source waits and fast top windows.  Its reflected
workload increment is bounded, and the audited debt arithmetic gives a
strict negative mean coefficient.  Combining the lower-reaction factorial
identity with the shell overshoot gives an upper endpoint surrogate $Z_n$
such that

\[
 \Delta G_\ell\le Z_n,
 \qquad \mathbb EZ_n\le-c\log N,
 \qquad \mathbb E|Z_n|^q=O(\log^qN)                 \tag{4.1}
\]

for every fixed $q$.  Notice that positive lower-reaction debt may itself
be order $\log N$; what is uniform is the positive *shell* overshoot.  The
moment statement needed for the full block is exactly the scaled estimate
in (4.1).

Since $\log N=o(G)$, monotonicity followed by the same exact binomial
expansion gives

\[
 \mathbb E\Delta W_\ell
 \le-cG^3\log N
   +O(G^2\log^2N+G\log^3N+\log^4N)
 \le-c'G^3\log N.                                  \tag{4.2}
\]

The block duration is a bounded sum of fixed-rate exponential waits and
fast windows, so it has all fixed moments and is lower order in (4.2).
The endpoint is the actual completing, competing, or capped physical
endpoint.  No nominal activation target is substituted.

## 5. Verdict boundary

The four frozen tests pass and reproduce row hash
`5478bf16e158420669fd1fe07a7f763de25e8c5a25452a43abff65e6aa86d54a`
and payload hash
`2b9280cb7ef663d57c249d27d60d2081fb7cf194a3de0ae95b517e5f785efdcf`.
The analytic replay proves the local $W_\ell$ stopped estimate on all 114
rows for arbitrary fixed strong orientations and arbitrary fixed positive
rates.  The certificate correctly leaves the independent-audit,
pair-recurrence, and global-T3-2 flags false; changing those frozen flags is
a separate composition decision.
