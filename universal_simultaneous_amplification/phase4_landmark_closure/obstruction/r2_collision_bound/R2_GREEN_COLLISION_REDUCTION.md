# The exact Green--collision reduction at dB fitness two

Date: 2026-08-02 (America/Los_Angeles)

## Status

The identities in this note are **PROVED** directly from the forward
heat-bath chain and the exact geometric-union dual.  They reduce the finite
complete-graph maximizer conjecture to one explicit stationary inequality.
That final inequality remains **OPEN**:

\[
 \rho_{\rm dB}(G,2)\le \rho_{\rm dB}(K_n,2)
 \quad\Longleftrightarrow\quad {\cal L}(G)\le {\cal V}(G).
 \tag{1}
\]

Here \({\cal V}\) is a manifestly nonnegative subset-dispersion functional,
whereas \({\cal L}\) is a weighted stationary cut surplus.  The reduction is
finite, exact, and scale invariant.  It is not yet a proof of (1).

The same calculation also produces an exact factorial collision hierarchy.
It isolates a sufficient universal density ceiling
\(\rho_{\rm dB}(G,2)\le1/2\), but the required stationary second-collision
inequality is likewise **OPEN**.

## 1. Heat-bath edges and level flux

Let

\[
 P_{vu}={w_{vu}\over d_v},\qquad
 h(x)={2x\over1+x},\qquad N=n-1.
\]

At fitness two, the forward dB clock at vertex \(v\) writes a mutant with
probability \(h(P_{vS})\), independently of the old status of \(v\).  Thus,
on the hypercube edge from \(S\) to \(S+v\),

\[
 q(S,v)=h(P_{vS}),\qquad q(S,v)+q(S+v,v)=1.       \tag{2}
\]

Let \(f(S)\) be the fixation committor for the graph under study and put

\[
 \Delta(S,v)=f(S+v)-f(S)\ge0.
\]

For \(0\le k\le n-1\), define

\[
 D_k=\sum_{|S|=k,\ v\notin S}\Delta(S,v),\qquad
 W_k=\sum_{|S|=k,\ v\notin S}q(S,v)\Delta(S,v). \tag{3}
\]

Summing the harmonic equation for \(f\) over the entire level \(k\) and
using (2) gives the exact flux recurrence

\[
 \boxed{W_k+W_{k-1}=D_{k-1}\quad(1\le k\le n-1).} \tag{4}
\]

This recurrence contains no lumpability assumption.  It is valid on every
finite loopless heat-bath kernel.

Let \(\Pi\) be the stationary law of the exact dB geometric-union dual.  The
coverage representation

\[
 f(S)=\Pr_{A\sim\Pi}(A\cap S\ne\varnothing)
\]

gives the further exact formulas, with \(H=A^c\),

\[
 D_k=E_\Pi\left[|A|{ |H|\choose k}\right],       \tag{5}
\]

and

\[
 W_k=E_\Pi\sum_{v\in A}
       \sum_{\substack{S\subseteq H\\|S|=k}}h(P_{vS}). \tag{6}
\]

In particular, (4) is also an exact hierarchy of stationary coupon-union
identities.

## 2. Complete harmonic and Green weights

For the complete graph, the level-edge mutant probability is

\[
 q_k^K=h(k/N)={2k\over N+k}.
\]

The exact complete-graph committor is

\[
 \boxed{
 \phi_K(k)=
 {1-(n+k)/(n2^k)\over1-2^{1-n}}.}                \tag{7}
\]

Consequently

\[
 \rho_K:=\rho_{\rm dB}(K_n,2)
 ={(n-1)2^{n-2}\over n(2^{n-1}-1)}.              \tag{8}
\]

Let \(\mu_k\) be the expected occupation time of one *labelled* level-
\(k\) state for the complete forward chain started from a uniformly random
singleton.  The reversible speed of the complete count chain is

\[
 m_k={2^{k-1}(n-1)\over k(n-k)},
\]

and its killed Green function gives

\[
 \mu_k={m_k(1-\phi_K(k))\over {n\choose k}}
 ={(n+k)/(2n)-2^{k-n}\over
 n{n-2\choose k-1}(1-2^{1-n})},                 \tag{9}
\]

for \(1\le k\le n-1\), with \(\mu_0=\mu_n=0\).  Set

\[
 c_k=\mu_k+\mu_{k+1}\quad(0\le k\le n-1).       \tag{10}
\]

Every \(c_k\) is strictly positive.

Applying the complete Green kernel to the arbitrary committor and pairing
the two endpoints of every hypercube edge yields

