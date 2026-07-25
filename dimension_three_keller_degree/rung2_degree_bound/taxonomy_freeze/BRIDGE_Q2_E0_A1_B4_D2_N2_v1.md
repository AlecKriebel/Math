# Post-freeze bridge for `Q2-E0-A1-B4-D2-N2`

**Recorded (UTC):** 2026-07-25T20:39:41Z.

**Verdict:** PASS.  Relative to `FROZEN_TAXONOMY_v1`, the inclusive row
`Q2-E0-A1-B4-D2-N2` is certified excluded.  This certificate promotes
exactly that row; it does not change the frozen denominator or any hashed
version-one artifact.

The resulting honest post-freeze numerator is
\[
\boxed{1/14\ \text{certified excluded},\qquad
       6/14\ \text{provisional},\qquad
       7/14\ \text{open}.}
\]

This note was produced with substantial AI assistance and is not peer
reviewed.  The exact checks cited below are evidence about the encoded
algebra, not peer review or a priority certificate.

## 1. Exact scope

Let
\[
F=L_0X+H_2+H_3+H_4:\mathbb A^3_{\mathbb C}\longrightarrow
\mathbb A^3_{\mathbb C}
\]
have exact total degree four, with \(L_0\in\operatorname{GL}_3(\mathbb C)\)
and \(H_j\) homogeneous of degree \(j\).  Assume that its leading term lies
in the frozen inclusive row
\[
R=\texttt{Q2-E0-A1-B4-D2-N2}.
\]
Thus the canonical leading tuple is
\[
(\operatorname{rank}JH_4,e,a,b,\delta,\nu)=(2,0,1,4,2,2).
\tag{1}
\]
No hypothesis is made about \(H_2,H_3\), their incidences with \(H_4\), or
the first nonzero coefficient of \(H_4\).

The purpose of this note is only to bridge every point of every frozen
coefficient-pivot stratum \(R/\mathrm C_i\) to the normal form used in
`WORKING_CONIC_DOUBLE_COVER_EXIT.md`.  The lower-degree exclusion and its
independent hostile reconstruction already cover arbitrary lower terms
after that normal form has been reached.

## 2. Uniform leading-normal-form lemma

### Lemma

For every \(H_4\) satisfying (1), there are linear automorphisms
\[
S\in\operatorname{GL}_3(\mathbb C)
\quad\text{and}\quad
T\in\operatorname{GL}_3(\mathbb C)
\]
such that
\[
T\,H_4(SX)=(x^4,x^2y^2,y^4)^T.
\tag{2}
\]
The construction uses no coefficient-pivot \(c_i\) as a denominator.

### Proof

The canonical-pencil theorem in `FROZEN_TAXONOMY_v1.md`, applied to (1),
gives an exact factorization
\[
H_4=A(p,q),
\tag{3}
\]
where \(p,q\) are coprime ternary linear forms and
\(A=(A_0,A_1,A_2)\) is a primitive, basepoint-free triple of binary
quartics.  The projective morphism
\[
\alpha=[A_0:A_1:A_2]:\mathbb P^1\longrightarrow C\subset\mathbb P^2
\]
has degree two, and \(C\) is the reduced irreducible plane curve of degree
two.

Because \(p,q\) are coprime linear forms, they are linearly independent.
Choose a third linear form \(r\) completing them to a basis.  The source
change \(S\) chosen so that
\[
p(SX)=x,\qquad q(SX)=y,\qquad r(SX)=z
\]
is invertible and reduces (3) to a binary quartic triple.  This is the only
source-coordinate step before the degree-two cover is normalized.

Over \(\mathbb C\), an irreducible reduced plane conic is smooth and
projectively equivalent to the Veronese conic
\[
\operatorname{Ver}([u:v])=[u^2:uv:v^2].
\]
After such a projective target change, \(\alpha\) becomes a separable
degree-two map
\[
f:\mathbb P^1\longrightarrow\mathbb P^1
\]
followed by \(\operatorname{Ver}\).

