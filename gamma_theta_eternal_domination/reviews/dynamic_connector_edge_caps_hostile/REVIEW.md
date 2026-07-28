# Hostile review: dynamic connector caps and the cap-and-escape ladder

Date: 2026-07-27 (PDT)

## Verdict

**PASS** for both frozen targets, with the exact scopes stated in the
targets.

1. `math/working/dynamic_connector_edge_caps/NOTE.md`
   - reviewed SHA-256:
     `185e29a4b8e231aa5e90126f7fd16be32c696cd3f99e46c00f90cb61f27548e7`;
   - verdict: **PASS**;
   - accepted scope: Theorem 2.1 and Corollary 2.2 are valid for an
     arbitrary specified eternal family of triples under
     \(\gamma(G)=3\).  They give an edge-by-edge cap system only and do not
     identify ports or prove the \(k=3\) conjecture.

2. `math/working/gamma3_port_identification_proof/NOTE.md`
   - reviewed SHA-256:
     `0b852592548e72face4eb8944909c1dd24c4fbedd31e1a468d118ceb9b0d1487`;
   - verdict: **PASS**;
   - accepted scope: Theorems 2.1 and 2.2, Corollary 3.1, Theorem 4.1,
     and Corollary 4.2 are valid.  The stronger target proves the cap
     completeness and cap-and-escape conclusions for the exact
     separated-port core.  It still does not exclude every separated-port
     lollipop or resolve the \(k=3\) slice.

The second target is the stronger accepted result.  Its Theorem 2.1 is
the all-dynamic specialization of the first target's edge-cap theorem;
Theorem 2.2 and Sections 3--4 add genuinely stronger propagation.

This was a bounded symbolic audit.  I did not independently replay the
\(524{,}288\)-extension scan, and I agree with the target's conservative
classification of that scan as `OBSERVED`.

## Definitions reconstructed

Let \(\mathcal F\) be an eternal family of triples, let
\(S=\{a,b,c\}\in\mathcal F\) be independent, and define

\[
 L(x)=\{u\in S:S-u+x\in\mathcal F\}.
\]

The edge condition in the longer definition of \(L\) is redundant here,
but not assumed away: if \(S-u+x\in\mathcal F\), that state must dominate
the omitted anchor \(u\).  The other two anchors are nonadjacent to \(u\),
so necessarily \(ux\in E(G)\).

I also reconstructed the maximum-independent-state fact rather than
treating it as a black box.  Given an independent triple \(I\), repeatedly
attack an unoccupied vertex of \(I\).  A guard already on \(I\) cannot move
to another vertex of \(I\), so every response increases the number of
occupied vertices of \(I\).  After at most three attacks the state is
exactly \(I\).  Hence every independent triple belongs to every eternal
triple-family.

The two C-079 dead states follow directly from one-guard closure:

- from \(\{h,x,y\}\), with \(h\in\{b,c\}\) and both \(x,y\) omitting
  \(a\), attack the other anchor; every possible successor is one of the
  two absent direct \(a\)-swaps;
- from three outside \(a\)-omitting vertices, attack \(b\); every possible
  successor is a dead state of the preceding type.

These arguments use family nonmembership only.  They never infer a graph
nonedge from a missing response.

## Audit of the base edge-cap theorem

### Nonempty cap

Since \(\gamma(G)=3\), no two-vertex set dominates.  Therefore
\(\{x,y\}\) misses a vertex \(z\), and such a vertex is nonadjacent in
\(G\) to both \(x\) and \(y\).  This is exactly
\(z\in N_H(x)\cap N_H(y)\).  A missed vertex cannot be \(x\) or \(y\),
so there is no closed/open-neighborhood ambiguity.

### The cap is a \(G\)-clique

The independent state \(S\) gives \(\alpha(G)\geq3\), while an eternal
triple-family gives
\(\alpha(G)\leq\gamma^\infty(G)\leq3\).  Thus
\(\alpha(G)=3\), equivalently \(\omega(H)=3\).
If two cap vertices were adjacent in \(H\), they together with the
connector endpoints would induce an \(H\)-\(K_4\).  Therefore distinct cap
vertices are adjacent in \(G\).

### Anchor exclusions and the recovered list color

If \(b\) or \(c\) were a cap vertex, its triple with the two connector
endpoints would be a maximum independent set, hence a member of
\(\mathcal F\), contradicting the first dead-state lemma.  Thus \(b,c\)
are excluded.

Every cap vertex other than a possible \(a\) is consequently outside
\(S\).  Its triple with the connector endpoints is maximum independent
and is forced into \(\mathcal F\).  If that cap vertex also omitted \(a\),
the second dead-state lemma would exclude the same triple.  Hence the cap
vertex has \(a\) in its actual family-response list.

If either endpoint is \(G\)-adjacent to \(a\), then \(a\) is not a common
complement-neighbor.  This proves the final clause and, edge by edge,
Corollary 2.2.

