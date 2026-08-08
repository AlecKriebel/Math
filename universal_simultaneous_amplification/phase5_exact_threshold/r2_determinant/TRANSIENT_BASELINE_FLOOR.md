# The transient baseline-floor route at fitness two

Date: 2026-08-08 (America/Los_Angeles)

## Status

This note isolates a new sufficient route to the universal fitness-two
bound.  It is weaker than the previously named stationary-promotion lemma
and survives all current hostile tests.

The following statements are **PROVED** here.

1. A baseline floor at every finite time implies the true stationary
   collision inequality by Cesaro convergence.
2. The floor is exactly a quenched-versus-annealed inequality under random
   vertex relabelling.
3. Its first nontrivial grouped path sums are positive at times two and
   three on every directed triangle.  The time-three increment has an
   explicit coefficientwise certificate.
4. Individual transverse excursions can be negative, even for a reversible
   weighted triangle.  Therefore any proof must group all paths of a fixed
   length (or a still larger positive packet).

Complete-ray Bernstein positivity and the boundary searches below are
**EXACT FINITE COMPUTATIONS**.  They are not a universal proof.  The
all-order transient floor remains **OPEN**.

## 1. The conjecture and why it is enough

Let `K_P` be the forward active chain on

\[
 \mathcal Y=\{(B,v):\varnothing\ne B\subseteq V\setminus\{v\}\},
\]

let

\[
 H(B,v)={1\over |B|},\qquad
 \nu_0(B,v)={|B|\over n(n-1)2^{n-2}},
\]

and put

\[
 a_t(P)=\nu_0K_P^tH,\qquad
 a_0={2^{n-1}-1\over(n-1)2^{n-2}}={1\over m_K}.       \tag{1}
\]

The proposed transient baseline floor is

\[
 \boxed{a_t(P)\ge a_0\quad\hbox{for every integer }t\ge0.}          \tag{TF}
\]

It is strictly weaker than promotion.  Promotion asks that the Cesaro
limit be at least `a_2(P)`, whereas `(TF)` only compares every term with
`a_0`.  Since every finite active chain has

\[
 \lim_{T\to\infty}{1\over T}\sum_{t<T}a_t(P)={1\over m(P)},         \tag{2}
\]

`(TF)` would prove

\[
 {1\over m(P)}\ge {1\over m_K},\qquad m(P)\le m_K,                 \tag{3}
\]

which is exactly death--Birth complete-graph maximality at fitness two.
No stationary-promotion equivalence is used.

## 2. Quenched versus annealed

For a permutation `sigma` of the vertices, let `P^sigma` be the conjugate
kernel and let `U_sigma` relabel active states.  Then

\[
 K_{P^\sigma}=U_\sigma^{-1}K_PU_\sigma,
 \qquad \nu_0U_\sigma=\nu_0,
 \qquad U_\sigma H=H.                               \tag{4}
\]

The active kernel is linear in `P`, and averaging all conjugates of a
loopless row-stochastic kernel makes every off-diagonal entry `1/(n-1)`.
Consequently

\[
 E_\sigma K_{P^\sigma}=K_0.                         \tag{5}
\]

Equations `(4)`--`(5)` turn `(TF)` into the exact matrix inequality

\[
 \boxed{
 E_\sigma\,\nu_0K_{P^\sigma}^{,t}H
 \ \ge\
 \nu_0(E_\sigma K_{P^\sigma})^tH.}                 \tag{6}
\]

The left side fixes one random labelling for the entire history; the right
side refreshes it independently at every step.  Thus the missing theorem is
a quenched-versus-annealed collision inequality.  The proved two-step SOS is
the first nontrivial case.

## 3. Exact rank/transverse expansion

Let `S` average functions uniformly within each active rank and put
`T=I-S`.  Direct subset averaging gives

\[
 SK_PS=SK_0S=:R.                                    \tag{7}
\]

Write the four blocks

\[
 R=SK_PS,\qquad B=SK_PT,\qquad C=TK_PS,\qquad D=TK_PT.             \tag{8}
\]

Since `nu_0` and `H` lie in the rank sector and
`nu_0R^tH=a_0`, exact expansion gives

\[
 a_2-a_0=\nu_0BCH,                                  \tag{9}
\]

\[
 \boxed{
 a_3-a_0=\nu_0(RBC+BCR+BDC)H.}                     \tag{10}
\]

The first expression is the known two-step SOS.  The three terms in `(10)`
cannot be certified separately.  For the reversible triangle with edge
weights

\[
 (w_{01},w_{02},w_{12})=(1,10,10),
\]

they are, in the order displayed,

\[
 {27\over968},\qquad {27\over1936},\qquad
 -{135\over85184}.                                  \tag{11}
\]

Their grouped sum is

\[
 {3429\over85184}>0.                                \tag{12}
\]

There is an even smaller failure of termwise positivity.  If
`Delta=K_P-K_0`, the reversible triangle `(1,2,2)` has

\[
 \nu_0\Delta K_0^2\Delta H=-{1\over6912}.           \tag{13}
\]

Thus neither single excursions nor single two-colour words are the desired
certificate.  Fixed-length grouping is mathematically essential.

## 4. A complete directed-triangle certificate at time three

Every directed loopless three-vertex kernel has the form

\[
 P=\begin{pmatrix}
 0&x&1-x\\
 y&0&1-y\\
 z&1-z&0
 \end{pmatrix},\qquad 0\le x,y,z\le1.               \tag{14}
\]

Put `X=x-1/2`, `Y=y-1/2`, and `Z=z-1/2`.  Exact multiplication of the
nine-state active chain gives

\[
 \boxed{a_2-a_0={X^2+Y^2+Z^2\over12},}              \tag{15}
\]

and