Riemann--Hurwitz gives exactly two ramification points of \(f\), each of
index two.  They are distinct, and their branch values are distinct:
two ramification points cannot lie in one degree-two fibre because each
already contributes multiplicity two.  Independent projective changes on
the source and target copies of \(\mathbb P^1\) send the ramification
points and their branch values to \(0,\infty\).  In those coordinates, the
zero and pole divisors of \(f\) are \(2[0]\) and \(2[\infty]\).
Consequently
\[
f([x:y])=[\lambda x^2:\mu y^2],
\qquad \lambda\mu\ne0,
\]
and invertible rescaling gives \(f([x:y])=[x^2:y^2]\).

The projective change on the source \(\mathbb P^1\) lifts to an invertible
change on the span of \(p,q\), and hence to a member of
\(\operatorname{GL}_3\) after retaining the complementary coordinate
\(r\).  Every projective automorphism of the normalized conic is induced
by the symmetric-square representation of
\(\operatorname{PGL}_2\), so the target change on the second
\(\mathbb P^1\) lifts to a projective target automorphism of
\(\mathbb P^2\).

We have therefore obtained the projective equality
\[
[T H_4(SX)]=[x^4:x^2y^2:y^4].
\tag{4}
\]
The left triple is primitive because \(e=0\), and the right triple is
primitive.  Two primitive triples over the UFD
\(\mathbb C[x,y,z]\) defining the same projective map differ by a nonzero
constant.  Absorbing that constant into the invertible target change gives
the exact polynomial equality (2).  ∎

## 3. Every invertibility condition

The preceding construction uses only the following nonvanishing data.

1. The \(2\times3\) coefficient matrix of \(p,q\) has rank two.  This is
   equivalent to their coprimality in degree one.  A complementary form
   \(r\) can therefore be chosen with
   \(\det(p,q,r)\ne0\).
2. The two ramification points are distinct.  The determinant of their
   two homogeneous coordinate vectors is nonzero, so the projectivity
   sending them to \(0,\infty\) is invertible.
3. The two branch values are distinct, giving the analogous nonzero
   determinant for the target projectivity.
4. The constants \(\lambda,\mu\) are nonzero because the two coordinates
   of a degree-two morphism are nonzero and have the stated zero divisors.
5. A matrix \(M\in\operatorname{GL}_2\) used on the normalized conic lifts
   through \(\operatorname{Sym}^2(M)\); in the basis
   \(u^2,uv,v^2\),
   \[
   \det\operatorname{Sym}^2(M)=(\det M)^3\ne0.
   \]
6. The final proportionality scalar in (4) is nonzero because neither
   primitive triple is zero.

These are intrinsic row conditions.  In particular, the construction
never divides by the first nonzero frozen coefficient \(c_i\), by a
coefficient of \(H_2\) or \(H_3\), or by a lower-degree incidence
parameter.

## 4. Explicit routing of `C00`--`C44`

Use the frozen coefficient order, in blocks of fifteen coefficients for
the three target components.

First, \(H_{4,1},H_{4,2},H_{4,3}\) are linearly independent as quartic
forms.  Otherwise the projective image of \(H_4\) would lie in a target
line, contradicting \(\delta=2\).  In particular \(H_{4,1}\ne0\).
Therefore
\[
R/\mathrm C_i=\varnothing\qquad(15\le i\le44).
\tag{5}
\]

Now fix \(0\le i\le14\).  If \(R/\mathrm C_i\) is empty, there is nothing
to prove.  If it is nonempty, take an arbitrary \(H_4\) in that stratum.
Its equations
\[
c_0=\cdots=c_{i-1}=0,\qquad c_i\ne0
\]
serve only to assign the unique frozen pivot label.  Apply the uniform
lemma using the canonical factorization (3).  Since none of its six
invertibility conditions is \(c_i\ne0\), the same construction works
unchanged on every such point and on every specialization inside the
stratum that preserves the frozen tuple.

