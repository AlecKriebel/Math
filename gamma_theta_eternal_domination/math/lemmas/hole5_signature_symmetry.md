# The six-vertex signature symmetry in the `hole5` synthesis instance

## Scope and notation

Let \(F_5\) be the retained complete `hole5` coloring-bank CNF for the
order-12, parameter-three synthesis problem.  As throughout the synthesis
code, \(H=\overline G\), and the Boolean variable \(e_{uv}\) is true exactly
when \(uv\in E(H)\).

The `hole5` template fixes the induced cycle \(0,1,2,3,4,0\), fixes vertex
\(5\) as a common \(H\)-neighbor of \(0\) and \(1\), and leaves vertices
\[
X=\{6,7,8,9,10,11\}
\]
undistinguished.  Put \(K=\{0,1,2,3,4,5\}\).  For \(v\in X\), define its
ordered core signature
\[
s(v)=(e_{0v},e_{1v},e_{2v},e_{3v},e_{4v},e_{5v})\in\{0,1\}^6.
\]
We order signatures lexicographically with \(0<1\), reading the coordinates
in the displayed order.

The symmetry-breaking predicate is
\[
S:\qquad s(6)\leq_{\rm lex}s(7)\leq_{\rm lex}\cdots
\leq_{\rm lex}s(11).
\]

## Invariance of the complete formula

**Lemma 1.**  Every permutation of \(X\), extended by the identity on \(K\),
is an automorphism of the satisfiability problem represented by \(F_5\).

**Proof.**  Relabel graph-edge variables by
\(e_{uv}\mapsto e_{\pi(u)\pi(v)}\), sorting the two endpoints after
relabeling.  Relabel the auxiliary variables in the same way:

- \(w_{uvx}\mapsto w_{\pi(u)\pi(v)\pi(x)}\);
- \(f_{\{a,b,c\}}\mapsto f_{\{\pi(a),\pi(b),\pi(c)\}}\);
- every move variable maps by relabeling its configuration, attacked
  vertex, and moving guard.

The graph constraints—\(\omega(H)\leq3\), the external-common-neighbor
conditions, connectedness of \(G\), domination of selected configurations,
one-guard response closure, nonemptiness of the family, and the redundant
triangle/family strengthening—are all stated uniformly over vertices,
pairs, triples, or cuts.  The connectedness clauses single out vertex \(0\),
which \(\pi\) fixes.

The `hole5` template clauses are also preserved.  The induced cycle and the
two distinguished common-neighbor edges lie inside \(K\).  The no-external-
hub clauses for vertices \(6,\ldots,11\) are merely permuted among
themselves; the corresponding clause for distinguished vertex \(5\) is
fixed.

It remains to check the complete coloring bank.  A bank clause depends only
on the partition of the vertices into equal-color blocks.  Permuting \(X\)
maps a coloring proper on the forced template edges to another such
coloring.  Renaming its three colors by first occurrence restores the
bank's restricted-growth-string convention without changing its equal-color
blocks.  Hence the induced permutation maps the set of all bank clauses to
itself.  Thus a satisfying assignment of \(F_5\) maps to another satisfying
assignment. \(\square\)

## Coverage of the symmetry breaker

**Lemma 2.**  Every satisfying assignment of \(F_5\) has a relabeled
satisfying assignment satisfying \(S\).

**Proof.**  The six signatures form a multiset in the totally ordered set
\(\{0,1\}^6\).  Choose a permutation of \(X\) that places this multiset in
nondecreasing order.  Lemma 1 shows that applying the same permutation to
all graph and auxiliary variables preserves satisfaction of \(F_5\).  The
result satisfies \(S\).  Equal signatures may be ordered arbitrarily.
\(\square\)

**Theorem 3 (equisatisfiability).**
\[
F_5\text{ is satisfiable}\quad\Longleftrightarrow\quad F_5\land S
\text{ is satisfiable}.
\]

**Proof.**  The reverse implication is immediate because \(F_5\land S\)
contains every clause of \(F_5\).  The forward implication is Lemma 2.
\(\square\)

Consequently, a checked refutation of \(F_5\land S\), together with an audit
that the appended clauses encode exactly \(S\), refutes the original
`hole5` instance.  This is a semantic symmetry argument, not a claim that
the symmetry clauses are logical consequences of \(F_5\).

## Auxiliary-free CNF encoding

For two signatures
\[
a=(a_0,\ldots,a_5),\qquad b=(b_0,\ldots,b_5),
\]
the forbidden event \(a>_{\rm lex}b\) has a unique first differing
coordinate \(t\) with \(a_t=1\), \(b_t=0\), and a common prefix
\(p\in\{0,1\}^t\).

For every \(t\in\{0,\ldots,5\}\) and every common prefix
\(p=(p_0,\ldots,p_{t-1})\), append the clause
\[
\left(\bigvee_{\substack{0\leq q<t\\p_q=0}}(a_q\vee b_q)\right)
\vee
\left(\bigvee_{\substack{0\leq q<t\\p_q=1}}(\neg a_q\vee\neg b_q)\right)
\vee\neg a_t\vee b_t.
\tag{1}
\]
Clause (1) is false exactly on assignments having prefix \(p\) on both
signatures and first difference \(1,0\) at coordinate \(t\).  Therefore the
\(\sum_{t=0}^5 2^t=63\) clauses for one adjacent pair encode exactly
\(a\leq_{\rm lex}b\).

Applying them to the five adjacent pairs
\((6,7),(7,8),(8,9),(9,10),(10,11)\) gives exactly
\[
5\cdot63=315
\]
clauses.  Their literal count is
\[
5\sum_{t=0}^5 2^t(2t+2)=3{,}210.
\]
No new variable is introduced.  Thus the retained formula counts change
from \(6{,}886\) variables, \(23{,}653\) clauses, and \(188{,}959\)
literals to \(6{,}886\) variables, \(23{,}968\) clauses, and \(192{,}169\)
literals.

## Independent audit obligations

A certificate-backed use of this theorem must check all of the following.

1. The retained `hole5` package and exact CNF are bound by cryptographic
   hashes.
2. The retained CNF is an exact byte prefix, apart from its updated DIMACS
   clause count; exactly the 315 clauses above are appended.
3. Exhaustive truth-table evaluation over all \(2^6\times2^6=4{,}096\)
   pairs of signatures confirms that each 63-clause comparator is true
   exactly for the ordered pairs.
4. The retained complete CNF clause multiset is invariant under the five
   adjacent transpositions of \(6,\ldots,11\), which generate the full
   \(S_6\) action.  The variable map must include graph, witness, family,
   and move variables.
5. Source files, input artifacts, generated artifacts, tools, commands, and
   proof files are hash-bound.  A solver timeout or unchecked proof remains
   a nonclaim.

The symmetry theorem is only a coverage reduction.  It does not by itself
prove `hole5` unsatisfiable and does not resolve the \(\gamma\)–\(\theta\)
conjecture.
