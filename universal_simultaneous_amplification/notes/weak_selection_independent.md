# Exact weak-selection coefficients from the neutral genealogy

Date: 2026-08-01 (America/Los_Angeles)

This note was derived from the process definitions, without a literature
search.  No outside contact was made.  All initial mutants below are placed
uniformly at random.

## 1. Statement of the formulas

Let

\[
 d_i=\sum_jw_{ij},\qquad D=\sum_i d_i,\qquad
 H=\sum_i\frac1{d_i},\qquad C=H^{-1}.
\]

For each update rule, let \(\tau^U_{ij}\) be the expected number of neutral
updates until two ancestral lineages, initially at distinct vertices \(i,j\),
coalesce.  Put \(\tau^U_{ii}=0\).  Then

\[
\boxed{
c_{\rm Bd}(G)=
\frac{2C}{n^2}\sum_{\{i,j\}}
 \frac{w_{ij}}{d_i d_j}\tau^{\rm Bd}_{ij}}
\tag{1}
\]

and

\[
\boxed{
c_{\rm dB}(G)=
\frac1{n^2D}\sum_v\frac1{d_v}
 \sum_{i,j}w_{vi}w_{vj}\tau^{\rm dB}_{ij}.}
\tag{2}
\]

The outer sum in (1) is over unordered pairs.  The inner sum in (2) is over
ordered pairs; diagonal terms vanish because \(\tau_{ii}=0\).

Equivalently, both comparisons admit exact effective-size criteria.  Define
the neutral ancestral rates

\[
 a^{\rm Bd}_{ij}=\frac{w_{ij}}{d_j},\qquad
 a^{\rm dB}_{ij}=\frac{w_{ij}}{d_i},
\tag{3}
\]

their exit rates \(t_i^U=\sum_j a^U_{ij}\), and their stationary
probabilities

\[
 \pi_i^{\rm Bd}=\frac{C}{d_i},\qquad
 \pi_i^{\rm dB}=\frac{d_i}{D}.
\tag{4}
\]

Let \(h^U_{ij}=\tau^U_{ij}/n\).  Thus \(h^U_{ij}\) is the meeting time for
two continuous-time lineages with rates \(a^U\).  Define the remeeting time

\[
 R_i^U=\frac1{2t_i^U}+
       \sum_j\frac{a^U_{ij}}{t_i^U}h^U_{ij}
\tag{5}
\]

and

\[
 N_U=2\sum_i\pi_i^U t_i^U R_i^U.
\tag{6}
\]

Then

\[
\boxed{c_{\rm Bd}(G)=\frac{N_{\rm Bd}-1}{2n},\qquad
       c_{\rm dB}(G)=\frac{N_{\rm dB}-2}{2n}.}
\tag{7}
\]

Since

\[
c_{\rm Bd}(K_n)=\frac{n-1}{2n},\qquad
c_{\rm dB}(K_n)=\frac{n-2}{2n},
\tag{8}
\]

the exact weak-amplification tests are

\[
\boxed{N_{\rm Bd}>n\quad\hbox{and}\quad N_{\rm dB}>n,}
\tag{9}
\]

respectively.  In particular, a simultaneous weak amplifier would have to
satisfy both inequalities in (9).

## 2. Neutral reproductive-value martingales

Write a state as \(x=(x_i)\in\{0,1\}^n\).  At neutrality the following are
martingales:

\[
 M_{\rm Bd}(x)=\sum_i\frac{C}{d_i}x_i,
 \qquad
 M_{\rm dB}(x)=\sum_i\frac{d_i}{D}x_i.
\tag{10}
\]

For Bd, the expected one-step increment is

\[
 \frac1n\sum_{u,v}\frac{w_{uv}}{d_u}\frac{C}{d_v}(x_u-x_v)=0,
\]

because the coefficient \(Cw_{uv}/(d_ud_v)\) is symmetric in \(u,v\).
For dB it is

\[
 \frac1n\sum_{v,u}\frac{w_{vu}}{d_v}\frac{d_v}{D}(x_u-x_v)=0.
\]

At absorption either martingale equals the fixation indicator.  A uniformly
placed neutral single mutant therefore has mean fixation probability
\(n^{-1}\sum_i\pi_i=1/n\), even though the individual starting vertices need
not have fixation probability \(1/n\).

Let \(r=1+s\), and let \(T\) be absorption time.  If

\[
 f_U(x)=\left.\frac{\partial}{\partial s}
 E_s[M_U(X_{t+1})-M_U(X_t)\mid X_t=x]\right|_{s=0},
\tag{11}
\]

then

\[
 \left.\frac{\partial}{\partial s}\rho_U(G,1+s)\right|_{s=0}
 =E_0\sum_{t<T}f_U(X_t).
\tag{12}
\]

This follows by writing the selected fixation probability as

\[
 M_U(x)+E_s\sum_{t<T}E_s[\Delta M_U\mid X_t]
\]

