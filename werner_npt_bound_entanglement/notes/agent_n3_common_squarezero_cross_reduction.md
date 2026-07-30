# The common-plane plus square-zero cross reduction

## Status

Every rank-two matrix has a canonical orthogonal splitting
\[
 C=N+S
\tag{1}
\]
in which

* \(N\) has the same two-dimensional row and column support;
* \(S\) has orthogonal initial and final supports and satisfies
  \(S^2=0\);
* \(N\) and \(S\) are Hilbert--Schmidt orthogonal.

The common-plane term is already known to satisfy \(Q_3(N)\geq0\).
There is no established theorem for a general orthogonal-plane
square-zero term \(S\).

This note computes the interference exactly.  If
\[
 z={\cal B}_3(N,S),
\]
then
\[
\boxed{
 z=\frac34\left(
 \langle\Pi _3N,\Pi _3S\rangle
 -
 \langle\Pi _2N,\Pi _2S\rangle
 \right).
}
\tag{2}
\]
Equivalently,
\[
\boxed{
 z=
 -\frac12\sum_i
 \langle\operatorname{Tr}_iN,\operatorname{Tr}_iS\rangle
 +\frac14\sum_{i<j}
 \langle\operatorname{Tr}_{ij}N,
         \operatorname{Tr}_{ij}S\rangle .
}
\tag{3}
\]
Thus the apparent degree-one interference cancels exactly.  The live
cross term is one coherent contrast between the degree-two and
degree-three overlaps.

The unrestricted three-copy theorem is equivalent to positivity of
the single \(2\times2\) matrix
\[
\boxed{
 {\cal G}(N,S)=
 \begin{pmatrix}
 Q_3(N)&{\cal B}_3(N,S)\\
 \overline{{\cal B}_3(N,S)}&Q_3(S)
 \end{pmatrix}\succeq0
}
\tag{4}
\]
for every compatible split.  Since the first diagonal entry is
already nonnegative, the two remaining statements are precisely
\[
\boxed{
 Q_3(S)\geq0,\qquad
 |{\cal B}_3(N,S)|^2\leq Q_3(N)Q_3(S).
}
\tag{5}
\]
The first is the orthogonal-plane square-zero frontier; the second is
one phase-covariant cross Cauchy inequality.

For one fixed canonical matrix, rotating the orthogonal component of
the right singular plane gives a physical phase orbit
\[
 C_\phi=N+e^{-i\phi}S.
\]
Its exact minimum is
\[
\boxed{
 \min_\phi Q_3(C_\phi)
 =Q_3(N)+Q_3(S)-2|{\cal B}_3(N,S)|.
}
\tag{6}
\]
Thus no phase may be discarded.  Universally, applying (6) also to
\(N+tS\) for every \(t\geq0\) recovers exactly (4)--(5).

An exact embedded-qubit spin-flip zero occurs at principal overlap
\(\operatorname{Tr}K^\dagger K=1\) and sharply saturates (5):
\[
 Q_3(N)=Q_3(S)=\frac18,\qquad
 {\cal B}_3(N,S)=-\frac18.
\tag{7}
\]
Its full degree table shows that bounding the degree-two and
degree-three contributions independently is much too weak.  Hence
(2) is a useful exact reduction, but ordinary sectorwise
Cauchy--Schwarz does not prove the remaining determinant.

The dependency-free exact checker is
`verification/verify_n3_common_squarezero_cross_reduction.py`.

## 1. Canonical orthogonal splitting

Let
\[
 C=U\Sigma V^\dagger
\tag{8}
\]
be a thin singular-value decomposition.  Thus \(U,V:\mathbb C^2
\to{\cal H}\) are isometries and \(\Sigma\) is a nonnegative
\(2\times2\) diagonal matrix.  Put
\[
 P=UU^\dagger,\qquad K=U^\dagger V.
\tag{9}
\]
The orthogonal component of \(V\) has the polar decomposition
\[
 (I-P)V=WR,\qquad
 R=(I-K^\dagger K)^{1/2},
\tag{10}
\]
where \(W^\dagger U=0\), and \(W\) may be extended to an isometry on
the null space of \(R\).  Therefore
\[
 V=UK+WR.
\tag{11}
\]

