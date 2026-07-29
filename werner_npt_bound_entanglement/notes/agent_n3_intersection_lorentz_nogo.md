# Intersection-one: exact Lorentz reduction and a formal no-go

## Status

The intersection-one three-copy problem has an exact four-real-variable
form.  The already proved self-adjoint theorem makes the relevant
quadratic form nonnegative on the **real** determinant cone in
\(\operatorname{Herm}(2)\).  The desired nonnormal inequality asks for
nonnegativity on the corresponding **complex** determinant cone.

The real-cone information is not sufficient.  This note gives an exact
rational model which simultaneously has:

1. a positive (indeed uniformly positive) common-plane Gram form;
2. the sharp rank-one floor \(1/8\);
3. the full sharp self-adjoint lower bound;
4. every real-null Gram determinant nonnegative;
5. the two-sided projector bounds furnished by the self-adjoint theorem;
6. the sharper orthogonal-projector upper bound;
7. a positive-partial-transpose two-qubit Gram operator;

but whose complex-null defect is exactly \(-1/256\).

Thus these properties alone cannot prove the intersection-one theorem.
The first model below fails one stronger constraint enjoyed by every
physical three-copy compression:
\[
 {\mathsf G}^{\Gamma}\succeq\frac18I_4.
\]

The addendum in Section 4 closes that apparent escape.  It gives a
second exact rational model satisfying the quantitative partial-transpose
floor, the physical swap-sector spectral bounds, swap invariance, and
positivity of both the Gram and its partial transpose, while the desired
diagonal-to-dyad implication still fails.  Consequently the missing
ingredient must be a genuinely stronger common-origin relation between
the plane Gram and the cross functional.

## 1. The exact Lorentz reduction

Let \(S\) be a two-dimensional subspace and let \(w\) be a unit vector.
For \(H\in\operatorname{Herm}(S)\), put
\[
 g(H)=Q_3(H),\qquad
 t(H)={\cal B}_3(P_w,H),\qquad
 a=Q_3(P_w),
\]
and define
\[
 h(H)=a\,g(H)-t(H)^2.                                    \tag{1}
\]
Every real linear combination of \(P_w\) and a rank-one Hermitian
operator \(P_x\) has rank at most two.  The established self-adjoint
theorem therefore gives
\[
 h(P_x)\geq0\qquad(x\in S).                               \tag{2}
\]

Use Pauli coordinates
\[
 H=x_0I+x_1X+x_2Y+x_3Z.
\]
Then
\[
 \det H=x_0^2-x_1^2-x_2^2-x_3^2.                         \tag{3}
\]
Every nonzero real point of the cone \(\det H=0\) is a real scalar
multiple of a rank-one Hermitian operator.  Hence (2) says exactly
that \(h\) is nonnegative on the real Lorentz null cone.

Now let \(D=|u\rangle\langle v|\in M(S)\) have rank one, and write
\[
 D=A+iB,\qquad A=A^\dagger,\quad B=B^\dagger.
\]
Because the endpoint form is the complexification of its restriction
to Hermitian matrices,
\[
\begin{aligned}
 Q_3(D)&=g(A)+g(B),\\
 |{\cal B}_3(P_w,D)|^2&=t(A)^2+t(B)^2.
\end{aligned}
\]
Consequently the desired Gram determinant is
\[
\boxed{\quad
 aQ_3(D)-|{\cal B}_3(P_w,D)|^2=h(A)+h(B).
\quad}                                                    \tag{4}
\]
The rank-one equation \(\det(A+iB)=0\) is equivalent to
\[
 \det A=\det B,\qquad
 \langle A,B\rangle_{\det}=0.                             \tag{5}
\]
Thus \(A,B\) are an equal-length Lorentz-orthogonal spacelike pair
(with the degenerate rank-one-Hermitian case included by continuity).
Equivalently, if \(H_h\) is the real symmetric matrix representing
\(h\) and \(J=\operatorname{diag}(1,-1,-1,-1)\), then (4) asks for
\[
\boxed{\quad
 z^\dagger H_hz\geq0
 \quad\text{whenever}\quad z\in\mathbb C^4,\ z^{\mathsf T}Jz=0.
\quad}                                                    \tag{6}
\]
The self-adjoint theorem supplies only the restriction of (6) to real
\(z\).