and differentiating at zero.  The derivative of the path law multiplies the
zero neutral drift and hence drops out.  Analyticity is also immediate from
the finite transient matrix \((I-Q(s))^{-1}\) near \(s=0\).

## 3. First-order drift under Bd

Let \(k=\sum_i x_i\).  The selected expected martingale increment is

\[
 \sum_{u,v}\frac{1+s x_u}{n+s k}
 \frac{w_{uv}}{d_u}\frac{C}{d_v}(x_u-x_v).
\]

The derivative of the denominator contributes a multiple of the neutral
drift, hence zero.  Using \(x_u^2=x_u\), one obtains

\[
 f_{\rm Bd}(x)=\frac{C}{n}\sum_{\{i,j\}}
 \frac{w_{ij}}{d_i d_j}(x_i-x_j)^2.
\tag{13}
\]

## 4. First-order drift under dB

Put

\[
 p_{vi}=\frac{w_{vi}}{d_v},\qquad
 \bar x_v=\sum_i p_{vi}x_i.
\]

Conditional on death at \(v\), the selected parent probability expands as

\[
 \frac{w_{vu}(1+s x_u)}{d_v+s\sum_iw_{vi}x_i}
 =p_{vu}\{1+s(x_u-\bar x_v)\}+O(s^2).
\]

Consequently

\[
 f_{\rm dB}(x)=\frac1{nD}\sum_{v,u}
 w_{vu}(x_u-x_v)(x_u-\bar x_v).
\]

For fixed \(v\), the inner sum is exactly

\[
 d_v\bar x_v(1-\bar x_v).
\]

Using the two-sample variance identity gives

\[
 f_{\rm dB}(x)=\frac1{2nD}\sum_v\frac1{d_v}
 \sum_{i,j}w_{vi}w_{vj}(x_i-x_j)^2.
\tag{14}
\]

## 5. Neutral genealogy and proof of (1)--(2)

In a neutral copy event, the lineage at the replaced vertex jumps backward
to the parent.  Two lineages coalesce when such a jump lands on the other
lineage.  For Bd the backward jump \(i\to j\) has one-update probability
\(a^{\rm Bd}_{ij}/n=w_{ij}/(nd_j)\); for dB it has probability
\(a^{\rm dB}_{ij}/n=w_{ij}/(nd_i)\).

For either rule, the exact pair equations are

\[
 (t_i^U+t_j^U)\tau^U_{ij}
 =n+\sum_k a^U_{ik}\tau^U_{kj}
    +\sum_k a^U_{jk}\tau^U_{ik},
 \qquad i\ne j,
\tag{15}
\]

with \(\tau^U_{ii}=0\).  Connectedness makes the solution finite and unique.

Now average over the uniformly selected initial mutant vertex.  Conditional
on two distinct ancestral vertices at time zero, the two sampled types differ
with probability exactly \(2/n\); if the lineages have coalesced, they agree.
Thus

\[
 \sum_{t\ge0}E_{\rm unif}(X_i(t)-X_j(t))^2
 =\frac2n\tau^U_{ij}.
\tag{16}
\]

Substitution of (16) into the occupation formula (12), first with (13) and
then with (14), proves (1) and (2).

## 6. Remeeting identities and proof of (7)

Dividing (15) by \(n\) gives the continuous-time pair meeting equations

\[
 (t_i+t_j)h_{ij}=1+\sum_k a_{ik}h_{kj}+\sum_k a_{jk}h_{ik}.
\tag{17}
\]

The rates in (3) are reversible with respect to (4):
\(\pi_i a_{ij}=\pi_j a_{ji}\).  Multiplying (17) by
\(\pi_i\pi_j\), summing over \(i\ne j\), and cancelling the stationary
off-diagonal terms yields the exact remeeting identity

\[
 \boxed{2\sum_i\pi_i^2t_iR_i=1.}
\tag{18}
\]

For completeness, the uncancelled diagonal contribution is

\[
 1-\sum_i\pi_i^2
 =2\sum_i\pi_i^2\sum_j a_{ij}h_{ij},
\]

which is equivalent to (18) by (5).

For Bd, reversibility and (5) give

\[
 \sum_i\pi_i t_iR_i
 =\frac12+\sum_{i,j}\pi_i a_{ij}h_{ij}
 =\frac12+2C\sum_{\{i,j\}}\frac{w_{ij}}{d_id_j}h_{ij}.
\]

Comparing with (1) gives \(c_{\rm Bd}=(N_{\rm Bd}-1)/(2n)\).

For dB, \(t_i=1\).  Define

\[
 B=\sum_i\pi_i\sum_{j,k}p_{ij}p_{ik}h_{jk}.
\]

Multiplying the pair recurrence
\(2h_{ij}=1+\sum_kp_{ik}h_{kj}+\sum_kp_{jk}h_{ik}\) by
\(\pi_i p_{ij}\), summing, and using reversibility on the last term gives

\[
 \sum_i\pi_i\sum_jp_{ij}h_{ij}=\frac12+B.
\]

