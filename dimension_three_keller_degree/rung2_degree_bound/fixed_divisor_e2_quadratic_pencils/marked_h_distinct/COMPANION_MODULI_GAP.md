# Companion-moduli gap and freeze violation

## Verdict

The proposed denominator
\[
3\text{ marked-\(h\) orbits}\times
2\text{ cubic companion orbits}=6
\]
is **not complete**.  The six exact \(E_7/E_6\) calculations in this
directory are valid coordinate slices, but they are not an exhaustive
taxonomy.

Under the freeze-violation protocol, lower exclusion work was stopped.
The subsequent clean-room reconstruction in
`../audit_marked_orbit_reconstruction/REPORT.md` independently confirmed
the exact quotient \(3+\mathbb P^1+3\).  See
`FREEZE_READINESS_COMPARISON.md` for the name map and symbolic
\(E_7/E_6\) comparison.  Nothing in this note closes or promotes the
frozen row.

This note is not peer reviewed.  It was materially AI-assisted.  The
accompanying exact checks are evidence about the encoded identities, not
peer review.

## 1. Exact counterexample to endpoint exhaustion

Take
\[
s=x^2,\qquad h=r=yz,\qquad
H_4=(h^2,hs,0).
\]
The certified top kernel is
\[
x\langle s,h\rangle.
\]
Besides the two endpoint cubics \(xh=xyz\) and \(xs=x^3\), it contains
\[
\boxed{G=x(s+h)=x(x^2+yz)}.                           \tag{1}
\]
Direct expansion gives
\[
\operatorname{Jac}(h^2,hs,G)=0.                      \tag{2}
\]
The quadratic quotients by the intrinsic line \(x=0\) have ranks
\[
\operatorname{rank}(s)=1,\qquad
\operatorname{rank}(h)=2,\qquad
\operatorname{rank}(s+h)=3.                          \tag{3}
\]
Consequently (1) cannot be equivalent to either endpoint under an
invertible source change preserving the marked leading data: quadratic
rank is invariant.

A second counterexample occurs on the smooth marked member of the same
pencil:
\[
h=s+r=x^2+yz,\qquad G=xr=xyz.                         \tag{4}
\]
Here \(G/x=r\) has rank two, whereas the previously computed quotients
\(h\) and \(s\) have ranks three and one.  Again
\[
\operatorname{Jac}(h^2,hs,G)=0.
\]

Both SymPy and PARI/GP reconstruct (2)--(4) exactly in
`verify_companion_moduli_sympy.py` and
`verify_companion_moduli_pari.gp`.

## 2. Why the pencil-shear argument fails

