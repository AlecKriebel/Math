# Frozen quartic taxonomy, version 1

**Freeze candidate recorded (UTC):** 2026-07-25T20:08:55Z.
**Content replay passed (UTC):** 2026-07-25T20:24:07Z.

**Status:** frozen as version one.  The mandatory hashes are recorded in
`FROZEN_SHA256_v1.txt`, and `FREEZE_CERTIFICATE_v1.md` records the final
verifier pass.  Any content change requires a new freeze version.

## 1. Object being partitioned

Let \(\Phi\) be an exact-degree-four Keller map over \(\mathbb C\), and
choose a source point \(x_0\).  Replace \(\Phi(x)\) by
\(\Phi(x+x_0)-\Phi(x_0)\), put \(L=J\Phi(x_0)\), and postcompose by
\(L^{-1}\).  Since the Keller determinant is nonzero, \(L\) is invertible.
The normalized map has constant term zero, linear part \(X\), and determinant
\[
(\det L)^{-1}\det J\Phi=1.
\]
An invertible target change cannot kill its leading term.  Thus every
quartic Keller map can be normalized to
\[
F=X+H_2+H_3+H_4,
\tag{1}
\]
where \(H_i\) is homogeneous of degree \(i\) and \(H_4\ne0\).  Let
\(\mathcal K_4\) denote the coefficient space of all maps (1) satisfying
\(\det JF\in\mathbb C^\times\).

The degree-nine part of the determinant identity is
\[
\det JH_4=0.
\tag{2}
\]
The frozen leaves below partition \(\mathcal K_4\) by intrinsic invariants of
\(H_4\).  They do not claim that the quotient by linear equivalence is
finite.  Each leaf contains all lower terms \(H_2,H_3\), all continuous
moduli, and every internal degeneration that preserves its frozen
invariants.

This choice is deliberate.  The earlier 68-bucket proposal was neither
disjoint nor independently certified and is not part of this freeze.

## 2. Canonical pencil principle

Equation (2) gives \(\operatorname{rank}JH_4\le2\).  In characteristic zero,
rank zero would make every positive-degree homogeneous component constant,
and hence zero, contrary to \(H_4\ne0\).

If \(\operatorname{rank}JH_4=1\), the affine image closure is an irreducible
one-dimensional cone.  Because all three target coordinates have the same
quartic weight,
\[
H_4(\lambda x)=\lambda^4H_4(x),
\]
so its projectivization is a zero-dimensional irreducible variety, hence one
point.  The cone is therefore a target line, and
\[
H_4=a h
\]
for a constant nonzero target vector \(a\) and a quartic form \(h\).  This is
the rank-one leaf `Q1`.

Assume \(\operatorname{rank}JH_4=2\).  Extract the component gcd:
\[
h=\gcd(H_{4,1},H_{4,2},H_{4,3}),\qquad
e=\deg h,\qquad G=H_4/h.
\]
Let
\[
K_G=\mathbb C(G_i/G_j:G_j\ne0)
  \subset M=\mathbb C(\mathbb P^2),
\]
and let \(E_G\) be the relative algebraic closure of \(K_G\) in \(M\).
The extension \(E_G/K_G\) is finite because \(M/K_G\) is finitely generated.
The field \(E_G\) is the function field of a curve \(D\) dominated rationally
by \(\mathbb P^2\).  Restriction to a general source line gives a dominant
rational map \(\mathbb P^1\dashrightarrow D\), so \(D\) is unirational and
hence rational over \(\mathbb C\).  Consequently
\[
E_G=\mathbb C(p/q),
\]
where \(p,q\) are coprime homogeneous forms of a common degree \(a\).

Let \(C\subset\mathbb P^2\) be the reduced projective image of \(G\), of
degree \(\delta\).  The inclusion \(K_G\subset E_G\) induces a finite map
\[
\beta:\mathbb P^1_{E_G}\longrightarrow\widetilde C
\]
of degree \(\nu=[E_G:K_G]\).  Composing with the normalization map to
\(C\subset\mathbb P^2\) pulls a line back to a divisor of degree
\(b=\delta\nu\).  It is represented by a basepoint-free binary triple \(A\)
of degree \(b\), and projectively \([G]=[A(p,q)]\).

