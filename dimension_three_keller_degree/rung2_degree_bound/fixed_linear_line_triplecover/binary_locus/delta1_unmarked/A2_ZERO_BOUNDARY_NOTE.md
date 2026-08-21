# The \(a_2=0\) unmarked boundary leaves exact \(\delta=1\)

**Exact candidate checkpoint:** 2026-07-25T14:21:02Z  
**Status:** complete primary proof; pending independent hostile audit; not
peer reviewed.

## 1. Scope

In the unmarked chart write
\[
\begin{aligned}
A&=q^2(a_2p+a_3q),\\
B&=p^3+b_1p^2q+b_2pq^2+b_3q^3,\\
R&=c_0p^3+\frac34b_1c_0p^2q+c_2pq^2+c_3q^3,\\
P&=pA,\qquad Q=pB.                               \tag{1}
\end{aligned}
\]
The \(p^3\)-coefficient of \(B\) is nonzero and normalized to one; if
it vanished when \(a_2=0\), then \(q\) would divide both \(A\) and \(B\)
and the leading form would belong to a higher fixed-divisor row.

This note treats the final boundary \(a_2=0\).  Here \(a_3\ne0\), since
\(A\ne0\).

**Candidate conclusion.**  The \(a_2=0\) boundary contains no nonzero
contact point in exact \(\delta=1\).  Consequently every Keller map on
its exact-\(\delta=1\) part is an automorphism.

## 2. One coefficient forces a repeated divisor

Put
\[
\alpha=J(Q,R),\qquad\beta=-J(P,R),\qquad
\gamma=J(P,Q),
\]
and use the unmarked tangent
\[
N=q^{-1}\left(\partial_q-\frac{b_1}{4}\partial_p\right)(P,Q,R).
\]
For a nonzero tangent parameter, its curvature must satisfy
\[
K_N=\lambda\alpha+\mu\beta.
\]
On \(a_2=0\), the \(p^5\)-coefficient of the residual is
\[
-\frac34a_3D,\qquad
D=3b_1^2c_0-24b_2c_0+32c_2.                     \tag{2}
\]
Characteristic zero and \(a_3\ne0\) therefore give \(D=0\).

After removing the chart divisor \(q\), the three minors satisfy
\[
\begin{aligned}
\left.\frac{\alpha}{q}\right|_{q=0}
   &=\frac14Dp^4,                                \tag{3}\\
\frac{\beta}{q}
   &=\frac{a_3q}{4}
      (15b_1c_0p^2q+36c_0p^3+4c_2pq^2-12c_3q^3),
                                                               \tag{4}\\
\frac{\gamma}{q}
   &=-4a_3p^2q(2b_1pq+b_2q^2+3p^2).             \tag{5}
\end{aligned}
\]
Equation (2) makes (3) vanish.  Since \(\alpha/q\) is homogeneous,
\(q\mid\alpha/q\); equations (4)--(5) show the same for the other two
reduced minors.  Hence
\[
q^2\mid\gcd(\alpha,\beta,\gamma).                 \tag{6}
\]
Every contact point therefore lies in \(\delta\ge2\), disjoint from the
exact-\(\delta=1\) stratum.

The only remaining exact-\(\delta=1\) branch has zero tangent parameter.
The injective binary lower block and plane-plus-shear exit make its Keller
maps automorphisms.

## 3. Verification and disclosure

`verify_a2_zero_sympy.py` and `verify_a2_zero_pari.gp` independently
reconstruct the general tangent, curvature coefficient, and reduced
minors without normalizing \(b_1\) or \(c_0\).

The exact checks certify the encoded identities.  They do not replace
hostile review of the chart coverage or zero-tangent exit, establish
scholarly priority, or constitute peer review.  AI systems materially
assisted the discovery, verification, and exposition.
