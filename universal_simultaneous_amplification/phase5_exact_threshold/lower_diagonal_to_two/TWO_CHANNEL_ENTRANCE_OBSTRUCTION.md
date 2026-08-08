# A temperature-budget obstruction to complementary two-channel relays

Date: 2026-08-08 (America/Los_Angeles)

## Status and scope

This note gives an exact obstruction to the proposed dense network of
asymmetric two-root triggers.  The obstruction permits arbitrary connected
loopless undirected weighted graphs, arbitrary relay and merger topology, and
arbitrary behavior after the first mutant expansion.  In fact, fixation is
optimistically granted after that first expansion.

The conclusion is deliberately scoped.  It excludes a *complementary
two-channel* architecture in which a class `A` carries asymptotically all Bd
fixation and a disjoint class `B` carries asymptotically all dB fixation.
It does not exclude a construction in which a positive-density class has a
substantial fixation probability under both rules.

There are two sharp consequences for the current construction program.

1. If `B` has positive limiting density, its average dB fixation probability
   is bounded away from one.  Thus the dilute two-root limit
   `u_dB(B)->1` cannot be made dense.
2. Even allowing an arbitrary split between the two specialized classes, the
   complementary-channel scheme cannot simultaneously amplify beyond the
   algebraic number

   \[
   R_{\rm split}=1.7548776662466927\ldots,
   \qquad
   R_{\rm split}^3-2R_{\rm split}^2+R_{\rm split}-1=0. \tag{1}
   \]

   For literal equal two-root triggers the sharper class threshold is the
   golden ratio.

## 1. The exact singleton entrance bound

Let

\[
 P_{xv}={w_{xv}\over d_x},\qquad
 d_x=\sum_z w_{xz},\qquad
 T_v=\sum_xP_{xv}.                                    \tag{2}
\]

Thus `P` is the resident random-walk kernel and `T_v` is the incoming column
sum (temperature) of vertex `v`.  Row normalization gives the exact budget

\[
                         \sum_vT_v=n.                 \tag{3}
\]

Start dB updating from the singleton mutant `{v}`.  Multiplying all rates by
`n`, death of `v` has rate one and causes extinction.  If `x!=v` dies, the
probability that `v` supplies the replacement is

\[
 {r w_{xv}\over d_x+(r-1)w_{xv}}
 ={rP_{xv}\over1+(r-1)P_{xv}}.
\]

Hence the exact rate of the first expansion is

\[
 \beta_v(r)=\sum_x{rP_{xv}\over1+(r-1)P_{xv}},        \tag{4}
\]

and the probability that the first changing event is an expansion is

\[
                         g_v={\beta_v\over1+\beta_v}. \tag{5}
\]

Fixation requires such an expansion.  Moreover

\[
 \beta_v\le rT_v,
 \qquad
 \boxed{h_{dB}(\{v\})\le g_v
       \le {rT_v\over1+rT_v}.}                        \tag{6}
\]

No branching, establishment, or post-establishment approximation enters
(6).

## 2. A sharp density bound

Let `B` be any set of `b=delta*n` vertices.  The function
`phi(t)=rt/(1+rt)` is increasing and concave.  Equations (3) and (6), followed
by Jensen, give the finite-graph inequality

\[
 \boxed{
 {1\over n}\sum_{v\in B}h_{dB}(\{v\})
 \le {\delta r\over r+\delta}.}                       \tag{7}
\]

Indeed, the temperature available to `B` is at most `n`, so its mean is at
most `1/delta`.  Equality in the Jensen envelope would require all the
temperature budget to be placed uniformly on `B`, as well as equality in
both steps of (6) and certain fixation after the first gain.  The bound is
therefore already an optimistic relaxation of any relay implementation.

In particular, if `delta` is bounded below, the average singleton fixation
inside `B` is at most

\[
                         {r\over r+\delta}<1.          \tag{8}
\]

Thus no positive-density dB-specific root class can have singleton success
tending to one.  The high-load root in the asymmetric two-root local limit
must be dilute; a dense `50--50` population of such limits violates the
exact temperature budget (3).

## 3. The complete complementary-channel normal form

