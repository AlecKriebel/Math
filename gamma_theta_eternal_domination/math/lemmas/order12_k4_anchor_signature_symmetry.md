# Anchor-canonical minimum signatures for the order-12 parameter-four target

Status: **PROPOSED PROVED SYMMETRY REDUCTION PENDING HOSTILE REVIEW**

Claim boundary: this note gives a four-cube satisfiability reduction for the
accepted anchored connected target.  It does not assert that every discarded
cube is itself unsatisfiable, does not alter the immutable 16-cube production
run, and does not exclude the \((12,4)\) slice or resolve the universal
conjecture.  No literature-novelty claim is made.

## 1. Setting

Let \(F_0\) denote the accepted anchored order-12 parameter-four formula
before the outer-signature ordering clauses, but including the complete
anchor-normalized four-coloring bank.  In a decoded model, put
\(H=\overline G\), let
\[
 A=\{0,1,2,3\}
\]
be the anchored \(H\)-clique, and let \(X=\{4,\ldots,11\}\).  For
\(v\in X\), define
\[
 s(v)=(e_{0v},e_{1v},e_{2v},e_{3v})\in\{0,1\}^4.
\]

Let \(S\) be the already accepted outer \(S_8\) breaker
\[
 s(4)\le_{\rm lex}s(5)\le_{\rm lex}\cdots\le_{\rm lex}s(11),
\qquad 0<1,
\]
and write \(F=F_0\land S\) for the frozen parent.

The four entries of \(s(4)\) are DIMACS variables
\[
 4,\quad 14,\quad 23,\quad 31.
\]

## 2. The anchor action before outer sorting

Every permutation \(\pi\in S_4\) of the anchor vertices preserves the
decoded constraints of \(F_0\), after the following simultaneous relabeling.

1. Relabel anchor vertices by \(\pi\), fixing the outer vertex set as a set.
2. Relabel every edge, common-neighbor witness, family, and move variable by
   the induced vertex permutation.
3. In the four-coloring interpretation, apply the same permutation \(\pi\)
   to the four color names.

The static graph constraints, connected cuts, one-guard clauses, and anchor
clique units are invariant under vertex relabeling.  For the coloring bank,
an anchor-normalized coloring has anchor colors
\((0,1,2,3)\).  Permuting anchor vertices and color names by the same
\(\pi\) again gives anchor colors \((0,1,2,3)\).  The outer color row is
merely sent to another of the \(4^8\) rows already present in the complete
bank.  Hence the complete bank is preserved as a set.

Thus an anchor permutation maps every model of \(F_0\) to another model of
\(F_0\).  The breaker \(S\) need not be syntactically invariant under this
action.  After applying \(\pi\), however, permute the eight outer vertices
to sort their transformed signatures.  The accepted outer \(S_8\) argument
then produces a model of \(F=F_0\land S\).

## 3. Four canonical cubes

For a sorted model of \(F\), concatenate the eight signatures into the
32-bit word
\[
 L=s(4)s(5)\cdots s(11).
\]
Starting from any model of \(F\), apply each of the 24 anchor permutations
described above and re-sort the outer vertices.  Choose an image for which
\(L\) is lexicographically least.

**Lemma.**  In this least image, the four bits of \(s(4)\) are
nondecreasing.

**Proof.**  Suppose instead that \(s(4)\) has an adjacent inversion:
its coordinates \(j,j+1\) are \(1,0\).  Swap the corresponding two anchor
vertices, and then re-sort the outer vertices.  The swapped image of the old
vertex \(4\) has a signature agreeing with \(s(4)\) before coordinate \(j\)
and having \(0,1\) at coordinates \(j,j+1\).  Its signature is therefore
strictly smaller than the old \(s(4)\).

After re-sorting, the new minimum signature is no larger than that swapped
signature.  Hence the new first signature, and therefore the new
concatenated word \(L\), is strictly smaller than the chosen least \(L\), a
contradiction.  Thus no adjacent inversion exists. \(\square\)

The only nondecreasing four-bit words are
\[
 0000,\quad 0001,\quad 0011,\quad 0111,\quad 1111.
\]
The word \(1111\) would make outer vertex \(4\), together with the anchored
\(H\)-\(K_4\), an \(H\)-\(K_5\).  The accepted target has no \(H\)-\(K_5\).
Therefore the last word is impossible.

**Theorem (four-cube anchor reduction).**  The frozen parent \(F\) is
satisfiable if and only if at least one of
\[
 F\land C_{0000},\qquad
 F\land C_{0001},\qquad
 F\land C_{0011},\qquad
 F\land C_{0111}
\]
is satisfiable.

**Proof.**  If \(F\) is satisfiable, the least-orbit construction above gives
a model of \(F\) in one of the four displayed cubes.  The converse is
immediate because each displayed formula contains \(F\). \(\square\)

## 4. What the theorem does and does not say

The theorem is an orbit-coverage statement.  In particular, it does **not**
claim that the four noncanonical zero-first cubes
\[
 0010,\quad0100,\quad0101,\quad0110
\]
are unsatisfiable.  A model in one of those labeled cubes would have an
anchor-and-outer relabeling whose sorted representative lies in one of the
four canonical cubes.

The separate minimum-signature lemma proves that every `1***` cube is
actually unsatisfiable in the frozen parent.  That logical implication is
stronger than symmetry redundancy for those eight leaves, but it is not
needed for the four-cube orbit argument once the no-\(K_5\) condition is
used.

The existing v3 production directory remains a 16-cube append-only run.  It
must not be rewritten or have statuses inferred from this note.  A future
negative result may instead combine:

1. this independently reviewed four-cube orbit-coverage proof;
2. independently replayed UNSAT certificates for the four canonical leaves;
   and
3. a coverage audit checking that the solver leaves are exactly those four
   formulas.

Until all three items are accepted, the complete connected parent remains
open.