Thus the complete routing map is
\[
\begin{array}{c|c}
\text{frozen pieces}&\text{route}\\ \hline
R/\mathrm C_{00},\ldots,R/\mathrm C_{14}
  &\text{if nonempty, use the uniform lemma to reach (2)},\\
R/\mathrm C_{15},\ldots,R/\mathrm C_{44}
  &\varnothing\text{ by (5)}.
\end{array}
\tag{6}
\]
No orbit representative is selected by a coefficient pivot, so a pivot
vanishing on a boundary cannot create a missed normal-form chart.

## 5. Transfer of the lower exclusion

For the source and target changes in (2), set
\[
F'(X)=T\,F(SX).
\]
Then
\[
\det JF'(X)=\det(T)\det(S)\det JF(SX).
\tag{7}
\]
Thus \(F\) is Keller if and only if \(F'\) is Keller.  Linear equivalence
also preserves exact total degree and the property of being a polynomial
automorphism.  The transformed lower terms remain completely arbitrary
homogeneous terms of degrees two and three, and the transformed linear
part remains invertible.

The theorem in `WORKING_CONIC_DOUBLE_COVER_EXIT.md` begins with precisely
this arbitrary-lower-term situation and leading form (2).  Its exact
SymPy calculation and the methodologically independent PARI/GP hostile
reconstruction exhaust the branches
\[
(a,b)=(0,0),\quad ab\ne0,\quad a\ne0=b,\quad b\ne0=a,
\]
including every lower specialization.  Each branch either forces
\(\det L_0=0\) or gives a degree-at-most-four plane Keller map plus a
shear; the latter uses the unconditional bounded-degree plane theorem.
Hence no point of any nonempty frozen pivot stratum in (6) is a quartic
Keller counterexample.

This proves the advertised promotion of exactly
`Q2-E0-A1-B4-D2-N2`.

## 6. Exact replay and fixed inputs

Run

```text
/usr/bin/python3 taxonomy_freeze/verify_bridge_q2_e0_a1_b4_d2_n2_v1.py
/usr/bin/python3 verify_conic_double_cover_exit_sympy.py
audit_conic_double_cover_hostile/audit_conic_double_cover_pari_strict.sh
audit_conic_double_cover_hostile/audit_conic_double_cover_wrapper_selftest.sh
```

from `dimension_three_keller_degree/rung2_degree_bound`.

The bridge verifier is fail closed.  It checks the exact frozen row and
all 45 pivot IDs, pins the precise frozen and lower-proof inputs by
SHA-256, verifies the canonical conic equation and rank-two leading form,
and reconstructs
\(\det\operatorname{Sym}^2(M)=(\det M)^3\) symbolically.

The fixed input hashes are:

```text
41fccc44d23fab125819990a2b27526771fbfb62293910b98cfcf1821576d03d  FROZEN_TAXONOMY_v1.md
5a2bdd57438e9ebcca18d04c53ebc98ced2b61209e2de99674aede501c615c23  frozen_manifest_v1.json
087f682b708e3c339eb6f315d517e861fac8af1a8d754620520da0cb76cedbad  WORKING_CONIC_DOUBLE_COVER_EXIT.md
884b37ffd54c4f27f834139cefd6ce345548f4f24f376f967201572537060577  verify_conic_double_cover_exit_sympy.py
d4b97d26ddf01d707132b7ded678a22b0da686e8448a8047f42b117091240f91  audit_conic_double_cover_hostile/RESEARCH_LOG.md
bed2c80f1b73dcc92aac81e21148bf6cfa4584feea4a240dfef2e655c5985b33  audit_conic_double_cover_hostile/audit_conic_double_cover_pari.gp
5d151bff683bc86963844d984df4093e2b6f6404098799589a406569b640f30f  audit_conic_double_cover_hostile/audit_conic_double_cover_pari_strict.sh
```

The earlier hostile audit independently reconstructed the global
degree-two-cover normalization as well as the raw lower determinant
systems.  This post-freeze replay additionally checked that the frozen
pivot partition contributes no omitted denominator chart.
