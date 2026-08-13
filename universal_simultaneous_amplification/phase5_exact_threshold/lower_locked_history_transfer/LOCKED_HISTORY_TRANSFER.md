# Exact locked-history transfer and the finite-terminal obstruction

Date: 2026-08-13 (America/Los_Angeles)

No literature search or external communication was used.

## 1. Result

The exact dB graphical dual contains the hoped-for transfer factor.  On the
fully labelled history space, one stage has favorable/adverse transfer

\[
                         T_r={1\over r}
                         \begin{pmatrix}1&0\\0&r-1\end{pmatrix}. \tag{1}
\]

After `L` independent locked stages, the adverse/favorable ratio is exactly
`(r-1)^L`.  This is the proof-realizable abstract transfer matrix sought by
the lower program.

There is also an exact obstruction: no fixed finite two-terminal module can
realize (1) after histories are projected to ordinary mutant sets.  The
favorable and adverse history classes overlap on singleton outputs because
selective samples can repeat the final neutral source.  The overlap is
strict for every finite row kernel.

A growing diffuse fan-out removes the *collision* obstruction.  However,
Section 5 proves a stronger obstruction: an ordinary terminal fixation or
hitting harmonic is a coverage function, so it cannot distinguish a
singleton from a strict superset in the direction required by the history
bit.  Thus diffuse fan-out alone still does not realize (1).  A viable route
must use a signed difference of terminal harmonics or leave the additive-OR
graphical class.

## 2. Exact labelled transfer

The dB graphical update at fitness `r>1` samples

\[
 K\sim\operatorname{Geom}(1/r),\qquad
 \Pr(K=k)={1\over r}\left({r-1\over r}\right)^{k-1},
 \quad k\ge1.                                               \tag{2}
\]

Conditional on `K`, it samples iid sources `U_1,...,U_K` from the locked
target row `p=(p_u)`, then replaces the target by their Boolean OR.  Regard
`U_K` as the terminating neutral sample and put

\[
                         J=K-1.                              \tag{3}
\]

The `J` preceding samples are the selective part of the locked history.
Define two labelled history channels:

\[
 F=\{J=0\}\quad\hbox{(clean/favorable)},
 \qquad A=\{J\ge1\}\quad\hbox{(adverse)}.                  \tag{4}
\]

Then exactly

\[
                         \Pr(F)={1\over r},
 \qquad \Pr(A)={r-1\over r}.                               \tag{5}
\]

If a stage transmits the two channel weights without erasing the mark,
(5) is precisely (1).  Consequently

\[
 T_r^L={1\over r^L}
       \begin{pmatrix}1&0\\0&(r-1)^L\end{pmatrix},        \tag{6}
\]

and

\[
 {\Pr(A_1\cap\cdots\cap A_L)\over
  \Pr(F_1\cap\cdots\cap F_L)}=(r-1)^L.                   \tag{7}
\]

This is a conditional history statement.  It must be composed before
uniform-start averaging.  It is not the affine sum of response masses that
was excluded in the cold-root and hot--cold calculations.

## 3. Why a fixed finite terminal cannot preserve the channel

Let

\[
                         B=\{U_1,\ldots,U_K\}               \tag{8}
\]

be the ordinary set-valued output.  For every source `u` with `p_u>0`,

\[
 \Pr(B=\{u\},F)={p_u\over r}.                              \tag{9}
\]

The same singleton output also occurs in the adverse channel when all
samples equal `u`.  Summing over `K>=2` gives

\[
 \begin{aligned}
 \Pr(B=\{u\},A)
 &=\sum_{k\ge2}{1\over r}\left({r-1\over r}\right)^{k-1}p_u^k\\
 &={ (r-1)p_u^2\over r\{r-(r-1)p_u\}}.                    \tag{10}
 \end{aligned}
\]

Thus the adverse/favorable likelihood ratio on this common atom is

\[
 \boxed{
 {\Pr(B=\{u\},A)\over\Pr(B=\{u\},F)}
 ={(r-1)p_u\over r-(r-1)p_u}>0.}                          \tag{11}
\]

Any deterministic or randomized terminal map that depends only on `B`
must assign the same terminal law to the two occurrences of `{u}`.  It
therefore cannot send every `F` history to one terminal and every `A`
history to the other.  This proves:

> **Finite-terminal no-go.** For every finite nonempty row law, the exact
> labelled transfer (1) has no factor through the ordinary union set (8)
> into two disjoint terminal states.

If the row has at most `m` sources, `p_max>=1/m`, so (11) is at least

\[
                         {r-1\over rm-(r-1)}.                \tag{12}
\]

The obstruction is therefore scale-independent for a fixed finite stage.
It is the lower-bound analogue of the collision factor in the exact
locked-history conjugation audit.

