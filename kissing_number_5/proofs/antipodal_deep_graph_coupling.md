# Antipodal pairs force sparse residual deep graphs

Let \(C=\{x_1,\ldots,x_{41}\}\subset S^4\) be a hypothetical kissing
configuration, and let \(H\) be its strict deep-pair graph:

\[
 ij\in E(H)\quad\Longleftrightarrow\quad
 \langle x_i,x_j\rangle<-\frac12 .
\]

The already proved projective reduction gives

\[
 H\text{ is triangle-free},\qquad \alpha(H)\leq20.       \tag{1}
\]

This note records an exact coupling between the number of antipodal pairs
and the rest of \(H\).  It is stronger than imposing the antipodal-pair and
deep-edge bounds separately.

## The graph coupling

Suppose that \(C\) contains exactly \(r\) antipodal pairs.  Every such pair
\(\{x,-x\}\) is an isolated \(K_2\) component of \(H\).  Indeed, if a third
point \(z\) obeyed

\[
 \langle x,z\rangle<-\frac12,
\]

then

\[
 \langle -x,z\rangle=-\langle x,z\rangle>\frac12,
\]

contrary to the kissing inequality.  The same argument with \(x\) and
\(-x\) exchanged excludes every other deep edge incident to the pair.

Delete these \(r\) isolated edges and call the residual graph \(H_0\).  Put

\[
 n=41-2r,\qquad a=20-r.
\]

Then

\[
 H_0\text{ is triangle-free},\qquad \alpha(H_0)\leq a.  \tag{2}
\]

For the second assertion, an independent set of \(a+1=21-r\) residual
vertices, together with one representative from each antipodal pair, would
be an independent set of 21 vertices in \(H\), contradicting (1).

First observe that \(r\leq18\).  If \(r=19\), then \(H_0\) has three
vertices and independence number at most one, forcing a triangle; if
\(r=20\), its single residual vertex itself is an independent set, whereas
(2) would require independence number zero.  Thus \(a=20-r\geq2\) in every
branch still under consideration.

In a triangle-free graph the neighborhood of every vertex is independent.
Equation (2) therefore gives

\[
 \Delta(H_0)\leq a.
\]

The fact that \(H_0\) has odd order \(2a+1\) improves the handshake bound.
We use the following elementary lemma.

**Lemma.** If a triangle-free graph \(F\) has \(2a+1\) vertices and
\(\alpha(F)\leq a\), where \(a\geq2\), then

\[
 e(F)\leq a^2+1.                                      \tag{3}
\]

For \(a=2,3\), every neighborhood is independent, so
\(\Delta(F)\leq a\), and the handshake lemma gives (3).  Suppose \(a\geq4\)
and, for contradiction, that \(e(F)\geq a^2+2\).  Put

\[
 \delta_x=a-d(x),\qquad
 D=\sum_x\delta_x=a(2a+1)-2e(F)\leq a-4.              \tag{4}
\]

Some vertex \(v\) has degree \(a\): otherwise every degree is at most
\(a-1\), which is already incompatible with \(e(F)\geq a^2+2\).
Let \(A=N(v)\), and let \(B\) be the \(a\) vertices outside
\(\{v\}\cup A\).  The set \(A\) is independent.  Write

\[
 D_A=\sum_{x\in A}\delta_x,\qquad
 D_B=\sum_{x\in B}\delta_x,\qquad m=e(F[B]).
\]

Counting degrees first on \(A\) and then on \(B\) gives

\[
\begin{aligned}
 e(A,B)&=a(a-1)-D_A,\\
 a^2-D_B&=e(A,B)+2m.
\end{aligned}
\]

Consequently

\[
 m+D_B+1=\frac{a+D}{2}+1\leq a-1.                    \tag{5}
\]

