# Dynamic almost-caps: the one-sided chord obstruction

## Status and scope

Date: 2026-07-28 (PDT)

This note audits the proposed descent from the forced-witness theorem for
the shortest odd three-gate geometry.  It does **not** prove the arbitrary
odd-cycle exclusion.

The main rigorous conclusion is negative but useful: a third-type
almost-cap supplies only one of the two clauses needed to replace a tight
gate by an equality chord.  Consequently, neither raw implication-path
length nor the number of gates is presently a sound decreasing measure.
C-095 and the C-099 two-incidence equality control independently rule out
repairing this defect by assuming that a same-sign physical representative
preserves the almost-cap's incidences.  C-098 supplies a cap dichotomy only
under its stated \(\gamma=3\) and physical-endpoint hypotheses.  None of
these accepted results supplies a proved decreasing measure for the
remaining repair process.

All notation below is local.  No claim of literature priority is made.

## 1. Exact Boolean signature of an almost-cap

Let the anchor colors be cyclically ordered as \(a,b,c\).  Suppose

\[
 L(x)=\{a,c\},\qquad L(y)=\{a,b\},\qquad L(q)=\{b,c\},
\tag{1.1}
\]

so \(x,y,q\) have types \(b,c,a\), respectively, and suppose

\[
 xq,yq\in E(H).
\tag{1.2}
\]

Use the chirality coordinates

\[
\begin{array}{c|cc}
&0&1\\ \hline
x&a&c\\
y&b&a\\
q&c&b.
\end{array}
\tag{1.3}
\]

Write the corresponding Boolean variables as \(X,Y,Q\).  The edge \(xq\)
has common allowed color \(c\), and hence contributes

\[
 \neg(X=1\wedge Q=0),
 \qquad\text{equivalently}\qquad
 \neg X\lor Q.
\tag{1.4}
\]

The edge \(yq\) has common allowed color \(b\), and contributes

\[
 \neg(Y=0\wedge Q=1),
 \qquad\text{equivalently}\qquad
 Y\lor\neg Q.
\tag{1.5}
\]

Resolving (1.4) and (1.5) on \(Q\) gives exactly

\[
 \boxed{\neg X\lor Y.}
\tag{1.6}
\]

Thus the two cap arms forbid only

\[
 (X,Y)=(1,0),\qquad\text{that is,}\qquad (x,y)=(c,b).
\tag{1.7}
\]

By contrast, the ordinary cross clause between the two endpoint types,
whose common color is \(a\), is

\[
 \boxed{X\lor\neg Y;}
\tag{1.8}
\]

it forbids

\[
 (X,Y)=(0,1),\qquad\text{that is,}\qquad (x,y)=(a,a).
\tag{1.9}
\]

The conjunction of (1.6) and (1.8) is \(X=Y\), which is the tight-gate
chirality equality.  The almost-cap arms alone provide only (1.6).

This calculation is independent of whether \(aq\) is an edge of \(H\) or
of \(G\).  The anchor incidence determines whether
\(\{a,x,y\}\) is visibly nondominating, but it does not add the missing
endpoint clause (1.8).

### Corollary 1.1 (a raw chord replacement is unsound)

Replacing a tight gate, or an equality subpath, by the two almost-cap arms
does not preserve the represented binary relation.  For example,

\[
 (X,Y,Q)=(0,1,0)
\tag{1.10}
\]

satisfies both (1.4) and (1.5), although \(X\ne Y\).  Therefore a descent
measure based only on shortening the signed gate cycle after inserting
\(q\) is not sound.

Equivalently, if the complementary route in an odd signed cycle imposes
\(X\ne Y\), the almost-cap eliminates at most one of the two inequality
orientations.  It can create a unit-bearing lollipop, but it does not by
itself create a smaller unsatisfiable bicycle.  A proof must track which
literal orientation survives.

## 2. Why same-sign physicalization does not finish the repair

Work now in the intended shortest-cycle setting with \(\gamma(G)=3\), where
the two original clause endpoints \(x\) and \(y\) have already been replaced
by same-sign physical representatives as required by C-098.  In the dynamic
case \(aq\in E(G)\), accepted same-sign physicalization supplies a
type-\(a\) vertex \(r\) with

\[
 ar\in E(H)
\tag{2.1}
\]

and with the same chirality event as \(q\).  It is tempting to replace
\(q\) by \(r\) and claim

\[
rx,ry\in E(H).
\tag{2.2}
\]

That inference is false.  Accepted C-095 has an equality control in which
a same-sign physical representative loses a specified original clause
edge.  Accepted C-099 has an equality control in which the unique
same-sign representative loses both specified incidences simultaneously.
These controls refute raw incidence transport; they do not by themselves
instantiate every physical-endpoint hypothesis of the shortest-cycle
geometry.

For each failed incidence in (2.2), apply C-094 to physicalize both
endpoints of the corresponding original clause.  If those representatives
are adjacent in \(H\), the physical complement edge is already restored.
If they are adjacent in \(G\), C-098 (using \(\gamma(G)=3\)) supplies the
new virtual-rainbow cap.  In the exact third-type case this repairs the
corresponding logical clause, but it may add a tight gate.

The accepted controls therefore show that raw complement-edge incidence
need not transport and that a descent based only on reducing the number of
tight gates is unsound.  They do **not** prove monotonicity of:

- the number of tight gates;
- total connector length;
- same-sign physicalization distance; or
- the number of failed physical incidences.

In particular, no accepted theorem presently proves that the last three
quantities decrease, stay fixed, or increase during every repair.

## 3. Precisely delimited remaining lemma

A valid descent needs a marked, oriented obstruction rather than an
unoriented signed cycle.  One possible sufficient statement is:

> **Paired-repair lemma (open).**  In an inclusion-minimal unit-free
> response bicycle, let a gamma witness produce the third-type
> almost-cap clauses (1.4)--(1.5).  Then either the resolution clause
> (1.6) shortens one of the two marked literal-to-complement paths while
> retaining the other terminal obstruction, or every C-098 repair of the
> missing physical incidences produces a marked obstruction with a
> strictly smaller lexicographic pair
> \[
>   (\text{number of original bicycle clauses},
>     \text{number of unresolved representative incidences}).
> \]

The first alternative must explicitly retain both directions required
for 2-SAT unsatisfiability.  Merely observing that (1.6) is a shorter
implication is insufficient, by Corollary 1.1.  The second alternative
must survive the C-095/C-099 equality controls and remain compatible with
the C-098 cap theorem.

No proof of this paired-repair lemma is given here.  The exact obstruction
in Section 1 is the reason a simple physical-cap or gate-count descent
cannot be claimed.
