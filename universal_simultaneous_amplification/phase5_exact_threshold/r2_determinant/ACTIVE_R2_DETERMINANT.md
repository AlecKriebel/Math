# The exact fitness-two determinant problem

Date: 2026-08-08 (America/Los_Angeles)

## Status

This note isolates the universal `r=2` question without importing the
strictly stronger stationary-promotion conjecture.

The exact target is the active-tree coefficient

\[
 \boxed{\mathfrak F_0(P)=
 \sum_{y\in\mathcal Y}\tau_y
 \left\{H(y)-{1\over m_K}\right\}\ge0.}             \tag{T}
\]

It is equivalent to complete-graph maximality for dB fixation at fitness
two.  It remains **OPEN** for arbitrary finite connected undirected weighted
graphs.

The previously named promotion coefficient replaces `1/m_K` in `(T)` by a
larger graph-dependent number `c_P`.  It implies `(T)` but is not known to be
equivalent to it.  Treating those two signs as equivalent was an exact
logical overclaim in the phase-4 handoff.

This note also gives a new exact coefficient certificate at order three:
after clearing the positive row-degree denominator, `(T)` is a cyclic sum of
three squared edge differences times a positive polynomial.  The raw
monomial expansion has negative coefficients, so a certificate cannot be
coefficientwise in the unrecentered edge-weight monomial basis even on a
triangle.

## 1. Probability space and dual law

Let `G=(V,w)` have order `n>=3`, with

\[
 w_{uv}=w_{vu}\ge0,\qquad w_{vv}=0,\qquad
 d_v=\sum_u w_{vu}>0,
\]

and connected positive support.  Put

\[
 P_{vu}={w_{vu}\over d_v},\qquad N=n-1.
\]

Then `P` is loopless, irreducible, row stochastic, and reversible:

\[
 d_vP_{vu}=d_uP_{uv}=w_{uv}.                         \tag{1}
\]

At fitness two, the dB dual replaces an occupied target `v` by the union of
`J>=1` independent samples from row `P_v`, where

\[
 \Pr(J=j)=2^{-j}.                                     \tag{2}
\]

Uniformly choosing the target gives an irreducible chain on the nonempty
proper subsets.  Let `Pi` be its stationary law and

\[
 m=E_\Pi|A|,
 \qquad
 m_K={N2^{N-1}\over2^N-1}.                           \tag{3}
\]

The already proved coverage duality gives

\[
 \rho_{\rm dB}(G,2)={m\over n},\qquad
 \rho_{\rm dB}(K_n,2)={m_K\over n}.                 \tag{4}
\]

Thus the universal finite-baseline question is exactly `m<=m_K`.

## 2. Marked one-sample law and collision

For `v notin C`, let

\[
 \sigma_v(C)=\Pi(C\cup\{v\}),\qquad
 \lambda_v(C)={\sigma_v(C)+\nu_v(C)\over2},          \tag{5}
\]

where `nu_v` is the effective incoming mass at output `(C,v)`.  The proved
posterior and Cayley identities are

\[
 \sum_{v\notin B}\nu_v(B)=|B|\Pi(B),
 \qquad \nu_v=\lambda_vA_v,                           \tag{6}
\]

with `A_v` adjoining one sample from `P_v`.

On

\[
 \mathcal X=\{(C,v):v\notin C\},                     \tag{7}
\]

the marked kernel `M_P` acts as follows.

1. Draw `I~P_v` and set `B=C union {I}`.
2. Toss a fair coin.
3. On continue, move to `(B,v)`.
4. On stop, draw `W` uniformly from `B` and move to
   `(B minus {W},W)`.

The unnormalised measure `lambda` is stationary and

\[
 \sum_{v,C}\lambda_v(C)=m.                            \tag{8}
\]

Under the normalized stationary marked law, including the fair stop coin,

\[
 \mathcal C(P):=\Pr(W=I)={1\over2m}.                 \tag{9}
\]

Consequently the literal stationary-collision target is