Also \(m=(a+2D_A-D)/2\geq(a-D)/2\geq2\), so \(F[B]\)
has an edge.  Take one such edge \(yz\), and write
\(q_y=d_{F[B]}(y)\), \(q_z=d_{F[B]}(z)\).  Triangle-freeness makes the
two \(A\)-neighborhoods of \(y,z\) disjoint.  Hence

\[
 (a-\delta_y-q_y)+(a-\delta_z-q_z)\leq a,
\]

or

\[
 q_y+q_z+\delta_y+\delta_z\geq a.                    \tag{6}
\]

On the other hand, the edges of \(F[B]\) incident with \(y\) or \(z\)
form a union of \(q_y+q_z-1\) edges, so \(q_y+q_z\leq m+1\).
Also \(\delta_y+\delta_z\leq D_B\).  Equation (5) therefore makes the
left side of (6) at most \(a-1\), a contradiction.  This proves the lemma.

Applying the lemma to \(H_0\) proves the branchwise bound

\[
 \boxed{\;
 e(H)\leq r+(20-r)^2+1 .
 \;}                                                    \tag{7}
\]

This includes all boundary cases because \(H\) uses the strict threshold
\(-1/2\).  A pair at inner product exactly \(-1/2\) is not a deep edge and
is not removed by the argument.

The most relevant endpoint values are

\[
\begin{array}{c|c|c|c}
r&|V(H_0)|&\alpha(H_0)\text{ upper bound}&e(H)\text{
 upper bound}\\ \hline
18&5&2&23\\
17&7&3&27\\
16&9&4&33\\
15&11&5&41\\
14&13&6&51.
\end{array}
\]

In particular, the universal lower bound \(e(H)\geq23\) makes the \(r=18\)
branch an equality case.  Then \(H_0\) has five vertices, independence
number at most two, and five edges, so \(H_0\cong C_5\); hence

\[
 H\cong18K_2\sqcup C_5.
\]

## An exact weighted constraint on the residual \(C_5\)

The equality case has a useful continuous consequence that does not assume
a finite inner-product alphabet.  In dimension five, use the normalized
Gegenbauer polynomials

\[
 P_2(t)=\frac{5t^2-1}{4},\qquad
 P_4(t)=\frac{21t^4-14t^2+1}{8},
\]

and define

\[
\begin{aligned}
q(t)
 &=\frac{64}{315}
   +\frac{256}{135}P_2(t)
   +\frac{2048}{945}P_4(t)\\
 &=\frac{64}{45}t^2(4t^2-1).                         \tag{8}
\end{aligned}
\]

Both nonconstant Gegenbauer coefficients are positive.  Harmonic
positivity therefore gives

\[
\begin{aligned}
\sum_{\substack{x,y\in C\\x\ne y}}q(\langle x,y\rangle)
&\geq
41\cdot40\cdot\frac{64}{315}
-41\left(\frac{256}{135}+\frac{2048}{945}\right)\\
&=\frac{10496}{63}.                                  \tag{9}
\end{aligned}
\]

The 36 ordered pairs belonging to the 18 antipodal pairs contribute

\[
36q(-1)=36\cdot\frac{64}{15}=\frac{768}{5}.           \tag{10}
\]

Every other ordered pair outside the residual \(C_5\) has absolute inner
product at most \(1/2\).  Since \(q(t)\leq0\) on
\([-1/2,1/2]\), those pairs make a nonpositive contribution.  If

\[
s_i=\langle z_i,z_{i+1}\rangle<-\frac12
\quad(i\ {\rm mod}\ 5)
\]

are the five residual cycle inner products, (9)--(10) imply the exact
weighted bound

\[
\boxed{\quad
 \sum_{i=1}^{5}q(s_i)\geq\frac{2048}{315}.
\quad}                                                \tag{11}
\]

Arbitrary nonnegative weights strengthen (11).  Collapse each antipodal
pair to a representative \(u_j\), assign all 18 representatives weight
\(\lambda\geq0\), and assign each residual vertex weight one.  The positive
Gegenbauer expansion of \(q\) gives

