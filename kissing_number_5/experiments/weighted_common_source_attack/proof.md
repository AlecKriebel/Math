# Exact consequences and barriers for weighted isotropy

## Scope

Throughout this note \(G\) is an \(N\)-by-\(N\) real symmetric matrix and
\(P=\operatorname{diag}(p)\), where
\[
G\succeq0,\quad G_{ii}=1,\quad p\geq0,\quad {\bf1}^{\mathsf T}p=1,
\quad Gp=0,\quad GPG=\frac15G.                    \tag{1}
\]
When \(G_{ij}\leq1/2\) off the diagonal, (1) is precisely the
weighted-isotropy branch of the five-dimensional kissing problem.  The
results below do **not** rule out \(N=41\).

## 1. The quadratic matrix identity recovers rank five

The rank hypothesis is redundant once the full identity \(GPG=G/5\) is
retained.

**Lemma 1.**  If \(G\succeq0\), \(G_{ii}=1\),
\({\bf1}^{\mathsf T}p=1\), and \(GPG=G/5\), then
\(\operatorname{rank}G=5\), even when some \(p_i\) vanish.

**Proof.**  Factor \(G=XX^{\mathsf T}\), where \(X\) has \(r\) columns
and full column rank, with \(r=\operatorname{rank}G\).  A left inverse
of \(X\), applied to
\[
X(X^{\mathsf T}PX)X^{\mathsf T}=\frac15XX^{\mathsf T},
\]
gives
\[
X^{\mathsf T}PX=\frac15I_r.
\]
Taking traces and using \(G_{ii}=1\) gives
\[
\frac r5=\operatorname{tr}(X^{\mathsf T}PX)
=\operatorname{tr}(PG)=\sum_i p_i=1.
\]
Thus \(r=5\).  Notice that deleting the quadratic identity, or checking it
only on the positive-weight principal block, would invalidate this
argument. \(\square\)

## 2. Euclidean-distance common-source identity

Put
\[
D=2(J-G).
\]
Thus \(D_{ii}=0\), while for a kissing code
\[
1\leq D_{ij}\leq4\qquad(i\ne j).
\]
Expanding (1) gives the especially simple identities
\[
\boxed{Dp=2{\bf1}},                                    \tag{2}
\]
\[
\boxed{DPD=\frac{24}{5}J-\frac25D.}                   \tag{3}
\]
Indeed, (2) is \(2(J-G)p=2{\bf1}\), and
\[
DPD=4(J-G)P(J-G)=4J+\frac45G
=\frac{24}{5}J-\frac25D.
\]

Let \(v=\sqrt p\) and
\[
Q=P^{1/2}DP^{1/2}.
\]
Equations (2)--(3) become
\[
Qv=2v,\qquad
Q^2=\frac{24}{5}vv^{\mathsf T}-\frac25Q.              \tag{4}
\]
As \(\|v\|=1\), every eigenvalue on \(v^\perp\) is \(0\) or \(-2/5\).
Also \(\operatorname{tr}Q=0\), so the exact spectrum is
\[
\boxed{\operatorname{Spec}Q=
\{2,(-2/5)^5,0^{\,N-6}\}.}                            \tag{5}
\]
Equivalently,
\[
T=\frac12DP
\]
is a reversible row-stochastic matrix with stationary distribution \(p\)
and
\[
\boxed{T^2=\frac65{\bf1}p^{\mathsf T}-\frac15T},\qquad
\operatorname{Spec}T=\{1,(-1/5)^5,0^{\,N-6}\}.         \tag{6}
\]
Zero weights cause zero columns in \(T\), but do not invalidate (2)--(6).

## 3. The Naimark stress and all-subset inequalities

