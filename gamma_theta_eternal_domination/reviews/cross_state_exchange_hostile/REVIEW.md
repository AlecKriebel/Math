# Hostile review: cross-state exchange and base-orderability

## Verdict

**ACCEPT THEOREM 2.1, COROLLARY 2.2, THEOREM 3.1, COROLLARY 3.2, AND
PROPOSITIONS 1.1, 2.1, AND 2.2.**

No false theorem, illegal guard move, response-table error, or parameter
error was found.  The two universal cross-state results were re-derived
directly from the one-guard definition.  An evaluator-independent checker
exhausted every labeled abstract exchange system through rank three and
literally replayed all 100 displayed state/attack responses.

All defects found during hostile review have been repaired in the reviewed
bytes:

1. “without **every** base ordering” is now correctly “without **any** base
   ordering”; and
2. the undefined, unbound assertion about an enumerated cross pair
   dominating the endpoint positions has been removed;
3. rank zero is excluded explicitly by \(m\geq1\);
4. the endpoint-reversal dual needed for \(|F|\geq5\) is explicit; and
5. the open problem now quantifies \(G,\mathcal F,S,T\) and states the exact
   specified-pair refutation boundary.

No novelty or literature-priority claim is made in this review.

## Frozen review object

| Artifact | Lines | Bytes | SHA-256 |
|---|---:|---:|---|
| `math/working/cross_state_response_exchange.md` | 452 | 13,534 | `e30a0ac4e028deefbf4c4533646ff934b617d8ff61dce38ec2389a50d622d8e7` |
| `math/working/cross_state_base_orderability_obstruction.md` | 467 | 13,718 | `40ba7b5805f276cd1c5d4496f090371c04bbb44b28b6174c1efc83cb6fa82707` |
| independent checker `audit.py` | 536 | 17,561 | `94f4825e5f9f7fa8dc2f0e2706f2e8d27a2eb1f32eddc5f9dc93ec56ba2dc671` |
| checker result `evidence.json` | 85 | 2,845 | `75a90ac05eeef9e18b31579cf8c08eda3e60a23993edd9ec698cf091e78c8756` |

Repository commit at review time:
`d99d2b8b1fcb55be919cd0121ef7c22636b94e25`.

The checker imports no campaign evaluator, search engine, NetworkX, or SAT
solver.  It uses ordinary Python sets, a fresh graph6 decoder, exhaustive
subset/coloring routines, and a literal greatest-fixed-point implementation.
The author notes were not edited by this reviewer.

## 1. Exact model and independent-state forcing

Both notes use the correct one-guard-moves model:

- attacks occur only outside the current configuration;
- one occupied adjacent guard moves to the attacked vertex;
- the successor remains in the specified family; and
- every member of that family dominates.

The independent-state forcing argument is exact.  Starting from any family
state, repeatedly attack unoccupied vertices of an independent \(k\)-set
\(S\).  A guard already on \(S\) cannot answer an attack at another member
of \(S\), so every response strictly increases \(|D\cap S|\).  After at most
\(k\) steps the state is \(S\).  Thus every independent \(k\)-set belongs to
every eternal \(k\)-family, not merely to the greatest family.

The notes also keep the family-response list distinct from static viability:

\[
L^{\mathcal F}_S(x)
=\{u\in S:ux\in E(G),\ S-u+x\in\mathcal F\}.
\]

No proof silently replaces membership in \(\mathcal F\) by domination of a
single successor.

## 2. Theorem 2.1 and Corollary 2.2

Let

\[
C=S\cap T,\qquad A=S-T,\qquad B=T-S,
\]

and let \(D(U,X)=C\cup(A-U)\cup X\) be a family state.

For target expansion, \(b\in B-X\) is unoccupied.  Every guard in
\(C\cup X\) is nonadjacent to \(b\), since all those vertices lie in the
independent set \(T=C\cup B\).  Closure therefore moves a guard from
\(A-U\), giving exactly

\[
(U+a,X+b)\in\mathcal Q_{\mathcal F}(S,T).
\]

For source restoration, \(a\in U\) is unoccupied.  Every guard in
\(C\cup(A-U)\) is nonadjacent to \(a\), since those vertices lie in the
independent set \(S=C\cup A\).  Closure therefore moves a guard from \(X\),
giving exactly

\[
(U-a,X-b)\in\mathcal Q_{\mathcal F}(S,T).
\]

The quantifier order is the advertised adversarial one: for every current
accepted pair and every requested next target/restoration position, some
legal source exists.  Successive expansion accepts any ordering of \(B\);
at level \(m\), all of \(A\) has been removed and all of \(B\) inserted, so
the endpoint is exactly \(T\).  Successive restoration gives the reverse
statement from any intermediate pair.  Corollary 2.2 does not infer a
single subset-compatible bijection.

