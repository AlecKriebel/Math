# Exact \(\delta=2\) Hilbert--Burch stratification

**Scope.**  This note concerns only the binary top row
\[
H_4=h(p,q)(p^2,q^2,0),\qquad
R=(H_3)_3\in\mathbb C[p,q]_3.
\]
It classifies the two possible Hilbert--Burch shapes at exact
\(\delta=2\).  It does not assert that any top-identity survivor is a
Keller map.

**Status.**  Exact symbolic derivation and independent PARI/GP replay
pass.  This note is not peer reviewed.  The checks are evidence about the
encoded algebra, not peer review.

## 1. Statement

Put
\[
\begin{aligned}
P&=hp^2,& Q&=hq^2,\\
\alpha&=J(Q,R),&
\beta&=-J(P,R),&
\gamma&=J(P,Q)=8h^2pq,
\end{aligned}
\]
and
\[
g=\gcd(\alpha,\beta,\gamma),\qquad \delta=\deg g.
\]
Assume that \(\alpha,\beta\) are constant-linearly independent.  At
\(\delta=2\), the abstract Hilbert--Burch calculation leaves precisely
\[
\{k_1,k_2\}=\{1,1\}\quad\hbox{or}\quad\{2,0\}.       \tag{1}
\]
Equivalently, for the three \(E_7\) blocks
\[
(\mathcal M_2,\mathcal M_1,\mathcal M_0)
\]
the rank tuples are respectively
\[
(2,5,6)\quad\hbox{or}\quad(2,4,6).                  \tag{2}
\]

### Theorem

In the four fixed-divisor orbit charts from
`WORKING_BINARY_LOCUS.md`, every exact-\(\delta=2\) point has the
\(\{1,1\}\) shape except for the following complete list, up to the
stabilizer, interchange of \(p,q\), and interchange of the two fixed
roots.

1. **Two ramification contacts, squarefree fixed divisor.**
   The orbit modulus is
   \[
   \kappa=\eta^2=16.
   \]
   In the normalized chart
   \[
   h=p^2+\eta pq+q^2,\qquad \eta^2=16,
   \]
   the family is
   \[
   R=ap^3+\frac34a\eta p^2q+
        \frac34d\eta pq^2+dq^3,                    \tag{3}
   \]
   on the open set where \(R\) has no fixed root.  Its shape is
   \(\{2,0\}\).

2. **One fixed-root incidence and one ramification contact,
   squarefree fixed divisor.**
   The orbit modulus is
   \[
   \kappa=\frac{16}{3}.                             \tag{4}
   \]
   Every exact-\(\delta=2\) point of this incidence type at (4) has
   shape \(\{2,0\}\).

3. **Doubled nonbranch fixed root plus one ramification contact.**
   Here \(\kappa=4\).  Normalize
   \[
   h=(p+q)^2,\qquad
   R=ap^3+bp^2q+\frac32d\,pq^2+dq^3.                \tag{5}
   \]
   The displayed form imposes contact at \(p=0\).  On the exact
   \(\delta=2\) open set
   \[
   (3a-2b)(2a-2b+d)\ne0,                            \tag{6}
   \]
   the shape is \(\{2,0\}\) exactly on
   \[
   6a-5b+3d=0.                                      \tag{7}
   \]
   The swapped contact gives the other representative.

Thus the nominal \(\{2,0\}\) row in the abstract table is genuinely
occupied.  In particular it cannot be discarded before the \(E_6\)
analysis.

## 2. Local divisor calculation

The enumeration of exact-\(\delta=2\) incidences is independent of the
maximal-minor calculation.  Let \(L\) be a binary linear form and take
coordinates with \(L=p\).  If \(f,g\) are homogeneous of degrees \(d,e\)
and have positive \(L\)-orders \(m,n\), their leading terms give
\[
\operatorname{ord}_L J(f,g)=m+n-1                 \tag{8}
\]
unless
\[
em-dn=0.                                           \tag{9}
\]
Indeed, the coefficient at order \(m+n-1\) is a nonzero scalar times
\(em-dn\).  For degrees \(4\) and \(3\), the only positive integral
cancellation within range is \((m,n)=(4,3)\).  This is the already
separated power-fibre endpoint; direct calculation handles it.

When both orders are zero, the leading coefficient is the endpoint
contact determinant instead.  Applying (8) to
\(\alpha,\beta,\gamma\) gives the following exact bookkeeping.

