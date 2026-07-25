# A valuation obstruction on the all-vertical \((e,a)=(2,2)\) frontier

**Status:** exact working lemma; independent hostile audit passed at
2026-07-25T08:05:00Z.  Not peer reviewed.

## 1. Setting and result

Let
\[
H_4=(hp,hq,0)^T,
\qquad \deg h=\deg p=\deg q=2,
\]
where \(p,q\) are coprime, nonproportional, and form a minimal quadratic
pencil.  Put
\[
P=hp,\qquad Q=hq,\qquad G=(H_3)_3.
\]
The degree-eight Keller identity is
\[
\operatorname{Jac}(P,Q,G)=0. \tag{1}
\]
Assume every prime factor of \(h\) is vertical for the pencil.

The following sharpens the three-shape frontier in the parent note.

### All-vertical top-obstruction lemma

1. If \(h=\ell^2\) and a vertical member is
   \[
   p=\ell m,\qquad m\not\sim\ell,
   \]
   then (1) has no nonzero homogeneous cubic solution.

2. If \(h=\ell_1\ell_2\), with \(\ell_1,\ell_2\) distinct, and the two
   vertical members are distinct,
   \[
   p=\ell_1m_1,\qquad q=\ell_2m_2,
   \]
   then (1) has no nonzero homogeneous cubic solution under the standing
   coprimality and minimality hypotheses.

3. In the remaining shape \(p=h\), a nonzero homogeneous cubic solution
   exists if and only if the minimal quadratic pencil contains a double
   line \(s=\ell^2\).  Such a double line is unique, and
   \[
   \ker\!\left(\operatorname{Jac}(hp,hq,-):
       \mathbb C[x,y,z]_3\to\mathbb C[x,y,z]_8\right)
   =\ell\langle p,q\rangle. \tag{2}
   \]
   After source and pencil changes, the pair \(\langle p,q\rangle\) is
   exactly one of
   \[
   \boxed{\langle x^2,yz\rangle},
   \qquad
   \boxed{\langle x^2,y^2+xz\rangle}, \tag{3}
   \]
   and the complete cubic kernel is respectively
   \[
   \langle x^3,xyz\rangle,\qquad
   \langle x^3,x(y^2+xz)\rangle. \tag{4}
   \]

Consequently, the genuine \(\ell^2,\ell m\) shape and the distinct-member
\(\ell_1\ell_2\) shape cannot occur for a Keller counterexample: (1)
forces \(G=0\), after which the banked quadratic-component exit applies.
The same holds in the \(p=h\) shape unless the pencil has the unique
double-line normal form (3).

Thus the only all-vertical top-identity frontier left by this lemma is
\[
\boxed{p=h,\quad
 \langle p,q\rangle\text{ contains a unique double line }s=\ell^2,
 \quad G=\ell(\alpha p+\beta q).} \tag{5}
\]

## 2. Same-fibre valuation obstruction

The homogeneous first-integral descent from the parent theorem does not
require a horizontal divisor.  Minimality gives, for every nonzero
homogeneous cubic \(G\) satisfying (1),
\[
\frac{G^4}{P^3}=R(q/p),\qquad R\in\mathbb C(t). \tag{6}
\]
Taking the valuation at a prime \(f\) gives
\[
4v_f(G)-3v_f(P)=v_f(R(q/p)). \tag{7}
\]

If \(f_1,f_2\) are distinct reduced components of the same pencil member
\(p=0\), coprimality makes \(q\) a unit at both generic points.  If
\(v_{f_i}(p)=1\), then \(q/p\) has the same simple pole at both primes.
Therefore
\[
v_{f_1}(R(q/p))=v_{f_2}(R(q/p)), \tag{8}
\]
without knowing the order of \(R\) at infinity.  Subtracting (7) yields
the coordinate-free congruence
\[
4\bigl(v_{f_1}(G)-v_{f_2}(G)\bigr)
=3\bigl(v_{f_1}(P)-v_{f_2}(P)\bigr). \tag{9}
\]
The identical statement holds for two simple components of \(q=0\), now
using the order of \(R\) at zero.

For \(h=\ell^2,p=\ell m\) with \(m\not\sim\ell\),
\[
v_\ell(P)=3,\qquad v_m(P)=1.
\]
Equation (9) becomes
\[
4\bigl(v_\ell(G)-v_m(G)\bigr)=6, \tag{10}
\]
which is impossible.  Notice that this tests the two primes of one fibre;
no factor of \(h\), no value of \(R\), and no coefficient of \(G\) is
divided out.  If \(m\sim\ell\), this is the \(p=h\) shape rather than the
genuine second shape.

For
\[
h=\ell_1\ell_2,\qquad p=\ell_1m_1,\qquad q=\ell_2m_2,
\]
coprimality first excludes \(m_1\sim\ell_2\) and
\(m_2\sim\ell_1\).  If \(m_1\not\sim\ell_1\), comparison inside the
\(p\)-fibre gives
\[
4\bigl(v_{\ell_1}(G)-v_{m_1}(G)\bigr)=3, \tag{11}
\]
impossible.  Hence a nonzero \(G\) would require
\(m_1\sim\ell_1\).  The same comparison in the \(q\)-fibre requires
\(m_2\sim\ell_2\).  This leaves
\[
p\sim\ell_1^2,\qquad q\sim\ell_2^2, \tag{12}
\]
but then \(p/q\) is a degree-two rational function of
\(\ell_1/\ell_2\), contradicting minimality.  This proves parts 1 and 2.

