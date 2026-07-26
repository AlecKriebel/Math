# Hostile review: order-12, parameter-four structural split

**Review date:** 2026-07-26  
**Source reviewed:** `math/lemmas/order12_k4_structural_split.md`  
**Source SHA-256:** `a28a544325549972191f40e087131316f5cd1a52b4f27d9a9ea617a31a4f5e5f`  
**Overall verdict:** `ACCEPT_PROVED_RELATIVE_TO_STATED_ACCEPTED_INPUTS`

I found no mathematical defect in P3, Lemmas 1--2, Theorem 3, the
one-guard \(C_9\) cross-check, Corollary 4, or the three-template conclusion
of Theorem 5.  The result is exactly a structural reduction: it does not
exclude the full connected \((n,k)=(12,4)\) slice and does not resolve the
\(\gamma\)--\(\theta\) conjecture.

The verdict is relative to the explicitly cited accepted inputs: the
parameter chain, component additivity, induced-subgraph monotonicity for the
one-guard model, the two cycle/anticycle eternal-domination values, and the
Strong Perfect Graph Theorem.  I rechecked every use of those inputs in this
note, but this review does not replace their existing source reviews.

## 1. Complement and quantifier audit

Put \(H=\overline G\).  If \(\gamma(G)=4\), every three-set
\(A\subseteq V(G)\) fails to dominate \(G\).  Thus there is a vertex
\(x\in V(G)\setminus A\) with no \(G\)-neighbor in \(A\).  (An undominated
vertex cannot belong to the dominating set itself because closed
neighborhoods are used.)  Complementing on distinct vertices gives

\[
  \forall A\in{V(H)\choose3}\ \exists x\in V(H)\setminus A\
  \forall a\in A:\ xa\in E(H),
\]

which is exactly P3.  The complement sign and the
\(\forall A\,\exists x\,\forall a\) order are correct.

The other parameter translation is also correct:

\[
  \omega(H)=\alpha(G)=4,\qquad
  \chi(H)=\theta(G)>4.
\]

No step confuses a clique partition of \(G\) with a coloring of \(G\);
the coloring is always in \(H=\overline G\).

## 2. Lemmas 1 and 2

### Lemma 1

For an induced rim \(C\) of length at least five, a rim vertex has exactly
two rim neighbors.  It therefore cannot be adjacent to all three distinct
vertices of a rim triple.  P3 supplies a common neighbor outside the triple,
and the preceding observation forces that witness outside the entire rim.
This proves the claimed quantifiers for **every** rim triple.  Inducedness is
used correctly here; with chords, the statement would not follow.

### Lemma 2

Assume \(1\leq |X|\leq3\) and no \(x\in X\) is a hub.  Choosing one missed
rim vertex \(t_x\) for each \(x\) produces a set of at most three rim
vertices.  Repetitions among the \(t_x\)'s cause no problem: the resulting
set can be extended to a three-set \(T\) because the rim has at least five
vertices.  Every \(x\) still misses its own selected member of \(T\).
Lemma 1, however, says some member of \(X\) contains all of \(T\) in its
neighborhood.  The contradiction is exact.  In particular, the proof does
not silently assume that the three selected missed vertices are distinct.

## 3. Theorem 3, case by case

Let \(r=|V(H)\setminus V(C)|\).

| Case | Hostile check | Decision |
|---|---|---|
| \(r=0\) | Lemma 1 requires an outside witness for any rim triple, but the outside set is empty. | `ACCEPT` |
| \(r=1\) | Lemma 2 makes the sole outside vertex complete in \(H\) to the entire rim.  It is then universal in \(H\), hence isolated in \(G\), contradicting connectedness. | `ACCEPT` |
| \(r=2\) | Take a hub \(a\) and the other vertex \(b\).  If \(ab\in E(H)\), then \(a\) is isolated in \(G\), so connectedness forces \(ab\notin E(H)\).  For a rim edge \(uv\), no rim vertex is adjacent in the induced cycle to both \(u\) and \(v\).  In P3 for \(\{a,u,v\}\), the only remaining candidate is \(b\), which fails on \(a\). | `ACCEPT` |
| \(r=3\) | Take a hub \(a\).  Connectedness forces an \(H\)-nonneighbor \(c\) of \(a\) among the other outside vertices; call the third vertex \(b\).  P3 on \(\{a,u,v\}\), for every rim edge \(uv\), has only \(b\) as a possible witness.  Hence \(ab\in E(H)\) and \(b\) is complete to the rim.  Thus \(b\)'s only possible \(G\)-neighbor is \(c\), so connectedness forces \(bc\notin E(H)\).  P3 on \(\{c,u,v\}\) then has no witness: \(a\) and \(b\) both miss \(c\) in \(H\), while no rim vertex sees both endpoints of the rim edge. | `ACCEPT` |

At each P3 invocation the proposed witness is required to lie outside the
attacked triple.  The two endpoints \(u,v\) and the named outside vertex in
the triple are therefore never accidentally counted as witnesses.

