# Hostile review: odd subdivided lollipop connector

Date: 2026-07-27 (PDT)

## Target and verdict

Target:

`math/working/k3_long_bicycle_connectors/NOTE.md`

SHA-256:

`d3a23bb0171a047a85f2a05c5ccb5faeef0c0c7ceb6d7bb139c6a7a86b8b1f10`

Verdict:

**PASS.** Lemmas 2.1 and 2.2 and Theorem 3.1 are valid as stated in the
standard one-guard-moves model.  I found no missing successor, occupied
attack, all-guards move, complement confusion, or inference from dynamic
family absence to graph nonadjacency.  The exact map to the canonical
one-unit/two-binary-clause lollipop is correct and its limitations are stated
accurately.  No correction is required for these claims.

This verdict does not promote the theorem to an exclusion of arbitrary
2-SAT lollipops or bicycles.  The physical hypotheses in Theorem 3.1,
especially the one common terminal vertex \(q\), the vertex-distinct odd
path, and omission of \(a\) by every path vertex, remain essential to its
present scope.

## Independent reconstruction

Let \(S=\{a,b,c\}\in\mathcal F\) be independent.  For any outside \(x\),
membership of \(S-u+x\) in \(\mathcal F\) forces \(ux\in E(G)\): the
successor must dominate the omitted \(u\), while the other two members of
\(S\) are nonneighbors of \(u\).  Hence

\[
S-u+x\in\mathcal F\quad\Longleftrightarrow\quad u\in L(x).
\]

This equivalence is about a direct successor of the independent reference
state.  It does not equate absence from \(\mathcal F\) with a graph
nonedge.

### Lemma 2.1

Assume \(a\notin L(x)\cup L(y)\) and hypothetically retain
\(\{h,x,y\}\), where \(h\in\{b,c\}\).  Let \(d\) be the other anchor.
The attack at \(d\) is unoccupied.  Its complete successor list is:

\[
\begin{array}{c|c|c}
\text{moving guard}&\text{successor}&\text{reason unavailable}\\ \hline
h&\{d,x,y\}&hd\notin E(G),\text{ since }S\text{ is independent}\\
x&\{h,d,y\}=S-a+y&S-a+y\notin\mathcal F\\
y&\{h,d,x\}=S-a+x&S-a+x\notin\mathcal F.
\end{array}
\]

For the last two rows the move edge may exist; the proof only uses absence
of the successor from the family.  If either move edge is absent, there are
fewer responses.  Thus the hypothetical state cannot be in
\(\mathcal F\).

### Lemma 2.2

Assume three distinct outside vertices \(x,y,z\) all omit \(a\), and
hypothetically retain \(\{x,y,z\}\).  Attack the unoccupied \(b\).  Moving
any one of the three guards yields \(\{b,r,s\}\) for a pair
\(\{r,s\}\subset\{x,y,z\}\).  Lemma 2.1, with \(h=b\), excludes all three
successors.  These are all legal one-guard successor shapes, so the
hypothetical state is impossible.

### Theorem 3.1

The positive response \(a\in L(p)\) retains

\[
D_0=\{b,c,p\}.
\]

Attack \(v_0\).  A \(p\)-move, if its graph edge exists, reaches the absent
direct swap \(S-a+v_0\).  Therefore one of \(b,c\) must move, retaining
\(\{h,p,v_0\}\) for the other anchor \(h\).  Attack \(v_1\).  The
\(v_0\)-move is blocked by \(v_0v_1\in E(H)\); a \(p\)-move reaches a
Lemma 2.1 dead state; hence the \(h\)-move is forced and

\[
P_{0,1}=\{p,v_0,v_1\}\in\mathcal F.
\]

For every valid \(i\), the state

\[
P_{i,i+2}=\{p,v_i,v_{i+2}\}
\]
is absent: attack \(v_{i+1}\), observe that both path guards are blocked by
the two consecutive complement edges, and observe that the only remaining
successor is a Lemma 2.2 dead triple.  Independently,

\[
P_{0,m}=\{p,v_0,v_m\}
\]
is absent because none of its guards dominates \(q\).

