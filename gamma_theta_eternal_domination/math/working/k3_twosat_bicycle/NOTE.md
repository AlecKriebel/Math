# Minimal 2-SAT bicycles at \(k=3\): component paths and two closure exclusions

## Status and exact boundary

Date: 2026-07-26 (PDT)

All graph statements in this note use the standard one-guard-moves eternal
domination model.  Attacks are made only at unoccupied vertices, exactly one
occupied adjacent guard moves, and every state retained in an eternal family
dominates.

This note studies an inclusion-minimal unsatisfiable subformula of the exact
no-full-list 2-SAT instance from
`math/working/k3_projection_gluing.md`.  The main outcomes are:

1. **PROVED:** every inclusion-minimal unsatisfiable 2-CNF has one of three
   exact terminal forms: a chain between two forced literals, a one-unit
   literal-to-complement lollipop, or a unit-free pair of opposite
   implication paths.
2. **PROVED:** in a response-list formula, every implication path expands
   into alternating complement edges and paths inside frozen projection
   components.  The parity of every internal connector is determined by
   whether its two collision colors agree.
3. **PROVED:** full one-guard closure forbids a canonical vertex- and
   edge-minimal realization of the one-unit lollipop.
4. **PROVED:** full one-guard closure also forbids a canonical vertex- and
   edge-minimal realization of the unit-free two-variable bicycle.
5. **EXACT CHECK:** `GFznc{` has a 35-state eternal triple-family whose
   no-full-list formula is unsatisfiable at both ends of an actual
   independent-state ridge.  Ridge covariance acts nonvacuously and
   transports the unsatisfiable instance.  This graph has
   \[
     (\gamma,\alpha,\gamma^\infty,\theta)=(2,3,3,3),
   \]
   so the missing hypothesis is again \(\gamma=3\).
6. **OBSERVED BOUNDED FALSIFICATION:** an exact order-eight scan found no
   unit-free family-list obstruction among the tested equality graphs or
   the larger \(\gamma=2,\alpha=\gamma^\infty=3\) near-host slice.

Items 3 and 4 exclude exact canonical geometries, not their arbitrary
subdivisions.  No theorem here says that every bicycle contains the mixed
\(P_4\), that the two end-witness systems must overlap, or that a longer
bicycle is impossible.  The \(k=3\) slice and the universal
\(\gamma\)--\(\theta\) conjecture remain open.

The following predecessor and concurrent proof notes, together with the
listed hostile reviews, were read in full before this note was frozen:

- `math/working/universal_complement_local_balance_attack.md`;
- `math/working/cross_state_response_exchange.md`;
- `math/working/cross_state_base_orderability_obstruction.md`;
- `math/working/k3_cross_state_attack.md`;
- `math/working/k3_mixed_p4_attack.md`;
- `math/working/k3_mixed_witness_followup.md`;
- `math/working/k3_projection_gluing.md`;
- `math/working/forced_c5_contradiction/NOTE.md`;
- `reviews/universal_complement_local_balance_attack_hostile/REVIEW.md`;
- `reviews/universal_transition_hall_hostile_review/REVIEW.md`;
- `reviews/cross_state_exchange_hostile/REVIEW.md`;
- `reviews/k3_mixed_p4_hostile/REVIEW.md`;
- `reviews/k3_mixed_witness_followup_hostile/REVIEW.md`; and
- `reviews/k3_projection_gluing_hostile/REVIEW.md`.

No literature-priority claim is made.

## 1. The exact response formula

Let \(\mathcal F\) be an arbitrary specified eternal family of triples,
let

\[
  S=\{a,b,c\}\in\mathcal F
\]

be independent, and put \(H=\overline G\).  For \(x\notin S\), write

\[
  L(x)=L^{\mathcal F}_S(x)
  =\{u\in S:ux\in E(G),\ S-u+x\in\mathcal F\}.
\tag{1.1}
\]

Because \(S\) is independent, family membership of a direct swap already
forces the missing graph edge: if \(S-u+x\in\mathcal F\), that state must
dominate \(u\), while no member of \(S-\{u\}\) sees \(u\).  Hence
\(ux\in E(G)\), and