Connectedness is genuinely necessary for the theorem as stated.  For
example, both

\[
  H=K_2\vee C_5
  \quad\text{and}\quad
  H=K_3\vee C_5
\]

satisfy P3, but their complements have isolated vertices and are
disconnected.  These boundary examples also confirm that the proof is using
connectedness at the right complement sign, rather than merely adding a
redundant hypothesis.

## 4. Independent one-guard check at \(C_9\)

In the \(r=3\) proof, once \(a\) and \(b\) are forced to be adjacent hubs,
the induced graph on \(V(C)\cup\{a,b\}\) is indeed

\[
  G[V(C)\cup\{a,b\}]
  =2K_1\mathbin{\dot\cup}\overline C.
\]

Both \(a\) and \(b\) are isolated inside this induced subgraph of \(G\):
each is \(H\)-adjacent to the other and to every rim vertex.  For \(C=C_9\),
one-guard component additivity gives

\[
  \gamma^\infty(2K_1\dot\cup\overline{C_9})
  =1+1+3=5.
\]

Induced-subgraph monotonicity has the correct direction,
\(\gamma^\infty(G)\geq5\), contradicting the target value four.  A
clean-room greatest-fixed-point evaluator, using attacks only at unoccupied
vertices and exactly one edge move per response, independently returned
\(\gamma^\infty(\overline{C_9})=3\) and
\(\gamma^\infty(2K_1\dot\cup\overline{C_9})=5\).

This cross-check is logically optional, as the note says; Theorem 3 already
discharges the \(r=3\) case using P3 and connectedness.

## 5. SPGT and the exact three templates

Because \(\omega(H)=4<\chi(H)\), \(H\) is not perfect.  SPGT therefore
supplies an induced odd hole or odd antihole.

For odd holes in a 12-vertex graph, the possible lengths are
\(5,7,9,11\).  Theorem 3 excludes lengths 9 and 11 because they leave,
respectively, three and one vertices outside.  Hence only \(C_5\) and
\(C_7\) remain.

For an odd antihole \(\overline{C_{2q+1}}\), its clique number is
\(\alpha(C_{2q+1})=q\).  Since it is induced in a graph with
\(\omega(H)=4\), one has \(q\leq4\), so only lengths \(5,7,9\) occur.
The length-five antihole is \(C_5\).  A length-nine antihole in \(H\)
induces \(C_9\) in \(G\), and

\[
  \gamma^\infty(C_9)=5
  \leq\gamma^\infty(G)
\]

contradicts \(\gamma^\infty(G)=4\).  The sole remaining antihole template is
\(\overline{C_7}\).  Thus the list

\[
  C_5,\quad C_7,\quad\overline{C_7}
\]

is exhaustive.  It is not asserted that these templates are sufficient for
a counterexample.

The proposed search partition is also sound.  Adding “no induced \(C_5\)”
to the \(C_7\) case and excluding both earlier holes from the
\(\overline{C_7}\) case makes the cases disjoint without changing coverage.
The warning that an independently anchored \(K_4\) and a labeled template
cannot both be fixed without an orbit-complete placement argument is
correct and important.

## 6. Clean-room finite probe

The independent standard-library probe is
`reviews/order12_k4_structural_split_hostile_probe.py`, SHA-256
`2d36433e708c78b0cc9602daf6479417f12a478d14ead116ef551ff47c6e2eb2`.
Its canonical output is
`reviews/order12_k4_structural_split_hostile_probe.log`.

It exhausts every graph formed from a fixed induced \(C_5\) and
\(r=0,1,2,3\) outside vertices, including every rim--outside and
outside--outside edge.  Of the \(262{,}144\) graphs in the largest case,
274 satisfy P3, all 274 contain a hub, and none has connected complement.
Across all four values of \(r\), no P3 graph has connected complement.

The same probe directly evaluates the one-guard game by greatest-fixed-point
deletion.  It returns

\[
\begin{array}{c|rrrr}
n&5&7&9&11\\ \hline
\gamma^\infty(C_n)&3&4&5&6\\
\gamma^\infty(\overline{C_n})&3&3&3&3.
\end{array}
\]

These bounded computations are sign and model-mutation checks, not the
proof of the general theorem.  The written arguments above establish the
unbounded cycle-length statement.

## 7. Final decisions

| Item | Verdict |
|---|---|
| P3 derivation and complement signs | `ACCEPT` |
| Lemma 1 | `ACCEPT` |
| Lemma 2 | `ACCEPT` |
| Theorem 3, all \(r=0,1,2,3\) cases | `ACCEPT` |
| \(C_9\) one-guard cross-check | `ACCEPT` |
| Corollary 4 | `ACCEPT` |
| SPGT antihole bounds | `ACCEPT` |
| Theorem 5 three-template conclusion | `ACCEPT` |
| Claim boundary and search consequence | `ACCEPT` |

**Final verdict:** `ACCEPT_PROVED_RELATIVE_TO_STATED_ACCEPTED_INPUTS`.
