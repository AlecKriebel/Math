# Complete-ray fixed-colour form of the fitness-two product inequality

Date: 2026-08-13 (America/Los_Angeles)

No literature search or external communication was used.

## 1. Status and the surviving all-order target

For a connected loopless undirected conductance matrix `W`, let `L` be the
fitness-two Bd dual on the nonempty subsets and let `D` be the
fair-geometric dB dual on the nonempty proper subsets.  Write

\[
 \begin{array}{lll}
 Z_L=\sum_A\tau_L(A),&Y_L=\sum_A|A|\tau_L(A),&m_L=Y_L/Z_L,\\
 Z_D=\sum_B\tau_D(B),&Y_D=\sum_B|B|\tau_D(B),&m_D=Y_D/Z_D,
 \end{array}                                                   \tag{1}
\]

where the `tau` are directed in-arborescence cofactors.  The complete-graph
means are

\[
 b_n={N_b\over D_b}={n2^{n-1}\over2^n-1},\qquad
 d_n={N_d\over D_d}={(n-1)2^{n-2}\over2^{n-1}-1}.             \tag{2}
\]

The decisive product inequality is

\[
                         m_Lm_D\le b_nd_n.                    \tag{PAPT_n}
\]

It rules out simultaneous strict amplification at fitness two.  This note
puts `PAPT_n` into one exact denominator-cleared complete-ray form.  Its
fixed-colour coefficients are expectations under a genuine unsigned law
on two coupled decorated directed forests.

**PROVED here:** the positive polynomial clearing, the coloured-forest
expectation identity, vanishing of colour levels zero and one, positivity
of every colour level for `n=3`, and the exact two-orbit quadratic base in
the sole order-four audit.

**OPEN:** the conditional root-rank expectation at general `n` and colour
level `j>=3`.  This is now the single sign in this route.

## 2. Positive polynomial clearing of both duals

Put

\[
 d_v=\sum_{u\ne v}w_{vu},\qquad
                         \Lambda(W)=\prod_vd_v.              \tag{3}
\]

Every off-diagonal `L` rate is a sum of row-arrow terms `w_vu/d_v`.
Consequently every entry of

\[
                             \widehat L=\Lambda L             \tag{4}
\]

is a homogeneous polynomial of degree `n`, and every off-diagonal entry is
coefficientwise nonnegative.  Explicitly, one arrow term becomes

\[
                  w_{vu}\prod_{x\ne v}d_x.                   \tag{5}
\]

The corresponding statement for `D` needs the following exact local
identity.  Let `p_vu=w_vu/d_v`, let `N>=1` have
`Pr(N=k)=2^{-k}`, and take `N` iid samples from row `p_v`.  If `g_v(J)` is
the probability that the set of distinct samples is exactly the nonempty
set `J`, then partitioning sample strings by the order `pi` in which their
elements first appear gives

\[
 \boxed{
 g_v(J)=\sum_{\pi\in\mathfrak S(J)}
       \prod_{r=1}^{|J|}
       {w_{v\pi_r}\over 2d_v-w_v(S_r)},\qquad
 S_r=\{\pi_1,\ldots,\pi_r\}.}                                \tag{6}
\]

Indeed, after the first appearance of `pi_r`, any number of repeats in
`S_r` has total geometric weight
`1/(1-p_v(S_r)/2)`.  Multiplying that factor by the weight
`p_{v,pi_r}/2` of the next first appearance gives exactly the `r`th factor
in `(6)`.

Define the **full positive clearing**

\[
 \Gamma_v(W)=
 \prod_{\varnothing\ne S\subseteq V\setminus\{v\}}
                 (2d_v-w_v(S)),\qquad
                         \Gamma(W)=\prod_v\Gamma_v(W).       \tag{7}
\]

The full-neighbour factor is `d_v`; it must be retained here.  For every
prefix in `(6)`, its denominator is one distinct factor of `Gamma_v`, and

