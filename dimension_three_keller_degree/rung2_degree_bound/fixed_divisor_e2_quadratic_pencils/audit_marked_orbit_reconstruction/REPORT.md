# Clean-room reconstruction: marked \(h\ne s\) quadratic-pencil orbits

## Result

**COMPLETE.**  There are exactly three marked-pair orbits.  Two have three
nonzero companion orbits each.  The third has a full
\(\mathbb P^1(\mathbb C)\) of companion orbits, separated by an intrinsic
cross-ratio.  Thus the marked-member taxonomy is complete but not finite.
These are internal branch IDs inside one inclusive frozen leaf; they do not
alter the frozen denominator.

## Scope and input boundary

This report reconstructs the marked-member orbit taxonomy inside the frozen
quartic row
`Q2-E2-A2-B1-D1-N1`.  During the derivation it used only the frozen row
definition, the statement of the all-vertical top-obstruction theorem, the
statement of the top row theorem, and elementary linear algebra.

The existing `marked_h_distinct/` package, its branch names, the row
`READINESS` report, and all exclusion proofs remained unread until the
classification below was complete and checkpointed.

## 1. Intrinsic marked object

The frozen row has
\[
H_4=(hp,hq,0),\qquad
\deg h=\deg p=\deg q=2,
\]
where \(p,q\) are coprime and span a minimal quadratic pencil.  The
all-vertical top theorem reduces the nonzero cubic-normal frontier to
\[
p=h,\qquad
s=\ell^2\in L:=\langle h,q\rangle,\qquad
G=(H_3)_3=\ell r,\quad 0\ne r\in L.
\]
The double-line point \([s]\in\mathbb P(L)\) is unique.  This report treats
the missing marked case
\[
[h]\ne[s].
\]

Since \(h\) and \(s\) are distinct members, they form a basis of \(L\).
Writing \(s=ah+bq\) has \(b\ne0\), so
\(\gcd(h,s)=\gcd(h,q)=1\).
Thus, after a target change inside the pencil,
\[
H_4=(h^2,hs,0).
\]
The classification problem is therefore the ordered projective
configuration
\[
\bigl(L;\ [h],\ [s=\ell^2],\ [r]\bigr)
\]
under source \(\operatorname{PGL}_3(\mathbb C)\).  A change of pencil basis
only changes coordinates on \(\mathbb P(L)\); it does not move any of the
intrinsic marked points.  In particular, cross-ratios of intrinsic points
cannot be discarded by a target reparametrization.

Allowing a source translation does not enlarge the companion action.  Its
change to the cubic term is a directional derivative of \(H_4\), which
still lies in the two-dimensional target span of \(H_4\).  The normal
quotient kills that change, so the projective normal companion \([r]\)
is unaffected.

The zero-normal case \(G=0\) is recorded separately as a terminal branch.
For \(G\ne0\), scalar changes of the normal target coordinate make
\([r]\), rather than a chosen scalar representative \(r\), intrinsic.

## 2. Reduction of the ordered pair \(([h],[s])\)

Choose source coordinates with \(\ell=x\), so \(s=x^2\).  Write
\[
h=a x^2+2xv^Tu+u^TCu,\qquad u=(y,z)^T,
\]
with \(C=C^T\) a binary symmetric matrix.  Coprimality of \(h\) and \(s\)
forces \(C\ne0\): if \(C=0\), then \(x\mid h\).

### Rank-two restriction

Suppose \(\operatorname{rank}C=2\).  A shear
\[
u\longmapsto u-C^{-1}v\,x
\]
kills the \(xu\) terms.  Over \(\mathbb C\), a nonsingular binary
quadratic form is equivalent to \(yz\).  The remaining coefficient of
\(x^2\) is either zero or nonzero, giving exactly
\[
h=yz
\qquad\text{or}\qquad
h=x^2+yz.
\]
These cannot be equivalent as marked conics because their ranks are
respectively \(2\) and \(3\).

### Rank-one restriction

Suppose \(\operatorname{rank}C=1\).  A binary source change and an
\(x\)-shear put
\[
h=y^2+2B xz+A x^2.
\]
If \(B=0\), then
\[
y^2=h-Ax^2\in L
\]
is a second double-line member, contradicting uniqueness of \(s\).
Therefore \(B\ne0\).  A \(z\)-shear kills \(A x^2\), and rescaling gives
\[
h=y^2+xz.
\]

These cases are exhaustive because \(C\ne0\).  Hence the ordered marked
pair has exactly three source orbits:

| independent pair ID | \(s\) | \(h\) | pencil \(L\) | \(\operatorname{rank}h\) | \(\operatorname{rank}(h|_{x=0})\) |
|---|---|---|---|---:|---:|
| `Q2-E2-A2-B1-D1-N1-MD-P21-HR2` | \(x^2\) | \(yz\) | \(\langle x^2,yz\rangle\) | 2 | 2 |
| `Q2-E2-A2-B1-D1-N1-MD-P21-HSM` | \(x^2\) | \(x^2+yz\) | \(\langle x^2,yz\rangle\) | 3 | 2 |
| `Q2-E2-A2-B1-D1-N1-MD-P3-HSM` | \(x^2\) | \(y^2+xz\) | \(\langle x^2,y^2+xz\rangle\) | 3 | 1 |