Write a general nonzero normal cubic as
\[
G=x(\alpha h+\beta s).
\]
When \(\beta\ne0\), one can introduce a new pencil basis member
\[
q'=s+\frac{\alpha}{\beta}h
\]
and then write \(G=\beta xq'\).  But this basis change also changes the
second leading coordinate from \(hs\) to \(hq'\).  If one shears the
leading pair back to the canonical \((h^2,hs)\), the mixed term in \(G\)
returns, because an invertible target change among the first two
coordinates does not change the third cubic component.

Thus “choose \(q'=G/x\)” is a useful coordinate description, not an
equivalence between \(G=x(\alpha h+\beta s)\) and \(G=xs\).

More invariantly, the two-dimensional leading component span determines
the component gcd \([h]\) and the residual pencil \(V\).  Its unique
double member determines \([s]=[\ell^2]\), hence the line \([\ell]\).
The target covector annihilating the leading component span is unique up
to scalar, so it determines \([G]\), and therefore
\[
[g]=[G/\ell]\in\mathbb P(V),                          \tag{5}
\]
up to the source stabilizer.  A target basis change in \(V\) does not
erase the projective point (5).

## 3. The invariant moduli problem

Let \(W\cong\mathbb C^3\), let
\[
V\subset\operatorname{Sym}^2(W^\vee)
\]
be one of the two minimal canonical pencils, let \([s]=[\ell^2]\) be its
unique double member, and let \([h]\in\mathbb P(V)\setminus\{[s]\}\) be
the fixed-gcd member.  Define
\[
\Gamma_{V,[h]}
=
\left\{
\gamma\in\operatorname{PGL}(W):
\gamma^*V=V,\ \gamma^*[h]=[h]
\right\}.                                             \tag{6}
\]
The unique double member is intrinsic, so every element of (6) also
fixes \([s]\).

The correct companion parameter space is
\[
\boxed{
\mathcal C(V,[h])
=
\Gamma_{V,[h]}\backslash\mathbb P(V),
}                                                     \tag{7}
\]
where \([g]\in\mathbb P(V)\) represents the nonzero cubic
\([G]=[\ell g]\).  Equivalently, the global problem is the
\(\operatorname{PGL}(W)\)-quotient of quadruples
\[
(V,[s],[h],[g]).
\]
This is the object an independent reconstruction must freeze before any
further lower-identity case count is meaningful.

## 4. Pre-audit candidate quotient stratification over \(\mathbb C\)

The following was derived before the hostile reconstruction and was later
confirmed exactly by it.  It is retained here to preserve provenance; the
clean-room report is authoritative for stable IDs.

Write a pencil member as
\[
g=a\,s+b\,r,\qquad t=a/b,
\]
so \(r\) is \(t=0\) and \(s\) is \(t=\infty\).

### Rank-two pencil

For
\[
V_{\mathrm{RT}}=\langle x^2,yz\rangle
\]
the conic determinant is
\[
\det(a\,x^2+b\,yz)=-\frac14ab^2.                     \tag{8}
\]
The double and simple points of this discriminant divisor are intrinsic,
so the induced base action fixes \(s\) and \(r\).  Conversely diagonal
source scalings realize every \(t\mapsto ct\) over \(\mathbb C\).  Thus
the induced group is \(\mathbb G_m\).

- If \(h=r\), the proposed companion orbits are
  \[
  \{r\},\qquad\{s\},\qquad
  \mathbb P(V)\setminus\{r,s\},
  \]
  represented by \(r,s,s+r\).
- If \(h=s+r\), fixing \(h\) kills the \(\mathbb G_m\) action.  The
  proposed quotient is the entire projective line:
  \[
  \mathcal C(V_{\mathrm{RT}},[s+r])\cong\mathbb P^1.
  \]
  In particular this marked orbit carries a genuine companion modulus,
  not a finite two-leaf split.

### Rank-one pencil

For
\[
V_{\mathrm{RO}}=\langle x^2,y^2+xz\rangle
\]
the conic determinant is
\[
\det(a\,x^2+b(y^2+xz))=-\frac14b^3.                  \tag{9}
\]
The induced base action fixes only \(s\).  The source shear
\[
z\mapsto z+\lambda x
\]
sends \(r\mapsto r+\lambda s\), and compatible diagonal scalings realize
the dilations.  These generate the affine group on
\(\mathbb P^1\setminus\{s\}\).  With \(h=r\) fixed, the remaining action
is \(t\mapsto ct\), giving the proposed three companion orbits
\[
\{r\},\qquad\{s\},\qquad
\mathbb P(V)\setminus\{r,s\}.
\]

Equations (8)--(9) and the displayed source actions are independently
checked in SymPy and PARI.  The later hostile reconstruction also checked:

1. the claim that every legal source/target equivalence induces exactly
   the stated base action;
2. the intrinsic recovery of \([g]\) in (5) under the full allowed
   normalization group;
3. the boundary charts and stable identifiers for the parameterized
   rank-two smooth-marked family.

## 5. Effect on the six calculations

The existing calculations cover only:

| Marked orbit | computed companion points | omitted companion locus |
|---|---|---|
| RT, \(h=r=yz\) | \(g=h\), \(g=s\) | smooth orbit \(g=s+r\) |
| RT, \(h=s+r=x^2+yz\) | \(g=h\), \(g=s\) | \(\mathbb P^1\setminus\{h,s\}\) |
| RO, \(h=r=y^2+xz\) | \(g=h\), \(g=s\) | nonzero affine orbit \(g=s+r\) |

Their \(E_7/E_6\) ranks and compatibility ideals remain correct on those
six points.  They must be described as endpoint slices and cannot support
a completeness or promotion claim.

## 6. Gate

The independent reconstruction of (7) is now complete and agrees with
this note.  Do not resume \(E_5\) exclusions until the parent freeze
records:

- every discrete orbit;
- the full parameter space of every moduli leaf;
- every boundary and rank-drop chart;
- the exact action used to identify parameter values.

The reconstruction did not disagree with Section 4.  The remaining gate
is the explicit parent freeze, not another orbit derivation.