\[
 2d_v-w_v(S)=\sum_{u\in S}w_{vu}
              +2\sum_{u\notin S,\,u\ne v}w_{vu}              \tag{8}
\]

is a positive linear form.  Therefore

\[
 \Gamma_vg_v(J)=\sum_{\pi\in\mathfrak S(J)}
   \left(\prod_rw_{v\pi_r}\right)
   {\Gamma_v\over\prod_r(2d_v-w_v(S_r))}                     \tag{9}
\]

is a coefficientwise nonnegative polynomial.  It follows that

\[
                              \widehat D=\Gamma D             \tag{10}
\]

has homogeneous polynomial entries and coefficientwise nonnegative
off-diagonal entries.

This corrects a tempting smaller clearing which omits the full-neighbour
factor.  The smaller clearing is algebraically valid after cancellations,
but it hides the unsigned first-appearance expansion and therefore is not
the canonical choice for fixed-colour conditioning.

## 3. The canonical homogeneous paired-tree polynomial

The two state-space sizes and the degrees of one hatted rate are

\[
 M_L=2^n-1,\quad M_D=2^n-2,\qquad
 \ell=n,\quad \gamma=n(2^{n-1}-1).                            \tag{11}
\]

Thus a hatted `L` tree has degree `ell(M_L-1)`, a hatted `D` tree has
degree `gamma(M_D-1)`, and every paired tree has the common degree

\[
 \boxed{q_n=n(2^n-2)+n(2^{n-1}-1)(2^n-3).}                   \tag{12}
\]

Let `widehat tau`, `widehat Z`, and `widehat Y` denote the tree cofactors
and their zeroth and root-rank moments formed from `(4)` and `(10)`.  Since
global scalar multiplication of an `M`-state generator multiplies each
tree cofactor by the scalar to power `M-1`, the polynomial

\[
 \boxed{
 \mathscr P_n(W)=N_bN_d\widehat Z_L\widehat Z_D
                 -D_bD_d\widehat Y_L\widehat Y_D}            \tag{13}
\]

has the same sign as `b_nd_n-m_Lm_D`.  It is homogeneous of degree `q_n`.

Equivalently, if `T_L,T_D` range over hatted directed in-trees, `r(T)` is
the root subset, and

\[
 \chi(T_L,T_D)=N_bN_d-D_bD_d|r(T_L)|\,|r(T_D)|,              \tag{14}
\]

then

\[
 \mathscr P_n(W)=\sum_{T_L,T_D}\chi(T_L,T_D)
                       \omega_{T_L,T_D}(W),                  \tag{15}
\]

where each paired-tree weight `omega` is a coefficientwise nonnegative
homogeneous polynomial of degree `q_n`.

## 4. Fixed colours on the complete-to-actual ray

Let `K` be the unit complete conductance matrix and

\[
                         W_\alpha=(1-\alpha)K+\alpha W.       \tag{16}
\]

For a degree-`q_n` polynomial `F`, write `Pol_F` for its symmetric
`q_n`-linear polarization, normalized by `Pol_F(X,...,X)=F(X)`.  Define

\[
 C_{n,j}(W)=\operatorname{Pol}_{\mathscr P_n}
       (\underbrace{K,\ldots,K}_{q_n-j},
        \underbrace{W,\ldots,W}_{j}).                        \tag{17}
\]

Then the exact Bernstein expansion is

\[
 \boxed{
 \mathscr P_n(W_\alpha)=\sum_{j=0}^{q_n}\binom{q_n}{j}
 C_{n,j}(W)\alpha^j(1-\alpha)^{q_n-j}.}                      \tag{18}
\]

The positive formulas `(5)` and `(9)` refine every tree into decorated
terms which are products of exactly `q_n` nonnegative linear forms.  For
one such product `omega=prod_s ell_s`,

\[
 \operatorname{Pol}_{\omega}(K^{q_n-j},W^j)
 ={1\over\binom{q_n}{j}}
 \sum_{\substack{J\subseteq[q_n]\\|J|=j}}
       \prod_{s\in J}\ell_s(W)
       \prod_{s\notin J}\ell_s(K).                          \tag{19}
\]