\[
  S-u+x\in\mathcal F
  \quad\Longleftrightarrow\quad
  u\in L(x).
\tag{1.1a}
\]

Throughout the formula analysis, assume

\[
  1\leq |L(x)|\leq2
  \qquad(x\notin S).
\tag{1.2}
\]

For \(u\in S\), let

\[
  B_u=H[(S-\{u\})\cup W_u],
  \qquad
  W_u=\{x\notin S:u\notin L(x)\}.
\tag{1.3}
\]

The accepted frozen-color theorem makes every \(B_u\) bipartite.  Fix a
bipartition coordinate \(\pi_u\) on each component.  Its anchor component
has a fixed orientation; every other component \(K\) has a flip variable

\[
  z_{u,K}\in\{0,1\}.
\tag{1.4}
\]

Order the two remaining colors as

\[
  S-\{u\}=\{r_u^0,r_u^1\},
\]

and let \(\iota_u(w)\) be the index of \(w\) in this ordering.

### Port literals

Suppose \(L(x)=S-\{u\}\) and \(x\in K\).  For
\(w\in S-\{u\}\), define the **port event**

\[
  P(x,w):\quad
  z_{u,K}=\pi_u(x)\oplus\iota_u(w).
\tag{1.5}
\]

This is exactly the event that the oriented projection assigns color \(w\)
to \(x\).

If \(xy\in E(H)\), the lists are

\[
  L(x)=S-\{u\},\qquad L(y)=S-\{v\},\qquad u\ne v,
\]

and \(w\) is their common color, then the cross-projection clause is

\[
  \neg P(x,w)\ \lor\ \neg P(y,w).
\tag{1.6}
\]

Its two implication arcs are

\[
  P(x,w)\longrightarrow\neg P(y,w),
  \qquad
  P(y,w)\longrightarrow\neg P(x,w).
\tag{1.7}
\]

A singleton list \(L(s)=\{d\}\) imposes, in each projection \(B_u\) with
\(u\ne d\),

\[
  z_{u,K_u(s)}
  =\pi_u(s)\oplus\iota_u(d).
\tag{1.8}
\]

After substituting fixed anchor-component orientations and deleting
logical duplicates, equations (1.6) and (1.8) are the formula
\(\Phi_S\).  A violated fixed-component requirement is a
projection-internal parity certificate and needs no 2-SAT bicycle.  The
rest of this note concerns a nonconstant inclusion-minimal unsatisfiable
subformula of \(\Phi_S\).

## 2. Exact terminal classification of a minimal 2-CNF

A literal will be written as \(p\), with its complement \(\bar p\).  For a
binary 2-CNF \(B\), let \(I(B)\) be its implication digraph.  Every
implication path has a contraposed path:

\[
  p\leadsto q
  \quad\Longrightarrow\quad
  \bar q\leadsto\bar p.
\tag{2.1}
\]

### Theorem 2.1 (minimal-unsatisfiable terminal trichotomy) — PROVED

Let \(F\) be an inclusion-minimal unsatisfiable 2-CNF after tautologies and
duplicate clauses have been removed and every repeated-variable binary
clause has been simplified to a unit or tautology.  Let \(U\) be its unit
clauses and \(B=F-U\) its binary clauses.  Exactly one of the following
descriptions applies.

1. **Two-unit chain.**  The formula has two unit clauses \(p,q\).  There is
   a simple implication path
   \[
     p\leadsto\bar q
     \quad\text{or}\quad
     q\leadsto\bar p
   \tag{2.2}
   \]
   whose set of binary clauses is all of \(B\).
2. **One-unit lollipop.**  The formula has one unit clause \(p\).  There is
   a simple implication path
   \[
     p\leadsto\bar p
   \tag{2.3}
   \]
   whose set of binary clauses is all of \(B\).
3. **Unit-free bicycle.**  The formula has no units.  For some literal
   \(p\), there are simple implication paths
   \[
     p\leadsto\bar p,\qquad
     \bar p\leadsto p
   \tag{2.4}
   \]
   whose combined set of binary clauses is all of \(B\).

In particular,

