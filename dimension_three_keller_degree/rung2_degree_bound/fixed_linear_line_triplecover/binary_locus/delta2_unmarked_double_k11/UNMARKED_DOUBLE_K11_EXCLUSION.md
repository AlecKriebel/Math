# The \(\{1,1\}\) unmarked-double component has no quartic counterexample

**Candidate checkpoint:** 2026-07-25T18:59:50Z

**Status:** complete primary proof with exact dual-CAS checks;
independent hostile audit pending; not peer reviewed.

## 1. Statement

In the binary fixed-linear line-triple-cover row, suppose the common
Hilbert--Burch divisor of the three top minors is the square of an
unmarked line.  The complete \(q^2\)-jet normal form, after scaling and
a target shear, is
\[
\begin{aligned}
P&=pq^3,\\
Q&=p(p^3+bp^2q+cpq^2),\\
R&=d\left(
p^3+\frac34bp^2q+
\left(\frac34c-\frac3{32}b^2\right)pq^2
\right)+eq^3.                                    \tag{1}
\end{aligned}
\]
The exceptional splitting divisor is
\[
K=3b^2-8c.                                       \tag{2}
\]
The component \(K=0\), whose Hilbert--Burch splitting is
\(\{2,0\}\), is handled separately.

**Candidate theorem.**  No quartic Keller counterexample on the exact
gcd-\(q^2\) open of (1) satisfies \(K\ne0\).

Together with the separately certified \(K=0\) theorem, this
provisionally excludes the entire unmarked-double exact-\(\delta=2\)
locus in the fixed-linear row.

## 2. The \(\{1,1\}\) basis

Let \(F_0=(P,Q,R)^T\) and put
\[
\begin{aligned}
N&=\frac1q\left(\partial_q-\frac b4\partial_p\right)F_0,\\
M&=\frac1q\left(pN+\frac K{16}\partial_pF_0\right).
                                                               \tag{3}
\end{aligned}
\]
Both columns are polynomial.  Direct reconstruction gives
\[
\begin{pmatrix}P_p&P_q\\Q_p&Q_q\\R_p&R_q\end{pmatrix}
=
\begin{pmatrix}N&M\end{pmatrix}
\begin{pmatrix}
-16p/K&(3b^2q-4bp-8cq)/K\\
16q/K&4bq/K
\end{pmatrix}.                                    \tag{4}
\]
The determinant of the right matrix is
\[
-\frac{16q^2}{K}.                                 \tag{5}
\]
On \(K\ne0\) and exact gcd \(q^2\), (4)--(5) make \(N,M\) the two
minimal Hilbert--Burch columns, with splitting \(\{1,1\}\).
Consequently every degree-seven transverse dependence is
\[
S=xN+yM.                                          \tag{6}
\]

The \(r\)-coefficient of \(E_6\) is the contact-curvature condition
\[
\mathcal K(S)=\lambda\alpha+\mu\beta,\qquad
\alpha=J(Q,R),\quad\beta=-J(P,R),                 \tag{7}
\]
giving six homogeneous binary coefficients.  We now solve them on all
parameter charts.

## 3. The generic chart \(bd\ne0\)

Diagonal source changes and independent target scalings send
\[
b\mapsto(\beta/\alpha)b,\qquad
c\mapsto(\beta/\alpha)^2c,\qquad
\frac ed\mapsto(\beta/\alpha)^3\frac ed.
\]
Over \(\mathbb C\), the chart \(bd\ne0\) therefore has the normalization
\[
b=d=1,                                            \tag{8}
\]
with \(c,e\) free.

Here exact gcd \(q^2\) requires
\[
e\ne0,\qquad
J(c,e)\ne0,                                       \tag{9}
\]
where
\[
J=192c^3-48c^2-1024ce-5c+1024e^2+320e.           \tag{10}
\]
Indeed, after division by \(q^2\),
\[
\gamma=-4p^2(3p^2+2pq+cq^2),
\]
the \(p=0\) value of \(\beta\) is \(-3eq^3\), and
\[
\operatorname{Res}_p\!\left(
\beta/q^2,\,3p^2+2p+c
\right)=\frac{243}{1024}J.                        \tag{11}
\]
Thus \(e=0\) or \(J=0\) is precisely a larger-gcd boundary on this
component.

### 3.1 The chart \(y=0\)

A nonzero contact has \(x\ne0\); scale \(x=1\).  The last coefficient
of (7) is
\[
\frac38e(c+8\mu),
\]
so (9) gives \(\mu=-c/8\).  The preceding coefficient is
\[
-\frac38e(16\lambda c-8c-3).
\]
It forces \(c\ne0\) and
\[
\lambda=\frac{8c+3}{16c}.                         \tag{12}
\]
The next two coefficients now become
\[
\begin{aligned}
&-\frac{3(8c-3)}{512c}
 (96c^2-36c-128e+5),\\
&-\frac{3(8c-3)}{128c}
 (32ce+c-24e).                                   \tag{13}
\end{aligned}
\]
Because \(K=3-8c\ne0\), the first equation gives
\[
e=\frac{96c^2-36c+5}{128}.                        \tag{14}
\]
The second then reads
\[
\frac3{16}(4c-1)^2(8c-5)=0.                       \tag{15}
\]
But substitution of (14) in (10) gives
\[
J=\frac9{16}(4c-1)^2(8c-5)^2.                    \tag{16}
\]
Every contact allowed by (15) therefore has \(J=0\), contrary to the
exact-gcd condition (9).

