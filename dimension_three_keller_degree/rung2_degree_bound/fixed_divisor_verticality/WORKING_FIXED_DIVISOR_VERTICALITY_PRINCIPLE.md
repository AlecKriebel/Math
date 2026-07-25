# Provisional theorem: every fixed divisor of a quartic line pencil must be vertical

**Status:** exact working theorem; independent hostile audit passed at
2026-07-25T06:54:01Z.  This is not peer reviewed.

**Recorded:** 2026-07-25T06:18:12Z.

## 1. Statement

After translating the source and target, let
\[
F=L_0X+H_2+H_3+H_4:\mathbb A^3_{\mathbb C}\longrightarrow
\mathbb A^3_{\mathbb C}
\]
have total degree four, with \(L_0\in\operatorname{GL}_3(\mathbb C)\)
and \(H_i\) homogeneous of degree \(i\).  Suppose independent linear
source and target changes put
\[
\boxed{H_4=(hp,hq,0)^T,}                                 \tag{1}
\]
where
\[
1\le e=\deg h\le3,\qquad a=\deg p=\deg q=4-e,
\]
\(p,q\) are coprime and nonproportional, and \((p,q)\) is the minimal
pair for its projective pencil.  Here minimal means, equivalently, that
\[
\mathbb C(p/q)\ \text{is relatively algebraically closed in}\
\mathbb C(\mathbb P^2).                                  \tag{2}
\]

Assume at least one prime component of \(h=0\) is horizontal for the
pencil:
\[
\boxed{
\text{there is an irreducible }f\mid h\text{ such that }
f\nmid\alpha p+\beta q
\quad\text{for all }(\alpha,\beta)\ne(0,0).
}                                                        \tag{3}
\]

### Theorem

If \(F\) is Keller and (1)--(3) hold, then \(F\) is a polynomial
automorphism.  Thus, in every quartic line-pencil row
\[
(e,a)=(1,3),\ (2,2),\ \text{or }(3,1),                  \tag{4}
\]
a Keller counterexample would have to make **every** prime component of
\(h=0\) vertical for the minimal pencil.

The vertical boundary in (3) is genuine for the top identity.  Section 8
gives a minimal quadratic pencil with a vertical component of \(h\) and a
nonzero cubic normal first integral.  It is not asserted to be a Keller
map.

## 2. Minimality and relative algebraic closure

For completeness, suppose the relative algebraic closure of
\(\mathbb C(p/q)\) in \(\mathbb C(\mathbb P^2)\) were strictly larger.
A general line in \(\mathbb P^2\) dominates the corresponding curve, so
that curve is rational; Lüroth and homogeneity therefore identify the
closure with \(\mathbb C(r/s)\) and give
\[
\frac pq=\frac{A(r,s)}{B(r,s)},                           \tag{5}
\]
where \(r,s\) are coprime homogeneous forms of a common degree \(b\), and
\(A,B\) are coprime binary forms of a common degree \(n>1\).
The substituted forms \(A(r,s),B(r,s)\) are coprime: a common prime would
make \([r:s]\) a common projective zero of \(A,B\) at its generic point.
Uniqueness of reduced fractions and degrees then give
\[
p=A(r,s),\qquad q=B(r,s),\qquad a=nb.                    \tag{6}
\]
Conversely, any such composition makes the relative algebraic closure
larger.  Since here \(a\in\{1,2,3\}\), nonminimality can only be a
degree-\(a\) binary composition of a linear pencil.  This proves the
stated equivalence with the minimal-pair convention.

## 3. The homogeneous first-integral lemma

Put
\[
P=hp,\qquad Q=hq,\qquad
D(G)=\operatorname{Jac}(P,Q,G).                           \tag{7}
\]
Let \(G\ne0\) be homogeneous of degree \(d\), and assume \(D(G)=0\).
The forms \(P,Q\) are algebraically independent: a homogeneous binary
relation between two nonproportional forms of the same degree factors
into linear factors and would make them proportional.  In characteristic
zero, \(D(G)=0\) therefore makes \(G\) algebraic over
\(\mathbb C(P,Q)\).

The degree-zero function
\[
\Theta=\frac{G^4}{P^d}\in\mathbb C(\mathbb P^2)            \tag{8}
\]
is algebraic over \(\mathbb C(q/p,P)\).  A scaling coordinate writes
\[
\mathbb C(x,y,z)=\mathbb C(\mathbb P^2)(s),\qquad
P=s^4P_0,\qquad G=s^dG_0.                                \tag{9}
\]
Thus \(P\) is transcendental over the projective function field.
Clearing an algebraic relation for \(\Theta\) and collecting powers of
\(P\) shows that \(\Theta\) is algebraic over \(\mathbb C(q/p)\).
Relative algebraic closure (2) yields
\[
\boxed{\frac{G^4}{(hp)^d}=R(q/p)}
\qquad\text{for some }R\in\mathbb C(t).                  \tag{10}
\]

Choose the horizontal irreducible factor \(f\) supplied by (3), and put
\[
m=v_f(h)\in\{1,\ldots,e\}\subseteq\{1,2,3\}.             \tag{11}
\]
Condition (3) gives
\[
v_f(p)=v_f(q-\lambda p)=0
\quad\text{for every }\lambda\in\mathbb C.                \tag{12}
\]
After factoring the numerator and denominator of \(R\), including the
factor at infinity, (12) gives
\[
v_f(R(q/p))=0.                                           \tag{13}
\]
Taking \(v_f\) in (10) therefore gives the exact constraint
\[
\boxed{4v_f(G)=dm.}                                      \tag{14}
\]

