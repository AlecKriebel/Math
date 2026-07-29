# The coherent two-skew concurrence as one rank-two exterior inequality

## Status

This note gives an exact reduction and an exact counterexample to the
resulting inequality.  Let
\[
 Q_{(2)}
 =\frac49\,W^\dagger
 \left(\sum_{1\leq i<j\leq3}{\mathsf A}_i{\mathsf A}_j\right)W,
 \qquad {\mathsf A}_i=\frac{I-F_i}{2},
\]
be the coherent two-skew logical feature of two qutrit code planes.
Then
\[
 \boxed{\quad {\cal C}(Q_{(2)})\leq\frac29
 \quad\hbox{for all code planes}\quad}                  \tag{1}
\]
is exactly equivalent to the following single scalar theorem:
\[
\boxed{
\begin{aligned}
 &3\|C\|_2^2
 -2\sum_{i=1}^3\|\operatorname{Tr}_iC\|_2^2
 +\sum_{1\leq i<j\leq3}
      \|\operatorname{Tr}_{ij}C\|_2^2\\
 &\hspace{42mm}
 +2s_1(C)s_2(C)\geq0
 \qquad(\operatorname{rank}C\leq2).
\end{aligned}}                                          \tag{2}
\]
Thus all Takagi mixing and all three coherent pair channels collapse
to one rank-two exterior correction \(2s_1s_2\).  The Gaussian-integer
rank-two matrix in Section 5 violates (2).  Consequently the
standalone coherent bound (1) is **false**.  This does not disprove
the coupled bound for \(Q_{(2)}+Q_{(3)}\), because the omitted
triple-skew feature can compensate.

The dependency-free checker is
`verification/verify_n3_q2_concurrence_exterior_reduction.py`.

## 1. The partially transposed two-skew form

Put
\[
 S_2^0=\sum_{i<j}{\mathsf A}_i{\mathsf A}_j
\]
and partially transpose the second physical replica.  Since
\[
 F_i^\Gamma=3P_i,\qquad
 {\mathsf A}_i^\Gamma=\frac12(I-3P_i),
\]
the coefficient-matrix contraction formula gives
\[
\boxed{
\begin{aligned}
 {\cal J}(C)
 &:=
 \langle\psi_C|(S_2^0)^\Gamma|\psi_C\rangle\\
 &=\frac34\|C\|_2^2
 -\frac12\sum_i\|\operatorname{Tr}_iC\|_2^2
 +\frac14\sum_{i<j}
       \|\operatorname{Tr}_{ij}C\|_2^2 .
\end{aligned}}                                          \tag{3}
\]
Consequently (2) is precisely
\[
 \boxed{\qquad
 {\cal J}(C)+\frac12s_1(C)s_2(C)\geq0 .
 \qquad}                                                 \tag{4}
\]
The correction is genuinely exterior:
\[
 s_1(C)s_2(C)=\|\bigwedge\nolimits^2 C\|_2
\]
for a rank-two matrix.

In the scalar/traceless local decomposition, if \(w_k\) is the
squared mass with exactly \(k\) traceless factors, then
\[
 {\cal J}(C)=3w_0-\frac34w_2+\frac34w_3.                 \tag{5}
\]
The degree-one mass cancels identically.  Thus the surviving
realizability assertion can also be written
\[
 w_2\leq4w_0+w_3+\frac23s_1s_2.                         \tag{6}
\]
Unlike a linear sector bound, the last term in (6) remembers the
common rank-two Pluecker tensor.

## 2. A determinant-one filter formula for concurrence

Let \(R\succeq0\) be any two-qubit operator and let \(F_{\rm L}\)
be the logical swap.  Homogeneous concurrence obeys
\[
\boxed{
 {\cal C}(R)
 =
 \sup_{A,B\in SL(2,\mathbb C)}
 \left\{
 -\operatorname{Tr}\!\left[
 F_{\rm L}(A\otimes B)R(A\otimes B)^\dagger
 \right]
 \right\}_+ .
}                                                        \tag{7}
\]

