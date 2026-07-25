# Candidate quartic incidence manifest

**Recorded (UTC):** 2026-07-25T19:30:28Z.

**Status:** candidate F1 enumeration, not frozen and not yet independently
certified.

## 1. Granularity rule

The global denominator must not change merely because a computation needs
another pivot.  Accordingly:

- a **row** is one of the fourteen leading rows in
  `CANDIDATE_GLOBAL_TAXONOMY.md`;
- a **leaf** is separated only by the structural invariants declared in
  this document; and
- every further coefficient specialization, resultant divisor, contact
  component, orbit representative, or normalization pivot is a **chart
  inside its existing leaf**, unless it changes a declared invariant.

If a specialization changes a declared invariant, the routing tables below
assign it to another frozen leaf.  If it fits neither rule, it is a freeze
violation.

The candidate denominator is
\[
\boxed{68\text{ structural leaves in }14\text{ leading rows}.}
\]
This is a proposed bookkeeping denominator, not a theorem until the blinded
derivation and chart audit agree with it.

## 2. Universal boundary atlas

Every normal-form parameter space is projectivized before localization.
Order its surviving homogeneous coefficients lexicographically as
\(c_0,\ldots,c_m\).  Its mandatory charts are
\[
\mathrm C_i=D_+(c_i)\setminus\bigcup_{j<i}D_+(c_j)
\qquad(0\le i\le m).
\]
This disjoint first-nonzero-coordinate atlas is exhaustive and has stable
labels.  A proof may use more convenient overlapping coordinates, but it
must certify their coverage of these frozen charts.  A denominator or
matrix pivot vanishing inside a \(\mathrm C_i\) is not a new leaf or chart:
it must be handled by saturation or by a division-free calculation in the
same chart.

At leading degree, a specialization that changes
\[
(\operatorname{rank}JH_4,e,a,b,\delta,\nu)
\]
is routed to the unique row with the new tuple.  Rank one is routed to
`Q1`; \(H_4=0\) is the already known degree-at-most-three boundary and is
outside the quartic denominator.

## 3. Rank-one row — 7 leaves

Write \(H_4=a h\), and let \(P,Q\) be the cubic pencil obtained from
\(H_3\bmod\mathbb Ca\).  Let \(f=\deg\gcd(P,Q)\) when \(P,Q\) are
independent.

| ID | Frozen invariant description |
|---|---|
| `Q1/L01` | \(\dim\langle P,Q\rangle\le1\). |
| `Q1/L02` | \(P,Q\) independent and \(f=2\); the reduced pencil is linear. |
| `Q1/L03` | \(P,Q\) independent, \(f=1\), and the reduced quadratic pencil is primitive. |
| `Q1/L04` | \(P,Q\) independent, \(f=1\), and the reduced quadratic pencil is a degree-two outer composite of a linear pencil. |
| `Q1/L05` | \(f=0\) and the cubic pencil is primitive. |
| `Q1/L06` | \(f=0\), the pencil is a degree-three outer composite of a linear pencil, and \(\gcd(J(P,Q),J(P,h),J(Q,h))=1\). |
| `Q1/L07` | The same composite case with nonconstant common Jacobian gcd. |

The values \(f=0,1,2\) are exhaustive for an independent cubic pair.
Relative algebraic closure gives the displayed primitive/composite split:
the only nontrivial factorizations of reduced degrees two and three are
\(2=1\cdot2\) and \(3=1\cdot3\).  Gcd growth routes from `L05`--`L07`
to `L03`/`L04` or `L02`; linear dependence routes to `L01`.

## 4. Rank-two rows

### `Q2-E0-A4-B1-D1-N1` — 2 leaves

| ID | Description |
|---|---|
| `L01` | The normal cubic component \(R_3\) vanishes. |
| `L02` | \(R_3\ne0\); the primitive first-integral theorem forces the \(L^4/L^3\) power-fibre incidence. |

The \(R_3=0,R_2=0\) and \(R_3=0,R_2\ne0\) branches are charts of `L01`,
not additional leaves.

### `Q2-E0-A2-B2-D1-N2` — 3 leaves

Separate the minimal quadratic pencil by its number and Kronecker type of
double-line members:

