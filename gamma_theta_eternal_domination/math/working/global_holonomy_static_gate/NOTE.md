# Static-strengthening audit: the accepted seven-cycle control already refutes it

## Status and scope

Date: 2026-07-28 (PDT)

This note tests the following proposed static implication in the \(k=3\)
complement language.  Write \(H=\overline G\), and suppose that

1. \(H\) is \(K_4\)-free;
2. every pair of vertices of \(H\) has a common neighbor; and
3. every vertex link \(H[N_H(w)]\) is bipartite and isolate-free.

Does it follow that \(\chi(H)\leq3\)?

The answer is **no**, already at order seven.  The necessary control was
already present in the campaign:

\[
 G=C_7,\qquad H=\overline{C_7}.
\tag{0.1}
\]

In fact every link of \(H\) is a **connected** \(P_4\), so disconnected
links are not the issue.  The flag clique complex of \(H\) is the standard
seven-vertex triangulation of the Möbius band.  Thus the example realizes
literal global holonomy: all local link two-colorings exist and all links
are connected, but they do not glue to a global three-coloring.

This note makes no novelty claim for \(C_7\), its parameter tuple, its facet
loop, or its two-attack failure tree.  In particular:

* accepted C-064, Section 4 of
  `math/working/cross_state_response_exchange.md`, already uses the
  seven-facet \(C_7\) loop and its nontrivial transported three-cycle to show
  that ridge transport alone does not kill holonomy; and
* accepted C-020, Section 4 of
  `math/lemmas/two_step_transition_kernel.md`, already gives the same
  two-attack certificate proving that three guards are not eternal on
  \(C_7\).

The genuinely added content here is an audit of the *newly proposed static
strengthening*: \(H=\overline{C_7}\) also has a common neighbor for every
pair and has a connected \(P_4\) at every vertex link.  The note packages
those facts, identifies the accepted seven-facet loop as the flag Möbius
band, certifies order-minimality for this exact static implication, and
provides a standalone replay.

This graph is not a counterexample to the gamma--theta conjecture.  Its
already accepted exact parameters are

\[
 \boxed{(\gamma,i,\alpha,\gamma^\infty,\theta)(C_7)
       =(3,3,3,4,4).}
\tag{0.2}
\]

The already accepted dynamic equality failure is replayed in Section 4.
The sharpened control therefore isolates exactly what is missing from the
new purely static local-holonomy proposal.

## 1. The static countermodel

Label the vertices by \(\mathbb Z/7\mathbb Z\), with \(ij\in E(G)\) when
\(j-i\equiv\pm1\pmod7\).  Hence

\[
 ij\in E(H)
 \quad\Longleftrightarrow\quad
 j-i\not\equiv0,\pm1\pmod7.
\tag{1.1}
\]

The labeled and canonical graph6 strings are:

| graph | labeled graph6 | canonical graph6 |
|---|---|---|
| \(G=C_7\) | `FhCKG` | `FoDPO` |
| \(H=\overline{C_7}\) | `FUzro` | `F}hXw` |

The pinned `labelg` executable independently reconstructs the canonical
strings.

### Proposition 1.1 — PROVED

The graph \(H=\overline{C_7}\) is \(K_4\)-free, every pair of its vertices
has a common neighbor, every link is a connected \(P_4\), and
\(\chi(H)=4\).

#### Proof

A clique of \(H\) is an independent set of \(C_7\).  An independent set in
an odd seven-cycle has size at most three, so \(H\) is \(K_4\)-free.

For any root \(w\),

\[
 N_H(w)=\{w+2,w+3,w+4,w+5\}.
\tag{1.2}
\]

The link edges are

\[
 (w+4)(w+2),\quad
 (w+2)(w+5),\quad
 (w+5)(w+3),
\tag{1.3}
\]

so the link is the path

\[
 w+4\;-\;w+2\;-\;w+5\;-\;w+3.
\tag{1.4}
\]

It is therefore connected, bipartite, and isolate-free.

For the common-neighbor condition, translate one endpoint to \(0\).
A direct check of the six possible differences gives a common neighbor;
equivalently, (1.2) and its translate have nonempty intersection for every
distinct pair.  The verifier prints all 21 intersections explicitly.

A color class of \(H\) is a clique of \(C_7\), hence has size at most two.
Three colors cover at most six vertices, so \(\chi(H)\geq4\).  Four colors
are supplied by the \(C_7\) clique partition

\[
 \{0,1\},\quad\{2,3\},\quad\{4,5\},\quad\{6\}.
\tag{1.5}
\]

Thus \(\chi(H)=4\). \(\square\)

This disproves the proposed static implication even after strengthening
“bipartite and isolate-free link” to “connected \(P_4\) link.”

## 2. Exact parameters of \(G=C_7\)

