# Haar boundary filters sharpen the three-copy pair ceiling

## Status

This note proves a new exact consequence of the established
local-support boundary theorem.  It does **not** prove unrestricted
three-copy positivity.

For a normalized rank-at-most-two qutrit operator \(C\), write
\[
 w_S=\|\Pi_S C\|_2^2,\qquad
 w_k=\sum_{|S|=k}w_S .
\]
Then every site \(i\), with
\(\{i,j,k\}=\{1,2,3\}\), obeys
\[
 \boxed{\quad
 \frac14w_{\{i\}}
 +w_{\{1,2,3\}}
 \geq
 \frac12\bigl(w_{\{i,j\}}+w_{\{i,k\}}\bigr).
 \quad}                                                     \tag{1}
\]
Every pair obeys
\[
 \boxed{\qquad
 w_{\{i,j\}}\leq2w_{\{1,2,3\}}.
 \qquad}                                                     \tag{2}
\]
In particular,
\[
 \boxed{\qquad
 w_2\leq
 \frac34-\frac34w_0-\frac{11}{16}w_1 .
 \qquad}                                                     \tag{3}
\]
This improves the previously recorded unconditional ceiling
\(w_2\leq24/31\) to
\[
 w_2\leq\frac34.
\]

The endpoint functional consequently satisfies
\[
 \boxed{\qquad
 Q_3(C)\geq-\frac18+\frac9{32}w_1 .
 \qquad}                                                     \tag{4}
\]
Thus the unrestricted theorem is already proved throughout the
sector region \(w_1\geq4/9\).  Any negative witness must lie in the
strictly smaller region \(w_1<4/9\).

The exact checker is
`verification/verify_n3_haar_boundary_filter_strengthening.py`.

## 1. One local Haar identity

On \(M_3\), let
\[
 {\cal L}(X)=X-\frac12\operatorname{Tr}(X)I_3,\qquad
 {\cal P}(X)=\frac{\operatorname{Tr}X}{3}I_3,\qquad
 {\cal Q}=I-{\cal P}.
\]
For a Haar-uniform unit vector \(z\in\mathbb C^3\), put
\[
 A_z=I-|z\rangle\langle z|.
\]
The following identity is an equality of Hermitian quadratic forms:
\[
 \boxed{\qquad
 {\mathbb E}_z\,
 \langle A_zX,{\cal L}(A_zX)\rangle
 =\frac58\|{\cal Q}X\|_2^2 .
 \qquad}                                                     \tag{5}
\]

To prove it, first take \(X=I/\sqrt3\).  Since \(A_z\) is a rank-two
projection,
\[
 \|A_zX\|_2^2=\frac23,\qquad
 |\operatorname{Tr}(A_zX)|^2=\frac43,
\]
so the left side of (5) is zero.

If instead \(\operatorname{Tr}X=0\) and \(\|X\|_2=1\), then
\[
 {\mathbb E}\|A_zX\|_2^2=\frac23
\]
and the elementary second-moment identity
\[
 {\mathbb E}|z^\dagger Xz|^2
 =\frac{\|X\|_2^2+|\operatorname{Tr}X|^2}{3(3+1)}
 =\frac1{12}
\]
gives
\[
 {\mathbb E}\,
 \langle A_zX,{\cal L}(A_zX)\rangle
 =\frac23-\frac12\frac1{12}
 =\frac58.
\]
The scalar--traceless mixed term actually vanishes before averaging.
For traceless \(Y\),
\[
 \langle A_zI/\sqrt3,A_zY\rangle
 =\frac1{\sqrt3}\operatorname{Tr}(A_zY),
\]
whereas the trace term in \({\cal L}\) is
\[
 -\frac12\,
 \overline{\operatorname{Tr}(A_z/\sqrt3)}
 \operatorname{Tr}(A_zY)
 =-\frac1{\sqrt3}\operatorname{Tr}(A_zY).
\]
This proves (5).

## 2. Conditional sector inequalities

Fix a site \(i\).  The filtered matrix \(A_z^{(i)}C\) has a
two-dimensional local left support.  The established local-support
boundary theorem therefore gives
\[
 Q_3(A_z^{(i)}C)\geq0                                      \tag{6}
\]
for every \(z\).

Average (6) and apply (5) at site \(i\).  Formula (5) kills every
sector which is scalar at \(i\), while multiplying every sector which
is traceless there by \(5/8\).  On the two unfiltered sites the
endpoint eigenvalues remain \(-1/2\) on the scalar direction and
\(1\) on the traceless direction.  Hence
\[
 0\leq\frac58\left[
 \frac14w_{\{i\}}
 -\frac12\bigl(w_{\{i,j\}}+w_{\{i,k\}}\bigr)
 +w_{\{1,2,3\}}
 \right],
                                                               \tag{7}
\]
which is (1).

Apply two independent filters at sites \(i,j\).  The output still has
deficient local support, so its endpoint expectation is nonnegative.
Twice using (5) kills all sectors except those containing both
filtered sites.  The remaining unfiltered site contributes
\(-1/2\) in degree two and \(1\) in degree three:
\[
 0\leq
 \left(\frac58\right)^2
 \left(-\frac12w_{\{i,j\}}+w_{\{1,2,3\}}\right).
                                                               \tag{8}
\]
This proves (2).

## 3. Grouped consequences

Sum (1) over the three sites.  Each degree-two sector appears twice,
so
\[
 \frac14w_1-w_2+3w_3\geq0.                                \tag{9}
\]
Using \(w_0+w_1+w_2+w_3=1\) in (9) gives (3).
Likewise, summing (2) over the three pairs gives
\[
 w_2\leq6w_3.                                             \tag{10}
\]

The exact endpoint sector formula is
\[
 Q_3(C)
 =1-\frac98w_0-\frac34w_1-\frac32w_2.
                                                               \tag{11}
\]
Substitution of (3) into (11) gives
\[
 Q_3(C)
 \geq
 1-\frac98w_0-\frac34w_1
 -\frac32\left(
 \frac34-\frac34w_0-\frac{11}{16}w_1\right)
 =-\frac18+\frac9{32}w_1,
\]
proving (4).

## 4. Equality is an unaveraged nonlinear condition

The derivation retains more information than the grouped inequality.
Every integrand in (6) is continuous and nonnegative.  Therefore,
if equality holds in the sum (9), then equality holds in every
sitewise average (7), and hence
\[
 \boxed{\qquad
 Q_3\bigl((I-|z\rangle\langle z|)^{(i)}C\bigr)=0
 \quad\text{for every }i\text{ and every unit }z.
 \qquad}                                                     \tag{12}
\]
Similarly, equality in (2) forces every corresponding two-filter
endpoint expectation to vanish.

This is the nonlinear information hidden by (3).  The formal sector
point
\[
 (w_0,w_1,w_2,w_3)
 =\left(\frac19,0,\frac23,\frac29\right)
\]
saturates (3) and would give \(Q_3=-1/8\), but sector arithmetic does
not show that one common rank-two matrix can satisfy the continuum of
zero conditions (12).  The remaining sharp subproblem is therefore
to combine (12) with the common-\(C\) Lie/Pluecker compatibility, or
to construct an exact physical matrix satisfying it.
