# Hostile review: greatest-family complementary-exchange reciprocity

## Verdict

**PASS on the reviewed bytes.**

The checkpoint draws the correct boundary:

- pairwise reciprocity under
  \(\gamma=\alpha=\gamma^\infty=k\) remains **OPEN**;
- Proposition 3.1 is a valid conditional implication from that open
  reciprocity statement to symmetry of the C-108 active-response relation;
- `GEjbug` is an exact greatest-family countermodel after the hypothesis
  \(\gamma=\alpha\) is removed; and
- none of the extension, random, or SAT experiments is promoted into a
  universal or certified-frontier theorem.

No occupied-vertex attack, multiple-guard move, static/family substitution,
graph/complement reversal, or greatest/arbitrary-family substitution was
found.  The universal gamma--theta conjecture is not resolved by this
checkpoint.

No correction is required.  One dependency deserves an explicit reading:
the sentence saying C-064 supplies a perfect matching uses the full
target-expansion **and source-restoration** theorem (equivalently, the
accepted family-response Hall lemma), not merely the existence of one
monotone path.

## Frozen objects

| Artifact | SHA-256 |
|---|---|
| candidate `NOTE.md` | `4e195ff3ba8375a0319efd7a8362c5c09bc7fe9ec1970460d57721911ee1ef9f` |
| candidate `MANIFEST.json` | `3fcd40c6589b4faa525ee8337d798a8ac144d7e40d00eeaf8c375a71585a4b2e` |
| candidate exact result | `21c7aeedc2659714e0e63fe15b33c0983988d35ac155ad5ba09e824c2d875d33` |
| hostile `independent_check.py` | `d7ed0fa04c3de40285b945ef382f9fb29ec82d29384be87d0cf8e554b6121e7d` |
| hostile `independent_result.json` | `ddd0271c4965cd45cfeeb04d3d4ea7c483a01faa914ef8823c8da837aba523a6` |

The hostile checker imports no campaign evaluator, candidate verifier,
candidate search module, NetworkX, or SAT solver.  For the graph-specific
kernel it builds the colored obligations explicitly and removes losing
states through reverse dependency counts.  Its extension replay uses a
second compact implementation over the complete stated 17-bit mask range.

## 1. Exchange notions are separated correctly

For independent \(k\)-sets \(S,T\), put

\[
A=S-T,\qquad B=T-S.
\]

The candidate defines

\[
E_{S,T}
=\{(u,x)\in A\times B:S-u+x\in\mathcal K\}
\]

and, on the same ordered bipartition,

\[
E^\leftarrow_{S,T}
=\{(u,x)\in A\times B:T-x+u\in\mathcal K\}.
\]

The distinctions in the note are exact.

1. Pairwise reciprocity is equality of these entire relations.
2. A mutual matching asks only for one perfect matching in their
   intersection.
3. A family base ordering is a single bijection
   \(\phi:A\to B\) for which every Boolean-cube state
   \((S-U)\cup\phi(U)\) lies in the family.
4. Matroid exchange would require membership in a collection of
   independent bases.  The mixed eternal configurations here may contain
   graph edges, so neither reciprocity nor a family cube is a matroid
   assertion.

A family base ordering gives a mutual matching: singleton subsets give the
forward exchanges, and the complementary subsets \(A-\{u\}\) give the
reverse exchanges.  When \(|A|\le3\), those two levels, together with the
endpoint levels, exhaust the Boolean cube.  Thus mutual matching and family
base ordering coincide in those ranks.  At rank at least four, mutual
matching data alone do not specify the intermediate levels.

Pairwise reciprocity is stronger than mutual matching in the present
eternal-family setting because the family-response Hall theorem supplies a
perfect matching in \(E_{S,T}\).  To see the dependency directly, attack an
independent subset \(Z\subseteq B\) from \(S\), then use source restoration
until only one omitted source remains.  This proves Hall for the initial
family-response lists.  Since members of \(S\cap T\) are nonadjacent in
\(G\) to every member of \(B\), the matching uses only \(A\).  Reciprocity
then makes it mutual.

The note also correctly keeps the arbitrary-family failure C-065 separate
from the proposed greatest-family statement.  A proper eternal family can
omit a reverse state even when the greatest family contains it.

## 2. Conditional active-edge symmetry

The proof of Proposition 3.1 uses every necessary hypothesis and no more.
Assume

\[
\gamma(G)=\alpha(G)=\gamma^\infty(G)=k
\]

and that the proposed greatest-family reciprocity statement holds for
\(G\).

If \(u\triangleright x\), a maximum independent state \(S\) containing
\(u\) has the legal retained successor \(S-u+x\).  In particular
\(ux\in E(G)\), so \(x\notin S\).

The equality \(\gamma=\alpha=k\) makes \(G\) well-covered: every maximal
independent set is dominating, hence has size at least \(\gamma=k\), and
has size at most \(\alpha=k\).  Extending \(\{x\}\) to a maximal
independent set therefore gives a maximum independent \(k\)-set \(T\).
The edge \(ux\) ensures \(u\notin T\).  Maximum-independent-state forcing
puts both \(S\) and \(T\) in every optimal eternal family, including the
greatest family.

Applying the proposed reciprocity statement to \(S,T,u,x\) gives

\[
T-x+u\in\mathcal K.
\]

This is exactly the legal response \(x\to u\) from \(T\), proving
\(x\triangleright u\).  Interchanging the roles proves the converse.
C-108 then legitimately transports each orientation across all maximum
independent states containing its responder.

The fixed-state identity

