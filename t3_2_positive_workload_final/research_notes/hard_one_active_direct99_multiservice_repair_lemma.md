# Proof-only repair lemmas for the direct 99 and open six one-active rows

**Scope, 2026-08-12 PDT.**  This note supplies the analytic lemmas missing
from the frozen 1,104-row candidate.  It contains no support, orientation,
history, or state-box enumeration.  The direct rows require a new
multi-service stopping rule.  The open rows instead use rapid mixing of an
independent immigration--death spectator.  No pair or global claim is made
here.

## 1. Direct mixed physical-source rows

Let (V) be the old active species and (Z=(Z_1,Z_2)) the inactive
species.  Assume molecularity at most two, no source has active degree two,
and one strongly connected mixed linkage contains the pure active complex
(V) and at least one active-free complex.  Hence every active-bearing
complex is in

\[
                    \{V,V+Z_1,V+Z_2\}.                       \tag{1.1}
\]

Call a reaction **top-sourced** if its source has active degree one and
**paid** if its source has active degree zero.  A top-sourced reaction to an
active-free target is a **service**; it lowers (V) by exactly one.

Start from

\[
                 V(0)=n,\qquad |Z(0)|_1=u=n^{o(1)},             \tag{1.2}
\]

with positive incoming reflected (V)-debt.  Put (K=u+1), and choose a
cutoff (L_n=n^{\delta+o(1)}), where (0<\delta<1).  Stop at the first of:

1. (D_K): completion of the (K)-th top-sourced service;
2. (E): the included first paid reaction;
3. (B): the included first hit of (|Z|_1\ge L_n).

Give (B) priority in a simultaneous boundary tie and (E) priority over
(D_K) if the same physical reaction is paid.  There is no outer no-fast
(P)-endpoint in this direct route.  The first internal service before
(D_K) is the included first crossing below the entrance active level and
therefore services actual incoming debt.  The rule after that eligibility
check is mark-blind and continues to update the real reflected marks.

### Lemma 1.1 (top-only multi-service kernel)

Suppress the paid clocks only for the present construction and use active
time

\[
                         s=\int_0^tV_r\,dr.                    \tag{1.3}
\]

Let (S_s) count top-sourced services, let
(H_K=\inf\{s:S_s=K\}), and put (M_s=|Z_s|_1).  There are constants
(T,p,c,C>0), depending only on the fixed graph and rates, such that

