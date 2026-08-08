# The stationary marked one-sample lift at fitness two

Date: 2026-08-08 (America/Los_Angeles)

## Status

This note gives a **PROVED exact lift** of the fair-geometric dB dual to a
single-sample Markov chain.  It is valid for every loopless row-stochastic
kernel; reversibility is not needed for the identities.

The lift turns the geometric burst into a nearest-neighbour rank process and
recasts the open finite complete-baseline inequality as a stationary
collision inequality:

\[
 \boxed{\Pr\{W=I\}\ge {1\over 2m_K}},\qquad
 m_K={ (n-1)2^{n-2}\over2^{n-1}-1}.                 \tag{1}
\]

Here `I` is the one sampled neighbour and, on a stopping step, `W` is the
uniformly selected new target.  In fact

\[
                 \Pr\{W=I\}={1\over2m},             \tag{2}
\]

where `m=E_Pi|A|`.  Thus (1) is **equivalent**, not merely sufficient, to
`m<=m_K`.

The marked lift also led to a stronger event-rank stochastic-domination
conjecture.  That conjecture is **EXACTLY FALSE** on a six-vertex reversible
integer-weight graph recorded in Section 6.  The actual harmonic collision
inequality (1) remains strict on that witness.  This prevents the new lift
from being mistaken for a completed universal theorem.

## 1. Midpoint measures

Let `Pi` be the stationary law of the proper fair-geometric union dual.  For
a target `v` and a set `C` omitting `v`, define

\[
 \sigma_v(C)=\Pi(C\cup\{v\}),
\]

and let `nu_v(B)` be the effective incoming mass at the output `(v,B)`.
The already proved posterior identity is

\[
 \sum_{v\notin B}\nu_v(B)=|B|\Pi(B).               \tag{3}
\]

Put

\[
 \lambda_v(C)={\sigma_v(C)+\nu_v(C)\over2}.         \tag{4}
\]

If `A_v` adjoins one sample from row `P_v`, the fair-geometric Cayley
identity is

\[
                       \nu_v=\lambda_v A_v.          \tag{5}
\]

Equivalently, `lambda_v` is the law after a geometric number
`M in {0,1,...}` of preliminary samples, with
`Pr(M=j)=2^{-(j+1)}`, before one final sample is taken.

## 2. The marked chain

The marked state space is

\[
 \mathcal X=\{(C,v):v\notin C\}.
\]

From `(C,v)`:

1. sample `I` from row `P_v` and put `B=C union {I}`;
2. toss an independent fair coin;
3. on **continue**, move to `(B,v)`;
4. on **stop**, choose `W` uniformly from `B` and move to
   `(B minus {W},W)`.

Call this kernel `M_P`.  Its rows sum to one because `B` is always nonempty.

### Proposition 1 (exact marked stationarity)

The unnormalised measure `lambda=(lambda_v(C))` is stationary for `M_P`, and

\[
                       \sum_{v,C}\lambda_v(C)=m.      \tag{6}
\]

### Proof

After the sample, (5) gives the marked output mass `nu_v(B)`.  Continuing
therefore contributes `nu_v(B)/2` to `(B,v)`.  For a stopped step ending at
`(D,w)`, put `B=D union {w}`.  Summing over the old target and using (3),

\[
 {1\over2|B|}\sum_{v\notin B}\nu_v(B)
 ={\Pi(B)\over2}={\sigma_w(D)\over2}.
\]

The total incoming mass is `(nu_w(D)+sigma_w(D))/2=lambda_w(D)`.  Finally,
both `sigma_v` and `nu_v` have total mass `Pr(v in A)`, so summing (4) over
`v` gives (6).  \(\square\)

## 3. Nearest-neighbour rank and its exact law

Write `K=|C|` and `x=P_(vC)`.  On a continue step the rank increases by one
exactly when the sample is new.  On a stop step the rank decreases by one
exactly when the sample is redundant.  Hence

\[
 \begin{array}{c|ccc}
 &K+1&K&K-1\\ \hline
 \Pr(\text{next rank}\mid C,v)&(1-x)/2&1/2&x/2.
 \end{array}                                           \tag{7}
\]

Let

\[
 \Lambda_k=\sum_{v,C:\,|C|=k}\lambda_v(C),\qquad
 \pi_k=\Pr_\Pi(|A|=k).
\]

Then directly from (4) and (3),

\[
 \boxed{2\Lambda_k=(k+1)\pi_{k+1}+k\pi_k.}           \tag{8}
\]