\[
 \boxed{
 \rho_{\rm dB}(G,2)-\rho_K
 =\sum_{k=0}^{n-1}c_k R_k,\qquad
 R_k=W_k-q_k^KD_k.}                               \tag{11}
\]

The endpoint residuals \(R_0,R_{n-1}\) vanish.  Formula (11) is the desired
aggregate identity: an individual level residual need not have the complete
sign.

Indeed, on the regular weighted \(K_4\)

\[
 (w_{01},w_{02},w_{03},w_{12},w_{13},w_{23})
 =(1,1,2,2,1,1),                                  \tag{12}
\]

exact arithmetic gives

\[
 R_1=-{1\over82},\qquad R_2={1\over205}>0.        \tag{13}
\]

Thus the per-level Jensen claim \(R_k\le0\) is **FALSE**, even for a
positive regular kernel.

## 3. Tangent dispersion and the single open sign

For \(a,x\in[0,1]\), the concavity of \(h\) has the exact remainder

\[
 h(x)-h(a)
 ={2(x-a)\over(1+a)^2}
 -{2(x-a)^2\over(1+a)^2(1+x)}.                   \tag{14}
\]

For a dual set \(A\), write \(a=|A|\), \(s=|A^c|\), and

\[
 C_\partial(A)=\sum_{v\in A,u\notin A}P_{vu}.
\]

Define the positive rank coefficient

\[
 U_s=\sum_{k=1}^s c_k{2N^2\over(N+k)^2}
 {s-1\choose k-1}.                                \tag{15}
\]

Also define

\[
 \begin{aligned}
 {\cal V}(G)=E_\Pi\sum_{v\in A}
 \sum_{k=1}^{|A^c|}c_k{2\over(1+k/N)^2}
 \sum_{\substack{S\subseteq A^c\\|S|=k}}
 {\{P_{vS}-k/N\}^2\over1+P_{vS}}.
 \end{aligned}                                    \tag{16}
\]

Every atom in (16) is nonnegative.  Summing the linear term in (14) over
all \(k\)-subsets uses

\[
 \sum_{\substack{S\subseteq A^c\\|S|=k}}P_{vS}
 ={s-1\choose k-1}P_{v,A^c}.
\]

Therefore (11) becomes the exact Green--collision decomposition

\[
 \boxed{
 \rho_{\rm dB}(G,2)-\rho_K={\cal L}(G)-{\cal V}(G),}
 \tag{17}
\]

where

\[
 \boxed{
 {\cal L}(G)=E_\Pi\left[
 U_{|A^c|}\left\{C_\partial(A)
 -{|A||A^c|\over n-1}\right\}\right].}           \tag{18}
\]

Thus the universal finite-baseline theorem is exactly the inequality

\[
 \boxed{{\cal L}(G)\le {\cal V}(G).}              \tag{19}
\]

Neither term can simply be discarded.  On the weighted path with consecutive
edge weights \((1,2)\),

\[
 {\cal L}={2\over135}>0,\qquad
 {\cal V}={8\over135},\qquad
 \rho-\rho_K=-{2\over45}.                         \tag{20}
\]

So the tempting claim \({\cal L}\le0\) is **EXACTLY FALSE**.  On the
regular graph (12),

\[
 {\cal L}={207\over22960},\qquad
 {\cal V}={247\over22960},\qquad
 \rho-\rho_K=-{1\over574}.                        \tag{21}
\]

The missing theorem must use stationarity to bound the cut surplus by the
full subset-dispersion, not merely show that either level residual or the
linear cut term is nonpositive.

### 3.1 Conductance form, exact covariance, and quadratic control

The cut surplus has two other useful exact forms.  Row stochasticity gives

\[
 \begin{aligned}
 Z(A)&:=C_\partial(A)-{|A||A^c|\over N}\\
 &= {|A|(|A|-1)\over N}
   -\sum_{v,u\in A}P_{vu}.                           \tag{22}
 \end{aligned}
\]

For undirected conductances this is

\[
 \boxed{
 Z(A)=\sum_{\{u,v\}\subseteq A}
 \left\{{2\over N}-w_{uv}
 \left({1\over d_u}+{1\over d_v}\right)\right\}.} \tag{23}
\]

Thus the apparent oriented-cut term is actually a signed *internal-pair
deficit*.  The antisymmetric part of the row kernel cancels exactly.

Let

\[
 \Pi_K(A)={|A^c|\over n(2^{n-1}-1)},
 \qquad \varnothing\ne A\ne V,                     \tag{24}
\]

