# A nonvanishing endpoint product counterexample

## 1. The result

For an integer `m>=1`, let `G_m` consist of a hub `H`, ordinary vertices
`C_1,...,C_{8m}`, and leaves `L_1,...,L_m`.  The hub and ordinary vertices
induce the unit-weight clique `K_{8m+1}`; each leaf has its sole unit-weight
edge to `H`.  Hence

\[
        |V(G_m)|=9m+1.                                      \tag{1}
\]

All weights and the graph itself are independent of fitness.

**Theorem.**  At `r=3/2`, if the initial mutant is uniform on `V(G_m)`,

\[
\begin{aligned}
 \rho_{Bd}(G_m,3/2)&\longrightarrow {32\over81},\\
 \rho_{dB}(G_m,3/2)&\longrightarrow {8\over27}.             \tag{2}
\end{aligned}
\]

Consequently

\[
 {\rho_{Bd}(G_m,3/2)\over\rho_{Bd}(K_{9m+1},3/2)}
       \longrightarrow {32\over27},\qquad
 {\rho_{dB}(G_m,3/2)\over\rho_{dB}(K_{9m+1},3/2)}
       \longrightarrow {8\over9},                           \tag{3}
\]

and the product of the normalized ratios tends to

\[
                         {256\over243}>1.                    \tag{4}
\]

Thus (4) is a growing, nonvanishing counterexample to the endpoint product
inequality.  It does **not** disprove the endpoint disjunction: the second
ratio in (3) is below one.

The proof below separates the exact finite chain, a rare-state limit, and a
post-establishment lemma.  In particular, (2) is not inferred from a
branching-process survival probability alone.

## 2. Exact lumped chain

Write a mutant configuration as

\[
       (h,i,j)\in\{0,1\}\times\{0,\ldots,c\}
                    \times\{0,\ldots,m\},\qquad c=8m,       \tag{5}
\]

where `h` is the type of `H`, and `i,j` count mutant ordinary vertices and
leaves.  The group `S_c x S_m` acts transitively on each fibre in (5), and
both update rules commute with this action.  The sum of transition
probabilities from a labelled state to any target fibre therefore depends
only on `(h,i,j)`.  This proves strong lumpability, rather than merely
exchangeability of the initial state.

Put `n=c+m+1`, `d=c+m`, and

\[
                 F=n+(r-1)(h+i+j).
\]

For Bd, the six possible type-changing transitions are

\[
\begin{array}{ll}
i\mapsto i+1:&\displaystyle {r(c-i)\over F}
                         \left({h\over d}+{i\over c}\right),\\[4pt]
i\mapsto i-1:&\displaystyle {i\over F}
                         \left({1-h\over d}+{c-i\over c}\right),\\[4pt]
0\mapsto1\text{ at }H:&\displaystyle {r\over F}
                         \left({i\over c}+j\right),\\[4pt]
1\mapsto0\text{ at }H:&\displaystyle {1\over F}
                         \left({c-i\over c}+m-j\right),\\[4pt]
j\mapsto j+1:&\displaystyle {rh(m-j)\over dF},\\[4pt]
j\mapsto j-1:&\displaystyle {(1-h)j\over dF}.
\end{array}                                                   \tag{6}
\]

Multiplication of every rate in a state by `F` is a time change and does not
alter absorption probabilities.  We use this time-changed version below.

For dB, the six changing probabilities are

\[
\begin{array}{ll}
i\mapsto i+1:&\displaystyle {c-i\over n}
 {r(h+i)\over c+(r-1)(h+i)},\\[4pt]
i\mapsto i-1:&\displaystyle {i\over n}
 {c-i+1-h\over c+(r-1)(i-1+h)},\\[4pt]
0\mapsto1\text{ at }H:&\displaystyle {1\over n}
 {r(i+j)\over d+(r-1)(i+j)},\\[4pt]
1\mapsto0\text{ at }H:&\displaystyle {1\over n}
 {d-i-j\over d+(r-1)(i+j)},\\[4pt]
j\mapsto j+1:&\displaystyle {h(m-j)\over n},\\[4pt]
j\mapsto j-1:&\displaystyle {(1-h)j\over n}.
\end{array}                                                   \tag{7}
\]

Terms leading outside (5) are zero and the remaining mass is the self-loop.
Equations (6)--(7) follow directly by listing the parent--target ordered
pairs.  The verifier independently aggregates all labelled rows for a small
instance and compares them with these formulas.