\[
 \boxed{\mathcal C(P)\ge {1\over2m_K}.}              \tag{10}
\]

Equations `(4)`, `m<=m_K`, and `(10)` are equivalent.

## 3. Active chain

Let

\[
 \mathcal Y=\{(B,v):\varnothing\ne B\subseteq
 V\setminus\{v\}\}.                                \tag{11}
\]

Starting from `y=(B,v)`, the forward active chain `K_P=R A_P` has the
following exact transition experiment.

* With probability `1/2`, retain target `v`, sample `i~P_v`, and output
  `(B union {i},v)`.
* With probability `1/2`, choose `w` uniformly from `B`, delete `w`, sample
  `i~P_w`, and output `((B minus {w}) union {i},w)`.

Let `nu` be its stationary probability law and put

\[
 H(B,v)={1\over |B|}.                                \tag{12}
\]

The marked identities give

\[
 \nu H={1\over m}.                                   \tag{13}
\]

Equivalently, relative to the complete active law

\[
 \nu_K(B,v)={|B|\over nN2^{N-1}},                    \tag{14}
\]

the stationary density `g=dnu/dnu_K` is the positive fixed point

\[
 g=\mathcal T_Pg,\qquad \mathcal T_P=\mathcal B_P\mathcal Q,          \tag{15}
\]

where

\[
 (\mathcal Qg)(C,v)
 ={ |C|\over N}g(C,v)
 +{1\over N}\sum_{u\notin C\cup\{v\}}g(C\cup\{v\},u),             \tag{16}
\]

\[
 (\mathcal B_Ph)(B,v)
 ={N\over2|B|}\left\{P_{vB}h(B,v)
 +\sum_{i\in B}P_{vi}h(B\setminus\{i\},v)\right\}.                 \tag{17}
\]

With normalization

\[
 \sum_{B,v}|B|g(B,v)=nN2^{N-1},                     \tag{18}
\]

one has

\[
 {1\over m}={1\over nN2^{N-1}}\sum_{B,v}g(B,v).     \tag{19}
\]

Therefore the exact target is also

\[
 \boxed{\sum_{\mathcal Y}g\ge |\mathcal Y|.}        \tag{20}
\]

## 4. Exact tree and determinant forms

Put `L_P=I-K_P`.  For an active state `y`, define

\[
 \tau_y=\det L_P^{(y)},                              \tag{21}
\]

the total weight of directed spanning in-arborescences rooted at `y`.
The tree theorem gives

\[
 \nu(y)={\tau_y\over Z_P},\qquad
 Z_P=\sum_y\tau_y>0.                                \tag{22}
\]

Combining `(13)` and `(22)`, the following are equivalent:

\[
 \rho_{\rm dB}(G,2)\le\rho_{\rm dB}(K_n,2),
\quad m\le m_K,
\quad \mathcal C(P)\ge {1\over2m_K},
\quad \mathfrak F_0(P)\ge0,                         \tag{23}
\]

where

\[
 \mathfrak F_0(P)=
 \sum_y\tau_y\left(H(y)-{1\over m_K}\right).       \tag{24}
\]

By multilinearity, `(24)` is the coefficient of `epsilon` in

\[
 \det\left[L_P+\epsilon\operatorname{diag}
 \left(H-{1\over m_K}\right)\right].                \tag{25}
\]

This is the minimal active-arborescence sign.  It is not merely sufficient.

## 5. The stronger promotion sign is not the target

Let `U` be uniform on `X`, let `psi` be the exact alternating rank
observable, and set

\[
 c_P=UM_P^2\psi
 ={1\over m_K}+a_nD_1(P)+b_nD_2(P),                 \tag{26}
\]

with `a_n,b_n>0` and

\[
 D_1=\sum_{v,i}P_{vi}^2-{n\over n-1}\ge0,           \tag{27}
\]

\[
 D_2=\sum_i\left(\sum_vP_{vi}-1\right)^2
 +{1\over2}\sum_{v,i}(P_{vi}-P_{iv})^2\ge0.         \tag{28}
\]