## 2. An exact rational formal obstruction

Put \(m=1/8\), \(a=1/4\), and define on
\(\operatorname{Herm}(2)\)
\[
\boxed{
\begin{aligned}
 g(x_0I+x_1X+x_2Y+x_3Z)
 &=\frac34x_0^2+\frac14(x_1^2+x_2^2+x_3^2),\\
 t(x_0I+x_1X+x_2Y+x_3Z)
 &=\frac{-x_0+3x_1}{8}.
\end{aligned}}                                            \tag{7}
\]
Extend \(g\) to complex matrices by
\[
 g(A+iB)=g(A)+g(B).                                       \tag{8}
\]

### 2.1 All rank-one and self-adjoint tests pass

In the Hilbert--Schmidt orthonormal Pauli basis
\[
 I/\sqrt2,\ X/\sqrt2,\ Y/\sqrt2,\ Z/\sqrt2,
\]
the Gram operator of \(g\) has eigenvalues
\[
 \frac38,\ \frac18,\ \frac18,\ \frac18.
\]
Therefore
\[
 g(C)\geq\frac18\|C\|_2^2                               \tag{9}
\]
for every complex \(2\times2\) matrix \(C\), which is stronger than
the required rank-one floor.

The sharp self-adjoint bound also holds.  If
\(H=x_0I+x\cdot\sigma\), its two eigenvalues are
\(x_0\pm|x|\).  When \(|x_0|\geq|x|\), their singular-value difference
is \(2|x|\), while
\[
 g(H)\geq\left(\frac34+\frac14\right)|x|^2
 \geq\frac18(2|x|)^2.
\]
When \(|x|\geq|x_0|\), their singular-value difference is
\(2|x_0|\), while
\[
 g(H)\geq\frac34|x_0|^2
 \geq\frac18(2|x_0|)^2.                                  \tag{10}
\]

For a pure qubit projector
\[
 P_n=\frac12(I+n\cdot\sigma),\qquad |n|=1,
\]
one has
\[
 g(P_n)=\frac14,\qquad
 t(P_n)=\frac{-1+3n_1}{16}.                              \tag{11}
\]
Thus
\[
 -\frac14\leq t(P_n)\leq\frac18                         \tag{12}
\]
and
\[
\begin{aligned}
 h(P_n)
 &=\frac1{16}-\frac{(-1+3n_1)^2}{256}\\
 &=\frac{3(1+n_1)(5-3n_1)}{256}\geq0.                    \tag{13}
\end{aligned}
\]

This also passes the exact two-sided bounds for an orthogonal external
vector \(w\).  Here
\[
 a-m=g(P_n)-m=\frac18,
\]
so the self-adjoint theorem gives the interval
\[
 -m-\sqrt{(a-m)(g(P_n)-m)}
 \leq t(P_n)\leq
 m+\sqrt{(a-m)(g(P_n)-m)},
\]
namely \([-1/4,1/4]\).  Equation (12) obeys it and also obeys the
strictly sharper orthogonal-projector estimate \(t(P_n)\leq m=1/8\).

### 2.2 The Gram is PPT

Let \(e_\mu=\sigma_\mu/\sqrt2\), and let
\[
 {\mathsf G}
 =\frac38|e_0\rangle\langle e_0|
  +\frac18\sum_{j=1}^3|e_j\rangle\langle e_j|.            \tag{14}
\]
Under vectorization, the four \(e_\mu\) are the Bell basis.  Hence
\[
 {\mathsf G}
 =\frac18I_4+\frac14P_{\Phi},
\]
where \(P_\Phi\) is the normalized maximally entangled projection.
Partial transpose gives
\[
\boxed{\quad
 {\mathsf G}^{\Gamma}
 =\frac18(I+F)=\frac14P_{\rm sym}\succeq0.
\quad}                                                    \tag{15}
\]
It even has the explicit product decomposition
\[
 I+F
 =\sum_{\nu=x,y,z}\sum_{s=\pm1}
 P_{\nu,s}\otimes P_{\nu,s}.                             \tag{16}
\]

### 2.3 The complex-null target nevertheless fails

