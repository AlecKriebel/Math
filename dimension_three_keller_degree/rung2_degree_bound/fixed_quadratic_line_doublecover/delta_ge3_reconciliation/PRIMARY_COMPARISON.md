# Reconciliation of the frozen primary and blinded \(\delta\geq3\) denominators

**Compared packages.**

- Frozen primary:
  `binary_locus/delta_ge3_universal/`, count \(17/6/1\).
- Formerly blinded hostile audit:
  `audit_delta_ge3_denominator/`, count \(19/6/1\).

Neither package was edited during this reconciliation.

## 1. Executive conclusion

The numerical discrepancy
\[
19-17=2
\]
comes entirely from the branch-square chart.  Each of the primary
branch-square parameter families contains two distinct torus orbit types,
distinguished by whether one coefficient is zero.  The audit assigns
stable identifiers to all four orbits; the primary assigns two identifiers
and retains the zero-coefficient points inside them.  Thus the count
difference itself is quotient granularity, not two missing incidence
mechanisms.

There are nevertheless two substantive defects in the frozen primary
atlas which are independent of that arithmetic:

1. `D3-DN-L3` has an overlarge exact open.  Besides \(A=B\), the loci
   \(2A+B=0\) and \(A+2B=0\) have \(\delta=4\), not three.  They route to
   `D4-DN-PL3`.
2. `D3-SF-2C` incorrectly quotients its oriented incidence by
   \(z\leftrightarrow z^{-1}\), where \(z=s^2\), and consequently excludes
   the whole fibre \(\kappa=-16/5\).  Only \(z=-5\) jumps to
   \(\delta=4\); the reciprocal point \(z=-1/5\) remains exact
   \(\delta=3\).  This is one actual point-orbit omitted by the primary
   exact-open statement.

The correct F1 main denominator is therefore the audit's
\[
\boxed{19\text{ exact-}\delta=3+
6\text{ exact-}\delta=4+
1\text{ power fibre}=26.}
\]
It should be supplemented by stable identifiers for every retained
orbit-type pivot and every exit arrow, without counting those identifiers
again as main incidence families.

Both exact replays pass:

- primary marker:
  `DELTA_GE3_UNIVERSAL_STRICT_PASS_17_6_1`;
- audit marker:
  `DELTA_GE3_DENOMINATOR_STRICT_PASS_26`.

The first marker certifies the primary encoding; it does not repair the
two omitted parameter factors, because those factors were not encoded as
claims to test.

## 2. Coordinate dictionary

The primary squarefree chart uses
\[
L=p-sq,\qquad M=sp-q.
\]
The audit uses
\[
X=p-rq,\qquad Y=p-r^{-1}q,\qquad z=r^2.
\]
Set \(r=s\).  Then
\[
L=X,\qquad M=sY,\qquad LM=sXY,
\]
so scalar factors aside the two fixed divisors agree, and
\[
\kappa=(s+s^{-1})^2=z+2+z^{-1}.
\]

For all squarefree families except the oriented doubled-root/contact
family, the reciprocal presentations \(z,z^{-1}\) are equivalent and the
modulus is \(\kappa\).  For that oriented family they are distinct generic
orbits on one \(z\)-curve.

In the doubled-nonbranch chart \(L=p+q\), the parameter conversions are:

- primary `D3-DN-L3`: \(u=A,v=B\);
- primary `D3-DN-PL2`: audit \(B_{\rm aud}=C/2\);
- primary `D3-DN-PQL`: audit \(a=2A,d=2B\).

## 3. Complete ID map: exact \(\delta=3\)

### Branch-square chart

