# Dynamic connector edge caps at \(k=3\)

## Status and scope

Date: 2026-07-27 (PDT)

The theorem below is `PROVED`, pending independent hostile review.  It uses
the standard one-guard-moves model and an arbitrary specified eternal
family.  It is a local consequence of the missing domination equality
\(\gamma=3\); it does not color the graph or resolve the gamma--theta
conjecture.

The result supplies exact new structure on the separated-port branch left
open by C-079 and C-081.  It never interprets a missing family response as a
graph nonedge.

## 1. Setup and two accepted dead states

Let \(\mathcal F\) be an eternal family of triples in \(G\), let

\[
 S=\{a,b,c\}\in\mathcal F
\]

be independent, and put \(H=\overline G\).  For \(x\notin S\), write

\[
 L(x)=\{u\in S:S-u+x\in\mathcal F\}.
\tag{1.1}
\]

Membership in (1.1) already forces the move edge \(ux\in E(G)\), because
the successor must dominate the omitted anchor \(u\).

We use the two dead-state lemmas proved in C-079:

1. if \(a\notin L(x)\cup L(y)\), then
   \[
     \{h,x,y\}\notin\mathcal F
     \qquad(h\in\{b,c\});
   \tag{1.2}
   \]
2. if three distinct outside vertices \(x,y,z\) all omit \(a\), then
   \[
     \{x,y,z\}\notin\mathcal F.
   \tag{1.3}
   \]

Both statements concern family membership, not graph adjacency.

## 2. The edge-cap theorem

### Theorem 2.1 (dynamic connector edge caps) — PROVED

Assume additionally that

\[
 \gamma(G)=3.
\tag{2.1}
\]

Let \(x,y\notin S\) be distinct, suppose

\[
 xy\in E(H),
 \qquad
 a\notin L(x)\cup L(y),
\tag{2.2}
\]

and put

\[
 C_{xy}=N_H(x)\cap N_H(y).
\tag{2.3}
\]

Then:

1. \(C_{xy}\ne\varnothing\);
2. \(G[C_{xy}]\) is a clique;
3. \(C_{xy}\cap\{b,c\}=\varnothing\);
4. every \(z\in C_{xy}-\{a\}\) lies outside \(S\), satisfies
   \[
     a\in L(z),
   \tag{2.4}
   \]
   and gives the forced maximum-independent family state
   \[
     \{x,y,z\}\in\mathcal F.
   \tag{2.5}
   \]

Consequently, if at least one of \(x,y\) is adjacent to \(a\) in \(G\),
then \(a\notin C_{xy}\), and \(C_{xy}\) is a nonempty outside clique all of
whose vertices positively support response color \(a\).

#### Proof

The pair \(\{x,y\}\) cannot dominate \(G\), since \(\gamma(G)=3\).
Therefore some vertex is nonadjacent in \(G\) to both \(x\) and \(y\),
which is exactly a member of \(C_{xy}\).  This proves item 1.

The independent triple \(S\) and the eternal triple-family give
\(\alpha(G)=3\): the lower bound comes from \(S\), while
\(\alpha(G)\leq\gamma^\infty(G)\leq3\).  If two distinct vertices
\(z,w\in C_{xy}\) were adjacent in \(H\), then

\[
 \{x,y,z,w\}
\]

would be a clique of \(H\), equivalently an independent four-set of \(G\),
contradicting \(\alpha(G)=3\).  Thus every two vertices of \(C_{xy}\) are
adjacent in \(G\), proving item 2.

Suppose \(h\in C_{xy}\cap\{b,c\}\).  The three vertices \(h,x,y\) form a
clique of \(H\), hence a maximum independent set of \(G\).  Every maximum
independent triple belongs to every eternal triple-family, so
\(\{h,x,y\}\in\mathcal F\).  This contradicts the dead-state conclusion
(1.2).  Therefore item 3 holds.

Now take \(z\in C_{xy}-\{a\}\).  Item 3 and the definition of \(C_{xy}\)
show that \(z\notin S\).  The vertices \(x,y,z\) form a clique of \(H\), so
\(\{x,y,z\}\) is a maximum independent set of \(G\) and belongs to
\(\mathcal F\), proving (2.5).  If \(a\notin L(z)\), all three outside
vertices \(x,y,z\) would omit \(a\), and the dead-state conclusion (1.3)
would say that the same triple is absent.  Hence \(a\in L(z)\), proving
item 4.

Finally, \(a\in C_{xy}\) is equivalent to both \(ax,ay\in E(H)\).  If at
least one of these pairs is an edge of \(G\), then \(a\notin C_{xy}\), so
all preceding cap vertices are outside and satisfy (2.4). \(\square\)

### Corollary 2.2 (all-dynamic connector)

Let

\[
 v_0v_1\ldots v_m
\]

be a complement path whose vertices all omit \(a\) from their family lists
and are all adjacent to \(a\) in \(G\).  Under \(\gamma(G)=3\), every path
edge \(v_iv_{i+1}\) has a nonempty \(G\)-clique of outside common
complement neighbors, and every member of that clique has \(a\) in its
family-response list.

This is an edge-by-edge cap system.  The theorem does not say that caps for
different edges are distinct, that they lie in one frozen component, or that
they identify the terminal ports of a Boolean implication walk.

## 3. Exact relation to the separated-port control

In the nine-vertex C-081 control `HFzvvn{`, every nonfull outside vertex is
adjacent in \(G\) to every anchor, so every omitted response is dynamic.
For example, the connector edge \(45\in E(H)\) has

\[
 N_H(4)\cap N_H(5)=\varnothing.
\]

Thus \(\{4,5\}\) is a dominating pair, and the first conclusion of
Theorem 2.1 fails precisely because that control has \(\gamma(G)=2\).

The bounded extension scan in
`math/working/separated_port_gamma3_extensions/` finds the same boundary:
every tested graph retaining the exact separated-port response pattern has
a dominating singleton or pair.  That scan is supporting evidence only;
the universal theorem above does not depend on it.

## 4. Stopping boundary

The theorem converts every all-dynamic omitted-color connector into a
chain of positively colored triangle caps.  It does not yet prove:

- that two terminal Boolean occurrences use the same physical port;
- that the cap chain contains an odd fan forbidden by C-079;
- that caps belonging to successive connector edges are distinct or
  ridge-connected; or
- that a separated-port lollipop is impossible under \(\gamma=3\).

Those are the next propagation questions.  No novelty or priority claim is
made.