Thus `(17)` means: expand both directed trees into positive local-arrow and
first-appearance decorations, choose exactly `j` of their combined
`q_n` microscopic linear slots to receive the actual colour `W`, give the
other slots the complete colour `K`, and globally sum.

Let

\[
 \Omega_{n,j}(W)=\sum_{T_L,T_D}
 \operatorname{Pol}_{\omega_{T_L,T_D}}(K^{q_n-j},W^j)>0.     \tag{20}
\]

Normalizing these unsigned weights defines a probability law
`mu_{n,j}^W` on the coupled decorated tree pair and its fixed-size colour
set.  Equations `(14)--(20)` give the exact central identity

\[
 \boxed{
 C_{n,j}(W)=\Omega_{n,j}(W)
 \left\{N_bN_d-D_bD_d
 \mathbb E_{\mu_{n,j}^W}[R_LR_D]\right\},}                   \tag{21}
\]

where `R_L=|r(T_L)|` and `R_D=|r(T_D)|`.  Therefore

\[
 \boxed{C_{n,j}(W)\ge0
 \quad\Longleftrightarrow\quad
 \mathbb E_{\mu_{n,j}^W}[R_LR_D]\le b_nd_n.}                \tag{22}
\]

The live theorem-shaped target is

\[
                         C_{n,j}(W)\ge0\quad(2\le j\le q_n). \tag{23}
\]

It implies `PAPT_n` by setting `alpha=1`.  It is weaker than the refuted
orbital-midpoint conjecture and does not assert convexity or positivity of
one-edge second derivatives.

### 4.1 Exact sector convolution

It is useful to expose precisely how the two replicas are coupled.  Put

\[
 q_L=n(2^n-2),\qquad q_D=n(2^{n-1}-1)(2^n-3),\qquad q_n=q_L+q_D.\tag{24}
\]

Let `Z^L_a,Y^L_a` be the colour-`a` polarizations of the hatted `L` tree
partition and root moment, and define `Z^D_b,Y^D_b` analogously.  Then

\[
 \boxed{
 C_{n,j}={1\over\binom{q_n}{j}}
 \sum_{a+b=j}\binom{q_L}{a}\binom{q_D}{b}
 \{N_bN_dZ^L_aZ^D_b-D_bD_dY^L_aY^D_b\}.}                   \tag{25}
\]

Conditional on the split `(a,b)`, the roots are independent; conditioning
only on the **total** number `j` couples them through the positive sector
partition functions `Z^L_aZ^D_b`.  This distinction matters below.

## 5. The zero-, one-, and two-colour bases

The complete graph has equality, so `C_{n,0}=mathscr P_n(K)=0`.  Moreover,
`mathscr P_n` is invariant under every vertex permutation.  At `K` all
edge partial derivatives are therefore equal.  Euler's identity and
`mathscr P_n(K)=0` force their common value to vanish.  Hence

\[
                             C_{n,0}=C_{n,1}=0.               \tag{26}
\]

In algebraic terms, if

\[
 I_K=(w_e-w_f:e,f\in E(K_n)),                                \tag{27}
\]

then

\[
                             \mathscr P_n\in I_K^2.           \tag{28}
\]

This proves formal second-order vanishing, not positivity: `I_K^2`
contains signed mixed products.

For `n>=4`, the edge permutation representation off the constant direction
has two irreducible quadratic orbit types.  Equivalently an invariant
quadratic form needs both the adjacent- and disjoint-edge energies

\[
 E_{\rm adj}(H)=\sum_{e<f,\ e\cap f\ne\varnothing}(H_e-H_f)^2,
 \quad
 E_{\rm dis}(H)=\sum_{e<f,\ e\cap f=\varnothing}(H_e-H_f)^2. \tag{29}
\]

The sole exact order-four audit uses

