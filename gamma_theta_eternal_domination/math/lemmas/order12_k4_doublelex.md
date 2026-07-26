# A doubly lexicographic symmetry breaker for the order-12 parameter-four target

Status: **PROPOSED PROVED SYMMETRY REDUCTION PENDING HOSTILE REVIEW**

Claim boundary: this note gives an equisatisfiable strengthening of the
accepted anchored connected target.  It does not alter the immutable
16-cube production run, prove that the strengthened formula is
unsatisfiable, exclude the \((12,4)\) slice, or resolve the universal
conjecture.  No literature-novelty claim is made.

## 1. The anchor--outer matrix

Let \(F_0\) be the accepted anchored order-12 parameter-four formula before
the outer-signature ordering clauses, including its complete
anchor-normalized four-coloring bank.  Put \(H=\overline G\), let
\[
 A=\{0,1,2,3\},\qquad X=\{4,\ldots,11\},
\]
and form the \(8\)-by-\(4\) binary matrix
\[
 M_{v,j}=e_{jv}\qquad(v\in X,\ j\in A),
\]
where \(e_{jv}=1\) means \(jv\in E(H)\).  Read \(M\) in row-major order,
with the outer vertices in the order \(4,\ldots,11\) and the anchor
vertices in the order \(0,\ldots,3\).

The group \(S_8\times S_4\) acts on \(M\) by permuting its rows and columns.
The corresponding simultaneous relabeling of every graph, witness,
family, and move variable preserves \(F_0\).  For an anchor permutation,
also permute the four color names in the same way.  This restores the
normalization \(c(j)=j\) on the relabeled anchor, and the complete bank of
\(4^8\) outer color rows is preserved as a set.

## 2. A simultaneous row-and-column representative

For any model of \(F_0\), consider the finite set of its
\(S_8\times S_4\) images and choose one whose row-major matrix word is
lexicographically least, using \(0<1\).

**Lemma 1 (row order).**  The rows in this least image are
lexicographically nondecreasing.

**Proof.**  If an earlier row were lexicographically larger than a later
row, swapping those two outer vertices would put the smaller row first and
strictly decrease the row-major word.  The swap is an allowed \(S_8\)
action, contradicting minimality. \(\square\)

For an anchor \(j\), write its column word as
\[
 c(j)=(e_{j4},e_{j5},\ldots,e_{j,11})\in\{0,1\}^8.
\]

**Lemma 2 (column order).**  The columns in the same least image are
lexicographically nondecreasing:
\[
 c(0)\le_{\rm lex}c(1)\le_{\rm lex}c(2)\le_{\rm lex}c(3).
\]

**Proof.**  Suppose adjacent columns \(j,j+1\) are inverted.  At the first
row on which they differ, their entries are \(1,0\).  Swap anchor vertices
\(j,j+1\), together with their semantic variables and color names.  All
earlier matrix entries are unchanged, while at the position of that first
\(1\) the new entry is \(0\).  The row-major word strictly decreases.  This
is an allowed \(S_4\) action, contradicting minimality. \(\square\)

Let \(R\) be the accepted row-order breaker already present in the frozen
parent, and let \(C\) be the column-order predicate in Lemma 2.

**Theorem (DoubleLex equisatisfiability).**
\[
 F_0\quad\text{is satisfiable}\quad\Longleftrightarrow\quad
 F_0\land R\land C\quad\text{is satisfiable}.
\]
Equivalently, since the frozen parent is \(F=F_0\land R\),
\[
 F\quad\text{is satisfiable}\quad\Longleftrightarrow\quad
 F\land C\quad\text{is satisfiable}.
\]

**Proof.**  A model of \(F_0\) has a least orbit image as above.  Lemmas 1
and 2 show that this image satisfies \(R\land C\).  The reverse implication
is immediate.  The second equivalence follows because \(F_0\) and
\(F_0\land R\) are already proved equisatisfiable. \(\square\)

This is an orbit-coverage theorem, not a claim that a labeled model
violating \(C\) cannot exist.

## 3. Auxiliary-free clauses and exact census

The same auxiliary-free comparator used for the accepted four-bit row
order can compare adjacent eight-bit columns.  For columns
\(a=(a_0,\ldots,a_7)\) and \(b=(b_0,\ldots,b_7)\), forbid every unique
first difference \(a_t=1,b_t=0\).  For each
\(t\in\{0,\ldots,7\}\) and prefix \(p\in\{0,1\}^t\), add
\[
 \left(
   \bigvee_{\substack{q<t\\p_q=0}}(a_q\vee b_q)
 \right)
 \vee
 \left(
   \bigvee_{\substack{q<t\\p_q=1}}(\neg a_q\vee\neg b_q)
 \right)
 \vee\neg a_t\vee b_t.
\tag{3.1}
\]
It is false exactly on the named first-difference event.  Thus one
eight-bit comparator contributes
\[
 \sum_{t=0}^7 2^t=255
\]
clauses and
\[
 \sum_{t=0}^7 2^t(2t+2)=3,586
\]
literals.  The three adjacent column comparators contribute exactly
\[
 765\ \text{clauses}\qquad\text{and}\qquad10,758\ \text{literals},
\]
with no new variables.

Starting from the accepted frozen-parent census, the DoubleLex formula
therefore has
\[
 18,381\ \text{variables},\quad
 115,507\ \text{clauses},\quad
 1,190,774\ \text{literals}.
\]
An implementation must independently reconstruct and hash the exact bytes;
these combinatorial counts are not a substitute for that audit.

## 4. Consequences for the first signature

Column order immediately makes the first matrix row nondecreasing.  Hence
the first outer signature is one of
\[
 0000,\quad0001,\quad0011,\quad0111,\quad1111.
\]
The last word would extend the anchored \(H\)-\(K_4\) to an \(H\)-\(K_5\),
which the target forbids.  Consequently every \(S_8\times S_4\) orbit has a
representative in one of the four canonical cubes
\[
 0000,\quad0001,\quad0011,\quad0111.
\]

The DoubleLex formula is stronger than merely selecting one of these four
first-row patterns: it also orders the complete eight-bit anchor columns.
This additional restriction is nevertheless sound by the theorem above.

## 5. Required acceptance gate

Before this reduction can support a finite negative result, an independent
review must check:

1. the exact \(S_8\times S_4\) action on every semantic variable family;
2. covariance of the complete anchor-normalized coloring bank;
3. the two least-orbit arguments, including their use of row-major order;
4. all \(2^{16}\) truth assignments for an eight-bit comparator, or an
   equivalent exhaustive check;
5. the exact generated clause suffix, counts, hash, and parent binding; and
6. any UNSAT certificate against the exact strengthened CNF.

