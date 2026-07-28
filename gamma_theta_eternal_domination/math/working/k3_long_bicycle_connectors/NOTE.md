# Odd subdivided lollipops in the \(k=3\) response geometry

## Status and exact boundary

Date: 2026-07-27 (PDT)

All statements use the standard one-guard-moves eternal domination model:
attacks are at unoccupied vertices, exactly one adjacent guard moves, and
every retained state dominates.

The main result is **PROVED**.  It strictly extends the canonical
tail-triangle exclusion in
`math/working/k3_twosat_bicycle/NOTE.md` from one connector edge to every
odd-length connector path.  It is insensitive to extra complement edges
and, crucially, does not interpret an absent response as a graph nonedge.

It does **not** exclude every abstract 2-SAT lollipop or bicycle.  To invoke
the theorem one must exhibit the stated physical vertices in the complement
graph.  In particular, this note does not prove that an arbitrary
implication walk can be made vertex-distinct, that different connectors do
not intersect, or that its two terminal cross edges share one physical
vertex \(q\).

## 1. Response lists

Let \(\mathcal F\) be an arbitrary specified eternal family of triples,
let

\[
  S=\{a,b,c\}\in\mathcal F
\]

be independent, and put \(H=\overline G\).  For \(x\notin S\), write

\[
  L_S^{\mathcal F}(x)
  =
  \{u\in S:ux\in E(G),\ S-u+x\in\mathcal F\}.
\tag{1.1}
\]

For an independent reference state, family membership alone implies the
edge in (1.1).  Indeed, if \(S-u+x\in\mathcal F\), that state must dominate
the omitted vertex \(u\); no member of \(S-\{u\}\) sees \(u\), so \(x\)
must see \(u\).  Consequently

\[
  S-u+x\in\mathcal F
  \quad\Longleftrightarrow\quad
  u\in L_S^{\mathcal F}(x).
\tag{1.2}
\]

We abbreviate the list to \(L(x)\).

## 2. Two dead-state lemmas

### Lemma 2.1 (one anchor and two \(a\)-avoiding vertices) — PROVED

Let \(x,y\notin S\) be distinct and suppose

\[
  a\notin L(x)\cup L(y).
\tag{2.1}
\]

For either \(h\in\{b,c\}\), the state

\[
  \{h,x,y\}
\tag{2.2}
\]

does not belong to \(\mathcal F\).

#### Proof

Let \(d\) be the other member of \(\{b,c\}\), and attack the unoccupied
vertex \(d\) from (2.2).  The guard at \(h\) cannot move because \(S\) is
independent.  If the guard at \(x\) moves, the successor is

\[
  \{h,d,y\}=S-a+y,
\]

which is absent by (1.2) and \(a\notin L(y)\).  If the guard at \(y\)
moves, the successor \(S-a+x\) is absent for the same reason.  Missing
graph edges only remove these possible responses.  Thus no retained
response exists. \(\square\)

### Lemma 2.2 (three \(a\)-avoiding vertices) — PROVED

Let \(x,y,z\notin S\) be distinct and suppose

\[
  a\notin L(x)\cup L(y)\cup L(z).
\tag{2.3}
\]

Then

\[
  \{x,y,z\}\notin\mathcal F.
\tag{2.4}
\]

#### Proof

Attack the unoccupied vertex \(b\).  Every possible one-guard successor
has the form \(\{b,r,s\}\), where \(r,s\) are two of \(x,y,z\).  Lemma 2.1
says that every such successor is absent.  Again, a missing move edge only
reduces the response set. \(\square\)

The proofs deliberately distinguish dynamic absence from nonadjacency:
we never infer a graph nonedge from a missing successor.

## 3. The odd subdivided-lollipop exclusion

### Theorem 3.1 (odd fan-path exclusion) — PROVED

Let \(S=\{a,b,c\}\) be an independent state in an arbitrary eternal
triple-family \(\mathcal F\).  There do not exist distinct outside vertices

\[
  p,q,v_0,v_1,\ldots,v_m
\]

