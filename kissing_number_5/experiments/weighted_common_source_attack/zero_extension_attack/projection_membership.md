# A single exact quadratic equality recovers support realization

Let \(S\) be the Gram matrix of the positive-weight support, let
\(P=\operatorname{diag}(p)\), and assume
\[
Sp=0,\qquad SPS=\frac15S,\qquad p>0,\qquad
{\bf1}^{\mathsf T}p=1.
\]
Put
\[
K=5P^{1/2}SP^{1/2}.
\]
Then \(K\) is an orthogonal projection of rank five and
\(K\sqrt p=0\).

Consider a proposed height vector \(h\), intended to mean
\[
h_i=\langle x_i,y\rangle
\]
for one additional unit point \(y\).  Suppose only that
\[
h^{\mathsf T}Ph=\frac15.
\tag{1}
\]
Writing \(z=P^{1/2}h\), projection positivity gives
\[
\begin{aligned}
h^{\mathsf T}PSPh
&=\frac15z^{\mathsf T}Kz\\
&\leq\frac15z^{\mathsf T}z
=\frac1{25}.                                         \tag{2}
\end{aligned}
\]
Moreover, equality in (2) holds if and only if \(Kz=z\), because
\[
\frac1{25}-h^{\mathsf T}PSPh
=\frac15\|(I-K)z\|^2.                                \tag{3}
\]
Since every support weight is positive, \(Kz=z\) is equivalent to
\[
\boxed{h=5SPh.}                                      \tag{4}
\]

Thus the twelve or twenty separate-looking column-space equations can be
replaced by the single exact quadratic equality
\[
\boxed{h^{\mathsf T}PSPh=\frac1{25}.}                \tag{5}
\]

When (5) holds, define
\[
y=5\sum_i p_ih_ix_i.
\]
Then (4) gives \(\langle x_j,y\rangle=h_j\) for every support point, and
\[
\|y\|^2=25h^{\mathsf T}PSPh=1.
\]
Consequently (1), (5), and the coordinate inequalities \(h_i\leq1/2\)
are an exact realization test for one proposed extension point.

For two realized profiles \(h,k\),
\[
\langle y,z\rangle
=25h^{\mathsf T}PSPk
=5h^{\mathsf T}Pk.                                   \tag{6}
\]
Therefore the additional inequality
\[
h^{\mathsf T}Pk\leq\frac1{10}
\]
is exactly the kissing constraint between the two extension points.

This gives a bidirectional support-extension formulation.  It is not an
upper bound: for a six-point regular-simplex support, (4) merely describes
the whole five-dimensional sum-zero height subspace.  Its value is to
identify precisely which equality the triangle-level scalar
countermodel omits.