This projective factorization is polynomial.  The triple \(G\) is primitive
by gcd extraction.  The substituted triple \(A(p,q)\) is also primitive:
an irreducible source divisor common to all its components would either
divide both \(p,q\), or make \([p:q]\) a common projective zero of \(A\).
Both are impossible.  Two primitive triples over the UFD
\(\mathbb C[x,y,z]\) defining the same projective rational map differ by a
unit.  Absorbing that nonzero scalar into \(A\) gives the exact factorization
\[
G=A(p,q),
\]
and degree comparison gives
\[
\nu=[E_G:K_G],\qquad
e+ab=4,\qquad b=\delta\nu.
\tag{3}
\]

The relative-closure definition makes the tuple
\[
(\operatorname{rank}JH_4,e,a,b,\delta,\nu)
\tag{4}
\]
canonical.  For any other polynomial-pencil presentation \(r/s\), one has
\(\mathbb C(r/s)\subset E_G\).  Hence \(r/s=R(p/q)\) for a rational map
\(R:\mathbb P^1\to\mathbb P^1\), and the presentation degree is
\((\deg R)a\).  Equality occurs only for a Möbius change of \(p/q\).

This proves both uniqueness and the least-degree property needed for
disjoint routing.

## 3. Frozen denominator

The one rank-one leaf and thirteen rank-two leaves are:

| Frozen ID | rank | \(e\) | \(a\) | \(b\) | \(\delta\) | \(\nu\) | inclusive geometric description | current status |
|---|---:|---:|---:|---:|---:|---:|---|---|
| `Q1` | 1 | -- | -- | -- | -- | -- | \(H_4=a h\), all ternary quartics \(h\) | open |
| `Q2-E0-A4-B1-D1-N1` | 2 | 0 | 4 | 1 | 1 | 1 | primitive quartic line pencil | open |
| `Q2-E0-A2-B2-D1-N2` | 2 | 0 | 2 | 2 | 1 | 2 | quadratic pencil, line double cover | excluded-audited |
| `Q2-E0-A2-B2-D2-N1` | 2 | 0 | 2 | 2 | 2 | 1 | quadratic pencil, conic embedding | excluded-audited |
| `Q2-E0-A1-B4-D1-N4` | 2 | 0 | 1 | 4 | 1 | 4 | binary quartic line cover | open |
| `Q2-E0-A1-B4-D2-N2` | 2 | 0 | 1 | 4 | 2 | 2 | conic double cover | excluded-audited |
| `Q2-E0-A1-B4-D4-N1` | 2 | 0 | 1 | 4 | 4 | 1 | birational rational plane quartic | open |
| `Q2-E1-A3-B1-D1-N1` | 2 | 1 | 3 | 1 | 1 | 1 | fixed line, primitive cubic pencil | open |
| `Q2-E1-A1-B3-D1-N3` | 2 | 1 | 1 | 3 | 1 | 3 | fixed line, line triple cover | open |
| `Q2-E1-A1-B3-D3-N1` | 2 | 1 | 1 | 3 | 3 | 1 | fixed line, rational plane cubic | excluded-audited |
| `Q2-E2-A2-B1-D1-N1` | 2 | 2 | 2 | 1 | 1 | 1 | fixed conic, primitive quadratic pencil | excluded-audited |
| `Q2-E2-A1-B2-D1-N2` | 2 | 2 | 1 | 2 | 1 | 2 | fixed conic, line double cover | open |
| `Q2-E2-A1-B2-D2-N1` | 2 | 2 | 1 | 2 | 2 | 1 | fixed conic, conic embedding | excluded-audited |
| `Q2-E3-A1-B1-D1-N1` | 2 | 3 | 1 | 1 | 1 | 1 | fixed cubic, linear pencil | excluded-audited |

