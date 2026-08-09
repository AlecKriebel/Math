# Marked requests and the failure of hypergeometric cache order

Date: 2026-08-08 (America/Los_Angeles)

## Status and scope

This note gives two exact probabilistic forms of the open standard-sector
fitness-two sign.  They are derived from the labelled active chain.

The following statements are **PROVED**.

1. A cumulative standard-sector atom is exactly a request-count/cache-cut
   covariance in the complete pin environment.
2. Choosing one request time uniformly turns the centered pin counts into a
   single marked-request occupation law.
3. The probability-generating-function difference has a canonical
   degree-`N-2` Bernstein quotient.  Every one of its Bernstein
   coefficients is a positive constant times a hypergeometric empty-cache
   probability difference.
4. Rank-CDF ordering, a tempting stronger statement, is **EXACTLY
   REFUTED** on four vertices.  The hypergeometric transform remains
   positive on that witness.
5. The all-order hypergeometric marked-cache inequality is itself
   **EXACTLY REFUTED** on eight vertices.  In particular, the PGF Schur
   order is false.  The inverse-rank comparison remains positive on the
   same witness, so the true standard-sector sign is not refuted.

The marked-cache Bernstein coefficients are positive on the earlier finite
corpus stated in Section 7, but that finite pattern does not extend to all
orders.  The exact counterexample in Section 7 closes this proposed route.

## 1. Complete pins and a marked request

Put `n=N+1`.  For each vertex `x`, let `Q_x` be the pin replacement kernel

\[
 Q_x(x,y)=\frac1N\quad(y\ne x),\qquad
 Q_x(y,x)=1\quad(y\ne x),                         \tag{1}
\]

and write `L_x=K(Q_x)` for its active operator.  Their uniform mixture is
the complete active kernel

\[
 K_0=\frac1n\sum_xL_x.                            \tag{2}
\]

The active states are `(B,v)`, where `B` is nonempty, `v` is not in `B`,
and the active rank is `K=|B|`.  The complete stationary row is

\[
 \nu_0(B,v)=\frac{|B|}{nN2^{N-1}}.                \tag{3}
\]

Draw iid uniform pins `X_1,...,X_t`, start the active state from `nu_0`, and
apply `L_(X_1),...,L_(X_t)`.  Let

\[
 C_t(u)=\sum_{s=1}^t1_{\{X_s=u\}},\qquad
 d_t(u)=C_t(u)-\frac tn.                           \tag{4}
\]

For `1<=k<=N`, define the two centered occupation moments

\[
\begin{aligned}
 X_t(k)&=E\left[d_t(v_t)1_{\{K_t=k\}}\right],\\
 I_t(k)&=E\left[\sum_{u\in B_t}d_t(u)1_{\{K_t=k\}}\right].     \tag{5}
\end{aligned}
\]

Now choose `J` uniformly from `{1,...,t}`, independently conditional on the
history, and mark the past request `Z=X_J`.  Double counting the occurrences
in `(4)` gives

\[
\boxed{
\begin{aligned}
 X_t(k)&=t\left\{P(Z=v_t,K_t=k)-\frac1nP(K_t=k)\right\},\\
 I_t(k)&=t\left\{P(Z\in B_t,K_t=k)-\frac{k}{n}P(K_t=k)\right\}.
                                                               \tag{6}
\end{aligned}}
\]

Thus `X_t` and `I_t` compare a uniformly marked past request with an
independent uniform vertex.  No branching approximation is involved.

## 2. Exact derivative law

Fix a vertex `x`.  Give pin `x` probability `p` and each other pin
probability `(1-p)/N`; put `p_0=1/n`.  If `mu_t(p)` is the terminal active
law, differentiating the finite pin-history probability gives the exact
score

\[
 \left.\frac d{dp}\log P_p(X_1,...,X_t)\right|_{p=p_0}
 =\frac{n^2}{N}\left(C_t(x)-\frac tn\right).       \tag{7}
\]

Let `A_k` denote `v=x`, `I_k^x` denote `x\in B`, and `O_k` denote neither.
Label exchangeability and `(5)` therefore give