\[
\sum_{v,w}a_va_wq(\langle v,w\rangle)
\geq\frac{64}{315}(18\lambda+5)^2.                    \tag{12}
\]

All off-diagonal \(u\)-\(u\) and \(u\)-\(z\) terms are nonpositive.
Dropping them from the upper side of (12), and retaining only the diagonal
and residual-cycle terms, gives

\[
2\sum_{i=1}^{5}q(s_i)
\geq
\frac{64}{315}(18\lambda+5)^2
-18\frac{64}{15}\lambda^2
-5\frac{64}{15}.                                     \tag{13}
\]

The right side is a concave quadratic whose maximum occurs at
\(\lambda=5/3\).  Therefore

\[
\boxed{\quad
 \sum_{i=1}^{5}q(s_i)\geq\frac{64}{9}.
\quad}                                                \tag{14}
\]

More generally, giving the five residual vertices arbitrary nonnegative
weights \(a_1,\ldots,a_5\), and optimizing the common representative weight
at \(\lambda=(a_1+\cdots+a_5)/3\), proves the copositive family

\[
\sum_{i=1}^{5}a_i a_{i+1}q(s_i)
\geq
\frac{32}{45}
\left[
  \left(\sum_{i=1}^{5}a_i\right)^2
  -3\sum_{i=1}^{5}a_i^2
\right].                                             \tag{15}
\]

This also explains why the coarser quarter-grid relaxation rejects the
branch: at its only strict-deep grid node \(t=-3/4\), one has \(q(t)=1\),
whereas \(64/9>5\).  That finite-grid contradiction is not a continuous
proof.  For example, \(q(t)>1\) when \(t<-3/4\), so (14)--(15) do not by
themselves eliminate a genuine residual pentagon.

## Odd-harmonic cancellation on each branch

There is a compatible analytic consequence.  Let \(P_k\) be the normalized
dimension-five Gegenbauer polynomial and let \(\Phi_k\) be a normalized
spherical-harmonic feature map, so that

\[
 P_k(\langle x,y\rangle)
 =\langle\Phi_k(x),\Phi_k(y)\rangle,\qquad
 \|\Phi_k(x)\|=1.
\]

For odd \(k\), parity gives
\(\Phi_k(-x)=-\Phi_k(x)\).  All \(r\) antipodal pairs therefore cancel from
the harmonic sum.  If \(z_1,\ldots,z_n\) are the unpaired points, then

\[
\begin{aligned}
\sum_{x,y\in C}P_k(\langle x,y\rangle)
 &=\left\|\sum_{x\in C}\Phi_k(x)\right\|^2\\
 &=\left\|\sum_{j=1}^{n}\Phi_k(z_j)\right\|^2
 \leq n^2.                                             \tag{16}
\end{aligned}
\]

For \(k=1\), the kissing inequality sharpens the last bound:

\[
\left\|\sum_{j=1}^{n}z_j\right\|^2
=n+2\sum_{i<j}\langle z_i,z_j\rangle
 \leq n+\binom n2=\frac{n(n+1)}2.                       \tag{17}
\]

In the average ordered pair-distribution normalization
\(\sum_t\alpha_t=40\), equations (8)--(9) become

\[
1+\sum_t\alpha_tP_k(t)\leq\frac{(41-2r)^2}{41}
\quad(k\text{ odd}),                                  \tag{18}
\]

and

\[
1+\sum_t\alpha_t t
\leq\frac{(41-2r)(42-2r)}{82}.                         \tag{19}
\]

These are necessary conditions on every exact antipodal-count branch.
They do not assume that the rest of the code is antipodal, centered,
rigid, or supported on a finite inner-product alphabet.

## Scope

The inequalities above do not exclude all branches and therefore do not
resolve the five-dimensional kissing problem.  Their immediate use is to
prevent a relaxation from combining the energy contribution of eighteen
antipodal pairs with a residual deep graph that could not fit on the five
remaining vertices.