\[
  |U|\leq2.
\tag{2.5}
\]

The paths need not be unique.  One binary clause can supply an implication
arc in more than one place, so the statement concerns the set of clauses
used, not a claim that every clause occurs once.  A path is allowed to have
length zero; this includes the minimal formula consisting only of two
contradictory unit clauses.

#### Proof

If \(B\) itself is unsatisfiable, minimality of \(F\) makes every unit
clause redundant.  Hence \(U=\varnothing\), and the standard 2-SAT
criterion gives a literal \(p\) with both paths in (2.4).  Choose each path
simple.  The clauses on their union already form an unsatisfiable
subformula; inclusion-minimality says their union uses every clause of
\(F=B\).  This is case 3.

Now suppose \(B\) is satisfiable but \(B\cup U\) is not.  Close the forced
unit literals under reachability in \(I(B)\).  The closure contains some
literal \(x\) and \(\bar x\).  Thus there are unit literals \(p,q\in U\),
possibly the same literal, with

\[
  p\leadsto x,\qquad q\leadsto\bar x.
\]

Contraposing the second path gives

\[
  x\leadsto\bar q,
\]

and therefore

\[
  p\leadsto\bar q.
\tag{2.6}
\]

The units \(p,q\) and the clauses on a simple version of (2.6) already form
an unsatisfiable subformula.  Minimality implies that no third unit exists
and that the path uses every binary clause.

If \(p,q\) are distinct unit clauses, this is case 1.  If only one unit
clause \(p\) is involved, equation (2.6) is
\(p\leadsto\bar p\), giving case 2.  These cases exhaust the formula.
\(\square\)

### Interpretation for response lists

The unit count in Theorem 2.1 is the number of unit **constraints selected
by the logical core**.  It is not necessarily the number of singleton
vertices.  One singleton response vertex supplies two projection units;
one or both may be redundant to a selected minimal core.  Conversely, the
two terminal units of a two-unit chain can come from the same physical
singleton marker in two different frozen projections.  A cross clause can
also simplify to a unit after a fixed anchor-component orientation is
substituted, so singleton markers are not an exhaustive taxonomy of the
physical sources of terminal units.

The mixed

\[
  \{a\},\{a,c\},\{b,c\},\{b\}
\]

complement \(P_4\) is the shortest cross-projection two-unit chain: two
units and one binary clause.  Theorem 2.1 shows that it is not the only
logical geometry that must be considered.

## 3. Expanding an implication path back into \(H\)

### Theorem 3.1 (component-connector parity law) — PROVED

