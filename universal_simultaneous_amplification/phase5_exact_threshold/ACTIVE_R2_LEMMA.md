# Canonical fitness-two lemma

Last updated: 2026-08-08.  Status labels are literal.

## 1. Graph kernel and exact dual law

Let `G` be a finite connected loopless undirected weighted graph of order
`n>=3`, with weighted degrees `d_v`, and put

\[
P_{vu}=w_{vu}/d_v,qquad N=n-1.
\]

Thus `P` is loopless, row stochastic, irreducible, and reversible with
respect to `(d_v)`.  Let `Pi` be the stationary law on nonempty proper
subsets of the exact fair-geometric union dual for dB updating at fitness
two, and put

\[
m=E_\Pi|A|,
\qquad
m_K={N2^{n-2}\over2^{n-1}-1}.
\]

The coverage dual gives

\[
\rho_{\rm dB}(G,2)=m/n,
\qquad
\rho_{\rm dB}(K_n,2)=m_K/n.
\]

Therefore the exact universal theorem is equivalent to

\[
\boxed{m\le m_K.}                                      \tag{R2-1}
\]

## 2. Literal collision form

For a target `v` and cache `C` with `v notin C`, define

\[
\sigma_v(C)=\Pi(C\cup\{v\}),
\qquad
\lambda_v(C)={\sigma_v(C)+\nu_v(C)\over2},
\]

where `nu_v` is the exact effective incoming target mass and satisfies the
proved Cayley identity `nu_v=lambda_v A_v`, with `A_v` adjoining one sample
from row `P_v`.

On the marked space

\[
\mathcal X=\{(C,v):v\notin C\},
\]

the one-sample chain draws `I~P_v`, sets `B=C union {I}`, and with equal
probability either continues at `(B,v)` or selects `W` uniformly from `B`
and moves to `(B minus {W},W)`.  The unnormalised law `lambda` is stationary
and has total mass `m`.

On a stopping step,

\[
\Pr\{W=I\}={1\over2m}.
\]

Hence (R2-1) is exactly the collision inequality

\[
\boxed{\Pr\{W=I\}\ge {1\over2m_K}.}                   \tag{R2-2}
\]

## 3. Active Perron form

Let

\[
\mathcal Y=\{(B,v):\varnothing\ne B\subseteq V\setminus\{v\}\}.
\]

Relative to the complete active law, the stationary active density `g` is
the positive fixed point

\[
g=\mathcal T_Pg,
\qquad
\mathcal T_P=\mathcal B_P\mathcal Q,
\]

where, for `k=|C|` and `b=|B|`,

\[
(\mathcal Qg)(C,v)
 ={k\over N}g(C,v)
 +{1\over N}\sum_{u\notin C\cup\{v\}}g(C\cup\{v\},u),
\]

\[
(\mathcal B_Ph)(B,v)
 ={N\over2b}\left(P_{vB}h(B,v)
 +\sum_{i\in B}P_{vi}h(B\setminus\{i\},v)\right).
\]

Normalize by

\[
\sum_{(B,v)\in\mathcal Y}|B|g(B,v)
 =nN2^{N-1}.
\]

Then

\[
{1\over m}={1\over nN2^{N-1}}\sum_{\mathcal Y}g,
\]

so (R2-1) is exactly

\[
\boxed{\sum_{\mathcal Y}g\ge|\mathcal Y|.}            \tag{R2-3}
\]

## 4. Proved two-step surplus and the named promotion lemma

For the exact alternating rank observable `psi`, uniform marked law `U`, and
marked kernel `M_P`, the proved identity is

\[
UM_P^2\psi={1\over m_K}+a_nD_1(P)+b_nD_2(P),           \tag{R2-4}
\]

where `a_n,b_n>0` and

\[
D_1=\sum_{v,i}P_{vi}^2-{n\over n-1}\ge0,
\]

\[
D_2=\sum_i\left(\sum_vP_{vi}-1\right)^2
 +{1\over2}\sum_{v,i}(P_{vi}-P_{iv})^2\ge0.
\]

