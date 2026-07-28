# Hostile review: side-purity and the finite cap-cycle control

Date: 2026-07-27 (PDT)

## Verdict

**PASS.**

The side-purity theorem, its open-neighborhood contrapositive, the
singleton-buffer corollary, and the cap-continuation corollary are valid on
the reviewed bytes.  In particular:

- the proof correctly handles the case \(q\in W_a\) and proves that \(q\)
  cannot be a vertex of the selected path;
- \(N_H(q)\cap P_a=\varnothing\) remains the correct contrapositive even
  when \(q\in P_a\), because \(N_H(q)\) is an open neighborhood in a simple
  graph; and
- the singleton conclusion is restricted to outside complement neighbors
  that lie in \(W_v\).  Its connector specialization concerns an internal
  connector in the nonanchor component of the \(v\)-projection, not an
  arbitrary cross-projection edge or arbitrary neighbor of the port.

The graph6 control `GCXfVG` also passes a clean-room reconstruction.  It is
connected, has

\[
(\gamma,\alpha,\gamma^\infty,\theta)=(3,3,3,3),
\]

has exactly the displayed 26-state greatest eternal triple-family, has the
displayed response lists and two compatible list colorings, and has a
single \(a\)-positive cap repeated around the entire \(a\)-omitting
complement \(C_4\).  There is no physical C-079 embedding for any anchor,
no complement \(K_4\), and no dominating pair.

No correction is required.  The control is colorable and does not refute
the gamma--theta conjecture.  Its stated negative conclusion is correctly
limited to recurrence arguments using cap identity, finiteness, and first
repetition without the missing cross-port or terminal-unit data.

## Reviewed bytes

| artifact | SHA-256 |
|---|---|
| `math/working/k3_side_purity_cap_cycle/NOTE.md` | `64312289f6d3d87a4c302692c92901caeb9788b16354493e07be01920549f11b` |
| `math/working/k3_side_purity_cap_cycle/verify.py` | `decdf31f361222f5959b1c590aab48c7acd9b37736d8b5b897e3f3f0ab2932d4` |
| `math/working/k3_side_purity_cap_cycle/result.json` | `f9dd30333986b0c984910fe3e13464c28bd64a98d85932c8e2df14f805fb1998` |
| `math/working/k3_side_purity_cap_cycle/RESEARCH_LOG.md` | `a2874b9c1736efc22aed3e56b7017e4f4a08e5e537874d593a39b71fd4d81a3a` |

The prerequisite bytes independently reread for this review were:

| prerequisite | SHA-256 |
|---|---|
| C-079 source, `math/working/k3_long_bicycle_connectors/NOTE.md` | `d3a23bb0171a047a85f2a05c5ccb5faeef0c0c7ceb6d7bb139c6a7a86b8b1f10` |
| frozen projection, `math/working/k3_cross_state_attack.md` | `3e87ca4e7c04987c2f56576c4e8b0f28113e254fdb1a024b4da7a3e0d6bf4c68` |
| accepted parameter-two reduction, `math/reductions.md` | `d2c899b68f0d2142c250dee26047af43d01e10d83a0ed112c289a14c3f3d5e13` |

## Prerequisite audit

Let \(\mathcal F\) be an arbitrary eternal family of triples, let
\(S=\{a,b,c\}\in\mathcal F\) be independent, and define the family-response
lists relative to \(S\).

Every outside list is nonempty: attack that outside vertex from \(S\), and
closure supplies a retained one-guard response.  Moreover, if
\(S-u+t\in\mathcal F\), the retained state must dominate the omitted
anchor \(u\).  The other two anchors miss \(u\), so \(ut\in E(G)\).
Thus the abbreviated list definition in the target has the same content as
the edge-explicit definition used in C-079.

For a fixed \(a\), the frozen family-response projection on

\[
(S-\{a\})\cup W_a
\]

has an eternal two-family and has
\(\alpha=\gamma^\infty=2\).  The accepted parameter-two theorem therefore
gives clique-partition number two for that projected graph.  Equivalently,
its complement is bipartite.  Hence \(H[W_a]\), and every one of its
components, is bipartite.  This conclusion needs only the eternal
triple-family containing the independent \(S\); it does not secretly need
\(\gamma(G)=3\).

