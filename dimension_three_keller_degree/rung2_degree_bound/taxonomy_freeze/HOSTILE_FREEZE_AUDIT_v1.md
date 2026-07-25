# Hostile audit of `FROZEN_TAXONOMY_v1`

**Audit date:** 2026-07-25 (America/Los_Angeles).

**Files inspected:** only `FROZEN_TAXONOMY_v1.md`,
`frozen_manifest_v1.json`, `verify_frozen_manifest_v1.py`,
`blind_independent/BLIND_TAXONOMY.md`, and `RECONCILIATION.md`.
No exclusion proof was inspected.

## 1. Release verdict

\[
\boxed{\textbf{FAIL AS A RELEASE ARTIFACT; CORE TAXONOMY MATHEMATICS PASSES.}}
\]

The mathematical core survived the hostile replay:

* the normalization \(F=X+H_2+H_3+H_4\) is valid;
* the rank-one classification is complete;
* the relative-algebraic-closure field is rational;
* it gives an actual polynomial factorization \(G=A(p,q)\), not merely a
  rational or projective factorization;
* the relative-closure pencil is unique and least-degree;
* the fourteen inclusive leading rows are exhaustive and disjoint; and
* the 45 coefficient pivot pieces per row form a fixed disjoint complete
  set-theoretic cover of every nonzero \(H_4\).

The release nevertheless fails in its present form for exact, repairable
reasons:

1. `verify_frozen_manifest_v1.py` calls itself fail-closed but silently skips
   checksum verification when the checksum file is absent.
2. The verifier prints that it has checked "canonical" and "exhaustive"
   mathematics although it checks only finite manifest arithmetic and,
   optionally, file hashes.
3. It does not check that each stable row ID encodes its attached tuple, or
   that the monomial strings are the actual fixed list rather than merely
   fifteen distinct strings.
4. The frozen Markdown asserts the two hardest factorization steps without
   recording their short proofs.
5. Section 6 says every specialization obeys "exactly one" of five rules, but
   rule 5 is a meta-level proof-coverage failure, not a mutually exclusive
   specialization case.
6. The objects in (6) are disjoint locally closed pivot strata, not a
   Zariski-open atlas. The computational meaning is valid, but the terminology
   should be made exact.

After the required corrections in Section 9, the mathematical freeze can
pass. The seven `excluded-audited` statuses remain outside this audit.

## 2. Scorecard

| Claim | Result | Hostile conclusion |
|---|---|---|
| Normalize every quartic Keller map to \(X+H_2+H_3+H_4\) | **PASS** | Keller invertibility makes the linear normalization legitimate |
| Rank-zero handling | **PASS** | Nonzero exact quartic excludes rank zero in characteristic zero |
| Rank-one form \(H_4=a h\) | **PASS** | A one-dimensional image cone for equal weights is a line |
| Rank-two projective image is a rational curve | **PASS** | It is dominated by \(\mathbb P^2\), and a general line dominates it |
| Relative closure \(E_G\) is rational | **PASS** | The corresponding curve is unirational over \(\mathbb C\) |
| Polynomial factorization \(G=A(p,q)\) | **PASS** | Basepoint-freeness and UFD primitivity remove the rational scalar |
| Least-degree and uniqueness | **PASS** | Any other pencil degree is \(k a\) |
| Thirteen rank-two tuples | **PASS** | Direct enumeration agrees between Markdown and JSON |
| Fourteen-row coverage/disjointness | **PASS** | Rank plus the canonical tuple is single-valued |
| 45 pieces per row cover | **PASS, terminology correction** | Complete disjoint locally closed pivot partition, not an open atlas |
| Finite moduli/orbit classification | **NOT CLAIMED, correctly** | Continuous moduli remain inside leaves |
| JSON arithmetic | **PASS** | 14 unique IDs, 13 tuples, 45 IDs, 630 intersections, 7/7 statuses |
| Verification program | **FAIL** | Optional checksums and semantic overclaim |
| Exclusion statuses | **NOT AUDITED** | No conclusion |