for an odd integer \(m\geq1\) such that

\[
  a\in L(p),\qquad a\notin L(v_i)\quad(0\leq i\leq m),
\tag{3.1}
\]

and

\[
  pq,\ qv_0,\ qv_m,\ v_0v_1,\ v_1v_2,\ldots,v_{m-1}v_m
  \in E(H).
\tag{3.2}
\]

No hypothesis on \(L(q)\) is needed.  The displayed path need not be
induced, and arbitrary additional complement edges among the displayed
vertices are allowed.

#### Proof

By \(a\in L(p)\),

\[
  D_0=S-a+p=\{b,c,p\}\in\mathcal F.
\tag{3.3}
\]

Attack \(v_0\).  A move by \(p\), if available, gives
\(\{b,c,v_0\}=S-a+v_0\), which is absent because \(a\notin L(v_0)\).
Closure therefore retains a response by \(b\) or \(c\).  Thus, for some
\(h\in\{b,c\}\),

\[
  \{h,p,v_0\}\in\mathcal F.
\tag{3.4}
\]

Attack \(v_1\) from (3.4).  The guard at \(v_0\) cannot move because
\(v_0v_1\in E(H)\).  A move by \(p\), if available, gives
\(\{h,v_0,v_1\}\), which is absent by Lemma 2.1.  Hence the only retained
response must move \(h\), and

\[
  P_{0,1}:=\{p,v_0,v_1\}\in\mathcal F.
\tag{3.5}
\]

We record two kinds of forbidden \(P\)-states.  First, whenever the indices
exist,

\[
  P_{i,i+2}:=\{p,v_i,v_{i+2}\}\notin\mathcal F.
\tag{3.6}
\]

To see this, attack \(v_{i+1}\).  Neither path guard can move, by the two
consecutive complement edges.  A move by \(p\), if available, creates
\(\{v_i,v_{i+1},v_{i+2}\}\), which is absent by Lemma 2.2.

Second,

\[
  P_{0,m}:=\{p,v_0,v_m\}\notin\mathcal F,
\tag{3.7}
\]

because it does not dominate \(q\): all three pairs \(pq,qv_0,qv_m\)
are complement edges.

If \(m=1\), equations (3.5) and (3.7) already contradict one another.
Assume \(m\geq3\).  Attack \(v_m\) from \(P_{0,1}\).  A move by \(p\)
leads to a three-\(v\) state forbidden by Lemma 2.2.  A move by \(v_1\)
leads to the nondominating state \(P_{0,m}\).  Closure therefore forces

\[
  P_{1,m}\in\mathcal F.
\tag{3.8}
\]

Here and below, if an additional complement edge removes the asserted
move, closure fails even earlier; it never creates a new response.

Because \(m\) is odd, repeatedly apply the following forcing step.  From
\(P_{1,t}\), where \(t\geq5\) is odd, attack \(v_{t-2}\).

- Moving \(p\) creates a forbidden three-\(v\) state.
- Moving \(v_1\) creates the distance-two state \(P_{t-2,t}\), forbidden
  by (3.6).
- Thus closure forces \(v_t\) to move and retains \(P_{1,t-2}\).

Starting with \(t=m\), this gives

\[
  P_{1,m},P_{1,m-2},\ldots,P_{1,3}\in\mathcal F.
\tag{3.9}
\]

But \(P_{1,3}\) is itself a distance-two state forbidden by (3.6), a
contradiction.  Every attack in the argument is at an unoccupied vertex,
and every possible successor considered changes exactly one guard.
\(\square\)

### Corollary 3.2 (canonical theorem and all odd subdivisions) — PROVED

Theorem 4.1 of `math/working/k3_twosat_bicycle/NOTE.md` is the case
\(m=1\), with \(v_0=r,v_1=s\) and the stronger listed assumptions
\(L(p)=\{a\}\), \(L(r)=L(s)=\{b,c\}\).

More generally, the same contradiction holds after replacing the
complement edge \(rs\) by any odd path whose vertices all omit \(a\) from
their family-response lists, while retaining a common complement neighbor
\(q\) at the two ends.  Exact two-list equality is unnecessary.

