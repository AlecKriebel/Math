# Audit report

## Setup

Let the 18 antipodal pairs be \(\{\pm u_j\}\), and choose either sign as
the representative \(u_j\).  Let \(z_1,\ldots,z_5\) be the residual
vertices, whose strict deep graph is \(C_5\).  Write
\[
s_i=\langle z_i,z_{i+1}\rangle<-\frac12.
\]
The polynomial is
\[
q(t)=\frac{64}{315}
 +\frac{256}{135}P_2(t)
 +\frac{2048}{945}P_4(t)
=\frac{64}{45}t^2(4t^2-1).
\]

## Representative choice

For every other code point \(w\), the original code contains both \(u_j\)
and \(-u_j\).  The kissing inequalities give
\[
\langle u_j,w\rangle\leq\frac12,\qquad
-\langle u_j,w\rangle\leq\frac12.
\]
Therefore
\[
|\langle u_j,w\rangle|\leq\frac12.
\]
The same argument applies to two chosen representatives because both signs
of either pair occur in the original code.  Consequently every
representative--representative and representative--residual term lies in
the full closed interval \([-1/2,1/2]\), independently of the sign chosen
for each representative.

Since
\[
q(t)=\frac{64}{45}t^2(4t^2-1)\leq0
\quad\text{when }|t|\leq\frac12,
\]
all those off-diagonal terms are nonpositive.  Equality at
\(t=-1/2,0,1/2\) is harmless.  A residual nonedge also lies in this closed
interval.  The only potentially positive off-diagonal terms are the five
strict residual deep edges.

## Ordered-pair audit

The full 41-point sum has \(41\cdot40\) ordered off-diagonal pairs.  The 18
antipodal pairs account for \(2\cdot18=36\) ordered pairs.  Each of the
five undirected residual cycle edges occurs in both orientations, so its
contribution to an ordered sum has a factor of two.

After collapsing to 18 representatives plus five residual vertices, put
weight \(\lambda\geq0\) on every representative and weight \(a_i\geq0\)
on \(z_i\).  Harmonic positivity gives
\[
\sum_{v,w}a_va_wq(\langle v,w\rangle)
\geq\frac{64}{315}\left(18\lambda+A\right)^2,
\qquad A=\sum_i a_i.
\]
Dropping only nonpositive off-diagonal terms gives the upper estimate
\[
\sum_{v,w}a_va_wq(\langle v,w\rangle)
\leq18q(1)\lambda^2+q(1)S_2+2E,
\]
where
\[
q(1)=\frac{64}{15},\qquad
S_2=\sum_i a_i^2,\qquad
E=\sum_i a_i a_{i+1}q(s_i).
\]
Thus
\[
2E\geq R(\lambda):=
\frac{64}{315}(18\lambda+A)^2
-18\frac{64}{15}\lambda^2
-\frac{64}{15}S_2.
\tag{A}
\]

The exact expansion is
\[
R(\lambda)
=-\frac{384}{35}\lambda^2
 \frac{256}{35}A\lambda
 \frac{64}{315}A^2
-\frac{64}{15}S_2.
\]
It is concave, and its vertex is
\[
\lambda=\frac A3.
\]
This is admissible for every nonnegative weight vector, including the
all-zero boundary.  Substitution into (A) gives
\[
R(A/3)=\frac{64}{45}(A^2-3S_2)
\]
and hence
\[
E\geq\frac{32}{45}(A^2-3S_2).
\]
This is equation (15).  Taking every \(a_i=1\) gives
\[
\sum_iq(s_i)\geq\frac{64}{9},
\]
which is equation (14).

The inequality remains valid when some \(a_i=0\).  If the right side is
negative it is simply non-sharp; no division by a weight or strict
positivity assumption was used.

## Immediate edge-depth corollary

From the five-term bound, at least one edge has
\[
q(s_i)\geq\frac15\frac{64}{9}=\frac{64}{45}.
\]
Put \(u=s_i^2\).  Since \(s_i<-1/2\), one has \(u>1/4\), and
\[
q(s_i)\geq\frac{64}{45}
\quad\Longleftrightarrow\quad
u(4u-1)\geq1
\quad\Longleftrightarrow\quad
u\geq\frac{1+\sqrt{17}}8.
\]
The last equivalence is boundary-safe because \(4u^2-u-1\) is strictly
increasing for \(u\geq1/4\).  As \(s_i<0\), this proves
\[
\boxed{
s_i\leq-\sqrt{\frac{1+\sqrt{17}}8}
}
\approx-0.8002425902.
\]
All inequalities are inclusive at the forced threshold.

## Verdict and production-verifier coverage

No ordered/unordered factor error, representative-sign error, arbitrary
weight error, or boundary loss was found.  Equations (12)--(15) and the
edge-depth corollary are mathematically valid.

The production verifier correctly checks the polynomial coefficients and
the two scalar bounds.  However, it merely compares the stored
`copositive_constant` with \(32/45\); it does not derive the
arbitrary-weight quadratic identity.  It also does not machine-check the
sign of \(q\) on the full closed interval or the representative absolute
inner-product argument.  These are verification-coverage gaps, not
mathematical counterexamples.  The independent checker in this folder
derives the exact quadratic coefficients and threshold algebra.