If

\[
 q_k={k\pi_k\over m},\qquad \eta_k={\Lambda_k\over m},
\]

then `q` is the stationary size law seen at an active dual event and

\[
 \boxed{\eta_k={q_k+q_{k+1}\over2}},\qquad q_0=q_n=0. \tag{9}
\]

Thus a marked rank has the law `Y-Z`, where `Y` has law `q` and `Z` is an
independent fair Bernoulli variable.  For the complete graph,

\[
 \eta_k^K={\binom{n-1}{k}\over2^{n-1}},\qquad
 q_k^K={\binom{n-2}{k-1}\over2^{n-2}}.               \tag{10}
\]

The complete marked rank is therefore exactly binomial, without a finite
conditioning correction.

## 4. Exact collision and Poisson forms of the target

After the sample, `B=C union {I}` has the active-event rank law `q`.  On a
stopping step, `W` is uniform in `B`; consequently

\[
 \Pr(W=I\mid B,I,\text{stop})={1\over|B|}.
\]

Normalising `lambda` by its mass `m` gives

\[
 E{1\over|B|}=\sum_{k=1}^{n-1}{q_k\over k}
 ={1\over m},                                      \tag{11}
\]

where the last equality is simply `q_k=k pi_k/m` and `sum pi_k=1`.
Including the fair stopping coin proves (2).

There is also a rank-only form on the marked side.  Put `N=n-1` and

\[
 \psi_N=0,\qquad
 \psi_j=2\sum_{k=j+1}^{N}{(-1)^{k-1-j}\over k}
 \quad(0\le j<N).                                  \tag{12}
\]

Inverting (9) gives

\[
 \boxed{E_{\lambda/m}\psi(|C|)={1\over m}.}         \tag{13}
\]

Under the complete binomial law the right side is exactly `1/m_K`.  Hence
either (11) or (13) is an exact restatement of the finite-baseline problem.

## 5. Complete Poisson comparison

Let `phi` solve the one-dimensional complete marked-chain Poisson equation

\[
 (I-M_K)\phi(k)=\psi_k-{1\over m_K}.                 \tag{14}
\]

For a marked state of rank `k`, (7) gives the exact comparison

\[
 (M_P-M_K)\phi(C,v)
 ={1\over2}\left(P_{vC}-{k\over N}\right)
       \{\phi_{k-1}-\phi_{k+1}\}.                  \tag{15}
\]

Stationarity of `lambda` turns (14)--(15) into a single global correlation
identity for `1/m-1/m_K`.  Pointwise control is impossible: the two-state
high-rank edge already forces incompatible radial inequalities.  The
remaining task is to control (15) using the labelled target/sample flow,
not only its rank projection.

## 6. Universal two-step theorem

Although a pointwise Poisson comparison fails, the uniform marked law has an
exact nonnegative response after two applications of the *same* kernel.  Let
`U` denote the uniform law on the `n 2^(n-1)` marked states and put

\[
 f_t(C,v)=t^{|C|},\qquad 0\le t\le1.
\]

For a loopless row-stochastic matrix `P`, define

\[
 \begin{split}
 R&=\sum_{v,i}P_{vi}^2,\\
 C_2&=\sum_i\left(\sum_vP_{vi}\right)^2,\\
 J&=\sum_{v,i}P_{vi}P_{iv}.
 \end{split}                                           \tag{16}
\]

For `n>=4`, write `s=n-2` and

\[
 S_s(t)=\sum_{j=0}^{s-2}{\binom{s-2}{j}\over j+2}t^j,
\]

\[
 \begin{split}
 \alpha_n(t)&={1-t^2\over2n2^s}
 \left\{{(1+t)^{s-1}\over2}-S_s(t)\right\},\\
 \beta_n(t)&={1-t^2\over4n2^s}S_s(t).
 \end{split}                                           \tag{17}
\]

### Proposition 2 (exact two-step sum of squares)

For every loopless row-stochastic `P` and `0<=t<=1`,

\[
 \boxed{
 U M_P^2f_t-Uf_t
 =\alpha_n(t)\left(R-{n\over n-1}\right)
 +\beta_n(t)\{(C_2-J)-(n-R)\}\ge0.}                  \tag{18}
\]

For `n=3`, the corresponding identity is

\[
 U M_P^2f_t-Uf_t
 ={1-t^2\over24}\left(R-{3\over2}\right)\ge0.       \tag{19}
\]