Let the rows of \(X\) be the unit vectors \(x_i\).  The \(N\)-by-6 matrix
whose \(i\)-th row is
\[
\sqrt{p_i}(1,\sqrt5\,x_i)
\]
has orthonormal columns.  Consequently
\[
R=I-\sqrt p\sqrt p^{\mathsf T}
  -5P^{1/2}GP^{1/2}\succeq0.
\]
After congruence by \(P^{1/2}\),
\[
\boxed{\Omega=P-pp^{\mathsf T}-5PGP\succeq0.}          \tag{7}
\]
For every subset \(A\), applying (7) to its indicator gives
\[
\boxed{
5\left\|\sum_{i\in A}p_ix_i\right\|^2
\leq p(A)(1-p(A)).
}                                                       \tag{8}
\]
The one-point case recovers
\[
p_i\leq\frac16.                                        \tag{9}
\]
The two-by-two principal minors give the pairwise refinement
\[
\boxed{
p_ip_j(1+5G_{ij})^2
\leq(1-6p_i)(1-6p_j).
}                                                       \tag{10}
\]
All formulas remain valid at zero weights, where (10) becomes vacuous.

There is a second pair bound directly from the distance common-source
identity.  For \(i\ne j\), write \(t=G_{ij}\).  For any third point \(k\),
put \(u=G_{ik}\), \(w=G_{jk}\).  Since \(1-u,1-w\geq0\),
\[
\begin{aligned}
D_{ik}D_{jk}
&=4(1-u)(1-w)\\
&\leq4\left(1-\frac{u+w}{2}\right)^2\\
&\leq4\left(1+\sqrt{\frac{1+t}{2}}\right)^2.
\end{aligned}
\]
The final inequality uses
\(u+w=\langle x_i+x_j,x_k\rangle\geq-\|x_i+x_j\|\).
The \(k=i,j\) terms vanish in (3), hence
\[
\boxed{
p_i+p_j\leq
1-\frac{1+t/5}
        {\left(1+\sqrt{(1+t)/2}\right)^2}.
}                                                       \tag{11}
\]
In particular, an antipodal positive-weight pair has total weight at most
\(1/5\).

## 4. A sparse support is always available

Map \(x\in S^4\) to
\[
\left(x,\ xx^{\mathsf T}-\frac15I\right).
\]
The second coordinate lies in the 14-dimensional space of traceless
symmetric matrices, so the lifted space has dimension \(5+14=19\).
Weighted centering and isotropy say that the origin lies in the convex hull
of the lifted code points.  Carathéodory's theorem therefore gives:

\[
\boxed{\text{The weights may always be chosen with support at most }20.}
\tag{12}
\]

This is only a reduction, not an obstruction.  Support sizes six through
ten already occur among exact kissing codes.  For any partition
\[
5=d_1+\cdots+d_r,
\]
take mutually orthogonal regular \(d_a\)-simplices.  Give each of the
\(d_a+1\) vertices in component \(a\) weight
\[
\frac{d_a}{5(d_a+1)}.
\]
The union is a weighted spherical two-design, has
\(5+r\) support points, and all cross-component inner products are zero.
As \(r=1,\ldots,5\), every support size from six through ten occurs.

More seriously, the exact \(D_5\) 40-point kissing code admits weights
supported on only 12 points.  In the verifier's deterministic root order,
the positive entries are
\[
\begin{array}{c|c}
\text{indices}&p_i\\ \hline
9,11,16,17,26,27,28,30&1/10\\
12,13,14,15&1/20 .
\end{array}                                             \tag{13}
\]
Thus a genuine 40-point code satisfying the complete common-source
identities can already have 28 zero-weight vertices.  Merely replacing a
hypothetical 41-point problem by “a support of size at most 20 plus
zero-weight extensions” leaves essentially the original extension
difficulty.

## 5. Exact zero-point moment constraints

