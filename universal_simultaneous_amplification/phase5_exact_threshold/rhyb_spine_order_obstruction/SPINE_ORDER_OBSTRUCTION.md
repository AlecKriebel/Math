# A two-cycle obstruction to endpoint-spine order proofs

Date: 2026-08-13 (America/Los_Angeles)

No graph search, kernel search, parameter search, numerical optimization,
literature search, or external communication was used.

## 1. Status

**PROVED ROUTE OBSTRUCTION; THE ENDPOINT SIGN REMAINS OPEN.**  The linked
spine reduction writes the outstanding endpoint gap as

\[
 G=\langle A,K(x-1)\rangle_m
  =\langle A,x-1\rangle_m-\mathcal E_K(A,x),             \tag{1}
\]

where

\[
 \mathcal E_K(A,x)
 ={1\over2}\sum_{i,j}m_iK_{ij}(A_i-A_j)(x_i-x_j).       \tag{2}
\]

A natural proof attempt is to order the endpoint label `A` with the ground
ratio `x`, or to show that the spine average `KA` preserves an order with
`x-1`.  The exact family below shows that the endpoint equations do not
provide either favorable conclusion.  Throughout the whole interval

\[
                         {3\over2}\le r\le {151\over100},
\]

it has all three properties

\[
 \begin{array}{ll}
 \text{(i)}&x_0-1\text{ and }x_1-1\text{ have opposite signs},\\
 \text{(ii)}&(A_0-A_1)(x_0-x_1)>0,\\
 \text{(iii)}&((KA)_0-(KA)_1)(x_0-x_1)<0,
 \end{array}                                             \tag{3}
\]

while nevertheless

\[
                              G>0.                       \tag{4}
\]

Thus even the strongest possible two-point one-crossing does not make the
spine preserve the relevant monotone order.  Edgewise antitonicity cannot
make (2) nonpositive either: in this family (2) is strictly positive.

This is only a stopping certificate for that qualitative monotonicity
architecture.  It does **not** rule out a quantitative comparison
\(\mathcal E_K(A,x)\leq\langle A,x-1\rangle_m\) that uses more of the
linked endpoint equations, and
it does not prove or refute the universal endpoint inequality.

## 2. Exact endpoint family

Fix `kappa>0`, `kappa!=1`, and put

\[
 P=\begin{pmatrix}0&1\\1&0\end{pmatrix},\qquad
 \pi={1\over2}(1,1),\qquad
 a={2\over1+\kappa}(1,\kappa),\qquad
 p={1\over1+\kappa}(1,\kappa).                          \tag{5}
\]

Then

\[
 R=D_a^{-1}PD_a=\begin{pmatrix}0&\kappa\\\kappa^{-1}&0\end{pmatrix},
 \qquad t={Pa\over a}=(\kappa,\kappa^{-1}).             \tag{6}
\]

The positive Bd and dB endpoints are

\[
 q=\left(
 {\kappa r+1\over r(\kappa+r)},
 {\kappa+r\over r(\kappa r+1)}
 \right),                                               \tag{7}
\]

\[
 s=\left(
 {\kappa(r-1)(r+1)\over r(\kappa r+1)},
 {(r-1)(r+1)\over r(\kappa+r)}
 \right).                                               \tag{8}
\]

Writing `b=1-q` and `h=1-s`, direct substitution gives

\[
                       tb=rqPb,\qquad s=rhRs.            \tag{9}
\]

Let `X=(r-1)q`, `h1=(1+rRX)^{-1}`, `v=as`, and use the linked
spine definitions

\[
 K_{ij}={P_{ij}v_j\over ((Pv)_i/v_i)v_i},\qquad
 x={X\over s},\qquad A={rhh_1\over as}.                 \tag{10}
\]

Because `P` is the deterministic swap, its Doob transform is again the
swap:

\[
                              K=P.                      \tag{11}
\]

## 3. One crossing and order reversal

The two ground ratios are

\[
 x_0={(\kappa r+1)^2\over
              \kappa(\kappa+r)(r+1)},\qquad
 x_1={(\kappa+r)^2\over
              (r+1)(\kappa r+1)}.                      \tag{12}
\]

Their displacements from one factor as

\[
 x_0-1={(\kappa-1)\{\kappa(r^2-r-1)-1\}\over
              \kappa(\kappa+r)(r+1)},                  \tag{13}
\]

\[
 x_1-1=-{(\kappa-1)\{-\kappa+r^2-r-1\}\over
              (r+1)(\kappa r+1)}.                      \tag{14}
\]

On the stated fitness interval, `r^2-r-1<0`.  Hence `x0-1` has sign
`-sign(kappa-1)`, whereas `x1-1` has sign `sign(kappa-1)`.  This proves
the strict one-crossing claim.

The label differences have the exact forms

\[
 x_0-x_1={(\kappa-1)(\kappa+1)
   \{-\kappa^2+\kappa r^3-3\kappa r-1\}
  \over
  \kappa(\kappa+r)(r+1)(\kappa r+1)},                  \tag{15}
\]

and

\[
 A_0-A_1=-{r(\kappa-1)(\kappa+1)(\kappa+r)(\kappa r+1)
                  (\kappa^2+\kappa r+2\kappa+1)
 \over
 2\kappa(r+1)(\kappa^2+\kappa r^2+r-1)
       \{\kappa^2(r-1)+\kappa r^2+1\}}.                \tag{16}
\]

Since `r^3-3r<0`, the brace in (15) is negative.  Every other
unlabelled factor in (15)--(16) is positive.  Consequently both
differences have sign `-sign(kappa-1)`, proving

\[
                       (A_0-A_1)(x_0-x_1)>0.             \tag{17}
\]

The only undirected spine edge therefore makes
\(\mathcal E_K(A,x)>0\).  On the other hand, (11) gives

\[
                       (KA)_0-(KA)_1=-(A_0-A_1),         \tag{18}
\]

so the smoothed label has the strictly opposite order:

\[
                \{(KA)_0-(KA)_1\}(x_0-x_1)<0.           \tag{19}
\]

## 4. The true gap stays positive

The exact endpoint gap is

\[
 G={\kappa(\kappa-1)^2(r-1)
        \{C_2(r)(\kappa^2+1)+C_1(r)\kappa\}
 \over
 r(\kappa+r)(\kappa r+1)(\kappa^2+\kappa r^2+r-1)
       \{\kappa^2(r-1)+\kappa r^2+1\}},                \tag{20}
\]

where

\[
 C_2(r)=r^4-2r^3+r+1,
 \qquad
 C_1(r)=r^5-r^4-3r^2+3r+2.                             \tag{21}
\]

Put `u=r-3/2`, so `0<=u<=1/100`.  Then

\[
 C_2={13\over16}+u+{9\over2}u^2+4u^3+u^4>0,            \tag{22}
\]

\[
 C_1={73\over32}+{93\over16}u+{69\over4}u^2
             +{33\over2}u^3+{13\over2}u^4+u^5>0.       \tag{23}
\]

Every denominator factor in (20) is positive.  Equations (20)--(23)
prove `G>0` for every admitted `r,kappa`.  The endpoint inequality thus
survives precisely where the proposed qualitative spine-order mechanism
fails.

## 5. Exact replay

From the repository root run

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B \
  universal_simultaneous_amplification/phase5_exact_threshold/\
rhyb_spine_order_obstruction/verify_spine_order_obstruction.py
```

The replay reconstructs both endpoints and the Doob spine, verifies the
linked gap identity, factors every order difference, and checks the
interval signs by exact rational arithmetic.
