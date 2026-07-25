# The vertical fixed-linear primitive cubic-pencil frontier

**Status:** exact theorem and frontier reduction; independent hostile audit
passed in `audit_vertical_hostile/REPORT.md`.  This is not peer reviewed.

**Recorded:** 2026-07-25T10:55:06Z.

## 1. Setting

Let
\[
F=L_0X+H_2+H_3+H_4:\mathbb A^3_{\mathbb C}\longrightarrow
\mathbb A^3_{\mathbb C}
\]
have total degree four, with \(L_0\in\operatorname{GL}_3(\mathbb C)\).
Suppose independent source and target changes put
\[
H_4=(hp,hq,0)^T,                                      \tag{1}
\]
where \(h\) is linear and \(p,q\) are coprime, nonproportional homogeneous
cubics.  Assume that \((p,q)\) is the minimal pair of the pencil, or
equivalently that
\[
\mathbb C(p/q)\text{ is relatively algebraically closed in }
\mathbb C(\mathbb P^2).                                \tag{2}
\]
Assume now that the unique vertical member is \(p\):
\[
p=h^m r,\qquad 1\leq m\leq3,\qquad
\deg r=3-m,\qquad h\nmid rq.                            \tag{3}
\]
The member is unique because two vertical members would make \(h\) divide
both \(p\) and \(q\).

Write
\[
G_3=(H_3)_3,\qquad G_2=(H_2)_3.
\]

## 2. Result

### Vertical multiplicity theorem

The degree-eight Keller identity has the following exact consequences.

1. If \(m=1\) or \(m=2\), then
   \[
   \boxed{G_3=0.}                                      \tag{4}
   \]
   Hence the third component of \(F\) has degree at most two, and the
   banked quadratic-component exit makes \(F\) a polynomial automorphism.
   In particular neither the simple nor the double vertical stratum can
   contain a Keller counterexample.

2. If \(m=3\), normalize \(h=z\), so \(p=z^3\).  Then
   \[
   \boxed{G_3\in\langle z^3,q\rangle.}                 \tag{5}
   \]
   If \(G_3=0\), the same quadratic-component exit applies.  If
   \(G_3\ne0\), the residual pencil transformation
   \(q\mapsto aq+bz^3\), together with scaling of the third target
   coordinate, gives exactly two normal companion types:
   \[
   \boxed{G_3=z^3}\qquad\text{or}\qquad
   \boxed{G_3=q}.                                      \tag{6}
   \]

For reference, the degree-seven normal first-integral equation, when it is
uncoupled by \(G_3=0\), has the following complete solutions:
\[
\begin{array}{c|c}
\text{vertical multiplicity} &
\ker(\operatorname{Jac}(hp,hq,-):\mathbb C[X]_2\to\mathbb C[X]_7)\\ \hline
m=1 & 0,\ \text{unless }r=L^2,\text{ when it is }\mathbb C\,hL,\\
m=2 & 0,\\
m=3 & \mathbb C\,h^2.
\end{array}                                             \tag{7}
\]
The \(m=1,r=L^2\) witness is the previously recorded \(hp=(hL)^2\);
it does not rescue a counterexample because (4) has already made the
third component quadratic.

The two surviving companion types in (6) really escape the top three
determinant coefficients.  For the primitive pencil
\[
h=z,\qquad p=z^3,\qquad q=x^3+y^3,                      \tag{8}
\]
both choices
\[
L_0=I,\qquad H_2=0,\qquad
H_3=(0,0,z^3)^T
\quad\text{or}\quad
H_3=(0,0,q)^T                                           \tag{9}
\]
satisfy
\[
\boxed{E_8=E_7=E_6=0.}                                 \tag{10}
\]
They are not Keller maps: lower determinant coefficients remain.  Thus
any exclusion of the triple-vertical frontier must use \(E_5\) or below,
or a new global mechanism.

In fact the vertical companion \(G_3=z^3\) escapes \(E_5\) as well.  Keep
(8), and take
\[
\begin{aligned}
L_0&=I,\\
H_3&=(q+\tfrac43z^3,\,0,\,z^3)^T,\\
H_2&=(0,\,xz,\,z^2)^T.
\end{aligned}                                           \tag{11}
\]
Then
\[
\det\!\left(I+\tau JH_2+\tau^2JH_3+\tau^3JH_4\right)
=(1+3\tau^2x^2)(1+2\tau z+3\tau^2z^2),                 \tag{12}
\]
so
\[
E_8=E_7=E_6=E_5=0,\qquad E_4=9x^2z^2\ne0.              \tag{13}
\]
Thus the vertical-companion branch requires \(E_4\) or below.

## 3. Full source-orbit classification of the vertical member