Both defects in (18) are sums of squares.  Rowwise Cauchy--Schwarz gives

\[
 R-{n\over n-1}\ge0,
\]

while, writing `c_i=sum_v P_(vi)`, direct expansion gives

\[
 (C_2-J)-(n-R)
 =\sum_i(c_i-1)^2+{1\over2}\sum_{v,i}(P_{vi}-P_{iv})^2\ge0.              \tag{20}
\]

Moreover, `beta_n(t)>=0`, and

\[
 S_s(t)\le {1\over2}(1+t)^{s-2}
            \le {1\over2}(1+t)^{s-1},
\]

so `alpha_n(t)>=0`.  Equality throughout an open `t` interval forces every
row of `P` to be uniform on the other `n-1` vertices, hence `P=P_K`.

For completeness, if `k=|C|` and `x=P_(vC)`, one marked step gives the exact
radial drift

\[
 (M_P-I)f_t(C,v)
 ={t-1\over2}t^{k-1}\{t-(t+1)x\}.                   \tag{21}
\]

Apply the same transition once more and average over uniform `v` and a
uniform subset `C` of `V minus {v}`.  Splitting the second application into
its continue and stop branches, the continue branch contains the row
collision `R`; the stop-and-retarget branch contains `C_2-J`.  Grouping the
binomial subset averages by `|C|` gives exactly (18).  The verifier performs
this expansion independently over rational directed kernels, including the
separate `n=3` boundary case.

The alternating correction in `psi` disappears after one step:

\[
 M_P(-1)^{|C|}=0,                                    \tag{22}
\]

because the equal continue/stop branches have opposite rank parity.  Also

\[
 \psi_j=2\int_0^1{t^j-(-1)^{N-j}t^N\over1+t}\,dt.   \tag{23}
\]

Integrating Proposition 2 against `2/(1+t)` and using (22)--(23) therefore
proves

\[
             \boxed{U M_P^2\psi\ge U\psi={1\over m_K}},
\]

strictly unless `P=P_K`.  This is a global exact theorem, but it is not yet
the stationary theorem: the sole remaining promotion inequality is

\[
 {\lambda\over m}\psi\ \stackrel{?}{\ge}\ U M_P^2\psi.                 \tag{24}
\]

The inequality cannot be justified by monotonicity in time.  Exact and
high-precision screens contain kernels for which `U M_P^t psi` eventually
decreases, although every screened value remains above the two-step value.
Thus (24), if true, requires a time-homogeneous lower-envelope, return-time,
or stationary-flow argument.

## 7. Exact failure of event-rank stochastic domination

The tempting strengthening

\[
 q\ \le_{\rm st}\ 1+\operatorname{Bin}(n-2,1/2)     \tag{25}
\]

passes the historical exact corpus through five vertices but is false.
On six vertices, take lexicographic edge weights

\[
 (1,3,3,1000,30,1000,300,3,1,10,1,30,1,300,30).    \tag{26}
\]

The graph has complete positive support.  An exact 62-state rational solve
gives

\[
 \sum_{k\ge2}q_k>{15\over16}
\]

with strict excess `0.001463330069...`.  Thus (25) is exactly refuted.
Nevertheless

\[
 \sum_k{q_k\over k}-{1\over m_K}
 =0.046284704868\ldots>0,                            \tag{27}
\]

so the graph remains strictly below the complete fixation baseline.

This witness rules out first-order event-rank domination, but not the
harmonic collision inequality actually required.

## 8. Verification

Run

```text
PYTHONDONTWRITEBYTECODE=1 python3 -B verify_marked_lift.py
```

The verifier reconstructs the proper geometric-union chain over exact
rationals, builds every marked transition, checks row normalisation and
stationarity, verifies (5)--(13), checks complete binomiality, verifies the
two-step identity (18) over exact rational directed kernels, and certifies
both strict signs in Section 7.

Classification:

* **PROVED:** the marked chain, its stationary law, nearest-neighbour rank
  transition, collision identity, complete binomial reference, and universal
  two-step sum-of-squares theorem (18).
* **EXACTLY REFUTED:** first-order stochastic domination (25), as well as
  naive monotonicity of `U M_P^t psi` in time.
* **EXACTLY COMPUTED:** the positive harmonic margin (27) on the same graph.
* **OPEN:** the stationary promotion inequality (24), equivalently the
  universal collision inequality (1) and `rho_dB(G,2)<=rho_dB(K_n,2)`.
