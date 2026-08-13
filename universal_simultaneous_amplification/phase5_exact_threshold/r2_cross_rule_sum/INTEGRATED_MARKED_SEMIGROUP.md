# The integrated marked-semigroup recurrence at fitness two

Date: 2026-08-13 (America/Los_Angeles)

No literature search or external communication was used.

## 1. Status

This note keeps the common marked construction at the integrated level.  It
proves an exact recurrence for

\[
 a_t=q_LM_P^t\psi,
\]

and isolates the stationary comparison as one antisymmetrized two-step
current.  For every weighted three-vertex path it also proves the finite
midpoint lower bound

\[
 \boxed{{a_1+a_2\over2}\ge {m_L\over b_3d_3}.}              \tag{1}
\]

The tempting other half of a two-sign sandwich is **EXACTLY FALSE**, already
on the unweighted path:

\[
 {1\over m_D}-{a_1+a_2\over2}=-{9\over6160}<0.              \tag{2}
\]

Thus (1) cannot be promoted to the decisive product inequality by separately
proving that the stationary marked value exceeds the midpoint.  The surviving
proof target must keep the finite midpoint surplus and the stationary current
summed.  A direct calculation below nevertheless proves `PAPT_3` for every
weighted three-vertex path.

## 2. Active factorization and exact recurrence

Let

\[
 \mathcal X=\{(C,v):v\notin C\},\qquad
 \mathcal Y=\{(B,v):\varnothing\ne B\subseteq V\setminus\{v\}\}.
\]

Write `A_P` for the channel which samples `i` from row `P_v` and sends
`(C,v)` to `(C union {i},v)`.  Write `R` for the fair channel which either
continues with the same target or deletes a uniformly chosen `w` from `B`
and retargets at `w`.  Then

\[
 M_P=A_PR,\qquad K_P=RA_P.                                  \tag{3}
\]

For `H(B,v)=1/|B|`, the alternating inverse-rank recurrence gives

\[
                            R\psi=H.                         \tag{4}
\]

The complemented occupied-target Palm law of the stationary `L` dual is

\[
 q_L(C,v)={\pi_L(V\setminus C)\over m_L}.
\]

Put `nu_L=q_LA_P`.  Directly from (3)--(4), after using `L` stationarity to
construct `q_L`,

\[
 \boxed{a_t=\nu_LK_P^{t-1}H\quad(t\ge1).}                   \tag{5}
\]

If

\[
 \vartheta={m_L\over b_nd_n},\qquad
 \overline H={I+K_P\over2}H,
\]

define

\[
 s_t={a_t+a_{t+1}\over2}-\vartheta
     =\nu_LK_P^{t-1}\overline H-\vartheta.                  \tag{6}
\]

It obeys the exact integrated recurrence

\[
 \boxed{s_{t+1}-s_t={1\over2}\nu_LK_P^{t-1}(K_P^2-I)H.}    \tag{7}
\]

Let `nu_D` be the invariant probability law of `K_P`, so

\[
                         \nu_DH={1\over m_D}=:c_D.           \tag{8}
\]

Let `g` solve

\[
 (I-K_P)g=H-c_D\mathbf1.                                    \tag{9}
\]

Because

\[
 \overline H=c_D\mathbf1+{1\over2}(I-K_P^2)g,
\]

the stationary-versus-midpoint remainder is exactly

\[
 \boxed{c_D-{a_1+a_2\over2}={1\over2}\nu_L(K_P^2-I)g.}    \tag{10}
\]

Writing `F_yz=nu_L(y)K_P^2(y,z)`, it also has the literal current form

\[
 \boxed{
 c_D-{a_1+a_2\over2}
 ={1\over4}\sum_{y,z}(F_{yz}-F_{zy})\{g(z)-g(y)\}.}         \tag{11}
\]

The exact product gap is therefore the **combined** identity

\[
 \boxed{
 {1\over m_D}-{m_L\over b_nd_n}
 =\left\{\nu_L\overline H-{m_L\over b_nd_n}\right\}
   +{1\over2}\nu_L(K_P^2-I)g.}                              \tag{12}
\]

Equation (2) proves that the current in (12) can be negative.  It must stay
coupled to the finite midpoint surplus.

For reference, the active initial law has the exact local formula