### Exact map back to a minimal 2-SAT lollipop

In the notation of the predecessor note, the theorem covers the following
physical expansion of the **canonical one-unit, two-binary-clause core**.

1. The unit-support vertex is \(p\), and its required positive response is
   \(a\in L(p)\).
2. The complement edge \(pq\) is the unit tail.
3. The two terminal cross-clause edges are \(qv_0\) and \(qv_m\); in
   particular, the same physical port vertex \(q\) occurs in both.
4. The repeated projection variable is expanded inside \(W_a\) as the
   component path \(v_0\ldots v_m\).  Thus every path vertex omits \(a\).
5. The component-connector parity law makes this path odd when the two
   collision colors agree.  Every such odd subdivision is excluded,
   independently of chords or other additional complement edges.

The theorem does not yet cover a general one-unit implication path
\(z\leadsto\bar z\) using three or more binary clauses, because its
successive cross clauses can use different physical port vertices and
different frozen components.  It also does not cover a realization in
which the expanded walk repeats a vertex, the two terminal clauses use
different \(q\)-vertices, or the connector leaves \(W_a\).  The other two
minimal-2SAT terminal types remain separate: longer two-unit chains and
unit-free opposite implication paths are not consequences of Theorem 3.1.

## 4. Why the parity is a real boundary

The proof cannot be extended mechanically to even \(m\).  Abstract away
the dead \(p\)-moves and represent \(P_{i,j}\) by the two-token set
\(\{i,j\}\) on the path indices.  Consecutive indices are forbidden move
edges.  For even \(m\), the family

\[
  \mathcal C_{\mathrm{par}}
  =
  \{\{i,j\}:i\not\equiv j\pmod2\}
\tag{4.1}
\]

is closed under every unoccupied attack: if the attacked index \(k\) has
the parity of one token, move that token to \(k\) and retain the token of
opposite parity.  The moved token is at a nonzero even distance from
\(k\), hence not on a forbidden consecutive path edge.  Since \(m\) is
even, the nondominating endpoint pair \(\{0,m\}\) is not in
\(\mathcal C_{\mathrm{par}}\).

Thus even connector length has an equality-compatible *transition
abstraction*.  This is not asserted to be a graph counterexample or even
to lift to a dominating eternal family.  It proves only that a successful
even-path argument must use information beyond the attack mechanism in
Theorem 3.1.

For odd \(m\), the endpoint pair has opposite parity, so this escape is
destroyed.  The forcing chain in (3.8)--(3.9) is the concrete reason.

## 5. Exact controls and failed contraction

Two accepted gamma-two controls were replayed against the exact hypotheses.

- For `GFznc{`, using its checked 35-state family, both independent
  reference states and every possible odd path on the remaining vertices
  were enumerated.  There are zero embeddings of Theorem 3.1.
- For the exact 21-state mixed-\(P_4\) family in `FDzro`, every independent
  reference state and every possible odd path were likewise enumerated.
  There are zero embeddings of Theorem 3.1.

This is the intended outcome.  `GFznc{` realizes a two-unit chain with
nontrivial ridge covariance, and `FDzro` realizes the mixed two-unit
\(P_4\); neither is the one-unit fan-path geometry excluded here.  Both
retain \(\gamma=2\), so neither is a gamma--theta counterexample.

The tempting broader connector contraction remains invalid.  Along a
frozen component path, an absent family response can mean either:

1. the proposed guard move is a graph nonedge; or
2. the move edge exists but its successor is dynamically absent from
   \(\mathcal F\).

Only the first interpretation transports adjacency.  The proof above
avoids this ambiguity by classifying every non-\(P\) successor as an
already forbidden family state.  What remains open is a comparable
classification for:

- even fan-path connectors;
- paths containing vertices whose list includes \(a\);
- repeated or intersecting physical connectors;
- longer two-unit chains; and
- unit-free bicycles with more than the canonical two variables.

No literature-priority claim is made.
