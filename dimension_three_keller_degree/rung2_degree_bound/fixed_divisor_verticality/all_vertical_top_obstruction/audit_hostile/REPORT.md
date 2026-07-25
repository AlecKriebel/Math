# Hostile audit: all-vertical \((e,a)=(2,2)\) top obstruction

## Verdict

**PASS.**  I reconstructed the field and divisor arguments independently,
checked every frontier incidence case, and found no counterexample or missing
normal form.  The theorem is valid with exactly the scope stated in
`../NOTE.md`.

The audit did find a verification hazard, not a mathematical defect:
reducing the degree-eight Jacobian map modulo \(5\) or \(11\) can create
purely inseparable or accidental modular cubic kernels that do not exist in
characteristic zero.  Those small-characteristic experiments were discarded.
The retained modular script uses \(101\), and none of its sampled searches is
used as a proof of the universal theorem.

## 1. Same-fibre valuation equality

Let
\[
u=q/p,\qquad \frac{G^4}{P^3}=R(u),\qquad P=hp.
\]
The parent minimality descent applies without a horizontal divisor.  It uses
only that \(p,q\) are the minimal coprime pair, that \(P,Q\) have the same
degree, and that \(G\) is a nonzero homogeneous first integral.  Thus no
extra genericity assumption enters the candidate note.

Suppose \(f_1,f_2\) are distinct simple components of \(p=0\).
Coprimality gives \(v_{f_i}(q)=0\), hence
\[
v_{f_i}(u)=-1.
\]
Writing \(w=1/t\) at infinity and
\[
R(t)=w^{n_\infty}\cdot(\text{unit}),\qquad
n_\infty=\operatorname{ord}_\infty R,
\]
gives
\[
v_{f_i}(R(u))=n_\infty
\]
at both components.  This proves the claimed equality without assuming
anything about the value or sign of \(n_\infty\).  At two simple components
of \(q=0\), the same calculation uses
\[
v_{f_i}(u)=1,\qquad
v_{f_i}(R(u))=\operatorname{ord}_0R.
\]
Distinct pencil fibres cannot share a prime because \(\gcd(p,q)=1\).

Consequently
\[
4\bigl(v_{f_1}(G)-v_{f_2}(G)\bigr)
=3\bigl(v_{f_1}(P)-v_{f_2}(P)\bigr)
\]
is exact.

For \(h=\ell^2,\ p=\ell m\) with \(m\not\sim\ell\), the two \(P\)-orders
are \(3\) and \(1\), so the equation is \(4N=6\), impossible.

For
\[
h=\ell_1\ell_2,\qquad
p=\ell_1m_1,\qquad q=\ell_2m_2,
\]
coprimality excludes \(m_1\sim\ell_2\) and
\(m_2\sim\ell_1\).  If \(m_1\not\sim\ell_1\), comparison in the
\(p\)-fibre gives \(4N=3\).  Avoiding it forces
\(p\sim\ell_1^2\).  The \(q\)-fibre similarly forces
\(q\sim\ell_2^2\).  Then
\[
\mathbb C\!\left(\frac{\ell_1^2}{\ell_2^2}\right)
\subsetneq
\mathbb C\!\left(\frac{\ell_1}{\ell_2}\right)
\subset\mathbb C(\mathbb P^2),
\]
contradicting relative algebraic closure.  This confirms that minimality is
used exactly once and is indispensable.

## 2. Divisor parity in the \(p=h\) shape

The determinant expansion is correct:
\[
\operatorname{Jac}(h^2,hq,G)
=2h^2\operatorname{Jac}(h,q,G).
\]
Since the polynomial ring is a domain, the top identity is equivalent to
\(\operatorname{Jac}(h,q,G)=0\).  Minimality of the quadratic pencil then
gives
\[
\frac{G^2}{h^3}=S(q/h).
\]

Let \(n_a=\operatorname{ord}_aS\) for \(a\in\mathbb P^1\).  Because
\(\gcd(h,q)=1\), different pencil members share no divisorial component,
and
\[
\operatorname{div}(S(q/h))=\sum_{a\in\mathbb P^1}n_aD_a,
\]
where \(D_\infty=(h=0)\) and \(D_a=(q-ah=0)\) for finite \(a\).

If the pencil has no double line, every conic \(D_a\) is reduced.  On every
finite component the coefficient identity is
\[
n_a=2v_f(G),
\]
so every finite \(n_a\) is even.  On each component of the reduced
\(h\)-fibre it is
\[
n_\infty=2v_f(G)-3,
\]
so \(n_\infty\) is odd.  This contradicts
\[
\sum_{a\in\mathbb P^1}n_a=0
\]
for the principal divisor of \(S\) on \(\mathbb P^1\).  There is no hidden
base-curve contribution: base points have codimension two and
\(\gcd(h,q)=1\) excludes a common prime divisor.  A nonreduced conic is
precisely a double line, so the necessity argument is exhaustive.

