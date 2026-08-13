# Exact coverage structure and a refuted degree-profile envelope

Date: 2026-08-13 (America/Los_Angeles)

## Status

This note formalizes an exact structural fact about the fitness-two dB
fixation committor: it is a normalized coverage function and hence is
monotone and submodular.  The statement is **PROVED** for the actual finite
chain, with all coalescence retained.

The note then records a proof-first attempt to combine this structure with
reversibility.  The resulting stationary-degree profile envelope is
**EXACTLY REFUTED** by a six-vertex equitable weighted graph.  Consequently
coverage/submodularity by itself does not turn reversible vertex masses into
the sharp complete-graph bound.  The universal fitness-two upper bound
remains **OPEN**.

## 1. Exact Boolean duality and coverage representation

Let `V` be the vertex set of a finite connected loopless undirected weighted
graph, and put

\[
 P_{vu}=\frac{w_{vu}}{d_v},\qquad d_v=\sum_u w_{vu}.
\tag{1}
\]

At fitness two, a dB update at target `v` writes a mutant with probability

\[
 \frac{2P_{vS}}{1+P_{vS}}.
\tag{2}
\]

Let `N` have the fair geometric law

\[
 \Pr(N=q)=2^{-q},\qquad q\geq1,
\tag{3}
\]

and let `U_1,...,U_N` be iid samples from row `P_v`.  Since

\[
 \Pr(U_1,\ldots,U_N\notin S)
 =E(1-P_{vS})^N
 =\frac{1-P_{vS}}{1+P_{vS}},
\tag{4}
\]

the forward update is exactly the additive Boolean map

\[
 x_v\longleftarrow x_{U_1}\vee\cdots\vee x_{U_N}.
\tag{5}
\]

Its transpose sends a dual set `A` to

\[
 A\longmapsto
 \begin{cases}
 (A\setminus\{v\})\cup\{U_1,\ldots,U_N\},&v\in A,\\
 A,&v\notin A.
 \end{cases}
\tag{6}
\]

Use the same graphical marks forward and backward.  Composition of the
one-step transpose identity gives, for every forward mutant set `S` and dual
set `A`,

\[
 \Pr_S(X_t\cap A\ne\varnothing)
 =\Pr_A(S\cap A_t\ne\varnothing).
\tag{7}
\]

The dual never reaches the empty set.  Let `Pi` be its limiting invariant
law from `V` (equivalently the invariant law on its recurrent proper-set
class).  The finite forward chain absorbs almost surely.  Taking `A_0=V`
and then `t\to\infty` in (7) proves the exact representation

\[
 \boxed{
 h(S)=\Pr_{A\sim\Pi}(A\cap S\ne\varnothing),
 }
\tag{8}
\]

where `h(S)` is the forward fixation probability from `S`.

## 2. Exact monotonicity and submodularity

For a fixed nonempty set `A`, define

\[
 c_A(S)=\mathbf1_{\{A\cap S\ne\varnothing\}}.
\tag{9}
\]

This is a coverage function.  It obeys

\[
 c_A(S\cup\{i\})-c_A(S)
 =\mathbf1_{\{A\cap S=\varnothing,\ i\in A\}}\geq0,
\tag{10}
\]

and, for distinct `i,j` outside `S`,

\[
 \begin{split}
 &c_A(S\cup\{i\})+c_A(S\cup\{j\})
       -c_A(S)-c_A(S\cup\{i,j\})\\
 &\hspace{28mm}
 =\mathbf1_{\{A\cap S=\varnothing,\ i,j\in A\}}\geq0.
 \end{split}
\tag{11}
\]

Averaging (10)--(11) under `Pi` proves

\[
 \boxed{h(S\cup\{i\})\geq h(S)}
\tag{12}
\]

and

\[
 \boxed{
 h(S\cup\{i\})+h(S\cup\{j\})
 \geq h(S)+h(S\cup\{i,j\}).
 }
\tag{13}
\]

There is a stronger exact Möbius formula.  For every nonempty named set
`T` disjoint from `S`,

\[
 \boxed{
 (-1)^{|T|+1}\Delta_T h(S)
 =\Pr_\Pi(A\cap S=\varnothing,\ T\subseteq A)\geq0,
 }
\tag{14}
\]

where `Delta_T=prod_(i in T) Delta_i`.  Thus the fixation committor is not
merely submodular: it is a completely alternating normalized coverage
function.