be the complete dual law at fitness two.  On every fixed cardinality level,
the uniform average of \(Z(A)\) is zero for every row-stochastic loopless
kernel: each directed entry is internal with probability
\(|A|(|A|-1)/(nN)\), and \(\sum_{v,u}P_{vu}=n\).  Since \(U_{|A^c|}\) is
constant on a level,

\[
 E_{\Pi_K}\{U_{|A^c|}Z(A)\}=0.
\]

Writing \(g(A)=\Pi(A)/\Pi_K(A)\), (18) is therefore the exact covariance

\[
 \boxed{
 {\cal L}(G)=E_{\Pi_K}\left[(g(A)-1)
 U_{|A^c|}Z(A)\right].}                             \tag{25}
\]

This confirms that the linear term is second order near the complete graph:
the raw graph perturbation has zero reference mean and must correlate with
the induced stationary-law perturbation.  Cauchy--Schwarz gives the rigorous
but currently nonclosing estimate

\[
 |{\cal L}|
 \le \sqrt{\chi^2(\Pi\Vert\Pi_K)}
 \left(E_{\Pi_K}[U_{|A^c|}^2Z(A)^2]\right)^{1/2}.   \tag{26}
\]

The dispersion already controls the same cut surplus quadratically.  Put
\(s=|A^c|\), \(a=n-s\), and
\(\delta_v=P_{v,A^c}-s/N\).  Then
\(Z(A)=\sum_{v\in A}\delta_v\).  Keeping only the \(k=s\) atom in (16),
using \(1+P_{v,A^c}\le2\), and applying Cauchy gives

\[
 \boxed{
 {\cal V}(G)\ge E_\Pi\left[
 {c_{|A^c|}\over
 |A|(1+|A^c|/N)^2}\,Z(A)^2\right].}               \tag{27}
\]

Equations (25)--(27) isolate a precise remaining stability problem: control
the stationary likelihood displacement from \(\Pi_K\) by the same
row-subset dispersion.  A bare pointwise Cauchy or Young inequality cannot
do this sharply, because \({\cal L}\) is linear in \(Z\) before its
stationary/reference cancellation is used.

There is also an exact Poisson/Dirichlet formulation.  Let \(D_P\) and
\(D_K\) be the dB-dual generators on the nonempty proper subsets for the
actual and complete kernels.  Because the right side has zero \(\Pi_K\)
mean, solve

\[
 D_K\psi(A)=U_{|A^c|}Z(A),                         \tag{28}
\]

with any additive normalization.  Stationarity of \(\Pi\) gives

\[
 \boxed{
 {\cal L}(G)=E_\Pi[(D_K-D_P)\psi].}                \tag{29}
\]

A statewise domination of this forcing by the integrand of \({\cal V}\)
would prove (19), but it is **FALSE**.  On the path (20), with the
normalization \(\psi(\{0\})=0\), the state \(A=\{0,1\}\) has exact residual

\[
 v(A)-(D_K-D_P)\psi(A)=-{16\over4455}<0,           \tag{30}
\]

where \(v(A)\) denotes the conditional dispersion in (16).  Thus the
Dirichlet representation is exact, but its sign too is irreducibly
stationary/aggregate.

## 4. Exact factorial collision hierarchy

For a dual state \(A\) with hole set \(H=A^c\), define

\[
 B_j(A)=\sum_{v\in A}
 \sum_{\substack{C\subseteq H\\|C|=j}}h(P_{vC}),
 \qquad B_0(A)=0.                                  \tag{31}
\]

Here \(B_j\) is a sum of probabilities that a geometric burst hits at least
one vertex of a named \(j\)-set; it is not the probability that all \(j\)
vertices appear.

The hit-indicator generator, summed over all \(j\)-subsets, gives

\[
 \boxed{
 E_\Pi\{B_j+B_{j-1}\}
 =E_\Pi\left[|A|{|H|\choose j-1}\right]
 \quad(1\le j\le n-1).}                           \tag{32}
\]

Equivalently, (32) is stationarity of \({|H|\choose j}\).  In particular,

\[
 E B_1=E|A|=:m,qquad
 E(B_2+B_1)=E\{|A||H|\}.                           \tag{33}
\]

For nonnegative \(x_1,\ldots,x_j\) with sum at most one,

\[
 h\left(\sum_i x_i\right)
 \ge {j+1\over2j}\sum_i h(x_i).                   \tag{34}
\]

Indeed, concavity first gives
\(\sum_i h(x_i)\le jh(q/j)\), where \(q=\sum_i x_i\), and
\(h(q)/(jh(q/j))=(j+q)/(j(1+q))\ge(j+1)/(2j)\).
Subadditivity gives the matching elementary upper bound.  Hence, pointwise,