\[
 \boxed{
 a_3-a_2={1\over16}\left[
 (y+z)X^2+(1+x-z)Y^2+(2-x-y)Z^2
 \right].}                                         \tag{16}
\]

Every coefficient in `(16)` is nonnegative on the unit cube.  If the sum
vanishes, the three boundary possibilities for a zero coefficient force a
different term to be positive unless `X=Y=Z=0`.  Hence

\[
 a_3>a_2>a_0
\]

for every noncomplete directed triangle.  Formula `(16)` is a genuine
grouped two-replica certificate, not a sampled numerical inequality.

The same calculation gives a full ray-convexity theorem in order three.
For `P_alpha=P_0+alpha(P-P_0)`, put

\[
 S=X^2+Y^2+Z^2,
 \qquad T=(X+Y)(X-Z)(Y+Z).
\]

Then

\[
 A_{3,P}(\alpha)={\alpha^2\over48}\{7S+3\alpha T\}.               \tag{17}
\]

On the cube `|X|,|Y|,|Z|<=1/2`, one has `T>=-S/2`.  Here is a short
direct proof.  Put `b=X-Z` and `c=Y+Z`; minimizing `S` over the remaining
free coordinate gives

\[
 S\ge {2\over3}(b^2+bc+c^2).
\]

If `b,c<=0`, write `b=-p,c=-q`; the cube gives `p+q<=1`, and
`3pq(p+q)<=p^2+pq+q^2`.  If they have opposite signs and `T<0`, write
`b=p,c=-q`, `p>= q`; then `p<=1` and
`3pq(p-q)<=p^2-pq+q^2`.  The other signs are symmetric.  Differentiating
`(17)` now gives

\[
 {1\over2}A_{3,P}''(\alpha)
 ={7S+9\alpha T\over48}\ge {5S\over96}>0            \tag{18}
\]

off the complete kernel.  This convexity is special to the short triangle
history; it fails in higher order as recorded below.

## 5. Complete-ray Bernstein coefficients

For an arbitrary kernel define

\[
 K_\alpha=(1-\alpha)K_0+\alpha K_P,
\qquad
 A_{t,P}(\alpha)=\nu_0K_\alpha^tH-a_0.              \tag{19}
\]

This is a polynomial of degree at most `t`.  In its degree-`t` Bernstein
basis write

\[
 A_{t,P}(\alpha)=
 \sum_{j=0}^t\binom tj b_{t,j}(P)
 \alpha^j(1-\alpha)^{t-j}.                          \tag{20}
\]

The coefficient `b_(t,j)` is the reward excess averaged over all histories
with exactly `j` actual-coloured updates and `t-j` complete-coloured
updates.  Equation `(7)` proves

\[
 b_{t,0}=b_{t,1}=0.                                 \tag{21}
\]

This interpretation has an exact vector recurrence.  If `V_(s,j)` is the
degree-`s` Bernstein control vector for `K_alpha^s H`, set `V_(0,0)=H` and
zero outside `0<=j<=s`.  Then

\[
 \boxed{
 V_{s+1,j}={s+1-j\over s+1}K_0V_{s,j}
          +{j\over s+1}K_PV_{s,j-1}.}               \tag{22}
\]

Thus `b_(t,j)=nu_0 V_(t,j)-a_0`, and `(22)` literally averages all words
with a fixed number of actual updates.  It is also a stable exact way to
compute the controls without high-degree interpolation.

The exact verifier finds every remaining coefficient nonnegative on seeded
reversible and directed rational kernels through order five and time thirty.
It also checks the baseline floor directly on every deterministic loopless
row map at orders three and four, and every equal-weight two-neighbour row
support at order four, through time fifty.

These are exact finite computations.  The attractive universal conjecture

\[
 \boxed{b_{t,j}(P)\ge0\quad(2\le j\le t)}           \tag{23}
\]

would imply `(TF)` immediately.  It is stronger than the endpoint floor and
remains **OPEN**.

Two exact hostile checks delimit the claim.

1. Direct Bernstein positivity in the independent row-simplex coordinates
   is false already for the directed order-four, time-three polynomial.  At
   product-simplex multi-index

   ```text
   ((0,0,3),(0,1,2),(1,1,1),(1,1,1))
   ```

   the degree-three-elevated control coefficient is `-11/5184`.  Even the
   completely symmetric control index has coefficient `-187/3456`.  These
   are control coefficients, not negative values, but they rule out a raw
   simplex-Bernstein proof.
2. Complete-ray convexity fails.  On the reversible five-vertex graph with
   lexicographic edge weights

   ```text
   (2,1233002,865,13228210,1106078,12,1130,56225120,385413,2)
   ```

   exact derivative propagation gives
   `A_(18,P)''(1)<0` (approximately `-0.0312589498239`).  Nevertheless every
   degree-18 complete-ray Bernstein coefficient remains nonnegative, with
   `b_0=b_1=0` and every `b_j>0` for `j>=2`.

Thus it is the flexible complete-ray grouping `(20)`, not raw product
coefficients or convexity, that survives.

## 6. Hostile numerical optimization and remaining gap

Boundary kernels are not benign omitted cases: deterministic maps and sparse
rows are included in the exact verifier.  Separately, high-precision global
searches over directed and reversible kernels of orders three and four, with
logits allowed to approach the boundary, found no value below `a_0` for
times two through twelve.  This is **NUMERICAL EVIDENCE ONLY**.

The proof obligation is now precise: prove `(TF)`, or preferably the
coefficientwise strengthening `(23)`, by a two-replica/history grouping that
allows the cancellations in `(10)`--`(13)`.  A termwise excursion proof is
falsified.  The most plausible remaining objects are a reflection-positive
pair-history expansion or a tree-indexed homomorphism inequality comparing
one fixed random labelling with independently refreshed labellings.