Here `MD` means “marked distinct,” `P21` and `P3` record the
multiplicity partition of the pencil discriminant, and `HR2`/`HSM`
record whether the fixed gcd member \(h\) is rank two or smooth.

Indeed, for pencil coordinates \([A:B]\),
\[
\begin{array}{c|c}
L&\det(A s+B h)\\ \hline
\langle x^2,yz\rangle,\ h=yz
   &-\frac14 A B^2,\\[2mm]
\langle x^2,yz\rangle,\ h=x^2+yz
   &-\frac14(A+B)B^2,\\[2mm]
\langle x^2,y^2+xz\rangle
   &-\frac14B^3 .
\end{array}
\]
In all three cases \(s\) is the unique rank-one member.  In the first two
cases the pencil has one additional rank-two member
\[
t=yz;
\]
in the third case \(s\) is the only singular member.

## 3. Source action on the pencil

The companion classification must use the source-induced action on
\(\mathbb P(L)\), not the full abstract
\(\operatorname{PGL}_2\) after marked points have been fixed.

### The `P21` pencil

For
\[
L_{21}=\langle s=x^2,t=yz\rangle,
\]
the unique rank-one point \(s\) and the unique other singular point \(t\)
are intrinsic, so every source automorphism of the pencil fixes both.
Diagonal source changes
\[
x\mapsto ax,\qquad y\mapsto cy,\qquad z\mapsto dz
\]
scale \(s\) by \(a^2\) and \(t\) by \(cd\).  Their ratio is arbitrary.
Thus the induced group on
\(\mathbb P(L_{21})\) is the full one-dimensional torus fixing \(s,t\).

- If the marked gcd is \(h=t\), the residual torus remains.
- If the marked gcd is a smooth point, normalize it to \(h=s+t\).
  Its stabilizer must fix the three distinct points \(s,t,h\), so it acts
  identically on \(\mathbb P(L_{21})\).

### The `P3` pencil

For
\[
L_3=\langle s=x^2,u=y^2+xz\rangle,
\]
the discriminant has the single triple root \(s\).  The source shear
\[
z\mapsto z+\mu x
\]
sends \(u\) to \(u+\mu s\), while diagonal changes realize dilations of
the affine parameter.  Hence the source-induced group is the affine group
fixing \(s\), and is transitive on the smooth members.  Normalize the
marked gcd to \(h=u\).  The residual stabilizer fixes \(s,h\) and acts
transitively on the other smooth members.

## 4. Complete companion taxonomy

Append `-C0` to any pair ID for the terminal case \(G=0\).  For
\(G\ne0\), write \(G=xr\) in the displayed coordinates.

### Pair `Q2-E2-A2-B1-D1-N1-MD-P21-HR2`

Here \(h=t=yz\).  The residual torus has exactly three orbits on
\(\mathbb P(L)\):

| stable branch ID | companion point | representative \(G=xr\) |
|---|---|---|
| `Q2-E2-A2-B1-D1-N1-MD-P21-HR2-CH` | \(r=h=yz\) | \(xyz\) |
| `Q2-E2-A2-B1-D1-N1-MD-P21-HR2-CS` | \(r=s=x^2\) | \(x^3\) |
| `Q2-E2-A2-B1-D1-N1-MD-P21-HR2-CO` | \(r\notin\{h,s\}\) | \(x(yz+x^2)\) |

`CO` is one open companion orbit.

### Pair `Q2-E2-A2-B1-D1-N1-MD-P21-HSM`

Here
\[
s=x^2,\qquad t=yz,\qquad h=s+t=x^2+yz.
\]
The residual action on the pencil is trivial.  Therefore **the companion
has a genuine one-parameter invariant**; it is not legitimate to merge all
smooth companions.

Define the intrinsic coordinate \(\tau\in\mathbb P^1\) by
\[
[r_\tau]=[h+\tau s]\quad(\tau\in\mathbb C),
\qquad [r_\infty]=[s].
\]
Equivalently, it is the unique projective coordinate satisfying
\[
h\longmapsto0,\qquad t\longmapsto-1,\qquad s\longmapsto\infty.
\]
Thus \(\tau\) is a cross-ratio coordinate defined by intrinsic points, not
by arbitrary scalar choices.

| stable branch ID | parameter | companion |
|---|---:|---|
| `Q2-E2-A2-B1-D1-N1-MD-P21-HSM-CH` | \(0\) | \(r=h\) |
| `Q2-E2-A2-B1-D1-N1-MD-P21-HSM-CT` | \(-1\) | \(r=t\), the rank-two member |
| `Q2-E2-A2-B1-D1-N1-MD-P21-HSM-CS` | \(\infty\) | \(r=s\) |
| `Q2-E2-A2-B1-D1-N1-MD-P21-HSM-CTAU` | \(\tau\in\mathbb C\setminus\{0,-1\}\) | \(r=h+\tau s\) |