C-079 excludes distinct outside vertices

\[
p,q,v_0,\ldots,v_m
\]

when \(m\geq1\) is odd, \(a\in L(p)\), all path vertices omit \(a\), and
the literal complement edges

\[
pq,\ qv_0,\ qv_m,\ v_0v_1,\ldots,v_{m-1}v_m
\]

are present.  It places no condition on \(L(q)\), does not require an
induced path, and tolerates extra complement edges.  These are exactly the
quantifiers used by the target proof.

## Side-purity: complete distinctness and quantifier check

Fix a component \(K\) of \(H[W_a]\), with bipartition \(U_K\mid V_K\).
Let \(q\notin S\), and suppose that a distinct positive vertex
\(p\in P_a-\{q\}\) satisfies \(pq\in E(H)\).

If \(q\) had neighbors

\[
x\in U_K,\qquad y\in V_K,
\]

then \(x\ne y\), and neither equals \(q\), because both belong to the open
neighborhood \(N_H(q)\).  A shortest \(x\)-\(y\) path in \(K\) is simple,
has positive odd length, and has every vertex in \(W_a\).

The path avoids \(p\) because \(p\in P_a\) and
\(P_a\cap W_a=\varnothing\).  The remaining delicate point is \(q\):

1. If \(q\notin W_a\), then \(q\notin K\), so it is not on the path.
2. If \(q\in W_a\), the literal edge \(qx\) places \(q\) in the same
   component \(K\).  Both \(x\) and \(y\) are then neighbors of \(q\) in
   the bipartite graph \(K\), so both lie on the side opposite \(q\).
   This contradicts their placement on opposite sides.

Thus the mixed-side hypothesis itself forces \(q\notin K\).  Together with
the explicit condition \(p\ne q\), all vertices

\[
p,q,v_0,\ldots,v_m
\]

are distinct.  The positive-list condition, two hub endpoint edges, tail
edge, and odd \(W_a\)-path are precisely a forbidden C-079 fan.  Therefore
all of \(N_H(q)\cap K\) lies on one side.

For the contrapositive, a mixed neighborhood in one component rules out
every vertex of \(P_a-\{q\}\) from \(N_H(q)\).  Since the graph is simple,

\[
q\notin N_H(q),
\]

and hence

\[
N_H(q)\cap(P_a-\{q\})=N_H(q)\cap P_a.
\]

This justifies the stronger-looking formula
\(N_H(q)\cap P_a=\varnothing\), including when \(q\in P_a\).

## Singleton-buffer and cap-continuation scope

Assume

\[
L(q)=S-\{v\}=\{a,d\},\qquad v\ne a,
\]

and \(q\) sees opposite sides of one \(H[W_a]\)-component.  Side-purity's
contrapositive gives

\[
N_H(q)\cap P_a=\varnothing.
\]

Now quantify only over an outside vertex \(r\) satisfying

\[
qr\in E(H),\qquad r\in W_v.
\]

The first condition makes \(r\ne q\).  If \(a\in L(r)\), then
\(r\in N_H(q)\cap P_a\), a contradiction.  The second condition says
\(v\notin L(r)\).  Nonemptiness of the outside response list then leaves
exactly

\[
L(r)=\{d\}.
\]

No conclusion is claimed for a neighbor \(r\notin W_v\), for an anchor,
or for a logical continuation lacking a literal complement edge.

The connector specialization preserves these hypotheses.  A nonanchor
component of the \(v\)-projection is disjoint from the anchor component
containing \(S-\{v\}\).  Consequently, every vertex on an internal
connector in that component is outside \(S\) and belongs to \(W_v\).
The first positive-length connector edge from \(q\) therefore has exactly
the two properties displayed above, so its endpoint is the singleton
\(\{d\}\).  This singleton imposes the usual parity unit on that same
component.  An arbitrary cross-projection clause edge is outside this
specialization and is not declared singleton.

For cap continuation, \(xy\in E(H[W_a])\) puts \(x\) and \(y\) on opposite
sides of one component.  A positive outside cap \(z\) with
\(zx,zy\in E(H)\) consequently satisfies

\[
N_H(z)\cap P_a=\varnothing.
\]