## 4. Exact projected transfer and diffuse approximation

Although the history bit is not exactly recoverable from `B`, the event
`|B|>=2` is a collision-free certificate of the adverse channel.  The total
singleton probability is

\[
 S(p):=\Pr(|B|=1)
 =\sum_u\sum_{k\ge1}{1\over r}
       \left({r-1\over r}\right)^{k-1}p_u^k
 =\sum_u{p_u\over r-(r-1)p_u}.                             \tag{13}
\]

Hence the projected two-channel transfer is

\[
 \widetilde T_{r,p}=
 \begin{pmatrix}
 S(p)&0\\0&1-S(p)
 \end{pmatrix},                                           \tag{14}
\]

with projected ratio

\[
                         \widetilde q_r(p)={1-S(p)\over S(p)}. \tag{15}
\]

Let

\[
                         \eta(p)=\sum_up_u^2,
 \qquad p_*=max_up_u.                                    \tag{16}
\]

Subtracting the clean probability `1/r` from (13) gives the exact collision
leak

\[
 \boxed{
 \delta_r(p):=S(p)-{1\over r}
 ={r-1\over r}\sum_u{p_u^2\over r-(r-1)p_u}.}             \tag{17}
\]

Therefore, uniformly for `r>1`,

\[
 {r-1\over r^2}\eta(p)
 \le\delta_r(p)
 \le {r-1\over r}\,{\eta(p)\over r-(r-1)p_*}.             \tag{18}
\]

In particular `delta_r(p)=O(eta(p))`.  For the uniform law on `m` sources,

\[
                         S_m={m\over rm-(r-1)},             \tag{19}
\]

and the projected ratio is exactly

\[
 \boxed{\widetilde q_{r,m}=(r-1)\left(1-{1\over m}\right).} \tag{20}
\]

Thus a growing uniform fan-out recovers the desired one-stage multiplier.
At depth `L`, independent identical projected stages give

\[
 \widetilde q_{r,m}^{,L}
 =(r-1)^L\left(1-{1\over m}\right)^L.                     \tag{21}
\]

The relative error from the ideal history ratio obeys

\[
 0\le1-{\widetilde q_{r,m}^{,L}\over(r-1)^L}
 =1-\left(1-{1\over m}\right)^L\le {L\over m}.             \tag{22}
\]

For nonuniform stages, the same conclusion follows from
`sum_l eta(p_l)=o(1)`; a simple sufficient condition is

\[
                         Lp_*\longrightarrow0.              \tag{23}
\]

## 5. All-depth coverage no-go

Let `g(B)` be the probability that an ordinary terminal event eventually
occurs when the current mutant/source set is `B`, for any continuation built
from additive Boolean OR updates.  Run the continuation's graphical maps
backward from its terminal target.  Exactly as in the fixation duality, there
is a random nonempty ancestral set `Z` such that

\[
                         g(B)=\Pr(Z\cap B\ne\varnothing).   \tag{24}
\]

Therefore `g` is normalized, monotone, and submodular:

\[
 g(\varnothing)=0,qquad g(B)\le g(B'),\quad B\subseteq B', \tag{25}
\]

\[
                         g(A\cup B)\le g(A)+g(B).           \tag{26}
\]

The desired router would send every clean singleton to the favorable
terminal and every certified adverse set of size at least two to the adverse
terminal.  No single coverage harmonic can do this in either orientation.

First orient `g` as the adverse probability.  If all singleton false-positive
errors obey `g({u})<=epsilon`, then submodularity gives

\[
                         g(B)\le |B|\epsilon.               \tag{27}
\]

For a pair, adverse true-positive error at most `epsilon` would require
`g({u,v})>=1-epsilon`; hence

\[
                         \boxed{\epsilon\ge {1\over3}.}     \tag{28}
\]

Second orient `g` as the favorable probability.  If a singleton is accepted
with probability at least `1-epsilon`, monotonicity forces every superset
containing it to be accepted with at least the same probability.  Rejecting
that pair with error at most `epsilon` gives

\[
                         \boxed{\epsilon\ge {1\over2}.}     \tag{29}
\]

These bounds do not depend on fan-out size.  They persist under arbitrary
scale separation and at every stage depth.  In particular, if a depth-`L`
construction applies ordinary terminal coverage routers successively, its
per-stage classification error cannot tend to zero, so its transfer cannot
converge to the diagonal matrix (1).

There is also a distributional version that directly fits the diffuse
history law.  Conditional on a certified adverse pair `{U,V}`, (26) gives

\[
 E g(\{U,V\})\le 2E g(\{U\}).                              \tag{30}
\]

Thus any adverse detector whose average singleton leakage is `epsilon` has
average pair detection at most `2epsilon`.  Diffusing the labels changes
collision probabilities but does not relax this coverage inequality.

This proves:

> **Ordinary-terminal no-go.** The exact labelled transfer (1), and even an
> approximation with vanishing per-stage classification error, cannot be
> realized by a finite or growing undirected module whose two outputs are
> ordinary fixation/hitting events under additive-OR graphical dynamics.

## 6. Necessary scale separations for any non-coverage realization

Equations (1)--(23) identify a realizable *abstract* transfer, not yet a
finite-graph construction.  An undirected realization at depth `L=L_k`
must supply disjoint stage reservoirs `R_l` and locked targets `v_l` with
the following checkable conditions.

1. **Diffuse row law.** Conditional on a stage event at `v_l`, the parent
   law on `R_l` is `p^{(l)}` and

   \[
   \sum_{l=1}^{L_k}\eta(p^{(l)})=o(1).                    \tag{31}
   \]

   Uniform fan-out of size `m_k` satisfies this if `L_k/m_k->0`.

2. **Locked target clock.** During the entire geometric batch, the same
   target `v_l` is retained and all `K` parent samples see the same row law
   up to total variation error `epsilon_{l,k}` with

   \[
                         \sum_l\epsilon_{l,k}=o(1).         \tag{32}
   \]

3. **Ordered handoff.** On a favorable or certified-adverse stage exit, the
   process reaches the next locked target before any prior reservoir is
   revisited, with failure probability `zeta_{l,k}` satisfying

   \[
                         \sum_l\zeta_{l,k}=o(1).            \tag{33}
   \]

4. **Reverse-arrow suppression.** Because every undirected edge is
   reciprocal, all unintended reverse entrances over the full depth must
   have total probability `o(1)`.  In weighted-degree notation, a sufficient
   trace condition is that the sum of reverse successful-rate ratios at all
   interfaces tends to zero.

5. **Vanishing initialization mass.** If `H_k` is the set of all stage and
   fan-out vertices, then

   \[
                         {|H_k|\over |V(G_k)|}=o(a_k),       \tag{34}
   \]

   where `a_k` is the favorable response amplitude.  This exports every
   uniform-start source term to a bulk reservoir below the response scale.

Conditions (24)--(27) are sufficient for relative transfer accuracy
`1+o(1)`.  If the final theorem needs an *absolute* error smaller than the
adverse amplitude `(r-1)^{L_k}` uniformly on

\[
                         I_k=[1+1/k,2-1/k],                 \tag{35}
\]

then each displayed total error must satisfy the stronger condition

\[
 \boxed{
 {L_k\over m_k}+\sum_l(\epsilon_{l,k}+\zeta_{l,k}
      +\text{reverse}_{l,k})+{|H_k|\over a_k|V(G_k)|}
 =o(k^{-L_k}).}                                            \tag{36}
\]

Here `k^{-L_k}` is the minimum of `(r-1)^{L_k}` on `I_k`.  This is a very
strong uniform requirement.  For the actual pointwise lower quantifier it
is enough to diagonalize errors for each fixed `r>1`; endpoint-uniform
control down to `1+1/k` need not be imposed unless a uniform-on-`I_k`
intermediate theorem explicitly uses it.

The coverage theorem shows that these conditions are only necessary, not
sufficient: even perfect scale separation cannot make an ordinary positive
terminal event implement the router.  They apply only after one supplies a
non-coverage, for example signed, terminal observable.

## 7. What is proved and what remains

Proved here:

- the exact labelled transfer matrix (1);
- its exact power law (6)--(7);
- the finite-terminal no-go (9)--(12);
- the exact diffuse projected law (13)--(22);
- the all-depth coverage/submodularity no-go (24)--(30);
- necessary quantitative scale separations for an undirected realization.

Not yet proved here:

- a signed or non-OR terminal observable that separates the two history
  classes without paying a response-scale uniform-start cost;
- an undirected graph whose rare-event trace implements ordered handoff
  while meeting (31)--(34);
- the identification of the favorable labelled channel with net Bd gain and
  the adverse channel with net dB cost after the complete uniform-start
  fixation trace;
- a positive favorable amplitude surviving the vanishing-density export.

Those are now the exact construction obligations.  Positive ordinary
two-terminal gadgets are closed even at growing fan-out.  The smallest
surviving algebraic route is a signed difference of coverage harmonics.

## 8. Exact replay

Run

```text
PYTHONDONTWRITEBYTECODE=1 ../../../.venv/bin/python -B verify_locked_history_transfer.py
```

The replay checks the labelled matrix, singleton overlap, projected law,
uniform-fanout multiplier, depth error identity, and the sharp elementary
coverage-router error bounds exactly.
