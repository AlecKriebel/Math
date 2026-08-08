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

## 7. Exact density factorisation of the remaining sign

The promotion problem has a compact Perron--Frobenius form.  Besides the
marked space `X`, introduce the active space

\[
 \mathcal Y=\{(B,v):\varnothing\ne B\subseteq V\setminus\{v\}\}.
\]

Write `R` for the fixed continue-or-retarget channel from `Y` to `X`, and
`A_P` for the one-sample channel from `X` to `Y`, so `M_P=A_P R`.  The
complete reference laws are

\[
 U(C,v)={1\over n2^N},\qquad
 \nu_K(B,v)={|B|\over nN2^{N-1}}.                  \tag{25}
\]

One checks directly that `nu_K R=U`.  Its reverse density channel
`Q` is especially simple.  If `k=|C|`, then

\[
 (\mathcal Qg)(C,v)
 ={k\over N}g(C,v)
 +{1\over N}\sum_{u\notin C\cup\{v\}}g(C\cup\{v\},u).                  \tag{26}
\]

Let `mu=lambda/m` be marked stationarity, let `nu=mu A_P`, and define
density ratios

\[
 h={d\mu\over dU},\qquad g={d\nu\over d\nu_K}.
\]

Then `h=Q g`.  Conversely, direct enumeration of the two possible
pre-sample caches gives, for `b=|B|`,

\[
 (\mathcal B_Ph)(B,v)
 ={N\over2b}\left\{P_{vB}h(B,v)
       +\sum_{i\in B}P_{vi}h(B\setminus\{i\},v)\right\}.              \tag{27}
\]

Thus the actual active density is the positive fixed point

\[
                 \boxed{g=\mathcal T_Pg},\qquad
 \mathcal T_P=\mathcal B_P\mathcal Q.              \tag{28}
\]

The left invariant functional is size weight:

\[
 \sum_{B,v}b(\mathcal T_Pg)(B,v)=\sum_{B,v}b g(B,v).
\]

With the probability normalization,

\[
 \sum_{B,v}b g(B,v)=nN2^{N-1}=\sum_{B,v}b.          \tag{29}
\]

The collision target is the *unweighted* mass of this Perron vector:

\[
 {1\over m}={1\over nN2^{N-1}}\sum_{B,v}g(B,v).     \tag{30}
\]

Since `|Y|=n(2^N-1)`, complete maximality is now exactly the scalar fixed
point inequality

\[
 \boxed{\sum_{B,v}g(B,v)\ge |\mathcal Y|.}          \tag{31}
\]

No stationary subset law appears in (26)--(31).  These equations quantify
precisely where reuse of one row kernel matters.  Indeed

\[
 (\mathcal T_P1)(B,v)={N P_{vB}\over b},            \tag{32}
\]

and the active density after successive applications of the same marked
environment is `T_P^j1`.  In particular,

\[
 U M_P^2\psi={1\over nN2^{N-1}}\sum_{B,v}(\mathcal T_P^2 1)(B,v).
\]

Consequently the sole promotion inequality (24) is exactly

\[
 \boxed{\sum_{B,v}g(B,v)
       \stackrel{?}{\ge}
       \sum_{B,v}(\mathcal T_P^2 1)(B,v).}          \tag{33}
\]

This is the minimal surviving obstruction: prove (33) for the Perron vector
of the explicit positive operator (26)--(28), normalized by (29).  A
state-dependent sample policy destroys (31), so the proof must use that the
same row `P_v` is reused for every cache with target `v`.

There is a useful annealed interpretation.  Averaging all conjugates of a
fixed loopless `P` over uniform vertex permutations gives `P_K`.  Refreshing
that conjugation before every step produces the complete chain, whereas
fixing it produces the powers in (32)--(33).  Proposition 2 is the exact
two-step quenched-minus-annealed square.  Extending that positivity to the
Perron limit would prove (33); no such all-history argument is claimed here.

## 8. Exact failure of event-rank stochastic domination

The tempting strengthening

\[
 q\ \le_{\rm st}\ 1+\operatorname{Bin}(n-2,1/2)     \tag{34}
\]

passes the historical exact corpus through five vertices but is false.
On six vertices, take lexicographic edge weights

\[
 (1,3,3,1000,30,1000,300,3,1,10,1,30,1,300,30).    \tag{35}
\]

The graph has complete positive support.  An exact 62-state rational solve
gives

\[
 \sum_{k\ge2}q_k>{15\over16}
\]

with strict excess `0.001463330069...`.  Thus (34) is exactly refuted.
Nevertheless

\[
 \sum_k{q_k\over k}-{1\over m_K}
 =0.046284704868\ldots>0,                            \tag{36}
\]

so the graph remains strictly below the complete fixation baseline.

This witness rules out first-order event-rank domination, but not the
harmonic collision inequality actually required.

Two further exact reversible five-vertex witnesses delimit the promotion
route.  Edge weights

```text
(1,20000,1,15000,660,164,1280000,1000000,3150,293)
```

give `U M_P^37 psi < U M_P^36 psi`, while the stationary value remains
strictly above `U M_P^2 psi`.  Thus temporal monotonicity is false.  Edge
weights

```text
(12,3150,1850000,812000,1810000,4180,295000,4,159000,1)
```

give the strict reverse of (33) when `psi` is replaced by the rank-zero PGF
observable.  Thus no pointwise-in-the-PGF-parameter stationary envelope is
available.  Both signs are certified over exact rationals.

## 9. Verification

Run

```text
PYTHONDONTWRITEBYTECODE=1 python3 -B verify_marked_lift.py
```

The verifier reconstructs the proper geometric-union chain over exact
rationals, builds every marked transition, checks row normalisation and
stationarity, verifies (5)--(13), checks complete binomiality, verifies the
two-step identity (18) over exact rational directed kernels, and certifies
all strict counterexample and surviving-promotion signs in Section 8.

Classification:

* **PROVED:** the marked chain, its stationary law, nearest-neighbour rank
  transition, collision identity, complete binomial reference, and universal
  two-step sum-of-squares theorem (18).
* **PROVED REDUCTION:** the Perron fixed-point formulation (26)--(33).
* **EXACTLY REFUTED:** first-order stochastic domination (34), naive temporal
  monotonicity, and a full radial-PGF stationary envelope.
* **EXACTLY COMPUTED:** the positive harmonic margin (36) and strict
  promotion on every displayed hostile witness.
* **OPEN:** the stationary promotion inequality (24)/(33), equivalently the
  universal collision inequality (1) and `rho_dB(G,2)<=rho_dB(K_n,2)`.