- For
  \(h=p^2+\eta pq+q^2\) squarefree, with fixed roots \(L_1,L_2\),
  \[
  \begin{aligned}
  \operatorname{ord}_{L_i}g
     &=\min\{\operatorname{ord}_{L_i}R,2\},\\
  \operatorname{ord}_{p}g=1
     &\Longleftrightarrow 4c-3d\eta=0,\\
  \operatorname{ord}_{q}g=1
     &\Longleftrightarrow 3a\eta-4b=0,
  \end{aligned}                                    \tag{10}
  \]
  and all three displayed branch orders are otherwise zero.
- For \(h=L^2\), with \(L\) nonbranch,
  \[
  \operatorname{ord}_L g=1+\operatorname{ord}_L R, \tag{11}
  \]
  while the two branch-contact tests remain those in (10).
- For \(h=p^2\),
  \[
  \operatorname{ord}_p g=1+\operatorname{ord}_pR,
  \qquad
  \operatorname{ord}_q g=1\Longleftrightarrow b=0. \tag{12}
  \]
- For \(h=pq\),
  \[
  \operatorname{ord}_p g=\operatorname{ord}_pR,
  \qquad
  \operatorname{ord}_q g=\operatorname{ord}_qR.    \tag{13}
  \]
- For \(h=p(p+q)\),
  \[
  \begin{aligned}
  \operatorname{ord}_p g&=\operatorname{ord}_pR,\\
  \operatorname{ord}_{p+q}g
    &=\min\{\operatorname{ord}_{p+q}R,2\},\\
  \operatorname{ord}_qg=1&\Longleftrightarrow3a-4b=0.
  \end{aligned}                                    \tag{14}
  \]

The orders in (11)--(14) are capped by the corresponding order of
\(\gamma=8h^2pq\).  At total order two, (10)--(14) give exactly:

- one contribution of order two; or
- two distinct contributions of order one.

This exhausts the incidence types used below.  It also keeps the
constant-dependent power fibre \(h=p^2,R=p^3\) separate.

## 3. The \(r^1\) matrix

The possible \(r^1\) tangent is
\[
(U_r,V_r,T_r)=(u_1p+u_2q,\ v_1p+v_2q,\ t).
\]
Its \(E_7\) equation is
\[
\alpha(u_1p+u_2q)+
\beta(v_1p+v_2q)+\gamma t=0.                        \tag{15}
\]
Let \(\mathcal M_1\) be the \(7\times5\) coefficient matrix of (15).
By (1), at exact \(\delta=2\),
\[
\operatorname{rank}\mathcal M_1=
\begin{cases}
5,&\{k_1,k_2\}=\{1,1\},\\
4,&\{k_1,k_2\}=\{2,0\}.
\end{cases}                                        \tag{16}
\]
Thus maximal minors decide the split.

### Boundary charts

For \(h=p^2\), the two exact-\(\delta=2\) mechanisms have decisive
minors
\[
41472d^4,\qquad -1024bc^3.                          \tag{17}
\]
For \(h=pq\), representatives have
\[
-3240a^3b,\qquad 8b^2c^2.                           \tag{18}
\]
For \(h=p(p+q)\), put \(L=p+q\).  Representatives of all mechanisms,
up to swap, and decisive minors are
\[
\begin{array}{c|c}
R&\text{minor}\\ \hline
p^2(Ap+Bq)&-1080B(A-B)^2(3A-4B)\\
L^2(Ap+Bq)&-648B^3(5A+4B)\\
pL(Ap+Bq)&8B^2(A-B)(A+4B)\\
p(4Tp^2+3Tpq+Cq^2)&72C^2(C+T)^2\\
L(-4Bp^2+Bpq+Cq^2)&-648C^3(5B-C).
\end{array}                                        \tag{19}
\]
Every factor in (17)--(19) is nonzero on the corresponding exact
\(\delta=2\) open set.  Hence all boundary points have shape
\(\{1,1\}\).

### Squarefree interior

Write
\[
L=p-sq,\qquad M=sp-q,\qquad h=LM,
\qquad s\ne0,\quad s^2\ne1.                         \tag{20}
\]
After division by the nonzero scalar \(s\), this is the normalized
interior form with
\[
\eta=-(s+s^{-1}),\qquad\kappa=(s+s^{-1})^2.         \tag{21}
\]

If one fixed root occurs twice in \(R\), or if both fixed roots occur
once, a maximal minor is a nonzero constant times the product of:

- \(s^2-1\);
- the evaluations excluding an additional fixed root; and
- the two branch-contact expressions.

It is therefore nonzero at exact \(\delta=2\).

