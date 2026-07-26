# Base-orderability of the two-state exchange system

## Status

Date: 2026-07-26 (PDT)

This note follows Theorem 2.1 of
`math/working/cross_state_response_exchange.md`.  It asks whether the two
abstract expansion/restoration axioms force a single bijection between two
independent family states whose every partial exchange remains in the
family.

The answer is **no**.  The smallest possible rank of a counterexample is
three, and a smallest rank-three counterexample has twelve states.  It is
realized by a genuine one-guard eternal family on
\(K_{3,3}\) with one edge deleted.  That realization has

\[
 \gamma=2<\alpha=\gamma^\infty=\theta=3,
\]

so it fails exactly the static equality required of a conjecture
counterexample.

The stronger hope that \(\gamma=\alpha=3\) forces pairwise reciprocity
between complementary exchanges is also **refuted** below by the equality
graph `FCXfO`.  That equality graph still has a base ordering.  Whether
every two independent triples in an eternal family satisfying
\(\gamma=\alpha=3\) admit at least one base ordering remains open.

No literature-priority claim is made.

## 1. Abstract exchange systems

Let \(A\) and \(B\) be disjoint sets of size \(m\geq1\).  An abstract two-state
exchange system is a set

\[
 \mathcal Q\subseteq
 \{(U,X):U\subseteq A,\ X\subseteq B,\ |U|=|X|\}
\tag{1.1}
\]

which contains \((\varnothing,\varnothing)\) and \((A,B)\), and satisfies:

1. for every \((U,X)\in\mathcal Q\) and \(b\in B-X\), there is
   \(a\in A-U\) with
   \[
   (U+a,X+b)\in\mathcal Q;
   \tag{1.2}
   \]
2. for every \((U,X)\in\mathcal Q\) and \(a\in U\), there is
   \(b\in X\) with
   \[
   (U-a,X-b)\in\mathcal Q.
   \tag{1.3}
   \]

These are exactly the abstract conclusions of the target-expansion and
source-restoration parts of Theorem 2.1.  Graph edges are suppressed in
this section.

Call \(\mathcal Q\) **base-orderable** if there is a bijection
\(\phi:A\to B\) such that

\[
 (U,\phi(U))\in\mathcal Q
 \qquad\text{for every }U\subseteq A.
\tag{1.4}
\]

Thus one Boolean subcube of paired mixed states lies inside
\(\mathcal Q\).

### Proposition 1.1 (ranks at most two are base-orderable) — PROVED

Every abstract exchange system with \(m\leq2\) is base-orderable.

#### Proof

Rank one is immediate.  Let \(m=2\), and join \(a\in A\) to \(b\in B\)
when \((\{a\},\{b\})\in\mathcal Q\).

Expansion from \((\varnothing,\varnothing)\) gives every vertex of \(B\)
a neighbor.  Restoration from \((A,B)\), once for each attacked member of
\(A\), gives every vertex of \(A\) a neighbor.  A bipartite graph with two
vertices on each side and no isolated vertex has a perfect matching.
The matching supplies the two singleton states required by (1.4), while
the empty and full states are already present. \(\square\)

## 2. A cardinality-minimal rank-three obstruction

Put

\[
 A=\{a,b,c\},\qquad B=\{x,y,z\}.
\tag{2.1}
\]

For rank three, encode the level-one states by

\[
 E=\{(p,q):(\{p\},\{q\})\in\mathcal Q\},
\tag{2.2}
\]

and encode the level-two states by their missing pair:

\[
 F=\{(p,q):(A-\{p\},B-\{q\})\in\mathcal Q\}.
\tag{2.3}
\]

Take

\[
\begin{aligned}
 E&=\{ay,az,bx,by,cx\},\\
 F&=\{ay,az,bz,cx,cy\}.
\end{aligned}
\tag{2.4}
\]

Together with the empty and full states, these ten middle states define a
twelve-state system \(\mathcal Q_0\).

In configuration notation, where \((U,X)\) represents
\((A-U)\cup X\), its states are