## 3. Ridge response covariance, including \(x=b\)

Write

\[
S=C\cup\{a\},\qquad T=C\cup\{b\}.
\]

Since \(T\) dominates \(a\), while no member of \(C\) is adjacent to \(a\),
the edge \(ab\) is forced.

The special domain point \(x=b\) is handled correctly.  It satisfies
\(b\notin S\), while \(\rho(b)=a\notin T\), so both lists in the covariance
identity are defined.  Independence of \(T\), the edge \(ab\), and
\(S-a+b=T\in\mathcal F\) give

\[
L^{\mathcal F}_S(b)=\{a\},\qquad
L^{\mathcal F}_T(a)=\{b\}.
\]

For \(x\notin S\cup T\), membership of the exchanged color transports
because the common successor \(C\cup\{x\}\) must dominate the opposite
exchanged vertex.

For a common color \(u\in C\), suppose

\[
D=C-\{u\}+\{a,x\}\in\mathcal F.
\]

Attack the unoccupied vertex \(b\).  The guards in \(C-\{u\}\) cannot
respond.  A response \(x\to b\) would produce

\[
C-\{u\}+\{a,b\},
\]

which leaves \(u\) undominated by independence of both \(S\) and \(T\).
That successor cannot lie in an eternal dominating family.  Closure forces
\(a\to b\), hence \(T-u+x\in\mathcal F\).  Symmetry gives the reverse
implication.  This proves the full list identity, not only equality of list
sizes.

## 4. Closed ridge paths and the domain audit

For each ridge step, its transposition maps the current reference state to
the next state and maps the current outside domain bijectively to the next
outside domain.  Consequently, if \(x\notin S_0\), every partial image of
\(x\) remains outside the reference state at which the next response list
is evaluated.  Composition is therefore legitimate:

\[
\rho(L^{\mathcal F}_{S_0}(x))
=L^{\mathcal F}_{S_\ell}(\rho(x)).
\]

When \(S_\ell=S_0\), the product permutation stabilizes \(S_0\) and its
complement setwise.  The displayed identity is equivalent to

\[
(u,x)\in\mathcal R_{S_0}
\iff
(\rho(u),\rho(x))\in\mathcal R_{S_0},
\]

so \(\rho\) is an automorphism of the bipartite response-incidence
relation.  The theorem does not claim that \(\rho\) is a graph automorphism
or that it is the identity.

The separate ordinary-set probe through order eight recorded zero failures
of ridge list transport.  That is supporting finite evidence only; the
proof above, not the enumeration, establishes the universal theorem.

## 5. Ranks at most two

At rank two, make a bipartite graph from the accepted singleton exchanges.
Expansion at the empty state gives every target vertex positive degree.
Restoration at the full state gives every source vertex positive degree
(the attacked source and the singleton row are complementary, but as the
attack ranges over both sources, both rows occur).  A bipartite graph with
two vertices on each side and no isolated vertex has a perfect matching.
That matching supplies the only non-endpoint subsets required for a base
ordering.

The independent exhaustion found seven labeled rank-two systems satisfying
both axioms and zero non-base-orderable systems.

## 6. Rank-three minimum

At rank three, \(E\) records level-one states and \(F\) records level-two
states by their missing pairs.  A base ordering is equivalent to a perfect
matching in \(E\cap F\).

The endpoint axioms first show that \(E\) has no empty column and \(F\) has
no empty row.  The middle-level axioms then show that neither relation has
an isolated vertex on either side.

If \(|E|=3\), it is a perfect matching.  Restoration from any \(F\)-state
forces its missing column to be the matched column of its missing row.
Thus \(F\subseteq E\); the absence of empty \(F\)-rows gives \(F=E\).

If \(|E|=4\) and \(E\) had no perfect matching, the no-isolate condition
would force two disjoint two-edge stars.  The two degree-one rows in one
star would force every \(F\)-edge to avoid their shared column, contradicting
the absence of empty \(F\)-columns.  Hence \(E\) has a perfect matching.
It is unique; after relabeling it as

\[
M=\{a_0b_0,a_1b_1,a_2b_2\}
\]

with extra edge \(a_0b_1\), restoration forces the needed row/column
incidences and hence \(M\subseteq F\).  Therefore \(M\subseteq E\cap F\),
again producing a base ordering.  A non-base-orderable system must have
\(|E|\geq5\).

### Explicit endpoint-reversal dual

To derive \(|F|\geq5\), define an exchange system with source \(B\) and
target \(A\) by

\[
\mathcal Q^\dagger
=\{(B-X,A-U):(U,X)\in\mathcal Q\}.
\]