\[
\boxed{
 \mu_t'(A_k)=\frac nN X_t(k),\qquad
 \mu_t'(I_k^x)=\frac nN I_t(k).}                  \tag{8}
\]

The rank marginal does not depend on `p` at `p_0`.  Hence

\[
 \mu_t'(O_k)=-\frac nN\{X_t(k)+I_t(k)\}\quad(k<N),
 \qquad I_t(N)=-X_t(N).                           \tag{9}
\]

Equations `(7)--(9)` are the exact probability law behind the standard
two-feature recurrence.

## 3. The cumulative atom is a cache cut

Let `s_x=N`, `s_y=-1` for `y\ne x`, and let `\Delta` be the active
perturbation associated with the canonical standard embedding `E(s)`.  The
pin scale is

\[
 \Delta=\frac{N^2}{n(N-1)}(A-B),                 \tag{10}
\]

where `A=L_x` and `B=N^{-1}\sum_{y\ne x}L_y`.  Let
`h_j(k)=1_{\{k<=j\}}`.  The standard force of this atom is

\[
 a_j=\frac{j}{2n(N-1)},\qquad
 b_j=\frac{N}{2n(N-1)},\qquad
 b_{j+1}=\frac{j}{2(j+1)(N-1)},                  \tag{11}
\]

with every other feature coefficient zero.

Define the cumulative prefix atom

\[
 R_{L,j}=\frac1{nN}\sum_{q=0}^L
          \nu_0\Delta K_0^q\Delta h_j.           \tag{12}
\]

Since `nu_0 K_0=nu_0`, differentiating `mu_t(p)` with `t=L+1`, using
`(8)--(11)`, gives

\[
\boxed{
 R_{L,j}=\frac{jX_t(j)+NI_t(j)+\frac{jn}{j+1}I_t(j+1)}
                 {2n(N-1)^2}.}                  \tag{13}
\]

This also treats the physical upper boundary correctly through
`I_t(N)=-X_t(N)`.

The first two terms in the numerator are literally an ordered cut.  Put
`O_t=V\setminus(B_t\cup\{v_t\})`.  Since `\sum_u d_t(u)=0`,

\[
\boxed{
 NI_t(j)+jX_t(j)
 =E\left[\sum_{u\in B_t}\sum_{z\in O_t}
       \{d_t(u)-d_t(z)\}1_{\{K_t=j\}}\right].}    \tag{14}
\]

Likewise,

\[
 nI_t(j+1)=E\left[\sum_{u\in B_t}\sum_{z\notin B_t}
       \{d_t(u)-d_t(z)\}1_{\{K_t=j+1\}}\right].  \tag{15}
\]

Thus `(13)` asks for cache-versus-complement alignment of empirical request
counts, with the adjacent-rank term required by a physical down-crossing.

## 4. The exact PGF quotient

Let `c` be a pin-count vector, and let `p_c(k)` be the terminal rank law
after averaging uniformly over all pin words with multiplicities `c`.
Suppose `c_x>=c_y`, and compare

\[
 p^+(k)=p_{c+e_x}(k),\qquad p^-(k)=p_{c+e_y}(k).   \tag{16}
\]

Put `delta p_k=p^+(k)-p^-(k)` and

\[
 D(z)=\sum_{k=1}^N\delta p_kz^{k-1}.              \tag{17}
\]

Normalization gives `D(1)=0`.  If

\[
 C_r=\sum_{k=1}^r\delta p_k,                      \tag{18}
\]

then direct telescoping gives

\[
 \boxed{D(z)=(1-z)Q(z),\qquad
 Q(z)=\sum_{r=1}^{N-1}C_rz^{r-1}.                \tag{19}
\]

Rank-CDF domination would assert every `C_r>=0`.  Section 6 gives an exact
counterexample.  The PGF statement only asks `Q(z)>=0` on `0<=z<=1`.

## 5. Hypergeometric Bernstein coefficients

Expand `Q` in the Bernstein basis of its natural degree `d=N-2`:

\[
 Q(z)=\sum_{m=0}^{N-2}\binom{N-2}{m}b_m
             z^m(1-z)^{N-2-m}.                   \tag{20}
\]

Power-to-Bernstein conversion and `(19)` give

\[
 b_m=\sum_{r=1}^{m+1}
       \frac{\binom m{r-1}}{\binom{N-2}{r-1}}C_r.              \tag{21}
\]

The coefficient of `delta p_k` in `(21)` is

\[
 \sum_{r=k}^{m+1}\frac{\binom m{r-1}}
                          {\binom{N-2}{r-1}}
 =\frac{\binom{N-k}{m-k+1}}{\binom{N-2}{m}},                  \tag{22}
\]

where the value is zero when `k>m+1`.  Put `q=N-1-m`.  Since

\[
 \frac{\binom{N-k}{m-k+1}}{\binom{N-2}{m}}
 =\frac{N-1}{q}\frac{\binom{N-k}{q}}{\binom{N-1}{q}},         \tag{23}
\]

we obtain the exact hypergeometric identity

\[
\boxed{
 b_m=\frac{N-1}{q}\left{E_+\psi_q(K)-E_-\psi_q(K)\right},
 \qquad
 \psi_q(k)=\frac{\binom{N-k}{q}}{\binom{N-1}{q}}.}            \tag{24}
\]

The reward `psi_q` has a literal marked-cache interpretation.  Given
`(B,v)` with `|B|=k`, choose an anchor `a` uniformly from `B`, then choose a
uniform `q`-subset `U` of `V\setminus\{v,a\}`.  This universe has `N-1`
vertices and `B\setminus\{a\}` has `k-1` vertices, so

\[
 \psi_q(k)=P\{U\cap(B\setminus\{a\})=\varnothing\mid B,v\}.   \tag{25}
\]

Therefore every `b_m>=0` is precisely an empty marked-cache comparison,
not a rank-tail comparison.  Coefficient positivity in `(20)` proves the
PGF order on the whole interval and, after integrating the Hausdorff
identity

\[
 \frac1k=\int_0^1z^{k-1}\,dz,                   \tag{26}
\]

proves the inverse-rank comparison needed by the standard sector.

## 6. Exact failure of rank-CDF order

Take `n=4` and base pin counts

\[
 c=(0,0,1,2).                                     \tag{27}
\]

Compare adding the next pin to the fourth coordinate (the already more
frequent label) with adding it to the third.  Exact word symmetrization and
the labelled active chain give

\[
 C_1=\frac{13}{2592}>0,\qquad
 C_2=-\frac{227}{46656}<0.                        \tag{28}
\]

Thus rank-CDF Schur ordering is false.  Nevertheless

\[
 Q(z)=\frac{13}{2592}-\frac{227}{46656}z,         \tag{29}
\]

and both endpoint values are positive:

\[
 Q(0)=\frac{13}{2592},\qquad Q(1)=\frac7{46656}. \tag{30}
\]

The marking average in `(24)--(25)` is therefore essential.

## 7. Exact refutation of all-order marked-cache order

The finite corpus

\[
 n=3, t\le25;\qquad n=4, t\le12;\qquad n=5, t\le8             \tag{31}
\]

has all `89,433` marked-cache Bernstein comparisons nonnegative.  That
pattern is not universal.

Take `n=8`, so `N=7`, and use only two pin labels `x,y`.  At total word
length `26`, compare the uniformly shuffled pin multisets

\[
 (C_x,C_y)=(14,12)\qquad\hbox{and}\qquad(13,13).                \tag{32}
\]

The first multiset is obtained from the base counts `(13,12)` by adding a
request to the already more frequent label.  For `q=1`, the empty-cache
reward in `(24)` is

\[
 \psi_1(k)={N-k\over N-1}.
\]

The exact labelled-chain calculation gives

\[
\begin{aligned}
 &E_{(14,12)}\psi_1(K)-E_{(13,13)}\psi_1(K)\\
 &\quad=
 -{5097841855133683116602026973677867709383649499615439175346534343452763341123776494668866115269
 \over
 2209253741490523003907776625044372951761360171795984893713024521622498836480000000000000000000000000}
 <0.                                                               \tag{33}
\end{aligned}
\]

Its decimal value is approximately `-2.30749495153e-6`.  By `(24)`, the
last natural Bernstein control is `(N-1)` times `(33)`, and is therefore
strictly negative.  Thus the PGF quotient is negative in a neighborhood of
`z=1`; neither the Bernstein order nor the weaker pointwise PGF Schur order
holds universally.

For orientation, the six CDF differences on this witness have decimal
values

\[
 (4.5297983\,10^{-4},-2.7315554\,10^{-6},-2.4420987\,10^{-4},
 -1.6294688\,10^{-4},-5.0271620\,10^{-5},-6.6648680\,10^{-6}), \tag{34}
\]

and the six natural Bernstein controls are

\[
 (4.5297983\,10^{-4},4.5243351\,10^{-4},4.2746622\,10^{-4},
 3.6178324\,10^{-4},2.2903558\,10^{-4},-1.3844970\,10^{-5}). \tag{35}
\]

The stronger route fails without falsifying the desired inverse-rank sign.
On the same two multisets, exact arithmetic gives

\[
 E_{(14,12)}{1\over K}-E_{(13,13)}{1\over K}
 ={25801268944756526477036175355372435803145464088958168680881355283347745154642235159793307444839
 \over
 131839524215120724870881810531207252023269575469496114714332239142007603200000000000000000000000000}
 >0,                                                               \tag{36}
\]

approximately `1.95702078708e-4`.  Therefore `(33)` is a refutation of the
marked-cache/PGF strengthening only.  The true inverse-rank standard-sector
comparison remains **OPEN**.

The independent verifier reconstructs the pin active chains and checks:

* `(6)--(13)` against labelled pin histories and the separate standard
  two-feature recurrence;
* `(19)--(25)` by exact binomial algebra;
* the CDF counterexample `(27)--(30)`;
* all `89,433` positive marked-cache comparisons in `(31)`;
* the exact negative comparison `(33)` from the full `1,016`-state labelled
  active chain;
* the positive inverse-rank comparison `(36)` on the same witness.

The eight-vertex computation is also rebuilt through an independent
two-label orbit quotient and checked against the labelled chain.  No
numerical sign is used in the refutation.