## 3. The establishment lemma

The following elementary lemma supplies the step that a bare early
branching approximation omits.

**Lemma 1 (a mesoscopic core seed fixes).**  Fix `r>1` and `a>0`, and
put `c=am` (along an integer subsequence).  Let `k_m` satisfy

\[
             k_m\longrightarrow\infty,qquad k_m=o(m).
\]

For either update rule, uniformly in the hub type and in the leaf count,

\[
 \inf_{h,j}\Pr_{(h,k_m,j)}(\text{fixation})\longrightarrow1. \tag{8}
\]

**Proof.**  Only explicit rate ratios are needed.  Stop first when `i=0` or
`i=(1-delta)c`, where `delta>0` is fixed and small.  Conditional on a change
of `i`, (6) gives, uniformly in `h,j`,

\[
 {q^+_{Bd}\over q^-_{Bd}}
 \ge {r\over1+c/[d(c-i)]}=r-o(1)                             \tag{9}
\]

throughout this strip.  From (7), direct cancellation gives

\[
 {q^+_{dB}\over q^-_{dB}}
 =r\,{h+i\over i}\,{c-i\over c-i+1-h}\,
 {c+(r-1)(i-1+h)\over c+(r-1)(i+h)}=r-o(1)                  \tag{10}
\]

uniformly when `k_m<=i<=(1-delta)c`.  Choose `eta>0` so that the right
sides exceed `1+eta`.  The usual exponential gambler-ruin supermartingale,
applied only at times when `i` changes, bounds the probability of hitting
zero first by `(1+eta)^(-k_m)`.

It remains to control the upper strip.  Put `R=c-i`.  While
`R<=2 delta c`, (6) gives

\[
 {\operatorname{rate}(R\mapsto R-1)\over
  \operatorname{rate}(R\mapsto R+1)}
 \ge {r(1-2\delta)R\over R+1},                              \tag{11}
\]

and (7) gives the same lower bound up to a factor `1-o(1)`.  Take `delta`
so that `r(1-2 delta)>1`.  Above a fixed `R_0`, the right side of (11) is
`1+eta_0` for some `eta_0>0`.  Apply the exponential supermartingale
between `R_0` and `2 delta c`, and then use the strong Markov property at
returns to `R_0`.  For every fixed `A`, the chance to escape before time
`m^A` is at most `C_A m^(A+1) exp(-gamma_A m)=o(1)`.  The polynomial
factor bounds the number of `R`-changes after uniformization.  The same
comparison shows that `R` reaches `R_0` in `O(log m)` mean time and
thereafter has a geometric excursion tail, up to this negligible event.

For completeness, here is the absorption argument inside this confined
strip.  It is useful because this is where an establishment-only proof would
have a gap.

For Bd, first observe the leaf process during recurrent epochs `R<=R_0`;
the geometrically tailed `R`-excursions only change its clock.  Conditional
on `(i,j)`, the hub's off-to-on and on-to-off rates in the time change
following (6) are

\[
 A=r(i/c+j),\qquad B=R/c+m-j.                               \tag{12}
\]

Renewal decomposition at successive returns of the hub gives the following
up/down ratio whenever the leaf count is stopped away from an endpoint,
uniformly apart from an `o(1)` error:

\[
 {A\,r(m-j)\over B j}
 = {r^2(i/c+j)(m-j)\over(R/c+m-j)j}
 \ge {r^2\over1+2\delta}                                   \tag{13}
\]

for `1<=j<m`.  Here is a block proof that also handles both endpoints.
When `j=O(1)`, a hub excursion has probability `O(1/m)` of one leaf
change and `O(1/m^2)` of two.  On the time scale `t/m`, recurrent returns
of `R` to `R<=R_0` therefore produce a linear leaf process with positive
immigration from the core and per-particle birth/death ratio `r^2+o(1)>1`.
Repeated immigrant families hit `m^(2/3)` in polynomial time with
probability `1-o(1)`.  Inequality (13), stopped between `m^(2/3)` and
`epsilon m`, then makes the chance of returning to zero exponentially
small.  Thus any fixed small `epsilon>0` is reached in polynomial time.