Define
\[
\boxed{
\begin{aligned}
 N&=CP=U\Sigma K^\dagger U^\dagger,\\
 S&=C(I-P)=U\Sigma R W^\dagger.
\end{aligned}}
\tag{12}
\]
Then
\[
 PNP=N,\qquad S=PS(I-P),\qquad S^2=0.
\tag{13}
\]
Moreover,
\[
 \operatorname{Tr}S=0,\qquad
 \langle N,S\rangle_{\rm HS}=0.
\tag{14}
\]
For example,
\[
 \operatorname{Tr}S
 =\operatorname{Tr}(\Sigma RW^\dagger U)=0,
\]
and the same orthogonality gives the second identity.

In logical coordinates, write
\[
 A=\Sigma K^\dagger,\qquad B=\Sigma R.
\tag{15}
\]
The common origin of the two pieces includes the exact compatibility
\[
\boxed{
 AA^\dagger+BB^\dagger=\Sigma^2.
}
\tag{16}
\]
Indeed, \(K^\dagger K+R^2=I\).  Any proof of (5) may use (16);
treating \(A,B\) as unrelated matrices is a relaxation.

## 2. Exact endpoint cross term

Let \(\Pi_k\) be the orthogonal projection onto the qutrit operator
sector having exactly \(k\) traceless local factors.  Put
\[
 z_k=\langle\Pi_kN,\Pi_kS\rangle_{\rm HS}.
\tag{17}
\]
Equation (14) and orthogonality of the four sectors give
\[
 \sum_{k=0}^3z_k=0.
\tag{18}
\]
Also \(\operatorname{Tr}S=0\), so \(z_0=0\).  Hence
\[
 z_1+z_2+z_3=0.
\tag{19}
\]

The endpoint superoperator \(L^{\otimes3}\) has eigenvalues
\[
 -\frac18,\quad\frac14,\quad-\frac12,\quad1
\tag{20}
\]
on degrees \(0,1,2,3\).  Consequently
\[
\begin{aligned}
 {\cal B}_3(N,S)
 &=\frac14z_1-\frac12z_2+z_3\\
 &=\frac34(z_3-z_2),
\end{aligned}
\tag{21}
\]
which proves (2).

The partial-trace formula gives another proof which does not mention
the degree decomposition:
\[
 {\cal B}_3(N,S)
 =
 \sum_{T\subseteq[3]}
 \left(-\frac12\right)^{|T|}
 \left\langle
 \operatorname{Tr}_TN,\operatorname{Tr}_TS
 \right\rangle .
\tag{22}
\]
The empty term vanishes by (14), and the full-trace term vanishes
because \(\operatorname{Tr}S=0\).  The six remaining terms are exactly
(3).

## 3. Phase orbit and the \(2\times2\) frontier

For every \(\phi\in\mathbb R\), put
\[
 V_\phi=UK+e^{i\phi}WR.
\tag{23}
\]
Since \(U^\dagger W=0\),
\[
 V_\phi^\dagger V_\phi
 =K^\dagger K+R^2=I.
\tag{24}
\]
Thus \(V_\phi\) is an isometry with the same singular values, and
\[
 C_\phi=U\Sigma V_\phi^\dagger
 =N+e^{-i\phi}S.
\tag{25}
\]
Polarization gives
\[
 Q_3(C_\phi)
 =q_N+q_S+2\operatorname{Re}(e^{-i\phi}z),
\quad
 q_N=Q_3(N),\quad q_S=Q_3(S).
\tag{26}
\]
Minimizing the last scalar phase proves (6).

There is a stronger universal form.  For arbitrary complex
\(\alpha,\beta\),
\[
\begin{aligned}
 Q_3(\alpha N+\beta S)
 ={}&|\alpha|^2q_N+|\beta|^2q_S\\
 &+2\operatorname{Re}
   \left(\overline\alpha\beta z\right).
\end{aligned}
\tag{27}
\]
Every matrix \(\alpha N+\beta S\) has range contained in
\(\operatorname{ran}U\), and hence has rank at most two.  Therefore
unrestricted endpoint positivity implies (4).

Conversely, split an arbitrary rank-two \(C\) by (12).  Positivity of
(4), tested at \((\alpha,\beta)=(1,1)\), gives \(Q_3(C)\geq0\).
This proves the equivalence.  A \(2\times2\) Hermitian matrix is
positive semidefinite exactly when its diagonal entries and
determinant are nonnegative.  The common-plane theorem supplies
\(q_N\geq0\), leaving exactly (5).