\[
u\in L_S^\mathcal K(x)
\quad\Longleftrightarrow\quad
x\triangleright u
\]

uses the just-proved symmetry; without reciprocity its left side would
define \(u\triangleright x\), not the reversed orientation.  The candidate
does not skip this point.

The full-list consequence is also valid.  If
\(S=\{s_1,s_2,s_3\}\) has all three retained responses at \(x\), then
each \(s_i\) is adjacent to \(x\) in \(G\).  A maximum independent triple
\(T=\{x,b,c\}\) therefore contains no \(s_i\), and reciprocity gives all
three states \(T-x+s_i\).  Combining family-response Hall with reciprocity
gives a mutual matching between disjoint triples; at rank three this yields
one complete eight-state family cube.

None of these conditional consequences synchronizes responder colors
across different ridge components.  The note correctly refuses to infer
the remaining C-108 color intersection, the complete \(k=3\) theorem, or
the universal conjecture.

## 3. Exact `GEjbug` boundary

The hostile graph6 decoder round-trips

```text
GEjbug
```

and reconstructs the stated 15 edges on eight vertices.  The graph is
connected.  Direct subset and clique-partition searches give

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,3).
\]

In particular:

- `06` is an independent dominating pair, proving
  \(\gamma=i=2\);
- the only maximum independent triples are `012` and `345`;
- the clique partition
  \[
  037,\qquad15,\qquad246
  \]
  proves \(\theta\le3\), while \(\alpha=3\) proves the reverse bound; and
- the one- and two-guard greatest kernels are empty, while the greatest
  triple-kernel has 41 states.

The independently reconstructed greatest triple-kernel has canonical hash

```text
59b74f7c52c11f9672407c5c05d6ab9a0131904787742e3715c68e1b39c9eace
```

and exactly 205 unoccupied-attack obligations and 296 retained legal
one-edge responses.  Its literal state set matches the candidate's
41-state list.

For

\[
S=012,\quad T=345,\quad u=0,\quad x=4,
\]

the edge `04` is present and `124` belongs to the greatest kernel, but
`035` does not.  The latter state does dominate, so the asymmetry is
genuinely dynamic.  Its attack at the unoccupied vertex 7 has all three
possible movers and no dominating successor:

| mover | successor | undominated vertex |
|---:|---|---:|
| 0 | `357` | 4 |
| 3 | `057` | 6 |
| 5 | `037` | 2 |

Thus `035` cannot belong to any eternal triple-family.  The selected pair
still has two mutual perfect matchings and two family base-ordering cubes,
so this graph does not accidentally refute either weaker property.

This proves only that greatestness plus
\(\alpha=\gamma^\infty=3\) is insufficient.  Because
\(\gamma=2<3\), it neither refutes the equality reciprocity conjecture nor
the gamma--theta conjecture.

## 4. Delimited extension replay

The hostile implementation independently enumerated all

\[
2^{17}=131{,}072
\]

labeled graphs obtained by fixing `GEjbug` on vertices \(0,\ldots,7\) and
freely choosing the sixteen old--new edges plus edge `89`.  It reproduced
the candidate counts exactly:

| filter/result | count |
|---|---:|
| extension masks | 131,072 |
| \(\alpha=3\) | 65,410 |
| \(\gamma=\alpha=3\) | 210 |
| \(\gamma=\alpha=\gamma^\infty=3\) | 36 |
| independent-state pairs tested | 3,136 |
| reciprocity violations | 0 |

The coverage statement is exact only for this fixed induced-extension
class.  Old-edge edits, substitutions, other host graphs, and arbitrary
order-ten graphs are outside it.  Retaining the candidate's `OBSERVED`
classification is therefore conservative and correct; this review does
not turn the census into a universal reciprocity theorem or a graph-order
frontier.

## 5. Random and SAT evidence

The two random JSON records have valid internal hashes and explicitly set
`coverage_claim` to false.  Their arithmetic totals are 32,141 equality
graphs and 20,382,718 independent-state pairs.  Every sampled graph comes
with a displayed partition into three \(G\)-cliques, so after the equality
filter it already has \(\theta=3\).  As the candidate says, this is a
falsification stress test that cannot distinguish the proposed
reciprocity theorem from behavior restricted to already colorable graphs.
Its `EXPLORATORY` status is mandatory and is preserved.

The SAT source has the advertised semantics:

- `012` and `345` are independent;
- every four-set contains an edge, so \(\alpha\le3\);
- every pair has an external common nonneighbor, so \(\gamma\ge3\);
- the independent triple `012` is maximum and hence dominating, giving
  \(\gamma=3\);
- level zero is exactly the set of dominating triples;
- each next level retains precisely the states that were live and answer
  every unoccupied attack by one adjacent guard into a live predecessor
  level; and
- \(\binom n3\) rounds suffice for stabilization of a descending chain on
  \(\binom n3\) states.

The formula fixes disjoint endpoint triples and one labeled exchange.
That restricted scope is disclosed.  No DRAT/LRAT or other proof log for
the reported UNSAT instances is present.  The source and the reported
solver outcomes are therefore correctly classified as `EXPLORATORY`; no
negative finite theorem is available from them.

## 6. Manifest and replay audit

All 13 files listed in the candidate manifest have the declared byte
counts and SHA-256 hashes.  The candidate's exact result and replay log are
byte-identical.  The graph6 hash, greatest-family serialization hash, and
the internal hashes of the extension and random JSON records all verify.

The decisive graph-specific facts are now supported by an implementation
that does not share the candidate's transition core.  The extension census
also has an independent replay, while its deliberately weaker
classification remains unchanged.