## 3. Hostile replay of the normalization

Start with an arbitrary exact-degree-four Keller map \(\Phi\). Choose a source
base point \(x_0\), replace \(\Phi(x)\) by
\[
                  \Phi(x+x_0)-\Phi(x_0),
\]
and let \(L=J\Phi(x_0)\). Since \(\det J\Phi\in\mathbb C^\times\),
\(L\in\mathrm{GL}_3(\mathbb C)\). Postcompose by \(L^{-1}\). The result has
constant term zero and linear part \(X\), hence uniquely decomposes as
\[
                         F=X+H_2+H_3+H_4.
\]
An invertible target change cannot kill the nonzero leading term, so
\(H_4\ne0\). In this normalization \(\det JF(0)=1\), so the constant Keller
determinant is in fact \(1\).

**Counterexample attempted:** choose a map with singular linear part.
This is impossible for a Keller map because its Jacobian determinant is
nonzero at every point.

**Required textual clarification:** Section 1 should record
\(L=J\Phi(x_0)\), postcomposition by \(L^{-1}\), and the resulting determinant
normalization to \(1\). The existing statement is correct but compressed.

## 4. Hostile replay of the rank split

The degree-nine determinant term is \(\det JH_4\), so
\(\operatorname{rank}JH_4\le2\). In characteristic zero, rank zero makes every
component constant; positive homogeneity then makes \(H_4=0\), outside exact
degree four.

Suppose the rank is one. By the Jacobian criterion, the affine image closure
is an irreducible one-dimensional cone. Homogeneity gives the **standard**
scalar action
\[
                         H_4(\lambda x)=\lambda^4H_4(x)
\]
on all target coordinates with the same weight. The projectivization of an
irreducible one-dimensional cone has dimension zero and is one point.
Therefore the cone is a target line and
\[
                         H_4=a h
\]
for a nonzero constant target vector \(a\) and one quartic \(h\).
Conversely such a triple has rank one.

**Counterexample attempted:** use a nonlinear monomial curve such as
\((t^2,t^3)\). It is a cone only for unequal target weights. Equal quartic
homogeneity imposes standard diagonal scaling and rules it out.

Thus `Q1` is exactly the rank-one locus, including all smooth, singular,
reducible, and nonreduced ternary quartics \(h\).

**Required textual correction:** add this cone-line proof after the rank-one
assertion. Euler's identity alone does not display why no nonlinear cone curve
survives.

## 5. Hostile replay of the canonical pencil theorem

Let \(H_4\) have rank two. Write
\[
 h=\gcd(H_{4,1},H_{4,2},H_{4,3}),\qquad G=H_4/h,
\]
and \(m=\deg G=4-e\). The triple \(G\) is primitive. Its projective ratios
define a one-dimensional field
\[
 K=K_G\subset M=\mathbb C(\mathbb P^2).
\]

### 5.1 Finiteness and rationality of the relative closure

Let \(E\) be the relative algebraic closure of \(K\) in \(M\). Since
\(M/K\) is finitely generated, its algebraic subextension \(E/K\) is finite.
The field \(E\) is the function field of a curve \(D\) dominated rationally
by \(\mathbb P^2\).

A general line in \(\mathbb P^2\) is not contained in a fiber of the
nonconstant map to \(D\), so restriction gives a dominant rational map
\[
                         \mathbb P^1\dashrightarrow D.
\]
Thus \(D\) is unirational. Over \(\mathbb C\), a unirational curve is
rational, so
\[
                         E=\mathbb C(t).
\]
Represent \(t=p/q\) by coprime homogeneous forms of a common degree \(a\).

**Counterexample attempted:** make \(E\) the function field of a
positive-genus curve embedded in \(\mathbb C(\mathbb P^2)\). Such a curve
would be dominated by a general source line, contradicting
Riemann--Hurwitz/unirationality.

