# Full-target propagation across maximum-independent facets at \(k=3\)

## Status and exact boundary

Date: 2026-07-28 (PDT)

This note uses the standard **one-guard-moves** eternal domination model.
Attacks are made only at unoccupied vertices, exactly one adjacent guard
moves, and every retained successor dominates.

The results are conditional structural theorems.  They do not resolve the
\(\gamma\)--\(\theta\) conjecture or its complete \(k=3\) slice.

The main conclusions are:

1. **PROVED:** for a fixed outside target \(x\), whether a physical vertex
   \(v\) can answer the attack at \(x\) is independent of which maximum
   independent triple containing \(v\) is used as the current state.
   This propagates across facets sharing only one vertex, not merely across
   ridges.
2. **PROVED:** after fixing any proper three-coloring of
   \(\overline{G-x}\), every ridge component of the maximum-independent
   triangle complex has a nonempty, well-defined set of responder colors.
3. **PROVED:** if one color belongs to the responder-color set of every
   ridge component, then that color is absent from \(N_{\overline G}(x)\),
   so the coloring extends over \(x\).
4. **PROVED:** in the equality-critical deletion branch of a hypothetical
   minimum counterexample, a full target therefore forces at least three
   ridge components.  The component containing the full reference state
   has all three responder colors and contains no vertex of
   \(N_{\overline G}(x)\).  The nonroot component responder-color sets are
   nonempty but have empty total intersection.
5. **SHARP BOUNDARY:** connected equality graphs can have many ridge
   components.  The accepted
   \(G=\overline{L(K_{3,3})}\) control has six isolated maximum-independent
   facets.  Thus equality and connectedness alone cannot replace the
   missing global response argument.

The exact remaining obstruction is a global incompatibility among the
nonempty responder-color sets of at least two nonroot facet components.
This is a precise full-list analogue of global facet holonomy.

## 1. Setup

Let \(G\) be a finite simple graph with

\[
 \alpha(G)=3,
\tag{1.1}
\]

let \(\mathcal F\) be an eternal family of dominating triples, and fix a
vertex \(x\).  Let \(\mathscr T_x\) be the set of independent triples of
\(G\) that avoid \(x\).  Every member of \(\mathscr T_x\) is a maximum
independent set, so the accepted maximum-independent-state theorem places
it in every eternal triple-family, including \(\mathcal F\).

For \(T\in\mathscr T_x\), define

\[
 L_T(x)=
 \{v\in T:vx\in E(G),\ T-v+x\in\mathcal F\}.
\tag{1.2}
\]

This set is nonempty: \(x\) is an unoccupied attack at the retained state
\(T\), and eternal closure supplies a response.

Let \(\Gamma_x\) be the graph whose vertices are the triples in
\(\mathscr T_x\), with two triples adjacent when they share two vertices.
Its connected components will be called **ridge components**.

## 2. Response membership is constant on a vertex star

### Theorem 2.1 (vertex-star propagation) — PROVED

