# Clean-room bridge for `Q2-E0-A2-B2-D2-N1`

## Scope and source discipline

This note was completed before opening any proposed bridge or any downstream
conic-type proof.  Its only inputs are the frozen taxonomy and frozen
manifest, version one.

Let a point of the frozen row be represented by

\[
F=X+H_2+H_3+H_4,\qquad \det JF=1.
\]

The frozen tuple says, intrinsically,

\[
\operatorname{rank}JH_4=2,\quad e=0,\quad a=2,\quad b=2,\quad
\delta=2,\quad \nu=1.
\]

Thus there are coprime quadratic forms \(p,q\), unique up to the canonical
Möbius ambiguity, and a basepoint-free binary quadratic triple
\(A=(A_1,A_2,A_3)\) such that

\[
H_4=A(p,q),\qquad
\mathbb C(p/q)=E_{H_4}=K_{H_4}.
\tag{1}
\]

Here the second equality is the essential `N1` relative-closure condition.

## Intrinsic leading normal form

The map \([s:t]\mapsto[A_1(s,t):A_2(s,t):A_3(s,t)]\) is a birational
degree-two map onto a plane conic.  A reduced irreducible plane conic over
\(\mathbb C\) is smooth.  Its image is nondegenerate, so \(A_1,A_2,A_3\)
are linearly independent.  Since
\(\dim H^0(\mathbb P^1,\mathcal O(2))=3\), they form a basis of the complete
binary quadratic linear system.

Consequently, after a target transformation \(T\in\mathrm{GL}_3(\mathbb C)\)
and a basis change of the pencil \(\langle p,q\rangle\),

\[
T H_4=(p^2,pq,q^2).
\tag{2}
\]

This can be made as a conjugation of the full normalized map:

\[
\widetilde F(X)=T F(T^{-1}X).
\tag{3}
\]

Then \(J\widetilde F=T(JF)(T^{-1}X)T^{-1}\), so
\(\det J\widetilde F=1\), the constant term remains zero, the linear part
remains \(X\), all lower terms remain arbitrary homogeneous maps of degrees
two and three, and

\[
\widetilde H_4=(\widetilde p^2,\widetilde p\widetilde q,\widetilde q^2)
\]

for the transformed coprime quadratic pencil.  Thus (2) loses none of the
Keller problem and makes no restriction on \(H_2,H_3\).

There is also a coordinate-free construction.  The projective image of
\([H_4]\) is the intrinsic smooth conic \(C\); its normalization is
\(\mathbb P^1\), and the pullback of \(\mathcal O_C(1)\) is
\(\mathcal O_{\mathbb P^1}(2)\).  Choosing coordinates only after this
intrinsic construction yields (2).  No coefficient of \(H_4\) is selected,
inverted, or assumed nonzero.

## Pointwise coverage of the frozen coefficient pivots

For each frozen pivot stratum \(C_i\), take an arbitrary point \(F\in C_i\).
The construction above uses only its canonical image conic and canonical
relative-closed pencil.  It therefore applies verbatim to that point.

The conic spans the target \(\mathbb P^2\), so the three component quartics
of \(H_4\) are linearly independent.  In particular, its first component
is never the zero polynomial.  Since the frozen coefficient order puts all
fifteen coefficients of that component first, `C15`--`C44` are empty on
this row.  The coverage map is:

| Frozen pivots | Pointwise destination |
|---|---|
| `C00`, `C01`, `C02`, `C03`, `C04` | canonical Veronese form (2) |
| `C05`, `C06`, `C07`, `C08`, `C09` | canonical Veronese form (2) |
| `C10`, `C11`, `C12`, `C13`, `C14` | canonical Veronese form (2) |
| `C15`, `C16`, `C17`, `C18`, `C19` | empty |
| `C20`, `C21`, `C22`, `C23`, `C24` | empty |
| `C25`, `C26`, `C27`, `C28`, `C29` | empty |
| `C30`, `C31`, `C32`, `C33`, `C34` | empty |
| `C35`, `C36`, `C37`, `C38`, `C39` | empty |
| `C40`, `C41`, `C42`, `C43`, `C44` | empty |

Any additional empty intersection among `C00`--`C14` causes no problem.
For every nonempty intersection the route is pointwise and
coefficient-pivot-independent.
The 45 pivots do **not** determine the internal geometry of the quadratic
pencil.  Any downstream split must therefore be by an invariant of the
canonical pencil, not by a preferred coefficient.

## Relative closure and the generic conic

Resolve the base locus of the rational map

\[
\pi=[p:q]:\mathbb P^2\dashrightarrow\mathbb P^1.
\]