For one simple fixed root and contact at \(p=0\), take
\[
R=L\{Ap^2+(1-3s^2)Tpq+4sTq^2\}.                   \tag{22}
\]
A maximal minor is
\[
\begin{aligned}
72&(s^2-1)^2(s^2-3)
  \{A+T(s^3+s)\}^2\\
&\cdot\{-As+3Ts^2-5T\}
 \{As^2-3A+12Ts^3-4Ts\}.                           \tag{23}
\end{aligned}
\]
Apart from \(s^2-3\), every factor in (23) is excluded from zero by
exactness.  Relabelling the fixed root and swapping the branches replaces
\(s\) by \(s^{-1}\).  Hence rank drops exactly when
\[
s^2=3\quad\hbox{or}\quad s^2=\frac13,
\]
which by (21) is precisely \(\kappa=16/3\).

For the two branch contacts, write
\[
\begin{aligned}
R={}&4sA p^3-3(1+s^2)A p^2q\\
   &-3(1+s^2)D pq^2+4sDq^3.                        \tag{24}
\end{aligned}
\]
The first and last rows of \(\mathcal M_1\) vanish, and its sole
possibly nonzero \(5\times5\) minor is a nonzero constant times
\[
(s^2-1)^2(s^2-4s+1)(s^2+4s+1)
R(L)^2R(M)^2.                                      \tag{25}
\]
Exactness makes the evaluation factors nonzero.  The remaining two
factors say \(s+s^{-1}=\pm4\), hence \(\kappa=16\).

### Doubled nonbranch root

For \(h=(p+q)^2\), if \(p+q\mid R\), the decisive minor is
\[
-512(A-2B)(2B-C)(A-B+C)^2                          \tag{26}
\]
for \(R=(p+q)(Ap^2+Bpq+Cq^2)\), and exactness makes it nonzero.

Otherwise impose one branch contact as in (5).  The decisive minor is
\[
576(3a-2b)(2a-2b+d)^2(6a-5b+3d).                  \tag{27}
\]
The first two factors are exactly the open conditions (6); the last
factor is the genuine exceptional equation (7).  This proves the
classification.

## 4. Literal regression points

The following exact points prevent the three exceptional mechanisms from
being accidentally discarded.

### \(\kappa=16\)

\[
h=p^2+4pq+q^2,\qquad
R=p^3+3p^2q+6pq^2+2q^3.                            \tag{28}
\]
Here
\[
g=2pq,\qquad \operatorname{Res}(h,R)=-18,
\qquad
\operatorname{rank}(\mathcal M_2,\mathcal M_1,\mathcal M_0)
=(2,4,6),
\]
and a literal \(\mathcal M_1\)-kernel vector is
\[
(-5,-1,1,5,3)^T.                                   \tag{29}
\]
More generally, on (3) a polynomial kernel vector is
\[
\left(5,\frac{\eta}{4},-1,-\frac{5\eta}{4},
3\left(a-\frac{\eta d}{4}\right)\right)^T.          \tag{30}
\]

### \(\kappa=16/3\)

Over \(\mathbb Q(\sqrt3)\), take
\[
\eta=\frac{4\sqrt3}{3},\quad
h=p^2+\eta pq+q^2,\quad
R=8p^2q+12\sqrt3\,pq^2+12q^3.                      \tag{31}
\]
Then
\[
g=p(p+\sqrt3q),\qquad
\operatorname{rank}(\mathcal M_2,\mathcal M_1,\mathcal M_0)
=(2,4,6),
\]
with kernel
\[
(-\eta,-1,0,1,4)^T.                                \tag{32}
\]

### \(\kappa=4\)

\[
h=(p+q)^2,\qquad R=6p^2q+15pq^2+10q^3.             \tag{33}
\]
Here
\[
g=2p(p+q),\qquad \operatorname{Res}(h,R)=1,
\qquad
\operatorname{rank}(\mathcal M_2,\mathcal M_1,\mathcal M_0)
=(2,4,6),
\]
and a kernel is
\[
(-3,-2,0,1,3)^T.                                   \tag{34}
\]
On the general exceptional locus (7), a polynomial kernel is
\[
(6,4,0,-2,6a-b)^T.                                 \tag{35}
\]

## 5. Verification

Run
```sh
./verify_delta2_hb_stratification_strict.sh
```
from this directory.  The strict harness runs:

- `verify_delta2_hb_stratification_sympy.py`, which reconstructs the
  Jacobians and every displayed maximal minor; and
- `verify_delta2_hb_stratification_pari.gp`, an independent CAS replay
  of the three literal regressions and the exceptional determinant
  factors.

The local valuation calculation in Section 2 independently controls the
exhaustiveness of the incidence list.  The computational checks control
the encoded coefficient algebra.

## AI-assistance and review disclosure

This derivation was developed with AI assistance.  All displayed
identities used in the classification are encoded in exact verification
scripts, but those scripts verify only the algebra they encode.  This
document is not peer reviewed, and exact computer algebra is not a
substitute for peer review.
