# Geometric batching versus the reversed-arrow dual

## 1. Status

The proposed universal inequality at `r=3/2`,

\[
 \frac{m_D(G)}{m_C(G)}
 \leq
 R_n:=\frac{n-1}{n}
       \frac{1-(2/3)^n}{1-(2/3)^{n-1}},                 \tag{1}
\]

is **OPEN**.  Here `m_U=E_{pi_U}|A|`, `C` is the unbatched
reversed-arrow dual, and `D` is the geometric-union dB dual.  This note
records an exact interpolation which reduces (1) to one quantitative
derivative inequality, together with exact obstructions to several simpler
proofs.

Everything below is derived from the generators.  Numerical searches are
labelled as such and are not used as proof.

## 2. Forward edge slowing

Write `P_vu=w_vu/d_v`, let `S` be a mutant set, and put

\[
 x_v(S)=\sum_{u\in S}P_{vu}.
\]

The forward process dual to `C` has flip rates

\[
 q_C(S,S+v)=\frac32x_v(S),\qquad
 q_C(S+v,S)=1-x_v(S).                                  \tag{2}
\]

The dB rates are obtained by multiplying both directions of the same
configuration edge by

\[
 c_e=\frac1{1+x_v(S)/2}.                               \tag{3}
\]

Thus `C` and dB have identical edgewise up/down ratios.  Only their symmetric
edge speeds differ.

For `0<=s<=1`, introduce the exact interpolation

\[
 q_s(S,S+v)=\frac{(3/2)x_v(S)}{1+s x_v(S)/2},\qquad
 q_s(S+v,S)=\frac{1-x_v(S)}{1+s x_v(S)/2}.              \tag{4}
\]

It joins `C` at `s=0` to dB at `s=1`.

## 3. The whole interpolation is additive

This fact is useful and exact.  Set

\[
 r_s=1+\frac{s}{2},\qquad
 \beta_s=\frac{3/2-r_s}{r_s}.
\]

At every target run the following two independent graphical mechanisms:

1. at rate one, replace the target by the OR of `K_s` row-`P` samples,
   where `K_s` is geometric on `{1,2,...}` with mean `r_s`;
2. at rate `beta_s`, retain the target and add the OR of an independent
   `K_s` sample batch.

The first mechanism has resident-to-mutant rate

\[
 \frac{r_sx}{1+(r_s-1)x}
\]

and mutant-to-resident rate

\[
 \frac{1-x}{1+(r_s-1)x}.
\]

The second adds

\[
 \beta_s\frac{r_sx}{1+(r_s-1)x}
 =\frac{(3/2-r_s)x}{1+s x/2}.
\]

Their sum is exactly (4).  Transposing the two Boolean maps therefore gives
an exact set dual `E_s` for every `s`, and

\[
 \rho_s(G)=\frac1n\mathbb E_{\pi_s}|A|.                \tag{5}
\]

The size drift of this dual is

\[
 \mathcal L_s|A|
 =\sum_{v\in A}\left[
   -1+\sum_{u\notin A}
       \frac{(3/2)P_{vu}}{1+sP_{vu}/2}
   \right].                                            \tag{6}
\]

For a fixed set, its derivative is the transparent collision penalty

\[
 \partial_s\mathcal L_s|A|
 =-\frac34\sum_{v\in A,u\notin A}
   \frac{P_{vu}^2}{(1+sP_{vu}/2)^2}.                   \tag{7}
\]

The stationary law also changes with `s`; (7) alone does not determine the
derivative of (5).

## 4. Exact complete-graph curve

On `K_n`, the count chain has

\[
 u_k(s)=\frac{(3/2)k(n-k)}{n-1+sk/2},\qquad
 d_k(s)=\frac{k(n-k)}{n-1+s(k-1)/2}.                   \tag{8}
\]

Consequently

\[
 \prod_{j=1}^{\ell}\frac{d_j(s)}{u_j(s)}
 =\left(\frac23\right)^\ell
  \left(1+\frac{s\ell}{2(n-1)}\right).                \tag{9}
\]

Define

\[
 A_n=\sum_{\ell=1}^{n-1}(2/3)^\ell,qquad
 B_n=\frac1{2(n-1)}
     \sum_{\ell=1}^{n-1}\ell(2/3)^\ell.               \tag{10}
\]

The complete fixation curve and its logarithmic derivative are