Therefore \(N_{\rm dB}=2+2B\), while (2) says
\(c_{\rm dB}=B/n\).  This proves the second formula in (7).

## 7. Complete graph and regular-graph check

For Bd on \(K_n\), the down/up ratio in every nonabsorbing mutant-count
state is \(1/r\), so direct solution of the one-dimensional chain gives

\[
 \rho_{\rm Bd}(K_n,r)=\frac{1-r^{-1}}{1-r^{-n}}
 =\frac1n+\frac{n-1}{2n}(r-1)+O((r-1)^2).
\]

For dB at neutrality, the probabilities of an up-step and a down-step from
mutant count \(k\) are both

\[
 q_k=\frac{k(n-k)}{n(n-1)}.
\]

The first-order drift of \(k/n\) is

\[
 \frac{k(n-k)(n-2)}{n^2(n-1)^2}.
\]

If \(g_k\) is the derivative of fixation probability, then

\[
 q_k(g_{k+1}-2g_k+g_{k-1})
 =-\frac{k(n-k)(n-2)}{n^2(n-1)^2},
\]

with \(g_0=g_n=0\).  Hence

\[
 g_k=\frac{(n-2)k(n-k)}{2n(n-1)},
\]

and \(g_1=(n-2)/(2n)\), proving (8).

There is also a useful broad-class consequence.  If all weighted degrees
are equal, then the two ancestral rate matrices in (3) coincide, have
\(t_i=1\), and have uniform stationary distribution.  Equation (18) then
forces \(N_{\rm Bd}=N_{\rm dB}=n\).  Thus every connected weighted-regular
graph ties the complete graph to first order under both rules; no such graph
is a strict weak simultaneous amplifier.

## 8. Exact small checks

### Unit-weight three-vertex path

For the path \(0-1-2\), exact solution of (15) gives

\[
(\tau^{\rm Bd}_{01},\tau^{\rm Bd}_{02},\tau^{\rm Bd}_{12})=(4,7,4),
\]

and

\[
(\tau^{\rm dB}_{01},\tau^{\rm dB}_{02},\tau^{\rm dB}_{12})
=\left(\frac52,4,\frac52\right).
\]

Equations (1)--(2) give

\[
c_{\rm Bd}=\frac{16}{45}=\frac13+\frac1{45},\qquad
c_{\rm dB}=\frac19=\frac16-\frac1{18}.
\]

Thus this graph weakly amplifies Bd but suppresses dB.

### A rational dB weak amplifier

Take the five-vertex path with consecutive edge weights

\[
 5,\ 1,\ 1,\ 5.
\]

Its degree vector is \((5,6,2,6,5)\).  Exact pair-chain solution and
substitution into (1)--(2) gives

\[
c_{\rm dB}=\frac{1397}{4655}
=\frac3{10}+\frac1{9310},
\]

while

\[
c_{\rm Bd}=\frac{185012}{537055}
=\frac25-\frac{5962}{107411}.
\]

Equivalently,

\[
N_{\rm dB}=\frac{4656}{931}=5+\frac1{931},\qquad
N_{\rm Bd}=\frac{477435}{107411}<5.
\]

This exact example rules out the tempting but false claim that every
undirected weighted graph is a dB suppressor at weak selection.

For independent checking, the dB global-update pair times, listed up to
reflection, are

\[
\begin{array}{c|c}
01,34&10225/1862\\
02,24&33420/931\\
03,14&117265/1862\\
04&60960/931\\
12,23&60625/1862\\
13&2960/49
\end{array}
\]

and the Bd times are

\[
\begin{array}{c|c}
01,34&40743/5806\\
02,24&66037/2903\\
03,14&191965/5806\\
04&209383/5806\\
12,23&51763/2903\\
13&86081/2903.
\end{array}
\]

## 9. Exact verifier recipe

For rational weights, (15) is an independent rational verifier requiring
only a linear solve of order \(\binom n2\):

1. Enumerate unordered distinct pairs \(\{i,j\}\).
2. For each neutral oriented copy event parent \(u\), target \(v\), use
   probability \(w_{uv}/(nd_u)\) for Bd and \(w_{uv}/(nd_v)\) for dB.
3. Backward-map any lineage at \(v\) to \(u\).  Omit a transition if the two
   images coincide; that is absorption of the pair chain.
4. Form \((I-Q)\tau={\bf1}\) on the distinct-pair states and solve exactly.
5. Substitute the solution in (1) and (2), and separately check (18).

This verifies every neutral transition and both derivative formulas without
constructing the full \(2^n\)-state evolutionary chain.

## 10. Scope of the weak-selection obstruction

The rigorous universal conclusion obtained here is the weighted-regular
obstruction above, together with the exact simultaneous sign criterion (9).
I did not obtain a proof of a cross-rule inequality such as
\(N_{\rm Bd}+N_{\rm dB}\le 2n\); such an inequality must not be assumed from
small examples.  The five-vertex path above also shows why an obstruction
based only on a universal dB weak-suppression claim cannot work.