Let \(y\) be a zero-weight code point and set
\(t_i=\langle y,x_i\rangle\) on the positive support.  Then
\[
\sum_i p_it_i=0,\qquad \sum_i p_it_i^2=\frac15,\qquad
-1\leq t_i\leq\frac12.                                \tag{14}
\]
For \(0\leq a<2/5\), the polynomial
\[
\phi_a(t)=(t+a)(1/2-t)
\]
is nonnegative on \([-a,1/2]\), is bounded below by
\(-3(1-a)/2\) on \([-1,-a]\), and has weighted expectation
\(a/2-1/5\).  Therefore
\[
\boxed{
\sum_{t_i<-a}p_i\geq\frac{2-5a}{15(1-a)}.
}                                                       \tag{15}
\]
In particular the support mass in the open negative hemisphere is at
least \(2/15\), and the mass below \(-1/4\) is at least \(1/15\).
At the endpoint \(a=2/5\), (14) shows that some support point satisfies
\(t_i\leq-2/5\); equality throughout forces every positive-weight height
to lie in \(\{-2/5,1/2\}\).

The positive tail is stronger.  For \(0\leq b<1/5\), use
\[
\psi_b(t)=(t+1)(b-t).
\]
This is nonnegative on \([-1,b]\), is bounded below by
\(-3(1/2-b)/2\) on \([b,1/2]\), and has expectation \(b-1/5\).
The negative region is the strict set \(t>b\); the boundary \(t=b\)
contributes zero.  Therefore
\[
\boxed{
\sum_{t_i>b}p_i\geq
\frac{4(1-5b)}{15(1-2b)}.
}                                                       \tag{16}
\]
At \(a=b=1/50\), the two exact bounds are respectively
\[
\sum_{t_i<-1/50}p_i\geq\frac{19}{147},\qquad
\sum_{t_i>1/50}p_i\geq\frac14.
\]
These bounds apply specifically to a zero-weight point.  A
positive-weight code point contributes a self atom at \(t=1\), so it
cannot be inserted into this off-diagonal support interval without a
separate correction.

Combining (8) with
\(\left\langle y,\sum_{i\in A}p_ix_i\right\rangle<-ap(A)\)
also gives, for \(A=\{i:t_i<-a\}\),
\[
p(A)\leq\frac1{1+5a^2}.                                \tag{17}
\]
The lower and upper bounds (15)--(17) have a wide gap and do not rule out
even one zero-weight point.  The sparse \(D_5\) model (13), with 28 such
points, is an exact adversarial instance.

## 6. The weighted row-energy identity and its exact barrier

For \(N=41\), taking diagonal entries of \(GPG=G/5\) and summing yields
\[
\boxed{
\sum_i p_i\sum_jG_{ij}^2=\frac{41}{5}.
}                                                       \tag{18}
\]
A universal local inequality
\(\sum_jG_{ij}^2\leq41/5\) would therefore be extremely attractive.
It is false.

`local_row_energy_counterexample.json` contains 25 exact rational unit
vectors with every distinct inner product strictly below \(1/2\), while
the row anchored at \(e_1\) has
\[
\sum_j\langle e_1,x_j\rangle^2>\frac{41}{5}.
\]
The certificate was discovered under the stricter floating-point cap
0.492 and then rationalized by stereographic parametrization.  The
standard-library verifier ignores the optimizer report, reconstructs all
rational coordinates, checks all norms and all 300 pairs exactly, and
checks the strict energy inequality.  Thus no numerical tolerance enters
the counterexample.

## 7. Exact remaining gap

The unresolved task on this branch is still to rule out 41 points
satisfying (1) and \(G_{ij}\leq1/2\).  The exact reductions above show why
three natural shortcuts fail:

1. rank cannot be dropped before the quadratic identity, although the
   full identity itself recovers rank five;
2. sparse-support reduction alone is weak, because an exact 40-point code
   already has a 12-point design support and 28 zero-weight extensions;
3. the weighted average (18) cannot be closed by a universal pointwise
   row-energy bound at \(41/5\).

A successful continuation must couple several zero-weight points to the
same small support, using their mutual kissing inequalities.  The
one-point mass bounds (15)--(17) and support-pair inequalities (10)--(11)
do not yet supply that multi-extension compatibility.
