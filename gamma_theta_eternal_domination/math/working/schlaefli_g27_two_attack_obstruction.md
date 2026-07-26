# Schläfli \(G(27)\): an exact two-attack obstruction at \(k=3\)

**Status:** `PROVED` for the self-contained \(k=3\) obstruction below;
`CERTIFIED-FINITE` for the two small exhaustive replays; `UNRESOLVED` for the
universal \(\gamma\)–\(\theta\) conjecture.

**Scope warning.** This is a structured proof stress test, not an order
frontier and not a counterexample.  It proves only that the displayed
27-vertex graph has no one-guard eternal family of size three.  It does not
compute \(\gamma^\infty(G)\) above three.

## 1. The graph

Use the 27 labels
\[
 E_i,\ C_i\quad(1\leq i\leq6),\qquad
 L_{ij}\quad(1\leq i<j\leq6).
\]
Let \(H\) be their intersection graph, with the following rules:

- no two \(E\)'s and no two \(C\)'s are adjacent;
- \(E_iC_j\in E(H)\) exactly when \(i\ne j\);
- \(E_iL_{jk},C_iL_{jk}\in E(H)\) exactly when \(i\in\{j,k\}\);
- \(L_{ij}L_{k\ell}\in E(H)\) exactly when
  \(\{i,j\}\cap\{k,\ell\}=\varnothing\).

Set \(G=\overline H\).  Direct counting from these rules gives
\[
 H=\operatorname{srg}(27,10,1,5);
\]
that is, \(H\) is 10-regular, adjacent pairs have one common neighbor, and
nonadjacent pairs have five common neighbors.  Thus \(G\) is the 16-regular
Schläfli graph.

With the displayed label order, the SHA-256 of the newline-terminated labeled
edge list of \(G\) is
`c507b9d74f40bb73f7fdf63700e30009ff48fef87dde71af1ab11b8779fd414b`.
Nauty 2.9.3 gives the canonical Graph6 record

```text
Z~~vnZjvUtw~nSmis{{k~a^||QBtQJNHLU[VQ^BxkFnDK\zEEvn@Tn^_Tn^w
```

## 2. Static parameters

### Proposition 1

\[
\gamma(G)=i(G)=\alpha(G)=3.
\]

### Proof

An independent set in \(G\) is a clique in \(H\).  The graph \(H\) contains
triangles, for example \(\{E_1,C_2,L_{12}\}\).  It contains no \(K_4\):
otherwise an edge of that \(K_4\) would have at least two common neighbors,
contrary to \(\lambda=1\).  Hence \(\alpha(G)=3\).

No pair dominates \(G\).  Indeed, every pair of vertices has a common
\(H\)-neighbor: one if it is an \(H\)-edge and five if it is an \(H\)-nonedge.
That common neighbor is \(G\)-nonadjacent to both members of the pair.  On the
other hand, an \(H\)-triangle is a maximum, hence maximal, independent set of
\(G\), so it dominates \(G\).  Therefore \(\gamma(G)=3\).  The inequalities
\(\gamma\leq i\leq\alpha\) now give \(i(G)=3\). \(\square\)

The exact value
\[
\theta(G)=\chi(H)=6
\]
is **computationally exact** here, not claimed as a new human proof.  The upper
bound is witnessed by these six stable sets of \(H\):

```text
{E1,E2,E3,E4,E5,E6}
{C1,C2,C3,C4,C5,C6}
{L12,L13,L14,L15,L16}
{L23,L24,L25,L26}
{L34,L35,L36}
{L45,L46,L56}
```

Two independent complete lower-bound checks reject five colors:

1. a DSATUR search visits 8,003 nodes;
2. a separate coverage checker finds exactly 72 stable six-sets and no stable
   seven-set.  Any five-coloring would contain two disjoint six-sets.  It
   exhausts all 756 such pairs and rejects a three-coloring of each 15-vertex
   residue (7,800 total recursive calls).

## 3. Which triples dominate?

For a triple \(D\), a vertex outside \(D\) is undominated in \(G\) exactly when
it is an \(H\)-neighbor of all three members of \(D\).

Every \(H\)-independent triple has exactly three common \(H\)-neighbors.  This
can be checked without search: up to permuting \(1,\ldots,6\) and swapping
\(E\) with \(C\), the possible independent triples and their centers are

| type | representative | its three common \(H\)-neighbors |
|---|---|---|
| \(EEE\) | \(E_1,E_2,E_3\) | \(C_4,C_5,C_6\) |
| \(EEL\) | \(E_1,E_2,L_{34}\) | \(C_3,C_4,L_{12}\) |
| \(ECL\) | \(E_1,C_1,L_{23}\) | \(L_{14},L_{15},L_{16}\) |
| \(ELL\) | \(E_4,L_{12},L_{13}\) | \(C_1,L_{45},L_{46}\) |
| \(LLL\), star | \(L_{12},L_{13},L_{14}\) | \(E_1,C_1,L_{56}\) |
| \(LLL\), triangle | \(L_{12},L_{13},L_{23}\) | \(L_{45},L_{46},L_{56}\) |