Here is a self-contained proof.  For a pure column
\(z=\operatorname{vec}M\), partial transposition gives
\[
 \lambda_{\min}\bigl((|z\rangle\langle z|)^\Gamma\bigr)
 =-|\det M|.
\]
Since \(F_{\rm L}/2\) is the partial transpose of a normalized
maximally entangled projector,
\[
 -\langle z,F_{\rm L}z\rangle\leq2|\det M|.
\]
This remains true after determinant-one local filters.  Taking an
arbitrary pure-column decomposition and then the convex-roof infimum
proves that the right side of (7) is at most \({\cal C}(R)\).

For \(R\succ0\), determinant-one positive filters make both logical
marginals scalar; two logical unitaries then put the spatial Pauli
block in real diagonal form.  Thus the filtered operator is Bell
diagonal.  Rotate its largest Bell eigenvector to the singlet.  If
the Bell eigenvalues are \(q_0\geq q_1,q_2,q_3\), then
\[
 -\operatorname{Tr}(F_{\rm L}R)
 =q_0-q_1-q_2-q_3
 ={\cal C}(R)
\]
in the positive-concurrence case, while both sides of (7) vanish in
the separable case.  Positive semidefinite \(R\) follows by
continuity from \(R+\varepsilon I\).  This proves (7).

## 3. Collapse of the physical feature

Let \(X,Y:\mathbb C^2\to(\mathbb C^3)^{\otimes3}\) be the two
full-column physical frames after determinant-one logical filters.
They need not be isometries, but
\[
 \det(X^\dagger X)=\det(Y^\dagger Y)=1.                  \tag{8}
\]
Choose the physical product-frame convention
\[
 W|a,b\rangle=x_a\otimes y_b.
\]
With
\[
 C=XY^\dagger,
\]
the swap/partial-transpose contraction sends the normalized logical
maximally entangled vector to the coefficient vector
\(\operatorname{vec}(C)/\sqrt2\).  Therefore
\[
\boxed{
 \operatorname{Tr}\!\left[
 F_{\rm L}W^\dagger S_2^0W
 \right]
 ={\cal J}(C).
}                                                        \tag{9}
\]
This is just the swap identity
\(\operatorname{Tr}(F_{\rm L}R)
=2\langle\Phi_2|R^\Gamma|\Phi_2\rangle\), followed by (3).

The two nonzero singular values of \(C=XY^\dagger\) satisfy
\[
 s_1(C)s_2(C)
 =\sqrt{\det(X^\dagger X)\det(Y^\dagger Y)}
 =1.                                                     \tag{10}
\]
Equations (7), (9), and the factor \(4/9\) in \(Q_{(2)}\)
show that (4) implies
\[
 {\cal C}(Q_{(2)})
 \leq\frac49\cdot\frac12=\frac29.
\]

Conversely, take any rank-two \(C\), divide it by
\(\sqrt{s_1s_2}\), and use its singular-value decomposition to write
the result as \(XY^\dagger\), where \(X,Y\) are determinant-one
logical filters of isometries.  The particular filtered-swap
expectation in (7) is bounded by (1).  Equation (9) therefore gives
\({\cal J}(C)\geq-s_1s_2/2\).  Hence (1) and (2) are exactly
equivalent.

## 4. Exact equality and a no-go for termwise monogamy

The canonical sharp planes
\[
 U=(|000\rangle,|001\rangle),\qquad
 V=(|110\rangle,|111\rangle)
\]
give, for the unscaled coherent compression,
\[
 W^\dagger S_2^0W
 =
 \begin{pmatrix}
 1/4&0&0&0\\
 0&3/4&-1/2&0\\
 0&-1/2&3/4&0\\
 0&0&0&1/4
 \end{pmatrix}.                                         \tag{11}
\]
Its Takagi values are
\((5/4,1/4,1/4,1/4)\), so its concurrence is \(1/2\).
The companion \(C=UV^\dagger\) has
\[
 s_1=s_2=1,\qquad {\cal J}(C)=-\frac12,
\]
and saturates (4).

The same code also disproves the tempting termwise route.  The three
individual unscaled pair compressions have concurrences
\[
 \frac12,\qquad\frac12,\qquad0.
\]
Their sum is \(1\), not at most \(1/2\), whereas coherent Takagi
mixing reduces the concurrence of their sum to \(1/2\).  Thus the
established two-copy theorem cannot be applied to the three pair
channels independently; the common three-channel origin in (2) is
essential.