The promotion conjecture is

\[
 \mathfrak F_2(P):=
 \sum_y\tau_y\{H(y)-c_P\}\ge0.                    \tag{29}
\]

It is equivalent to the previously recorded Perron, Cesaro, Abel, and
promotion-arborescence statements.  But

\[
 \boxed{\mathfrak F_0(P)=\mathfrak F_2(P)
 +(c_P-1/m_K)Z_P.}                                  \tag{30}
\]

Thus `(29)` implies `(24)`.  No converse has been proved, and `(30)` shows
that the two determinant coefficients are different off the complete
kernel.  The universal collision theorem must not be reported as equivalent
to promotion.

## 6. Green, posterior, and named quantities

For comparison with the other exact reductions, the complete Green
calculation gives

\[
 \rho_{\rm dB}(G,2)-\rho_{\rm dB}(K_n,2)
 =\mathcal L(G)-\mathcal V(G),                       \tag{31}
\]

where `L` is the stationary weighted cut surplus and `V>=0` is the explicit
Green-weighted subset-mass tangent dispersion.  Therefore

\[
 \mathfrak F_0(P)\ge0\quad\Longleftrightarrow\quad
 \mathcal L(G)\le\mathcal V(G).                     \tag{32}
\]

For a stationary output `B`, `k=|B|`, `h=n-k`, define the effective-target
posterior ratio and its collision excess by

\[
 e_v(B)={\nu_v(B)\over\Pi(B)},\qquad
 J(B)=\sum_{v\notin B}\left(e_v(B)-{k\over h}\right)^2.             \tag{33}
\]

The harmonic posterior dispersion used in the sharper sufficient route is

\[
 G(B)=\sum_{v\notin B}{1\over1+e_v(B)}-{h^2\over n}.                 \tag{34}
\]

The proved arithmetic--harmonic lemma bounds `J(B)` by a rank-dependent
multiple of `G(B)`.  The resulting stationary `G` inequality is sufficient,
not equivalent, to `(24)`.  The symbol `C` in that probability-space route
is the pre-update occupied-target flag; the literal collision observable
relevant here is `mathcal C(P)` in `(9)`.

## 7. Exact triangle forest certificate

Let `n=3` and let the three positive edge weights be

\[
 w_{01}=a,\qquad w_{02}=b,\qquad w_{12}=c.           \tag{35}
\]

Directly expanding all nine active cofactors and clearing the positive
denominator gives

\[
 \mathfrak F_0(P)=
 {3F(a,b,c)\over4096(a+b)^2(a+c)^2(b+c)^2},          \tag{36}
\]

where

\[
 \boxed{
 F(a,b,c)=
 (a-b)^2q(a,b,c)+(b-c)^2q(b,c,a)+(c-a)^2q(c,a,b)}   \tag{37}
\]

and

\[
 q(x,y,z)=16x^2y^2+20xy(x+y)z+19xyz^2+12(x+y)z^3.   \tag{38}
\]

Every coefficient of `q` is positive.  Hence `(24)` holds for every
positive weighted triangle, with equality exactly when `a=b=c`.
Continuity gives the connected zero-edge boundary as well, and equality
remains only the complete kernel.

This is a genuine coefficientwise certificate only after centering in the
edge differences.  In the raw monomial basis, `F` contains, for example,

\[
 -114a^2b^2c^2-8a^3b^3-13a^3b^2c,                  \tag{39}
\]

among other negative coefficients.  Thus a universal forest proof cannot
expect unrecentered monomial coefficient positivity.

## 8. Equality status

The complete replacement kernel satisfies equality in `(24)`.  The exact
triangle calculation proves it is the only equality kernel at order three.
The universal equality class remains **OPEN** together with `(24)`.  The
two-step defects vanish only at the complete kernel, so equality in the
stronger promotion sign, if proved, would force the same class.

## 9. Exact failures that constrain a forest proof

The following stronger routes have exact counterexamples and are not inputs
to `(24)`:

1. pointwise complete-Poisson comparison;
2. active-rank stochastic domination;
3. monotonicity of `UM_P^t psi`;
4. a stationary lower envelope for all radial PGFs;
5. per-rank residual negativity;
6. separate symmetric-flow signs;
7. edgewise, targetwise, cyclewise, or fixed state-tree-skeleton signs;
8. ordinary one-particle entropy and fixed-reference `L^2` contraction;
9. a state-dependent sampling-row relaxation.

The triangle expansion `(37)` also rules out a raw positive-monomial
arborescence certificate.  A viable all-order proof must group trees into
centered multi-tree packages, most plausibly packages carrying squared
differences of original replacement flows.

## 10. Current open coefficient problem

Expand every active transition into its labelled continue or
retarget/delete/sample event.  After multiplying `(24)` by a common positive
product of row degrees, group the resulting rooted-tree monomials into
packets.  The desired universal certificate is a decomposition

\[
 D(P)\mathfrak F_0(P)
 =\sum_\alpha \Delta_\alpha(P)^2Q_\alpha(P),         \tag{40}
\]

where `D(P)>0`, each `Q_alpha` has nonnegative labelled-forest
coefficients, and simultaneous vanishing of the `Delta_alpha` forces the
complete replacement kernel.  Formula `(37)` is the exact `n=3` model.

No such grouping is presently proved for arbitrary `n`.

## 11. Smaller subset-root determinant and failed polynomial shortcuts

The active determinant is not the smallest exact determinant.  Let `Q_P`
be the uniform-target fair-geometric union kernel on

\[
 \Omega=\{A:\varnothing\ne A\subsetneq V\},
\]

let `L_P^sub=I-Q_P`, and let

\[
 \widehat\tau_A=\det (L_P^{sub})^{(A)},\qquad
 Z_P(t)=\sum_{A\in\Omega}\widehat\tau_A t^{|A|}.     \tag{41}
\]

Then

\[
 {Z_P'(1)\over Z_P(1)}=m,                            \tag{42}
\]

so the true target is equivalently the smaller determinant sign

\[
 \boxed{m_KZ_P(1)-Z_P'(1)\ge0.}                     \tag{43}
\]

Also, for `D(t)=diag(t^{|A|})`,

\[
 Z_P(t)=[\epsilon]\det\{L_P^{sub}+\epsilon D(t)\}.  \tag{44}
\]

The active sign `(24)` and subset sign `(43)` have the same sign because
both are positive normalizations of `m_K-m`; no promotion hypothesis is
needed for this transfer.  The subset matrix has `2^n-2` states, compared
with `n(2^{n-1}-1)` active states.

Three tempting root-polynomial shortcuts are exactly unavailable.

1. **Real-rootedness/stability fails at the reference graph.**  For `K_4`,

   \[
   Z_K(t)\doteq t(t^2+3t+3),                       \tag{45}
   \]

   whose nonzero roots are not real.

2. **Ultra-log-concavity fails on the unweighted four-star.**  Its normalized
   level coefficients are

   \[
   (\pi_1,\pi_2,\pi_3)=\left({25\over36},{1\over4},{1\over18}\right),
   \]

   and

   \[
   \pi_2^2-3\pi_1\pi_3=-{23\over432}<0.             \tag{46}
   \]

3. **Even ordinary log-concavity fails at order five.**  Take the weighted
   tree with nonzero edges

   \[
   w_{02}=1000,\quad w_{03}=7,\quad w_{14}=7,\quad w_{24}=7.          \tag{47}
   \]

   Its exact stationary level law satisfies

   \[
   \pi_2^2-\pi_1\pi_3<0.                            \tag{48}
   \]

The six-vertex rank-tail witness also has

\[
 \Pr_\Pi\{|A|\ge2\}>{30\over31},                   \tag{49}
\]

while still having `m<80/31`.  Thus coefficientwise level domination and
root stochastic domination fail in the direction that would prove `(43)`.
Any successful use of `Z_P` must control its logarithmic derivative at one
directly, not through real stability, log-concavity, or levelwise ordering.
