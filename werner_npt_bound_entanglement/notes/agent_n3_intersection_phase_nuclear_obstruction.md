# Exact phase--nuclear obstruction on the intersection-one stratum

## Status

This note disproves a tempting finite-dimensional completion of the
unrestricted three-copy proof. It does **not** give a negative Werner
witness.

For every rank-at-most-two coefficient matrix \(C\), the established
Hermitian-quadrature estimate says
\[
 Q_3(C)\geq \frac18\left(
 2\|C\|_2^2-\|A_\theta\|_1^2-\|B_\theta\|_1^2
 \right),
 \tag{1}
\]
where
\[
 A_\theta=\operatorname{Re}(e^{-i\theta}C),\qquad
 B_\theta=\operatorname{Im}(e^{-i\theta}C).
 \tag{2}
\]
It would therefore suffice to prove that some phase obeys
\[
 \|A_\theta\|_1^2+\|B_\theta\|_1^2
 \leq 2\|C\|_2^2.
 \tag{3}
\]

The matrix
\[
 \boxed{
 C=
 \begin{pmatrix}
 0&1&1\\
 0&0&1\\
 0&0&0
 \end{pmatrix}}
 \tag{4}
\]
has rank two and
\[
 \dim(\operatorname{ran}C+\operatorname{ran}C^\dagger)=3,
 \qquad
 \dim(\operatorname{ran}C\cap\operatorname{ran}C^\dagger)=1.
 \tag{5}
\]
Nevertheless, for **every** phase,
\[
 \boxed{
 \|A_\theta\|_1^2+\|B_\theta\|_1^2\geq7
 >6=2\|C\|_2^2.}
 \tag{6}
\]
Thus the phase--quadrature lower bound cannot prove even the complete
intersection-one theorem. A proof must use the physical tensor
geometry inside \(Q_3\), not only the spectra of the two Hermitian
quadratures forced by rank two.

The dependency-free exact checker is
`verification/verify_n3_intersection_phase_nuclear_obstruction.py`.

## 1. Exact quadrature invariants

Put \(z=e^{-i\theta}\). The first quadrature is
\[
 A_\theta
 =\frac12
 \begin{pmatrix}
 0&z&z\\
 \overline z&0&z\\
 \overline z&\overline z&0
 \end{pmatrix}.
 \tag{7}
\]
Since \(C\) is strictly upper triangular,
\[
 \operatorname{Tr}C^2=0.
\]
Consequently
\[
 \operatorname{Tr}A_\theta=0,\qquad
 \operatorname{Tr}A_\theta^2=\frac32.
 \tag{8}
\]
Direct expansion of the two oriented three-cycles gives
\[
 \det A_\theta
 =\frac18(z+\overline z)
 =\frac14\cos\theta.
 \tag{9}
\]
Moreover,
\[
 B_\theta=A_{\theta+\pi/2},
 \tag{10}
\]
so
\[
 \operatorname{Tr}B_\theta=0,\qquad
 \operatorname{Tr}B_\theta^2=\frac32,\qquad
 |\det B_\theta|=\frac14|\sin\theta|.
 \tag{11}
\]

## 2. Trace norm of the cubic family

For \(0\leq x\leq1/4\), let \(r(x)\) be the largest real root of
\[
 t^3-\frac34t-x=0.
 \tag{12}
\]
If \(H\) is Hermitian with
\[
 \operatorname{Tr}H=0,\qquad
 \operatorname{Tr}H^2=\frac32,\qquad
 |\det H|=x,
 \tag{13}
\]
then
\[
 \boxed{\|H\|_1^2=4r(x)^2.}
 \tag{14}
\]

Indeed, replacing \(H\) by \(-H\) if necessary makes its determinant
nonnegative. Its characteristic polynomial is (12). Its spectrum
then has two nonpositive eigenvalues and one positive eigenvalue
\(r(x)\). The trace-zero condition says that the sum of the absolute
values of the two nonpositive eigenvalues is \(r(x)\). Hence
\(\|H\|_1=2r(x)\), proving (14). The endpoint \(x=0\) follows by
continuity and has spectrum
\(\{\sqrt3/2,0,-\sqrt3/2\}\).

Define
\[
 g(s)=r(\sqrt s)^2,\qquad 0\leq s\leq\frac1{16}.
 \tag{15}
\]
This function is concave. To see this without differentiating a
cubic root, put \(y=g(s)\). Equation (12) gives
\[
 s=h(y):=y\left(y-\frac34\right)^2,
 \qquad \frac34\leq y\leq1.
 \tag{16}
\]
On this interval,
\[
 h'(y)=\left(y-\frac34\right)
       \left(3y-\frac34\right)\geq0,
 \qquad
 h''(y)=6y-3\geq\frac32.
 \tag{17}
\]
Thus \(h\) is increasing and convex, and its inverse \(g\) is
increasing and concave. This remains valid at the left endpoint by
continuity.

## 3. Uniform failure for every phase

Set
\[
 s=\frac{\cos^2\theta}{16},\qquad
 t=\frac{\sin^2\theta}{16}.
 \tag{18}
\]
Then \(s+t=1/16\). By (8)--(15),
\[
 \|A_\theta\|_1^2+\|B_\theta\|_1^2
 =4\bigl(g(s)+g(t)\bigr).
 \tag{19}
\]
The function
\[
 s\longmapsto g(s)+g(1/16-s)
\]
is concave on \([0,1/16]\). It is symmetric about the midpoint, so
its two endpoint values agree and concavity puts every interior value
above their common chord. Since
\[
 g(0)=\frac34,\qquad g(1/16)=1,
 \tag{20}
\]
we obtain
\[
 g(s)+g(t)\geq\frac74.
 \tag{21}
\]
Equations (19)--(21) prove the lower bound \(7\) in (6).

Finally, \(C\) has three unit entries, so \(\|C\|_2^2=3\). Equality
in (6) is attained at \(\theta=0\): the spectra of \(A_0\) and \(B_0\)
are respectively
\[
 \{1,-1/2,-1/2\},\qquad
 \{\sqrt3/2,0,-\sqrt3/2\},
 \tag{22}
\]
whose squared trace norms are \(4\) and \(3\).

## Exact conclusion

The sufficient condition (3) is false on the smallest genuinely
nonnormal support geometry left by the self-adjoint theorem. The
failure is uniform in the phase and has the exact gap
\[
 \inf_\theta\left(
 \|A_\theta\|_1^2+\|B_\theta\|_1^2
 \right)-2\|C\|_2^2=1.
 \tag{23}
\]
This does not determine the sign of \(Q_3(C)\) after embedding the
three-dimensional support into a tensor-product physical space.
Rather, it proves that the tensor-independent phase--nuclear estimate
throws away indispensable information before \(Q_3\) is evaluated.
