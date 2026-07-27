# Hostile review: the \(k=3\) full family-response-list slice

## Verdict

**PASS.**

No mathematical correction is required in
`math/working/k3_full_list_slice/NOTE.md` at SHA-256

`ebcf7a6ef902889e5d70a657baf7e79613b3dd0e278be01263cf0882033d23be`.

The human theorems are valid for an **arbitrary specified** eternal family
in the standard one-guard model.  The full-core reduction is exact, not
merely necessary.  The graph/complement conventions in the spoke, link, and
coloring arguments are consistent.

The through-order-nine connected-unlabeled computation is accepted as
**CERTIFIED-FINITE for its narrowly stated predicate**, now that a
structurally separate replay has reproduced every graph-stream hash and
every count.  It is not a counterexample exclusion, a result for
disconnected graphs, or evidence beyond order nine.  The statement that the
24 surviving lists all happened to be singletons is exact in the audited
finite universe; treating singleton collapse as a pattern beyond that
universe must remain **OBSERVED**.

The order-12 graph with canonical identifier `K{eYptMJynEn` is independently
verified as a positive equality control with a genuine full greatest-family
list.  It refutes any proposed universal no-full-list lemma, but it is not a
counterexample to the gamma--theta conjecture.

## Reviewed artifacts

| artifact | SHA-256 |
|---|---|
| target note | `ebcf7a6ef902889e5d70a657baf7e79613b3dd0e278be01263cf0882033d23be` |
| target probe | `64faa7775df8c5b7145472ca8a4147c1c778e00b3a3061ecaf7d09e9db1c4eeb` |
| target result | `4e97308e937506f3ad52dbe4c99e1285aa9156ba46c27194526bcf13af9ba55a` |
| independent replay | `8e3021d266dc0bd5a4060f0719f54d066e0a2a30aa7ef5f5e1f4489de55820a7` |
| independent replay result | `85986f496e353e0c590d6c495439579885c9a5017c85bd19ac64ae20adffeb3c` |
| pinned `geng` | `588052a87e5313f331aa145a0a641702b6c13b6e2387dd3c4807bf7f49fdaca1` |
| pinned `labelg` | `ae8b1e7ef173c1665725e708bd7abd00b08ee4230ba2bd04117ec63d441274a0` |

The replay uses ordinary `frozenset` graph neighborhoods and an explicit
colored configuration digraph.  It imports neither the target probe nor a
campaign evaluator.

## 1. Family quantifiers and deletion

For an independent family state \(S=\{a,b,c\}\),

\[
L_S^{\mathcal F}(x)
=\{u\in S:ux\in E(G),\ S-u+x\in\mathcal F\}.
\]

Every eternal family is contained in the greatest safe fixed point, and
every retained state dominates.  Therefore

\[
L_S^{\mathcal F}(x)
\subseteq L_S^{\mathcal K_\ast}(x)
\subseteq L_S^{\mathrm{stat}}(x).
\]

This proves that a zero greatest-family full-list count also covers every
proper eternal family.  The finite scan does not need to enumerate
subfamilies.

For Theorem 2.2, let

\[
\mathcal F^{-x}=\{D\in\mathcal F:x\notin D\}.
\]

It is nonempty because \(S\) avoids \(x\).  If \(D\in\mathcal F^{-x}\) and
\(r\in V(G-x)-D\), closure in \(\mathcal F\) gives a one-edge response

\[
D-u+r\in\mathcal F.
\]

Neither the source nor the attack contains \(x\), so the successor avoids
\(x\) literally.  Thus the same move lies in \(\mathcal F^{-x}\) in
\(G-x\).  No greatest-family assumption occurs.

The independent triple \(S\) survives, while deletion cannot increase
\(\alpha\).  Hence \(\alpha(G-x)=3\); the restricted family gives
\(\gamma^\infty(G-x)\le3\), and
\(\alpha\le\gamma^\infty\) gives equality.  Response-list preservation is
literal because every direct state \(S-u+y\), \(y\ne x\), avoids \(x\), and
the edge \(uy\) is unchanged.