The endpoint cases are exhaustive:

- \(m=1\): \(P_{0,1}\) is both retained and equal to the nondominating
  \(P_{0,m}\).
- \(m=3\): attacking \(v_3\) from \(P_{0,1}\) eliminates the \(p\)-move by
  Lemma 2.2 and the \(v_1\)-move by nondomination of \(q\), so it forces
  \(P_{1,3}\), which is a forbidden distance-two state.
- \(m=5\): the same endpoint attack forces \(P_{1,5}\).  Attacking \(v_3\)
  eliminates the \(p\)-move by Lemma 2.2 and the \(v_1\)-move via forbidden
  \(P_{3,5}\), so it forces forbidden \(P_{1,3}\).

For arbitrary odd \(m\geq5\), the \(m=5\) step repeats with
\(t=m,m-2,\ldots,5\).  From retained \(P_{1,t}\), attack the unoccupied
\(v_{t-2}\).  The three and only three successor shapes are:

\[
\begin{array}{c|c|c}
\text{moving guard}&\text{successor}&\text{status}\\ \hline
p&\{v_1,v_{t-2},v_t\}&\text{dead by Lemma 2.2}\\
v_1&P_{t-2,t}&\text{dead distance-two state}\\
v_t&P_{1,t-2}&\text{therefore forced}.
\end{array}
\]

The odd index sequence terminates at \(P_{1,3}\), contradicting the
distance-two exclusion.

Every attack above is visibly outside the current triple, and each
successor replaces exactly one guard.  The proof is monotone under extra
complement edges: such an edge can delete a candidate guard move or make a
state fail domination, but cannot add a response.  Accordingly, chords and
other extra complement edges cannot invalidate the contradiction.

## Dynamic absence audit

The argument uses the following two logically distinct facts:

1. displayed complement edges rule out particular guard moves; and
2. response-list omissions and the dead-state lemmas rule out family
   membership of particular successors, whether or not their move edges
   exist.

No step converts item 2 into item 1.  The recurring language “if
available” is necessary and sufficient: if the edge exists, the successor
is absent; if it does not, that response is unavailable already.

## Map to the 2-SAT lollipop

The mapping to the predecessor note checks out:

- \(p\) supplies the selected unit response \(a\in L(p)\);
- \(pq\) is the physical unit-tail connector;
- \(qv_0\) and \(qv_m\) are the two terminal cross-clause edges and use the
  same physical port \(q\);
- the repeated nonanchor projection variable has a component connector
  \(v_0\ldots v_m\) inside \(W_a\), so every connector vertex omits \(a\);
  and
- equal collision colors force this connector to have odd parity.

A shortest component connector supplies the distinct simple path needed by
the theorem.  Because it represents a nonanchor flip variable, it lies in
\(W_a\), rather than passing through the fixed anchors \(b,c\).

This map does not show that a general implication walk has one common
terminal \(q\), remains inside a single \(W_a\) component, avoids repeated
physical vertices, or has only two binary clauses.  The source note
explicitly preserves all of those gaps, so it does not overstate the
consequence.

## Independent finite audit

`independent_sat_check.py` imports no campaign transition or search core.
For each tested \(m\), it introduces independent variables for all graph
edges and all triple-family memberships and directly encodes:

- \(S\in\mathcal F\), independence of \(S\), and the exact response-list
  membership assumptions;
- all required complement edges;
- domination of every retained triple; and
- every unoccupied attack with an existential response formed by one
  adjacent guard move to a retained successor.

CaDiCaL 3.0.1 reported UNSAT for the unrestricted graph/family instances
at \(m=1,3,5\).  As a polarity control, deleting only the terminal
complement constraint \(qv_m\in E(H)\) made all three instances SAT.
Instance hashes and counts are in `check_result.json`.

Reproduce with:

```text
python3 -I -B -W error \
  gamma_theta_eternal_domination/reviews/\
k3_long_bicycle_connectors_hostile/independent_sat_check.py
```

The finite solver runs are independent sanity checks, not proof
certificates for the infinite theorem.  The PASS verdict rests on the
complete symbolic successor exhaustion above.