Let \(T,T'\in\mathscr T_x\), and let

\[
 v\in T\cap T'.
\]

Then

\[
 \boxed{
 v\in L_T(x)\quad\Longleftrightarrow\quad v\in L_{T'}(x).
 }
\tag{2.1}
\]

Thus response membership of the physical guard \(v\) at the fixed target
\(x\) is independent of the maximum independent triple containing \(v\).

#### Proof

The implication is trivial if \(T=T'\).  By symmetry it is enough to prove
the forward implication in the two possible nontrivial intersection
sizes.

First suppose that \(T\) and \(T'\) share two vertices.  Write

\[
 T=\{v,u,p\},\qquad T'=\{v,u,q\}.
\]

The hypothesis \(v\in L_T(x)\) gives

\[
 D=T-v+x=\{u,p,x\}\in\mathcal F.
\tag{2.2}
\]

Attack the unoccupied vertex \(q\) from \(D\).  The guard at \(u\) cannot
move, because \(u,q\in T'\) and \(T'\) is independent.  A move
\(x\to q\) would produce

\[
 \{u,p,q\},
\]

which does not dominate \(v\): all three displayed vertices are
nonadjacent to \(v\), by independence of \(T\) and \(T'\).
Consequently closure forces \(p\to q\) and retains

\[
 \{u,q,x\}=T'-v+x.
\]

The edge \(vx\) is already part of \(v\in L_T(x)\), so
\(v\in L_{T'}(x)\).

Now suppose that \(T\cap T'=\{v\}\).  Write

\[
 T=\{v,a,b\},\qquad T'=\{v,p,q\}.
\]

Again \(v\in L_T(x)\) gives

\[
 D=T-v+x=\{a,b,x\}\in\mathcal F.
\tag{2.3}
\]

Attack \(p\).  If \(x\) moved, the successor \(\{a,b,p\}\) would miss
\(v\), because \(v\) is nonadjacent to \(a,b,p\).  Closure therefore
moves one of \(a,b\); relabel them if necessary so that the retained
successor is

\[
 D'=\{b,p,x\}\in\mathcal F.
\tag{2.4}
\]

Attack the still-unoccupied vertex \(q\).  The guard at \(p\) cannot move,
because \(p,q\in T'\).  If \(x\) moved, the successor
\(\{b,p,q\}\) would again miss \(v\).  Closure therefore forces
\(b\to q\) and retains

\[
 \{p,q,x\}=T'-v+x.
\]

Together with \(vx\in E(G)\), this says \(v\in L_{T'}(x)\).
Interchanging \(T,T'\) proves the reverse implication. \(\square\)

### Definition 2.2 (the active set)

Theorem 2.1 makes the following set well-defined:

\[
 A_x=
 \{v\ne x:
   v\text{ lies in a member }T\in\mathscr T_x
   \text{ and }v\in L_T(x)\}.
\tag{2.5}
\]

For every \(T\in\mathscr T_x\),

\[
 L_T(x)=T\cap A_x\ne\varnothing.
\tag{2.6}
\]

Every member of \(A_x\) is adjacent to \(x\) in \(G\), so

\[
 A_x\cap N_{\overline G}(x)=\varnothing.
\tag{2.7}
\]

If \(x\) has a full response at some independent state \(S\), then

\[
 S\subseteq A_x.
\tag{2.8}
\]

The active set is family-relative.  A vertex can be adjacent to \(x\) in
\(G\) but absent from \(A_x\) because the corresponding successor state
is not retained.

## 3. A nonempty responder-color set on every ridge component

Put

\[
 H'=\overline{G-x},
\]

and suppose that \(H'\) has a proper three-coloring

\[
 \kappa:V(G)-\{x\}\longrightarrow\{1,2,3\}.
\tag{3.1}
\]

Every \(T\in\mathscr T_x\) is a triangle of \(H'\), so its three vertices
receive all three colors.

### Theorem 3.1 (componentwise responder-color constancy) — PROVED

For a ridge component \(C\) of \(\Gamma_x\), define using any
\(T\in C\)

\[
 A_C^\kappa=\kappa(T\cap A_x)=\kappa(L_T(x)).
\tag{3.2}
\]

Then \(A_C^\kappa\) is independent of the choice of \(T\in C\), and

\[
 \varnothing\ne A_C^\kappa\subseteq\{1,2,3\}.
\tag{3.3}
\]

Moreover, every vertex

\[
 r\in N_{\overline G}(x)
\]

that belongs to the support of \(C\) satisfies

\[
 \kappa(r)\notin A_C^\kappa.
\tag{3.4}
\]

#### Proof

It is enough to compare ridge-adjacent facets

\[
 T=\{u,v,p\},\qquad T'=\{u,v,q\}.
\]

Theorem 2.1 makes the active status of the common vertices \(u,v\)
independent of the chosen facet.

For the exchanged positions,

\[
 T-p+x=T'-q+x=\{u,v,x\}.
\tag{3.5}
\]

Hence \(p\in A_x\) if and only if \(q\in A_x\): membership of the common
successor in \(\mathcal F\) is the same statement, and its domination of
the omitted vertex forces the required graph edge to \(x\) in either
direction.

Since \(\kappa\) is proper and \(u,v\) already use two different colors,
the exchanged vertices \(p,q\) have the same third color.  Thus the set of
colors on \(T\cap A_x\) is unchanged by a ridge step.  Connectivity proves
that (3.2) is well-defined.  Nonemptiness follows from (2.6).

Finally, take \(r\in N_{\overline G}(x)\) in a facet \(T\in C\).  The
vertex \(r\notin A_x\) by (2.7).  It is the unique vertex of \(T\) with
color \(\kappa(r)\).  If that color belonged to \(A_C^\kappa\), the unique
same-colored vertex of \(T\) would lie in \(A_x\), a contradiction.  This
proves (3.4). \(\square\)

### Corollary 3.2 (overlap consistency) — PROVED

If ridge components \(C,D\) have a common support vertex \(v\), then

\[
 \kappa(v)\in A_C^\kappa
 \quad\Longleftrightarrow\quad
 \kappa(v)\in A_D^\kappa.
\tag{3.6}
\]

In particular, if \(C_0\) contains a full-response state and \(D\) shares
a support vertex \(v\) with \(C_0\), then

\[
 \kappa(v)\in A_D^\kappa.
\tag{3.7}
\]

#### Proof

Equation (3.6) is Theorem 2.1 translated through the unique color of \(v\)
in a facet of each component.  A full state makes every one of its colors
active, and Theorem 3.1 propagates all three colors throughout \(C_0\).
This proves (3.7). \(\square\)

This is a genuine bridge across ridge components.  It uses two literal
one-guard attacks when the facets share only one vertex.

## 4. The common-color extension criterion

### Theorem 4.1 (common responder color extends \(x\)) — PROVED

Assume additionally that

\[
 \gamma(G-x)=\alpha(G-x)=\gamma^\infty(G-x)=3.
\tag{4.1}
\]

If, for some proper three-coloring \(\kappa\) of \(H'\),

\[
 w\in\bigcap_C A_C^\kappa,
\tag{4.2}
\]

where the intersection runs over all ridge components of \(\Gamma_x\),
then \(\kappa\) extends to a proper three-coloring of
\(\overline G\) by giving \(x\) color \(w\).  Consequently

\[
 \theta(G)=3.
\tag{4.3}
\]

#### Proof

The parameter equality in (4.1), together with
\(\gamma\le i\le\alpha\), makes \(G-x\) well-covered.  Every vertex of
\(G-x\) therefore belongs to a maximum independent triple and hence to
the support of at least one ridge component.

Let \(v\) be any vertex with \(\kappa(v)=w\), and choose a facet
\(T\) containing it, in a component \(C\).  The three vertices of \(T\)
have distinct colors.  Since \(w\in A_C^\kappa\), its unique
\(w\)-colored vertex \(v\) lies in \(A_x\).  Thus \(vx\in E(G)\), or
equivalently \(vx\notin E(\overline G)\).

No \(w\)-colored vertex is adjacent to \(x\) in \(\overline G\), so giving
\(x\) color \(w\) preserves properness.  The parameter chain already gives
\(\theta(G)\geq\alpha(G)=3\), proving (4.3). \(\square\)

### Corollary 4.2 (at least three ridge components) — PROVED

Suppose \(G\) is in the equality-critical full-target branch:

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3<\theta(G),
\tag{4.4}
\]

\[
 \gamma(G-x)=\alpha(G-x)=\gamma^\infty(G-x)=\theta(G-x)=3,
\tag{4.5}
\]

and \(x\) has a full response at an independent state \(S\).

For every proper three-coloring \(\kappa\) of \(\overline{G-x}\):

1. the component \(C_0\) containing \(S\) satisfies
   \[
   A_{C_0}^\kappa=\{1,2,3\};
   \tag{4.6}
   \]
2. the support of \(C_0\) is disjoint from
   \(N_{\overline G}(x)\);
3. every other responder-color set is nonempty; and
4.
   \[
   \bigcap_C A_C^\kappa=\varnothing.
   \tag{4.7}
   \]

Consequently \(\Gamma_x\) has at least three connected components.

#### Proof

Fullness gives all three active colors on \(S\), and Theorem 3.1 proves
(4.6).  Equation (3.4) then excludes every complement neighbor of \(x\)
from the support of \(C_0\).  Nonemptiness is (3.3).

If (4.7) failed, Theorem 4.1 would give \(\theta(G)=3\), contrary to
(4.4).  With one component the intersection is all three colors.  With
exactly two components it is the nonempty responder-color set of the
nonroot component, because the root set is all three colors.  Therefore
at least three components are necessary. \(\square\)

This is stronger than merely saying that the facet graph is disconnected.
The nonroot components must carry nonempty responder-color sets with a
genuinely empty global intersection.

## 5. Exact controls and sharpness

### 5.1 Connected equality does not imply ridge connectivity

Let

\[
 H'=L(K_{3,3})
\]

be the \(3\times3\) rook graph and put \(G'=\overline{H'}\).  The six
maximum cliques of \(H'\) are its three row triangles and three column
triangles.  Distinct such triangles share at most one vertex, so the
ridge graph consists of six isolated facets.

The accepted line-graph theorem C-060 gives

\[
 \gamma(G')=\alpha(G')=\gamma^\infty(G')=\theta(G')=3,
\]

and \(G'\) is connected.  Thus neither connectedness nor deletion equality
forces even two ridge facets to lie in the same component.  Any proof of
Corollary 4.2's obstruction must use the added full-target response data.

The smaller bow-tie complement gives the same warning without
connectedness: if \(H'\) is two triangles sharing one vertex, then
\(G'\cong K_1\dot\cup C_4\) has all four parameters equal to three while
its two facets are ridge-disconnected.

### 5.2 The order-12 positive full-list control

For the accepted equality graph with labeled record

```text
Ksv`f\knJVis
```

(canonical graph6 `K{eYptMJynEn`), use the incidence

\[
 S=\{1,2,3\},\qquad x=0
\]

from C-073/C-074.  The greatest eternal family has a full response at
\((S,x)\).  The seven independent triples avoiding \(x\) are seven
isolated ridge components.  Under the unique anchored full-graph coloring
(equivalently, the unique anchored deletion coloring that extends over
\(x\)) with clique fibers

\[
 \{1,5,8,11\}\mid
 \{2,6,7,10\}\mid
 \{0,3,4,9\},
\tag{5.1}
\]

their responder-color sets are

\[
 \{1,2,3\},\
 \{1,3\},\
 \{2,3\},\
 \{1,3\},\
 \{1,3\},\
 \{2,3\},\
 \{2,3\}.
\tag{5.2}
\]

Their intersection is exactly

\[
 \{3\},
\tag{5.3}
\]

which is the unique color that extends over \(x\).  The active set is

\[
 A_x=\{1,2,3,4,5,7,9\},
\]

and its complement among the deletion vertices is exactly

\[
 N_{\overline G}(x)=\{6,8,10,11\}.
\]

This control lies in the domination-drop branch
\(\gamma(G-x)=2\), so it is not covered by Theorem 4.1's
well-covered-deletion hypothesis.  Nevertheless, it shows that the
component responder-color intersection can nontrivially select the one
correct global color even when every facet is ridge-isolated.

## 6. Exact remaining gap

The equality-critical full-list branch is now reduced to the following
configuration.

1. The maximum-independent triangle complex of \(G-x\) has at least three
   ridge components.
2. One distinguished component has all three responder colors and contains
   no physical complement neighbor of \(x\).
3. Every component has a nonempty responder-color set.
4. Shared support vertices synchronize membership of their colors across
   components by Theorem 2.1.
5. For every deletion three-coloring, the total intersection of the
   component responder-color sets is empty.

What is not proved is that one-guard closure forbids this last global
incompatibility.  Equality graphs such as
\(\overline{L(K_{3,3})}\) show that many ridge components are possible,
so component count alone cannot finish the argument.  The missing theorem
must use the synchronized responder sets, not only the static facet
complex.

A particularly sharp next target is:

> **Responder-color intersection target.**  Under the hypotheses of
> Corollary 4.2, prove that the nonempty synchronized sets
> \(A_C^\kappa\) have nonempty total intersection for at least one proper
> three-coloring \(\kappa\) of \(\overline{G-x}\).

This target is strictly more structured than the original full-list
extension problem: it exposes a physical active set \(A_x\), a proved
vertex-star synchronization law, a distinguished all-color component, and
an exact common-color certificate.  It remains a genuine global gap and is
not claimed here as an equivalent reformulation in both directions.
