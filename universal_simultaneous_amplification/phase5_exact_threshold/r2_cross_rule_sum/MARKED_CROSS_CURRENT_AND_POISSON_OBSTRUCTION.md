# The common marked cross-rule current at fitness two

Date: 2026-08-13 (America/Los_Angeles)

## Status

This note records two **PROVED exact reductions** of the decisive product
target

\[
                         m_Lm_D\le b_nd_n.                    \tag{1}
\]

The first places the two update rules on one marked probability space.  The
second turns the surviving two-step floor into one two-`L`-replica Poisson
current.  The most direct pointwise sign for that current is then
**EXACTLY FALSE** on the weighted three-path.  The stationary two-step floor
and `(1)` remain open.

No literature search or external communication was used.

## 1. One marked space for both rules

Let

\[
 \mathcal X=\{(C,v):v\notin C\}.
\]

The fair one-sample dB kernel `M_P` samples `i` from row `P_v`, puts
`B=C union {i}`, and then, with equal probabilities, either continues at
`(B,v)` or chooses `w` uniformly from `B` and moves to
`(B minus {w},w)`.  Its stationary probability law is denoted by `mu_D`.
For the alternating inverse-rank observable `psi` from the marked lift,

\[
                         \mu_D\psi={1\over m_D}.               \tag{2}
\]

There is a canonical `L` measure on the same space.  If `pi_L` is the
stationary law of the Bd dual, put

\[
 \lambda_L(C,v)=\pi_L(V\setminus C),\qquad
 q_L={\lambda_L\over m_L}.                                  \tag{3}
\]

Every occupied set `A` contributes once for each `v in A`, and therefore

\[
 \lambda_L\mathbf1=m_L,\qquad q_L\mathbf1=1.                 \tag{4}
\]

For the complete replacement kernel, `pi_L` is uniform on the nonempty
sets.  Hence `lambda_L=b_nU`, where `U` is the uniform probability law on
`X`; this is also the complete marked dB stationary law.  Since
`U psi=1/d_n`, `(2)--(4)` give the exact common-space identity

\[
 \boxed{
 {1\over m_D}-{m_L\over b_nd_n}
 =\mu_D\psi-{1\over b_nd_n}\lambda_L\mathbf1.}               \tag{5}
\]

Thus `(1)` is exactly the nonnegativity of one signed marked pairing.  This
is not a comparison of two unrelated rank laws: both measures use the same
marked target and the same row-`P` sample.

The transport of `lambda_L` by that same marked kernel is also explicit.
For an output `(D,w)`, put

\[
 A=V\setminus D,\qquad B=D\cup\{w\},\qquad b=|B|.
\]

Writing `P_v(S)=sum_(i in S) P_vi` and setting `pi_L(empty)=0`, direct
inversion of the continue and stop branches gives

\[
\begin{aligned}
 2(\lambda_LM_P)(D,w)
={}&P_w(D)\pi_L(A)+\sum_{i\in D}P_{wi}\pi_L(A\cup\{i\})\\
 &+{1\over b}\left[
 \pi_L(A\setminus\{w\})
       \sum_{v\in A\setminus\{w\}}P_v(B)
 +\sum_{i\in B}\pi_L((A\setminus\{w\})\cup\{i\})
       \sum_{v\in(A\setminus\{w\})\cup\{i\}}P_{vi}
 \right].                                                   \tag{5a}
\end{aligned}
\]

This is the literal `lambda_L` transport requested by the shared-arrow
program.  It is generally not stationary; its signed pointwise residual has
both signs even on the weighted three-path.

There is a compact exact Green form which keeps that transport and the
radial term together.  Let `Gamma_D` be the group inverse of `I-M_P` and
put

\[
 g=\Gamma_D\psi,qquad
 (I-M_P)g=\psi-(\mu_D\psi)\mathbf1.                          \tag{5b}
\]

Then

\[
\boxed{
 m_L\left({1\over m_D}-{m_L\over b_nd_n}\right)
 =\lambda_L(M_P-I)g
  +\left\{\lambda_L\psi-{m_L^2\over b_nd_n}\right\}.}       \tag{5c}
\]

No sign has been assigned to either term.  The second is the exact radial
two-replica covariance: if

\[
 R_n(a)=a\psi_{n-a},                                         \tag{5d}
\]

then