| frozen primary ID | audit ID(s) | comparison |
|---|---|---|
| `D3-BS-P3` | `D3-BS-N2-Z`, `D3-BS-N2-NZ` | The primary form \(p^2(Ap+Bq)\), \(B\ne0\), is their union.  \(A=0\) gives `N2-Z`; \(A\ne0\) gives `N2-NZ` after the residual torus quotient.  \(B=0\) exits to the power fibre. |
| `D3-BS-P2Q` | `D3-BS-N1-BR2`, `D3-BS-N1-CONTACT` | The primary form \(p(Ap^2+Cq^2)\), \(C\ne0\), is their union.  \(A=0\) gives `N1-BR2`; \(A\ne0\) gives `N1-CONTACT` after the torus quotient.  \(C=0\) exits to the power fibre. |

This is the complete explanation of \(19-17=2\).  The zero/nonzero
condition is invariant under the residual diagonal torus, so the audit's
four stable IDs are required by the amended F1 convention.

### Two-branch and one-branch charts

| frozen primary ID | audit ID | normal-form check |
|---|---|---|
| `D3-TB-P3` | `D3-BB-30` | identical: \(h=pq,R=p^3\) |
| `D3-TB-P2Q` | `D3-BB-21` | identical: \(h=pq,R=p^2q\) |
| `D3-OB-P3` | `D3-OB-300` | identical |
| `D3-OB-P2L` | `D3-OB-210` | identical |
| `D3-OB-PL2` | `D3-OB-120` | identical |
| `D3-OB-P2Q` | `D3-OB-20C` | identical |
| `D3-OB-PQL` | `D3-OB-11C` | differs by the scalar \(-1\) in the residual linear factor |
| `D3-OB-QL2` | `D3-OB-02C` | differs by the scalar \(-1\) |

All eight correspondences have the same exact gcd signature and no guard
discrepancy.

### Doubled-nonbranch chart

| frozen primary ID | audit ID | comparison |
|---|---|---|
| `D3-DN-L3` | `D3-DN-2` | Same form \(R=L^2(Ap+Bq)\), but the primary guard \(A-B\ne0\) is incomplete.  The exact guard is \((A-B)(2A+B)(A+2B)\ne0\). |
| `D3-DN-PL2` | `D3-DN-1C` | Put \(B_{\rm aud}=C/2\).  The primary guard \((2A+C)(A-C)\ne0\) becomes \((A+B_{\rm aud})(A-2B_{\rm aud})\ne0\), exactly the audit guard. |
| `D3-DN-PQL` | `D3-DN-0CC` | Put \(a=2A,d=2B\).  The forms and guard \(A-B\ne0\) agree. |

The omitted factors in the first row are directly visible:
\[
\begin{aligned}
R&=L^2(p-2q)&&\Rightarrow&
g&\doteq pL^3,\\
R&=L^2(-2p+q)&&\Rightarrow&
g&\doteq qL^3.
\end{aligned}
\]
Thus both omitted points are the two swapped presentations of
`D4-DN-2C` / primary `D4-DN-PL3`.  No point is absent from the union of
primary rows, but the claimed exact-\(\delta=3\) open overlaps a
\(\delta=4\) row.

### Squarefree interior chart

| frozen primary ID | audit ID | normal-form and quotient check |
|---|---|---|
| `D3-SF-21` | `D3-SF-21` | \(L^2M=sX^2Y\); same family, \(\kappa\)-modulus, and exact guards. |
| `D3-SF-2C` | `D3-SF-20C` | The primary form is the negative of \(X^2((5-3z)p+4rq)\).  The form agrees, but the primary quotient and \(\kappa=-16/5\) guard do not; this family's modulus is \(z\). |
| `D3-SF-11C` | `D3-SF-11C` | A branch swap takes \(LM(4rp+(z+1)q)\) to the audit form \(XY((z+1)p+4rq)\); guards agree. |
| `D3-SF-1C2` | `D3-SF-10CC` | After the branch swap, its quadratic coefficients are proportional to \(A=4r(1-3z), B=(z-3)(1-3z), C=4r(z-3)\), which satisfy \((z-3)A=4rB\) and \((1-3z)C=4rB\).  Guards agree. |

