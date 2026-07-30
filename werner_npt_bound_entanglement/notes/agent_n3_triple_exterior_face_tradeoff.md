# The triple-skew exterior tradeoff in the common face variables

## Status

This note feeds the proved sharp triple-skew stable-rank theorem back
into the unrestricted three-copy face reduction.  It gives a new exact
nonlinear realizability inequality
\[
 \boxed{\qquad
 320R+28S\geq468c+405a+144\Delta ,
 \qquad}                                                   \tag{1}
\]
where \(R,S\) are the sums of the three rank-six and block-Haar face
slacks, \(a,c\) are the one- and two-traceless sector masses, and
\[
 \Delta=(s_1(C)-s_2(C))^2 .
\]

The common origin of (1) is the exterior mass
\[
 p=s_1(C)s_2(C)=\|\bigwedge^2C\|_2.
\]
Before eliminating \(p\), the sharper form is
\[
 \boxed{\qquad
 128R+4S+96p\geq252c+243a .
 \qquad}                                                   \tag{2}
\]
It is exactly the rank-two triple-Hodge inequality
\[
 {\cal J}_3(C)+\frac13p\geq0                             \tag{3}
\]
written in the common face coordinates.  Thus this is not another
linear sector inequality: the term \(p\) remembers the two common
singular planes.

For a hypothetical negative direction of generalized depth
\(\delta\), (1) gives
\[
 \boxed{\qquad
 2556\delta+
 459(1-5\delta)L+
 405a+144\Delta\leq324 ,
 \qquad}                                                   \tag{4}
\]
where \(L=\sum_i\theta_i\lambda_i>0\) is the exact face-simplex
coordinate.  Consequently every negative direction satisfies
\[
 \boxed{\qquad 0<\delta<\frac9{71}. \qquad}               \tag{5}
\]
This improves the preceding explicit bound \(3/22\).

The result still does not prove unrestricted three-copy positivity.
It shows, however, that the sharp triple-skew theorem supplies a
global pair/triple constraint after the common exterior mass is
retained; using only the separated bound
\({\cal C}(Q_{(3)})\leq8/27\) would hide (2).

The dependency-free exact checker is
`verification/verify_n3_triple_exterior_face_tradeoff.py`.

## 1. The triple-Hodge form

For a coefficient matrix \(C\), put
\[
\begin{aligned}
 N&=\|C\|_2^2,\\
 T_1&=\sum_i\|\operatorname{Tr}_iC\|_2^2,\\
 T_2&=\sum_{i<j}\|\operatorname{Tr}_{ij}C\|_2^2,\\
 T_3&=|\operatorname{Tr}C|^2.
\end{aligned}
\]
The partial transpose of the all-locally-antisymmetric feature has
quadratic form
\[
 {\cal J}_3(C)
 =\frac18(N-T_1+T_2-T_3).                                \tag{6}
\]

### Lemma 1.1

If \(\operatorname{rank}C\leq2\), then
\[
 \boxed{\qquad
 {\cal J}_3(C)\geq-\frac13s_1(C)s_2(C).
 \qquad}                                                   \tag{7}
\]

### Proof

First suppose that \(C\) has rank two and put
\[
 p=s_1(C)s_2(C)>0.
\]
Use its singular-value decomposition to write
\[
 C=U
 \begin{pmatrix}s_1&0\\0&s_2\end{pmatrix}
 V^\dagger ,
\]
where \(U,V:\mathbb C^2\to(\mathbb C^3)^{\otimes3}\) are
isometries.  Set
\[
 A=B=p^{-1/4}
 \begin{pmatrix}\sqrt{s_1}&0\\0&\sqrt{s_2}\end{pmatrix}.
\]
Then \(A,B\in SL(2,\mathbb C)\) and
\[
 \frac C{\sqrt p}=(UA)(VB)^\dagger.                     \tag{8}
\]

Let \(Q_{(3)}(U,V)\) be the logical two-qubit compression of
\[
 \frac89{\mathsf A}_1{\mathsf A}_2{\mathsf A}_3,
 \qquad {\mathsf A}_i=\frac{I-F_i}{2}.
\]
The proved sharp triple-skew stable-rank theorem, together with its
Takagi variational reduction, says
\[
 {\cal C}(Q_{(3)}(U,V))\leq\frac8{27}.                  \tag{9}
\]
Homogeneous concurrence is invariant under determinant-one logical
filters.  Its filtered-swap variational formula and the exact
partial-transpose contraction give
\[
\begin{aligned}
 -\frac89{\cal J}_3(C/\sqrt p)
 &=-\operatorname{Tr}\!\left[
 F_{\rm L}(A\otimes B)Q_{(3)}(U,V)
 (A\otimes B)^\dagger\right]\\
 &\leq{\cal C}(Q_{(3)}(U,V))
 \leq\frac8{27}.                                        \tag{10}
\end{aligned}
\]
Since \({\cal J}_3\) is quadratic, (10) is exactly (7).

