# Rank-refined posterior collision reduction at fitness two

Date: 2026-08-08 (America/Los_Angeles)

## Status

This note derives a **PROVED exact two-replica reduction** which retains the
finite complete-graph baseline. It also gives an **EXACT COUNTEREXAMPLE** to
the first natural rank weighting.

The surviving collision-reflection sign is

\[
 \boxed{
 E_\Pi\!\left[\sum_{v\notin B}
 \left(e_v(B)-{|B|\over n-|B|}\right)^2\right]
 \le n\{m_K-E_\Pi|B|\},}                         \tag{1}
\]

where

\[
 m_K={ (n-1)2^{n-2}\over2^{n-1}-1}.              \tag{2}
\]

Inequality (1) is **OPEN**. Unlike \(I_2\le2\), it would imply the exact
finite complete-baseline inequality, not merely half density. The exact
screen and extensive numerical search found no counterexample, but that is
not a proof.

## 1. Stationary posterior and collision excess

Let \(\Pi\) be the stationary law of the fair-geometric union dual. For a
fixed target \(v\), let

\[
 \nu_v(B)=\hbox{effective incoming mass at }(v,B),
 \qquad e_v(B)={\nu_v(B)\over\Pi(B)}\quad(v\notin B).
\]

For \(k=|B|\) and \(h=n-k\), the previously verified stationarity identity is

\[
 \sum_{v\notin B}e_v(B)=k.                       \tag{3}
\]

Define the conditional collision excess

\[
 \begin{split}
 J(B)&=\sum_{v\notin B}e_v(B)^2-{k^2\over h}\\
 &=\sum_{v\notin B}\left(e_v(B)-{k\over h}\right)^2
 \ge0.                                           \tag{4}
 \end{split}
\]

The equality in (4) uses (3). Thus \(J(B)\) is exactly the excess over the
sharp Cauchy lower envelope, not a relaxation.

There is also a literal two-replica interpretation. Conditional on an
effective update and output \(B\), the target posterior is

\[
 s_v(B)={e_v(B)\over k},\qquad v\notin B.
\]

For two conditionally independent posterior targets \(V_1,V_2\),

\[
 \Pr(V_1=V_2\mid B,\hbox{both effective})-{1\over h}
 ={J(B)\over k^2}.                                \tag{5}
\]

## 2. The first finite-baseline rank weight is false

The most direct use of the lower envelope is

\[
 E_\Pi\left[{h\over k}\sum_{v\notin B}e_v(B)^2\right]
 \stackrel{?}{\le}m_K.                            \tag{6}
\]

Indeed, the integrand in (6) is at least \(k\), with equality at a uniform
posterior. Therefore (6) would give the desired finite mean bound. But it is
false.

On the unweighted three-path,

\[
 E|B|={11\over9},\qquad
 E\left[{h\over k}\sum e_v^2\right]={14\over9}
 ={4\over3}+{2\over9}>m_K.                       \tag{7}
\]

The failure is not caused by irregular weighted degree. On the regular
weighted \(K_4\) with edge matrix

\[
 \begin{pmatrix}
 0&1&1&2\\1&0&2&1\\1&2&0&1\\2&1&1&0
 \end{pmatrix},
\]

exact arithmetic gives

\[
 E\left[{h\over k}\sum e_v^2\right]
 ={2514\over1435}
 ={12\over7}+{54\over1435}>m_K.                  \tag{8}
\]

Thus the rank choice \(a_k=h/k,b_k=0\) is **EXACTLY FALSIFIED**.

## 3. Finite-baseline collision reflection

The surviving weights are

\[
 \boxed{
 a_k={1\over n},\qquad
 b_k=k-{k^2\over n(n-k)}.}                       \tag{9}
\]

They give the exact identity

\[
 a_k\sum_{v\notin B}e_v(B)^2+b_k
 =k+{J(B)\over n}.                               \tag{10}
\]

The proposed upper bound is therefore

\[
 \boxed{
 E_\Pi\left[
 {1\over n}\sum_{v\notin B}e_v(B)^2
 +|B|-{|B|^2\over n(n-|B|)}
 \right]\le m_K.}                                \tag{11}
\]

By (4), the sharp lower envelope of the integrand is exactly \(|B|\).
Consequently (11) implies

\[
 E_\Pi|B|\le m_K,
 \qquad
 \rho_{\rm dB}(G,2)\le\rho_{\rm dB}(K_n,2).       \tag{12}
\]

