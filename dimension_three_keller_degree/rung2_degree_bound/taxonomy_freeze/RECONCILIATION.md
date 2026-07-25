# Reconciliation of the candidate quartic taxonomy with the blind derivation

**Date:** 2026-07-25 (America/Los_Angeles).

**Scope of audit.** This reconciliation uses only:

* `CANDIDATE_GLOBAL_TAXONOMY.md`;
* `CANDIDATE_INCIDENCE_MANIFEST.md`;
* `candidate_manifest.json`; and
* the prior blind derivation in `blind_independent/`.

No quartic exclusion proof was inspected. Accordingly, the seven
`excluded-audited` statuses are neither affirmed nor disputed here.

## 1. Verdict

There are three different claims that must not be conflated.

1. **Leading numerical coverage.** The candidate's rank-one row plus thirteen
   rank-two tuples agree exactly with the blind derivation. Under the canonical
   relative-algebraic-closure principle stated in Section 2, these fourteen
   leading rows are exhaustive, disjoint, and invariant under left-right
   linear equivalence.
2. **The proposed 68 incidence leaves.** The arithmetic is consistent:
   the Markdown counts and JSON counts both give fourteen row IDs and
   \(68\) leaves. The 68 predicates are nevertheless **not presently a
   certified stratification**. The ambient incidence space and equivalence
   are not defined, several predicates depend on undefined normal-form data,
   completeness assertions are cited rather than proved, and at least one
   pair of leaf descriptions overlaps literally.
3. **A finite orbit denominator.** No finite orbit denominator can be honest.
   Several leading rows already have positive-dimensional moduli under the
   coarser left-right action. A finite list can only be a coarse,
   convention-dependent list of computational buckets, not a list of
   geometric orbits.

Thus an honest finite freeze is currently possible at the level
\[
             \boxed{14\text{ canonical leading numerical rows}},
\]
but not at the level of the proposed 68 F1 incidence leaves. If "denominator"
means all source/target orbits, no finite denominator exists.

## 2. A stratification principle that makes the leading rows canonical

### 2.1 Equivalence

For this audit, the object at leading degree is a nonzero homogeneous quartic
triple
\[
 H=(H_0,H_1,H_2)\in
 \mathbb C[x_0,x_1,x_2]_4^{\oplus3},\qquad \det JH=0,
\]
under
\[
 H(x)\sim T H(S^{-1}x),\qquad
 S\in\mathrm{GL}_3(\mathbb C)_{\rm source},\quad
 T\in\mathrm{GL}_3(\mathbb C)_{\rm target}.             \tag{R1}
\]
If \(L=I\) is fixed first, conjugacy is a finer equivalence. The numerical
invariants below remain invariant, but orbit statements would become still
finer.

### 2.2 Canonical relative-closure principle

Assume \(\operatorname{rank}JH=2\). Let
\[
 h=\gcd(H_0,H_1,H_2),\qquad e=\deg h,\qquad G=H/h,
\]
so \(G\) is primitive of degree \(m=4-e\). Let
\[
 K=\mathbb C(G_i/G_j:\ G_j\ne0)\subset
 M=\mathbb C(\mathbb P^2).
\]
This is the function field of the projective image curve. Define
\[
 E=\operatorname{acl}_M(K),
                                                               \tag{R2}
\]
the relative algebraic closure of \(K\) in \(M\).

The **canonical pencil principle** is:

> The source pencil is the primitive homogeneous pencil
> \([p:q]:\mathbb P^2\dashrightarrow\mathbb P^1\) whose ratio generates the
> unique field \(E\).

This is stronger and safer than choosing an arbitrary presentation of least
degree. It also gives a precise meaning to the candidate phrase
"generate the relatively algebraically closed pencil field."

### 2.3 Existence and uniqueness

The field \(E/K\) is finite because \(M/K\) is finitely generated and
\(\operatorname{trdeg}_K M=1\). The curve with function field \(E\) is
dominated by \(\mathbb P^2\); restriction to a general line shows that it is
unirational, hence rational over \(\mathbb C\). Thus
\[
 E=\mathbb C(t)
\]
for some \(t=p/q\), with \(p,q\) coprime homogeneous forms of a common degree
\(a\).

Let \(C\) be the projective image of \(G\), of degree \(\delta\).
The inclusion \(K\subset E\) gives a finite map
\[
 \mathbb P^1_E\longrightarrow \widetilde C
\]
of degree
\[
                         \nu=[E:K].
\]
Composing with the normalization map
\(\widetilde C\to C\subset\mathbb P^2\) is represented by a basepoint-free
binary triple \(A\) of degree
\[
                         b=\delta\nu.                  \tag{R3}
\]
Projectively \(G\) and \(A(p,q)\) agree. Both triples are primitive: a source
prime dividing every \(A_i(p,q)\) would either divide both \(p,q\) or give a
base point of \(A\). Hence UFD primitivity upgrades projective agreement to
\[
                         G=cA(p,q),\qquad c\in\mathbb C^\times.
\]
Degree comparison gives
\[
                         m=ab,\qquad e+ab=4.            \tag{R4}
\]

