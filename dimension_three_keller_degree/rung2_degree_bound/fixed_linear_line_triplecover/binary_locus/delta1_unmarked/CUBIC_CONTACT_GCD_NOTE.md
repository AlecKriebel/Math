# The cubic contact component leaves exact \(\delta=1\)

**Exact candidate checkpoint:** 2026-07-25T13:58:58Z  
**Status:** complete primary algebraic certificate; pending independent
hostile audit; not peer reviewed.

## 1. Scope

This note treats the degree-three component of the contact eliminant in
the generic unmarked chart
\[
 a_2=c_0=b_1=1,\qquad b_2=0.
\]
It does not assert that this chart exhausts the boundary charts.

Put
\[
 C(a)=160a^3-384a^2+310a-85.
\]
On the component \(C(a)=0\), the leading forms are
\[
\begin{aligned}
P={}&p(pq^2+aq^3),\\
Q={}&p\left(p^3+p^2q-\frac5{16}(2a-1)q^3\right),\\
R={}&p^3+\frac34p^2q
  -\frac3{20}(10a^2-19a+8)pq^2\\
 &\hspace{39mm}
  -\frac1{320}(120a^2-198a+79)q^3.              \tag{1}
\end{aligned}
\]

**Candidate conclusion.**  Every point of (1) has Hilbert--Burch gcd
degree at least three.  Therefore the cubic contact component is disjoint
from the exact-\(\delta=1\) stratum.

## 2. Contact certificate

Let
\[
\alpha=J(Q,R),\qquad \beta=-J(P,R),\qquad
\gamma=J(P,Q).
\]
The common divisor \(q\) is the unmarked divisor defining this chart.
The divided directional gradient
\[
N=q^{-1}\left(\partial_q-\frac14\partial_p\right)(P,Q,R)
\]
is a syzygy of \((\alpha,\beta,\gamma)\).  Its signed curvature \(K_N\)
satisfies, modulo \(C(a)\),
\[
K_N=(2a^2-3a+2)\alpha-\frac{16a-5}{32}\beta.     \tag{2}
\]
Thus (1) really lies in the contact locus.  Formula (2) is included to
identify the eliminant component; the exclusion below uses only its gcd.

## 3. Literal higher gcd

Define the homogeneous quadratic
\[
G=p^2+\left(\frac52a-\frac34\right)pq
 +\left(\frac52a^2-\frac{23}{8}a+\frac{15}{16}\right)q^2. \tag{3}
\]
It is nonconstant for every \(a\), since its \(p^2\)-coefficient is one.
Direct reduction modulo \(C(a)\) gives
\[
\begin{aligned}
\frac{\alpha}{q}
={}&\left(-12a^2+\frac{114}{5}a-\frac{177}{20}\right)G\\
&\quad\cdot
\left[p^2+(1-a)pq+
\left(\frac5{16}a^2-\frac{27}{64}a+\frac{15}{128}\right)q^2\right],
                                                               \tag{4}\\
\frac{\beta}{q}
={}&6G\left[p^2+(1-a)pq+
\left(\frac12a^2-\frac7{10}a+\frac{17}{80}\right)q^2\right],
                                                               \tag{5}\\
\frac{\gamma}{q}
={}&-8p^2G\left[p+\left(\frac54-a\right)q\right].              \tag{6}
\end{aligned}
\]
Hence \(qG\) divides \(\alpha,\beta,\gamma\).  Its degree is three, so
the Hilbert--Burch gcd degree is at least three, not one.  No
irreducibility assertion about \(G\) is needed.

## 4. Verification and disclosure

`verify_unmarked_cubic_sympy.py` reconstructs the minors, tangent,
curvature, and identities (2)--(6) over
\(\mathbb Q[a]/(C)\).  `verify_unmarked_cubic_pari.gp` independently
reconstructs the same objects in PARI/GP.  The strict wrapper requires
both.

These exact checks are evidence about the encoded algebra.  They do not
prove completeness of the parent chart decomposition, establish
scholarly priority, replace hostile mathematical review, or constitute
peer review.  AI systems materially assisted the discovery,
verification, and exposition.