The minimum-counterexample dichotomy is also correct:

- if \(\gamma(G-x)=3\), minimality plus
  \(\alpha(G-x)=\gamma^\infty(G-x)=3\) forces
  \(\theta(G-x)=3\);
- if \(\gamma(G-x)=2\), a dominating pair of \(G-x\) must miss \(x\) at
  both positions, and \(x\) is its unique common neighbor in
  \(H=\overline G\).

The exclusion of \(\gamma(G-x)=1\) correctly uses the graph edge from the
full target \(x\) to any anchor.

## 2. Exact full-core reduction

Fix a proper coloring

\[
f:H[F_3(S)]\to S.
\]

For every non-full vertex \(y\), the set

\[
C_f(y)=\{f(x):x\in F_3(S),\ xy\in E(H)\}
\]

records exactly the colors forbidden by already colored full neighbors.
A singleton list conflicting with \(C_f(y)\) produces a false constant.  A
two-list conflict produces the corresponding projection unit; two
conflicts produce contradictory units.

If an anchored compatible coloring exists, its frozen-component
orientations satisfy the original projection formula and all added units.
Conversely, a satisfying orientation colors every non-full vertex from its
family list.  The accepted projection theorem separates:

1. anchor--non-full edges of \(H\);
2. non-full edges whose endpoints share an omitted color; and
3. cross-projection edges between distinct two-lists.

The proper coloring \(f\) handles full--full edges, and the new units handle
every full--non-full edge.  Full vertices have no \(H\)-edge to an anchor,
because full family membership includes all three graph edges to \(S\).
These cases exhaust \(E(H)\), so Theorem 3.1 is an equivalence.

When \(F_3(S)=\{x\}\), its induced full core has no edge, so the outer
choices are exactly \(x=a,b,c\).  Corollary 3.2 therefore really is three
2-SAT instances.  The theorem does not assert that one is satisfiable.

## 3. Spokes and the second witness layer

For \(u\in S\), let

\[
A_u=N_H(x)\cap N_H(u).
\]

The pair \(\{x,u\}\) cannot dominate because \(\gamma=3\), so \(A_u\ne
\varnothing\).  If \(S=\{u,v,w\}\) and \(p\in A_u\), the two full states

\[
\{x,u,v\},\qquad\{x,u,w\}
\]

must dominate \(p\).  Since \(x,u\) miss \(p\), these states force both
\(vp,wp\in E(G)\).  The unoccupied attack \(p\) from either appropriate
full state then has a unique one-guard response and forces

\[
\{x,u,p\}\in\mathcal F.
\]

Domination of another spoke vertex by this state forces each \(A_u\) to be
a \(G\)-clique.  If a vertex lay in two distinct spokes, the full state
containing those two anchors and \(x\) would fail to dominate it.  Thus the
three spokes are pairwise disjoint.

For \(p\in A_u\),

\[
Y_{u,p}=N_H(u)\cap N_H(p)
\]

is nonempty because \(\{u,p\}\) is not dominating.  Two nonadjacent
vertices in \(Y_{u,p}\), together with \(u,p\), would form an independent
four-set, so the layer is a \(G\)-clique.  The forced state
\(\{x,u,p\}\) makes every layer vertex adjacent to \(x\), while
\(\{u,p,y\}\) is a maximum independent triple and hence lies in every
eternal triple family.

The order-nine floor is valid.  The three spokes supply three distinct
vertices outside \(S\cup\{x\}\).  Each selected spoke has a nonempty
external \(Y\)-layer, and one vertex cannot lie in all three layers without
forming an independent four-set with \(S\).  Their union therefore
contributes at least two additional vertices:

\[
3+1+3+2=9.
\]

## 4. Complement link and response-role rigidity

Let

\[
R_x=N_H(x),\qquad J_x=H[R_x].
\]

The accepted antineighborhood projection applied to the independent
singleton \(\{x\}\) gives