| ID | Description |
|---|---|
| `L01` | no double-line member; |
| `L02` | unique double line, rank-two restriction type \(\langle x^2,yz\rangle\); |
| `L03` | unique double line, rank-one restriction type \(\langle x^2,y^2+xz\rangle\). |

Two distinct double-line members make the displayed \((a,b)=(2,2)\)
presentation nonminimal and route to
`Q2-E0-A1-B4-D2-N2`.

### `Q2-E0-A2-B2-D2-N1` — 2 leaves

| ID | Description |
|---|---|
| `L01` | the minimal quadratic pencil has no double-line member; |
| `L02` | it has one double-line member. |

The two-double-line boundary routes to
`Q2-E0-A1-B4-D2-N2`.

### `Q2-E0-A1-B4-D1-N4` — 8 leaves

For a nonzero normal cubic \(R\), put
\[
g=\gcd(J(Q,R),J(P,R),J(P,Q)),\qquad \rho=\deg g.
\]
When the first two Jacobians are independent, use the Hilbert--Burch
splitting \(\{k_1,k_2\}\).

| ID | \(\rho\) and splitting |
|---|---|
| `L00` | the normal cubic \(R\) is zero; |
| `L01` | \(\rho=0,\{0,0\}\); |
| `L02` | \(\rho=1,\{1,0\}\); |
| `L03` | \(\rho=2,\{2,0\}\); |
| `L04` | \(\rho=2,\{1,1\}\); |
| `L05` | \(\rho=3,\{2,1\}\); |
| `L06` | \(\rho=4,\{2,2\}\); |
| `L07` | dependent Jacobians, equivalently the \(L^4/L^3\) power fibre (\(\rho=5\)). |

The ramification-divisor root partitions are charts inside `L02`--`L06`.
Coalescing roots remains in the same \(\rho\)-leaf; increasing gcd degree
routes to the corresponding later leaf.

### `Q2-E0-A1-B4-D2-N2` — 3 leaves

In the canonical leading form
\(\operatorname{Ver}(p^2,q^2)\), the complete degree-eight tangent is
indexed by two scalars \((a,b)\).

| ID | Description |
|---|---|
| `L01` | \(a=b=0\); |
| `L02` | \(ab\ne0\); |
| `L03` | exactly one of \(a,b\) is nonzero, modulo the swapping involution. |

All lower relative-position parameters are charts inside these leaves.

### `Q2-E0-A1-B4-D4-N1` — 2 leaves

For the basepoint-free birational quartic parametrization \(A\), put
\(\Delta=A_p\times A_q\).

| ID | Description |
|---|---|
| `L01` | \(\gcd(\Delta_1,\Delta_2,\Delta_3)=1\); |
| `L02` | the common ramification gcd is nonconstant. |

Ramification degree, root partition, and singularity type are charts of
`L02`; they do not alter the denominator.

### `Q2-E1-A3-B1-D1-N1` — 2 leaves

| ID | Description |
|---|---|
| `L01` | horizontal: no member of the primitive cubic pencil is divisible by the fixed line \(h\); |
| `L02` | vertical: some pencil member is divisible by \(h\). |

Multiplicity and residual-factor types in the vertical pencil member are
charts of `L02`.

### `Q2-E1-A1-B3-D1-N3` — 9 leaves

First split the fixed linear divisor into its transverse and binary
positions.  On the binary locus use the same common-Jacobian gcd and
Hilbert--Burch splitting convention as above.

| ID | Description |
|---|---|
| `L00` | binary fixed line and zero normal cubic \(R\); |
| `L01` | nonbinary/transverse fixed line; |
| `L02` | binary \(\rho=0,\{0,0\}\); |
| `L03` | binary \(\rho=1,\{1,0\}\); |
| `L04` | binary \(\rho=2,\{2,0\}\); |
| `L05` | binary \(\rho=2,\{1,1\}\); |
| `L06` | binary \(\rho=3,\{2,1\}\); |
| `L07` | binary \(\rho=4,\{2,2\}\); |
| `L08` | binary dependent-Jacobian power fibre. |

