# An explicit counterexample to SIC(21)

**Alec Kriebel, with heavy assistance from ChatGPT 5.6 Sol (OpenAI)**

First public branch draft: **22 July 2026, 02:59:33 UTC**. Not peer reviewed.

> **Verification warning.** Alec Kriebel is a complete amateur exploring the
> limits of AI-assisted mathematics and cannot independently verify these
> claims. The construction and proof are being released for expert checking.
> The priority claim is provisional and limited by the documented audit.

## Abstract

Let

\[
 E:\mathbb C[\xi_1,\ldots,\xi_n,Z_1,\ldots,Z_n]\longrightarrow
 \mathbb C[Z_1,\ldots,Z_n],\qquad
 E(\xi^\alpha p(Z))=\partial_Z^\alpha p(Z).
\]

The Special Image Conjecture \(\mathrm{SIC}(n)\) says that \(\ker E\) is a
Mathieu--Zhao subspace. We give an exact rational polynomial
\(A\in\mathbb Q[\xi,Z]\) for \(n=21\), with 72 monomials and total degree
four, and take \(b=Z_1\). We prove

\[
 A^m\in\ker E\quad(m\geq1),\qquad
 bA^m\notin\ker E\quad\text{for infinitely many }m.
\]

Thus \(\mathrm{SIC}(21)\) is false. The witness is obtained from the
13-variable stable Keller model in Exploration 03 by adjoining eight
variables. The bridge is a scalar-parameter form of Abhyankar--Gurjar
inversion; unlike Zhao's homogeneous specialization, it permits the linear
block in this construction. Exact SymPy and dependency-free rational
checkers accompany a 72-term sparse certificate.

## 1. The Special Image Conjecture

Put

\[
 R_n=\mathbb C[\xi_1,\ldots,\xi_n,Z_1,\ldots,Z_n]
\]

and define \(E_n:R_n\to\mathbb C[Z]\) by

\[
 E_n(\xi^\alpha p(Z))=\partial_Z^\alpha p(Z).
\]

If \(\Theta_j=\xi_j-\partial_{Z_j}\), Zhao's theorem gives

\[
 \ker E_n=\sum_{j=1}^n\Theta_jR_n. \tag{1}
\]

A linear subspace \(M\) of a commutative algebra is a Mathieu--Zhao
subspace if

\[
 f^m\in M\ (m\geq1)
 \quad\Longrightarrow\quad
 qf^m\in M\ (m\gg0)\quad\text{for every }q.
\]

The assertion that \(\ker E_n\) is such a subspace is \(\mathrm{SIC}(n)\).

## 2. A scalar-parameter inversion lemma

The following form is useful because it does not require \(g\) to be
homogeneous or to have order at least two.

**Lemma 1 (pencil-Keller collision lemma).** Let \(k\) have characteristic
zero, let \(g\in k[Z]^n\), and suppose

\[
 \det(I+tJg)=1\quad\text{in }k[t,Z]. \tag{2}
\]

Set

\[
 A(\xi,Z)=-\sum_{j=1}^n\xi_jg_j(Z).
\]

Then \(E_n(A^m)=0\) for every \(m\geq1\). If the map
\(T=I+g\) has two points \(p,q\) with \(T(p)=T(q)\) and
\(p_i\ne q_i\), then

\[
 E_n(Z_iA^m)\ne0
\]

for infinitely many \(m\).

**Proof.** Work in the \(t\)-adically complete ring \(k[Z][[t]]\). The map

\[
 T_t(Z)=Z+tg(Z)=Z-H_t(Z),\qquad H_t=-tg,
\]

has a unique formal inverse \(Q_t\), because it is congruent to the identity
modulo \(t\). The Abhyankar--Gurjar inversion identity is valid in this
filtration: for \(p\in k[Z]\),

\[
 p(Q_t(Z))=
 \sum_{\alpha\in\mathbb N^n}
 \frac1{\alpha!}\partial_Z^\alpha
 \bigl(H_t(Z)^\alpha\det JT_t(Z)\,p(Z)\bigr). \tag{3}
\]

This is the usual formal identity applied modulo \(t^{N+1}\) for every
\(N\); the factor \(H_t^\alpha\) has \(t\)-adic order \(|\alpha|\), so every
coefficient is a finite sum. By (2), \(\det JT_t=1\). The multinomial theorem
then turns (3) into

\[
 p(Q_t(Z))=\sum_{m\geq0}\frac{t^m}{m!}E_n\bigl(p(Z)A^m\bigr). \tag{4}
\]

Taking \(p=1\) makes the left side equal to one, proving
\(E_n(A^m)=0\) for every positive \(m\).