If \(C\) has rank one, its coefficient vector is a product vector.
Partial transposition moves that product vector to another product
vector, so positivity of
\({\mathsf A}_1{\mathsf A}_2{\mathsf A}_3\) gives
\({\cal J}_3(C)\geq0\).  Here \(s_2=0\), and (7) follows.
\(\square\)

The constant is sharp.  Equality in (7) forces equality in (9) and
in the particular filtered-swap test in (10).  The equality
classification of the stable-rank theorem therefore places the two
underlying singular planes in the common-factor orbit.  In
particular, equality is disjoint from a negative endpoint direction:
that orbit has a two-dimensional one-site local support and is covered
by the established local-support-boundary theorem.

## 2. Conversion to face coordinates

Use the orthogonal scalar/traceless decomposition
\[
\begin{aligned}
 x&=\|\Pi_0C\|_2^2,\\
 a&=\sum_{|I|=1}\|\Pi_IC\|_2^2,\\
 c&=\sum_{|I|=2}\|\Pi_IC\|_2^2,\\
 d&=\|\Pi_3C\|_2^2 .
\end{aligned}                                             \tag{11}
\]
On one local qutrit, the partially transposed antisymmetric projector
has eigenvalue \(-1\) on the scalar operator direction and \(1/2\)
on the traceless direction.  Hence (6) is equivalently
\[
 \boxed{\qquad
 {\cal J}_3(C)=-x+\frac12a-\frac14c+\frac18d .
 \qquad}                                                   \tag{12}
\]

The exact summed face identities are
\[
 R=\frac32c+3a-\frac94x,\qquad
 S=9d+\frac34a-3c.                                      \tag{13}
\]
Solving them gives
\[
 x=\frac23c+\frac43a-\frac49R,\qquad
 d=\frac19S-\frac1{12}a+\frac13c.                       \tag{14}
\]
Substitute (14) into \(24({\cal J}_3+p/3)\).  There is no
inequality in this step:
\[
\boxed{
 24\left({\cal J}_3(C)+\frac p3\right)
 =
 \frac{32}{3}R+\frac13S-\frac{81}{4}a-21c+8p .
}                                                        \tag{15}
\]
Multiplying (15) by \(12\) and using Lemma 1.1 proves (2).

To eliminate \(p\), note that
\[
 N=x+a+c+d
 =2c+\frac94a+\frac19(S-4R),                            \tag{16}
\]
and, for rank at most two,
\[
 2p=N-\Delta.                                           \tag{17}
\]
Substitution of (16)--(17) into (2), followed by multiplication by
three, gives exactly (1).

Both (1) and (2) are strict on the negative endpoint locus.  Indeed,
equality would force equality in Lemma 1.1, hence the common-factor
local-support orbit described after its proof, where endpoint
negativity is already excluded.

## 3. Consequence for a hypothetical negative direction

Normalize the exact negative-depth simplex by
\[
 \langle S_V\rangle=1,\qquad
 \langle H_V\rangle=-\delta,\qquad \delta>0.
\]
Its established coordinates obey
\[
\begin{aligned}
 c&=\frac{1+\delta}{3},\\
 R&=\frac32(1-5\delta)(1-L),\\
 S&=\frac34(1-5\delta)L,\\
 L&=\sum_i\theta_i\lambda_i>0.
\end{aligned}                                             \tag{18}
\]
Insert (18) into (1).  Exact simplification gives
\[
 (1-5\delta)(480-459L)
 \geq156(1+\delta)+405a+144\Delta,
\]
which is (4).

All terms following \(2556\delta\) in (4) are nonnegative, and the
\(L\)-term is strictly positive because the face theorem gives
\(\theta_i>0\), \(0<\lambda_i\leq1\), and
\(\delta<1/5\).  Therefore
\[
 2556\delta<324,
\]
which reduces to (5).

Approaching the new formal endpoint \(9/71\) would force
simultaneously
\[
 (1-5\delta)L\longrightarrow0,\qquad
 a\longrightarrow0,\qquad
 \Delta\longrightarrow0,
\]
as well as asymptotic saturation of the sharp triple-skew
stable-rank theorem.  Its exact equality classification then points
back toward the already positive common-factor boundary.  Turning
this qualitative incompatibility into a global quantitative lower
bound is the next stability problem; (4) alone does not force
\(\delta=0\).