Conversely, if \(s=\ell^2\) is a pencil member, then
\(\operatorname{Jac}(h,q,\ell)=0\) follows from
\(\operatorname{Jac}(h,q,\ell^2)=0\) in characteristic zero.  Hence every
\(\ell(\alpha h+\beta q)\) is a cubic first integral.  This proves both
directions of the candidate statement.

## 3. Uniqueness and exhaustive normal forms

Two distinct double members would form a pencil basis
\(\ell_1^2,\ell_2^2\), making their ratio a quadratic function of
\(\ell_1/\ell_2\).  That violates minimality, so the double member is
unique.

Put it at \(s=x^2\), and let \(r\) be another member.  Since
\(\gcd(x^2,r)=1\), the binary restriction \(r(0,y,z)\) is nonzero; rank
zero is therefore impossible.

- In restriction rank two, a binary change takes the restriction to \(yz\).
  For
  \[
  r=yz+a\,xy+b\,xz+c\,x^2
  \]
  the exact identity
  \[
  r=(y+bx)(z+ax)+(c-ab)x^2
  \]
  gives \(\langle x^2,yz\rangle\) after a source change and a pencil
  change.

- In restriction rank one, take the restriction to \(y^2\).  For
  \[
  r=y^2+a\,xy+b\,xz+c\,x^2
  \]
  completing the square gives
  \[
  r=(y+\tfrac a2x)^2+b\,xz+
  (c-\tfrac{a^2}{4})x^2.
  \]
  If \(b=0\), both members are binary quadratics in \(x,y+a x/2\), so the
  pencil is a degree-two composition and is nonminimal.  If \(b\ne0\),
  scaling \(z\) gives \(\langle x^2,y^2+xz\rangle\).

Thus there is no omitted restriction-rank or transverse-coefficient case.
The PARI certificate independently verifies these normalization identities.
It also verifies directly that each canonical pencil has no second double
member.

## 4. Complete cubic kernels

Changing a pencil basis changes the Jacobian derivation only by a nonzero
scalar.  For the rank-two normal form,
\[
\operatorname{Jac}(x,yz,-)=z\partial_z-y\partial_y.
\]
Its degree-three zero-weight monomials are exactly
\[
x^3,\qquad xyz.
\]

For the rank-one normal form,
\[
\operatorname{Jac}(x,y^2+xz,-)=2y\partial_z-x\partial_y.
\]
Substitution of a general cubic gives exactly
\[
\ker=\langle x^3,\ x(y^2+xz)\rangle.
\]
There are no additional cancellation chains.  The independent exact
PARI matrix has rank \(8\) over \(\mathbb Q\) in both cases and verifies
the two displayed witnesses.  The dependency-free modular reconstruction
also finds rank \(8\) modulo \(101\), which supplies an independent nonzero
rank-\(8\) minor.

Since \(\langle x^2,r\rangle=\langle p,q\rangle\), both kernels are
\[
\ell\langle p,q\rangle.
\]
This confirms the coordinate-free kernel claim.

## 5. Keller-map scope and the quadratic-component exit

The lemma concerns only the quartic leading-form stratum
\[
H_4=(hp,hq,0),\qquad
\deg h=\deg p=\deg q=2,
\]
with a coprime minimal quadratic pencil.  It does not classify arbitrary
quartic leading forms, and the surviving top-identity solutions are not
asserted to extend to Keller maps.

For an actual Keller map in this stratum, the banked weight-eight identity is
\[
\operatorname{Jac}(hp,hq,(H_3)_3)=0.
\]
In the first two shapes, and in the \(p=h\) shape without a double member,
the audited lemma forces \((H_3)_3=0\).  The third components of \(H_4\) and
\(H_3\) then both vanish, so the third component of the full map has degree
at most two.  Its linear term is nonzero because the linear part is
invertible.  The independently banked quadratic-component exit therefore
applies exactly as claimed.  This step uses the unconditional plane
degree bound, not the plane Jacobian Conjecture.

## 6. Independent verification

All of the following pass:

```text
/usr/bin/python3 ../verify_top_obstruction_sympy.py
/usr/bin/python3 audit_reconstruct_mod101.py
./audit_exact_pari_strict.sh
./test_audit_guards.sh
```

`audit_exact_pari.gp` independently reconstructs the normal-form identities,
canonical kernel ranks over \(\mathbb Q\), representative zero kernels, the
nonminimal binary kernel, and the double-member witnesses.

`audit_reconstruct_mod101.py` uses a dependency-free sparse-polynomial
implementation.  It checks \(768\) accepted samples in each of the square
and split shapes and \(768\) samples in each restriction stratum, in addition
to canonical rank-minor certificates.  These samples are stress tests, not
the proof of a universal statement.

`test_audit_guards.sh` confirms rejection of optimized Python, a forged
algebraic failure, and a forged PARI diagnostic.  Exact computation is
evidence about the encoded algebra, not peer review.
