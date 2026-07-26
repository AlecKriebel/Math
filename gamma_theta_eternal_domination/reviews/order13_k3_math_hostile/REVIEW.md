# Hostile audit of the order-13, parameter-three mathematics

**Audit date:** 2026-07-26  
**Solver use:** none  
**Campaign implementation imported:** none  
**Verdict:** `ACCEPT_MATHEMATICS_WITH_NONMATHEMATICAL_WORDING_GAPS`

## Frozen scope

This review applies to exactly these theorem-note bytes:

| file | bytes | SHA-256 |
|---|---:|---|
| `math/lemmas/order13_k3_synthesis_target.md` | 26,112 | `02c661edf61db8f4b4a5769972e726ce8c1c693e418c1b97b2293e68765e0f44` |
| `math/lemmas/order13_k3_hole11_exclusion.md` | 16,303 | `ee492ff314ac2df5f9e1e80982c9bd455dcbce30106d54083d0cd7a930627408` |

No theorem file was edited during this review.

The verdict accepts, relative to the synthesis note's explicitly listed
campaign inputs:

1. the exact four-template order-13, \(k=3\) cover;
2. the graph/CNF equivalence for each abstract template formula;
3. the direct near-spanning odd-hole obstruction for every odd
   \(\ell\geq5\);
4. the resulting order-13 \(C_{11}\) exclusion and reduction to the three
   live \(C_5,C_7,C_9\) templates; and
5. the claimed exact parameters of the two infinite canonical families.

This review does not re-prove SPGT or accepted campaign inputs C-014, C-017,
C-050, the parameter chain, or additivity.  It does not accept an UNSAT
claim, a solver runner, a certificate, the three remaining computational
branches, the order-13 \(k=4,5\) slices, or any novelty or priority claim.

## Synthesis-note audit

### Coverage and complement signs

The parameter collapse is used correctly:

\[
 \gamma=i=\alpha=\gamma^\infty=3,\qquad
 \omega(H)=3<\chi(H),\quad H=\overline G.
\]

The pair/common-neighbor dictionary has the correct complement direction.
A two-set fails to dominate \(G\) exactly when an external vertex is
nonadjacent in \(G\), and therefore adjacent in \(H\), to both members.  The
clean-room checker confirmed this equivalence on all \(32,768\) labeled
graphs of order six and all \(491,520\) graph/pair cases.

The SPGT case reduction has no missing odd antihole.  An induced odd
antihole of order \(2q+1\) has clique number \(q\).  Since
\(\omega(H)=3\), only orders five and seven remain.  The order-five
antihole is \(C_5\), while accepted C-017 removes the order-seven antihole.
Accepted C-014 makes the resulting odd hole hub-free.

For every rim edge, the pair dictionary supplies a common \(H\)-neighbor
outside the induced rim.  Zero outside vertices are therefore impossible.
One outside vertex would be adjacent to the endpoints of every rim edge and
hence to the entire rim, contradicting hub-freeness.  At order 13 this leaves
exactly the odd lengths \(5,7,9,11\).  The argument is a cover, not a
partition, and the note never assumes uniqueness.

The connectedness reduction is also sound relative to C-050.  Componentwise
nonnegative differences
\(\gamma^\infty(G_j)-\gamma(G_j)\) sum to zero, so equality holds in every
component; the positive total difference
\(\theta(G)-\gamma(G)\) then occurs in a component of order at most 12.

### Relabeling and symmetry

The normalization loses no graph:

1. choose a supplied hub-free odd hole;
2. orient and label its rim;
3. choose a rim edge \(01\);
4. choose one guaranteed external common \(H\)-neighbor and call it
   \(z=\ell\); and
5. label every remaining vertex arbitrarily.

This relabels the whole graph.  It assumes neither a graph automorphism nor
an incidence relation with an unrelated independent set.  The fixed
independent triple \(\{0,1,z\}\) is forced by the selected rim edge and its
common neighbor.  First-use color canonicalization quotients only the six
names of the three colors; it is not a vertex symmetry.