\[
\begin{split}
\mathcal Q_0=\{&
abc,\\
&bcy,bcz,acx,acy,abx,\\
&axz,axy,bxy,cyz,cxz,\\
&xyz\}.
\end{split}
\tag{2.5}
\]

### Proposition 2.1 — PROVED

\(\mathcal Q_0\) satisfies (1.2) and (1.3), but it is not
base-orderable.

#### Proof

The legal-response table in Section 3 verifies both abstract axioms, with
actual graph edges as well.

For the obstruction, a base ordering in rank three is exactly a perfect
matching contained in \(E\cap F\).  Indeed, its singleton states require
\((p,\phi(p))\in E\), while its complementary two-element states require
\((p,\phi(p))\in F\).  Conversely, a perfect matching in \(E\cap F\)
supplies all eight subsets in (1.4).

Here

\[
 E\cap F=\{ay,az,cx\},
\tag{2.6}
\]

which leaves \(b\) isolated.  It has no perfect matching. \(\square\)

### Proposition 2.2 (minimum rank and minimum cardinality) — PROVED

The system \(\mathcal Q_0\) has the smallest possible rank of an abstract
counterexample.  At rank three, every non-base-orderable exchange system
has at least twelve states.

#### Proof

Proposition 1.1 proves the rank assertion.

For the cardinality assertion, use the relations \(E,F\) in (2.2)--(2.3)
for an arbitrary rank-three system.  Expansion from the empty state says
that \(E\) has no empty column.  Restoration from the full state says that
\(F\) has no empty row.

In fact neither relation has an isolated vertex on either side.  To see
that \(E\) has no empty row \(d\), choose \(p\ne d\) and an edge \(pq\in F\).
In the corresponding level-two state, restore the other member of
\(A-\{p,d\}\).  The remaining level-one state has removed vertex \(d\), so
it gives an edge of \(E\) in row \(d\).  Dually, to see that \(F\) has no
empty column \(q\), choose a different column \(b\), an edge \(ab\in E\),
and expand that state at the third target in \(B-\{b,q\}\).

Suppose \(|E|\leq4\).  If \(|E|=3\), the no-isolate condition makes \(E\)
a perfect matching, say \(a\mapsto\phi(a)\).  For any \(pq\in F\),
restoration requires both other rows of \(E\) to have a neighbor outside
column \(q\).  Hence \(q=\phi(p)\).  Thus \(F\subseteq E\); since \(F\)
has no empty row, \(F=E\), and this matching base-orders the system.

Now let \(|E|=4\).  A four-edge bipartite graph on \(3+3\) vertices with
no isolates but no perfect matching would be two disjoint two-edge stars.
Let one star have its two degree-one rows both adjacent to column \(q\).
For any \(F\)-edge, restoration must inspect at least one of those two
rows, forcing its column to differ from \(q\).  This would make column
\(q\) empty in \(F\), a contradiction.  Therefore \(E\) has a perfect
matching.

With four edges that perfect matching is unique.  Relabel it as
\[
 M=\{a_0b_0,a_1b_1,a_2b_2\},
 \tag{2.7}
\]
and let the extra edge be \(a_0b_1\).  A restoration check shows that the
only possible \(F\)-edge in row \(a_0\) is \(a_0b_0\).  Moreover, an
\(F\)-edge in column \(b_1\) must lie in row \(a_1\), since otherwise the
degree-one row \(a_1\) could not restore outside \(b_1\).  Similarly, an
\(F\)-edge in column \(b_2\) must be \(a_2b_2\).  Since \(F\) has no empty
rows or columns,
\[
 M\subseteq F.
 \]
Again \(M\subseteq E\cap F\) base-orders the system.

Thus non-base-orderability forces \(|E|\geq5\).  For completeness, define
the endpoint-reversed system
\[
 \mathcal Q^\dagger
 =\{(B-X,A-U):(U,X)\in\mathcal Q\}.
\tag{2.8}
\]
Target expansion in \(\mathcal Q^\dagger\) is source restoration in
\(\mathcal Q\), and source restoration in \(\mathcal Q^\dagger\) is target
expansion in \(\mathcal Q\).  Its level-one relation is \(F^{\mathsf T}\).
A base ordering for either system, inverted as a bijection, base-orders the
other.  Applying the proved \(|E|\geq5\) conclusion to
\(\mathcal Q^\dagger\) therefore gives \(|F|\geq5\).  Including the two
endpoints, every rank-three counterexample has at least
\[
 2+5+5=12
\]
states.  Equation (2.4) attains the bound. \(\square\)