Equality in (R2-4) holds exactly for the complete replacement kernel
`P_{vi}=1/(n-1)` for `i!=v`, hence for the unit complete graph up to global
weight scaling in the undirected model.

The currently named sufficient promotion lemma is

\[
\boxed{\sum_{\mathcal Y}g
 \ge \sum_{\mathcal Y}\mathcal T_P^2\mathbf1.}          \tag{PROM}
\]

Because the right side is at least `|Y|` by (R2-4), `PROM` implies (R2-3).
At phase start, no converse from (R2-3) to `PROM` has been proved.  The prior
note's use of the word "equivalent" at this point is under hostile audit and
must not be relied upon without an additional argument.

## 5. Exact dual forms of `PROM`

Let `K_P` be the forward active chain, `H(B,v)=1/|B|`, and

\[
a_t=\nu_KK_P^tH=UM_P^t\psi,
\qquad
c_P=a_2.
\]

Then the following are proved equivalent to `PROM`:

1. quenched Cesaro persistence

   \[
   \lim_{T\to\infty}{1\over T}\sum_{t<T}a_t\ge a_2;
   \]

2. rare-restart Abel limit, with

   \[
   r_\epsilon=\epsilon\sum_{t\ge0}(1-\epsilon)^ta_t,
   \qquad
   \lim_{\epsilon\downarrow0}r_\epsilon\ge a_2;
   \]

3. active in-arborescence sign

   \[
   \boxed{\sum_{y\in\mathcal Y}\tau_y\{H(y)-c_P\}\ge0,} \tag{R2-5}
   \]

   where `tau_y=det(I-K_P)^(y)` is the rooted in-tree cofactor;

4. nonnegativity of the coefficient of `epsilon` in

   \[
   \det\{I-K_P+\epsilon\operatorname{diag}(H-c_P)\}.
   \]

The required new ingredient is a nonnegative forest/determinant expansion,
cycle-surplus identity, or a direct proof of (R2-3) that bypasses `PROM`.

Independently of `PROM`, the Markov-chain tree theorem gives the determinant
form exactly equivalent to the true collision target:

\[
\boxed{\sum_{y\in\mathcal Y}\tau_y
 \left\{H(y)-{1\over m_K}\right\}\ge0.}              \tag{R2-5C}
\]

It is the coefficient of `epsilon` in

\[
\det\left\{I-K_P+\epsilon\operatorname{diag}
 \left(H-{1\over m_K}\right)\right\}.
\]

Since `c_P=a_2>=1/m_K`, the promotion tree sign (R2-5) implies (R2-5C),
but the converse is not proved.

## 6. Equality cases

- Complete kernel: equality in (R2-1)--(R2-3), and `D_1=D_2=0`.
- Any universal proof must determine whether another reversible loopless
  kernel can tie (R2-1).  No such kernel appears in the exact corpus.
- Equality of the two-step SOS already forces the complete kernel.

## 7. Stronger statements already refuted exactly

Do not use without a new ingredient:

1. stochastic domination of active rank by
   `1+Bin(n-2,1/2)`;
2. monotonicity of `UM_P^t psi` in `t`;
3. a stationary lower envelope for every radial PGF observable;
4. pointwise complete-Poisson forcing;
5. per-rank residual negativity;
6. the symmetric-flow split `L<=S<=V`;
7. ordinary one-particle entropy or fixed-reference `L^2` contraction;
8. edgewise, targetwise, or cyclewise positive stationary decomposition.

The exact six-vertex rank-tail witness and exact five-vertex temporal/PGF
witnesses still satisfy (R2-1) strictly.  They close routes, not the theorem.

## 8. Independent Green form

The exact forward/dual Green reduction is

\[
\rho_{\rm dB}(G,2)-\rho_{\rm dB}(K_n,2)
 =\mathcal L(G)-\mathcal V(G),
\qquad \mathcal V(G)\ge0.
\]

Thus (R2-1) is also exactly

\[
\boxed{\mathcal L(G)\le\mathcal V(G).}                \tag{R2-6}
\]

Here `L` is the stationary weighted cut surplus and `V` the explicit tangent
dispersion in the phase-4 Green--collision note.  Neither term has the
required sign separately.