### 5.2 From a field factorization to a polynomial factorization

Let \(C\subset\mathbb P^2\) be the reduced projective image of \(G\), of
degree \(\delta\). The inclusion \(K\subset E\) induces a finite morphism
\[
                    \beta:\mathbb P^1_E\longrightarrow\widetilde C
\]
of degree
\[
                         \nu=[E:K].
\]
The normalization map \(\widetilde C\to C\subset\mathbb P^2\), composed with
\(\beta\), pulls a line back to a divisor of degree
\[
                         b=\delta\nu.
\]
It is therefore represented by a basepoint-free binary triple \(A\) of
degree \(b\). Projectively,
\[
                         [G]=[A(p,q)].
\]

This projective equality is enough only after the following primitivity
check. If a source prime divided all components of \(A(p,q)\), then over the
prime's fraction field either both \(p,q\) would vanish or \([p:q]\) would be
a common projective zero of \(A\). The first contradicts
\(\gcd(p,q)=1\); the second contradicts basepoint-freeness. Hence
\(A(p,q)\) is primitive.

Two primitive polynomial triples over the UFD
\(\mathbb C[x,y,z]\) defining the same projective rational map differ by a
unit. Consequently, after absorbing a nonzero scalar into \(A\),
\[
                         G=A(p,q)
\]
as polynomial triples, and comparison of degrees gives
\[
                         4-e=ab.
\]

**Counterexample attempted:** introduce a nonconstant rational proportionality
factor between \(G\) and \(A(p,q)\). Any numerator or denominator prime would
be a common component factor of one of the primitive triples. No such factor
survives.

**Required textual correction:** Section 2 of the frozen Markdown must include
the rationality and primitivity arguments. They are the substantive bridge
from algebraic dependence to the displayed polynomial factorization.

### 5.3 Canonicity and least degree

The field \(E\) is unique by definition. Any two generators of
\(\mathbb C(t)\) differ by a Möbius transformation, so primitive homogeneous
representatives give the same pencil \(\langle p,q\rangle\) and the same
degree \(a\).

For any other polynomial presentation \(u=r/s\), the ratios of \(G\) lie in
\(\mathbb C(u)\), so
\[
                         K\subset\mathbb C(u)\subset E.
\]
Write \(u=R(t)\), where \(R:\mathbb P^1\to\mathbb P^1\) has degree \(k\).
Represent \(R\) by a coprime binary pair \((P,Q)\) of degree \(k\). Then
\[
                         [r:s]=[P(p,q):Q(p,q)].
\]
Both pairs are primitive, so equality is up to a constant and
\[
                         \deg r=\deg s=ka.
\]
Thus the relative-closure pencil is genuinely least-degree, and equality
occurs only for \(k=1\), a Möbius change.

**Stress test 1.**
\[
                         G=(x^4,y^4,0)
\]
has the misleading presentation \(r=x^4,s=y^4\) of degree four. Its ratio
field is \(K=\mathbb C((x/y)^4)\), whose relative closure in
\(\mathbb C(\mathbb P^2)\) is \(E=\mathbb C(x/y)\). The canonical row is
`E0-A1-B4-D1-N4`, not `E0-A4-B1-D1-N1`.

**Stress test 2.**
\[
                         G=(x^4,x^2y^2,y^4)
\]
has image a conic and
\[
 K=\mathbb C((x/y)^2)\subset E=\mathbb C(x/y)
\]
of degree two. It lands in `E0-A1-B4-D2-N2`, as frozen.

These examples confirm that the relative-closure clause, rather than a
presentation chosen by inspection, is essential for disjoint routing.

## 6. Completeness and disjointness of the fourteen rows

For rank two, \(e\le3\), \(a,b\ge1\), and
\[
                         e+ab=4,\qquad b=\delta\nu.
\]
The solutions are:

* \(e=0\): \((a,b)=(4,1),(2,2),(1,4)\), giving \(1+2+3=6\) rows;
* \(e=1\): \((3,1),(1,3)\), giving \(1+2=3\) rows;
* \(e=2\): \((2,1),(1,2)\), giving \(1+2=3\) rows;
* \(e=3\): \((1,1)\), giving one row.

This gives thirteen. The JSON contains exactly this set, each stable ID
encodes the attached tuple correctly, and `Q1` is the fourteenth row.

No object can occur in two rows:

* rank distinguishes `Q1` from rank two;
* the exact component gcd fixes \(e\);
* the unique relative-closure field fixes the pencil and \(a\);
* the degree equation fixes \(b\);
* the projective image fixes \(\delta\); and
* \([E:K]\) fixes \(\nu\).

No counterexample survives these invariants. Internal singularity,
factorization, ramification, base-scheme, contact, or moduli changes either
leave the tuple fixed or force recomputation into one of the same thirteen
rows.

**Mathematical result:** the frozen fourteen-row denominator is exhaustive,
disjoint, and canonical as an inclusive **leading-invariant** partition.

## 7. Hostile replay of the 45 coefficient pieces

There are exactly fifteen ternary monomials of degree four and three target
components, hence 45 fixed coefficients. For a nonzero coefficient vector
\[
                         (c_0,\ldots,c_{44}),
\]
there is a unique least index \(i\) with \(c_i\ne0\). Therefore
\[
 \{H_4\ne0\}
 =\bigsqcup_{i=0}^{44}
 \{c_0=\cdots=c_{i-1}=0,\ c_i\ne0\}.                    \tag{A1}
\]
Intersecting (A1) with any frozen row preserves disjointness and coverage.
Empty intersections cause no problem. Hence the claimed \(14\cdot45=630\)
row/pivot intersections, including empty ones, are correct.

**Counterexample attempted:** find a nonzero quartic with no first nonzero
coefficient. This is impossible in a finite ordered coefficient vector. The
only missed point is \(H_4=0\), explicitly outside \(\mathcal K_4\).

These pieces are fixed and complete even though:

* they depend on the chosen source/target coordinates and coefficient order;
* the same equivalence orbit may meet many pieces;
* they contain continuous moduli;
* they do not classify singularity, ramification, or stabilizer type; and
* they do not automatically prove that a separate normal-form atlas covers a
  row.

The last point is handled correctly by the required coverage map or
division-free fallback.

**Terminology correction:** each set in (A1) is locally closed, not generally
open in the leaf. Call them the "45 fixed disjoint locally closed pivot
strata" or explicitly define "atlas" to mean a computational set-theoretic
partition, not a Zariski-open coordinate atlas.

Subject to that terminology, the 45-piece claim **passes** and does not
pretend to classify moduli.

## 8. Static audit of the JSON and verifier

An independent read of the authorized JSON verifies:

* 14 rows and 14 unique IDs;
* the exact set of 13 rank-two tuples;
* correct ID-to-tuple encoding for every rank-two row;
* 7 `open` and 7 `excluded-audited` status strings;
* the 45 IDs `C00` through `C44`; and
* \(14\cdot45=630\) declared intersections.

The verification program correctly checks most arithmetic, but it has the
following release-blocking defects.

### V1. The checksum is optional

The code says:

```python
if CHECKSUMS.exists():
    ...
```

If the checksum file is absent, empty, or omits a critical frozen artifact,
the program still prints `PASS`. This contradicts both "fail-closed" and the
freeze's pending-checksum status.

**Required correction:** fail if the checksum file is absent; require an
exact nonempty set of expected frozen filenames; reject missing, duplicate,
unexpected, or path-traversing entries; then verify every digest.

### V2. Stable IDs are not checked against tuples

The verifier compares the **set** of tuples with the expected set. Swapping
the tuples attached to two stable IDs would still pass.