### Proposition 2.1 — PROVED

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)(C_7)=(3,3,3,4,4).
\tag{2.1}
\]

#### Proof

Each closed neighborhood in \(C_7\) has size three.  Two guards therefore
cover at most six vertices, while \(\{0,2,4\}\) dominates.  Hence
\(\gamma(C_7)=3\).

The usual alternating argument on an odd cycle gives
\(\alpha(C_7)=3\).  Every maximal independent set is dominating, so

\[
 3=\gamma(C_7)\leq i(C_7)\leq\alpha(C_7)=3.
\tag{2.2}
\]

Thus \(i(C_7)=3\) as well.

The cycle is triangle-free, so every clique contains at most two vertices.
Consequently any clique partition has at least four parts, and (1.5)
attains four.  Thus \(\theta(C_7)=4\).

Section 4 proves \(\gamma^\infty(C_7)>3\).  For the upper bound, place one
guard in each part of (1.5).  Whenever an unoccupied vertex is attacked,
move the guard within its two-vertex clique (or observe that the singleton
is permanently occupied).  The family of the eight resulting
configurations is a literal one-guard eternal four-family.  Therefore
\(\gamma^\infty(C_7)=4\). \(\square\)

The standalone verifier also computes the complete greatest kernels by two
different representations.  There are 14 dominating triples: seven are
deleted in synchronous round one and seven in round two.  The three-guard
kernel is empty in both implementations.  The four-guard kernel contains
28 configurations, including the explicit eight-state clique strategy.

## 3. Topological audit of C-064's accepted facet loop

This section repackages the seven-facet loop already used by C-064; it is
not a new graph construction or a new basic holonomy obstruction.

Let \(X=\operatorname{Cl}(H)\) be the clique complex.  Since it is a clique
complex, it is flag.  Its seven facets are

\[
 F_i=\{i,i+2,i+4\}\qquad(i\in\mathbb Z/7\mathbb Z).
\tag{3.1}
\]

Every edge lies in a facet, and there is no \(K_4\), so \(X\) is pure of
dimension two.  Its \(f\)-vector and Euler characteristic are

\[
 f(X)=(7,14,7),\qquad \chi(X)=7-14+7=0.
\tag{3.2}
\]

The seven boundary edges are

\[
 \{i,i+4\}\qquad(i\in\mathbb Z/7\mathbb Z),
\tag{3.3}
\]

and they form the single cycle

\[
 0-4-1-5-2-6-3-0.
\tag{3.4}
\]

Every vertex link is the path (1.4), so \(X\) is a connected triangulated
surface with boundary.  A connected compact surface with one boundary
component and Euler characteristic zero is a Möbius band.  One can also
see the twist directly by following the seven facets around their cyclic
dual adjacency.

This audits the assumptions that are easy to conflate:

* **flagness:** yes, by definition of \(X=\operatorname{Cl}(H)\);
* **purity:** yes, and checked facet-by-facet;
* **connectedness:** yes; in fact \(H\) has diameter at most two because
  every pair has a common neighbor;
* **link bipartiteness:** yes;
* **link isolate-freeness:** yes;
* **link connectedness:** yes, every link is \(P_4\);
* **closed pseudomanifold:** no.  The links are paths rather than cycles,
  and \(X\) has a boundary.

Accordingly, the example kills the stated static theorem and also kills the
natural strengthening obtained by requiring connected links.  It does not
settle a further strengthened theorem restricted to closed flag
two-manifolds.  An exploratory unlabeled scan found no closed-link
countermodel through order nine, but that scan has no proof-log package and
is recorded only as **OBSERVED**.

## 4. Replay of the accepted C-020 dynamic failure

Accepted C-020 already proves this two-ply failure.  It is repeated here
only so the static strengthening and its precise dynamic failure can be
checked from one artifact.

Put

\[
 S=\{0,2,4\}.
\tag{4.1}
\]

This is a maximum independent set of \(C_7\).  Every eternal three-family
would have to contain \(S\): successively attack unoccupied vertices of
\(S\); because its vertices are pairwise nonadjacent, a guard already moved
onto \(S\) cannot be the guard moved to another member of \(S\), so the
number of occupied vertices of \(S\) strictly increases until the state is
\(S\).

Attack vertex \(1\) from \(S\).  The only eligible guards are \(0\) and
\(2\).

1. Moving \(0\to1\) gives \(\{1,2,4\}\), which does not dominate vertex
   \(6\).
2. Moving \(2\to1\) gives \(T=\{0,1,4\}\), which does dominate.  Now attack
   vertex \(3\).  The only eligible guard is \(4\), and moving \(4\to3\)
   gives \(\{0,1,3\}\), which does not dominate vertex \(5\).