The maximum-independent-state lemma is applied with all hypotheses present.
Under \(\alpha=3\), every independent triple is maximum.  Repeated attacks on
its unoccupied vertices increase the number of guards on that triple because
guards already on it cannot move within an independent set.  Thus the
triangle-to-family clauses are sound for every target eternal family.

### CNF iff theorem

Every clause family has the stated quantifiers and sign:

- \(e_{uv}=1\) denotes an \(H\)-edge.
- No-\(K_4\) clauses give \(\omega(H)\leq3\), and
  \(\{0,1,z\}\) supplies equality.
- Witness implications plus one witness per pair assert exactly an external
  common \(H\)-neighbor; biconditionals are unnecessary.
- A selected state dominates because each unoccupied vertex has at least one
  negative \(e\)-literal to a guard, hence a \(G\)-edge.
- Move variables exist only for \(r\notin D\).
- A true move variable uses one guard \(u\), requires the negative
  \(e_{ur}\) literal, and selects exactly the successor \(D-u+r\).
- Multiple true move variables are alternative existential responses.  They
  do not move multiple guards.
- Domination clauses applied to every selected successor complete the
  closure condition.
- The cut clauses contain negative \(H\)-edge literals, so they characterize
  connectedness of \(G\), not of \(H\).

The checker exhaustively truth-tabled every local gadget and independently
tested the cut equivalence on all 1,024 graphs of order five.

The coloring bank is complete.  A proper coloring of the forced odd rim has
\(2^\ell-2\) choices.  Its adjacent vertices \(0,1\) force the unique third
color on \(z\).  The other \(12-\ell\) outside vertices are free before the
remaining graph edges are considered.  The forced triangle makes the
six-element color-name action free, giving

\[
 |B_\ell|=\frac{(2^\ell-2)3^{12-\ell}}6.
\]

An independent restricted-growth enumeration reproduced bank sizes
\(10{,}935, 5{,}103, 2{,}295, 1{,}023\).  It checked every retained row
against the rim and forced triangle.  For any graph extending the template,
every proper three-coloring has exactly one canonical row in this bank, and
the corresponding clause is false exactly for that proper coloring.

The independent clause census reproduced 9,802 variables and:

| branch | base clauses | bank clauses | full clauses |
|---|---:|---:|---:|
| `hole5` | 29,791 | 10,935 | 40,726 |
| `hole7` | 29,800 | 5,103 | 34,903 |
| `hole9` | 29,813 | 2,295 | 32,108 |
| `hole11` | 29,830 | 1,023 | 30,853 |

In the forward direction, a target graph, one witness per pair, and one legal
response per selected state/attack satisfy every clause.  In the reverse
direction, the witness clauses force \(\gamma\geq3\); the nonempty closed
dominating family gives \(\gamma^\infty\leq3\); the forced triangle and
no-\(K_4\) clauses give \(\alpha=3\); and the full bank gives
\(\theta>3\).  There is no inference from well-coveredness and no circular
use of the conjecture.

## Near-spanning-hole theorem audit

### Classification of the outside vertices

Let \(X,Y\) be the rim nonneighbors in \(H\) of the two outside vertices.
Hub-freeness makes both nonempty.  If an index belonged to both, an incident
rim edge would have no external common \(H\)-neighbor.  Thus
\(X\cap Y=\varnothing\).

For \(i\in X,j\in Y\), neither outsider can witness the pair
\(\{r_i,r_j\}\).  Their common neighbor must lie on the induced rim.  Two
distinct vertices of \(C_\ell\), \(\ell\geq5\), have a common rim neighbor
exactly at cyclic distance two.  Hence every cross distance is two.

After putting \(0\in X\), this gives
\(Y\subseteq\{-2,2\}\).  If both values occur, their distance-two spheres
intersect only at zero.  If only \(2\) occurs, then
\(\{0\}\subseteq X\subseteq\{0,4\}\), and the two-element choice becomes the
former case after swapping outsiders and rotating.  Therefore precisely the
two stated patterns remain under the full dihedral group and outsider swap:

\[
 (\{0\},\{2\}),\qquad(\{0\},\{-2,2\}).
\]

There is no hidden small-modulus exception at \(\ell=5\).  A clean-room
enumeration checked every odd length from 5 through 51.  At every length it
found \(4\ell\) ordered set pairs and exactly two
\(D_{2\ell}\)-times-swap orbits.  The all-orders proof is finite without
enumeration: choosing one member on either nonempty side restricts the other
side to a two-element distance-two sphere.

### The \(xy\) edge and all exceptional attacks

Under the contradiction hypothesis,
\(\alpha(G)\leq\gamma^\infty(G)=3\).  If \(xy\in E(H)\), any rim edge in the
common \(H\)-neighborhood of \(x,y\) gives a \(K_4\) in \(H\).  For
\(\ell\geq7\), and for Pattern I at \(\ell=5\), that common rim set is larger
than \(\alpha(C_\ell)\), so it contains such an edge.  The sole uncovered
case is \(\ell=5\), Pattern II.  Its displayed root is an independent
triple, and the attack on \(r_4\) has no dominating one-guard successor.
Thus all remaining cases correctly take \(xy\in E(G)\).

Every small attack tree was reconstructed from the definition with the
following exact branch counts:

| case | first dominating successors | terminal branches |
|---|---:|---:|
| \(\ell=5\), Pattern II, \(xy\in H\) exception | 0 | 1 |
| \(\ell=5\), Pattern I, \(xy\in G\) | 1 | 1 |
| \(\ell=5\), Pattern II, \(xy\in G\) | 2 | 2 |
| \(\ell=7\), Pattern I, \(xy\in G\) | 2 | 2 |
| \(\ell=7\), Pattern II, \(xy\in G\) | 2 | 2 |

All roots are independent dominating triples.  All attacks are unoccupied.
Every enumerated response moves exactly one guard along a \(G\)-edge, and
every omitted response either has no guard edge or leaves the explicit
witness in the note undominated.

### Uniform attack for every odd \(\ell\geq9\)

The uniform indices are valid, including the endpoint \(\ell=9\).
The root \(\{r_4,r_5,x\}\) is an \(H\)-triangle and hence a forced maximum
independent state.  After attack \(r_0\), the move by \(x\) leaves \(y\)
undominated.  The two remaining dominating successors are \(B\) and \(S_5\).
Attack \(r_2\) kills \(B\).

For odd \(5\leq j<\ell-4\), attack \(r_{j+2}\) at \(S_j\).  The guard at
\(x\) has no \(G\)-edge to the attacked rim vertex.  Moving \(r_0\) leaves
\(r_{j+1}\) undominated.  Therefore eternal closure forces
\(S_{j+2}\).  This reaches \(S_{\ell-4}\), where attack \(r_{\ell-2}\)
leaves respectively \(r_{\ell-3}\) or \(r_{\ell-1}\) undominated under the
only two rim-guard moves; \(x\) still cannot move.

For odd \(\ell\geq9\), the induction source is at most \(\ell-6\), its
attack is at most \(\ell-4\), and the local triples
\((j,j+1,j+2)\) do not wrap through zero.  The terminal residues
\(\ell-4,\ell-3,\ell-2,\ell-1,0\) are distinct.  At \(\ell=9\),
\(S_5=S_{\ell-4}\), so the induction is empty exactly as stated.

As an indexing regression, the checker verified 9,894 named transitions for
both patterns and every odd \(\ell\) from 9 through 201.  The written residue
argument, not that finite range, proves the universal statement.

The corollaries then follow without an additional assumption: a spanning
hole lacks the common neighbor required for a rim edge; one outside vertex
would be a hub; and exactly two outside vertices are excluded by the theorem.
Thus every such equality graph has at least three vertices outside every
induced odd hole, and the order-13 \(C_{11}\) branch is empty.

## Infinite-family parameter audit

The two families use exactly the two classified patterns with
\(xy\notin E(H)\).  The parameter proof is complete:

- Every \(H\)-pair has an external common neighbor.  For \(y,r_i\) in the
  second family, both rim neighbors could be missed only if
  \(4\equiv\pm2\pmod\ell\), impossible for odd \(\ell\geq5\).
  Hence \(\gamma(G)\geq3\).
- \(H\) has no \(K_4\), while \(x\) and any rim edge avoiding \(r_0\) form an
  \(H\)-triangle.  Thus \(\alpha(G)=3\).
- A maximum independent triple is maximal and dominates, giving
  \(\gamma(G)\leq3\); the parameter chain gives \(i(G)=3\).
- In a hypothetical three-coloring of \(H\), the even-vertex path
  \(r_1,\ldots,r_{\ell-1}\) alternates the two colors different from the
  color of \(x\).  Its endpoints differ, forcing \(r_0\) to have the color
  of \(x\).  Vertex \(y\) sees that color and both alternating colors even
  after its one or two missed path vertices.  Thus \(\chi(H)\geq4\).
- A proper three-coloring of the odd rim plus a shared fourth color on the
  nonadjacent \(x,y\) proves \(\chi(H)\leq4\).
- The near-spanning theorem gives \(\gamma^\infty(G)\geq4\), and the
  clique-cover strategy gives \(\gamma^\infty(G)\leq\theta(G)=4\).

Independent exact checks reproduced
\(\gamma=i=\alpha=3\) and \(\theta=4\) for both families at every odd length
5 through 41.  A separate greatest-fixed-point computation from the
one-guard definition found no eternal triple family and a nonempty eternal
four-family for both constructions at every odd length 5 through 15.  The
order-13 Graph6 strings were reproduced exactly:

```text
LUzvvz}~r~O?G@
LUzvvz}~r~O?GD
```

These finite checks are regressions; the displayed all-orders proof is the
theorem.  The local source scan found no exact match in the four retained
primary-source TeX files, but that limited scan is not a novelty audit and
supports no novelty claim.

## Fail-closed mutations

Twelve deliberate mutations were rejected:

- using \(G\), rather than \(H\), in the pair dictionary;
- reversing the connected-cut complement sign;
- adding an occupied attack;
- replacing \(D-u+r\) by a multi-guard successor;
- omitting Pattern II;
- changing cross distance two to one;
- dropping the second \(\ell=5\), Pattern-II branch;
- applying the uniform proof at \(\ell=7\);
- making \(y\) also miss \(r_0\) in a canonical family;
- changing \(xy\) to an \(H\)-edge in a canonical family;
- changing the coloring-bank exponent \(12-\ell\); and
- transposing Graph6 bit order.

## Nonmathematical wording gaps

No wording issue below affects a proof.

1. Synthesis-note lines 729--732 say “No implementation theorem yet.”  That
   status is stale because a separately frozen A/B constructor acceptance
   now exists.  The abstract CNF theorem itself remains correct and
   implementation-independent.
2. Hole-note lines 503--505 mention two exact evaluator checks without
   artifact paths or hashes.  Theorem 4 does not rely on this sentence, and
   the present clean-room checker independently reproduces the parameters.
3. The pre-audit status paragraphs in both notes still request the hostile
   review now supplied by this artifact.

These should be repaired as documentation-only edits, followed by a narrow
hash-binding addendum.  They do not justify weakening the verdict on the
frozen mathematical text.

## Reproduction

From the campaign directory:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONWARNINGS=error \
  python3 -W error reviews/order13_k3_math_hostile/audit.py |
  cmp - reviews/order13_k3_math_hostile/evidence.json
```

The replay uses the Python standard library, invokes no campaign module or
solver, and takes about five seconds on the campaign MacBook.

| artifact | bytes | SHA-256 |
|---|---:|---|
| `reviews/order13_k3_math_hostile/audit.py` | 47,177 | `35d405424127c1a28742ade277fd5c5add0a109749ccc51ab6d622740371241b` |
| `reviews/order13_k3_math_hostile/evidence.json` | 20,660 | `8c1f5b3fe4511a4d19efdc224a7ea6b10b38eac06275ddce615bd73949d22af1` |