On the complete common-factor chart
\[
 u_a=x\otimes e_a,\qquad v_a=y\otimes e_a,
\]
the earlier exact formula sharpens to
\[
 {\cal C}(Q_{(2)})
 =\frac29\left(1-|\langle\overline x,y\rangle|^2\right).
                                                               \tag{12}
\]
Hence equality includes the broad common-origin locus
\(\langle\overline x,y\rangle=0\); it is not confined to one
computational-basis orbit.  Whether every full-support equality
configuration reduces to this mechanism remains open.

## 5. Exact counterexample

Write \(X=(x_0,x_1)\) and \(Y=(y_0,y_1)\) as \(27\times2\)
Gaussian-integer matrices.  In lexicographic qutrit-word order, their
columns are
\[
\begin{aligned}
x_0={}&(50+38i,-18-41i,43+i,-43-12i,21+20i,-31+10i,\\
&7+i,-1+i,8-2i,115-6i,-183-12i,27+31i,-7+23i,\\
&73-20i,28-25i,-92+3i,63-17i,-78+14i,111+3i,\\
&-119+41i,93+26i,-42-21i,49-18i,-48-35i,\\
&-43+63i,24-48i,-25+58i),\\
x_1={}&(0,1-2i,-i,-1,0,i,1-i,-1+2i,1,0,-1-i,-1,\\
&0,-i,-i,-1,1+2i,1+i,0,1-2i,-1-i,-1,-i,-1,\\
&1-i,3i,2),\\[1mm]
y_0={}&(4+2i,-3-2i,3+i,-3-i,2+i,-2,i,0,i,-6-24i,\\
&2+17i,-10-16i,6+14i,-3-10i,8+9i,4-2i,-3+i,\\
&3-2i,-14-5i,9+5i,-12,10+2i,-6-2i,7-i,1-3i,\\
&2i,-2i),\\
y_1={}&(6+5i,6-6i,8-6i,-11-i,1+5i,-8+8i,9-i,-5,\\
&7-4i,4-6i,-13-3i,-7-2i,7+7i,10-6i,13-6i,\\
&-12-5i,-3+7i,-13+7i,5+4i,3+2i,9,-6-7i,-2i,\\
&-12-5i,3+8i,-4+3i,9+11i).
\end{aligned}                                           \tag{13}
\]
Put \(C=XY^\dagger\).  It has rank at most two.  Direct
Gaussian-integer contraction gives
\[
\begin{aligned}
\|C\|_2^2&=369939292,\\
\sum_i\|\operatorname{Tr}_iC\|_2^2&=842955888,\\
\sum_{i<j}\|\operatorname{Tr}_{ij}C\|_2^2&=560431501.
\end{aligned}                                           \tag{14}
\]
Therefore
\[
 4{\cal J}(C)
 =3\|C\|_2^2
 -2\sum_i\|\operatorname{Tr}_iC\|_2^2
 +\sum_{i<j}\|\operatorname{Tr}_{ij}C\|_2^2
 =-15662399.                                            \tag{15}
\]
The two-by-two Gram determinants are
\[
 \det(X^\dagger X)=7849591,\qquad
 \det(Y^\dagger Y)=6444692,
\]
so
\[
 \bigl(s_1(C)s_2(C)\bigr)^2
 =50588196320972.                                       \tag{16}
\]
There is no numerical comparison in the certificate:
\[
\begin{aligned}
(-15662399)^2
 -4(50588196320972)
 &=42957957151313>0,\\
4{\cal J}(C)&<0.
\end{aligned}                                           \tag{17}
\]
Equations (15)--(17) prove exactly that
\[
 {\cal J}(C)+\frac12s_1(C)s_2(C)<0.
\]

Normalize the determinant-one filtered companion by
\(\sqrt{s_1s_2}\).  The filter formula (7)--(10) then gives an exact
lower bound on the physical coherent two-skew concurrence:
\[
 {\cal C}(Q_{(2)})
 \geq
 \frac{15662399}
 {9\sqrt{50588196320972}}
 >\frac29,                                               \tag{18}
\]
where the final strict inequality is exactly (17).  Thus (13)
defines an exact physical counterexample after taking orthonormal
bases of the two column spaces and the positive algebraic
determinant-one filters constructed in Section 3.