Set \(h=z\).  For \(m=1\), classify the quadratic \(r\) under the parabolic
source group preserving the line \(z=0\).  Let
\[
\rho=\operatorname{rank}(r|_{z=0}),\qquad R=\operatorname{rank}(r).
\]
The five possible pairs \((\rho,R)\), and one representative for each,
are
\[
\begin{array}{c|c|c}
(\rho,R)&r&p=zr\\ \hline
(2,2)&xy&xyz\\
(2,3)&xy+z^2&z(xy+z^2)\\
(1,1)&x^2&zx^2\\
(1,2)&x^2+z^2&z(x^2+z^2)\\
(1,3)&x^2+yz&z(x^2+yz).
\end{array}                                             \tag{14}
\]
These are disjoint and exhaustive.  Indeed, if \(\rho=2\), completing
the two \(z\)-linear terms leaves \(xy+\kappa z^2\), with
\(\kappa=0\) or \(1\).  If \(\rho=1\), completing the square leaves
\(x^2+b\,yz+c z^2\).  The cases \(b\ne0\), \(b=0,c\ne0\), and
\(b=c=0\) give the last three representatives.  The two ranks are
invariant under the parabolic, so no representatives merge.

For \(m=2\) and \(m=3\), the unique representatives are respectively
\[
p=z^2x,\qquad p=z^3.                                   \tag{15}
\]
Thus (14)--(15) are the complete source normal forms for the marked pair
\((h,p)\); no finite list for \(q\) is asserted.

### The retained \(q\)-moduli

For every representative \(p\), the full remaining equivalence on \(q\)
is
\[
q\sim a\,T^*q+b\,p,\qquad a\ne0,\qquad
T\in\mathcal G_{z,p}:=
\{T\in\operatorname{GL}_3:T^*z\in\mathbb C^\times z,\
T^*p\in\mathbb C^\times p\}.                           \tag{16}
\]
The allowed locus is the open subset
\[
z\nmid q,\qquad \gcd(p,q)=1,                            \tag{17}
\]
of the quotient projective space
\(\mathbb P(\operatorname{Sym}^3\mathbb C^3/\langle p\rangle)\).
Formula (16), rather than a spurious finite orbit list, retains every
continuous modulus.

On the surviving triple stratum \(p=z^3\), (16) is completely explicit:
\[
\begin{aligned}
(x,y)^T&\longmapsto A(x,y)^T+vz,\\
z&\longmapsto cz,\\
q&\longmapsto a\,q(TX)+b z^3,
\end{aligned}
\qquad
A\in\operatorname{GL}_2,\quad v\in\mathbb C^2,\quad ac\ne0. \tag{18}
\]
For the exceptional simple-square stratum \(p=zx^2\), it is
\[
x\mapsto ax,\qquad
y\mapsto d y+e x+fz,\qquad
z\mapsto cz,\qquad
q\mapsto \alpha q(TX)+\beta zx^2,                       \tag{19}
\]
with \(a,c,d,\alpha\ne0\).  These formulas display the full stabilizers,
including the shears that are easily lost in a coefficient normalization.

For a concrete atlas on the surviving quotient, write
\[
q=q_3(x,y)+zq_2(x,y)+z^2q_1(x,y)+c_0z^3.
\]
The target translation in (18) kills \(c_0\).  The binary cubic \(q_3\)
is nonzero by (17), and its three root-multiplicity strata have
representatives
\[
xy(x-y),\qquad x^2y,\qquad x^3.                         \tag{20}
\]
Thus every retained modulus occurs among the five coefficients of
\((q_2,q_1)\), modulo the residual stabilizer of the applicable form in
(20), the two affine translations in (18), and relative scaling of \(z\).
This is an explicit finite atlas for the quotient (16), but deliberately
does not collapse its continuous moduli.

## 4. Nonminimal and reclassification boundaries

Because \(3\) is prime, a nonminimal cubic pair is exactly a pair of
binary cubics in a linear pencil: there is a two-dimensional linear
subspace \(W\subset\mathbb C[x,y,z]_1\) with
\[
p,q\in\operatorname{Sym}^3W.                            \tag{21}
\]
Consequently:

- the three essential-variable representatives
  \(xyz\), \(z(xy+z^2)\), and \(z(x^2+yz)\) in (14) are automatically
  minimal;
- for \(p=zx^2\), \(z(x^2+z^2)\), or \(z^2x\), the nonminimal boundary is
  exactly \(q\in\operatorname{Sym}^3\langle x,z\rangle\);
- for \(p=z^3\), the nonminimal boundary is
  \[
  q\in\operatorname{Sym}^3\langle z,\ell\rangle
  \quad\text{for some }\ell\notin\mathbb Cz.             \tag{22}
  \]