For the exceptional second row, the fibre
\(\kappa=-16/5\) consists of
\[
5z^2+26z+5=(z+5)(5z+1)=0.
\]
At \(z=-5\), `D3-SF-20C` acquires the fourth gcd factor and exits to
`D4-SF-21C`.  At \(z=-1/5\), its gcd remains exactly degree three.
The two points cannot be equivalent because \(\delta\) is invariant.
Hence the primary arrow
“\(\kappa=-16/5\to\)`D4-SF-21C`” for this oriented family is false on
one reciprocal sheet.

The special values \(z=3,1/3\), lying over \(\kappa=16/3\), remain in
the exact-\(\delta=3\) families.  The primary polynomial formulas happen
to remain defined there, but its denominator does not give these
alternate orbit-type presentations stable boundary IDs.

## 4. Complete ID map: exact \(\delta=4\) and power fibre

| frozen primary ID | audit ID | check |
|---|---|---|
| `D4-DN-L4` | `D4-DN-3` | identical: \(R=L^3,\ g\doteq L^4\) |
| `D4-DN-PL3` | `D4-DN-2C` | identical: \(R=L^2(p-2q),\ g\doteq pL^3\), up to swap |
| `D4-DN-PQL2` | `D4-DN-1CC` | identical: \(R=L(2p^2+pq+2q^2),\ g\doteq pqL^2\) |
| `D4-SF-21C` | `D4-SF-21C` | \(s^2+5=0\) is \(z=-5\), hence \(\kappa=-16/5\); forms agree up to scalar |
| `D4-SF-2C2` | `D4-SF-20CC` | \(5s^4-6s^2+5=0\) is \(5z^2-6z+5=0\), hence \(\kappa=16/5\); forms agree up to scalar |
| `D4-SF-11C2` | `D4-SF-11CC` | \(s^2-4s+1=0\) gives \(z+1=4s\), so the audit residual line is a scalar multiple of \(p+q\); the sign-conjugate equation is the same orbit |
| `PF-BS` | `PF-BRANCH-FOURTH-THIRD` | identical: \(h=p^2,R=p^3\), with homogeneous gcd \(p^4q\) of degree five |

Thus all six exact-\(\delta=4\) normal forms and the power orbit agree.

## 5. Exceptional-modulus ledger

| value | exact equation on the \(z\)-cover | reconciled role |
|---|---|---|
| \(\kappa=4\) | \((z-1)^2=0\) | doubled-nonbranch boundary; all primary destinations agree |
| \(\kappa=0\) | \((z+1)^2=0\) | retained stabilizer jump; for `D3-SF-20C` the two generic orientations meet |
| \(\kappa=-16/5\) | \((z+5)(5z+1)=0\) | `SF-21` and `SF-11C` descend to \(\kappa\) and jump to `D4-SF-21C`; oriented `SF-20C` jumps only at \(z=-5\), retaining \(z=-1/5\) |
| \(\kappa=16/5\) | \(5z^2-6z+5=0\) | one `D4-SF-20CC` orbit; primary and audit agree |
| \(\kappa=16/3\) | \((z-3)(3z-1)=0\) | retained exact-\(\delta=3\) alternate charts in `SF-20C` and `SF-10CC` |
| \(\kappa=16\) | \(z^2-14z+1=0\) | one `D4-SF-11CC` orbit; primary and audit agree |

This ledger checks every exceptional modulus appearing in either package.

## 6. Coverage verdict

The answer to “missing coverage or quotient granularity?” is necessarily
two-part:

- **For the numerical 19-versus-17 discrepancy:** quotient granularity.
  The two primary BS normal forms cover all four audit BS orbits, but do
  not assign the two zero-coefficient orbit types their own IDs.
- **For the frozen primary atlas as a whole:** there is one genuine
  missing exact-\(\delta=3\) point-orbit, `D3-SF-20C` at \(z=-1/5\),
  caused by an invalid reciprocal quotient.  There is also an exact-open
  overlap at the two omitted DN contact factors.

No new coarse mechanism, Hilbert--Burch shape, exact-\(\delta=4\) orbit,
or power fibre was found.