In particular,

\[
 h(\{i\})=\Pr_\Pi(i\in A),\qquad
 h(\{i\})+h(\{j\})-h(\{i,j\})=\Pr_\Pi(i,j\in A).
\tag{15}
\]

The uniform-singleton fixation probability is therefore

\[
 \rho_{\rm dB}(G,2)=\frac1n\sum_i h(\{i\})
 =\frac1n E_\Pi|A|.
\tag{16}
\]

## 3. A natural reversible degree-profile envelope

Normalize the reversible stationary vertex law by

\[
 \pi_i=\frac{d_i}{\sum_jd_j}.
\tag{17}
\]

The complete count-chain harmonic admits the continuous interpolation

\[
 \Phi_n(z)=
 \frac{1-(1+z)2^{-nz}}{1-2^{1-n}},\qquad0\leq z\leq1.
\tag{18}
\]

Indeed, at the lattice points `z=k/n`,

\[
 \Phi_n(k/n)
 =\frac{1-(n+k)/(n2^k)}{1-2^{1-n}},
\tag{19}
\]

the exact complete-graph fixation probability from `k` mutants.  In
particular

\[
 \Phi_n(1/n)
 =\rho_{\rm dB}(K_n,2)
 =\frac{(n-1)2^{n-2}}{n(2^{n-1}-1)}.
\tag{20}
\]

Direct differentiation gives, with `a=n log 2`,

\[
 \Phi_n''(z)
 =\frac{a e^{-az}\{2-a(1+z)\}}{1-2^{1-n}}.
\tag{21}
\]

Thus the function is not even globally concave for every `n`; more
importantly, the aggregate envelope

\[
 \frac1n\sum_i h(\{i\})
 \stackrel{?}{\leq}
 \frac1n\sum_i\Phi_n(\pi_i)
\tag{22}
\]

is false.  The failure below is strict and exact.

## 4. Exact six-vertex refutation

Partition the vertices into cells

\[
 A=\{0,1,3\},\qquad B=\{2,4\},\qquad H=\{5\}.
\]

Give every edge within `A` weight `5`, every edge from `A` to `H` weight
`2`, the edge within `B` weight `73`, and both edges from `B` to `H` weight
`1`.  All other weights vanish.  This is a connected undirected weighted
graph.  Its weighted degrees are

\[
 d_A=12,\qquad d_B=74,\qquad d_H=8,
\]

and hence

\[
 (\pi_i)=\left(
 {1\over16},{1\over16},{37\over96},{1\over16},
 {37\over96},{1\over24}\right).
\tag{23}
\]

The three-count orbit chain has `4*3*2-2=22` transient states.  Solving its
exact rational harmonic system gives

\[
 \boxed{
 \rho_{\rm dB}(G,2)=
 \frac{
 3068195756606417046102333640985779252
 }{
 8357819445634194964176471307640845009
 }
 =0.3671048144272996\ldots .
 }
\tag{24}
\]

To certify the strict failure of (22) without numerical logarithms, put

\[
 \alpha=2^{1/16},\qquad u={10443\over10000}.
\]

Exact integer arithmetic gives `u^16>2`, hence `alpha<u`.  From (18) and
(23),

\[
 \frac16\sum_i\Phi_6(\pi_i)
 ={32\over31}\left[
 1-{1\over6}\left{
 3{17\over16}\alpha^{-6}
 +2{133\over96}\alpha^{-37}
 +{25\over24}\alpha^{-4}
 \right}\right].                                  \tag{25}
\]

Since all coefficients in braces are positive and `alpha<u`, the right
side of (25) is strictly smaller than the rational number obtained by
replacing `alpha` by `u`.  Exact cross multiplication then gives

\[
 \rho_{\rm dB}(G,2)
 -{32\over31}\left[
 1-{1\over6}\left{
 3{17\over16}u^{-6}
 +2{133\over96}u^{-37}
 +{25\over24}u^{-4}
 \right}\right]
 >0.0042.                                             \tag{26}
\]

Equations (25)--(26) prove

\[
 \boxed{
 \rho_{\rm dB}(G,2)
 >\frac16\sum_i\Phi_6(\pi_i),
 }
\tag{27}
\]

so the degree-profile envelope is exactly refuted.  Notice that this graph
still lies below the complete baseline `rho_(K_6)=80/189`; it refutes only
the proposed intermediate theorem, not the universal fitness-two bound.