\[
 \rho_s(K_n)=\frac1{1+A_n+sB_n},\qquad
 \partial_s\log\rho_s(K_n)
 =-\frac{B_n}{1+A_n+sB_n}.                             \tag{11}
\]

At the endpoints, (11) gives exactly

\[
 \frac{\rho_1(K_n)}{\rho_0(K_n)}=R_n.                 \tag{12}
\]

Hence (1) would follow from the pointwise-in-`s` statement

\[
 \boxed{
 \partial_s\log\rho_s(G)
 \leq -\frac{B_n}{1+A_n+sB_n}}
 \quad(0\leq s\leq1).                                 \tag{13}
\]

This differential inequality is **OPEN**.  Direct optimization on positive
symmetric weights through order six and random screens through order seven
found no violation, but this is numerical evidence only.

## 5. Exact occupation-current identity

Let `h_s(S)` be the fixation committor of (4), and let

\[
 \nu_s(S)=\mathbb E_\alpha\int_0^T
       \mathbf1\{X_t=S\}\,dt                          \tag{14}
\]

be the transient occupation measure from the uniform-singleton law `alpha`.
For the configuration edge `e=(S,S+v)`, oriented upward, put

\[
 x_e=x_v(S),\quad
 \Delta h_e=h_s(S+v)-h_s(S),                           \tag{15}
\]

and

\[
 J_e=\nu_s(S)q_s(S,S+v)
     -\nu_s(S+v)q_s(S+v,S),                            \tag{16}
\]

where the occupation mass of an absorbing endpoint is zero.  Differentiating
the finite harmonic system and grouping the two orientations of every edge
gives

\[
 -\partial_s\log\rho_s(G)
 =\frac1{\rho_s(G)}
   \sum_e
   \frac{x_e/2}{1+sx_e/2}\,J_e\Delta h_e.             \tag{17}
\]

The net current through every rank cut above the starting rank is exact:

\[
 \sum_{\substack{e=(S,S+v)\\ |S|=k}}J_e
 =\rho_s(G),\qquad k=1,\ldots,n-1.                    \tag{18}
\]

Equation (18) is just net-crossing conservation: a path started at rank one
crosses such a cut once net upward if it fixes and zero times net if it goes
extinct.

Equations (17)--(18) isolate the missing theorem.  A proof of (13) needs a
weighted circulation inequality involving `x_e`, `Delta h_e`, and `J_e`.
Level flux alone is insufficient because individual internal currents can be
negative.  For the exact triangle with edge weights `(1,1,100)` at `s=0`,
the edge from mask `001` to mask `011` has

\[
 J_e=-\frac{4317}{186944}<0.                            \tag{19}
\]

## 6. Exact failure of statewise committor comparison

The `C` committor is a monotone submodular coverage function: if `Pi_C` is
the stationary `C` dual law, then

\[
 h_0(S)=\Pr_{A\sim\Pi_C}(A\cap S\ne\varnothing).       \tag{20}
\]

Nevertheless it is not dB-superharmonic statewise.  For the positive
symmetric weights

```text
[[0, 7, 3, 17],
 [7, 0, 15, 6],
 [3, 15, 0, 5],
 [17, 6, 5, 0]]
```

at mutant mask `0110`, exact arithmetic gives

\[
 \mathcal L_{dB}h_0
 =\frac{19320943980314880741118267311163716984393}
        {1350751487384526329949760252671364412445376}
 >0.                                                       \tag{21}
\]

Thus neither monotonicity nor submodularity supplies a pointwise sign
certificate.

## 7. Neutral-episode interpretation

There is a second exact description of the endpoint chains.  Observe either
set chain only at global neutral events.  In both chains the number of
selective arrows before the next neutral arrow is geometric with the same
law.

- In `C`, every selective arrow resamples a target uniformly from the
  currently occupied set, and the final neutral arrow does the same.
- In `D`, one target is selected at the start; every selective arrow and the
  final neutral arrow are locked to that target.

If `alpha_U(A)=|A|pi_U(A)/m_U` is the event-epoch law, then

\[
 m_U=\frac1{\mathbb E_{\alpha_U}(1/|A|)}.              \tag{22}
\]

The desired ratio is therefore also a sharp invariant-measure comparison
between resampled-target and locked-target geometric episodes.  No valid
pathwise ordering of those episode kernels is presently known.

## 8. Infinitesimal batching as an overlap inequality