\[
 \mathbb P\{S_{s+T}>S_s\mid\mathcal F_s\}\ge p               \tag{1.4}

whenever (S_s<K).  Consequently, for every fixed (r),

\[
 \mathbb EH_K^r\le C_rK^r,
 \qquad
 \mathbb E\sup_{s\le H_K}(1+M_s)^r
       \le C_r(1+u+K)^{C_r},                                  \tag{1.5}
\]

and

\[
 \mathbb E\int_0^{H_K}(1+M_s)^r\,ds
       \le C_r(1+u+K)^{C_r}.                                  \tag{1.6}

More sharply,

\[
 \mathbb P\{\sup_{s\le H_K}M_s\ge L\}
       \le \exp\{-cL+CK\},\qquad L\ge C(1+u+K).              \tag{1.7}

#### Proof

Choose a simple directed path in the mixed linkage from (V) to its first
active-free vertex.  Before its terminal edge, every vertex lies in (1.1).
If the first edge is (V\to V+Z_i), regard the created molecule as tagged.
The mass-action clocks of a tagged (Z_i)-particle are ordinary
per-particle clocks.  In active time their rates are the fixed rate
constants.  A different inactive particle cannot consume the tag, because
every stripped top source is (0,Z_1), or (Z_2), never a two-particle
source.  Thus the desired pure-(V) edge can fire and the tag can follow the
fixed path to its terminal service in a fixed active-time interval with a
probability (p>0), uniformly over the background population.  A direct
(V\)-to-lower edge is the same argument without a tag.  Other services can
only help.  This proves (1.4).

Divide active time into intervals of length (T).  The conditional success
probability in every interval is at least (p), so the number of intervals
needed for (K) services is stochastically dominated by a negative-binomial
random variable.  In particular

\[
             \mathbb EH_K^r\le C_rK^r,
 \qquad \mathbb E e^{aH_K}\le C^K                         \tag{1.8}

for some fixed (a>0).

The only top-to-top transitions which increase (M) have stripped source
zero; their total active-time rate is a fixed constant.  Let (I_s) count
these immigrations.  A top-to-top transition with nonzero stripped source
preserves or lowers (M), while a service changes (M) upward by at most
two.  Pathwise,

\[
                         M_s\le u+I_s+2S_s.                     \tag{1.9}

The count (I_s) has constant compensator.  Its stopped polynomial moments,
together with (1.8)--(1.9), prove (1.5)--(1.6).  Splitting according as
(H_K\le c_0L), using a Poisson Chernoff bound for (I_{c_0L}), and using
(1.8) on the complement gives

\[
 \mathbb P\{I_{H_K}\ge L-u-2K\}
 \le e^{-cL}+e^{-cL+CK},                                      \tag{1.10}

which proves (1.7). \(\square\)

### Lemma 1.2 (restoring every paid clock)

Run the actual process and use the stopping rule preceding Lemma 1.1.  For
every fixed (r),

\[
\begin{aligned}
 \mathbb E[(1+M_E+|V_E-n|)^r;E]
   &\le {C_r(1+u)^{C_r}\over n},\\
 \mathbb E\sigma^r&\le {C_r(1+u)^{C_r}\over n^r},             \tag{1.11}\\
 \mathbb P(B)+\mathbb E[(1+M_B)^r;B]&\le n^{-m}
       \quad\text{for every fixed }m,                         \tag{1.12}
\end{aligned}
\]

after increasing (n) by a sequence-dependent finite amount.  Moreover,

\[
                   \mathbb P(D_K)=1-n^{-1+o(1)}.               \tag{1.13}

#### Proof

Before (D_K), no paid reaction has occurred and

\[
                          V=n-S_s\ge n-K\ge n/2                \tag{1.14}

for all large (n).  The total physical paid propensity is bounded by
(C(1+M)^2).  In active time its intensity is therefore at most

\[
                         {C(1+M)^2\over n}.                     \tag{1.15}

The compensation formula, with the paid jump included, and (1.6) give

\[
 \mathbb E[(1+M_E+|V_E-n|)^r;E]
 \le {C_r\over n}\,
       \mathbb E\int_0^{H_K}(1+M_s)^{r+2}\,ds,
                                                                    \tag{1.16}

which is the first line of (1.11).  Physical time is at most
(H_K/(n-K)), proving its second line.  Equation (1.7), with
(K=u+1=n^{o(1)}) and (L=L_n), is superpolynomial; the boundary-causing
jump changes (M) by at most two.  This proves (1.12).  Finally (1.13)
follows by subtracting the paid and boundary probabilities. \(\square\)

### Lemma 1.3 (arbitrary fixed correction and fourth power)

For a fixed (ell\in\mathbb R^3), put

\[
 G_\ell(x)=K_\ell+\sum_i\log(x_i!)+\ell\cdot x\ge1,
 \qquad W_\ell=G_\ell^4.                                    \tag{1.17}

Then the actual block above satisfies, for some (c>0),

\[
 \mathbb E[W_\ell(X_\sigma)-W_\ell(X_0)+\sigma]
      \le-cG_\ell(X_0)^3K\log n
      \le-cG_\ell(X_0)^3\log n.                              \tag{1.18}

Every fixed endpoint moment, in particular every order (q>8), is
(n^{o(1)}).

#### Proof

Let (I=I_{H_K}).  On (D_K), (1.9) gives
(M_D\le u+I+2K).  The multinomial bound

\[
 \log z_1!+\log z_2!\ge\log(u!)-u\log2,
 \qquad z_1+z_2=u,                                      \tag{1.19}

and (log a!+\log b!\le\log((a+b)!)) give the one-sided inactive
estimate

\[
 \Delta G_{\ell,\mathrm{inact}}
 \le C_\ell(u+I+K)\log(u+I+K+e).                         \tag{1.20}

The exact active decrement is

\[
 \log((n-K)!)-\log(n!)-K\ell_V
 =-K\log n+O(K^2/n)+O_\ell(K).                         \tag{1.21}

Equations (1.8)--(1.10), with (K=u+1), now imply

\[
 \mathbb E[\Delta G_\ell;D_K]
 \le-\mathbb P(D_K)K\log n+C_\ell K\log(K+e)+o(K\log n).
                                                                  \tag{1.22}

Because (log K=o(\log n)), its right side is at most
(-cK\log n).

At a paid endpoint one physical jump changes the active count by at most
one and the inactive count by at most two.  Apply (1.16) with arbitrarily
high polynomial order and use

\[
 \log(a+j)!-\log(a!)\le Cj\log(a+j+e)                          \tag{1.23}

to obtain, for every fixed (r),

\[
 \mathbb E[|\Delta G_\ell|^r;E]
 \le n^{-1}(1+u)^{C_r}(\log n)^{C_r}=n^{-1+o(1)}.              \tag{1.24}

Equation (1.12), with its power chosen after (r), proves the analogous
negligible boundary estimate.  On the clean endpoint, (1.8), (1.20), and
(1.21) give

\[
                     \mathbb E|\Delta G_\ell|^r=n^{o(1)}.      \tag{1.25}

Since (G_\ell(X_0)=\Theta(n\log n)), the last three terms of

\[
 \Delta W_\ell
 =4G_\ell^3\Delta G_\ell+6G_\ell^2(\Delta G_\ell)^2
  +4G_\ell(\Delta G_\ell)^3+(\Delta G_\ell)^4                \tag{1.26}

are (o(G_\ell^3K\log n)).  The duration in (1.11) is smaller still.
Together with (1.22)--(1.25), this proves (1.18). \(\square\)

## 2. The open wholly-top rows need a different argument

Now assume the exact structural form

\[
             \{V,V+U\},\qquad \{0,I,2I,V+I\},                 \tag{2.1}

with both linkage graphs strongly connected, and start from
((U,V,I)=(u,n,0)), where (u=n^{o(1)}).  The first linkage preserves
(V); in active time it is the immigration--death chain

\[
 Qf(a)=\alpha\{f(a+1)-f(a)\}
       +\beta a\{f(a-1)-f(a)\}.                               \tag{2.2}

The entire (I,V) service block is independent of the (U)-clock after
conditioning on its active-time duration, because the second linkage does
not contain (U).

Use the full Poisson-averaged all-reaction service block on the second
linkage.  Write (	au) for its physical endpoint, (S=\int_0^\tau V_rdr),
(R_n) for its unresolved positive active entries, and (D_n) for its
unpaired services.  Its existing aggregate estimates are

\[
 \mathbb ED_n\ge p,
 \qquad \mathbb ER_n\le C/n,                                  \tag{2.3}
\]

with all fixed moments of (D_n,R_n,I_\tau,	au), and the raw event count.

### Lemma 2.1 (rapid spectator mixing before service)

For every fixed (r), outside the already endpoint-weighted moving-boundary
event,

\[
                   \mathbb E(1+U_\tau)^r\le C_r.              \tag{2.4}

For every fixed (ell_U\),

\[
 \mathbb E[\log(U_\tau!)+\ell_UU_\tau
             -\log(u!)-\ell_Uu]\le C_{\ell_U},                \tag{2.5}

while every fixed absolute moment of the same difference is (n^{o(1)}).

#### Proof

At (I=0), the first reaction of the second linkage has source zero.  Let
(R\) be its waiting time.  Its total rate is a fixed number
(ho>0).  No service or unresolved entry can occur before this reaction.
For a fixed block horizon (T>0), the service stopping time therefore obeys

\[
 S\ge n(R\wedge T)                                             \tag{2.6}

unless the (U)-moving boundary is hit first.  Consequently

\[
 \mathbb Ee^{-k\beta S}
 \le {C_k\over n}+e^{-k\beta nT},\qquad k\ge1.                \tag{2.7}

The same bound holds after a geometric number of completed blocks, since
the first block already gives (2.6).

Conditional on (S=s), the exact immigration--death transition law is

\[
 U_s\ \stackrel d=\
 \operatorname{Bin}(u,e^{-\beta s})
 +\operatorname{Pois}\!\left({\alpha\over\beta}
                       (1-e^{-\beta s})\right).                \tag{2.8}

The service clock is independent of the (U)-driving noise conditional on
(S).  Falling-factorial moments in (2.8), followed by (2.7), give

\[
 \mathbb E(1+U_\tau)^r
 \le C_r\{1+u^r/n\}=O(1),                                     \tag{2.9}

because (u=n^{o(1)}).  The immigration--death factorial maximum estimate
over the block duration makes a hit of (L_n=n^{\delta+o(1)})
superpolynomial and pays its included endpoint.

Finally (b(a)=\log(a!)+\ell_Ua) is bounded below on
\(\mathbb N_0\), while (2.9) bounds the expectation of its positive part at
the terminal point.  Hence

\[
 \mathbb E[b(U_\tau)-b(u)]
 \le \mathbb Eb(U_\tau)^+-\inf_{a\ge0}b(a)\le C_{\ell_U},     \tag{2.10}

which is (2.5).  Formula (2.8) and arbitrary fixed moments similarly give
the claimed (n^{o(1)}) absolute bounds. \(\square\)

### Lemma 2.2 (open-row fourth-power drift)

For the same arbitrary pair-fixed (ell), the Poisson block satisfies

\[
 \mathbb E[W_\ell(X_\tau)-W_\ell(X_0)+\tau]
      \le-cG_\ell(X_0)^3\log n.                              \tag{2.11}

#### Proof

After cancelling paired carriers, the active endpoint change is

\[
                         V_\tau-n=R_n-D_n.                    \tag{2.12}

The exact factorial finite difference, (2.3), and the fixed moments of the
two counts give

\[
 \mathbb E[\log(V_\tau!)-\log(n!)+\ell_V(V_\tau-n)]
      \le-p\log n+O(1).                                       \tag{2.13}

Lemma 2.1 controls the (U)-part from the subpower deterministic start;
the Poisson service theorem controls the (I)-part and all actual carrier
endpoints.  Therefore

\[
                         \mathbb E\Delta G_\ell\le-c\log n,   \tag{2.14}

and every fixed absolute moment of (Delta G_\ell) is (n^{o(1)}).
The endpoint-weighted moving-boundary estimate pays the causing reaction.
Since (G_\ell(X_0)=\Theta(n\log n)), applying the exact expansion (1.26)
makes its last three terms lower order than
(G_\ell^3\log n).  The physical duration has every fixed moment and is
lower order as well.  This proves (2.11). \(\square\)

## 3. Scoped conclusion

The direct and open repairs are analytically different.

* In a direct row, one fast killed exit is insufficient for an arbitrary
  subpower inactive cloud and arbitrary fixed (ell).  Repeating until
  (K=u+1) actual services creates a leading descent
  (-K\log n), while all inactive entropy and paid-clock exposure are only
  polynomial in (u).
* In an open row, the spectator is dynamically independent and is mixed for
  order (n) active time before the first slow service opportunity.  Its
  terminal factorial-linear entropy has a uniform one-sided upper bound, so
  the original order-one Poisson service block is sufficient; a
  (K)-service repetition is unnecessary.

Both blocks retain all physical clocks after the ordered-compensation
reconstruction, include every causing reaction, use the actual population
endpoint, and work for the same arbitrary fixed (W_\ell).  These lemmas
repair only the analytic gap identified in the frozen 1,104-row theorem;
they do not themselves certify its finite composition or any support pair.