## 3. Exact graph and eternal-family realization

Let \(G\) be the bipartite graph with parts \(A,B\) obtained from
\(K_{3,3}\) by deleting only the edge \(ax\).  The twelve configurations
in (2.5) form an eternal dominating family \(\mathcal F_0\).

Here is one response for every state/attack pair.  An entry
\(r:u\to D'\) means that attack \(r\) is answered by moving the guard
at \(u\), producing \(D'\).

```text
abc  x:b→acx  y:a→bcy  z:a→bcz
abx  c:x→abc  y:a→bxy  z:b→axz
acx  b:x→abc  y:c→axy  z:a→cxz
acy  b:y→abc  x:c→axy  z:a→cyz
axy  b:y→abx  c:x→acy  z:a→xyz
axz  b:z→abx  c:z→acx  y:a→xyz
bcy  a:y→abc  x:c→bxy  z:b→cyz
bcz  a:z→abc  x:b→cxz  y:b→cyz
bxy  a:y→abx  c:x→bcy  z:b→xyz
cxz  a:z→acx  b:x→bcz  y:c→xyz
cyz  a:z→acy  b:y→bcz  x:c→xyz
xyz  a:y→axz  b:z→bxy  c:x→cyz
```

Every displayed move uses an edge of \(G\), attacks an unoccupied vertex,
and retains exactly three guards.  Every successor is listed in
\(\mathcal F_0\).

The endpoint states \(A\) and \(B\) dominate.  A mixed listed state has a
guard in each bipartition class.  The only possible failure caused by the
missing edge \(ax\) would be a state omitting \(a\) whose only \(B\)-guard
is \(x\), or a state omitting \(x\) whose only \(A\)-guard is \(a\);
neither type occurs in (2.5).  Thus every listed state dominates, proving
that \(\mathcal F_0\) is an exact one-guard eternal family.

The two bipartition classes show \(\alpha(G)\geq3\).  Since \(ax\) is the
only cross nonedge, a mixed independent set has size at most two, so
\(\alpha(G)=3\).  The eternal family and
\(\alpha\leq\gamma^\infty\) give

\[
 \gamma^\infty(G)=3.
\tag{3.1}
\]

The pair \(\{a,x\}\) dominates \(G\): \(a\) sees \(y,z\), while \(x\)
sees \(b,c\).  No vertex is universal, so

\[
 \gamma(G)=2.
\tag{3.2}
\]

Finally, three cross edges partition the six vertices into cliques, while
\(\alpha=3\) is a lower bound, giving

\[
 \theta(G)=3.
\tag{3.3}
\]

Therefore ordinary graph realizability, domination of every family state,
and full eternal closure do not repair abstract base-orderability.  The
missing hypothesis in this realization is exactly \(\gamma=\alpha\).

## 4. Static equality does not force pairwise reciprocity

It is tempting to weaken base-orderability to the pairwise assertion

\[
 S-u+v\in\mathcal F
 \quad\Longrightarrow\quad
 T-v+u\in\mathcal F
\tag{4.1}
\]

for disjoint independent triples \(S,T\).  Even under all four equality
parameters, (4.1) is false for an arbitrary eternal family.

Take the graph

\[
 G=\texttt{FCXfO}
\tag{4.2}
\]

with edge set

\[
 \{03,06,14,15,16,24,25,26,46\}.
\tag{4.3}
\]

The following sixteen triples form an eternal family:

\[
\begin{split}
\mathcal F=\{&
012,014,016,024,025,026,045,056,\\
&123,134,136,234,235,236,345,356\}.
\end{split}
\tag{4.4}
\]

For independent endpoint states

\[
 S=012,\qquad T=345,
\tag{4.5}
\]

the edge \(14\) and the state \(024=S-1+4\) prove

\[
 1\in L^{\mathcal F}_S(4).
\tag{4.6}
\]

But \(135=T-4+1\notin\mathcal F\), so

\[
 4\notin L^{\mathcal F}_T(1).
\tag{4.7}
\]

Moreover, \(\{1,4\}\) does not dominate: vertex \(0\) is adjacent to
neither.  Thus nonreciprocity does not manufacture a dominating pair.

For independent checking, one response for every state/attack is:

```text
012 3:0→123 4:2→014 5:1→025 6:2→016
014 2:4→012 3:0→134 5:1→045 6:4→016
016 2:6→012 3:0→136 4:6→014 5:1→056
024 1:4→012 3:0→234 5:2→045 6:4→026
025 1:5→012 3:0→235 4:2→045 6:2→056
026 1:6→012 3:0→236 4:6→024 5:2→056
045 1:5→014 2:5→024 3:0→345 6:4→056
056 1:5→016 2:6→025 3:0→356 4:6→045
123 0:3→012 4:2→134 5:1→235 6:2→136
134 0:3→014 2:4→123 5:1→345 6:4→136
136 0:3→016 2:6→123 4:6→134 5:1→356
234 0:3→024 1:4→123 5:2→345 6:4→236
235 0:3→025 1:5→123 4:2→345 6:2→356
236 0:3→026 1:6→123 4:6→234 5:2→356
345 0:3→045 1:5→134 2:5→234 6:4→356
356 0:3→056 1:5→136 2:6→235 4:6→345
```

The clique partition

\[
 \{0,3\},\qquad\{1,5\},\qquad\{2,4,6\}
\tag{4.8}
\]

and the independent triple \(012\) give
\(\alpha=\theta=3\).  The displayed family gives
\(\gamma^\infty=3\).  No pair dominates; an undominated witness for the
pairs in lexicographic order is

```text
01:2 02:1 03:1 04:5 05:4 06:5 12:0
13:2 14:0 15:0 16:3 23:1 24:0 25:0
26:3 34:5 35:4 36:5 45:0 46:3 56:3
```

Hence

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=\theta(G)=3.
\tag{4.9}
\]

Despite the failed reciprocity, this family remains base-orderable between
\(S\) and \(T\), for example by

\[
 \phi(0)=3,\qquad\phi(1)=5,\qquad\phi(2)=4.
\tag{4.10}
\]

The eight states of its Boolean subcube are

\[
 012,014,025,045,123,134,235,345,
\]

all present in (4.4).

## 5. Exact boundary

The conclusions are now sharply separated:

1. expansion and restoration alone do not force base-orderability;
2. graph edges, domination, and a genuine eternal family still do not
   force it;
3. the specific abstract obstruction realized above fails
   \(\gamma=\alpha\);
4. exact equality \(\gamma=\alpha=\gamma^\infty=\theta=3\) does not force
   individual complementary exchanges to be reciprocal; but
5. no exact equality example without **any** base ordering is known.

The attempted proof that a nonreciprocal exchange \(S-u+v\) makes
\(\{u,v\}\) dominating is explicitly refuted by (4.6)--(4.9).
The graph `FCXfO` shows concretely that an outside vertex may remain
undominated by the nonreciprocal cross pair.  Hall's condition and the
frozen-color projection accommodate such an outside witness; no argument
presently forces it to create a missing reciprocal state.

Accordingly, the following is left **OPEN**, not promoted to a lemma.

> Let \(G\) satisfy \(\gamma(G)=\alpha(G)=3\), let
> \(\mathcal F\subseteq\binom{V(G)}3\) be a one-guard eternal dominating
> family, and let \(S,T\in\mathcal F\) be independent.  Must there exist a
> bijection
> \[
>   \phi:S-T\longrightarrow T-S
> \]
> such that
> \[
>   (S-U)\cup\phi(U)\in\mathcal F
>   \qquad\text{for every }U\subseteq S-T?
> \]

Proposition 1.1 settles \(|S-T|\leq2\); only disjoint triples remain open.
Proving the assertion would require a genuinely external-vertex argument.
Refuting it requires an equality graph, an exact eternal family, and a
specified pair \(S,T\) for which every bijection fails.