Thus the frozen denominator is
\[
\boxed{14\text{ disjoint inclusive leaves}},
\]
with current progress reported only as
\[
\boxed{7/14\text{ leaves excluded and audited}}.
\]
An internal calculation does not change this denominator.

## 4. Completeness

For rank two, solving (3) gives
\[
\begin{array}{c|c}
e&(a,b)\\ \hline
0&(4,1),(2,2),(1,4)\\
1&(3,1),(1,3)\\
2&(2,1),(1,2)\\
3&(1,1).
\end{array}
\]
Factoring \(b=\delta\nu\) gives respectively
\[
(1,1),\quad(1,2),(2,1),\quad(1,3),(3,1),\quad
(1,4),(2,2),(4,1).
\]
Substitution produces exactly the thirteen rank-two tuples in the table.
The canonical pencil principle proves that the same \(H_4\) cannot receive
two tuples.  Rank one is `Q1`, and rank zero is \(H_4=0\), outside exact
degree four.  Hence every element of \(\mathcal K_4\) lies in exactly one
frozen leaf.

## 5. Frozen coefficient-pivot partition

Write the degree-four monomials in this fixed order:
\[
\begin{split}
&x^4,x^3y,x^3z,x^2y^2,x^2yz,x^2z^2,xy^3,xy^2z,xyz^2,xz^3,\\
&y^4,y^3z,y^2z^2,yz^3,z^4.
\end{split}
\tag{5}
\]
Order the 45 coefficients of \(H_4\) first by target component
\(H_{4,1},H_{4,2},H_{4,3}\), then by (5), and call them
\(c_0,\ldots,c_{44}\).

For every frozen leaf \(R\), define its stable pivot strata by
\[
R/\mathrm C_i
=R\cap\{c_0=\cdots=c_{i-1}=0,\ c_i\ne0\},
\qquad 0\le i\le44.
\tag{6}
\]
Empty intersections are allowed.  These are disjoint locally closed pieces,
not a Zariski-open coordinate atlas.  The 45 pieces cover the leaf because
\(H_4\ne0\).  A proof may use a different local normal form, but it must give
a division-free calculation or a coverage map back to (6).  Vanishing of a
computational pivot never creates a new frozen leaf.

## 6. Boundary routing

Every mathematical specialization obeys exactly one ordered routing rule:

1. If \(H_4=0\), the map has total degree at most three and leaves
   \(\mathcal K_4\).
2. Otherwise, if \(\operatorname{rank}JH_4=1\), route to `Q1`.
3. Otherwise the rank is two.  Recompute the canonical tuple (4) after exact
   gcd extraction and relative closure, and route to its unique row.  If the
   tuple is unchanged, the point remains in the same leaf.  This includes
   every factorization, singularity, ramification, contact, Hilbert--Burch,
   marked-point, base-scheme, and stabilizer degeneration preserving the
   tuple.
There is no operation that appends a fifteenth leaf.  A newly discovered
computational subtype is a pivot stratum or subvariety inside its inclusive
row.

Separately, if a local normal-form proof supplies neither a division-free
argument nor coverage by the 45 pivot strata, that is a fail-closed audit
condition: the proof is incomplete and quartic work halts.  It is not a
fifth kind of specialization.

## 7. Scope

This freeze certifies a complete case denominator, not any exclusion.  The
seven status labels summarize separately audited work and are not evidence
for taxonomy completeness.  Continuous moduli are retained inside the
inclusive leaves and must be handled uniformly or by exhaustive internal
strata before a row can be called excluded.

The Markdown table and the machine-readable manifest were compared
independently during the hostile replay.  The verifier checks their stable
row IDs, tuples, statuses, exact monomial order, finite arithmetic, and
mandatory hashes; it does not prove the geometric canonicity argument above.

The taxonomy and proof were developed with substantial AI assistance.  This
is not peer review.