### Corollary

There is no nonzero homogeneous cubic \(G\) satisfying \(D(G)=0\).
Indeed, the right side of (14) is \(3m\), which is not divisible by \(4\)
for \(m=1,2,3\).

## 4. Degree eight kills the cubic normal component

Write
\[
G_3=(H_3)_3.
\]
The third row of \(JH_4\) is zero and its first two rows are
\(\nabla P,\nabla Q\).  Hence
\[
\operatorname{adj}(JH_4)
=(\nabla P\times\nabla Q)e_3^T.                           \tag{15}
\]
The weight-eight coefficient of the Keller determinant has only the
pattern \(3+3+2\), so
\[
\begin{aligned}
0=E_8
&=\operatorname{tr}\bigl(\operatorname{adj}(JH_4)JH_3\bigr)\\
&=\operatorname{Jac}(P,Q,G_3).
\end{aligned}                                             \tag{16}
\]
The corollary gives
\[
\boxed{G_3=0.}                                           \tag{17}
\]

No factor of \(h\), no pencil discriminant, and no coefficient of \(G_3\)
was divided out.

## 5. Quadratic-component exit

Because the third components of \(H_4\) and \(H_3\) vanish, the third
component of the full map has degree at most two:
\[
F_3=(L_0X)_3+(H_2)_3.                                    \tag{18}
\]
It is nonconstant because \(L_0\) is invertible.

The independently audited quadratic-component theorem
`../WORKING_QUADRATIC_COMPONENT_EXIT.md` states that a total-degree-four
Keller map in dimension three with a nonconstant target-linear component
of degree at most two is a polynomial automorphism.  Applying it to
(18) proves the theorem.

This uses the unconditional low-degree plane theorem inside that banked
result; it does not assume the plane Jacobian Conjecture.

## 6. Consequences in the three line-pencil rows

The theorem has the following concrete consequences.

1. For \((e,a)=(1,3)\), the fixed line \(h=0\) must be a component of a
   cubic pencil member.  This recovers the horizontal part of the
   independently audited fixed-linear cubic-pencil exclusion.  That
   earlier result additionally controls the quadratic normal component.
2. For \((e,a)=(2,2)\), every prime component of the fixed conic \(h=0\)
   must be vertical.  The exact remaining frontier is recorded below.
3. For \((e,a)=(3,1)\), every prime factor of \(h\) must itself be a
   member of the line pencil.  Consequently
   \[
   h\in\mathbb C[p,q],
   \]
   recovering the independently audited exclusion of the nonbinary
   fixed-cubic row.

These are consequences for the stated leading-form taxonomy.  They are
not claims about arbitrary quartic leading forms.

## 7. Exact all-vertical frontier for \((e,a)=(2,2)\)

The complement of (3) has three elementary shapes.

1. If \(h\) is irreducible, a vertical degree-two pencil member is
   proportional to \(h\).  After a pencil change,
   \[
   p=h.
   \tag{19}
   \]
2. If \(h=\ell^2\), verticality of its unique prime means that, after a
   pencil change,
   \[
   p=\ell m
   \tag{20}
   \]
   for a linear form \(m\), possibly proportional to \(\ell\).
3. If \(h=\ell_1\ell_2\) with distinct linear factors, the two vertical
   members are unique.  If they coincide, a pencil change gives \(p=h\).
   If they are distinct, a pencil change gives
   \[
   p=\ell_1m_1,\qquad q=\ell_2m_2
   \tag{21}
   \]
   with linear \(m_1,m_2\).  Two different members cannot both contain
   the same \(\ell_i\), since then \(\ell_i\mid\gcd(p,q)\).

Consequently (19)--(21), with the standing coprimality and minimality
conditions, are the complete remaining frontier for this taxonomy row.

## 8. The vertical boundary is sharp for \(E_8\)

Take
\[
h=z^2,\qquad p=z^2,\qquad q=x^2+y^2,\qquad G_3=z^3.       \tag{22}
\]
Then \(p,q\) are coprime and
\[
P=hp=z^4,\qquad Q=z^2(x^2+y^2),
\]
so
\[
\operatorname{Jac}(P,Q,G_3)=0.                           \tag{23}
\]
The pencil is minimal: over \(\overline{\mathbb C(t)}\), the generic conic
\[
z^2-t(x^2+y^2)=0                                         \tag{24}
\]
is smooth, hence geometrically integral.  But the prime \(z\mid h\)
divides the pencil member \(p\), so (3) fails.

Thus the horizontal-component hypothesis cannot be dropped from the
degree-eight vanishing statement.  The datum (22) satisfies only the displayed top
identity; it is not claimed to extend to a Keller map.

## 9. Verification and disclosure

`verify_fixed_divisor_verticality_sympy.py` checks the universal
weight-eight identity, complete cubic-kernel calculations in representative
horizontal samples for all three rows (4), and the vertical witness.

`verify_fixed_divisor_verticality_pari.gp`, run through
`verify_fixed_divisor_verticality_pari_strict.sh`, independently expands
the determinant coefficient and reconstructs the horizontal kernels and
sharp boundary identity in PARI/GP.

The field and valuation proof is mathematical; the scripts are exact
evidence about the encoded algebra, not peer review.  AI systems
materially assisted the proof, checks, and exposition.  The independent
hostile audit in `audit_hostile/REPORT.md` reconstructed the descent,
finite and infinite divisor valuations, \(E_8\) orientation, plane exit,
and all frontier cases.  It found no mathematical defect and added a
dependency-free modular reconstruction plus fail-closed runner tests.