Consider a graph sequence with disjoint vertex classes `A_n,B_n` and let

\[
 \alpha_n={|A_n|\over n},\qquad
 \delta_n={|B_n|\over n}.
\]

Every relay, merger, antenna, and far-field start lies either in these
classes or in their complement.  Define the wrong-channel and relay masses

\[
 \eta_B(n)={1\over n}\sum_{v\notin A_n}h_{Bd}(\{v\}),
 \qquad
 \eta_D(n)={1\over n}\sum_{v\notin B_n}h_{dB}(\{v\}). \tag{9}
\]

These terms explicitly count *all* relay starts and all far-field starts;
none are discarded.  From `h<=1` and (7),

\[
 \rho_{Bd}(G_n,r)\le\alpha_n+\eta_B(n),                \tag{10}
\]

\[
 \rho_{dB}(G_n,r)
 \le {\delta_n r\over r+\delta_n}+\eta_D(n).          \tag{11}
\]

Call the architecture complementary if

\[
                         \eta_B(n)+\eta_D(n)\longrightarrow0. \tag{12}
\]

Condition (12) is precisely the advertised division of labor: the
Bd-favored roots carry Bd fixation, the dB-favored roots carry dB fixation,
and the relay/merger population is vanishing and contributes no macroscopic
uniform-start mass.  It allows arbitrary interaction while a trigger is
discordant and arbitrary merging after establishment.

Put `p=(r-1)/r`.  If Bd eventually amplifies, (10) forces
`liminf alpha_n>=p`.  Since the classes are disjoint,

\[
                         \limsup\delta_n\le1-p={1\over r}. \tag{13}
\]

The right side of (11) is increasing in `delta`.  Therefore every
complementary architecture that can amplify Bd satisfies

\[
 \limsup_{n\to\infty}\rho_{dB}(G_n,r)
 \le {r\over r^2+1}.                                  \tag{14}
\]

Comparison with `p` is exact:

\[
 {r\over r^2+1}-{r-1\over r}
 =-{r^3-2r^2+r-1\over r(r^2+1)}.                      \tag{15}
\]

The cubic in (15) has exactly one real root, the number (1), and is positive
above it.  We obtain the following class theorem.

> **Theorem (complementary two-channel obstruction).**  Fix
> `r>R_split`.  No sequence of finite connected loopless undirected weighted
> graphs satisfying (9)--(12) can eventually amplify uniform-singleton
> fixation under both Bd and dB updating.  This remains true if every mutant
> lineage is granted fixation immediately after its first dB expansion.

The endpoint `r=R_split` is not claimed: (14) then matches the limiting
complete-graph baseline, and finite corrections would have to be retained.

## 4. Equal two-root triggers

For one `A` root and one `B` root per trigger, with a vanishing relay class,
`delta_n->1/2`.  Equation (11) becomes

\[
 \limsup\rho_{dB}(G_n,r)\le {r\over2r+1}.             \tag{16}
\]

Since

\[
 {r\over2r+1}-{r-1\over r}
 =-{r^2-r-1\over r(2r+1)},                            \tag{17}
\]

the literal dense two-root proposal is dB-suppressing for every fixed

\[
                         r>{1+\sqrt5\over2},           \tag{18}
\]

under its complementary-success hypothesis.

## 5. Construction consequence

The obstruction identifies the required escape without making a universal
claim about all graph families.  A lower construction approaching fitness
two cannot consist of opposite specialized halves plus a vanishing merger.
It must instead give a positive-density collection of vertices substantial
fixation probability under **both** update rules (or make a nonvanishing
relay population itself carry the missing uniform-start mass).  Merely
moving the high-load dB target from the bulk into a vanishing relay does not
create the temperature needed by a positive-density root class.

## 6. Exact replay

`verify_two_channel_entrance.py` independently:

1. constructs the labelled dB subset chain directly from the update rule;
2. checks `h_dB({v})<=g_v` and (7) exactly on rational weighted graphs;
3. verifies the Jensen and threshold algebra symbolically;
4. isolates the unique real root of the cubic in (1).

All theorem statements above are exact.  No sampled fixation value is used
as proof.
