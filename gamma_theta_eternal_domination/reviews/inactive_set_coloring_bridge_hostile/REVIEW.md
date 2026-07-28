# Hostile review: the inactive-set coloring bridge at \(k=3\)

## Verdict

**PASS.**

The frozen source note proves its component and global active-color
identities, the exact common-responder-color target, and the
triangle-freeness of the inactive induced complement.  Its 11-vertex
deletion graph and 12-vertex static boundary control also have exactly the
claimed data.

The boundary is essential.  The 12-vertex graph has

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,4,4),
\]

so it is not a counterexample and supplies no eternal family of triples.  It
only shows that the deletion equality, static full target, one-target-step
domination checks, facet hitting, and ridge covariance do not imply the
desired coloring without a genuinely multi-step closure argument.  The
source states this limitation correctly.

## Frozen artifacts

| artifact | SHA-256 |
|---|---|
| `math/working/inactive_set_coloring_bridge/NOTE.md` | `18847a21646b5692dc585cbe1aa8f4869ae47e39105c0f43f103b497f9e5574f` |
| `math/working/inactive_set_coloring_bridge/verify_control.py` | `64923c2d09d3312c98d9961bf33dc05e5363488898abab7cca21d496a7a6b521` |
| `math/working/inactive_set_coloring_bridge/control_result.json` | `1a891b0e65fd8ef363007869ad3797191b8fca96912e11a1b41ab02d82fd2faa` |
| `reviews/inactive_set_coloring_bridge_hostile/independent_check.py` | `b62d8b0ac5595ad34258e1b445a49a66f7acfb8a3f8a607c5c5f4958d05085ec` |

The two randomized searches reported in Section 5 are explicitly labeled
`OBSERVED`.  This audit makes no finite-exhaustion claim for them.

## 1. Vertex-star propagation