The obstruction is genuinely a same-fibre phenomenon.  Merely taking
one vertical valuation gives a congruence containing the unknown order of
\(R\) at the corresponding point of the pencil and proves nothing.

## 3. Reduction of the \(p=h\) shape

When \(p=h\),
\[
P=h^2,\qquad Q=hq,
\]
and direct expansion gives
\[
\operatorname{Jac}(P,Q,G)
=2h^2\operatorname{Jac}(h,q,G). \tag{13}
\]
Thus (1) is equivalent to
\[
\operatorname{Jac}(h,q,G)=0. \tag{14}
\]
The minimality descent for the quadratic pencil now gives
\[
\frac{G^2}{h^3}=S(q/h),\qquad S\in\mathbb C(t). \tag{15}
\]

Suppose the pencil has no double-line member.  Every fibre is reduced.
In the divisor identity
\[
2\operatorname{div}(G)-3\operatorname{div}(h)
=\pi^*\operatorname{div}(S), \tag{16}
\]
the coefficient of every fibre other than \(h=0\) is even.  If \(h\) is
reduced, the coefficient of its fibre is odd.  This contradicts the fact
that the coefficients of a principal divisor on \(\mathbb P^1\) sum to
zero.  If \(h\) is nonreduced, it is already a double line.  Therefore a
nonzero cubic solution forces a double-line member.

A minimal quadratic pencil cannot contain two distinct double lines:
if \(\ell_1^2,\ell_2^2\) were a pencil basis, then its ratio would be a
degree-two function of \(\ell_1/\ell_2\).  Hence the double member is
unique.

## 4. Exhaustive pencil and kernel normal forms

Put the unique double member at \(s=x^2\), and let \(r\) be any other
pencil member.  Coprimality implies \(r|_{x=0}\ne0\).  Its rank as a
binary quadratic in \(y,z\) is either two or one.

If the restriction has rank two, take it to \(yz\).  Write
\[
r=yz+x(ay+bz)+cx^2.
\]
The changes \(y\mapsto y+bx\), \(z\mapsto z+ax\), followed by adding a
multiple of \(s\) to \(r\), give
\[
(s,r)=(x^2,yz). \tag{17}
\]

If the restriction has rank one, take it to \(y^2\).  Completing the
square gives
\[
r=y^2+b\,xz+cx^2.
\]
Minimality forces \(b\ne0\); otherwise both pencil members are binary
quadratics in the linear pencil \(\langle x,y\rangle\).  Scaling \(z\)
and adding a multiple of \(s\) gives
\[
(s,r)=(x^2,y^2+xz). \tag{18}
\]
This proves that (3) is exhaustive.

Changing the pencil basis does not change (14) except by a nonzero scalar.
For \(s=x^2\),
\[
\operatorname{Jac}(s,r,G)=2x\operatorname{Jac}(x,r,G).
\]
In (17), the cubic kernel of
\(z\partial_z-y\partial_y\) is
\(\langle x^3,xyz\rangle\).  In (18), the cubic kernel of
\[
2y\partial_z-x\partial_y
\]
is \(\langle x^3,x(y^2+xz)\rangle\).  Both are
\[
x\langle x^2,r\rangle,
\]
which proves (2)--(4).  Conversely, every element of this two-dimensional
space visibly satisfies the top identity.

## 5. Exact witnesses and sharpness tests

The surviving kernel is real, not a parity artifact.  For example,
\[
h=p=x^2+y^2+z^2,\qquad q=z^2
\]
is a minimal pencil with double member \(z^2\), and
\[
G=z^3,\qquad G=z(x^2+y^2+z^2)
\]
are independent top-identity solutions.

By contrast, the following minimal samples have zero cubic kernel:
\[
\begin{array}{c|c|c}
h&p&q\\ \hline
z^2&zx&x^2+y^2\\
z^2&zx&y^2\\
yz&xy&z^2\\
x^2+y^2+z^2&x^2+y^2+z^2&x^2+2y^2+3z^2.
\end{array}
\]
They test respectively the genuine square shape with a generic second
member, the same shape even when another pencil member is a double line,
the distinct-member split shape, and the \(p=h\) shape with no double
line.

If minimality is deliberately dropped from the split shape,
\[
h=yz,\qquad p=y^2,\qquad q=z^2,
\]
then the cubic kernel has dimension four:
\[
\langle y^3,y^2z,yz^2,z^3\rangle.
\]
This exact counterexample shows that the final minimality step in (12)
is essential.

## 6. Verification and disclosure

The supplied SymPy script reconstructs the determinant identities and all
canonical cubic kernels.  The hostile audit independently reconstructed
the valuation and divisor arguments, both pencil normal forms, kernel
ranks over \(\mathbb Q\) in PARI/GP, and a dependency-free rank certificate
modulo \(101\).  Characteristics \(5\) and \(11\) were explicitly rejected
because they create spurious modular kernels.

AI systems materially assisted discovery, verification, audit, and
exposition.  Exact checks establish facts about the encoded algebra; they
are not peer review.  This theorem has not been peer reviewed, and its
source-specific priority audit is not a guarantee of worldwide priority.

`verify_top_obstruction_sympy.py` reconstructs these kernels, the
canonical derivations, the determinant identity (13), generic smoothness
of all minimal samples, and the nonminimal counterexample.