Target expansion in \(\mathcal Q^\dagger\) is source restoration in
\(\mathcal Q\), and source restoration in \(\mathcal Q^\dagger\) is target
expansion in \(\mathcal Q\).  Its level-one relation is \(F^{\mathsf T}\),
and base-orderability is preserved under inversion of the bijection.
Applying the already proved \(|E|\)-bound to \(\mathcal Q^\dagger\) gives
\(|F|\geq5\).

Thus every rank-three obstruction has at least

\[
2+|E|+|F|\geq12
\]

states.  The reviewed note now includes this displayed dual construction,
so the proof is complete.

The independent exhaustion checked all \(2^{18}=262{,}144\) choices of
middle levels:

| Rank | Valid labeled systems | Non-base-orderable | Minimum size |
|---:|---:|---:|---:|
| 1 | 1 | 0 | — |
| 2 | 7 | 0 | — |
| 3 | 5,653 | 1,224 | 12 |

There are 162 labeled non-base-orderable systems of size 12.  This is a
finite cross-check of the symbolic proof, not a replacement for it.

## 7. The twelve-state \(K_{3,3}-e\) realization

The checker reconstructed \(K_{3,3}\) on parts
\(\{a,b,c\}\) and \(\{x,y,z\}\), deleting only \(ax\).

It verified:

- all 12 listed configurations are distinct three-sets and dominate;
- all 36 state/unoccupied-attack pairs appear exactly once in the table;
- every displayed source is occupied and adjacent to the attack;
- every attack is unoccupied;
- every successor is exactly the one-guard replacement and belongs to the
  12-state family;
- the induced abstract system satisfies both exchange axioms; and
- its \(E\cap F=\{ay,az,cx\}\) has no perfect matching.

Fresh exhaustive evaluators give

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,3).
\]

In particular, \(\{a,x\}\) dominates, neither vertex is universal, the
displayed eternal three-family supplies the upper bound on
\(\gamma^\infty\), and \(\alpha=3\) supplies the matching lower bound.  The
realization therefore refutes base-orderability under graph realizability
and full closure, but not under the conjecture equality
\(\gamma=\alpha\).

## 8. The `FCXfO` certificate

The independent graph6 decoder reproduced exactly

\[
\{03,06,14,15,16,24,25,26,46\}.
\]

It then verified:

- all 16 listed triples dominate;
- all 64 state/unoccupied-attack obligations appear exactly once;
- every response is a legal one-edge, one-guard move to a listed state;
- all 21 displayed undominated-pair witnesses are correct;
- the clique partition
  \(\{0,3\},\{1,5\},\{2,4,6\}\) is valid;
- the nonreciprocal exchange \(012-1+4=024\) is present while
  \(345-4+1=135\) is absent; and
- the displayed bijection \(0\mapsto3,1\mapsto5,2\mapsto4\) supplies all
  eight Boolean-subcube states.

Fresh exact evaluation gives

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3).
\]

The scope must remain precise: nonreciprocity is shown for the specified
16-state eternal family.  That family is a strict subfamily of the
18-state greatest eternal three-family, and state \(135\) belongs to the
greatest family.  Thus this witness does not refute reciprocity formulated
only for greatest-family lists.

## 9. Exact status boundary

| Status | Content |
|---|---|
| `PROVED` | independent-state forcing; adversarial expansion/restoration; monotone paths for every target ordering; ridge response covariance; closed-path response-incidence automorphism; rank \(\leq2\) base-orderability; rank-three lower bound |
| `CERTIFIED-FINITE` | abstract exhaustion through rank three; the 12-state obstruction; both literal response tables; both parameter certificates; `FCXfO` nonreciprocity and its displayed base ordering |
| `OBSERVED` | zero failures in the separate ordinary-set graph probe through order eight; this finite observation is not used in a universal proof |
| `OPEN` | whether every pair of independent triples in an arbitrary eternal three-family on a graph with \(\gamma=\alpha=3\) has at least one base ordering |

A publication-ready statement of the open problem is:

> Let \(G\) satisfy \(\gamma(G)=\alpha(G)=3\), let
> \(\mathcal F\subseteq\binom{V(G)}3\) be a one-guard eternal dominating
> family, and let \(S,T\in\mathcal F\) be independent.  Must there exist a
> bijection \(\phi:S-T\to T-S\) such that
> \[
> (S-U)\cup\phi(U)\in\mathcal F
> \quad\text{for every }U\subseteq S-T?
> \]

Proposition 1.1 settles \(|S-T|\leq2\); only disjoint triples remain.
A refutation requires one specified tuple \((G,\mathcal F,S,T)\) for which
every bijection fails.

Neither note proves the universal \(\gamma\)--\(\theta\) conjecture, and
neither note claims otherwise.