There is a second exact form of (17) at `s=0`.  It exposes the collision
content of the conjecture.

Let `L_C` be the set generator `C`, let `pi_C` be its stationary law, put
`m_C=E_pi|A|`, and define the Poisson potential

\[
 \psi(A)=\int_0^\infty
   \left(\mathbb E_A|A_t|-m_C\right)dt.                \tag{23}
\]

Additivity implies that `psi` is monotone and submodular on nonempty sets,
and

\[
 L_C\psi=m_C-|A|.                                      \tag{24}
\]

Write its nonnegative discrete curvature as

\[
 \kappa_\psi(B;i,j)
 =\psi(B+i)+\psi(B+j)-\psi(B+i+j)-\psi(B).             \tag{25}
\]

For stationary `A`, sum over occupied targets `v`, and conditionally sample
`U,Z` independently from `P_v*`.  Define

\[
 \begin{aligned}
 C_3&=\mathbb E\sum_{v\in A}
       \kappa_\psi(A;U,Z),\\
 C_2&=\mathbb E\sum_{v\in A}
       \kappa_\psi(A-v+U;v,Z).
 \end{aligned}                                         \tag{26}
\]

Expanding the graphical interpolation to first order gives

\[
 L'_0
 =\frac12(N_2-N_1)-\frac34(S_1-I)
  +\frac14(S_2-S_1),                                   \tag{27}
\]

where `N_j` replaces the target by the union of `j` samples and `S_j`
retains it and adds that union.  Stationarity of `pi_C`, together with iid
symmetry of `U,Z`, reduces (27) exactly to