Let \(T,T'\) be maximum independent triples avoiding \(x\), both containing
\(v\), and suppose \(v\in L_T(x)\).

If

\[
T=\{v,u,p\},\qquad T'=\{v,u,q\},
\]

then \(\{u,p,x\}\) is retained.  At the unoccupied attack \(q\), the guard
\(u\) cannot move because \(uq\notin E(G)\).  Moving \(x\) would produce
\(\{u,p,q\}\), which misses \(v\), so that successor cannot belong to an
eternal family.  The only remaining possible response is \(p\to q\), and
closure retains \(\{u,q,x\}\).

If the triples share only \(v\), write

\[
T=\{v,a,b\},\qquad T'=\{v,p,q\}.
\]

From \(\{a,b,x\}\), attack \(p\).  Moving \(x\) again creates a set missing
\(v\), so one of \(a,b\) must respond; relabel it \(a\), obtaining
\(\{b,p,x\}\).  Now attack \(q\).  The guard \(p\) misses \(q\), and moving
\(x\) creates \(\{b,p,q\}\), which misses \(v\).  Thus \(b\to q\) is forced
and \(\{p,q,x\}\) is retained.  Reversing the argument gives the converse.

All attacks are at unoccupied vertices and every retained transition moves
exactly one guard.  The proof does not require the family to be greatest.
It follows that membership of a vertex in a target-response list is
independent of which maximum independent triple containing that vertex was
chosen.

## 2. Ridge covariance and the exact identities

For adjacent ridge facets

\[
T=\{u,v,p\},\qquad T'=\{u,v,q\},
\]

vertex-star propagation fixes the active status of \(u,v\).  The exchanged
roles also have the same status.  Indeed,

\[
T-p+x=T'-q+x=\{u,v,x\}.
\]

If this state is absent from the family, neither role is active.  If it is
present, domination of the omitted vertices \(p\) and \(q\) forces both
\(px,qx\in E(G)\), since \(u,v\) miss both.  Thus both roles are active.
Because every triangle is rainbow in a proper three-coloring of \(H'\), the
exchanged vertices have the same color.  Hence
\(\kappa(T\cap A_x)\) is constant throughout each ridge component.

For a ridge component \(C\), every facet has exactly one vertex of each
color.  A color occurs in the constant active-color set precisely when every
support vertex of that color is active.  This proves

\[
A_C^\kappa
=\{1,2,3\}\setminus
\kappa\!\left(R\cap\operatorname{supp}(C)\right).
\]

The deletion hypothesis gives \(i(G-x)=\alpha(G-x)=3\).  Every vertex
extends to a maximal independent set, and every such set consequently has
size three.  The ridge-component supports therefore cover all of \(V(H')\).
Intersecting the component identities is now exactly De Morgan's law and
gives

\[
\bigcap_C A_C^\kappa
=\{1,2,3\}\setminus\kappa(R).
\]

There is no hidden assumption that the ridge graph is connected.

Thus a common responder color exists exactly when the chosen deletion
coloring uses at most two colors on \(R\).  If \(w\notin\kappa(R)\), every
\(w\)-colored vertex is active and hence adjacent to \(x\) in \(G\); assigning
color \(w\) to \(x\) is therefore a valid extension to \(\overline G\).
The note correctly presents this as a sufficient active-set mechanism, not
as the only possible coloring of every positive graph.

Finally, an \(H'[R]\)-triangle would itself be a maximum independent triple
of \(G-x\), but every such triple has a nonempty response list at \(x\).
Therefore \(H'[R]\) is triangle-free.  A successful target coloring would
make it bipartite, but triangle-freeness does not imply that target.

## 3. Independent finite-control audit

The clean-room checker imports no source or campaign module.  It decodes both
graph6 strings directly and separately parses the complement edge word.  The
two constructions agree:

```text
G'  JUZeppVvS^_   11 vertices, 33 edges
G   KUZeppVvS^_~  12 vertices, 39 edges
```

It independently verifies the eight deletion-complement triangles

```text
017 048 12A 23A 269 289 345 567
```

and the six ridge components

```text
{017} {048} {12A,23A} {269,289} {345} {567}.
```

Their supports cover all 11 deletion vertices.  The induced inactive graph
is exactly the chordless five-cycle

```text
01 12 23 34 40.
```

All 12 labeled proper three-colorings of \(H'\) were enumerated.  For every
one, the checker verifies the component identity above, its global
intersection, and the fact that \(R\) uses all three colors.  It also checks
all 55 deletion pairs and all 66 full-graph pairs have a common complement
neighbor.

The prescribed static response lists at \(x=11\) are reproduced exactly:

```text
017:7  048:8  12A:A  23A:A
269:69  289:89  345:5  567:567
```

Every listed move is along a \(G\)-edge and every successor dominates the
12-vertex graph.  The state \(567\) has the claimed full static list.

Exhaustive subset and coloring checks independently give

\[
\begin{array}{c|ccccc}
 &\gamma&i&\alpha&\gamma^\infty&\theta\\ \hline
G'&3&3&3&3&3\\
G &3&3&3&4&4.
\end{array}
\]

There are eight maximal independent sets in \(G'\) and 13 in \(G\), all of
size three, so both graphs are well-covered.

An explicitly built colored configuration digraph gives:

```text
deletion k=3 greatest family: 72 states
full k=3 greatest family:      0 states
full k=4 greatest family:    427 states
```

The full triple kernel loses all 122 initially dominating configurations in
three simultaneous rounds.  In particular, each of the 12 statically listed
target successors is deleted in round one or two.  This directly confirms
the claimed boundary: the target attack is locally answerable, but those
answers cannot survive future attacks.

The independently reconstructed JSON is exactly equal as a parsed object to
`control_result.json`.

## Reproduction

From the campaign directory:

```text
python3 -I -B -W error \
  reviews/inactive_set_coloring_bridge_hostile/independent_check.py \
  reviews/inactive_set_coloring_bridge_hostile/evidence.json

python3 -I -B -W error \
  math/working/inactive_set_coloring_bridge/verify_control.py
```

Both commands pass on the frozen bytes above.