Thus \(S\) has no response to the first attack that can remain in an
eternal family.  This proves \(\gamma^\infty(C_7)>3\) without trusting a
fixed-point implementation.

The attack tree is depth two.  In complement language, all seven Möbius
facets are forced configurations, but each has synchronous deletion rank
two.  Local link bipartitions and their global topological twist therefore
do not by themselves model the online one-guard closure.

## 5. SAT/CEGAR discovery probe and soundness audit

`search_static_gate.py` uses one Boolean variable for every possible edge of
\(H\), with the following exact constraints.

1. A triangle on vertices \(0,1,2\) is fixed.  This loses no target graph:
   the common-neighbor condition produces an edge, and applying it to the
   endpoints of that edge produces a triangle.
2. Every four-set receives the clause forbidding all six of its edges.
3. For each pair \(u,v\), witness variables choose a vertex \(w\) and imply
   both \(uw\) and \(vw\).  Their disjunction is required.
4. For each root \(w\), an auxiliary bit colors every possible link vertex.
   Whenever \(wu,wv,uv\) are all edges, two guarded clauses force the colors
   of \(u,v\) to differ.  Existence of those bits is exactly link
   bipartiteness.
5. Isolate-freeness needs no additional clause: applying the pair
   common-neighbor condition to the endpoints of any edge \(wu\) produces
   a link neighbor of \(u\).

Non-three-colorability is imposed by sound CEGAR cuts.  When the exact
coloring search returns a three-coloring \(c\) of the current graph, the
next formula contains

\[
 \bigvee_{\{u,v\}:\ c(u)=c(v)} uv.
\tag{5.1}
\]

Any graph for which \(c\) remains a proper coloring makes every literal in
(5.1) false.  Hence the clause removes exactly the possibility that this
particular coloring is proper and cannot remove a genuinely
non-three-colorable graph.

`audit_cegar.py` exhausts all 64 labeled graphs on four vertices.  For each
graph it fixes every edge variable and compares SAT with a separately coded
direct predicate.  All 64 agree.  For each of the three satisfiable base
graphs it also confirms that the generated coloring cut excludes its source
graph.  This is a finite polarity/conditional audit, not a proof of
large-order coverage.

CaDiCaL discovery runs gave:

| order | result | status |
|---:|---|---|
| 6 | UNSAT after 27 coloring cuts | OBSERVED only (no proof log) |
| 7 | static non-three-colorable witness | OBSERVED discovery |
| 8, 9, 10 | static non-three-colorable witnesses | OBSERVED discovery |

The order-six conclusion does not rely on the unlogged SAT run:
`verify_witness.py` independently enumerates all labeled graphs through
order six, a total of

\[
 1+2+8+64+1024+32768=33867
\tag{5.2}
\]

graphs, and finds no static non-three-colorable graph.  The exact
triangle-normalized static-base counts at orders \(1,\ldots,6\) are

\[
 0,\ 0,\ 1,\ 6,\ 100,\ 2055,
\tag{5.3}
\]

all three-colorable.  Thus order seven is independently certified minimal
for the stated static implication.

As an exploratory cross-check, `geng` finds three unlabeled order-seven
static countermodels, with 12, 13, and 14 edges in \(H\).  The 14-edge
model is \(\overline{C_7}\); deleting any one of its seven boundary edges
gives the 13-edge isomorphism type.  This unlabeled classification remains
**OBSERVED** because it is not needed for, and is not part of, the
independent labeled minimality certificate.

## 6. Consequence for the proof program

The proposed static gate is exhausted.  It cannot prove the \(k=3\) case,
even with connected links, purity, flagness, and diameter two added.

The useful positive conclusion is more precise:

> Any successful global-holonomy argument must use the eternal transition
> relation, not merely the physical complement links or the topology of
> their clique complex.

The already accepted \(C_7\) control shows why.  It satisfies all static
equality conditions
\(\gamma=i=\alpha=3<\theta=4\), but its forced facets die after two attacks.
The next viable proof target is therefore a **dynamic** holonomy statement:
show that survival of every maximum independent triple forces the local
link two-colorings to glue.  One must not infer this gluing from static
connectedness or orientability assumptions alone.

Nor may the attack tree above be imported as a hereditary forbidden
subcomplex statement.  Extra vertices in a larger graph can create new
dominating successor states and new legal responses.  Any use of the
\(C_7\) core inside a larger equality graph must preserve those dynamic
quantifiers explicitly.

## 7. Reproduction

From the campaign root:

```text
math/working/global_holonomy_static_gate/verify_strict.sh
```

The strict script checks pinned tool hashes, replays the independent
witness verifier, replays the 64-graph CEGAR audit, and compares deterministic
outputs to frozen hashes.  It imports neither campaign eternal evaluator.