The field \(E\) is unique. If \(t'\) is another generator, then
\[
 t'=\frac{\alpha t+\beta}{\gamma t+\delta}
\]
for an element of \(\mathrm{PGL}_2(\mathbb C)\). Primitive homogeneous
representatives are therefore
\[
 [p':q']=[\alpha p+\beta q:\gamma p+\delta q].
\]
Consequently the pencil \(\langle p,q\rangle\), its degree \(a\), and then
\(b,\delta,\nu\), are unique.

It is also genuinely least-degree. For any other polynomial pencil
factorization with \(u=r/s\), the projective ratio field satisfies
\[
                         K\subset\mathbb C(u)\subset E.
\]
Writing \(u=R(t)\) with \(\deg R=k\), primitive homogeneous representatives
and the same UFD argument give
\[
                         \deg r=\deg s=ka.
\]
Thus every presentation degree is a positive multiple of the canonical
degree \(a\). Equality forces \(k=1\), hence the same field and the same
pencil up to \(\mathrm{PGL}_2\).

This closes the nonuniqueness gap in the blind derivation **provided** the
candidate's relative-algebraic-closure clause means exactly (R2). If
"minimal pair" means only "choose some presentation having least degree,"
without (R2), uniqueness has not been proved.

### 2.4 Leading completeness and disjointness

Rank zero is \(H=0\), outside exact total degree four. Rank one is exactly
\(H=c f\) and gives `Q1`. For rank two, (R4) and (R3) force the thirteen
candidate tuples. Because \(e,E,a,C,\delta\), and \([E:K]\) are intrinsic,
each \(H\) has exactly one tuple. Hence the fourteen-row numerical leading
denominator is exhaustive and disjoint under (R1).

The statement in `CANDIDATE_GLOBAL_TAXONOMY.md` that the thirteen integer
solutions have "no duplication" is therefore correct only after this field
uniqueness argument. Integer enumeration by itself proves neither
presentation independence nor disjointness.

## 3. Row-by-row reconciliation

The IDs differ only by the blind prefix `Q4-R2-`; the thirteen numerical
tuples match one-for-one.

The last column below records geometry already present **inside** a candidate
row. Positive dimensions refer to generic quotients under the coarser action
(R1), so they are conclusive evidence that the row is not a finite orbit
list.

| Candidate row | Blind reconciliation | Geometry inside the row |
|---|---|---|
| `Q1` | Same rank-one/projective-point case | Ternary quartic \(h\) has generic quotient dimension \(6\), plus all singular/reducible/nonreduced strata |
| `E0-A4-B1-D1-N1` | Exact match | Primitive quartic pencils: generic dimension \(18\) |
| `E0-A2-B2-D1-N2` | Exact match | Coupled quadratic-pencil/outer-plane quotient: generic dimension \(2\) |
| `E0-A2-B2-D2-N1` | Exact match | Finite leading Kronecker--Segre pencil types |
| `E0-A1-B4-D1-N4` | Exact match | Degree-four Hurwitz quotient: generic dimension \(3\) |
| `E0-A1-B4-D2-N2` | Exact match | One leading conic/double-cover orbit |
| `E0-A1-B4-D4-N1` | Exact match | Rational plane quartics: generic dimension \(3\), with all delta-\(3\) singularity baskets |
| `E1-A3-B1-D1-N1` | Exact match | A line plus primitive cubic pencil: generic dimension \(10\) |
| `E1-A1-B3-D1-N3` | Exact match | Degree-three covers: generic dimensions \(1\) in the transverse case and \(2\) when the fixed line marks the pencil |
| `E1-A1-B3-D3-N1` | Exact match | Node/cusp and transverse/in-pencil give four coarse pieces; the in-pencil pieces retain marked-normalization moduli |
| `E2-A2-B1-D1-N1` | Exact match | A conic plus primitive conic pencil: generic dimension \(5\) |
| `E2-A1-B2-D1-N2` | Exact match | Coupled conic/point and outer-plane quotient: generic dimension \(1\) |
| `E2-A1-B2-D2-N1` | Exact match | Exactly seven leading conic/center-point orbits |
| `E3-A1-B1-D1-N1` | Exact match | A cubic plus a linear pencil: generic dimension \(3\) |

The candidate manifest is therefore compatible with the blind leading
taxonomy only if its leaves are understood as coarse incidence buckets.
They cannot be understood as orbits or as a complete equisingular
stratification.

## 4. Audit of the proposed 68 leaves

### 4.1 What is verified

The manifest and JSON are arithmetically consistent:

* fourteen distinct row IDs occur;
* the declared row leaf counts sum to \(68\); and
* every incidence row is attached to one of the fourteen correct leading
  numerical rows.

Several coarse splits also agree independently with the blind geometry:

* `Q2-E1-A1-B3-D3-N1` uses node/cusp and transverse/in-pencil, the correct
  four coarse predicates;
* `Q2-E2-A1-B2-D2-N1` lists the same seven conic/center-point types obtained
  blindly;
* `Q2-E3-A1-B1-D1-N1` uses the invariant binary/nonbinary dichotomy;
* rank drops and changes of \((e,a,b,\delta,\nu)\) are routed to the correct
  leading row.

These agreements do not certify the other incidence predicates or the
global number \(68\).

### 4.2 Exact discrepancy D1: the ambient incidence space is undefined

The leading taxonomy classifies \(H_4\). The 68-leaf manifest also uses:

* the projection of \(H_3\) modulo a target subspace;
* a "normal cubic" \(R\) or \(R_3\);
* a "complete degree-eight tangent";
* companion components; and
* sometimes lower relative-position parameters.

It never defines whether a point of the incidence space is
\((H_4,H_3)\), \((L,H_2,H_3,H_4)\), a solution of selected homogeneous
Jacobian equations, or a normal-form parameter tuple after earlier
eliminations. Without an ambient set \(\mathcal X\), the assertion
\[
                         \mathcal X=\bigsqcup_{i=1}^{68}\mathcal L_i
\]
has no definite meaning.

### 4.3 Exact discrepancy D2: no equivalence is stated for the leaves

The documents use target normal components, parabolic stabilizers, pencil
shears, swapping involutions, and canonical forms, but do not state a global
source/target equivalence. Consequently "canonical leaf" is undefined.

The first-nonzero-coordinate atlas is reproducible only after choosing a
normal form, coefficient order, and projectivization. It is not invariant
under (R1), and it does not descend canonically to an orbit quotient without
additional construction.

### 4.4 Exact discrepancy D3: several leaf predicates are not defined

The manifest does not define, within the authorized freeze artifacts:

* \(J(P,Q)\) in the three-variable setting;
* the gcd of the displayed Jacobian objects;
* the Hilbert--Burch splitting \(\{k_1,k_2\}\);
* "dependent Jacobians";
* the \(L^4/L^3\) power fibre;
* the tangent scalars \((a,b)\);
* "vertical," "horizontal," and "restriction rank";
* the normal cubic component and its gauge freedom; or
* the mixed/triple companion equivalence.

Some may be well-defined elsewhere, but a frozen taxonomy must either define
them or point to a frozen definition with a proof of presentation
independence. Counts alone cannot do this.

### 4.5 Exact discrepancy D4: a literal overlap

In row `Q2-E2-A2-B1-D1-N1`:

* `L02` says \(h=\ell^2,\ p=\ell m\);
* `L04`--`L08` separately cover \(p=h\).

As written, `L02` allows \(m=\ell\), so \(p=h\). For a concrete leading
datum, take
\[
 h=x^2,\qquad p=x^2,\qquad q=yz,\qquad
 H_4=(x^4,x^2yz,0).
\]
Here \(\gcd(p,q)=1\), the pencil
\(\langle x^2,yz\rangle\) is one of the manifest's own minimal canonical
types, \(\gcd(H_{4,i})=x^2\), and \(JH_4\) has generic rank two. If the normal
cubic is zero, the datum satisfies both `L02` (with
\(\ell=m=x\)) and `L04`.

No condition \(m\not\parallel\ell\), no priority rule, and no proof that the
intersection is empty is stated. Because the taxonomy is required to be
complete independently of exclusions, a later proof that this locus has no
Keller extension would not repair the logical overlap.

A minimal repair is to state that `L02` has \(p\not\parallel h\), then handle
all \(p=h\) cases exclusively in `L04`--`L08`.

### 4.6 Exact discrepancy D5: key exhaustiveness assertions are unsupported

The following routing/classification claims are necessary to obtain exactly
68 leaves, but they are assertions rather than proofs in the freeze
artifacts:

* the two canonical unique-double-line restriction types exhaust the relevant
  minimal conic pencils;
* two double-line members always and only cause the displayed minimality
  drop;
* the listed \(\rho\)/Hilbert--Burch pairs exhaust all nonzero normal cubics;
* dependent Jacobians are equivalent to the stated power-fibre case;
* the two tangent scalars exhaust the conic-double-cover tangent;
* the eight vertical quadratic-divisor companion cases are exhaustive; and
* every unlisted specialization remains inside a leaf rather than changing a
  hidden invariant.

Any of these statements may be true, but the proposed denominator cannot be
certified from the three candidate artifacts without their definitions and
proofs.

### 4.7 Exact discrepancy D6: moduli are demoted to charts by convention

The manifest explicitly makes the following into charts rather than leaves:

* ramification root partitions and collisions;
* rational-quartic singularity types;
* marked/unmarked contact data;
* a nodal marked-point modulus;
* factor and root trees of fixed divisors; and
* lower relative-position parameters.

The blind audit shows that many of these are genuine orbit or equisingularity
invariants. It is logically permissible to place them in one coarse leaf,
but then the number 68 is a chosen computational granularity, not a canonical
geometric denominator. A different author could merge the two rational
quartic gcd leaves, or split one by gcd degree, and obtain another equally
exhaustive finite bucket count.

The rule "anything undeclared is a chart" makes coverage easier by
definition, but it cannot prove that the declared predicates are the uniquely
correct structural invariants.

### 4.8 Exact discrepancy D7: least-degree presentation must be replaced by
the canonical field construction

The blind derivation deliberately left open uniqueness of a least-degree
pencil. The candidate global taxonomy contains the right possible cure—the
relative-algebraic-closure clause—but does not prove it or define the field
explicitly.

All routing by \((a,b,\nu)\) is canonical only after adopting (R2). If a proof
uses a normal-form presentation that is merely "minimal" in an informal
compositional sense, the same object could receive different presentation
labels. Section 2 supplies the necessary invariant definition and uniqueness
proof.

### 4.9 Exact discrepancy D8: the JSON certifies arithmetic only

`candidate_manifest.json` records row IDs, counts, and current statuses. It
does not record:

* the ambient object;
* equivalence;
* predicate definitions;
* routing maps;
* refinement relations;
* moduli warnings; or
* a version/hash for the mathematical predicates.

It verifies that \(7+2+3+\cdots+2=68\), not that 68 subsets form a
partition.

### 4.10 Exact discrepancy D9: exclusion status is orthogonal

The labels `excluded-audited` and `open` are not part of leading
completeness and were not audited here. A denominator intended to support
exclusions must be frozen before relying on those exclusions; an exclusion
cannot retroactively make overlapping or undefined leaves into a
stratification.

## 5. Can any finite denominator be certified?

### 5.1 Yes: the fourteen leading numerical rows

Under (R1)--(R2), the following finite invariant map is canonical:
\[
 H_4\longmapsto
 \begin{cases}
 \texttt{Q1},&\operatorname{rank}JH_4=1,\\
 (e,a,b,\delta,\nu),&\operatorname{rank}JH_4=2.
 \end{cases}
\]
Its fibers are exactly `Q1` plus the thirteen candidate rank-two rows. This
is the strongest finite denominator certified by the present reconciliation.
It is a numerical leading denominator, not an orbit denominator and not the
claimed F1 incidence denominator.

### 5.2 No: a finite orbit denominator

A finite orbit list is impossible even before lower Keller data are added.
For example:

* rank-one smooth quartics have a six-dimensional quotient;
* primitive quartic pencils have an eighteen-dimensional quotient;
* degree-four line covers have a three-dimensional Hurwitz quotient;
* rational plane quartics have a three-dimensional quotient; and
* several fixed-divisor/pencil rows retain positive-dimensional coupled
  moduli.

Fixing \(L=I\) replaces left-right equivalence by a finer action and cannot
remove this obstruction.

### 5.3 Not yet: the number 68

The 68 count could be frozen as a **project-management convention** after
formal repairs, but it cannot currently be certified as exhaustive,
disjoint, or canonical. To make it an honest coarse stratification one must:

1. define the ambient jet/incidence scheme and exactly which Keller identities
   it satisfies;
2. state the global equivalence and all residual stabilizer actions;
3. define every normal component, Jacobian gcd, splitting, tangent scalar,
   and companion invariant intrinsically;
4. use the canonical field \(E\) from (R2) for every minimal-pair routing;
5. rewrite all 68 leaves as mutually exclusive Boolean predicates, repairing
   the explicit `L02`/`L04`--`L08` overlap;
6. prove row-by-row coverage and every cross-row boundary route without using
   the exclusions that the denominator is meant to organize;
7. label every positive-dimensional leaf as a moduli bucket, not a finite
   orbit; and
8. store predicate versions and routing data in the machine-readable
   manifest, not only counts.

Until those steps are complete, the honest freeze statement is:
\[
\boxed{\text{14 canonical leading numerical rows; 68 candidate coarse
incidence buckets, not certified.}}