\[
 \boxed{
 m'_0=\frac12(C_2-\tfrac32 C_3)},\qquad
 \left.\partial_s\log\rho_s\right|_{s=0}
 =\frac{C_2-(3/2)C_3}{2m_C}.                           \tag{28}
\]

More generally, at fitness `r`, (28) is

\[
 m'_0=(r-1)(C_2-rC_3).                                 \tag{29}
\]

The curvature has a literal Gram representation.  For a fixed realization
of the additive graphical map at time `t`, let `H_x(t)` be the set of initial
sites whose descendants cover `x`.  Then

\[
 \kappa_t(B;i,j)
 =\sum_x
  \mathbf1\{i,j\in H_x(t),\ H_x(t)\cap B=\varnothing\}.
                                                               \tag{30}
\]

Thus every curvature matrix is positive semidefinite, and `kappa_psi` is its
time integral.

For one fixed coverage hyperedge `H`, put `q_v=P_v(H)`.  Averaging over the
stationary background `A` turns the two terms in (26) into

\[
 \begin{aligned}
 C_3(H)&=\sum_{v\notin H}q_v^2
   \Pr_{\pi_C}\{v\in A,\ A\cap H=\varnothing\},\\
 C_2(H)&=\sum_{v\in H}q_v(1-q_v)
   \Pr_{\pi_C}\{A\cap H=\{v\}\}.                    \tag{31}
 \end{aligned}
\]

Equivalently, if `h_0` is the coverage committor, the integrand of
`(3/2)C_3-C_2` is

\[
 \frac32\sum_{v\notin H}q_v^2\,[h_0(H+v)-h_0(H)]
 -\sum_{v\in H}q_v(1-q_v)\,[h_0(H)-h_0(H-v)].         \tag{32}
\]

The set `H_x(t)` evolves as the forward link process from singleton `x`.
Integrating (32) over `x,t` is exactly the occupation-current formula (17)
at zero.  The positive-semidefinite representation is therefore not by
itself sufficient: (32) is precisely the statewise expression whose sign can
fail.

For a symmetric doubly stochastic kernel, `pi_C` is the conditioned product
law with mutant odds `r-1`.  At general fitness `r`, its Bernoulli density is
`(r-1)/r`, and (31) simplifies the integrand of `rC_3-C_2` to a positive
scalar times

\[
 \sum_v q_v^2-\sum_{v\in H}q_v
 =\mathbf1_H^T(P^2-P)\mathbf1_H.                       \tag{33}
\]

The matrix in (33) is not positive semidefinite when `P` has eigenvalues in
`(0,1)`.  This identifies the remaining difficulty even in the regular
case: the graphical occupation average must control the positive spectral
modes.  On the complete kernel all nonconstant eigenvalues are negative and
(33) reduces to `|H|(n-|H|)/(n-1)^2`.

## 9. Occupation averaging and a regular-case mass transport

The overlap formula has a useful exact occupation form.  Let `Q_r` denote
the forward link process

\[
 Q_r(H,H+v)=rP_v(H),\qquad
 Q_r(H,H-v)=1-P_v(H),                              \tag{34}
\]

and let `H_t^x` be this process started from `{x}`.  The hyperedges in the
coverage representation (30) have exactly this law.  Hence (31), before any
pointwise sign estimate, gives

\[
 rC_3-C_2
 =\sum_x\int_0^\infty
   \mathbb E_{\{x\}}\Gamma(H_t)\,dt,                 \tag{35}
\]

where

\[
 \begin{aligned}
 \Gamma(H)={}&r\sum_{v\notin H}P_v(H)^2
   \Pr_{\pi_C}\{v\in A,A\cap H=\varnothing\}\\
 &-\sum_{v\in H}P_v(H)(1-P_v(H))
   \Pr_{\pi_C}\{A\cap H=\{v\}\}.
 \end{aligned}                                      \tag{36}
\]

Thus the exact derivative is an occupation average under the graphical
`C`-flow:

\[
 m'_0=-(r-1)\sum_x\int_0^\infty
       \mathbb E_{\{x\}}\Gamma(H_t)\,dt.             \tag{37}
\]

There is a sharper mass-transport identity when `P` is symmetric and doubly
stochastic.  Put

\[
 p=\frac{r-1}{r},\qquad Z=1-r^{-n},\qquad
 E(H)=\mathbf1_H^T(P^2-P)\mathbf1_H.                 \tag{38}
\]

The stationary `C` law is Bernoulli-`p` conditioned to be nonempty, so (36)
reduces to

\[
 \Gamma(H)=\frac pZ r^{-(|H|-1)}E(H).                \tag{39}
\]

Now `z(H)=r^{-|H|}` is `Q_r`-harmonic.  Its Doob transform has upward rates
`P_v(H)` and downward rates `r(1-P_v(H))`; complementation converts it back
to `Q_r`.  Since `E(V\setminus H)=E(H)`, (35) becomes

\[
 rC_3-C_2=\frac pZ T(P),\qquad
 T(P):=\sum_x\mathbb E_{V\setminus\{x\}}
       \int_0^\tau E(H_t)\,dt.                       \tag{40}
\]

Because `m_C=np/Z`, the normalized derivative is therefore

\[
 \boxed{
 \left.\partial_s\log\rho_s\right|_{s=0}
 =-\frac{r-1}{n}T(P).}                               \tag{41}
\]

This is an exact occupation-averaged version of the indefinite Gram form
(33).  It admits a further neutral-flow decomposition.  Define

\[
 I(H)=\mathbf1_H^TP\mathbf1_H,qquad
 B(H)=\sum_{v\notin H}P_v(H)^2.                       \tag{42}
\]

For the neutral link generator `Q_1`, direct expansion gives

\[
 Q_1I=2E.                                             \tag{43}
\]

Moreover `Q_rI=2E+2(r-1)B`.  Dynkin's formula from every co-singleton, and
the isothermal absorption probability

\[
 \phi_{n-1}=\frac{1-r^{-(n-1)}}{1-r^{-n}},            \tag{44}
\]

give the exact mass-transport identity

\[
 \boxed{
 T(P)=\frac n2\,[n\phi_{n-1}-(n-2)]-(r-1)B_{\rm occ}(P),}
 \tag{45}
\]

where

\[
 B_{\rm occ}(P)=\sum_x\mathbb E_{V\setminus\{x\}}
        \int_0^\tau B(H_t)\,dt.                     \tag{46}
\]

The first term in (45) is independent of `P`.  Consequently, within the
regular class, the desired complete-graph derivative bound at `s=0` is
equivalent to saying that the complete kernel *maximizes the accumulated
collision local time* (46).  This extremal occupation statement is open.
It cannot be replaced by a pointwise comparison: on the four-cycle, for
the alternating two-set, `B(H)=2`, whereas the complete-kernel value at rank
two is `8/9`.

The occupation average nevertheless has the conjectured direction in an
exact noncomplete example.  At `r=3/2`,

\[
 T(C_4)=\frac{92}{65}>\frac{88}{65}=T(K_4),\qquad
 B_{\rm occ}(C_4)=\frac{208}{65}<\frac{216}{65}
=B_{\rm occ}(K_4).                                  \tag{47}
\]

The collision term also has an exact Green-function interpretation involving
only one, two, and three ancestral lines.  Let `a=r-1`, let `C_t` be the
reversible branching--coalescing `C`-chain, and define the centered source
`b_P` by

\[
 b_P(A)=
 \begin{cases}
 1,&A=\{i\},\\[2mm]
 \displaystyle\frac{2}{a}(P_{ij}^2-2P_{ij}),
      &A=\{i,j\},\\[2mm]
 \displaystyle\frac{2}{a^2}\sum_{v\in A}
       P_{vu}P_{vz},
      &A=\{v,u,z\},\\[2mm]
 0,&|A|\ge4.
 \end{cases}                                        \tag{48}
\]

Here `u,z` in the third line are the other two elements of `A`.  The
stationary law is

\[
 \pi_C(A)=\frac{a^{|A|}}{r^n-1},                     \tag{49}
\]

and a row-sum calculation gives `E_pi b_P=0`.  Forward--dual disjointness
started from `V\setminus{x}`, followed by reversibility of `C`, gives

\[
 \boxed{
 B_{\rm occ}(P)
 =\sum_x\int_0^\infty
       \mathbb E_{\{x\}}^C b_P(C_t)\,dt
 =\sum_x[(-L_C)^{-1}b_P](\{x\}).}                   \tag{50}
\]

Thus (46) is literally a two-neighbor collision Green function.  Formula
(50) is exact, but standard trace or spectral-gap estimates are not sharp
enough yet: both the reversible generator `L_C` and the centered source
`b_P` vary with `P`.

There are three exact boundary checks.

First, every symmetric stochastic zero-diagonal kernel of order four has

\[
 P=\begin{pmatrix}
 0&a&b&c\\ a&0&c&b\\ b&c&0&a\\ c&b&a&0
 \end{pmatrix},\qquad a+b+c=1.
\]

Lumping the link chain into its five translation orbits and solving its
Green equation gives, for every `r>1`,

\[
 \boxed{
 T(P)=T(K_4)+
 \frac{r(r-1)}{(r+1)(r^2+1)}
 \left(\operatorname{tr}P^2-\frac43\right),}         \tag{51}
\]

where

\[
 T(K_4)=\frac{4(r^2+2r+3)}{3(r+1)(r^2+1)}.           \tag{52}
\]

Equivalently, the excess in (51) is

\[
 \frac{4r(r-1)}{(r+1)(r^2+1)}
 \sum_{x\in\{a,b,c\}}(x-\tfrac13)^2.                \tag{53}
\]

This proves complete-minimality of `T`, uniquely, for every connected
order-four regular kernel.  The same algebra extends to the disconnected
boundary by continuous limits.  It is the desired trace/eigenvalue
certificate in the first nontrivial order.

Second, for the regular complete bipartite kernel on `K_{m,m}`, put
`n=2m`.  If its two mutant counts are `(i,j)`, then

\[
 E(i,j)=\frac{(i-j)^2}{m}.                            \tag{54}
\]

The embedded rank chain is the simple biased walk with upward probability
`r/(r+1)`.  If `N_{n-1}` is its expected number of jumps to absorption from
rank `n-1`, applying Dynkin's formula to `(i-j)^2` gives

\[
 T(K_{m,m})=\frac{N_{n-1}+1}{r+1}
 =\frac{n-1}{n}T(K_n)+\frac1{r+1}.                   \tag{55}
\]

For `m>=2`, this is strictly larger than `T(K_n)`.  Indeed the difference is
positive exactly when

\[
 \frac{\sum_{\ell=0}^{n-1}\ell r^{-\ell}}
      {(n-1)\sum_{\ell=0}^{n-1}r^{-\ell}}
 <\frac1{r+1};                                       \tag{56}
\]

after writing `t=1/r`, the numerator after cross multiplication pairs into
positive terms `(n-2j)(t^j-t^{n-j})`, `j<n/2`.

Third, consider two three-vertex modules, with total within-module row mass
`1-epsilon` and total cross-module row mass `epsilon`.  At `r=3/2`, exact
two-count lumping yields

\[
 \begin{aligned}
 T(P_\epsilon)-T(K_6)
 ={}&\frac{2(5\epsilon-3)^2}{3325(\epsilon+1)}\\
 &\times
 \frac{39\epsilon^3+2\epsilon^2-13439\epsilon-10602}
 {13\epsilon^2-149\epsilon-114}.                    \tag{57}
 \end{aligned}
\]

Both polynomials in the last quotient are negative on `[0,1]`.  Thus the
complete value, at `epsilon=3/5`, is the unique minimum along this entire
modular-to-bipartite segment.  The exact boundary values are

\[
 \lim_{\epsilon\downarrow0}T(P_\epsilon)=\frac{42}{19},
 \qquad T(P_1)=\frac{1212}{665},
 \qquad T(K_6)=\frac{5676}{3325}.                    \tag{58}
\]

Numerical optimization over positive symmetric stochastic kernels of orders
four, five, and six returned the complete kernel as the minimizer of `T`.
Random segment tests also found `T` convex on the symmetric stochastic
polytope through order seven, for several fitness values.  This is
falsification evidence, not a proof; convexity would imply the full regular
case immediately by permutation averaging.

There is an exact second-variation formula which isolates the convexity
problem.  On the transient forward-link state space let

\[
 A(P)=-Q_r(P),\qquad
 f_P(H)=\mathbf1_H^T(P^2-P)\mathbf1_H,\qquad
 T(P)=\alpha A(P)^{-1}f_P,                            \tag{59}
\]

where `alpha` places unit mass at every co-singleton.  Along a symmetric
stochastic line `P_t=P+tDelta`, write `A_t=A(P_t)`,
`A_Delta=partial_t A_t`, and

\[
 u_t=A_t^{-1}f_{P_t},\qquad
 y_t=\partial_tu_t
 =A_t^{-1}(f'_{P_t}-A_\Delta u_t),\qquad
 \nu_t=\alpha A_t^{-1}.                              \tag{60}
\]

Since

\[
 \frac12 f''_{P_t}(H)
 =\mathbf1_H^T\Delta^2\mathbf1_H
 =\|\Delta\mathbf1_H\|^2,                           \tag{61}
\]

differentiating `A_tu_t=f_{P_t}` twice gives

\[
 \boxed{
 T''(t)=2\nu_t\!\left[
       \|\Delta\mathbf1_H\|^2-A_\Delta y_t
       \right].}                                     \tag{62}
\]

The first term in (62) is nonnegative.  The response term has no known
sign and cannot be discarded: on exact rational order-four directions it is
strictly negative after the minus sign and cancels part of the square term,
although their sum remains positive as guaranteed by (51).  Thus convexity
is reduced exactly to the resolvent inequality

\[
 \nu_t A_\Delta y_t
 \leq \nu_t\|\Delta\mathbf1_H\|^2.                  \tag{63}
\]

No proof of (63) for arbitrary order is presently known.  The reversible
Green formula (50) has the exact polarization form

\[
 B_{\rm occ}(P)=\frac{1}{4\pi_1}
 \left[\mathcal V_P(s+b_P)-\mathcal V_P(s-b_P)\right], \tag{64}
\]

where `pi_1=(r-1)/(r^n-1)` is the mass of one specified singleton,
`s=1_{\{|A|=1\}}-\mathbb E_\pi 1_{\{|A|=1\}}`, and

\[
 \mathcal V_P(c)=\sup_{g:\,E_\pi g=0}
 \left\{2\langle c,g\rangle_\pi-
             \langle g,(-L_C(P))g\rangle_\pi\right\}.
                                                               \tag{65}
\]

For fixed `c`, (65) is a supremum of affine functions of `P`, because the
reversible Dirichlet form is affine in `P`.  But (64) is a *difference* of
two such functionals and `b_P` itself depends quadratically on `P`; it does
not by itself prove convexity.

## 10. Verification artifacts

- `verify_committor_sign_counterexample.py` checks (20)--(21) exactly.
- `verify_interpolation_certificates.py` checks the additive interpolation,
  complete-graph formula, occupation derivative, cut currents, and the exact
  negative current (19).
- `verify_regular_mass_transport.py` checks the identities and finite symbolic
  certificates in (40)--(63), including the Doob transform, neutral-flow and
  reversible-Green identities, full order-four trace formula, modular
  factorization, and square-plus-response Hessian calculation.
- `search_derivative_ratio.py` is a numerical falsification tool for (13).
- `search_batching_ratio.py` is a numerical endpoint falsification tool for
  (1).
- `search_regular_mass_transport.py` searches the symmetric stochastic
  polytope for violations of the regular-case occupation inequality.