## 7. F1-compliant canonical denominator

### 7.1 Main family ledger

Adopt the audit IDs and guards as the canonical main family ledger:

- 19 exact-\(\delta=3\) IDs:
  four BS, two BB, six OB, four SF, three DN;
- 6 exact-\(\delta=4\) IDs:
  three SF and three DN;
- 1 dependent power-fibre ID.

Retain the primary IDs only as aliases in a migration table.  In
particular:

- split each primary BS alias into its two audit IDs;
- correct `D3-DN-2` to include all three guard factors;
- parameterize `D3-SF-20C` by \(z\), not \(\kappa\), and retain
  \(z=-1/5\).

This gives disjoint parameterized incidence strata and a stable main
denominator of 26.

### 7.2 Stable boundary-chart registry

F1 requires boundary charts to be addressable even when they are retained
inside a main family and therefore do not increment the main count.
The canonical machine-readable denominator should have a separate
`boundary_charts` collection with fields
`id`, `source`, `condition`, `kind`, and `destination`.

At minimum, assign stable IDs to the following retained orbit-type pivots:

| proposed boundary ID | source and condition |
|---|---|
| `BC-SF21-K0` | `D3-SF-21`, \(\kappa=0\) |
| `BC-SF20C-ZM1` | `D3-SF-20C`, \(z=-1\) |
| `BC-SF20C-ZM1_5` | `D3-SF-20C`, \(z=-1/5\) |
| `BC-SF20C-Z3` | `D3-SF-20C`, \(z=3\) |
| `BC-SF20C-Z1_3` | `D3-SF-20C`, \(z=1/3\) |
| `BC-SF11C-K0` | `D3-SF-11C`, \(\kappa=0\) |
| `BC-SF10CC-K0` | `D3-SF-10CC`, \(\kappa=0\) |
| `BC-SF10CC-Z3` | `D3-SF-10CC`, \(z=3\) |
| `BC-SF10CC-Z1_3` | `D3-SF-10CC`, \(z=1/3\) |
| `BC-DN2-ANTIDIAG` | `D3-DN-2`, \([u:v]=[1:-1]\) |
| `BC-DN0CC-ANTIDIAG` | `D3-DN-0CC`, \([a:d]=[1:-1]\) |

The two BS closure pivots already have stable destination family IDs:

- `D3-BS-N2-NZ` tail \(a\to0\) lands in `D3-BS-N2-Z`;
- `D3-BS-N1-CONTACT` coefficient \(a\to0\) lands in
  `D3-BS-N1-BR2`.

Every exit condition in the audit boundary atlas should likewise receive
an arrow ID, even when its destination is already a main family.  A
deterministic convention such as
`BX-<SOURCE>-<CONDITION>` is sufficient.  Required exits include:

- the two BS-to-power exits and power-to-`L00`;
- all \(z=0,\infty\), \(\kappa=4\), and exceptional-modulus SF exits;
- all three `D3-DN-2` boundary divisors, both `D3-DN-1C` divisors, and
  the diagonal of `D3-DN-0CC`.

Boundary IDs belong to the completeness certificate but are not additional
main-family counts.  If the program instead chooses to count every
zero-dimensional retained pivot as a separate “family,” it must publish a
larger denominator and change the meaning of *family* globally; mixing
that convention with the audit's 19/6/1 count would be inconsistent.

## 8. Recommendation

Use the audit package as the canonical F1 denominator, after adding the
separate stable boundary-chart/arrow registry described above.  Mark the
frozen primary \(17/6/1\) artifact as a valuable coarse derivation that is
superseded for enumeration purposes, not rewritten:

- its Hilbert--Burch shape and all six \(\delta=4\) families survive;
- its two BS families refine into four;
- its DN guard needs two factors;
- its oriented SF quotient needs the \(z\)-modulus correction.

This resolves the independent-enumeration discrepancy without silently
growing either frozen source denominator.