\[
\begin{array}{c|rrrrrr}
e&01&02&03&12&13&23\\ \hline
H_{\rm std}&0&1&1&-1&-1&0\\
H_{\rm cyc}&1&-1&0&0&-1&1.
\end{array}                                                   \tag{30}
\]

For the fixation-product gap

\[
 G(W)={8\over15}{3\over7}-\rho_{Bd}(W,2)\rho_{dB}(W,2),     \tag{31}
\]

direct exact stationary differentiation at `K_4` gives

\[
 \begin{array}{c|cc}
 &H_{\rm std}&H_{\rm cyc}\\ \hline
 \rho_{Bd}''&-24256/1257525&0\\
 \rho_{dB}''&-29/245&-12/637\\
 G''&293288/4107915&32/3185\\
 E_{\rm adj}&16&24\\
 E_{\rm dis}&8&0.
 \end{array}                                                  \tag{32}
\]

Consequently the exact quadratic form is

\[
 \boxed{G''_K(H,H)=
 {4\over9555}E_{\rm adj}(H)
 +{431881\over53402895}E_{\rm dis}(H),}                     \tag{33}
\]

with both orbit coefficients positive.  Since `mathscr P_n` is a positive
clearing multiple of `G` and both `G` and its gradient vanish at `K`, its
two-colour coefficient is the same quadratic form times the positive
constant

\[
 {n^2D_bD_d\widehat Z_L(K)\widehat Z_D(K)\over q_n(q_n-1)}. \tag{34}
\]

Thus `C_{4,2}>=0`.  Equation `(33)` also refutes the previously proposed
single covariant vertex-wedge-square factorization: one adjacent-edge orbit
alone would force the ratio `16/24`, whereas `(32)` does not.

## 6. Every fixed-colour coefficient is positive for `n=3`

For a triangle with edge conductances `(x,y,z)`, the exact theorem in the
companion folder gives the primitive product-gap numerator

\[
 N=\sum_{(i,j,k)}\gamma_{ijk}
 \sum_{\pi\in S_3}x_{\pi(1)}^iy_{\pi(2)}^jz_{\pi(3)}^k
 (x_{\pi(1)}-y_{\pi(2)})^2,                                 \tag{35}
\]

where `i+j+k=16` and all 24 coefficients `gamma` are positive integers.
For the full clearing `(7)`, the canonical degree is `q_3=63`, and direct
comparison with the compact fixation formulas gives

\[
 \mathscr P_3=72(d_0d_1d_2)^7\delta^4N,                     \tag{36}
\]

where

\[
 \delta=(x+2y)(2x+y)(x+2z)(2x+z)(y+2z)(2y+z).               \tag{37}
\]

Along the complete ray,

\[
 x_\alpha^iy_\alpha^jz_\alpha^k(x_\alpha-y_\alpha)^2
 =\alpha^2(x-y)^2x_\alpha^iy_\alpha^jz_\alpha^k.           \tag{38}
\]

The remaining 16 monomial factors, the 21 factors in
`(d_0d_1d_2)^7`, and the 24 factors in `delta^4` are positive linear
interpolants.  Each has nonnegative endpoint controls, and products
preserve nonnegative Bernstein controls.  Applying this to every atom in
`(35)` proves

\[
                 \boxed{C_{3,j}(W)\ge0\quad(0\le j\le63).}   \tag{39}
\]

This is strictly stronger than endpoint `PAPT_3` and supplies the exact
fixed-colour base case.

## 7. The exact remaining inequality

The complete-ray route has now reduced to one statement:

> **Fixed-colour paired-root inequality.**  Under the unsigned decorated
> paired-tree law obtained by putting exactly `j` actual colours among all
> `q_n` microscopic slots, the product of the two root ranks has expectation
> at most its complete value `b_nd_n`.

Formula `(25)` shows why an unqualified appeal to sampling without
replacement is not yet a proof.  Given a decorated tree packet, its colour
set is sampled without replacement; but evaluation at `W` reweights both
the packet and the split `a+b=j`.  Moreover the rank product is a function
of the two **roots**, while the sampled objects are local linear slots.
Exchangeability of the colour labels alone gives `(26)` but supplies no
monotone relation between a slot colour and either root rank.