Take
\[
 D=|0\rangle\langle1|=\frac12(X+iY).
\]
Then
\[
 g(D)=\frac18,\qquad t(D)=\frac3{16}.
\]
Therefore
\[
\boxed{\quad
 a\,g(D)-|t(D)|^2
 =\frac1{32}-\frac9{256}
 =-\frac1{256}.
\quad}                                                    \tag{17}
\]
This is an exact counterexample to every proof which uses only the
properties listed above.  It is not a physical Werner witness.

## 3. The first missing physical constraint

Let \(V:\mathbb C^2\to{\cal H}\) be the isometry whose range is the
physical plane \(S\), and put
\[
 Y=\bigotimes_{i=1}^3\left(I-\frac12F_i\right).
\]
The common-plane compression is
\[
 K(V)=(V^\dagger\otimes V^\dagger)Y(V\otimes V).
\]
Since \(Y\succeq\frac18I\),
\[
 K(V)\succeq\frac18I_4.                                  \tag{18}
\]
The Hermitian Gram operator representing \(g\) is
\[
 {\mathsf G}=K(V)^\Gamma.
\]
Thus every physical plane satisfies the stronger, quantitative PPT
constraint
\[
\boxed{\quad
 {\mathsf G}^{\Gamma}\succeq\frac18I_4.
\quad}                                                    \tag{19}
\]
The formal model (14) lies exactly on the ordinary PPT boundary:
by (15), its partial transpose has a one-dimensional antisymmetric
kernel.  It therefore violates (19).

At this stage (19) was the first missing constraint exposed by the
formal model.  Section 4 shows that it is not sufficient, even after
the known physical swap-sector bounds are imposed.

## 4. Quantitative-PPT and swap-sector bounds still do not suffice

We now disprove the following entirely abstract implication.
Let \(G\) be a positive operator on \(M_2\), let
\(K=G^\Gamma\) commute with the swap \(F\), and suppose
\[
\frac18P_{\rm sym}\preceq K_{\rm sym}
\preceq\frac98P_{\rm sym},\qquad
\frac38P_{\rm asym}\preceq K_{\rm asym}
\preceq\frac{27}{8}P_{\rm asym}.                         \tag{20}
\]
Given \(T=T^\dagger\) and \(a>0\), assume
\[
 a\,g(P_x)\geq|\operatorname{Tr}(TP_x)|^2
 \quad\hbox{for every unit qubit }x,                     \tag{21}
\]
where \(g(D)=\langle\operatorname{vec}D,
G\operatorname{vec}D\rangle\).
The desired conclusion would be
\[
 a\,g(|u\rangle\langle v|)
 \geq |v^\dagger Tu|^2
 \quad\hbox{for every unit }u,v.                         \tag{22}
\]

### 4.1 Exact rational data

Let
\[
 |\Phi^+\rangle=\frac{|00\rangle+|11\rangle}{\sqrt2},
\qquad
 K=\frac25I_4+\frac25P_{\Phi^+}.
\]
In the computational basis,
\[
 K=
 \begin{pmatrix}
 3/5&0&0&1/5\\
 0&2/5&0&0\\
 0&0&2/5&0\\
 1/5&0&0&3/5
 \end{pmatrix}.                                         \tag{23}
\]
It is diagonal in the Bell basis.  Its eigenvalues on the symmetric
subspace are \(4/5,2/5,2/5\), and its eigenvalue on the antisymmetric
subspace is \(2/5\).  Hence it commutes with \(F\) and satisfies every
bound in (20).  Notice in particular that it satisfies the stronger
physical parity floor \(K_{\rm asym}\succeq3P_{\rm asym}/8\).

Since \(P_{\Phi^+}^\Gamma=F/2\),
\[
 G=K^\Gamma=\frac25I_4+\frac15F
 =
 \begin{pmatrix}
 3/5&0&0&0\\
 0&2/5&1/5&0\\
 0&1/5&2/5&0\\
 0&0&0&3/5
 \end{pmatrix}.                                         \tag{24}
\]
Thus \(G\) has eigenvalue \(3/5\) on the symmetric subspace and
\(1/5\) on the antisymmetric subspace.  In particular \(G\succ0\).
Moreover \(K\succeq2I_4/5\), so this example satisfies the physical
quantitative floor \(K=G^\Gamma\succeq I_4/8\) with room to spare.

