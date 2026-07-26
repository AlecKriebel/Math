# The minimum outer signature in the order-12 parameter-four target

Status: **PROPOSED PROVED SEARCH REDUCTION PENDING HOSTILE REVIEW**

Claim boundary: this note proves a logical consequence of the already
accepted connected anchored target and its sound outer-vertex ordering.  It
does not prove the full parent UNSAT, exclude the \((12,4)\) slice, resolve
the universal conjecture, or assert literature novelty.

## Setting

Let \(G\) be a connected graph represented by the exact anchored
order-12 parameter-four target, and put \(H=\overline G\).  The anchor
\[
 A=\{0,1,2,3\}
\]
is a clique in \(H\), equivalently an independent set in \(G\).  For each
outer vertex \(v\in X=\{4,\ldots,11\}\), write
\[
 s(v)=(e_{0v},e_{1v},e_{2v},e_{3v}),
\]
where \(e_{uv}=1\) means \(uv\in E(H)\).  The accepted \(S_8\) symmetry
breaker orders the outer vertices so that
\[
 s(4)\le_{\mathrm{lex}}s(5)\le_{\mathrm{lex}}\cdots
 \le_{\mathrm{lex}}s(11),
\]
with \(0<1\).

In the frozen parent DIMACS file, the four entries of \(s(4)\) are variables
\[
 4,\quad 14,\quad 23,\quad 31.
\]

## Minimum-signature lemma

**Lemma.** Every model of the exact connected anchored parent has
\[
 e_{0,4}=0.
\]

**Proof.**  Since \(A\) is independent in \(G\), vertex \(0\) has no
\(G\)-neighbor in \(A\setminus\{0\}\).  The graph \(G\) is connected and has
more than one vertex, so \(0\) has a \(G\)-neighbor \(v\) in the outer set
\(X\).  Equivalently, \(e_{0v}=0\), so the first coordinate of \(s(v)\) is
zero.

The signature \(s(4)\) is lexicographically no larger than \(s(v)\).
Every four-bit word whose first coordinate is one is lexicographically
larger than every four-bit word whose first coordinate is zero.  Hence the
first coordinate of \(s(4)\) is also zero.  Thus \(e_{0,4}=0\). \(\square\)

The same conclusion can be phrased contrapositively.  If \(e_{0,4}=1\),
then signature ordering forces \(e_{0v}=1\) for every outer vertex \(v\).
The anchored \(H\)-clique also gives \(e_{0j}=1\) for
\(j\in\{1,2,3\}\).  Vertex \(0\) is then universal in \(H\), hence isolated
in \(G\), contradicting connectedness.

## Eight-cube corollary

Let \(F\) be the frozen parent and let \(C_b\) be the exact Boolean cube on
\((e_{0,4},e_{1,4},e_{2,4},e_{3,4})\) indexed by
\(b\in\{0,1\}^4\).

**Corollary.**  For every \(b\) whose first bit is one,
\[
 F\land C_b
\]
is unsatisfiable.  Equivalently, only the eight cubes
\[
 0000,0001,0010,0011,0100,0101,0110,0111
\]
can contain a model of \(F\).

**Proof.**  Each of the eight omitted cubes contains the unit
\(e_{0,4}=1\), contrary to the lemma. \(\square\)

Combining this corollary with the elementary 16-cube coverage identity gives
the smaller exact identity
\[
 F\equiv
 \bigvee_{b\in\{0\}\times\{0,1\}^3}(F\land C_b).
\]
The eight displayed disjuncts remain pairwise inconsistent.

## Scope and production status

The immutable v3 production run deliberately contains all 16 Boolean cubes.
This note does not rewrite its partition, checkpoints, or statuses.  At the
time of writing, only case `1111` has a retained independently replayed LRAT
certificate; the production histogram therefore remains one
`UNSAT_LRAT_VERIFIED` leaf and 15 `PENDING` leaves.

For a future mixed hand-and-machine exclusion, an independent coverage
checker may combine this lemma with certificates for the eight `0***`
leaves.  Alternatively, the existing runner may still certify all 16 leaves.
Neither route supports an aggregate claim until its exact coverage and every
machine certificate used by that route receive independent verification.