Now take \(p=Z_i\). If \(E_n(Z_iA^m)=0\) for all sufficiently large
\(m\), (4) says that the \(i\)-th coordinate of \(Q_t\) is a polynomial in
\(t,Z\). The formal identity

\[
 Q_{t,i}(T_t(Z))=Z_i
\]

is then a polynomial identity, so it may be specialized at \(t=1\). Hence
\(Q_{1,i}(T(p))=p_i\) and \(Q_{1,i}(T(q))=q_i\), contradicting
\(T(p)=T(q)\) and \(p_i\ne q_i\). ∎

The point of the \(t\)-adic formulation is that \(g\) below has a linear
\(BU\) block. Zhao's homogeneous theorem therefore should not be quoted
verbatim for this witness; Lemma 1 supplies the needed extension.

## 3. The explicit 21-variable map

Use the coordinate order

\[
 Z=(x,y,z,a_1,b_1,a_2,b_2,a_3,b_3,a_4,b_4,a_5,b_6,
 U_1,\ldots,U_8).
\]

Define \(g=(g_1,\ldots,g_{21})\) by

**Normalization note.** The coefficient of \(U_1\) in \(g_1\) is one:
\(g_1=U_1+\tfrac12a_1b_1+\tfrac32a_1y\). There is no scalar prefactor on
\(g_1\).

\[
\begin{aligned}
g_1={}&U_1+\tfrac12a_1b_1+\tfrac32a_1y,\\
g_2={}&U_2-a_2b_2-2a_2z+a_3b_3+3xz,\\
g_3={}&U_3+b_1a_5-a_3b_6-a_4b_4-7a_4y+3a_5y+4y^2,\\
g_4={}&x^2,\\
g_5={}&-3U_2+3a_2b_2+6a_2z-3a_3b_3-8xz,\\
g_6={}&U_4,\\
g_7={}&U_5-2b_1a_5+2a_3b_6+2a_4b_4+14a_4y-6a_5y-5y^2,\\
g_8={}&xy,\\
g_9={}&a_2z+3b_2x,\\
g_{10}={}&U_6,\\
g_{11}={}&U_7-b_1a_3+7a_2b_2+14a_2z-7a_3b_3-3a_3y-18xz,\\
g_{12}={}&U_8,\\
g_{13}={}&b_1a_4-b_4y,
\end{aligned} \tag{5}
\]

and

\[
\begin{aligned}
g_{14}={}&-\tfrac12a_1xz-\tfrac12b_1x^2,\\
g_{15}={}&-a_2a_3z+3a_2y^2-3b_2a_3x-b_3xy-12xy^2,\\
g_{16}={}&b_1a_3a_4-a_3b_4y+3a_4xz-a_5xz+b_6xy-3xyz,\\
g_{17}={}&-3x^2y,\\
g_{18}={}&-2b_1a_3a_4+2a_3b_4y-6a_4xz+2a_5xz-2b_6xy+5xyz,\\
g_{19}={}&-xy^2,\\
g_{20}={}&b_1xy+7a_2a_3z-21a_2y^2+21b_2a_3x+a_3xz+7b_3xy+84xy^2,\\
g_{21}={}&-a_4xy.
\end{aligned} \tag{6}
\]

The 72-term polynomial in the theorem is simply

\[
 A(\xi,Z)=-\sum_{j=1}^{21}\xi_jg_j(Z),\qquad b=Z_1=x. \tag{7}
\]

Equations (5)--(7) are a human-readable certificate. The JSON certificate
records the same object as exact sparse rational data.

## 4. Determinant certificate

Here is the structure behind (5)--(6). Exploration 03 gives an exactly
certified map in 13 variables

\[
 \Psi(X)=X+H_2(X)+BK(X), \tag{8}
\]

where \(H_2\) is quadratic, \(K\) has eight cubic components, and
\(B\in\operatorname{Mat}_{13\times8}(\mathbb Q)\). Its Jacobian determinant
is one. With \(Z=(X,U)\), the displayed polynomial vector is

\[
 g(X,U)=\bigl(H_2(X)+BU,-K(X)\bigr). \tag{9}
\]

Thus

\[
 I+sJg=
 \begin{pmatrix}
 I_{13}+sJH_2&sB\\
 -sJK&I_8
 \end{pmatrix}.
\]

Taking the Schur complement of \(I_8\), and using the homogeneities of
\(H_2\) and \(K\), gives the polynomial identity

\[
\begin{aligned}
\det(I+sJg)
 &=\det\bigl(I_{13}+sJH_2+s^2BJK\bigr)\\
 &=\det J\Psi(sX)=1. \tag{10}
\end{aligned}
\]

The primary checker verifies the matrix equality in (10) entry by entry.
The dependency-free checker separately tests the determinant pencil at 66
exact rational specializations; a Node.js/BigInt implementation supplies a
third runtime and checks 18 further exact specializations.