Whether a ramification root is marked by \(h\), unmarked, doubled, or
distinct is a chart inside the corresponding \(\rho\)-leaf.  This rule
prevents the marked/unmarked contact analysis from changing the frozen
denominator.

### `Q2-E1-A1-B3-D3-N1` — 4 leaves

| ID | Description |
|---|---|
| `L01` | nodal cubic, fixed line transverse to the minimal pencil; |
| `L02` | nodal cubic, fixed line in the minimal pencil; |
| `L03` | cuspidal cubic, fixed line transverse to the minimal pencil; |
| `L04` | cuspidal cubic, fixed line in the minimal pencil. |

Marked-point orbits—including cusp, flex, general cuspidal point, and the
nodal marked-point modulus—are charts inside `L02` or `L04`.

### `Q2-E2-A2-B1-D1-N1` — 8 leaves

| ID | Description |
|---|---|
| `L01` | some prime component of the fixed quadratic divisor is nonvertical; |
| `L02` | all vertical, with \(h=\ell^2,\ p=\ell m\); |
| `L03` | all vertical, with \(h=\ell_1\ell_2,\ p=\ell_1m_1,\ q=\ell_2m_2\); |
| `L04` | \(p=h\) and the normal cubic component is zero; |
| `L05` | \(p=h\), pencil \(\langle x^2,yz\rangle\), mixed companion \(xq\); |
| `L06` | \(p=h\), pencil \(\langle x^2,yz\rangle\), triple companion \(x^3\); |
| `L07` | \(p=h\), pencil \(\langle x^2,y^2+xz\rangle\), mixed companion \(xq\); |
| `L08` | \(p=h\), pencil \(\langle x^2,y^2+xz\rangle\), triple companion \(x^3\). |

The canonical-pencil theorem and pencil shear make these companion orbits
exhaustive.

### `Q2-E2-A1-B2-D1-N2` — 9 leaves

| ID | Description |
|---|---|
| `L00` | binary fixed quadratic and zero normal cubic \(R\); |
| `L01` | nonbinary fixed quadratic divisor; |
| `L02` | binary \(\rho=0,\{0,0\}\); |
| `L03` | binary \(\rho=1,\{1,0\}\); |
| `L04` | binary \(\rho=2,\{2,0\}\); |
| `L05` | binary \(\rho=2,\{1,1\}\); |
| `L06` | binary \(\rho=3,\{2,1\}\); |
| `L07` | binary \(\rho=4,\{2,2\}\); |
| `L08` | binary dependent-Jacobian power fibre. |

The fifteen previously named \(\rho=2,\{1,1\}\) incidence pieces and the
three \(\rho=2,\{2,0\}\) pieces are charts of `L05` and `L04`,
respectively.  Their count can never again be reported as progress against
the global denominator.

### `Q2-E2-A1-B2-D2-N1` — 7 leaves

The parabolic stabilizer of the minimal linear pencil has seven fixed-conic
normal forms:

| ID | Fixed divisor |
|---|---|
| `L01` | binary \(p^2\); |
| `L02` | binary \(pq\); |
| `L03` | \(r^2\); |
| `L04` | \(r^2+p^2\); |
| `L05` | \(r^2+pq\); |
| `L06` | \(pr\); |
| `L07` | \(pr+q^2\). |

Tangent-field Jordan types and zero patterns are charts inside these
leaves.

### `Q2-E3-A1-B1-D1-N1` — 2 leaves

| ID | Description |
|---|---|
| `L01` | binary fixed cubic \(h\in\mathbb C[p,q]\); |
| `L02` | nonbinary fixed cubic. |

The squarefree/double/triple-root orbit tree in `L01` and the two residual
double-factor orbits in `L02` are frozen chart atlases, not new leaves.

## 5. Candidate count

\[
\begin{array}{c|rrrrrrrrrrrrrr}
\text{row}&Q1&01&02&03&04&05&06&07&08&09&10&11&12&13\\ \hline
\text{leaves}&7&2&3&2&8&3&2&2&9&4&8&9&7&2
\end{array}
\]
and the sum is \(68\).

The blinded derivation must either reproduce these invariants or identify
the first discrepancy.  Until then, this manifest is not the frozen F1
artifact.

This document was prepared with AI assistance.  It is not peer reviewed.