All implications above remain valid for an arbitrary specified eternal
family; no greatest-kernel assumption is used.

## Audit of the stronger cap theorem

The stronger Theorem 2.1 assumes both connector endpoints are
\(G\)-adjacent to \(a\).  This excludes \(a\) itself from the cap.
The preceding argument already excludes \(b,c\), so the entire cap lies
outside \(S\), lies in \(P_a\), is nonempty, and is a \(G\)-clique.
All four conclusions follow.

For Theorem 2.2, suppose a cap vertex \(t\) and another positive vertex
\(p\) had \(pt\in E(H)\).  The C-079 theorem applies with

\[
 (p,q,v_0,v_1)=(p,t,y,z),\qquad m=1.
\]

The four vertices are distinct: this is assumed for \(p\), a common open
neighbor cannot equal either endpoint, and the endpoints are distinct.
The required complement edges are precisely
\(pt,ty,tz,yz\); \(p\) has color \(a\), while \(y,z\) omit it.  This is
the forbidden length-one odd fan.  Therefore \(pt\in E(G)\).

The displayed qualification “distinct from \(t,y,z\)” does not weaken the
subsequent equivalent formulation: a member of \(P_a\) cannot equal
\(y\) or \(z\), since those vertices lie in \(W_a\).

## Audit of the exact separated-port consequences

### Corollary 3.1

Apply Theorem 2.1 to \(v_0v_1\).  The hypotheses
\(v_0,v_1\in W_a\), \(v_0v_1\in E(H)\), and
\(av_0,av_1\in E(G)\) are stated explicitly.  It yields a positive cap
\(z\) adjacent in \(H\) to both endpoints.

The cap cannot equal \(v_0\) or \(v_1\), since it belongs to the
intersection of two open neighborhoods in a simple graph.  It is outside
\(S\) by Theorem 2.1.  In the exact induced pattern, none of
\(x,r,s,q\) is adjacent in \(H\) to both \(v_0,v_1\), so \(z\) is new.

Each of \(x,r,s,q\) lies in \(P_a\).  Theorem 2.2 therefore makes the cap
\(G\)-adjacent to all four, proving (3.7), including
\(z\in N_G(x)-S\).  No unlisted complement incidence was assumed.

### Theorem 4.1

The pair \(\{x,z\}\) cannot dominate because \(\gamma(G)=3\), so it has a
common complement-neighbor \(w\).  Thus \(wx,wz\in E(H)\).

The distinctness exclusions are all sound:

- \(L(x)=S\) forces \(x\) to be \(G\)-adjacent to every anchor, so a
  complement-neighbor of \(x\) is not in \(S\);
- \(r,s,q\) are \(G\)-adjacent to \(z\) by Corollary 3.1, so none can be
  the complement-neighbor \(w\) of \(z\);
- the exact induced core makes \(v_0,v_1\) \(G\)-adjacent to \(x\), so
  neither can be \(w\);
- a member of \(N_H(x)\cap N_H(z)\) cannot equal \(x\) or \(z\).

If \(w\in P_a\), Theorem 2.2 applied to the cap \(z\) of
\(v_0v_1\) makes \(wz\in E(G)\), contradicting \(wz\in E(H)\).
Therefore \(w\in W_a\).

Finally, if \(w\) saw both \(v_0,v_1\) in \(H\), the six edges among
\(\{z,w,v_0,v_1\}\) would be

\[
 zv_0,zv_1,v_0v_1,zw,wv_0,wv_1.
\]

They form an \(H\)-\(K_4\), contradicting
\(\omega(H)=\alpha(G)=3\).  Hence \(w\) sees at most one endpoint in
\(H\).

### Corollary 4.2

Section 3 starts with nine explicitly distinct vertices.  Corollary 3.1
adds \(z\) outside all nine, and Theorem 4.1 adds \(w\) outside those ten.
Thus every realization of this exact pattern has order at least eleven.
The claim is an exact-pattern floor only, not a global lower bound for
counterexamples.

## Adversarial failure checks

- Attacks used in the reconstructed dead-state arguments are always at
  unoccupied anchors.
- Every transition changes exactly one guard and requires the move edge;
  absent move edges only remove responses.
- The arguments distinguish \(G\) from \(H=\overline G\) throughout.
- No response-list omission is converted into graph nonadjacency.
- The common-neighbor step uses \(\gamma=3\), not merely
  \(\alpha=3\) or well-coveredness.
- The cap-clique and escape exclusions use
  \(\omega(H)=\alpha(G)=3\), with the direction of complementation
  correct.
- The \(m=1\) C-079 invocation has all required physical vertices and
  all four literal complement edges; it does not contract a Boolean
  connector.
- The order floor counts only the exact named pattern and its two forced
  new vertices.

No circular appeal to the gamma--theta conjecture, no all-guards-move
transition, and no hidden coloring assertion appears in the audited
proofs.