\[
 {j+1\over2j}{|H|-1\choose j-1}B_1(A)
 \le B_j(A)
 \le {|H|-1\choose j-1}B_1(A).                    \tag{35}
\]

The stationary second-factorial inequality

\[
 E|A|^2\le {n\over2}E|A|                           \tag{36}
\]

would imply \(m\le n/2\) by Jensen and therefore the universal density
ceiling \(\rho_{\rm dB}(G,2)\le1/2\).  By (33), (36) is exactly

\[
 \boxed{E B_2\ge\left({n\over2}-1\right)m.}        \tag{37}
\]

The pointwise lower bound (35) does not imply (37), because it is weakest
precisely on states with few holes.  Higher members of (32) retain the
missing information, but no positive combination closing (37) is currently
known.

There is a particularly compact cut-variance form of the same open
second-moment inequality.  Define

\[
 S_1(A)=\sum_{v\in A,u\notin A}
 {\{P_{vu}-1/N\}^2\over1+P_{vu}}.                  \tag{38}
\]

Applying (14) with baseline \(1/N\) to every oriented cut edge gives,
pointwise,

\[
 B_1(A)={2|A||A^c|\over n}
 +{2N^2\over n^2}\{Z(A)-S_1(A)\}.                 \tag{39}
\]

Since stationarity gives \(E B_1=m\), (39) yields the exact identity

\[
 \boxed{
 E\{Z-S_1\}={n\over N^2}
 \left(E|A|^2-{n\over2}E|A|\right).}              \tag{40}
\]

Consequently (36), and hence the density ceiling, is exactly the stationary
cut-dispersion inequality

\[
 \boxed{E_\Pi Z(A)\le E_\Pi S_1(A).}              \tag{41}
\]

This is perhaps the shortest surviving collision target.  It is not
pointwise: on graph (12), each of the states
\(\{0,1\},\{0,2\},\{1,3\},\{2,3\}\) has
\(Z-S_1=16/135>0\).  On the path (20), the state containing the two endpoints
has \(Z-S_1=3/4\).  Stationarity is again essential.

## 5. A false pairwise shortcut to the density ceiling

Put

\[
 p_i=\Pr_\Pi(i\in A),\qquad
 a_{vi}=\Pr_\Pi(v\in A,\ i\notin A).
\]

Stationarity of the coordinate (1_{\{i\in A\}}) gives

\[
 p_i=\sum_v h(P_{vi})a_{vi}.                       \tag{42}
\]

A tempting pairwise estimate is

\[
 a_{vi}\stackrel{?}{\le}
 (1+P_{vi})p_v(1-p_i).                             \tag{43}
\]

Since (h(x)(1+x)=2x), summing (43) in (42) would prove the
component-odds inequality

\[
 {p_i\over1-p_i}\le2\sum_vP_{vi}p_v,              \tag{44}
\]

and summing (44) followed by Jensen would give (E|A|/n\le1/2).
Estimate (43) is **FALSE**, including on positive support.

First take the unweighted path (0-1-2-3).  For its exact stationary dual,

\[
 p_0=p_3={2\over7},\qquad
 a_{03}={16\over77},\qquad P_{03}=0.
\]

Thus the proposed upper side is (10/49), and its margin is

\[
 {10\over49}-{16\over77}=-{2\over539}<0.           \tag{45}
\]

The zero transition in (45) is not the cause.  On the regular weighted
(K_4) with

\[
 w_{02}=w_{13}=18,qquad w_{uv}=1
 \quad\hbox{on the other four edges},              \tag{46}
\]

every weighted degree is (20), and

\[
 p_i={827\over2026}\quad(0\le i<4),\qquad
 a_{01}={1029\over4052},\qquad P_{01}={1\over20}.
\]

The exact margin in (43) is

\[
 -{24507\over82093520}<0.                          \tag{47}
\]

The actual component-odds slack in (44) is nevertheless positive at every
vertex of (46), with common value

\[
 {153822\over1214587}>0.                           \tag{48}
\]

Therefore (45)--(47) close only the pairwise route.  The summed
component-odds inequality (44), and hence the universal density ceiling,
remain **OPEN**.

## 6. Verification

Run

```text
python3 verify_green_collision_reduction.py
```

The verifier uses exact rational arithmetic.  It independently builds the
forward heat-bath chain and the geometric-union dual, solves both systems,
checks Boolean coverage, verifies every level recurrence, and certifies
(11), (17)--(21), and the strict counterexamples (45)--(48).