This obstruction has a particularly sharp covariance form.  Let `nu_0`
be the complete-colour law on the fully decorated paired-tree packets.  If
the `q_n` positive linear slots in a packet `theta` are `ell_s`, put

\[
                         r_s(\theta)={\ell_s(W)\over\ell_s(K)}.\tag{41}
\]

Summing `(19)` over the colour set shows that `mu_{n,j}^W` is the tilt of
`nu_0` by the elementary symmetric polynomial:

\[
 {d\mu_{n,j}^W\over d\nu_0}(\theta)
 ={e_j(r_1(\theta),\ldots,r_{q_n}(\theta))
   \over\mathbb E_{\nu_0}e_j(r_1,\ldots,r_{q_n})}.           \tag{42}
\]

Since the complete root product has expectation `b_nd_n`, `(22)` is
exactly

\[
 \boxed{
 \operatorname {Cov}_{\nu_0}
 \left(R_LR_D,e_j(r_1,\ldots,r_{q_n})\right)\le0.}           \tag{43}
\]

The standard negative association of weighted sampling without replacement
does **not** imply `(43)`.  Conditional on `theta`, it controls increasing
functions of disjoint groups of the colour indicators, but `R_LR_D` is
already constant.  Its conditional covariance with every colour statistic
is therefore exactly zero.  The whole sign in `(43)` lives across forest
packets, in the relation between their roots and their slot ratios.  A proof
must supply negative regression for that packet law; exchangeability of the
colour set is not such a mechanism.

A sufficient elementary property would be a sign-preserving root/slot
coupling showing that the conditional mean

\[
 {Y^L_a\over Z^L_a}{Y^D_b\over Z^D_b}                       \tag{40}
\]

lies below `b_nd_n` after the hypergeometric-sector averaging in `(25)`.
It is not necessary that every individual sector in `(40)` have that sign;
the exact first-order cancellation already couples the `(1,0)` and `(0,1)`
sectors.  The minimal object to prove is therefore the globally weighted
sum `(25)`, or equivalently `(22)`, not separate marginal suppression and
not a packetwise forest injection.

One targeted exact `K_4` audit of `(43)` was made on the previously frozen
hostile conductance ray

\[
 (w_{01},w_{02},w_{03},w_{12},w_{13},w_{23})
 =(0,1000,2,1,1000,10).                                    \tag{44}
\]

Second-order-through-twelfth-order rational determinant series, converted
to the canonical degree-420 Bernstein basis, give

\[
 C_{4,j}>0\quad(2\le j\le12),\qquad
 \mathbb E_{\mu_{4,j}}[R_LR_D]
 \text{ strictly decreases for }0\le j\le12.               \tag{45}
\]

This supports negative regression but does not prove it.  No additional
graph or architecture scan was performed.

## 8. Replay and scope

Run

```text
PYTHONDONTWRITEBYTECODE=1 ../../../.venv/bin/python -B verify_complete_ray_coloured_forests.py
```

The verifier checks `(6)` against inclusion--exclusion, audits the positive
full clearing and degrees, replays the triangle Bernstein consequence, and
independently computes the two exact order-four stationary variations in
`(32)--(33)` using second-order rational series.

The adjacent exploratory script
`explore_n4_fixed_colour_path.py` performs only the targeted hostile-ray
audit `(44)--(45)`.  Its current filename is retained to avoid churn; it is
not a graph search and proves no general sign.

**PROVED:** `(6)--(22)`, `(26)--(28)`, the `n=3` fixed-colour theorem
`(39)`, and the two positive order-four quadratic orbit weights `(33)`.

**FALSIFIED:** a universal one-orbit covariant wedge-square completion.

**OPEN:** `(22)` for arbitrary `n` and `j>=3`, hence `PAPT_n` and the exact
fitness-two upper closure.