This also explains the relation between (5) and the phase bound (6).
Apply the universal phase bound to the rank-two pencil \(N+tS\).
For every \(t\geq0\), it says
\[
 q_N+t^2q_S-2t|z|\geq0.
\tag{28}
\]
Nonnegativity of this binary quadratic for all \(t\) is equivalent
to \(q_N,q_S\geq0\) and \(|z|^2\leq q_Nq_S\).

## 4. An exact midpoint equality

Embed the qubit labels \(0,1\) in each qutrit and define
\[
\begin{aligned}
 u_0&=|000\rangle,\\
 u_1&=\frac{|111\rangle+|001\rangle}{\sqrt2},\\
 w_0&=|110\rangle,\\
 w_1&=\frac{|111\rangle-|001\rangle}{\sqrt2}.
\end{aligned}
\tag{29}
\]
The frames \(U=(u_0,u_1)\) and \(W=(w_0,w_1)\) are isometries with
\(U^\dagger W=0\).  Put
\[
 K=R=\frac1{\sqrt2}I_2,\qquad
 V=\frac1{\sqrt2}(U+W),\qquad
 \Sigma=I_2.
\tag{30}
\]
Thus
\[
 N=\frac1{\sqrt2}UU^\dagger,\qquad
 S=\frac1{\sqrt2}UW^\dagger.
\tag{31}
\]
The principal-overlap scalar is exactly
\[
 \operatorname{Tr}K^\dagger K=1.
\tag{32}
\]

Direct exact contraction gives the complete sector table
\[
\begin{array}{c|ccc}
k&
\|\Pi_kN\|_2^2&
\|\Pi_kS\|_2^2&
\langle\Pi_kN,\Pi_kS\rangle\\ \hline
0&2/27&0&0\\
1&1/6&1/18&-1/18\\
2&4/9&5/9&1/9\\
3&17/54&7/18&-1/18.
\end{array}
\tag{33}
\]
In particular,
\[
\begin{aligned}
 q_N&=-\frac18\frac2{27}
 +\frac14\frac16
 -\frac12\frac49
 +\frac{17}{54}
 =\frac18,\\
 q_S&=\frac14\frac1{18}
 -\frac12\frac59
 +\frac7{18}
 =\frac18,\\
 z&=\frac34\left(-\frac1{18}-\frac19\right)
 =-\frac18.
\end{aligned}
\tag{34}
\]
Thus
\[
 {\cal G}(N,S)
 =\frac18
 \begin{pmatrix}1&-1\\-1&1\end{pmatrix}\succeq0
\tag{35}
\]
has rank one, and \(C=N+S\) is an exact endpoint zero.

The example is a sharp obstruction to independent sector bounds.
Ordinary Cauchy--Schwarz on degree two alone gives
\[
 \frac34
 \sqrt{\|\Pi_2N\|^2\|\Pi_2S\|^2}
 =\frac{\sqrt5}{6}.
\tag{36}
\]
But the complete phase budget in (6) is only
\[
 \frac{q_N+q_S}{2}=\frac18,
\tag{37}
\]
and
\[
 \frac{\sqrt5}{6}>\frac18
\]
already follows after squaring from \(5/36>1/64\).
Adding the independently bounded degree-three term only worsens the
gap.  Therefore (2) cannot be closed by bounding the two displayed
overlaps separately from their sector masses.  The remaining
determinant must use the shared \(U,\Sigma,K,R,W\) geometry.

## 5. Exact remaining lemma

The unrestricted three-copy endpoint is now equivalently the
conjunction of the following two statements.

1. **Orthogonal-plane square-zero positivity.**  For all isometries
   \(U,W:\mathbb C^2\to{\cal H}\) with \(U^\dagger W=0\), and every
   \(B\in M_2\),
   \[
   Q_3(UBW^\dagger)\geq0.
   \tag{38}
   \]

2. **Common/square-zero cross determinant.**  For every compatible
   canonical tuple in (8)--(16),
   \[
   \boxed{
   |{\cal B}_3(N,S)|^2
   \leq Q_3(N)Q_3(S).
   }
   \tag{39}
   \]

One may equivalently replace both by the single phase inequality
\[
\boxed{
 Q_3(N)+Q_3(S)
 \geq
 \frac32
 \left|
 \langle\Pi_3N,\Pi_3S\rangle
 -
 \langle\Pi_2N,\Pi_2S\rangle
 \right|.
}
\tag{40}
\]
Universal validity of (40), including all rescaled pencils, is
equivalent to (38)--(39).  The midpoint zero (29)--(35) proves that
all constants are sharp.
