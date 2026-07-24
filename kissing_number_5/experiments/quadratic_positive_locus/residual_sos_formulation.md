# Exact parameter-dependent kernel formulation

This note specifies a finite-degree certificate whose successful exact
instantiation would solve the residual quadratic-positive-locus occupancy
problem.  It does not assert that such a certificate exists at a particular
degree.

## Parameter set

Eliminate \(\lambda_5\) by setting it to one.  Let
\(\theta=(\lambda_1,\ldots,\lambda_4,b_1,\ldots,b_5)\), subject to
\[
\begin{aligned}
&\lambda_1+4\geq0,\quad
  \lambda_{i+1}-\lambda_i\geq0\ (1\leq i<4),\quad
  1-\lambda_4\geq0,\\
&b_i\geq0\ (1\leq i\leq5),\qquad
  2500-\sum_i b_i^2\geq0,\\
&1+\sum_{i=1}^4\lambda_i=0.
\end{aligned}
\tag{P}
\]
Call these inequality generators \(g_j(\theta)\geq0\) and the equality
\(h_\lambda(\theta)=0\).  This is a compact semialgebraic set with eight
degrees of freedom.

For \(x\in\mathbb R^5\), put
\[
q_\theta(x)=x_5^2+\sum_{i=1}^4\lambda_i x_i^2+
\sum_{i=1}^5b_i x_i.
\]

## Positive kernels without symmetry assumptions

Let \(\phi_d(x)\) be the vector of all monomials in five variables of total
degree at most \(d\).  Choose a symmetric polynomial matrix \(M(\theta)\)
of the matching size and define
\[
K_\theta(x,y)=\phi_d(x)^{\mathsf T}M(\theta)\phi_d(y).
\]
Require an exact matrix-SOS identity
\[
M(\theta)=R_0(\theta)^{\mathsf T}R_0(\theta)
+\sum_j g_j(\theta)R_j(\theta)^{\mathsf T}R_j(\theta)
+h_\lambda(\theta)H(\theta),
\tag{KPSD}
\]
where \(H\) is symmetric.  Therefore \(M(\theta)\succeq0\) on (P).  For any
finite set \(C\),
\[
\sum_{x,y\in C}K_\theta(x,y)
=\left(\sum_{x\in C}\phi_d(x)\right)^{\mathsf T}
 M(\theta)
\left(\sum_{x\in C}\phi_d(x)\right)\geq0.
\tag{1}
\]
Unlike a zonal Delsarte kernel, this kernel may adapt to every eigendirection
and linear component of the separating quadratic.

## Exact domain inequalities

Find a rational number \(D<40\) and exact SOS certificates for:

\[
D-K_\theta(x,x)\geq0
\tag{2}
\]
on
\[
\theta\in(P),\qquad \|x\|^2=1,\qquad q_\theta(x)\geq0,
\tag{D}
\]
and
\[
-1-K_\theta(x,y)\geq0
\tag{3}
\]
on
\[
\begin{split}
\theta\in(P),\quad &\|x\|^2=\|y\|^2=1,\\
q_\theta(x)&\geq0,\quad q_\theta(y)\geq0,\quad
\frac12-x\mathbin{\cdot}y\geq0.
\end{split}
\tag{O}
\]

For example, (3) must be supplied as a literal polynomial identity
\[
-1-K_\theta(x,y)
=\sigma_0+\sum_j\sigma_jg_j
+\sigma_xq_\theta(x)+\sigma_yq_\theta(y)
+\sigma_c(1/2-x\cdot y)
+a_x(1-\|x\|^2)+a_y(1-\|y\|^2)+a_\lambda h_\lambda,
\tag{4}
\]
where every \(\sigma\) is an explicitly factored sum of squares.  Products
of generators may be added if a preordering rather than the displayed
quadratic module is used.  Redundant exact ball constraints may be added to
make Archimedeanity manifest.  The diagonal identity is analogous.

Every coefficient in (KPSD) and (4), every Gram factor, and the comparison
\(D<40\) must be rational or exactly algebraic.  A checker need only expand
the identities, multiply exact matrices, and verify the stated factors.

## Summation lemma

Let \(N=|C|\).  If (1)--(3) hold for a fixed \(\theta\) and
\(C\subset\{q_\theta\geq0\}\) is a kissing code, then
\[
0\leq\sum_{x,y\in C}K_\theta(x,y)
\leq ND-N(N-1)=N(D-N+1).
\]
Thus \(N\leq D+1<41\), and integrality gives \(N\leq40\).

The use of \(D<40\), rather than a rounded numerical objective, is
essential.  All contact pairs and all points with \(q_\theta(x)=0\) are
included.

## Axisymmetric reduction

For either one-parameter family
\(q_\pm(t)\), averaging a candidate kernel over the stabilizer \(O(4)\)
preserves (1)--(3).  It can therefore be written in the usual
Bachoc--Vallentin block basis \(Y_k^5(u,v,t)\), with the height variables
restricted to the exact algebraic interval or union of intervals determined
by the roots of \(q_\pm\).  A parameter-uniform certificate treats
\(\beta\) as an additional variable and includes the polynomial inequality
\(q_\pm(u),q_\pm(v)\geq0\), avoiding square roots entirely.

This one-parameter problem is the first computational target.  The full
eight-parameter kernel is the symmetry-free endpoint.