\[
 m_L\nu_L(B,v)
 =P_v(B)\pi_L(V\setminus B)
  +\sum_{i\in B}P_{vi}\pi_L((V\setminus B)\cup\{i\}).       \tag{13}
\]

This is where `L` stationarity enters the marked history; an arbitrary
initial marked law does not retain the cross-rule structure.

## 3. Exact weighted-path formulas

Consider a weighted path with centre `1`.  After scaling its two positive
edge conductances,

\[
 P=\begin{pmatrix}
 0&1&0\\
 p&0&1-p\\
 0&1&0
 \end{pmatrix},\qquad 0<p<1.
\]

Put

\[
                         u=p(1-p),\qquad 0<u\le {1\over4}.   \tag{14}
\]

Exact symbolic stationary solves give

\[
 m_L={4u^2+46u+4\over4u^2+19u+4},                            \tag{15}
\]

\[
 {1\over m_D}={u+2\over3u+2},                               \tag{16}
\]

and the first two integrated marked values are

\[
 a_1={-20u^2+217u+10\over10(2u^2+23u+2)},                   \tag{17}
\]

\[
 a_2={3(-7u^2+29u+2)\over4(2u^2+23u+2)}.                    \tag{18}
\]

Since `b_3d_3=(12/7)(4/3)=16/7`, the midpoint surplus is

\[
 {a_1+a_2\over2}-{m_L\over b_3d_3}
 ={3N(u)\over
  40(2u^2+23u+2)(4u^2+19u+4)},                              \tag{19}
\]

where

\[
 N(u)=20+402u-888u^2-833u^3-240u^4.                         \tag{20}
\]

For `0<=u<=1/4`,

\[
 888u^2+833u^3+240u^4
 \le\left(222+{833\over16}+{15\over4}\right)u
 ={4445\over16}u.
\]

Therefore

\[
 N(u)\ge20+{1987\over16}u>0,                                \tag{21}
\]

which proves (1).

The stationary current itself is

\[
 {1\over m_D}-{a_1+a_2\over2}
 ={(5u+1)(103u^2-268u+60)\over
  40(3u+2)(2u^2+23u+2)}.                                    \tag{22}
\]

At the unweighted path `p=1/2`, hence `u=1/4`, equations (17)--(18) give

\[
 a_1={4\over5},\qquad a_2={47\over56},\qquad
 {a_1+a_2\over2}={459\over560},\qquad {1\over m_D}={9\over11}.
\]

Their difference is (2), exactly refuting a universal
stationary-over-midpoint sign.

## 4. Direct `PAPT_3` theorem

Keeping the two summands in (12) together yields directly

\[
 {1\over m_D}-{m_L\over b_3d_3}
 ={36-28u-295u^2-10u^3\over
   8(3u+2)(4u^2+19u+4)}.                                    \tag{23}
\]

For `0<=u<=1/4`,

\[
 28u+295u^2+10u^3
 \le 7+{295\over16}+{10\over64}
 ={819\over32}<36.                                          \tag{24}
\]

Thus (23) is positive.  We have proved:

> **Theorem (weighted-path `PAPT_3`).**  For every connected weighted
> three-vertex path at fitness two,
> `m_Lm_D<b_3d_3`.  Equivalently, Bd and dB cannot both strictly amplify on
> that graph.

The proof uses the combined identity (12).  The finite midpoint surplus is
positive, but the accompanying stationary current need not be.

## 5. Scope and remaining identity

Equations (5)--(13) are exact for every graph.  Equations (14)--(24) prove
only the weighted-three-path theorem and the minimal failure of the split
stationary sign.  The all-graph task is the combined sign

\[
 \boxed{
 \left\{\nu_L\overline H-{m_L\over b_nd_n}\right\}
 +{1\over2}\nu_L(K_P^2-I)g\ge0.}                             \tag{25}
\]

No separate sign for either term in (25) is available, and the second is
now exactly known to be negative on the smallest nontrivial unweighted
path.  Pointwise product-Poisson corrections are not used.

## 6. Verification

Run

```text
PYTHONDONTWRITEBYTECODE=1 ../../../../.venv/bin/python -B verify_integrated_marked_semigroup.py
```

The verifier constructs `L`, `M_P`, and `K_P` symbolically, solves both
invariant laws, checks (5)--(13), and proves the rational identities
(15)--(23) over `QQ(u)`.  The interval signs use only the elementary bounds
(21) and (24).
