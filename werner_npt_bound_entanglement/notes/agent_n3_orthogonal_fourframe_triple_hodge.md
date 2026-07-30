# Orthogonal four-frame triple-Hodge frontier

## Status

This note settles one of two proposed auxiliary bounds and leaves the
sharper coherent one open.

Let
\[
 {\mathsf G}={\mathsf A}_1{\mathsf A}_2{\mathsf A}_3,
 \qquad {\mathsf A}_i=\frac{I-F_i}{2},
\]
and let
\[
 u_0,u_1,w_0,w_1\in(\mathbb C^3)^{\otimes3}
\]
be an orthonormal four-frame.  Define
\[
 z_{01}={\mathsf G}(u_0\otimes w_1),\qquad
 z_{10}={\mathsf G}(u_1\otimes w_0).                    \tag{1}
\]

The proposed opposite-energy estimate
\[
 \|z_{01}\|^2+\|z_{10}\|^2\leq\frac14                 \tag{2}
\]
is false.  The exact sharp universal bound following from the proved
single-pair triple-Hodge theorem is instead
\[
\boxed{\qquad
 \|z_{01}\|^2+\|z_{10}\|^2\leq\frac13,
\qquad}                                                  \tag{3}
\]
and the explicit orthogonal four-frame below attains \(1/3\).

The coherent inequality
\[
\boxed{\qquad
 |\langle z_{01},z_{10}\rangle|\stackrel{?}{\leq}\frac18
\qquad}                                                  \tag{4}
\]
is not disproved by this construction: its two feature vectors are
orthogonal.  Unrestricted complex optimization repeatedly attains
\(1/8\), including from random starts, but this is only discovery
evidence.  No proof of (4) is claimed here.

The dependency-free exact checker is
`verification/verify_n3_orthogonal_fourframe_triple_hodge.py`.

## 1. Exact counterframe

On the first two qutrits put
\[
\begin{aligned}
 |\Phi_0\rangle
 &=\frac1{\sqrt3}(|00\rangle+|11\rangle+|22\rangle),\\
 |\Phi_1\rangle
 &=\frac1{\sqrt3}(|01\rangle+|12\rangle+|20\rangle).
\end{aligned}                                           \tag{5}
\]
These vectors are orthonormal.  On all three sites define
\[
\begin{aligned}
 u_0&=|\Phi_0\rangle|0\rangle,&
 w_1&=|\Phi_0\rangle|2\rangle,\\
 u_1&=|\Phi_1\rangle|0\rangle,&
 w_0&=|\Phi_1\rangle|2\rangle.
\end{aligned}                                           \tag{6}
\]
The four vectors in (6) are orthonormal.

Use the local Hodge convention
\[
 (A_p)_{ai}=2^{-1/2}\varepsilon_{pai}.
\]
For tensors \(x,y\), the coefficients of
\({\mathsf G}(x\otimes y)\), in the three local Hodge bases, are
\[
 \frac1{\sqrt8}
 \sum_{\substack{a,b,c\\d,e,f}}
 \varepsilon_{pad}\varepsilon_{qbe}\varepsilon_{rcf}
 x_{abc}y_{def}.                                       \tag{7}
\]

Before the \(1/\sqrt3\) normalizations in (5), the only nonzero
coefficients for the first pair in (6) are
\[
 (001),(111),(221),
\]
each equal to \(-2\).  For the second pair they are
\[
 (011),(121),(201),
\]
again each equal to \(-2\).  Restoring the factor
\[
 \frac1{\sqrt8}\frac1{3}
\]
from (7) and (5) gives
\[
\boxed{
 \|z_{01}\|^2=\|z_{10}\|^2
 =\frac{3\cdot4}{8\cdot9}=\frac16.}                    \tag{8}
\]
Their supports in the Hodge basis are disjoint, so
\[
\boxed{\langle z_{01},z_{10}\rangle=0.}                 \tag{9}
\]
Equations (8)--(9) prove that the left side of (2) is \(1/3\).

## 2. Sharp universal energy budget

For every orthonormal pair \(x,y\), the established sharp
triple-Hodge stable-rank theorem gives
\[
 \|{\mathsf G}(x\otimes y)\|^2\leq\frac16.              \tag{10}
\]
Both \((u_0,w_1)\) and \((u_1,w_0)\) are orthonormal pairs.  Applying
(10) twice proves (3).  Equation (8) proves sharpness.

Thus no proof of (4) can proceed by Cauchy--Schwarz followed by the
opposite-energy budget (2).  The best such argument gives only
\[
 |\langle z_{01},z_{10}\rangle|
 \leq\sqrt{\|z_{01}\|^2\|z_{10}\|^2}
 \leq\frac16.                                           \tag{11}
\]
The missing improvement from \(1/6\) to \(1/8\) must exploit
coherence between the two complementary pairs.  The sharp
energy-saturating frame (6) demonstrates the required compensation:
both diagonal energies reach \(1/6\), but their cross coherence
vanishes exactly.

