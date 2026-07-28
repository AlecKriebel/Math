# Independent backup hostile review: dynamic connector edge caps

**Review date:** 2026-07-27 (PDT)
**Model:** standard one-guard-moves eternal domination
**Verdict:** **PASS**

## Frozen targets

| target | SHA-256 |
|---|---|
| `math/working/dynamic_connector_edge_caps/NOTE.md` | `185e29a4b8e231aa5e90126f7fd16be32c696cd3f99e46c00f90cb61f27548e7` |
| `math/working/gamma3_port_identification_proof/NOTE.md` | `0b852592548e72face4eb8944909c1dd24c4fbedd31e1a468d118ceb9b0d1487` |

The accepted prerequisites checked for the decisive substitutions were:

| prerequisite | SHA-256 |
|---|---|
| `math/working/k3_long_bicycle_connectors/NOTE.md` | `d3a23bb0171a047a85f2a05c5ccb5faeef0c0c7ceb6d7bb139c6a7a86b8b1f10` |
| `math/lemmas/maximum_independent_states.md` | `08cfa394f5fb1778beac62d752ec2700027ac7710071ed635d9e914f71133e8e` |

No defect was found in any reviewed `PROVED` statement: the base edge-cap
theorem, cap completeness, the forced new cap in the exact separated core,
the cap-and-escape theorem, or the eleven-vertex exact-pattern floor.

The proofs use family-list omission only as a statement that a named
successor is absent from the specified eternal family.  They never infer a
graph nonedge from that omission.  Every adjacency used in a domination or
independence argument is explicitly an edge of \(G\) or of
\(H=\overline G\), with the direction correct.

## 1. Model and parameter audit

The base note starts with an independent family state
\(S=\{a,b,c\}\in\mathcal F\), where \(\mathcal F\) is an eternal family of
triples.  Therefore

\[
 3\leq\alpha(G)\leq\gamma^\infty(G)\leq3,
\]

so \(\alpha(G)=\gamma^\infty(G)=3\).  This justifies every later use of
\(\omega(H)=3\), and the maximum-independent-state lemma puts every
independent triple in the same arbitrary family \(\mathcal F\).

The response-list definition is also sound without separately writing the
move edge.  If \(S-u+x\in\mathcal F\), that state dominates the omitted
anchor \(u\).  Since the other two anchors are nonadjacent to \(u\), the
outside vertex \(x\) must satisfy \(ux\in E(G)\).  Thus positive list
membership really does include the required one-guard move edge.

The accepted dead-state lemmas have exactly the quantifiers used here:

1. two distinct outside vertices omitting \(a\) exclude
   \(\{h,x,y\}\) for \(h\in\{b,c\}\); and
2. three distinct outside vertices omitting \(a\) exclude their triple.

Neither lemma converts dynamic absence into static nonadjacency.

## 2. Base edge-cap theorem

Let \(x,y\notin S\) be distinct, with \(xy\in E(H)\), and let both omit
\(a\).  Because \(\gamma(G)=3\), the pair \(\{x,y\}\) is not dominating.
An undominated vertex is outside the occupied pair and is nonadjacent in
\(G\) to both, hence lies in

\[
 C_{xy}=N_H(x)\cap N_H(y).
\]

This proves nonemptiness with open neighborhoods; it does not accidentally
use \(x\) or \(y\) themselves as a witness.

If two distinct cap vertices \(z,w\) were adjacent in \(H\), then
\(\{x,y,z,w\}\) would be a complement \(K_4\), contradicting
\(\omega(H)=3\).  Hence \(G[C_{xy}]\) is a clique.

If \(b\) or \(c\) belonged to the cap, its triple with \(x,y\) would be a
maximum independent triple and hence a member of \(\mathcal F\), while the
first accepted dead-state lemma excludes the same state.  Thus neither
anchor belongs to the cap.  For
\(z\in C_{xy}-\{a\}\), distinctness from \(x,y\) follows from the use of
open neighborhoods, and exclusion of \(b,c\) makes \(z\) an outside
vertex.  The complement triangle \(\{x,y,z\}\) is a maximum independent
state in \(\mathcal F\).  If \(z\) also omitted \(a\), the second dead-state
lemma would exclude it.  Therefore \(a\in L(z)\).

Finally, if at least one of \(ax,ay\) is in \(E(G)\), then \(a\) cannot be
a common complement neighbor.  The stated outside positive cap follows.
All four conclusions of the more specialized Theorem 2.1 in the second
target are the same argument with both graph edges \(av_0,av_1\) assumed
at the outset.

## 3. Cap completeness via the odd fan theorem

Fix an omitted-color complement edge \(yz\), one of its caps \(t\), and a
distinct positive vertex \(p\).  Suppose for contradiction that
\(pt\in E(H)\).  The accepted odd fan-path theorem is applied with