The equality \(E_{H_4}=\mathbb C(p/q)\) means that
\(\mathbb C(p/q)\) is relatively algebraically closed in
\(\mathbb C(\mathbb P^2)\).  Equivalently, the geometric generic fibre of
the resolved map is connected.  Since the generic fibre is a degree-two
plane curve, this is equivalent here to geometric integrality of the
generic conic

\[
p-tq=0\quad\text{over }\mathbb C(t).
\tag{4}
\]

The coprimality of \(p,q\) is already part of the canonical construction;
there is no fixed curve component.

## Number of double-line pencil members

A double-line member is a projective pencil member equal to \(\ell^2\) for
a nonzero linear form \(\ell\).

### At most two

If the pencil contains two distinct double lines \(\ell^2,m^2\), then
\(\ell,m\) are linearly independent.  Every other member is
\(u\ell^2+v m^2\).  Such a member is a square only when \(uv=0\): a square
in the span must be \((a\ell+b m)^2\), whose cross coefficient forces
\(ab=0\).  Thus a pencil has at most two double-line members.

### Two are incompatible with canonical relative closure

If the two members exist, use them as a pencil basis:

\[
p=\ell^2,\qquad q=m^2.
\]

Then

\[
\frac pq=\left(\frac{\ell}{m}\right)^2,\qquad
\frac{\ell}{m}\in\mathbb C(\mathbb P^2).
\]

The element \(\ell/m\) is algebraic of degree two over
\(\mathbb C(p/q)\), but it is not in \(\mathbb C(p/q)\).  For example, the
divisor valuation at \(\ell=0\) is odd on \(\ell/m\) but every nonzero
element of \(\mathbb C((\ell/m)^2)\) has even valuation there.  Hence the
relative algebraic closure strictly contains \(\mathbb C(p/q)\), contrary
to \(\nu=1\).  Equivalently, (4) splits after adjoining \(\sqrt t\).

So **two double-line members cannot occur in this frozen row**.  Recomputing
relative closure replaces the quadratic pencil by the linear pencil
\(\langle\ell,m\rangle\).  Then
\[
H_4\sim(\ell^4,\ell^2m^2,m^4),
\]
whose binary quartic map has conic image and degree two onto that image.
Its canonical tuple is therefore
\((e,a,b,\delta,\nu)=(0,1,4,2,2)\), so it routes specifically to
`Q2-E0-A1-B4-D2-N2`.  It is not an internal subtype of `N1`.

### Exactly one is possible

Take

\[
p=x^2,\qquad q=yz.
\]

They are coprime.  The only double-line member of their pencil is \(x^2\).
The generic conic \(x^2-t yz=0\) is nonsingular over
\(\overline{\mathbb C(t)}\), hence geometrically integral.  Therefore
\(\mathbb C(p/q)\) is relatively algebraically closed in
\(\mathbb C(\mathbb P^2)\), so this pencil is compatible with `N1`.

Intrinsically, the one-double-line locus may be written after a source
change as

\[
\langle p,q\rangle=\langle x^2,Q(x,y,z)\rangle,
\tag{5}
\]

where \(x\nmid Q\) and no other projective member is a square.  Formula (5)
is an internal normal form, not a frozen coefficient chart.

### Zero is possible

Take

\[
p=x^2+y^2,\qquad q=y^2+z^2.
\]

They are coprime.  A member has diagonal matrix
\(\operatorname{diag}(u,u+v,v)\); no nonzero pair \([u:v]\) makes this
matrix rank one, so the pencil has no double line.  Its generic member has
rank three, hence is geometrically integral.  This is compatible with
`N1`.

Thus the exhaustive possibilities inside the frozen row are:

\[
\boxed{\text{zero or exactly one double-line member}.}
\]

The zero/one split is an inclusive internal split of the canonical
quadratic-pencil normal form.  It does not create a new frozen leaf and it
is independent of C00--C44.

## Fail-closed requirements for a downstream exclusion

A downstream proof excludes this row only if all of the following hold:

1. it treats the general leading form \((p^2,pq,q^2)\) for every coprime
   quadratic pencil satisfying the `N1` relative-closure condition;
2. it covers both the zero-double-line and one-double-line loci, or proves a
   stronger argument that does not distinguish them;
3. it permits arbitrary \(H_2,H_3\) (and, before normalized conjugation, an
   arbitrary invertible linear part);
4. every division or computational chart has a proved exhaustive coverage
   map, independent of the frozen coefficient pivot;
5. any two-double-line specialization is routed out by recomputing the
   canonical relative closure, not silently included or discarded;
6. symbolic checks establish the asserted identities over the stated
   coefficient ring and do not replace a completeness proof.

Failure of any item is `FAIL`.