Suppose two consecutive cross clauses on an implication path meet the same
projection variable \(z_{u,K}\).  Let their ports in \(K\) be
\((x,w)\) and \((y,w')\).  To continue the implication path through the
component, the two port events must be complements.  Equivalently,

\[
  \pi_u(x)\oplus\pi_u(y)
  =
  1\oplus\iota_u(w)\oplus\iota_u(w').
\tag{3.1}
\]

Every \(x\)--\(y\) path in \(B_u[K]\), and in particular a shortest one,
therefore has parity

\[
  \operatorname{dist}_{B_u}(x,y)
  \equiv
  \begin{cases}
    1\pmod2,&w=w',\\
    0\pmod2,&w\ne w'.
  \end{cases}
\tag{3.2}
\]

At a singleton terminal \(s\) with \(L(s)=\{d\}\), a first or last port
\((x,w)\) agrees with the forced unit precisely when

\[
  \operatorname{dist}_{B_u}(s,x)
  \equiv
  \iota_u(d)\oplus\iota_u(w)
  \pmod2.
\tag{3.3}
\]

Thus the connector is even when \(d=w\) and odd when \(d\ne w\).

#### Proof

The event \(P(x,w)\) is

\[
  z_{u,K}=\pi_u(x)\oplus\iota_u(w).
\]

After traversing a cross clause, equation (1.7) produces the complement of
the arrival port event.  For the next cross clause to use \(P(y,w')\) as
its tail, one needs

\[
  \pi_u(y)\oplus\iota_u(w')
  =
  1\oplus\pi_u(x)\oplus\iota_u(w),
\]

which is (3.1).  In a bipartite component, path-length parity is the
difference of the endpoint bipartition coordinates, proving (3.2).

At a singleton marker, equation (1.8) must equal the port value in (1.5).
Cancelling the common flip variable gives (3.3). \(\square\)

### Type-turn form

A variable in \(B_u\) has type \(u\).  Cross clauses join distinct types.
At a type sequence

\[
  v,\ u,\ t,
\]

the two collision colors at the middle component agree exactly when
\(v=t\).  Hence:

- an \(u\)-connector at an \(vuv\) turn is odd;
- an \(u\)-connector at a turn using all three types is even.

Every implication chain therefore expands into an alternating walk made of:

1. cross edges of \(H\) between vertices with distinct two-lists; and
2. parity-prescribed paths inside one bipartite frozen component.

A shortest internal connector is an induced path in its projection.
Nothing here makes the **whole** expanded walk induced.  Different
connectors can intersect, one component can recur, and extra complement
edges can form chords.  A minimal formula is a statement about essential
clauses, not a theorem that its physical realization is a hole.

### No necessary end-witness overlap

The end-witness cliques and the forced \(C_5\) in
`k3_mixed_witness_followup.md` and
`forced_c5_contradiction/NOTE.md` arise from the shortest two-unit mixed
\(P_4\).  In that exact geometry, the latter note proves

\[
  P_L\cap P_R=\varnothing.
\tag{3.4}
\]

Thus overlap is not merely unnecessary there: it is dynamically
impossible.  Theorem 2.1 additionally permits:

- longer two-unit component chains;
- two units supplied by the same physical marker;
- a one-unit lollipop; and
- a unit-free bicycle.

These alternatives have no canonical pair of mixed-\(P_4\) ends.  In
particular, an inclusion-minimal 2-SAT bicycle does **not** by itself define,
let alone force an overlap of, the left and right domination-witness
systems.  When a reduction to the mixed path is available, the proved
conclusion is separation, not overlap.  Disjoint end witnesses are therefore
the forced mixed-path branch, while longer bicycles require their own
witness analysis.

## 4. Full closure excludes a canonical one-unit lollipop

The next theorem uses information absent from abstract 2-SAT, clique-wise
Hall, and frozen bipartiteness.

### Theorem 4.1 (tail-triangle exclusion) — PROVED

Let \(S=\{a,b,c\}\) be an independent state in an arbitrary eternal
triple-family \(\mathcal F\).  There do not exist distinct vertices

\[
  p,q,r,s\notin S
\]

such that

\[
  pq,qr,qs,rs\in E(H)
\tag{4.1}
\]

and

\[
  L(p)=\{a\},\qquad
  L(r)=L(s)=\{b,c\}.
\tag{4.2}
\]

No hypothesis on \(L(q)\) is needed.  Additional complement edges among
the displayed vertices do not invalidate the conclusion.

#### Proof

The positive list at \(p\) puts

\[
  D_0=\{b,c,p\}=S-a+p
\]

in \(\mathcal F\).  Attack the unoccupied vertex \(r\).

The guard at \(p\), if adjacent to \(r\), would produce
\(\{b,c,r\}=S-a+r\), which is absent because
\(a\notin L(r)\).  The only retained response can therefore be

\[
  D_b=\{b,p,r\}
  \quad\text{or}\quad
  D_c=\{c,p,r\},
\tag{4.3}
\]

obtained by moving \(c\) or \(b\), respectively.  We show that neither
state can belong to \(\mathcal F\).

From \(D_b=\{b,p,r\}\), attack the unoccupied vertex \(s\).
The guard at \(r\) cannot respond because \(rs\in E(H)\).

- The move \(b\to s\) gives \(\{p,r,s\}\), which does not dominate \(q\)
  because all three edges \(pq,qr,qs\) lie in \(H\).
- The move \(p\to s\), if that graph edge exists, gives
  \(\{b,r,s\}\).  Attack the unoccupied vertex \(c\) there.  The guard at
  \(b\) cannot move because \(S\) is independent.  The only possible
  successors are
  \[
    \{b,c,r\}=S-a+r,\qquad
    \{b,c,s\}=S-a+s,
  \]
  and both are absent because \(a\) belongs to neither list.

Thus \(D_b\) cannot answer the attack at \(s\).

The proof for \(D_c=\{c,p,r\}\) is symmetric.  The move \(c\to s\)
gives the same nondominating state \(\{p,r,s\}\).  A move \(p\to s\)
gives \(\{c,r,s\}\), which cannot answer the unoccupied attack at \(b\):
its only possible successors are again the two forbidden direct swaps.

Consequently neither response in (4.3) can be retained, contradicting
closure at \(D_0\).  Every attack used above is unoccupied and every
considered move changes exactly one guard along one graph edge. \(\square\)

### The canonical lollipop instance

Set

\[
\begin{array}{c|cccc}
x&p&q&r&s\\ \hline
L(x)&\{a\}&\{a,b\}&\{b,c\}&\{b,c\},
\end{array}
\tag{4.4}
\]

and let the required complement edges be the tail-triangle

\[
  pq,\quad qr,\quad qs,\quad rs.
\tag{4.5}
\]

The exact projection formula has a minimal core consisting of one unit and
two binary clauses.  The unit forces one orientation of the component
containing \(q\); the two clauses then force both orientations of the
component containing the \(H\)-edge \(rs\).  This is the canonical
one-unit lollipop.

Every frozen projection is bipartite, every complement clique satisfies
response-list Hall, and the list instance is vertex- and edge-minimal
uncolorable.  Theorem 4.1 shows that full closure nevertheless forbids it.
The proof is stronger than this exact list instance because it never uses
the list of \(q\).

## 5. Full closure excludes a canonical unit-free bicycle

### Theorem 5.1 (canonical two-variable bicycle exclusion) — PROVED

Let \(S=\{a,b,c\}\) be an independent state in an arbitrary eternal
triple-family \(\mathcal F\).  There do not exist distinct outside vertices

\[
  p,q,r,y,z
\]

with response lists

\[
  L(p)=L(q)=L(r)=\{a,b\},
  \qquad
  L(y)=L(z)=\{a,c\},
\tag{5.1}
\]

and complement edges

\[
  pq,pr,py,pz,qz,ry,yz\in E(H).
\tag{5.2}
\]

Again, additional complement edges only remove possible guard moves and do
not invalidate the proof.

#### Proof

From \(S\), attack the unoccupied vertex \(q\).  The direct successor made
by moving \(c\), if that graph edge exists, is absent because
\(c\notin L(q)\).  Closure must retain at least one of

\[
  A=\{a,c,q\},\qquad B=\{b,c,q\}.
\tag{5.3}
\]

We first show that \(A\) is impossible.  Attack \(y\) from \(A\).  A move
of \(q\), if legal, gives the absent direct swap
\(\{a,c,y\}=S-b+y\).  The two remaining successor shapes are

\[
  A_a=\{a,q,y\},\qquad A_c=\{c,q,y\}.
\]

From either state, attack \(p\).  The guards at \(q,y\) cannot respond
because \(pq,py\in E(H)\).  Any remaining response gives
\(\{p,q,y\}\), which does not dominate \(z\), since

\[
  pz,qz,yz\in E(H).
\]

Thus \(A\notin\mathcal F\).

Now consider \(B=\{b,c,q\}\), and attack \(z\).  The guard at \(q\)
cannot respond because \(qz\in E(H)\).  The possible retained successors
are

\[
  B_b=\{b,q,z\},\qquad B_c=\{c,q,z\}.
\]

From \(B_b\), attack \(r\).  There are at most three response shapes.

1. \(b\to r\) gives \(\{q,r,z\}\), which does not dominate \(p\), since
   \(pq,pr,pz\in E(H)\).
2. \(q\to r\), if legal, gives \(\{b,r,z\}\).  Attack \(p\).  Only the
   guard at \(b\) can respond, and the successor \(\{p,r,z\}\) does not
   dominate \(y\), since \(py,ry,yz\in E(H)\).
3. \(z\to r\), if legal, gives \(\{b,q,r\}\).  Attack \(a\).  The guard
   at \(b\) cannot respond because \(S\) is independent.  Moving \(q\) or
   \(r\) gives
   \[
     \{a,b,r\}=S-c+r,\qquad
     \{a,b,q\}=S-c+q,
   \]
   both absent because \(c\) belongs to neither list.

Hence \(B_b\notin\mathcal F\).

From \(B_c=\{c,q,z\}\), attack \(y\).  The guard at \(z\) cannot respond
because \(yz\in E(H)\).

- The move \(c\to y\) gives \(\{q,y,z\}\), which does not dominate \(p\)
  because \(pq,py,pz\in E(H)\).
- A move \(q\to y\), if legal, gives \(\{c,y,z\}\).  Attack \(a\).
  The guard at \(c\) cannot respond, and the other two moves give the
  forbidden direct swaps
  \[
    \{a,c,z\}=S-b+z,\qquad
    \{a,c,y\}=S-b+y.
  \]

Thus \(B_c\notin\mathcal F\).  Both branches in (5.3) are impossible, a
contradiction. \(\square\)

### Why this is the canonical unit-free bicycle

In the two frozen components, write the two flip variables as \(X,Y\).
Up to complementing either variable, the four cross edges

\[
  py,\quad pz,\quad qz,\quad ry
\]

give all four binary clauses

\[
\begin{split}
 &(X\lor Y),\qquad (X\lor\neg Y),\\
 &(\neg X\lor Y),\qquad(\neg X\lor\neg Y).
\end{split}
\tag{5.4}
\]

Their conjunction is unsatisfiable, while deleting any clause admits the
unique assignment falsifying that deleted clause.  There are no unit
constraints.  The remaining same-projection edges in (5.2) supply the
required port parities.

The instance satisfies every frozen bipartiteness and clique-Hall
condition.  Theorem 5.1 is therefore a genuinely dynamic exclusion, not a
restatement of those local conditions.

The theorem does **not** exclude a subdivision in which the four ports are
joined through longer paths inside their projection components, nor a
unit-free bicycle involving three or more flip variables.

## 6. Sharp counterboundary: nonvacuous covariance does not glue

The prior gluing countermodels had no pair of independent family states
sharing a ridge.  The following exact example removes that evidentiary
vacuity.

### Proposition 6.1 (`GFznc{`) — EXACT CHECK

Let

\[
  G=\texttt{GFznc\{}
\]

on vertices \(0,\ldots,7\), with complement edges

\[
  E(H)=
  \{01,02,12,17,27,34,35,46,56\}.
\tag{6.1}
\]

The following 35 triples form an eternal dominating family:

\[
\begin{split}
\mathcal F=\{&
012,015,016,024,026,036,045,046,056,\\
&123,124,125,127,135,136,145,146,156,157,167,\\
&234,236,245,246,247,256,267,\\
&345,346,356,367,456,457,467,567\}.
\end{split}
\tag{6.2}
\]

At

\[
  S=012,
\]

the exact family-response lists are

\[
\begin{array}{c|ccccc}
x&3&4&5&6&7\\ \hline
L_S(x)&
\{0\}&\{0,1\}&\{0,2\}&\{1,2\}&\{0\}.
\end{array}
\tag{6.3}
\]

At the ridge-adjacent independent state

\[
  T=127,
\]

they are

\[
\begin{array}{c|ccccc}
x&0&3&4&5&6\\ \hline
L_T(x)&
\{7\}&\{7\}&\{1,7\}&\{2,7\}&\{1,2\}.
\end{array}
\tag{6.4}
\]

Both instances have no full list and no compatible coloring.  The
transposition

\[
  \rho=(0\ 7)
\]

maps the lists in (6.3) exactly to those in (6.4):

\[
  \rho(L_S(x))=L_T(\rho(x))
  \qquad(x\notin S).
\tag{6.5}
\]

Thus response covariance is nonvacuous **on the unsatisfiable formulas
themselves**.  It transports the obstruction across the ridge rather than
eliminating it.

The exact parameters are

\[
  (\gamma,\alpha,\gamma^\infty,\theta)=(2,3,3,3).
\tag{6.6}
\]

Indeed, \(\{0,3\}\) dominates, no singleton dominates, and \(012\) is
independent.  The family (6.2) proves
\(\gamma^\infty\leq3\), while
\(\alpha\leq\gamma^\infty\) proves equality.  The clique partition

\[
  \{0,7\}\mid\{1,3,6\}\mid\{2,4,5\}
\tag{6.7}
\]

proves \(\theta\leq3\), and \(\alpha\leq\theta\) proves equality.

The independent checker verifies all

\[
  35(8-3)=175
\]

unoccupied state/attack obligations in (6.2).  The only independent family
states are \(012\) and \(127\), so (6.5) is the unique nontrivial ridge
transport in this family.

Consequently the following strengthening is **REFUTED**:

> full closure, arbitrary-state restoration, Hall, frozen projection
> bipartiteness, and nonvacuous ridge covariance force a no-full-list
> response formula to be satisfiable.

The example does not refute the equality-specific statement because it
fails exactly at \(\gamma=3\).

## 7. Bounded scan and exact remaining branch

The evidence script performed the following order-eight falsification scan:

1. enumerate all 11,117 connected unlabeled graphs;
2. retain graphs with
   \[
     \alpha=\gamma^\infty=3,\qquad
     \gamma\in\{2,3\};
   \]
3. at every independent reference triple having at least two possible
   direct family responses at every outside vertex, select every exact
   two-list restriction;
4. ban the unselected direct swaps and compute the greatest safe family;
5. test the resulting exact family lists for a global coloring.

The scan found no unit-free uncolorable response instance.  This is
**OBSERVED** bounded evidence from one script, not an order-eight theorem,
not an independently certified coverage result, and not a finite-frontier
advance.  Its useful role is to support the proof priority suggested by
Theorems 4.1 and 5.1: the unit-free branch appears dynamically fragile even
before \(\gamma=3\) is imposed.

The exact unresolved alternatives are now:

1. a longer two-unit component chain not reducible to the mixed \(P_4\);
2. a subdivided or multi-component one-unit lollipop escaping
   Theorem 4.1;
3. a subdivided or at-least-three-variable unit-free bicycle escaping
   Theorem 5.1; and
4. the full-list slice, which the frozen projections do not see.

The forced-\(C_5\) and end-witness separation mechanisms apply only after
the first alternative has actually been reduced to the mixed \(P_4\).  No
such general reduction is proved here.

## 8. Reproduction and claim ledger

Run:

```text
python3 -I -B -W error \
  gamma_theta_eternal_domination/math/working/k3_twosat_bicycle/evidence.py
```

The output is

`math/working/k3_twosat_bicycle/evidence.json`.

The script:

- exhausts all ordinary 2-CNFs on at most three variables and checks the
  terminal trichotomy;
- reconstructs both canonical local list obstructions and their exact
  projection formulas;
- verifies the two decreasing-rank named-attack policies used in
  Theorems 4.1 and 5.1;
- independently reconstructs `GFznc{`, its 35-state family, all 175
  obligations, both list tables, both unsatisfiable formulas, covariance,
  and all four parameters; and
- performs the bounded order-eight scan.

### PROVED

- Theorem 2.1: minimal-unsatisfiable terminal trichotomy.
- Theorem 3.1: projection component-connector parity.
- Theorem 4.1: canonical one-unit tail-triangle exclusion.
- Theorem 5.1: canonical unit-free two-variable bicycle exclusion.

### EXACT CHECK

- `GFznc{` and the 35-state nonvacuous covariance countermodel.
- The literal finite attack policies supporting Theorems 4.1 and 5.1.
- Exhaustive trichotomy falsification through three Boolean variables.

### OBSERVED

- No unit-free family-list obstruction in the bounded order-eight scan.

### OPEN

- Longer or subdivided lollipops and bicycles.
- A reduction of every two-unit chain to the mixed \(P_4\).
- A witness-system analogue of the mixed-path separation theorem for a
  general bicycle.
- The full-list slice.
- The \(k=3\) and universal \(\gamma\)--\(\theta\) conjectures.