\[
 p_{\rm fan}=p,\qquad q_{\rm fan}=t,\qquad
 v_0=y,\qquad v_1=z,\qquad m=1.
\]

Its hypotheses are exactly:

\[
 a\in L(p),\quad a\notin L(y)\cup L(z),
\]

and

\[
 pt,\ ty,\ tz,\ yz\in E(H).
\]

The four vertices are distinct: \(t\) is in the open common neighborhood
of \(y,z\), while the theorem explicitly assumes \(p\notin\{t,y,z\}\).
Thus the cited theorem forbids the configuration and yields
\(pt\in E(G)\).

Because the endpoints \(y,z\) omit \(a\), every member of
\(P_a-\{t\}\) is automatically different from them.  Consequently the
equivalent statement that a cap is \(G\)-complete to
\(P_a-\{t\}\) is exact, not an overextension of the distinctness
hypothesis.

## 4. Exact separated-core cap

The six outside vertices

\[
 x,r,s,q,v_0,v_1
\]

are declared distinct, and the phrase “induce in \(H\) exactly” makes the
listed six edges the complete edge set among them.  Hence among
\(x,r,s,q\), no vertex sees both \(v_0,v_1\) in \(H\):

- \(x\) and \(s\) see neither;
- \(r\) sees only \(v_0\); and
- \(q\) sees only \(v_1\).

The specialized cap theorem applied to \(v_0v_1\) therefore supplies a cap
\(z\) outside \(S\), and the exact incidence list proves that it is also
different from all six old outside vertices.  Since
\(x,r,s,q\in P_a\), cap completeness gives

\[
 zx,zr,zs,zq\in E(G).
\]

In particular \(z\in N_G(x)-S\).  No unlisted response or adjacency is
assumed.

## 5. Cap-and-escape

Since \(\gamma(G)=3\), the pair \(\{x,z\}\) is not dominating.  An
undominated vertex \(w\) is therefore in
\(N_H(x)\cap N_H(z)\).  Its required distinctness is fully discharged:

- \(w\notin S\), because a full list for \(x\) forces
  \(x\) to be adjacent in \(G\) to every anchor;
- \(w\notin\{r,s,q\}\), because \(z\) is adjacent in \(G\) to those three;
- \(w\notin\{v_0,v_1\}\), because exactness of the old induced
  complement makes \(xv_0,xv_1\in E(G)\); and
- open neighborhoods exclude \(x,z\).

If \(a\in L(w)\), cap completeness for the cap \(z\) and positive vertex
\(w\) would give \(wz\in E(G)\), contrary to \(wz\in E(H)\).  Hence
\(w\in W_a\).  This is a valid dynamic-family conclusion, not a graph
nonedge inference.

If \(w\) saw both connector endpoints in \(H\), the six complement edges

\[
 zv_0,\ zv_1,\ v_0v_1,\ zw,\ wv_0,\ wv_1
\]

would form a \(K_4\) on four already proved distinct vertices.  This
contradicts \(\omega(H)=3\).  Therefore \(w\) sees at most one endpoint.

## 6. Exact-pattern order floor and boundary

The exact core contains nine pairwise distinct vertices: three anchors and
six outside vertices.  The cap proof forces a tenth vertex \(z\), and the
escape proof forces an eleventh vertex \(w\) outside the previous ten.
Thus every realization of this exact conditional pattern has order at
least eleven.

This is not a lower bound for arbitrary equality graphs or arbitrary
counterexamples, and the target correctly labels it only as an
**exact-pattern** order floor.  The notes also correctly stop short of
terminal-port identification, arbitrary connector contraction, or a proof
of the \(k=3\) conjecture.

## 7. Hostile checks specifically passed

- **Unoccupied attacks:** the reviewed new proofs use no attack directly;
  the only dynamic invocation is the already accepted odd fan theorem and
  the two accepted dead-state lemmas, whose attacks are unoccupied.
- **One guard only:** positive list membership and the prerequisites use
  one named guard replacement; no all-guards move is imported.
- **Complement direction:** common \(H\)-neighbors mean vertices missed by
  a guard pair in \(G\); complement triangles and \(K_4\)'s mean
  independent triples and four-sets in \(G\); all uses have the correct
  direction.
- **Dynamic omission:** \(a\notin L(v)\) is used only to exclude a family
  successor or invoke a family dead-state theorem.
- **Distinctness:** open neighborhoods, the exact old induced pattern, and
  the explicit hypotheses together establish every distinctness condition
  required by the dead-state and odd-fan lemmas.
- **Claim scope:** no reviewed theorem asserts clique colorability,
  counterexample exclusion, or universal resolution.

There are no qualifications to the `PROVED` statements within their stated
hypotheses.