## 5. Consequence for the live proof

The coverage theorem (8)--(14) is exact and globally valid, but it does not
couple the representing law `Pi` to the reversible stationary masses
`pi_i` sharply enough to compare the mean in (16).  In particular:

1. abstract coverage/submodularity cannot supply the missing extremal step;
2. even the full singleton vector is not bounded by the natural continuous
   complete harmonic evaluated at reversible vertex masses;
3. a successful proof must use the stationarity equations of the
   fair-geometric representing measure, or an equivalent two-labelled
   current/tree identity, in addition to complete alternation.

The exact remaining upper-bound target is unchanged:

\[
 E_\Pi|A|\leq
 \frac{(n-1)2^{n-2}}{2^{n-1}-1}.
\tag{28}
\]

## 6. Rank-summed harmonic edges as a dual/test-set coupling

The useful consequence of complete alternation is not a marginal profile,
but an exact coupling of a stationary dual set with an independent test set.
For `0<=k<=n-1`, put

\[
 \delta_vh(S)=h(S\cup\{v\})-h(S),\qquad v\notin S,
\tag{29}
\]

and define the unweighted and heat-bath-weighted rank sums

\[
 D_k=\sum_{|S|=k,v\notin S}\delta_vh(S),
\qquad
 W_k=\sum_{|S|=k,v\notin S}
 {2P_{vS}\over1+P_{vS}}\delta_vh(S).
\tag{30}
\]

Formula (14) at first order gives

\[
 \delta_vh(S)=
 \Pr_\Pi(v\in A,\ A\cap S=\varnothing).
\tag{31}
\]

Let `H=A^c`.  Tonelli's theorem, applied to the finite nonnegative sum,
therefore gives

\[
 \boxed{
 D_k=E_\Pi\left[|A|{|H|\choose k}\right],
 }
\tag{32}
\]

and

\[
 \boxed{
 W_k=E_\Pi\sum_{v\in A}
 \sum_{\substack{S\subseteq H\\|S|=k}}
 {2P_{vS}\over1+P_{vS}}.
 }
\tag{33}
\]

Thus the rank sum is exactly the joint experiment

1. draw `A` from its stationary fair-geometric law;
2. choose a marked vertex `v in A`;
3. choose a uniform `k`-subset `S` of `A^c`;
4. observe the row mass `P_(vS)`.

No independence between ancestral lineages appears.  Conditional on `A`
and `v`, only the auxiliary test set `S` is sampled.

There is an exact first-moment collapse which isolates the sole signed
quantity.  Write

\[
 I_P(A)=\sum_{v,u\in A}P_{vu},\qquad
 Z_P(A)={|A|(|A|-1)\over n-1}-I_P(A).
\tag{34}
\]

If `a=|A|` and `h=n-a`, uniform `k`-subset sampling gives

\[
 \sum_{v\in A}\sum_{\substack{S\subseteq A^c\\|S|=k}}
 \left(P_{vS}-{k\over n-1}\right)
 ={k\over h}{h\choose k}Z_P(A).
\tag{35}
\]

Indeed, each hole belongs to exactly `{h-1 choose k-1}` test sets, while

\[
 \sum_{v\in A,u\notin A}P_{vu}=|A|-I_P(A).
\]

For an undirected weighted graph, the apparent oriented term in (34) is the
symmetric internal-edge deficit

\[
 \boxed{
 Z_P(A)=\sum_{\{u,v\}\subseteq A}
 \left\{{2\over n-1}-w_{uv}
 \left({1\over d_u}+{1\over d_v}\right)\right\}.
 }
\tag{36}
\]

In particular its uniform average vanishes separately on every rank.

Finally use the exact tangent remainder, for `q(x)=2x/(1+x)`,

\[
 q(x)-q(b)={2(x-b)\over(1+b)^2}
 -{2(x-b)^2\over(1+b)^2(1+x)}.
\tag{37}
\]

Let `c_k>0` be the complete killed-Green edge weights and put

\[
 U_h=\sum_{k=1}^h c_k{2(n-1)^2\over(n-1+k)^2}
 {h-1\choose k-1}.
\tag{38}
\]

Then (32)--(37) give the exact comparison