\[
\gamma(G[R_x])=\alpha(G[R_x])=\gamma^\infty(G[R_x])=2.
\]

The proved parameter-two case gives
\(\theta(G[R_x])=2\), so the complement \(J_x\) is bipartite.  For every
\(p\in R_x\), the pair \(\{x,p\}\) is not dominating; a missed vertex is an
actual neighbor of \(p\) in \(J_x\).  Hence the link has no isolates.

Every link edge \(pq\) gives a maximum independent family state

\[
T_{pq}=\{x,p,q\}.
\]

Adjacent link edges \(pq,qr\) give independent states sharing
\(\{x,q\}\).  Since \(p,r\) lie on the same side of the bipartition, they
are adjacent in \(G\), and exact ridge covariance acts by
\((p\ r)\).  The attack anchor is outside every link state and remains
fixed.  Connectivity of the line graph therefore makes the three responder
roles \(X,U,V\) constant on an entire link component.

If \(p\in A_u\cap U_C\), its \(U\)-role is absent because \(pu\notin E(G)\).
For an incident edge \(pq\), the opposite endpoint \(q\) cannot also lie in
\(A_u\), because \(A_u\) is a \(G\)-clique while \(pq\in E(H)\).  A link
vertex misses at most one anchor: missing two would make the corresponding
full state fail domination.  Thus \(qu\in E(G)\), and the known spoke state
\(\{x,p,u\}\) makes the \(V\)-role present.  This proves side-purity.

## 5. Audit of the cross-spoke transport

Suppose distinct spoke types \(A_u,A_v\) meet the same side of one link
component at vertices

\[
p=v_0,\ v_1,\ldots,v_{2m}=q.
\]

The path has positive even length.  Let \(w\) be the third anchor and start
from the full state

\[
D=\{x,u,v\}.
\]

For \(m=1\), attack \(v_1\).  The guard \(x\) misses the attack.  Moving
\(v\) produces a state missing \(p\); moving \(u\) produces one missing
\(q\).  These are all possible responders, contradicting closure.

For \(m\ge2\), the same attack rules out \(x\) and \(v\), so closure forces

\[
u\to v_1,\qquad D_1=\{x,v,v_1\}\in\mathcal F.
\]

Domination of \(v_2\) by \(D_1\) forces \(vv_2\in E(G)\).  Hence at the
independent state

\[
T_2=\{x,v_1,v_2\},
\]

the attack at anchor \(v\) retains the responder role \(v_2\), with
successor \(D_1\).

Along

\[
T_i=\{x,v_{i-1},v_i\},\qquad 2\le i\le2m,
\]

successive ridge transpositions exchange
\(v_{i-1},v_{i+1}\) and fix the outside attack \(v\).  Their composite
maps the initial role \(v_2\) to \(v_{2m}=q\).  Covariance would therefore
put \(q\) in the response list to \(v\), requiring \(qv\in E(G)\), while
\(q\in A_v\) says exactly \(qv\notin E(G)\).  The contradiction proves
cross-spoke separation.  No graph automorphism or greatest-family lift is
used.

## 6. Local coloring criterion

A link vertex misses at most one anchor, so

\[
R_x=A_a\dot\cup A_b\dot\cup A_c\dot\cup A_\ast.
\]

If \(x\) is assigned color \(w\), every bipartite link component must use
the other two colors \(u,v\).  Vertices in \(A_u\) are forced to color
\(v\), and vertices in \(A_v\) are forced to color \(u\).  Because each
spoke is side-pure, a component orientation exists exactly when the two
relevant spoke types do not occupy the same side.  This proves Proposition
6.1 in both directions.

The cross-spoke theorem says that no two distinct spoke types ever occupy
one side.  Hence every bad-pair set \(\mathcal B_C\) is empty, and all three
choices of color for \(x\) pass the local link test.  This conclusion is
only local to

\[
H[S\cup\{x\}\cup R_x].
\]

The target correctly leaves global extension through the residual non-full
vertices to the augmented 2-SAT formulas.