## 5. Collision certificate and main theorem

The following three rational points use the coordinate order above:

\[
\begin{aligned}
p_0={}&(0,0,-\tfrac14,0,0,0,\tfrac12,0,0,0,0,0,0;
0,0,0,0,0,0,0,0),\\
p_+={}&(1,-\tfrac32,\tfrac{13}2,-1,-2,\tfrac92,-10,\tfrac32,\tfrac34,
-\tfrac94,-6,-\tfrac{27}8,\tfrac92;\\
&\hspace{9mm}-\tfrac{17}4,-\tfrac{45}8,\tfrac{99}{16},-\tfrac92,
-\tfrac{177}8,\tfrac94,\tfrac{213}8,\tfrac{27}8),\\
p_-={}&(-1,\tfrac32,\tfrac{13}2,-1,2,-\tfrac92,-10,\tfrac32,-\tfrac34,
\tfrac94,6,\tfrac{27}8,\tfrac92;\\
&\hspace{9mm}\tfrac{17}4,\tfrac{45}8,\tfrac{99}{16},\tfrac92,
-\tfrac{177}8,-\tfrac94,-\tfrac{213}8,-\tfrac{27}8).
\end{aligned} \tag{11}
\]

Direct substitution gives

\[
 (I+g)(p_0)=(I+g)(p_+)=(I+g)(p_-)
 =(0,0,-\tfrac14,0,0,0,\tfrac12,0,\ldots,0). \tag{12}
\]

Their first coordinates are \(0,1,-1\).

**Theorem 2.** For \(A\) and \(b\) in (7),

\[
 A^m\in\ker E_{21}\quad\text{for every }m\geq1,
\]

but

\[
 bA^m\notin\ker E_{21}
\]

for infinitely many \(m\). Consequently \(\mathrm{SIC}(21)\) is false.

**Proof.** Equation (10) and the collision \(p_0,p_+\) in (12), separated
by their first coordinate, satisfy Lemma 1 with \(n=21\) and \(i=1\).
The first assertion and the infinite obstruction follow. Equation (1)
identifies \(\ker E_{21}\) with the image appearing in the usual statement
of the Special Image Conjecture. ∎

As low-order guards, the symbolic checker also obtains

\[
 E_{21}(A)=E_{21}(A^2)=0,
 \qquad E_{21}(bA)\ne0,
 \qquad E_{21}(bA^2)=3x^2y\ne0. \tag{13}
\]

## 6. Scope and priority

Zhang's immediate-consequences note correctly established only that the Image
Conjecture fails in *some* finite dimension. There is, however, an immediate
explicit predecessor inside this repository: the 22-variable cubic
homogeneous map in Exploration 03, combined with Zhao's homogeneous theorem,
gives an explicit \(\mathrm{SIC}(22)\) witness. Thompson's 24-variable and
Harrison's 79-variable cubic models similarly imply larger witnesses. Those
corollaries need not have been written out as \((A,b)\) to count as prior
mathematics.

The contribution here is therefore narrower: removing the homogenizing
variable lowers the explicit dimension from 22 to 21, while the resulting
linear \(BU\) block requires the scalar-parameter Lemma 1. At the audit
cutoff, no earlier public source was located that supplied an explicit
\(\mathrm{SIC}(n)\) witness with \(n\leq21\), or the nonhomogeneous lemma in
the form used above.

That is evidence, not proof, of priority. Public work is changing hourly and
private or unindexed work may exist. The defensible claim is:

> This note gives an explicit 72-term rational counterexample to
> \(\mathrm{SIC}(21)\), one dimension below the immediate
> \(\mathrm{SIC}(22)\) consequence of Exploration 03, using a
> scalar-parameter extension that permits a nonhomogeneous linear block.

See `PRIORITY_AUDIT.md` for queries, exact repository snapshots, and limits.

## References

1. W. Zhao, *Images of Commuting Differential Operators of Order One with
   Constant Leading Coefficients*, J. Algebra 324 (2010), 231--247;
   [arXiv:0902.0210](https://arxiv.org/abs/0902.0210).
2. H. Derksen, A. van den Essen, and W. Zhao, *The Gaussian Moments
   Conjecture and the Jacobian Conjecture*, Israel J. Math. 219 (2017),
   917--928; [arXiv:1506.05192](https://arxiv.org/abs/1506.05192).
3. Z. Zhang, *Direct Consequences of the Three-Dimensional Counterexample to
   the Jacobian Conjecture*, 20 July 2026,
   <https://zzhang-iu.github.io/papers/direct-consequences-jacobian/>.
4. A. Kriebel, with ChatGPT 5.6 Sol, *Small explicit symmetric Keller and
   vanishing counterexamples*, Exploration 03, 21 July 2026.