### 3.2 The chart \(y\ne0\)

Scale \(y=1\).  The first contact coefficient gives
\[
e=-\frac{25-144c+192c^2}{512}.                    \tag{17}
\]
After (17), the second is
\[
-\frac{45}{2048}(8c-3)
 (64c^2-16c-1).
\]
Since \(K\ne0\), put
\[
h=64c^2-16c-1=0.                                  \tag{18}
\]

Reduce the last four cleared contact coefficients modulo \(h\).  Two
normalized remainders \(R_2,R_3\) satisfy the exact compatibility
\[
R_3-5R_2=-2(56c-17)(12x-1).                      \tag{19}
\]
Since
\[
\operatorname{Res}_c(h,56c-17)=128,               \tag{20}
\]
equation (19) forces \(x=1/12\).

At \(x=1/12\), take integral rescalings \(E_0,E_1,E_2\) of three
remaining contact equations.  They are linear in \(\lambda,\mu\):
\[
\begin{aligned}
E_0={}&9216\lambda c-2304\lambda+18432\mu
       +1256c-379,\\
E_1={}&4608\lambda c-1728\lambda
       -73728\mu c+9216\mu+12792c-3865,\\
E_2={}&221184\mu c-64512\mu-824c+249.
                                                               \tag{21}
\end{aligned}
\]
The determinant of their \(3\times3\) augmented matrix, reduced modulo
\(h\), is
\[
-31850496(79048c-23855).                           \tag{22}
\]
Finally,
\[
\operatorname{Res}_c(h,79048c-23855)=278656.       \tag{23}
\]
Thus (21) is incompatible on (18).  There is no contact on the
\(y\ne0\) chart.

## 4. The three boundary charts

The scaling argument leaves exactly three charts outside \(bd\ne0\).
Exact gcd always forces \(e\ne0\).

### 4.1 \(b\ne0,d=0\)

Scale \(b=e=1\).  The first contact coefficient is \(12y^2\), so
\(y=0\) and \(x=1\).  Two subsequent coefficients give
\[
\lambda=1,\qquad 8c+12\lambda-15=0.
\]
Hence \(c=3/8\), which is precisely \(K=0\), outside this component.

### 4.2 \(b=0,c\ne0,d\ne0\)

Scale \(c=d=1\).  The first coefficient is a nonzero multiple of
\(y^2\), hence \(y=0,x=1\).  The last three equations successively give
\[
e\mu=0,\qquad \mu+8e\lambda=0,\qquad \lambda+4e=0.
\]
Since exact gcd gives \(e\ne0\), the first two force
\(\mu=\lambda=0\), and the third forces \(e=0\), a contradiction.

### 4.3 \(b=d=0,c\ne0\)

Scale \(c=e=1\).  The first nonzero coefficient is \(30y^2\), so
\(y=0,x=1\).  A later coefficient is the literal constant \(-6\).
This chart has no contact.

These charts exhaust \(K\ne0\).

## 5. Zero contact and conclusion

If \(x=y=0\), the shifted degree-six syzygy block is injective: its
required row degrees \((1,1,0)\) lie below both minimal
\(\{1,1\}\) columns in (3).  Hence every nonlinear term is binary.
The unconditional plane low-degree theorem over \(\mathbb C(r)\),
followed by the birational Keller theorem, makes the map a polynomial
automorphism.

Sections 3--4 exclude every nonzero contact, so the candidate theorem
follows.

## 6. Verification and disclosure

`verify_unmarked_double_k11_sympy.py` reconstructs (1)--(7), the
exact-gcd boundary (10)--(11), every contact coefficient, the hand
elimination (12)--(23), and all three boundary charts.  It also gives
two direct unit-ideal checks: the \(y\ne0\) contact ideal is the unit
ideal, and the \(y=0\) ideal saturated by \(KeJ\) is the unit ideal.

`verify_unmarked_double_k11_pari.gp` independently rebuilds the raw
Jacobians and curvature in PARI/GP.  It replays the hand elimination
using polynomial remainders, augmented determinants, and resultants,
rather than the SymPy Gröbner calculation.

The strict wrapper rejects optimized Python and any PARI run that does
not reach its terminal certificate.  These exact checks are evidence
about the encoded algebra, not peer review.  The parameter
normalizations, exact-gcd interpretation, and zero-contact plane-field
exit require hostile audit.  AI systems materially assisted this work.