For `y=j/m` in `[epsilon,1-epsilon]`, the hub flips at order-`m` rate,
whereas `y` has jumps `1/m` at order-one rate.  Divide an interval of
length `m` into blocks of original-time length `m^(-1/2)`.  On each
block the hub makes order `m^(1/2)` transitions while `y` and `R/c`
change by `o(1)`.  The two-state occupation formula from (12), an
exponential holding-time bound, and a union bound over the blocks give,
uniformly on compact subintervals of `(0,1)`,

\[
 {d y\over d(t/m)}
 ={y(1-y)(r^2-1)\over
   (a+1)\{1+(r-1)y\}}+o(1).                              \tag{13a}
\]

The martingale part has quadratic variation `O(1/m)` on every bounded
slow-time interval.  Thus (13a), whose drift is strictly positive, carries
`y` from `epsilon` to `1-epsilon` with probability `1-o(1)`.

Finally put `L=m-j`.  For bounded `L`, the same excursion calculation,
now on slow time, gives

\[
 L\mapsto L-1:\ {rL\over a+1}+o(1),\qquad
 L\mapsto L+1:\ {L\over r(a+1)}+o(1).                   \tag{13b}
\]

This is a subcritical linear deficit process.  It reaches `L=0` in
polynomial time and has a geometric excursion tail.  While `L=0`, the
hub is resident for only an `O(m^{-2})` fraction of time when `R=O(1));
the `R`-rates converge to death `rR` and birth `R`.  Hence `R` hits
zero during one of the polynomially many `L=0` visits with probability
`1-o(1)`; the hub then activates and the chain is fixed.  Every phase takes
polynomial time, so the preceding exponentially stronger core-confinement
bound applies throughout.

For dB, (11) confines `R` in exactly the same way.  Whenever `h=1`, every
resident leaf changes at rate one after multiplication of (7) by `n`.
In the upper strip, the hub has a uniformly positive activation rate and a
uniformly bounded deactivation rate.  Choose a fixed, sufficiently large
`C_*`.  An activated interval of length `C_* log m` then occurs within
polynomial time with probability `1-o(1)`: each successive activation has
conditional chance at least `m^{-C_*}` to last that long.  During such an
interval all leaves change to mutant with probability `1-o(1)`.  The
`h=1` version of (11) couples `R` to a subcritical linear birth--death
chain, so increasing `C_*` if necessary also makes its chance of not
hitting zero during the interval `o(1)`.  Repetition
precedes escape from the strip with probability `1-o(1)`.  At the end of a
successful long interval we have `h=1,R=0,j=m`, which is fixation.  This
proves (8).  `square`

All estimates just used are finite-state estimates: waiting times are
exponential after the displayed statewise time changes.  The block argument
also displays the occupation and martingale errors, rather than assuming a
deterministic post-establishment trajectory.

## 4. A mutant ordinary clique vertex

Take, for example, `k_m=floor(m^(1/3))`.  Until `i` first hits `0` or `k_m`,
and while the number of non-core mutants is bounded, the `i`-rates from both
(6) and (7) are

\[
             i\mapsto i+1: ri\{1+o(1)\},\qquad
             i\mapsto i-1: i\{1+o(1)\}.                    \tag{14}
\]

The accumulated probability of a hub or leaf event before this stopping
time is `o(1)`.  Truncation at a fixed population level, followed by letting
that level grow, makes (14) a standard coupling with the linear birth--death
process.  Its probability, from one particle, of reaching an unbounded
level before zero is

\[
                         p=1-{1\over r}.                    \tag{15}
\]

Lemma 1 turns hitting `k_m` into fixation with probability `1-o(1)`.  Hence,
for either rule,

\[
 \Pr_{(0,1,0)}(\text{fixation})\longrightarrow1-{1\over r}.
                                                                    \tag{16}
\]

The same conclusion is unaffected by starting at the hub, but its value is
not needed: the hub has mass `1/(9m+1)` under uniform initialization.

## 5. A mutant leaf under Bd

We now derive the nontrivial value in (2).  Use the Bd time change following
(6), start with `(h,i,j)=(0,0,1)`, and observe the chain on the slow time
`tau=t/m`.  Suppose momentarily that `j=k` is fixed and bounded.

The hub activates at rate `r k`.  During an activated excursion its return
rate is `m+O(1)`, while its rates of creating a new leaf and an ordinary-core
mutant are, respectively,

\[
                 {r\over9}+o(1),\qquad {8r\over9}+o(1).     \tag{17}
\]

When the hub is resident, a mutant leaf dies at rate `1/(9m)+o(1/m)`.
Consequently, per leaf and per unit slow time, the limiting rates are

\[
 \lambda={r^2\over9}\quad\hbox{(new leaf)},\qquad
 \mu={1\over9}\quad\hbox{(leaf death)},                    \tag{18}
\]

and ordinary-core seeds arrive at rate `8r^2/9`.  By (15), a seed establishes
with probability `p=1-1/r`; failed seed families return to zero in `o(m)`
time, and the chance of a second slow event during such a family is `o(1)`.
Thus successful seeds mark the limiting leaf process at rate

\[
                  \kappa={8r^2p\over9}={8r(r-1)\over9}      \tag{19}
\]

per leaf.

Here is a direct convergence justification.  Stop when `j` reaches a fixed
`J` or a core family reaches `k_m`.  A hub excursion has probability
`O(1/m)` of one productive event and `O(1/m^2)` of two.  The duration of a
failed core family has an exponentially decreasing tail after conditioning
on extinction.  Summing these errors over `O(m)` excursions proves
convergence of every stopped path to the killed branching chain with rates
(18)--(19).  The probability that this limiting chain reaches `J` before
extinction or marking decreases to zero as `J` tends to infinity: after
adjoining the mark as a death, its no-mark mass is a subcritical Doob
transform.  We may therefore let first `m`, then `J`, tend to infinity.

Let `q` be the probability that the limiting process becomes extinct before
a successful mark, starting from one leaf.  Branching independence gives
`q^k` from `k` leaves, and the first-event equation is

\[
       \lambda q^2-(\lambda+\mu+\kappa)q+\mu=0,             \tag{20}
\]

where the relevant root is the one in `(0,1)`.  At `r=3/2`,

\[
 \lambda={1\over4},\qquad \mu={1\over9},\qquad
 \kappa={2\over3},
\]

so (20) is `9q^2-37q+4=0`, with roots `1/9` and `4`.  Lemma 1 shows that a
mark fixes with probability `1-o(1)`.  Therefore

\[
          \Pr^{Bd}_{(0,0,1)}(\text{fixation})
                    \longrightarrow 1-q={8\over9}.         \tag{21}
\]

## 6. A mutant leaf under dB

Multiply the probabilities in (7) by `n`.  From `(0,0,1)`, the only two
changing events before either extinction or hub activation have rates

\[
       1\quad\hbox{(leaf death)},\qquad
       {r\over 9m+(r-1)}\quad\hbox{(hub activation)}.        \tag{22}
\]

Even granting fixation with probability one after activation, (22) gives

\[
 \Pr^{dB}_{(0,0,1)}(\text{fixation})
 \le {r\over9m+(r-1)+r}=O(m^{-1})\longrightarrow0.          \tag{23}
\]

This bound is exact and needs no branching approximation.

## 7. Uniform initialization and comparison

Let `u_H,u_C,u_L` denote fixation from a mutant hub, ordinary vertex, and
leaf.  Strong lumpability and uniform initialization give exactly

\[
       \rho_U(G_m,r)={u_H+8m u_C+m u_L\over9m+1}.            \tag{24}
\]

At `r=3/2`, equations (16), (21), and (23), together with `0<=u_H<=1`, yield

\[
\begin{aligned}
 \rho_{Bd}(G_m,3/2)&\to {8\over9}{1\over3}
                          +{1\over9}{8\over9}={32\over81},\\
 \rho_{dB}(G_m,3/2)&\to {8\over9}{1\over3}={8\over27}.
\end{aligned}                                               \tag{25}
\]

Direct one-dimensional first-step recurrences on `K_n` give

\[
 \rho_{Bd}(K_n,r)={1-r^{-1}\over1-r^{-n}},\qquad
 \rho_{dB}(K_n,r)={n-1\over n}
             {1-r^{-1}\over1-r^{-(n-1)}}.                   \tag{26}
\]

Both tend to `1/3` at `r=3/2`.  Dividing (25) by (26) proves (3)--(4).

## 8. Exact status

- **PROVED:** exact strong lumping and transition formulas (6)--(7).
- **PROVED:** the post-establishment implication, including the high-density
  absorption step, by Lemma 1.
- **PROVED:** both singleton limits and the uniform limits (2).
- **PROVED:** the nonvanishing normalized-product violation (4).
- **PROVED:** this family is asymptotically dB-suppressing.
- **OPEN:** the weaker universal assertion that no graph simultaneously
  amplifies Bd and dB at `r=3/2`.