\[
 \boxed{
 \rho_{\rm dB}(G,2)-\rho_{\rm dB}(K_n,2)
 =E_\Pi[U_{|A^c|}Z_P(A)]-\mathcal V_P,
 }
\tag{39}
\]

where

\[
 \mathcal V_P=
 E_\Pi\sum_{v\in A}\sum_{k=1}^{|A^c|}
 c_k{2\over(1+k/(n-1))^2}
 \sum_{\substack{S\subseteq A^c\\|S|=k}}
 {\{P_{vS}-k/(n-1)\}^2\over1+P_{vS}}\ge0.
\tag{40}
\]

This identifies the proof-first frontier without another marginal guess.
The exact universal upper bound is implied, and in this Green formulation
is equivalent, to the named **stationary internal-edge deficit inequality**

\[
 \boxed{
 E_\Pi[U_{|A^c|}Z_P(A)]\le\mathcal V_P.
 }
\tag{SID}
\]

Both sides of `(SID)` arise from the same joint law `(A,v,S)`: the left is
its centered first row-mass moment after the reversible internal-edge
collapse (35)--(36), and the right is its full positive concavity remainder.
The left side is not pointwise nonpositive, so a proof must use stationarity
to convert its rank-centered internal-edge deficit into a global two-copy,
current, or tree cancellation.  Abstract submodularity alone stops at
(31)--(33).

## 7. Exact stationary generator of the internal-edge deficit

The stationarity requested by `(SID)` can be applied directly to `Z_P`.
This gives a closed pair-renewal identity, but it also exposes a precise
obstruction to the most immediate two-copy-square argument.

Put `N=n-1` and, using reversibility of the original graph, define the
symmetric original-edge discrepancy

\[
 e_{ij}={2\over N}-w_{ij}\left({1\over d_i}+{1\over d_j}\right)
       ={2\over N}-P_{ij}-P_{ji}.                         \tag{41}
\]

Thus `Z_P(A)=sum_{\{i,j\}\subseteq A}e_{ij}`.  Fix `v in A`, put
`B=A\setminus\{v\}` and `H=A^c`, and let `J\subseteq H` be the set of
holes hit at least once by the fair-geometric row-`v` burst.  The output is
`A'=B union J`.  At the event level,