\[
 \lambda_L\psi-{m_L^2\over b_nd_n}
 =E_{\pi_L\otimes\pi_L}\left[
 {R_n(|A|)+R_n(|A'|)\over2}
 -{|A||A'|\over b_nd_n}\right].                              \tag{5e}
\]

Thus `(5c)` is one marked stationary current plus its radial covariance,
not an orientation/batching sign split.  On the weighted three-path the
radial term is negative and is compensated by the current:

\[
 -{293\over581405}+{739\over5115}
 ={50224\over348843}>0.                                     \tag{5f}
\]

This exact cancellation rules out proving `(5c)` by signing its two
displayed summands separately.

Since every initial law converges in Cesaro mean to the stationary law of
the finite irreducible chain,

\[
 \lim_{T\to\infty}{1\over T}\sum_{t<T}q_LM_P^t\psi
 ={1\over m_D}.                                               \tag{6}
\]

Consequently the all-time floor

\[
 q_LM_P^t\psi\ge {m_L\over b_nd_n}\qquad(t\ge2)              \tag{7}
\]

would prove `(1)`.  Only the exact reduction is proved here; `(7)` remains
open.

## 2. Exact two-step forcing

For an occupied `L` state `A`, define

\[
 F_P(A)=\sum_{v\in A}(M_P^2\psi)(V\setminus A,v).             \tag{8}
\]

The definition of `q_L` immediately gives

\[
 \boxed{E_{\pi_L}F_P=m_Lq_LM_P^2\psi.}                       \tag{9}
\]

The time-two instance of `(7)` is therefore exactly

\[
 \boxed{E_{\pi_L}F_P\ge {m_L^2\over b_nd_n}.}                \tag{10}
\]

Equivalently, for independent `A,B` with law `pi_L`, set

\[
 G_P(A,B)={F_P(A)+F_P(B)\over2}
              -{|A||B|\over b_nd_n}.                         \tag{11}
\]

Then `(10)` is `E G_P>=0`.  This is the first literal two-replica forcing
which retains the common marked collision rather than replacing it by a
rank envelope.

The first marked step has the useful exact collapse

\[
 (M_P\psi)(C,v)=
 \begin{cases}
 1,&|C|=0,\\
 \displaystyle {1\over k+1}+{P_v(C)\over k(k+1)},&k=|C|\ge1.
 \end{cases}                                                 \tag{12}
\]

Thus `F_P` is a finite two-arrow observable.  The adjacent cross-rule note
gives its fully expanded local formula and checks the small-cache boundary
states directly.

## 3. Canonical complete product Poisson current

Let `Q_P^x=Q_L(P) tensor I + I tensor Q_L(P)` be the generator of two
independent `L` copies.  For the complete replacement kernel `K`, the mean
of `G_K` under the uniform product law is zero.  Let `Phi` be the canonical
complete Green potential, with an arbitrary additive gauge, solving

\[
                         -Q_K^x\Phi=G_K.                       \tag{13}
\]

Stationarity of `pi_L tensor pi_L` gives the exact identity

\[
 \boxed{
 E_{\pi_L\otimes\pi_L}G_P
 =E_{\pi_L\otimes\pi_L}\mathcal R_P,}                       \tag{14}
\]

where

\[
 \begin{aligned}
 \mathcal R_P(A,B)
 &=G_P(A,B)+(Q_P^x\Phi)(A,B)\\
 &={ (F_P-F_K)(A)+(F_P-F_K)(B)\over2}
   +\{(Q_P^x-Q_K^x)\Phi\}(A,B).                              \tag{15}
 \end{aligned}
\]

Formula `(15)` is the precise marked forcing plus shared-`L` transport
current.  It is the natural place to use the fitness-two adjoint
`Q_L^T=Q_C+V`: the first term contains the same two row arrows as the
marked collision, while the second transports the complete Green potential
through the reversed-arrow generator.

## 4. Exact failure of pointwise Poisson closure

The tempting strengthening

\[
                         \mathcal R_P(A,B)\ge0
                    \quad\hbox{for every }A,B                 \tag{16}
\]

is false.  Take the three-vertex weighted path

\[
 w_{01}=1,\qquad w_{02}=2,\qquad w_{12}=0.                    \tag{17}
\]

Here `b_3d_3=16/7`.  With the gauge `Phi(V,V)=0`, the complete potential is
radial and has the table

\[
\begin{array}{c|ccc}
 \Phi(a,b)&b=1&b=2&b=3\\ \hline
 a=1&17/24&59/96&19/32\\
 a=2&59/96&17/48&7/32\\
 a=3&19/32&7/32&0.
\end{array}                                                   \tag{18}
\]

At the ordered root pair

\[
                         A=\{0\},\qquad B=\{0,2\},            \tag{19}
\]

the two terms in `(15)` are respectively

\[
 -{25\over144},\qquad -{19\over96},                           \tag{20}
\]

and hence

\[
 \boxed{\mathcal R_P(\{0\},\{0,2\})=-{107\over288}<0.}      \tag{21}
\]

In fact `14` of the `49` ordered state pairs have negative residual.  This
is not a counterexample to `(10)`: exact integration gives

\[
 E_{\pi_L}F_P-{m_L^2\over b_3d_3}
 ={18560\over116281}>0,                                      \tag{22}
\]

or, after multiplying by `b_3d_3`,

\[
 b_3d_3E_{\pi_L}F_P-m_L^2={296960\over813967}>0.             \tag{23}
\]

Thus the canonical complete radial Green potential is correct after
stationary integration but cannot be closed statewise.  Any proof using
`(14)` must retain an additional overlap/full-pair correction with zero
stationary generator mean, or group the signed currents globally into
cycle/tree packets.  This is the sharp minimal obstruction furnished by
the direct two-replica route; it does not motivate another scalar lower
envelope.

The first bare overlap correction is also ruled out exactly.  Put

\[
                         H(A,B)=|A\cap B|.                     \tag{24}
\]

At `(A,B)=({0},V)` on the same weighted path,

\[
 (Q_P^\times H)({0},V)=0,
 \qquad \mathcal R_P({0},V)=-{11\over36}.                    \tag{25}
\]

Therefore no scalar multiple of `Q_P^x H` can repair the pointwise
residual, even if the scalar is allowed to depend arbitrarily on the graph
and vanish at the complete kernel.  A viable overlap correction must retain
labelled row/current information; the unweighted intersection count is too
coarse.

In fact the natural labelled bilinear enlargement is still insufficient.
For a symmetric matrix `Z` and a vertex vector `ell`, put

\[
 H_{Z,\ell}(A,B)
 =\sum_i Z_{ii}1_{i\in A}1_{i\in B}
 +\sum_{i<j}Z_{ij}
   \{1_{i\in A}1_{j\in B}+1_{j\in A}1_{i\in B}\}
 +\sum_i\ell_i\{1_{i\in A}+1_{i\in B}\}.                    \tag{26}
\]

This contains every symmetric labelled bilinear overlap and every one-copy
linear vertex correction.  On the weighted path `(17)`, define a probability
measure `eta` on ordered state pairs by

\[
\begin{array}{c|cccccccccc}
(A,B)&(001,011)&(001,100)&(001,110)&(001,111)&(011,011)&
(011,110)&(011,111)&(110,110)&(110,111)&(111,111)\\ \hline
\eta&13/250&1/25&337/2850&497/7125&21/2000&229/2375&
961/19000&151/600&373/1500&373/6000.
\end{array}                                                   \tag{27}
\]

The ten weights are positive and sum to one.  Direct exact evaluation gives

\[
 \boxed{E_\eta[Q_P^\times H_{Z,\ell}]=0
        \quad\hbox{for every }Z=Z^T,\ell,}                    \tag{28}
\]

whereas

\[
 \boxed{E_\eta\mathcal R_P=-{440101\over16416000}<0.}        \tag{29}
\]

Equations `(28)--(29)` are an exact Farkas certificate: for every choice of
`Z,ell`, at least one state pair has

\[
 \mathcal R_P+Q_P^\times H_{Z,\ell}<0.                       \tag{30}
\]

Thus even degree-labelled or full vertex-pair bilinear corrections cannot
turn the canonical product Poisson identity into a pointwise supersolution.
The remaining full-pair route must use higher-order set dependence or prove
the stationary current sign without pointwise closure.

## 5. Exact audit

`verify_marked_cross_current.py` constructs `L`, `M_P`, `F_P`, the complete
product Poisson solution, and every residual over `QQ`.  It verifies
`(3)--(15)`, the table `(18)`, the minimum `(21)`, the count of negative
ordered pairs, the bare-overlap obstruction `(25)`, the labelled-bilinear
Farkas certificate `(27)--(29)`, and the positive integrated value `(22)`.

The proof obligation left by this note is therefore precise:

1. prove the stationary current sign in `(14)` by a full-pair/cycle
   grouping, possibly after an exact zero-mean overlap correction; or
2. prove the later-time floor `(7)` directly and pass to the Cesaro limit.
