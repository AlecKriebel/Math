# Exact mixed-divisor \(\{2,0\}\) exclusion in the fixed-linear row

**Candidate checkpoint:** 2026-07-25T15:28:00Z  
**Status:** complete primary proof with exact dual-CAS checks; independent
hostile audit pending; not peer reviewed.

## 1. Statement

Continue with
\[
H_4=(P,Q,0)=(pA(p,q),pB(p,q),0),\qquad
R=(H_3)_3,
\]
and
\[
\alpha=J(Q,R),\qquad\beta=-J(P,R),\qquad
\gamma=J(P,Q).
\]
Suppose the exact common divisor is
\[
\gcd(\alpha,\beta,\gamma)\sim pq,                  \tag{1}
\]
where \(p=0\) is the marked fixed divisor and \(q=0\) is a distinct
unmarked contact.

After the standard contact normalization,
\[
\begin{aligned}
A&=q^2(a_2p+a_3q),\\
B&=p^3+b_1p^2q+b_2pq^2+b_3q^3,\\
R&=p\left(c_0p^2+\frac34b_1c_0pq+c_2q^2\right),
\qquad c_2\ne0.                                    \tag{2}
\end{aligned}
\]

**Candidate theorem.**  No quartic Keller counterexample satisfying
(1)--(2) lies on the exceptional first-jet divisor
\[
b_1=0.
\]
Equivalently, the entire mixed-divisor \(\{2,0\}\) Hilbert--Burch
component is excluded.

The complementary mixed component \(b_1\ne0\), which has splitting
\(\{1,1\}\), remains separate.

## 2. The twice-divided tangent

Set \(b_1=0\).  Then
\[
N=\frac1{pq}(P_q,Q_q,R_q)^T
 = (2a_2p+3a_3q,\;2b_2p+3b_3q,\;2c_2)^T.          \tag{3}
\]
This is a syzygy of \((\alpha,\beta,\gamma)\).  Since its component
degrees are \((1,1,0)\), the exact Hilbert--Burch table forces
\[
\boxed{\{k_1,k_2\}=\{2,0\}}.                       \tag{4}
\]
Thus the complete degree-seven dependence is
\[
(U_r,V_r,W_r)^T=fN,\qquad
f=mp+nq+\rho r.                                    \tag{5}
\]

The \(r^3\)-coefficient of \(E_6\) is governed by
\[
C(N)=-3p\left(
\{3c_0D+4a_3c_2\}p^2-c_2Dq^2
\right),\qquad D=a_2b_3-a_3b_2.                   \tag{6}
\]
If \(C(N)=0\), then \(D=0\), then \(a_3=0\), and finally
\(a_2b_3=0\).  This makes \(A,B\) share \(p\), contrary to their
coprimality.  Hence \(C(N)\ne0\), and (6) forces
\[
\rho=0.                                            \tag{7}
\]

It remains to classify the binary multiplier \(f=mp+nq\).

## 3. The two endpoint charts

Scale \(c_2=1\).  The value \((a_3,b_3)\ne(0,0)\) at \(p=0\) gives two
normal-form charts under the residual source and target group.

### 3.1 \(a_3=0\)

Here \(a_2b_3\ne0\), and the chart is
\[
(a_2,a_3,b_2,b_3)=(1,0,0,1),\qquad c=c_0.          \tag{8}
\]
The five nonzero contact coefficients are
\[
\begin{aligned}
0&=-18cm^2,\\
0&=-2(18cmn+3c\mu+4\lambda),\\
0&=-3(6cn^2-2m^2-3c\lambda),\\
0&=2(6mn+\mu),\\
0&=6n^2+\lambda.                                   \tag{9}
\end{aligned}
\]
If \(c\ne0\), the first equation gives \(m=0\), and the last two
followed by the second give \(n=0\).  If \(c=0\), the second and last
give \(n=0\), and the third gives \(m=0\).  This chart has no nonzero
contact.

### 3.2 \(a_3\ne0\)

The chart is
\[
(a_2,a_3,b_2,b_3)=(a,1,b,0),\qquad c=c_0.          \tag{10}
\]
Put \(E=4-3bc\).  The contact equations are
\[
\begin{aligned}
0&=-6Em^2,\\
0&=-2\{(24-18bc)mn+3ac\mu+E\lambda\},\\
0&=-3\{(8-6bc)n^2+2bm^2+3c\mu\},\\
0&=2(-6bmn+a\mu-b\lambda),\\
0&=-6bn^2-\mu.                                     \tag{11}
\end{aligned}
\]

On \(E\ne0\), a nonzero solution exists only on
\[
a=0,\qquad bc=\frac13,\qquad
m=0,\quad \lambda=0,\quad\mu=-6bn^2.              \tag{12}
\]
On \(E=0\), a nonzero solution requires
\[
a=0,\qquad bc=\frac43,\qquad
bm^2=12n^2.                                        \tag{13}
\]
But (13) is not exact \(\delta=2\): after division by \(pq\), all
three minors still vanish at \(q=0\), so \(pq^2\) divides their
original gcd.

## 4. Both contact loci leave exact \(\delta=2\)

The second locus (12) also has a larger gcd.  Put
\[
G=3p^2+bq^2.
\]
Since \(b\ne0\), \(G\ne0\), and direct reconstruction gives
\[
\begin{aligned}
\alpha&=2p^2qG,\\
\beta&=\frac1b\,pq^2G,\\
\gamma&=-4p^2q^2G.                                 \tag{14}
\end{aligned}
\]
Thus its gcd contains \(pqG\) and has degree at least four.  Together
with the \(pq^2\) divisor on (13), this shows that **every nonzero
contact lies outside exact \(\delta=2\)**.

As a regression check beyond what the proof needs, retaining a nonzero
multiplier \(f=\tau q\) on (12) makes \(E_6\) fix the two \(r^2\)
coefficients as \(0,3b\tau^2\), after which
\[
[r^2]E_5=12\tau^3q(3p^2+bq^2).
\]
This boundary therefore also fails at \(E_5\), but the higher-gcd
routing (14) is the exact-stratum argument.

## 5. The zero-multiplier exit

Suppose \(f=0\).  The degree-six syzygy block can retain one scalar
multiple of \(N\):
\[
(A_r,B_r,\ell_{33})=\eta N.                        \tag{15}
\]
If \(\eta\ne0\), then the third component has the form
\[
F_3=2c_2\eta\,r+h(p,q).
\]
A triangular source automorphism makes \(F_3=r\).  The remaining two
components form a plane Keller map of degree at most four over
\(\mathbb C(r)\), hence are birational by the unconditional plane
low-degree theorem.  The original Keller map is therefore birational
and so is a polynomial automorphism.

If \(\eta=0\), every nonlinear term is binary.  Since the linear part is
invertible, a target change again isolates a coordinate
\(r+h(p,q)\), and the same plane-field/birational exit applies.

Thus neither a nonzero nor a zero degree-seven multiplier can support a
counterexample, proving the candidate theorem.

## 6. Verification and disclosure

`verify_mixed_k20_sympy.py` reconstructs the Hilbert--Burch tangent,
the curvature (6), the complete systems (9) and (11), their exhaustive
projective solutions, both higher-gcd factorizations, and the optional
degree-five boundary regression.

`verify_mixed_k20_pari.gp` independently replays the same raw Jacobian
and determinant identities in PARI/GP.  The strict wrapper rejects
optimized Python runs in which assertions could be bypassed.

These checks are evidence about the encoded algebra, not peer review.
The group-action normal forms and birational automorphism exit remain
subject to independent hostile checking.  AI systems materially
assisted this work.