Every distinct value of \(\tau\) in the last row is a distinct source
orbit.  `CTAU` is a stable ASCII family ID whose branch key must also carry
the field `tau=<value>`; it is not a claim that the punctured parameter
line is one orbit.

### Pair `Q2-E2-A2-B1-D1-N1-MD-P3-HSM`

Here \(h=y^2+xz\).  The residual multiplicative group has exactly three
orbits:

| stable branch ID | companion point | representative \(G=xr\) |
|---|---|---|
| `Q2-E2-A2-B1-D1-N1-MD-P3-HSM-CH` | \(r=h\) | \(x(y^2+xz)\) |
| `Q2-E2-A2-B1-D1-N1-MD-P3-HSM-CS` | \(r=s=x^2\) | \(x^3\) |
| `Q2-E2-A2-B1-D1-N1-MD-P3-HSM-CO` | \(r\notin\{h,s\}\) | \(x(y^2+xz+x^2)\) |

Again, `CO` is one open companion orbit.

## 5. Completeness proof

The taxonomy is exhaustive in three independent stages:

1. The frozen row and top theorem reduce the marked frontier to a coprime
   ordered pair \((h,s=\ell^2)\) with \(s\in L\), \(h\ne s\), plus a
   projective companion point \([r]\in\mathbb P(L)\).
2. After \(s=x^2\), the nonzero restriction matrix \(C\) has rank two or
   one.  Rank two gives exactly the rank-two and smooth secant forms.
   Rank one either creates a forbidden second double line or gives the
   smooth tangent form.  Hence there are exactly three marked-pair orbits.
3. The source-induced pencil actions are respectively:
   a torus with \(h=t\), the identity with \(h=s+t\), and a torus after
   fixing \(h=u\) in the affine `P3` pencil.  Their orbit sets on the
   companion projective line are exactly those displayed above.

The invariants separating the three pair rows are ranks and discriminant
multiplicities.  The endpoints and open orbits in the first and third rows
are separated by equality with intrinsic marked points.  In the middle row,
the normalized cross-ratio \(\tau\) separates every remaining orbit.

Therefore the nonzero marked-\(h\)-distinct taxonomy consists of two
three-orbit families and one full projective-line family:
\[
\boxed{3\quad+\quad\mathbb P^1(\mathbb C)\quad+\quad3}.
\]
This count is an orbit-space description; it is not the cardinal sum
\(3+|\mathbb P^1|+3\) in a finite frozen denominator.

## 6. Independent conclusion before comparison

Any finite marked-member branch list is complete only if it either:

- retains the entire invariant \(\tau\) on
  `Q2-E2-A2-B1-D1-N1-MD-P21-HSM`, or
- proves an additional allowed equivalence or an independent Keller
  identity that removes it.

A bare source/projective pencil equivalence does not remove this modulus,
because the unique double line \(s\), the other singular member \(t\), and
the marked gcd member \(h\) fix three points of the pencil and leave no
nontrivial projective action.

## 7. Dependency-free exact checker

`verify_marked_orbits_exact.py` uses only the Python standard library.  It
checks:

- the ranks of the three canonical marked forms and their restrictions to
  \(x=0\);
- the three exact bivariate determinant polynomials;
- uniqueness of the double-line point in odd characteristics \(5\) and
  \(7\);
- an exhaustive enumeration of the full parabolic source group over
  \(\mathbb F_5\), recovering residual scaling images
  \(\mathbb F_5^\times\), \(\{1\}\), and the square subgroup for the three
  ordered pairs;
- the exact affine translation \(u\mapsto u+\mu s\) in the `P3` pencil;
- the second-double-line failure when the rank-one restriction has no
  transverse \(xz\) coupling.

The finite-field enumerations are fault-sensitive regression checks, not a
substitute for the characteristic-zero completeness proof above.  In the
third stabilizer, the finite-field square subgroup becomes all of
\(\mathbb C^\times\) because \(\mathbb C\) is algebraically closed.

Run:

```sh
cd dimension_three_keller_degree/rung2_degree_bound/fixed_divisor_e2_quadratic_pencils/audit_marked_orbit_reconstruction
/usr/bin/python3 verify_marked_orbits_exact.py
```

Observed output:

```text
PASS: 3 marked-pair types, discriminants, unique double lines, and residual companion actions verified
```

## 8. Post-derivation name-only comparison

Only after the independent classification and checker were locked, the
filesystem names under `marked_h_distinct/` were listed.  They are generic
package/checker names and expose no pre-existing branch nomenclature, so
there is no coordinate-safe name mapping to report.  No file in that
directory and no row `READINESS` report was opened or searched.

The stable IDs in this report are therefore deliberately independent.  They
encode the frozen row, the discriminant partition, the rank/location of
\(h\), and the companion position; the `CTAU` family additionally requires
the invariant `tau` field.
