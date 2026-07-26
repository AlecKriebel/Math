# Reconciliation of the two frozen \(\delta\geq3\) atlases

**Reconciled (UTC):** 2026-07-26T01:27:00Z.

## Verdict

The independently frozen atlases have the same six exact-\(\delta=4\)
orbits and power fibre.  Their numerical discrepancy
\[
17+6+1\qquad\hbox{versus}\qquad19+6+1
\]
is entirely a quotient-granularity discrepancy in the branch-square

The line-by-line reconciliation nevertheless found two genuine defects in
the frozen primary atlas:

1. `D3-DN-L3` omitted the guard factors \(2A+B\) and \(A+2B\).
   Its stated exact-\(\delta=3\) open therefore overlaps the
   exact-\(\delta=4\) orbit `D4-DN-PL3`.
2. The oriented family `D3-SF-2C` was incorrectly parameterized by
   \(\kappa=z+2+z^{-1}\).  At \(\kappa=-16/5\), only \(z=-5\)
   jumps to \(\delta=4\); the reciprocal point \(z=-1/5\) remains
   exact \(\delta=3\) and was omitted from the primary exact open.

Thus the count difference itself is not caused by missing mechanisms, but
the primary package is neither disjoint nor pointwise complete as frozen.
Its successful strict replay certifies its encoded algebra, not the two
guards that it failed to encode.

The canonical F1 denominator for subsequent lower work is the blinded
audit's finer denominator:
\[
\boxed{19\text{ exact-}\delta=3
      +6\text{ exact-}\delta=4
      +1\text{ power fibre}=26.}
\]
It is stored in
`../audit_delta_ge3_denominator/DENOMINATOR.json`.  Stable identifiers
for all retained pivots and exit arrows are separately frozen in
`BOUNDARY_CHARTS.json`; these do not increment the count twenty-six.

This reconciliation is an incidence classification only.  It excludes no
Keller map and changes neither the global frozen denominator of fourteen
quartic rows nor the certified total-degree floor of four.

## The only two splits

The primary family
\[
\texttt{D3-BS-P3}:\quad
h=p^2,\qquad R=p^2(Ap+Bq),\qquad B\ne0
\]
contains two residual-torus orbits:
\[
\begin{array}{c|c}
A=0&\texttt{D3-BS-N2-Z},\quad R=p^2q,\\
A\ne0&\texttt{D3-BS-N2-NZ},\quad R=p^2(p+q).
\end{array}
\]
The missing boundary \(B=0\) is the dependent power fibre.

Similarly,
\[
\texttt{D3-BS-P2Q}:\quad
h=p^2,\qquad R=p(Ap^2+Cq^2),\qquad C\ne0
\]
contains
\[
\begin{array}{c|c}
A=0&\texttt{D3-BS-N1-BR2},\quad R=pq^2,\\
A\ne0&\texttt{D3-BS-N1-CONTACT},\quad
R=p(p^2+q^2).
\end{array}
\]
The boundary \(C=0\) is again the power fibre.

A diagonal source transformation cannot turn a zero coefficient into a
nonzero one, while it makes every nonzero ratio in each display
equivalent over \(\mathbb C\).  Thus each primary display is the disjoint
union of exactly two quotient strata.  Under the amended F1 convention,
these orbit-type endpoints require stable identifiers, so the count
nineteen is canonical.

The retained points in the doubled-nonbranch and squarefree families are
different: after the continuous torus has been used to normalize \(h\),
they lie in genuine projective or root-cover parameter spaces modulo
finite groups.  Their stabilizer jumps and coordinate pivots are listed
inside the corresponding canonical family in
`DENOMINATOR.json`; they are not redundant torus orbits and are not
additional incidence families.

## Two primary guard defects

For
\[
\texttt{D3-DN-L3}:\quad
h=L^2,\qquad R=L^2(Ap+Bq),
\]
the correct exact open is
\[
(A-B)(2A+B)(A+2B)\ne0.
\]
The first removed point is `D4-DN-3`; the last two are swapped
presentations of `D4-DN-2C`.  The primary guard \(A-B\ne0\) therefore
made its \(\delta=3\) and \(\delta=4\) rows overlap.

For the squarefree oriented doubled-root/contact family, write
\(z=s^2\) and \(\kappa=z+2+z^{-1}\).  This relative orientation does
not descend through \(z\leftrightarrow z^{-1}\).  Indeed
\[
\kappa=-16/5
\quad\Longleftrightarrow\quad
(z+5)(5z+1)=0,
\]
but \(z=-5\) has gcd degree four while \(z=-1/5\) has gcd degree
three.  The canonical `D3-SF-20C` is therefore a \(z\)-family and
retains \(z=-1/5\); only \(z=-5\) exits to `D4-SF-21C`.

## Complete identifier map

The exact map is frozen in `canonical_mapping.json`.  Apart from the two
branch-square splits above, it is bijective:

| Primary ID | Canonical audit ID |
|---|---|
| `D3-TB-P3` | `D3-BB-30` |
| `D3-TB-P2Q` | `D3-BB-21` |
| `D3-OB-P3` | `D3-OB-300` |
| `D3-OB-P2L` | `D3-OB-210` |
| `D3-OB-PL2` | `D3-OB-120` |
| `D3-OB-P2Q` | `D3-OB-20C` |
| `D3-OB-PQL` | `D3-OB-11C` |
| `D3-OB-QL2` | `D3-OB-02C` |
| `D3-DN-L3` | `D3-DN-2` after adding the two missing guard factors |
| `D3-DN-PL2` | `D3-DN-1C` |
| `D3-DN-PQL` | `D3-DN-0CC` |
| `D3-SF-21` | `D3-SF-21` |
| `D3-SF-2C` | `D3-SF-20C` after replacing the false \(\kappa\)-quotient by the oriented \(z\)-family |
| `D3-SF-11C` | `D3-SF-11C` |
| `D3-SF-1C2` | `D3-SF-10CC` |
| `D4-DN-L4` | `D4-DN-3` |
| `D4-DN-PL3` | `D4-DN-2C` |
| `D4-DN-PQL2` | `D4-DN-1CC` |
| `D4-SF-21C` | `D4-SF-21C` |
| `D4-SF-2C2` | `D4-SF-20CC` |
| `D4-SF-11C2` | `D4-SF-11CC` |
| `PF-BS` | `PF-BRANCH-FOURTH-THIRD` |

The scalar and coefficient reparametrizations in the differently named
normal forms are recorded in the two source notes.  They do not change
the orbit.

## Verification and disclosure

Run `./verify_strict.sh`.  It first replays both frozen packages and then
checks that:

- all 24 primary identifiers occur exactly once as sources;
- all 26 canonical identifiers occur exactly once as destinations;
- precisely two sources split, both into two branch-square targets;
- the two primary guard defects are present and the canonical guards repair
  them;
- the coarse counts and Hilbert--Burch shapes agree; and
- the six exceptional moduli and the unique power fibre agree; and
- all 36 retained-pivot and exit-arrow identifiers cover the canonical
  boundary ledger exactly once.

This reconciliation and its checker were produced with substantial AI
assistance.  They are not peer reviewed.  Exact checks are evidence about
the encoded algebra, not peer review.
