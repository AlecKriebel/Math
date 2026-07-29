# A quantitative local-support floor at a pair-sector critical point

## Status

This note strengthens the qualitative full-local-support remainder for
the qutrit three-copy pair sector.  If an interior rank-two critical
point had pair-sector quotient \(f>2/3\), then every one of its six
left/right one-site density matrices would have to be uniformly
positive:
\[
 \lambda_{\min}(\rho_i^{L,R})
 \geq 1-\frac{2}{3f}.                                    \tag{1}
\]
The estimate is exact and follows only from:

1. the critical local-filter Hessian;
2. the established local-support-boundary theorem;
3. the best rank-two approximation of a full-rank \(3\times3\)
   matrix.

The abstract argument is sharp.  Consequently (1) cannot by itself
prove \(f\leq2/3\); a further tensor-specific relation among the six
local filters is essential.

This is a localization theorem for a hypothetical counterexample, not
a proof of the pair-sector theorem.  The independent exact checker is
`verification/verify_n3_pair_critical_local_spectral_floor.py`.

## 1. Critical local-filter forms

Let \({\cal P}=\Pi_2\), normalize \(\|C\|_2=1\), and suppose that
\[
 f=\|{\cal P}C\|_2^2
\]
is a local maximum on the smooth rank-two stratum.  Fix one left
physical site and put
\[
 \rho=\operatorname{Tr}_{\widehat i}(CC^\dagger).
\]
The qualitative boundary theorem already handles singular \(\rho\),
so assume \(\rho>0\).  For \(A,B\in M_3\), define
\[
\begin{aligned}
 {\cal N}(A,B)&=\operatorname{Tr}(A^\dagger B\rho),\\
 {\cal G}(A,B)&=
 \langle{\cal P}(A_iC),{\cal P}(B_iC)\rangle,\\
 {\cal W}(A,B)&=\frac23{\cal N}(A,B)-{\cal G}(A,B).
\end{aligned}                                             \tag{2}
\]
The complete critical equations and local-filter Hessian give
\[
\begin{aligned}
 {\cal G}(A,I)&=f{\cal N}(A,I),\\
 0\preceq{\cal G}&\preceq f{\cal N}.                    \tag{3}
\end{aligned}
\]
The local-support-boundary theorem applied to \(A_iC\) gives
\[
 {\cal W}(A,A)\geq0
 \qquad\text{whenever }\operatorname{rank}A\leq2.        \tag{4}
\]
Indeed, a rank-at-most-two local filter forces a deficient local
left support.

## 2. The spectral floor

Set
\[
 \kappa=\frac23-f.
\]
Use the rank-preserving isometry
\[
 X=A\rho^{1/2},\qquad A=X\rho^{-1/2},
\]
from \((M_3,{\cal N})\) to Hilbert--Schmidt \(M_3\).  Let \(H\) be
the Hermitian operator representing the transported form
\[
 \langle X,HY\rangle
 ={\cal W}(X\rho^{-1/2},Y\rho^{-1/2}).                   \tag{5}
\]
Equations (3) imply
\[
 H\preceq\frac23I,                                      \tag{6}
\]
while the first line of (3) gives
\[
 He=\kappa e,\qquad e=\rho^{1/2}.                       \tag{7}
\]
Here
\[
 \|e\|_2^2=\operatorname{Tr}\rho=\|C\|_2^2=1.
\]
Equation (4) says
\[
 \langle X,HX\rangle\geq0
 \qquad(\operatorname{rank}X\leq2),                     \tag{8}
\]
because right multiplication by \(\rho^{-1/2}\) preserves matrix
rank.