If a triple has exactly one \(H\)-edge \(ab\), let \(x\) be the unique common
neighbor of \(a,b\).  The set \(\{a,b,x\}\) is a triangle.  Every vertex outside
an \(H\)-triangle is adjacent to exactly one triangle vertex: it is adjacent to
at most one by \(\lambda=1\), while the three triangle vertices have
\(3(10-2)=24\) incidences with the 24 outside vertices.  Since the third member
of the original triple misses \(a,b\), it meets \(x\).  Thus a one-edge triple
also has a common \(H\)-neighbor.

An induced \(H\)-path \(a-b-c\) has no common neighbor: otherwise the edge from
\(b\) to that neighbor would have both \(a\) and \(c\) as common neighbors,
contradicting \(\lambda=1\).  An \(H\)-triangle likewise has no outside common
neighbor because each edge has its third triangle vertex as its unique common
neighbor.

Consequently the dominating triples of \(G\) are exactly

- the 45 \(H\)-triangles; and
- the 1,080 induced \(H\)-paths \(P_3\).

The counts are short: \(H\) has \(135\) edges and each lies in one triangle,
so there are \(135/3=45\) triangles.  The neighborhood of each vertex induces
five disjoint edges.  Hence it is the center of
\(\binom{10}{2}-5=40\) induced paths, giving \(27\cdot40=1080\).

## 4. The two-attack obstruction

### Theorem 2

There is no one-guard-moves eternal dominating family of size three in \(G\).
Equivalently,
\[
\gamma^\infty(G)>3.
\]

### Proof

First consider a dominating triple \(D=\{a,b,c\}\) inducing the path
\(a-b-c\) in \(H\).  The union of its three open \(H\)-neighborhoods has size
\[
 3(10)-(1+1+5)=23.
\]
Here the three pairwise intersection sizes are \(\lambda,\lambda,\mu=1,1,5\),
and the triple intersection is empty by the preceding argument.  The union
contains \(a,b,c\), so exactly four vertices outside \(D\) have no
\(H\)-neighbor in \(D\).  Attack any such vertex \(r\).  It is adjacent in
\(G\) to all three guards.  Moving an endpoint guard produces an \(H\)-triple
with one edge; moving the middle guard produces an \(H\)-independent triple.
Neither kind dominates \(G\).  Thus every path-state has four immediately
lethal attacks.

Now consider a dominating \(H\)-triangle \(D=\{a,b,c\}\).  As shown above,
every outside vertex \(r\) is adjacent in \(H\) to exactly one member, say
\(a\), of \(D\).  Therefore exactly the guards at \(b,c\) can move to \(r\) in
\(G\).  Either move produces an induced \(H\)-path:
\[
 \{a,c,r\}\quad\text{or}\quad\{a,b,r\}.
\]
The adversary then uses one of the four lethal attacks just established.
Thus every possible dominating starting triple loses in at most two attacks,
so no nonempty eternal family of size three exists. \(\square\)

For a concrete branch, start at
\(\{E_1,C_2,L_{12}\}\) and attack \(E_2\).  The only dominating responses are
\[
 C_2\to E_2:\ \{E_1,E_2,L_{12}\},
 \qquad
 E_1\to E_2:\ \{C_2,E_2,L_{12}\}.
\]
In the first branch attack \(E_3\); in the second attack \(L_{13}\).  Each
second attack has no dominating one-guard response.

## 5. Exact kernel replay and interpretation

Let \(K_0\) be all dominating three-configurations and synchronously delete a
configuration at each round if some unoccupied attack has no response inside
the current set.  Both independent implementations obtain

\[
 |K_0|=1125,\qquad |K_1|=45,\qquad |K_2|=0.
\]

More precisely, \(K_0\) consists of 45 triangles and 1,080 paths; \(K_1\)
consists exactly of the triangles.  This is precisely the two paragraphs of
the proof: paths die on the first ply, and triangles can only move to paths.

Artifacts:

- `math/working/schlaefli_g27_probe.py`: bit-mask construction, DSATUR, and
  synchronous kernel;
- `reviews/schlaefli_g27_structured_probe/audit.py`: independently written
  set-valued construction, transition kernel, and coloring-coverage check;
- `reviews/schlaefli_g27_structured_probe/REVIEW.md`: replay hashes and scope.

This graph is a useful stress test because it has
\(\gamma=i=\alpha=3<\theta=6\) but the one-guard condition fails at depth two.
It supports the proof program by making the missing dynamic mechanism explicit;
it does not by itself advance the finite order frontier or resolve the
conjecture.