**Required correction:** parse each ID with the exact pattern
`Q2-Ee-Aa-Bb-Ddelta-Nnu` and compare the parsed integers to that row's tuple.
Also require `Q1` to have `tuple: null` and every other row to have rank two.

### V3. The monomial content is not checked

The program verifies only that there are fifteen distinct monomial strings.
Fifteen arbitrary strings would pass.

**Required correction:** compare the JSON list to the exact ordered list in
equation (5), or generate all exponent triples summing to four and verify the
declared order separately.

### V4. The success message overclaims semantics

The final line says:

```text
PASS: 14 canonical rows, 13 exhaustive rank-two tuples, ...
```

The program does not and cannot prove relative-closure rationality,
polynomial factorization, rank-one completeness, or row canonicity.

**Required correction:** print something such as:

```text
PASS: frozen manifest schema/arithmetic and required checksums
```

The mathematical certificate must cite the proof audit separately.

### V5. The Markdown/manifest relation is not machine-checked

Hashes establish immutability, not semantic agreement. The current Markdown
and JSON agree on inspection, but the program does not compare the table and
scope claims.

**Required correction or explicit limitation:** either add a small
machine-readable source of truth from which the Markdown table is rendered,
or state that Markdown/JSON semantic agreement is a human-audited item in the
freeze certificate.

## 9. Exact required corrections before a pass

The release should remain failed until all of the following are made.

1. **Expand Section 1** with the explicit \(L^{-1}\) normalization and note
   that the normalized determinant is \(1\).
2. **Expand Section 2** with the rank-one cone-line proof.
3. **Expand Section 2** with:
   * finiteness and rationality of \(E_G/K_G\);
   * construction of the finite map \(\mathbb P^1_E\to\widetilde C\);
   * the degree calculation \(b=\delta\nu\);
   * primitivity of \(A(p,q)\); and
   * the UFD argument turning projective equality into
     \(G=A(p,q)\).
4. **Rename or define the 45 pieces** as a disjoint locally closed pivot
   partition, rather than an open atlas.
5. **Separate Section 6 rule 5** from rules 1--4. Rules 1--4 route
   mathematical specializations; rule 5 is a fail-closed audit condition and
   is not mutually exclusive with them.
6. **Repair the verifier** according to V1--V4.
7. **Record V5 explicitly** as either a generated-source check or a human
   certificate check.
8. After all content is final, **generate mandatory checksums**, run the
   repaired verifier, change the manifest status from
   `pending_hostile_replay`, and record the separate freeze certificate.

No new mathematical leaf is required.

## 10. What a corrected pass would and would not certify

After the corrections above, a pass would certify exactly this:

* every normalized exact-degree-four Keller map over \(\mathbb C\) has a
  nonzero \(H_4\) in exactly one of the fourteen inclusive leading leaves;
* the rank-two tuple is canonical via the relative algebraic closure of the
  projective ratio field;
* every leaf includes all lower terms and all continuous/internal
  degenerations preserving the tuple;
* every nonzero \(H_4\) lies in exactly one of 45 fixed coefficient pivot
  strata, giving 630 row/pivot intersections when empty intersections are
  counted; and
* future computations may subdivide a leaf internally but may not report
  those subdivisions as progress against a larger global denominator.

It would **not** certify:

* that any of the fourteen leaves is nonempty among non-linear Keller maps;
* any of the seven exclusion claims or their audits;
* that the fourteen leaves are source/target equivalence orbits;
* a finite classification of moduli, singularities, ramification, contacts,
  base schemes, or stabilizers;
* that the 45 pivot strata are Zariski-open coordinate charts;
* that a proof using other normal forms has supplied the required coverage
  maps; or
* any Jacobian-conjecture or novelty result.

The final mathematical denominator should remain
\[
\boxed{14\text{ canonical inclusive leading leaves}},
\]
with the 45-piece coefficient partition understood only as a fixed
fail-closed computational coverage device.