Equations (1) and (11) are identical. This is stronger than (12), because
it requires the mean deficit to pay for all posterior nonuniformity. It is
not being claimed equivalent to the desired fixation inequality.

For the complete graph, label symmetry and (3) give

\[
 e_v(B)={k\over h}\quad(v\notin B),\qquad J(B)=0,
\]

and the complete stationary mean is (2). Hence equality holds in (1) and
(11), including the finite conditioning correction.

## 4. Exact Cayley two-replica form

Let \(\sigma_v\) be the deleted occupied-source measure and put

\[
 \lambda_v={\sigma_v+\nu_v\over2}.
\]

The fair-geometric midpoint resolvent is the exact identity

\[
 \nu_v=\lambda_vA_v,                              \tag{13}
\]

where \(A_v\) adjoins one sample from row \(P_v\). Therefore the raw posterior
collision energy has the exact two-replica expansion

\[
 \begin{split}
 \mathcal E_2
 &:=
 \sum_v\sum_{B:v\notin B}{\nu_v(B)^2\over\Pi(B)}\\
 &=\sum_v\sum_B{1\over\Pi(B)}
 \left\{\sum_{C,i}\lambda_v(C)P_{vi}
 1_{\{B=C\cup\{i\}\}}\right\}^2\\
 &=\sum_v\sum_{C,D,i,j}
 {\lambda_v(C)\lambda_v(D)P_{vi}P_{vj}
 1_{\{C\cup\{i\}=D\cup\{j\}\}}\over
 \Pi(C\cup\{i\})}.                               \tag{14}
 \end{split}
\]

Only terms with positive denominator occur. Since

\[
 E_\Pi J(B)=\mathcal E_2-E_\Pi{|B|^2\over n-|B|},
\]

the sole remaining Cayley sign is

\[
 \boxed{
 \mathcal E_2-E_\Pi{|B|^2\over n-|B|}
 \le n\{m_K-E_\Pi|B|\}.}                         \tag{15}
\]

Formula (14) is the requested stationary two-replica object. Any proof of
(15) must compare coincident Cayley outputs with the rank correction on the
right. The fixed-reference \(L^2\) contraction and the revealed-flag bound
already have exact counterexamples and are not used here.

## 5. Exact and numerical screening

The exact witness values of the slack

\[
 \mathfrak R_n=n(m_K-E|B|)-EJ(B)                 \tag{16}
\]

are

\[
\begin{array}{c|c}
\text{graph}&\mathfrak R_n\\ \hline
\text{unweighted }P_3&1/6\\
\text{weighted }P_3\ (1,2)&1/5\\
\text{regular weighted }K_4&8/615.
\end{array}                                      \tag{17}
\]

The exact six-vertex split witness also has positive slack, approximately
\(3.13798934979\).

The deterministic exact screen covers:

* all 54 connected three-vertex graphs with weights in \(\{0,1,2,5\}\);
* all 624 connected four-vertex graphs with weights in \(\{0,1,2\}\);
* 48 seeded sparse/extreme five-vertex integer graphs;
* the frozen six-vertex split witness.

Every graph in this finite corpus satisfies (1). By contrast, the false
bound (6) fails on 51/54, 622/624, and 48/48 graphs in the first three
groups, respectively.

Floating search additionally tested full-support, sparse, and directed row
kernels through seven vertices and optimized the normalized ratio

\[
 {n(m_K-E|B|)\over EJ(B)}.
\]

No value below one was observed; the smallest optimized value was about
\(1.43016\). These searches are **NUMERICAL EVIDENCE ONLY**.

## 6. Verification and exact status

Run:

~~~text
PYTHONDONTWRITEBYTECODE=1 python3 -B verify_posterior_rank_collision.py
~~~

The verifier reconstructs the labelled one-target chains, stationary law,
effective measures, posterior variables, and Cayley identity over exact
rationals. It checks (3)--(4), (10), and (13)--(17), certifies the
counterexamples (7)--(8), and replays the exact corpus.

Classification:

* **PROVED:** posterior collision identities, Cayley two-replica expansion,
  complete equality, and (1) implies the exact finite-baseline theorem.
* **EXACTLY FALSIFIED:** the naive rank weighting (6).
* **EXACTLY COMPUTED:** positive slack on the stated finite corpus.
* **NUMERICALLY OBSERVED:** no violation in broader searches through seven
  vertices.
* **OPEN:** the universal collision-reflection inequality (1)/(15).