Every point of these boundaries reclassifies into the
\((a,b)=(1,3)\) row.  Conditions (17), (21), and (22) are part of the
normal-form statement; they must not be removed by choosing a convenient
sample \(q\).

## 5. Multiplicity proof

Put
\[
P=hp,\qquad Q=hq,\qquad
D(G)=\operatorname{Jac}(P,Q,G).
\]
The degree-eight identity is \(D(G_3)=0\).  The homogeneous
first-integral descent proved in the parent package gives, for a nonzero
homogeneous \(G\) of degree \(d\),
\[
\frac{G^4}{P^d}=R(q/p),\qquad R\in\mathbb C(t).           \tag{23}
\]
Let \(s=\operatorname{ord}_\infty R\).  If a prime \(f\) occurs in \(p\)
with multiplicity \(a\), then \(q/p\) has a pole of order \(a\) at \(f\).
Taking its valuation in (23) gives
\[
4v_f(G)-d\bigl(a+\mathbf1_{f=h}\bigr)=a s.               \tag{24}
\]
No reducedness of the fibre is used.

For \(d=3,m=1\), the \(h\)-valuation gives
\[
s\equiv2\pmod4.                                         \tag{25}
\]
Every prime of the quadratic \(r\) has multiplicity \(a=1\) or \(2\),
whereas its version of (24) requires
\[
a(3+s)\equiv0\pmod4.                                    \tag{26}
\]
Equations (25)--(26) are incompatible for both \(a=1\) and \(a=2\).
For \(d=3,m=2\), the \(h\)-equation itself reads
\[
4v_h(G)=9+2s,
\]
an even-plus-odd impossibility.  This proves (4).

For \(d=3,m=3\), (24) gives \(s\equiv0\pmod4\).  Degree and
nonnegativity leave only \(s=0\), when \(G\) has divisor \(3(h)\), or
\(s=-4\), when the zero divisor of \(R\) has total order four.  In the
first case \(G\sim h^3\).  In the second, a zero of order \(n<4\) would
require every component multiplicity of the corresponding cubic fibre to
make \(na\) divisible by \(4\).  This is impossible for a divisor of
total degree three.  Hence there is one zero of order four and
\(G\) is that cubic pencil member.  Varying the member gives precisely
\(\langle h^3,q\rangle\), proving (5).

For \(d=2\), the same congruence proves (7).  In the \(m=1\) case it
forces every prime of \(r\) to have multiplicity two, hence \(r=L^2\);
degree then forces \(G\sim hL\).  The \(m=2\) equations at \(h\) and at
the remaining line are incompatible.  For \(m=3\), degree forces
\(\operatorname{div}(G)=2(h)\), hence \(G\sim h^2\).

## 6. Exact top-identity survivors

Before recording the witnesses, it is useful to expose the exact next
identity.  Write \(H_3=(U,V,G_3)^T\) and
\((H_2)_3=W\), and put
\[
\{A,B\}_{x,y}=A_xB_y-A_yB_x.
\]
If \(G_3=z^3\), direct row expansion gives
\[
E_7=z^3\{q,\,4zW-3U\}_{x,y}.                            \tag{27}
\]
The cubic-kernel theorem above therefore says
\[
4zW-3U\in\langle z^3,q\rangle.                          \tag{28}
\]
If \(G_3=q\), the corresponding exact identity is
\[
E_7=
\{q,\,4z^4W-4z^3V+qU\}_{x,y}.                          \tag{29}
\]
Neither formula divides by \(z\), \(q\), or a discriminant.

For the first choice in (9), direct differentiation gives
\[
\det\!\left(I+\tau^2JH_3+\tau^3JH_4\right)
=(1+3\tau^2z^2)(1+3\tau^3y^2z).                         \tag{30}
\]
Its largest power is \(\tau^5\), proving (10).  The second choice in
(9) also has degree at most five in \(\tau\); the accompanying exact
scripts expand it independently.  Formula (12) independently supplies
the stronger \(E_5\) escape on the vertical-companion branch.  The generic member
\[
z^3-t(x^3+y^3)
\]
is smooth over \(\overline{\mathbb C(t)}\), so (8) is on the primitive
triple-vertical locus rather than the reclassification boundary.

## 7. Verification boundary

The accompanying SymPy and PARI/GP scripts independently check:

- the degree-two and degree-three kernels on all seven marked-member
  representatives;
- the two residual stabilizer formulas (18)--(19);
- the weighted determinant coefficients of both primitive survivors;
- smoothness of the generic witness pencil.

The scripts do not replace the relative-algebraic-closure input in (2),
the divisor argument in Section 5, or the banked quadratic-component
exit.  Exact computer algebra is evidence about the encoded identities,
not peer review.  AI systems materially assisted the proof, computation,
and exposition.