\[
\boxed{
 Z_P(A')-Z_P(A)
 =-\sum_{x\in B}e_{vx}
  +\sum_{i\in J}\sum_{x\in B}e_{ix}
  +\sum_{\{i,j\}\subseteq J}e_{ij}.}                    \tag{42}
\]

This is the point at which an edge decomposition is forced: it is simply
the deletion and creation formula for the quadratic set statistic `Z_P`.
No sign is assigned to an individual `e_ij`.

Write again `q(x)=2x/(1+x)`.  The one- and two-hole hit probabilities of
the burst are

\[
 b_{vi}=q(P_{vi}),                                        \tag{43}
\]

and

\[
\begin{split}
 b_{v,ij}
 &=q(P_{vi})+q(P_{vj})-q(P_{vi}+P_{vj})\\
 &={2P_{vi}P_{vj}(2+P_{vi}+P_{vj})\over
 (1+P_{vi})(1+P_{vj})(1+P_{vi}+P_{vj})}\geq0.            \tag{44}
\end{split}
\]

Consequently, for the dual generator normalized so that each occupied
target fires at rate one, define

\[
 C_1(A)=\sum_{v\in A}\sum_{i\in H}b_{vi}
              \sum_{x\in A\setminus\{v\}}e_{ix},        \tag{45}
\]

\[
 C_2(A)=\sum_{v\in A}\sum_{\{i,j\}\subseteq H}
              b_{v,ij}e_{ij}.                            \tag{46}
\]

Summing the deletion term in `(42)` counts every internal edge twice, so
the exact generator law is

\[
\boxed{\mathcal L Z_P(A)=-2Z_P(A)+C_1(A)+C_2(A).}        \tag{47}
\]

Stationarity of `Pi` therefore proves the pair-renewal balance

\[
\boxed{2E_\Pi Z_P=E_\Pi(C_1+C_2).}                       \tag{48}
\]

This is a genuine consequence of the full dual law, not a fixed-rank
average.  It expresses the internal deficit removed when an occupied
target is deleted as the deficit of the cross and hole--hole pairs created
by the same burst.

### 7.1 The rank-weighted law and its exact commutator

For the specific Green weight `U_h` in `(38)`, let `h=|A^c|`, and after an
effective burst write `h'=|(A')^c|`.  The only additional term caused by
the rank weight is the exact commutator

\[
 \mathcal R_U(A)=\sum_{v\in A}
 E_v\left[(U_{h'}-U_h)Z_P(A')\right].                    \tag{49}
\]

The product rule, with the second factor evaluated at the output in the
commutator, gives

\[
 \mathcal L(U_hZ_P)
 =U_h\mathcal LZ_P+\mathcal R_U.                         \tag{50}
\]

Combining `(47)` with stationarity yields the exact weighted renewal law

\[
\boxed{
 2E_\Pi[U_hZ_P]
 =E_\Pi[U_h(C_1+C_2)+\mathcal R_U].}                     \tag{51}
\]

Thus `(SID)` is equivalently

\[
 {1\over2}E_\Pi[U_h(C_1+C_2)+\mathcal R_U]
 \leq\mathcal V_P.                                      \tag{52}
\]

Formula `(52)` is the minimal identity left by direct stationarity of the
internal-edge deficit.  In particular, it retains the change in rank under
a burst; replacing `U_(h')` by `U_h` is not valid.

### 7.2 Why ordinary stationary-flow symmetrization is not yet a square

Although the original vertex kernel is reversible, the geometric-union
set chain generally is not.  This distinction is already visible in the
commutator in `(49)`.  Let `Q(A,B)` be the off-diagonal dual generator and
`F_AB=Pi(A)Q(A,B)` its stationary directed flow.  Choose any ordering of
the proper nonempty sets and, for `A<B`, put

\[
 s_{AB}={F_{AB}+F_{BA}\over2},\qquad
 j_{AB}=F_{AB}-F_{BA}.                                  \tag{53}
\]

With `Delta U=U_(h(B))-U_(h(A))` and
`Delta Z=Z_P(B)-Z_P(A)`, exact flow symmetrization gives

\[
 E_\Pi[U_h\mathcal LZ_P]
 =-\mathcal D_{UZ}+\mathcal C_{UZ},                     \tag{54}
\]

where

\[
 \mathcal D_{UZ}=\sum_{A<B}s_{AB}\,\Delta U\,\Delta Z,
 \qquad
 \mathcal C_{UZ}={1\over2}\sum_{A<B}j_{AB}
       \{U_{h(A)}+U_{h(B)}\}\Delta Z.                  \tag{55}
\]

Hence `E_Pi R_U=D_UZ-C_UZ`, and `(51)` becomes

\[
\boxed{
 2E_\Pi[U_hZ_P]
 =E_\Pi[U_h(C_1+C_2)]+\mathcal D_{UZ}-\mathcal C_{UZ}.} \tag{56}
\]

Neither term in `(55)` has the hoped-for automatic sign.  On the weighted
path `0--1--2` with consecutive edge weights `(1,2)`, exact rational
arithmetic gives

\[
 \mathcal D_{UZ}=-{13\over5400},\qquad
 \mathcal C_{UZ}={41\over5400},\qquad
 E_\Pi[U_h\mathcal LZ_P]={1\over100}.                    \tag{57}
\]

On the regular weighted `K_4` with edge weights

\[
 (w_{01},w_{02},w_{03},w_{12},w_{13},w_{23})
 =(1,1,2,2,1,1),
\]

one instead has

\[
 \mathcal D_{UZ}={43\over34440},\qquad
 \mathcal C_{UZ}={97\over57400},\qquad
 E_\Pi[U_h\mathcal LZ_P]={19\over43050}.                \tag{58}
\]

Thus the symmetric mixed Dirichlet term changes sign, while the
circulation term is strictly nonzero even on a regular original graph.
This exactly rules out treating `(54)` as a reversible carré-du-champ or
as a nonnegative two-copy square.  It does **not** refute `(SID)`: the two
graphs have respectively

\[
 \mathcal V_P-E_\Pi[U_hZ_P]={2\over45},\qquad
 \mathcal V_P-E_\Pi[U_hZ_P]={1\over574}>0.               \tag{59}
\]

The surviving obligation is therefore the circulation-corrected current
inequality obtained by substituting `(56)` into `(SID)`.  Any square
closure must use more than reversibility of the original edge kernel: it
must absorb the dual circulation and the signed mixed rank/internal-edge
current together with the subset-mass dispersion `(40)`.