Write the eigenvalues of \(\rho\) as
\[
 \lambda_1\geq\lambda_2\geq\lambda_3=m>0.
\]
In matching Schmidt bases,
\[
 e=\sum_{j=1}^3\sqrt{\lambda_j}\,|j\,j\rangle .
\]
Its normalized best rank-two truncation is
\[
 \psi=
 \frac{\sqrt{\lambda_1}|1\,1\rangle+
       \sqrt{\lambda_2}|2\,2\rangle}{\sqrt{1-m}}.        \tag{9}
\]
Thus
\[
 \operatorname{rank}\psi=2,\qquad
 |\langle e,\psi\rangle|^2=1-m.
\]
Write
\[
 \psi=\sqrt{1-m}\,e+\xi,\qquad
 \xi\perp e,\qquad \|\xi\|^2=m.                         \tag{10}
\]
By (7), the mixed terms vanish.  By (6), (8), and (10),
\[
\begin{aligned}
 0
 &\leq\langle\psi,H\psi\rangle\\
 &=\kappa(1-m)+\langle\xi,H\xi\rangle\\
 &\leq\kappa(1-m)+\frac23m .
\end{aligned}                                            \tag{11}
\]
Consequently
\[
 \boxed{\qquad
 \kappa\geq-\frac{2m}{3(1-m)}.
 \qquad}                                                  \tag{12}
\]
Since \(\kappa=2/3-f\), this is equivalently
\[
 \boxed{\qquad
 f\leq\frac{2}{3(1-m)}.
 \qquad}                                                  \tag{13}
\]
For \(f>2/3\), rearranging (13) proves (1).

The same proof applies independently to every left and right site.
Therefore a hypothetical critical maximum with \(f>2/3\) obeys
\[
 \boxed{\qquad
 \lambda_{\min}(\rho_i^L),\
 \lambda_{\min}(\rho_i^R)
 \geq1-\frac{2}{3f}
 \quad(i=1,2,3).
 \qquad}                                                  \tag{14}
\]
In particular, putting
\[
 \mu=1-\frac{2}{3f}\in(0,1/3],
\]
the unit-trace condition gives the determinant floors
\[
 \det\rho_i^{L,R}\geq\mu^2(1-2\mu).                     \tag{15}
\]
Indeed, among three numbers at least \(\mu\) with sum one, their
product is minimized at \((1-2\mu,\mu,\mu)\).

## 3. Equality information and abstract sharpness

Equality in (12) forces both:

1. the rank-two truncation (9) to be a zero direction of \(H\);
2. its orthogonal remainder \(\xi\) to lie in the \(2/3\)-eigenspace
   of \(H\).

No argument using only (6)--(8) can strengthen (12).  For example,
take
\[
 \rho=\operatorname{diag}\left(\frac12,\frac14,\frac14\right),
 \qquad
 e=\operatorname{vec}(\rho^{1/2}),
\]
and on \(M_3\cong\mathbb C^3\otimes\mathbb C^3\) put
\[
 H=\frac23I-\frac89|e\rangle\langle e|.                 \tag{16}
\]
Then
\[
 He=-\frac29e,\qquad H\preceq\frac23I.                  \tag{17}
\]
For every unit Schmidt-rank-at-most-two vector \(z\),
\[
 |\langle e,z\rangle|^2
 \leq\frac12+\frac14=\frac34,
\]
and hence
\[
 \langle z,Hz\rangle
 \geq\frac23-\frac89\frac34=0.                          \tag{18}
\]
Thus (6)--(8) all hold and (12) is attained exactly with
\[
 m=\frac14,\qquad
 \kappa=-\frac29,\qquad
 f=\frac89.
\]
This abstract form need not arise from a physical pair-sector
critical point.  It proves that the remaining exclusion must use the
common tensor origin of the six forms (2), rather than another
one-site two-block-positivity estimate.

## Exact conclusion

Established:

1. the quantitative six-marginal floor (14);
2. the determinant floor (15);
3. the exact equality conditions in the one-site argument;
4. an abstract sharp model showing why the six sites must be coupled.

Still open:

1. exclusion of a full-support critical point with \(f>2/3\);
2. the pair-sector theorem;
3. unrestricted three-copy endpoint positivity.