If \(L(z)=S-\{v\}\), the preceding singleton argument applies exactly to
each outside \(H\)-neighbor of \(z\) lying in \(W_v\), and only to those
neighbors.  The corollary's stated scope is therefore correct.

## Independent reconstruction of `GCXfVG`

The clean-room checker decodes the short graph6 bit stream without using
the working verifier and obtains the documented 13 edges.  Its complement
has 15 edges and consists of the anchor triangle, \(bz,cz\), all four
\(zx_i\), \(ax_0,ax_1\), and the rim

\[
x_0x_1x_2x_3x_0.
\]

The original graph is connected.

On

\[
R=\{b,c,x_0,x_1,x_2,x_3\},
\]

the exhaustive calculation finds exactly 13 dominating pairs: every
two-subset except \(\{x_0,x_2\}\) and \(\{x_1,x_3\}\).  Every dominating
triple contains exactly one of \(a,z\) and one of those 13 pairs.  Hence
all dominating triples are exactly the displayed 26 states

\[
\{\{t\}\cup D:t\in\{a,z\},\ D\in\mathcal D\}.
\]

The greatest-fixed-point computation deletes no triple.  All 130
unoccupied state/attack obligations have one or two retained responses.
There are no dominating states with one or two guards.  This independently
gives \(\gamma^\infty=3\), while direct exhaustive domination gives
\(\gamma=3\).

The anchors give an independent triple, and exhaustive search finds no
independent four-set, so \(\alpha=3\).  The displayed partition

\[
\{a,z\}\mid\{b,x_0,x_2\}\mid\{c,x_1,x_3\}
\]

is a three-clique partition of \(G\), while
\(\theta\geq\alpha=3\).  Thus \(\theta=3\).

At \(S=\{a,b,c\}\), direct swaps into the reconstructed family give

\[
L(z)=\{a\},\qquad L(x_i)=\{b,c\}\quad(0\leq i\leq3).
\]

There are exactly two compatible list colorings: \(z\) receives \(a\), and
the rim alternates \(b,c\) in either orientation.

For the \(a\)-projection,

\[
P_a=\{z\},\qquad W_a=\{x_0,x_1,x_2,x_3\},
\]

and \(H[W_a]\) is the displayed \(C_4\).  The common complement
neighborhoods of its edges are

\[
\begin{array}{c|c}
x_0x_1&\{a,z\}\\
x_0x_3&\{z\}\\
x_1x_2&\{z\}\\
x_2x_3&\{z\}.
\end{array}
\]

Thus the positive vertex \(z\) caps all four edges.  The edge \(x_2x_3\)
is fully dynamic relative to \(a\), and \(z\) is its unique cap.

The checker enumerates every vertex-distinct odd \(W_u\)-path, every
positive \(p\), and every distinct outside hub \(q\) for all three anchors.
The C-079 embedding counts are

\[
(0,0,0).
\]

Structurally, for \(a\), each possible outside hub adjacent to \(z\) is a
rim vertex and its two rim neighbors lie on the same bipartition side.  For
\(b\) and \(c\), the omitting set is the singleton \(\{z\}\), which has no
positive-length path.  Exhaustive search also finds zero complement
\(K_4\)'s and zero dominating pairs.

## Reproduction

The working verifier passed its frozen-result check, and its output was
byte-identical to `result.json`:

```text
python3 -I -B -W error \
  gamma_theta_eternal_domination/math/working/\
k3_side_purity_cap_cycle/verify.py \
  --check gamma_theta_eternal_domination/math/working/\
k3_side_purity_cap_cycle/result.json
```

The independent checker imports no working verifier or campaign search
core.  It uses integer bit masks and exhaustive standard-library search:

```text
python3 -I -B -W error \
  gamma_theta_eternal_domination/reviews/\
k3_side_purity_cap_cycle_hostile/independent_checker.py \
  --check gamma_theta_eternal_domination/reviews/\
k3_side_purity_cap_cycle_hostile/independent_result.json
```

The independent artifacts have SHA-256 hashes:

| artifact | SHA-256 |
|---|---|
| `independent_checker.py` | `af67c3e27e60767701139a039974793087c41748b806e28130aecd827a270946` |
| `independent_result.json` | `9f3285541225a7bd495811853cfbd5a65dce6171fd46cbac6b7fa1f6c5ff90cb` |

Both checks completed successfully.
