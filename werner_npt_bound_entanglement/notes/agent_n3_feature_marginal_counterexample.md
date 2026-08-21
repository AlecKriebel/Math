# Exact counterexample to the feature-state marginal inequality

## Result

Let
\[
 K_{\rm f}
 =\sum_R|z_R\rangle\langle z_R|
 \tag{1}
\]
be the positive two-logical-qubit feature state from the coherent
Takagi--Hodge reduction.  The proposed strengthening
\[
 \boxed{\quad
 \lambda_{\max}(K_{\rm f})
 \stackrel?{\leq}
 \frac29+\lambda_{\min}(\operatorname{Tr}_2K_{\rm f})
 \quad}
 \tag{2}
\]
is false.  It fails by the exact amount \(4/27\) on a qutrit graph-state
code.  The example already lies on the proved one-site-support
boundary.

The standard-library exact checker is
`verification/verify_n3_feature_marginal_counterexample.py`.

## Construction

Put \(\omega=e^{2\pi i/3}\).  For
\(z=(z_0,z_1,z_2)\in\mathbb F_3^3\), define
\[
 |g_z\rangle
 =\frac1{\sqrt{27}}
 \sum_{x\in\mathbb F_3^3}
 \omega^{\,2x_1x_2+z\cdot x}|x\rangle.
 \tag{3}
\]
This is the graph basis for the graph having only the edge
\(\{1,2\}\), of weight two.  Choose the two orthonormal frames
\[
 \begin{aligned}
 U&=(|g_{220}\rangle,\ |g_{011}\rangle),\\
 V&=(|g_{020}\rangle,\ |g_{022}\rangle).
 \end{aligned}
 \tag{4}
\]

Recall
\[
 S=\frac49E_2+\frac{20}{9}E_3
   =\frac49\sum_{i<j}{\mathsf A}_i{\mathsf A}_j
    +\frac89{\mathsf A}_1{\mathsf A}_2{\mathsf A}_3,
 \qquad {\mathsf A}_i=\frac{I-F_i}{2}.
 \tag{5}
\]
In the logical product basis
\((00,01,10,11)\), direct exact character summation gives
\[
 \boxed{\qquad
 K_{\rm f}
 =
 \operatorname{diag}\left(
 \frac49,\frac29,\frac1{27},\frac1{27}
 \right).
 \qquad}
 \tag{6}
\]
Therefore
\[
 \lambda_{\max}(K_{\rm f})=\frac49,
 \qquad
 \operatorname{Tr}_2K_{\rm f}
 =\operatorname{diag}\left(\frac23,\frac2{27}\right),
 \tag{7}
\]
and
\[
 \boxed{\qquad
 \lambda_{\max}(K_{\rm f})
 -\left(
 \frac29+\lambda_{\min}(\operatorname{Tr}_2K_{\rm f})
 \right)
 =\frac4{27}>0.
 \qquad}
 \tag{8}
\]

The verifier expands (5) into the eight commuting-swap monomials,
evaluates every matrix entry from (3) in
\(\mathbb Q(\omega)\), and obtains (6) without floating-point
arithmetic.

## Boundary geometry

The graph in (3) has an isolated zeroth site.  On that site,
\[
 \operatorname{rank}\rho_0^U=2,\qquad
 \operatorname{rank}\rho_0^V=1.
 \tag{9}
\]
The other two one-site reductions of each plane have rank three.
Thus (4) is on the established one-site-support boundary, not an
uncontrolled full-support example.

This counterexample does not violate the desired pair-sector
inequality.  Here \(K_{\rm f}\) is diagonal, hence
\(K_{\rm f}^{\Gamma_2}=K_{\rm f}\succeq0\).  The full compressed
witness
\[
 \frac29I_4+K_{\rm f}^{\Gamma_2}
 \tag{10}
\]
is therefore strictly positive.  What fails is only the stronger
marginal sufficient condition (2).

Because (2) fails strictly on the support boundary, its equality at
the canonical code
\[
 U=(|000\rangle,|001\rangle),\qquad
 V=(|110\rangle,|111\rangle)
 \]
cannot be used to infer a global boundary equality classification.
No Hessian repair of (2) at that canonical point can make (2) a
universal proof route.