Take
\[
 T=\frac35X=\begin{pmatrix}0&3/5\\3/5&0\end{pmatrix},
 \qquad a=\frac35.                                      \tag{25}
\]
These scalars obey the elementary physical normalization windows.  A
normalized three-party pure projector always has endpoint energy in
\([1/8,5/8]\); here \(a=3/5\), while (26) below shows that
\(g(P_x)\in[2/5,3/5]\) for every pure logical projector.

### 4.2 Every diagonal test passes

For a unit qubit \(x\), write its Bloch vector as
\((n_x,n_y,n_z)\).  Since
\(\operatorname{vec}(P_x)=x\otimes\overline{x}\),
\[
\begin{aligned}
 g(P_x)
 &=\frac25+\frac15
   \langle x\otimes\overline{x},
   F(x\otimes\overline{x})\rangle\\
 &=\frac25+\frac15|x^{\mathsf T}x|^2
 =\frac35-\frac15n_y^2.                                 \tag{26}
\end{aligned}
\]
Also \(\operatorname{Tr}(TP_x)=3n_x/5\).  The pure-state Bloch identity
\(n_x^2+n_y^2+n_z^2=1\) therefore gives
\[
\boxed{
\begin{aligned}
 a\,g(P_x)-|\operatorname{Tr}(TP_x)|^2
 &=\frac9{25}-\frac3{25}n_y^2-\frac9{25}n_x^2\\
 &=\frac9{25}n_z^2+\frac6{25}n_y^2\geq0.
\end{aligned}}                                          \tag{27}
\]
Thus the full continuum of hypotheses (21), not merely a finite sample,
holds exactly.

This rescaling also passes the sharp self-adjoint singular-value
estimate used in the physical problem.  If
\(H=x_0I+x_1X+x_2Y+x_3Z\) is Hermitian and
\(r^2=x_1^2+x_2^2+x_3^2\), then
\[
 g(H)=\frac65(x_0^2+x_1^2+x_3^2)+\frac25x_2^2
 \geq\frac25(x_0^2+r^2).
\]
Since
\((s_1(H)-s_2(H))^2=4\min(x_0^2,r^2)\), this is at least
\(\frac18(s_1(H)-s_2(H))^2\).

Even the known sharp two-sided projector-pair bounds can be made
simultaneously consistent with this model.  Assign the formal overlap
profile
\[
 r_x^2=\frac{1+n_x}{2}.
\]
With \(m=1/8\), one has
\[
 a-m=\frac{19}{40},\qquad
 g(P_x)-m=\frac{19-8n_y^2}{40}.
\]
The upper estimate
\[
 \frac35n_x\leq
 \frac18+\sqrt{(a-m)(g(P_x)-m)}
\]
is automatic for \(n_x\leq5/24\).  Otherwise, squaring and using
\(n_y^2\leq1-n_x^2\) reduces it to
\[
 8(1-n_x)(53n_x+23)\geq0.
\]
The lower estimate with the displayed overlap profile reduces, for
\(n_x<0\), to
\[
 19(11n_y^2+19n_z^2)\geq0,
\]
and is automatic for \(n_x\geq0\).  Thus the obstruction survives all
currently available scalar pair constraints.  The overlap profile is
only formal: no assertion is made that it and \(T\) arise from the same
physical anchor.

### 4.3 An off-diagonal dyad fails

Set \(u=|0\rangle\) and \(v=|1\rangle\).  Then
\(\operatorname{vec}(|u\rangle\langle v|)=|01\rangle\), so (24) gives
\[
 g(|0\rangle\langle1|)=\frac25.
\]
On the other hand \(v^\dagger Tu=3/5\).  Consequently
\[
\boxed{
 a\,g(|0\rangle\langle1|)
 =\frac6{25}<\frac9{25}=|v^\dagger Tu|^2.}               \tag{28}
\]
The exact complex-null defect is therefore \(-3/25\).

This is an exact rational counterexample to the abstract implication
(20)--(22).  It is not a counterexample to the physical three-copy
Werner endpoint: no claim is made that \(G\) and \(T\) arise together
from one physical triple \((w,u,v)\).  What it proves is that positivity,
quantitative PPT, swap invariance, the sharp swap-sector spectral
windows, and every diagonal rank-one test still fail to encode the
necessary common-origin geometry.