## 7. Independent finite coverage audit

The independent replay exhausted the same pinned connected graph6 streams.
Every stream hash and every count agreed:

| quantity | replay |
|---|---:|
| connected unlabeled graphs, orders \(1\)--\(9\) | 273,193 |
| \(\gamma=\alpha=3\) graphs with a static-full incidence | 51 |
| such incidences | 61 |
| equality graphs among those candidates | 15 |
| equality/static-full incidences | 24 |
| greatest-family full incidences | 0 |

The list-size histogram on the 24 equality incidences is

\[
(0,24,0,0)
\]

for sizes \(0,1,2,3\).  All such incidences occur at order nine.

The coverage mechanism is exact:

1. `geng -cq n` supplies one representative of every connected unlabeled
   graph;
2. the stream count and SHA-256 are recorded separately for each order;
3. every independent triple/target pair is tested for static fullness;
4. only then are \(\gamma=\alpha=3\) checked;
5. the complete colored configuration digraph of dominating triples is
   reduced to its greatest safe kernel; and
6. the family list is read from literal successor membership.

If an arbitrary proper eternal family had a full response list, monotonicity
would make the greatest-family list full as well.  Thus the zero count
covers proper families without enumerating them.

This supports the `CERTIFIED-FINITE` label for the exact connected,
through-order-nine statement.  It supplies no disconnected result, no
order-ten result, and no global counterexample frontier.

## 8. Independent control replay

For the labeled order-12 graph

```text
Ksv`f\knJVis
```

the replay independently found an isomorphism to

```text
K{eYptMJynEn
```

and pinned `labelg` returned the latter canonical identifier.  It verified:

\[
(\gamma,\alpha,\gamma^\infty,\theta)=(3,3,3,3);
\]

- all 127 dominating triples survive the greatest fixed point;
- all \(127(12-3)=1,143\) state/attack obligations have a legal one-edge,
  one-guard successor;
- at \(S=\{1,2,3\}\), target \(0\) has list \(\{1,2,3\}\);
- the other eight lists match the target note;
- exactly one compatible anchored coloring exists;
- target \(0\) receives color \(3\);
- the displayed three-clique partition is valid;
- the link edges are \(6\!-\!8\) and \(10\!-\!11\); and
- the spokes and external witnesses are exactly those displayed in the
  note.

The replay also reproduced:

- the 17-state, 68-obligation proper `FDzro` family with full target \(4\)
  and \((\gamma,\alpha,\gamma^\infty)=(2,3,3)\);
- `HCQebjw` with all three static swaps at target \(8\), greatest-family
  list \(\{1\}\), and equality parameters;
- the full-column exchange system satisfying both abstract exchange axioms
  but having no base ordering; and
- the marked link claw with no extension for any of the three target colors,
  whose realizing graph has \(\gamma=2\) and no eternal triple family.

These controls support exactly the refutations claimed and no stronger
ones.

## 9. Reproducibility notes and exact boundary

Two nonmathematical cleanup items remain:

1. the target probe does not close its `Popen` pipes explicitly and emits
   `ResourceWarning` messages at interpreter shutdown;
2. its research log points to a temporary replay path rather than the
   committed result.

Neither affected the completed output, and the independent replay uses
context-managed subprocesses.  They should nevertheless be cleaned before
archival release.

Reproduction:

```text
python3 -I -B -W error \
  gamma_theta_eternal_domination/reviews/k3_full_list_slice_hostile/independent_replay.py \
  --max-order 9
```

The accepted endpoint is:

- full lists can genuinely occur under
  \(\gamma=\alpha=\gamma^\infty=3\);
- their local link geometry is completely color-feasible;
- extension through the remaining non-full vertices is exactly an outer
  full-core coloring plus augmented 2-SAT; and
- no argument here proves that one global augmented formula must be
  satisfiable.

Accordingly, the full-list slice remains open globally and neither the
\(k=3\) slice nor the universal gamma--theta conjecture is resolved.
