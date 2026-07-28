# Hostile review: all-\(k\) inactive-link extension bridge

Review date: 2026-07-28 PDT

Candidate:
`math/working/all_k_extension_bridge/NOTE.md`

Candidate SHA-256:
`1edb9fb1aa0f3865bbb8906ca86ea11cbc897d28e9e703083ee384f2931b4ad0`

Frozen manifest SHA-256:
`c99b154ed344c7efd076e5115e6d64eed9e9d8eeff6d28810889b405cb39874f`

## Verdict

**UNCONDITIONAL PASS on the manifest-frozen candidate bundle.**

Theorem 2.1 is correct.  Target inactivity places \(x\) in the exact
family-response omission set, every complement neighbor of \(r\) lies in
the frozen projection, the accepted projection theorem supplies the three
parameter equalities, and minimum-counterexample minimality supplies
\(\theta=k-1\).  Restricting the resulting complement coloring and using
the fixed \((k-1)\)-clique \(T-\{r\}\) gives both equalities in (2.1).

When \(rx\in E(G)\), the suspension contains the additional vertex \(x\)
outside the ordinary complement link, so the result is strictly stronger
than the previously accepted face-link statement.  The note correctly
stops at local colorings and does not assert compatibility or global
gluing.

The clean-room control audit also passes: the greatest triple-family has
127 states and a full target; the active and inactive sets are exact; all
12 labeled deletion three-colorings were exhausted; the split is exactly
6/6; and the deletion has the claimed \(\gamma=2\) boundary.

## 1. Reference state and target inactivity

The graph \(G\) is a minimum-order counterexample with

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=k<\theta(G).
\]

Every independent \(k\)-set is maximum and belongs to every eternal
\(k\)-family, so the chosen independent state \(T\) is legitimately a
state of the arbitrary fixed family \(\mathcal F\).  The target \(x\)
avoids \(T\), and \(r\in T\).

The family-relative list

\[
 L_T^\mathcal F(y)
 =
 \{u\in T:uy\in E(G),\ T-u+y\in\mathcal F\}
\]

contains both the move-edge and retained-successor requirements.  Hence

\[
 r\notin L_T^\mathcal F(x)
\]

is exactly the statement \(x\in W_{T,r}\).  This remains true in both
possible kinds of inactivity:

- physical inactivity, \(rx\in E(H)\); and
- dynamic inactivity, \(rx\in E(G)\) but
  \(T-r+x\notin\mathcal F\).

C-108 is used only to make the term “\(r\) is inactive at \(x\)”
independent of which maximum independent state containing \(r\) is
chosen.  The local projection proof itself is valid for the displayed
state \(T\).

## 2. Exact containment in the frozen projection

The projected graph is

\[
 Q_{T,r}
 =
 G[(T-\{r\})\cup W_{T,r}].
\]

First, inactivity gives \(x\in W_{T,r}\).

Now take any \(z\in N_H(r)\).

- If \(z\in T-\{r\}\), it lies in the first part of the projected vertex
  set.
- Otherwise \(z\notin T\).  The literal complement edge
  \(rz\in E(H)\) means \(rz\notin E(G)\).  Thus the guard at \(r\) cannot
  answer an attack at \(z\), regardless of family membership, and
  \(r\notin L_T^\mathcal F(z)\).  Hence \(z\in W_{T,r}\).

These cases include \(z=x\) when \(rx\in E(H)\), though \(x\) was already
included by inactivity.  Therefore

\[
 \{x\}\cup N_H(r)\subseteq V(Q_{T,r}).
\]

No response omission is converted into a graph nonedge.  The only
adjacency inference in the second case starts from the already literal
edge \(rz\in E(H)\).

The projection is a proper induced subgraph of \(G\): \(r\) lies in
neither \(T-\{r\}\) nor \(W_{T,r}\), whose definition only admits vertices
outside \(T\).

## 3. Frozen-projection hypotheses and minimality

The accepted all-\(k\) frozen-color theorem applies with:

- the arbitrary eternal family \(\mathcal F\);
- independent family state \(T\);
- frozen guard \(r\);
- the family-response omission set \(W_{T,r}\); and
- \(\gamma(G)=k\).

It gives

\[
 \gamma(Q_{T,r})
 =
 \alpha(Q_{T,r})
 =
 \gamma^\infty(Q_{T,r})
 =
 k-1.
\]

The parameter-\(k-1\) graph \(Q_{T,r}\) is smaller than \(G\).  If
\(\theta(Q_{T,r})>k-1\), then

\[
 \gamma(Q_{T,r})
 =
 \gamma^\infty(Q_{T,r})
 =
 k-1
 <
 \theta(Q_{T,r}),
\]

so \(Q_{T,r}\) would itself be a smaller counterexample.  Minimum-order
minimality forbids this.  Conversely,
\(\alpha(Q_{T,r})=k-1\le\theta(Q_{T,r})\).  Thus

\[
 \theta(Q_{T,r})=k-1.
\]

This argument does not assume a monotonic formula relating
\(\theta(G)\) and \(\theta(Q_{T,r})\), nor does it assume the conjecture
at parameter \(k-1\).  It uses only the definition of a minimum-order
counterexample.

## 4. Chromatic upper bound and clique lower bound

Because \(Q_{T,r}\) is induced on \(V(Q_{T,r})\), the complement of that
induced graph is exactly

\[
 H[V(Q_{T,r})].
\]

A partition of \(Q_{T,r}\) into \(k-1\) cliques is therefore a proper
\((k-1)\)-coloring of this complement.  Restricting the coloring to the
contained vertex set \(\{x\}\cup N_H(r)\) proves

\[
 \chi\!\left(H[\{x\}\cup N_H(r)]\right)\le k-1.
\]

The independent state \(T\) in \(G\) is a \(k\)-clique in \(H\).
Consequently

\[
 T-\{r\}\subseteq N_H(r)
\]

is a \((k-1)\)-clique of the displayed suspension.  Therefore

\[
 k-1
 \le
 \omega\!\left(H[\{x\}\cup N_H(r)]\right)
 \le
 \chi\!\left(H[\{x\}\cup N_H(r)]\right)
 \le k-1.
\]

This proves both exact equalities in (2.1).

The frozen theorem is stated for \(k\ge2\).  Any counterexample in the
campaign has \(k\ge3\), so there is no unhandled \(k=1\) edge case.

## 5. The dynamic case is a genuine extension

If \(rx\in E(H)\), then \(x\in N_H(r)\) and the suspension is just the
ordinary link covered by C-051.

If instead

\[
 rx\in E(G),\qquad T-r+x\notin\mathcal F,
\]

then \(x\notin N_H(r)\).  The new theorem says that adjoining this
additional vertex and all of its actual complement incidences to the
entire link still leaves chromatic number \(k-1\).  C-051 colors only
\(H[N_H(r)]\) and does not imply this extension.

For \(k=3\), the suspension is bipartite.  Within any connected component
of \(H[N_H(r)]\), two neighbors of \(x\) on opposite bipartition sides
would be joined by an odd path; adding their two incident \(x\)-edges
would form an odd cycle.  Thus the stated side-purity consequence is
correct.

## 6. No global gluing is asserted

In the equality-critical deletion branch, well-coveredness ensures that
every deletion vertex lies in a maximum independent \(k\)-state, so the
local theorem applies to each \(r\in R_x\).

For each such \(r\), however, the theorem produces a coloring only on

\[
 H[\{x\}\cup N_H(r)].
\]

The color names may be independently permuted on different projections,
and the projected eternal family need not be the greatest family of the
projected graph.  A clique partition of a projection gives static
colorability but does not certify original family-response membership.
Nothing in the proof synchronizes overlapping suspensions.

Accordingly, the note correctly declines to infer that
\(H[R_x]\) is \((k-1)\)-colorable, that the local colorings extend through
all of \(H-x\), or that a deletion coloring omitting one inactive-set
color exists.  The remaining problem is genuinely global.

The normalized \(n\le14\) UNSAT runs in Section 5 are explicitly labeled
`OBSERVED`; no theorem, certified finite exclusion, or coverage claim is
based on them.

## 7. Clean-room audit of the order-12 control

The checker
`reviews/all_k_extension_bridge_hostile/independent_check.py` imports no
candidate verifier, search code, graph library, or campaign evaluator.
It independently decodes the labeled graph6 record

```text
Ksv`f\knJVis
```

and reconstructs all claimed data.

### Full graph

The graph has order 12, size 39, and

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3).
\]

The greatest kernels for one, two, and three guards have sizes

```text
0, 0, 127.
```

Thus the 127-state family is literally the greatest eternal
triple-family.  All 1,143 unoccupied-attack obligations pass, with 1,422
retained legal responses.

For \(S=\{1,2,3\}\) and \(x=0\), all three guards can answer:

\[
 L_S(x)=\{1,2,3\}.
\]

The checker enumerated the seven maximum independent triples avoiding
\(x\), verified that their support is all 11 deletion vertices, and
checked active status on all 21 state/guard incidences.  It obtained

\[
 A_x=\{1,2,3,4,5,7,9\},
\qquad
 R_x=\{6,8,10,11\}.
\]

The inactive set is also exactly \(N_H(x)\), as declared.

### Deletion graph

For \(G-x\), the checker obtains

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,3).
\]

Its one-, two-, and three-guard greatest kernels have sizes

```text
0, 0, 101.
```

Thus the deletion is genuinely in the domination-drop branch:
\(\gamma(G-x)=2\) while
\(\alpha(G-x)=\gamma^\infty(G-x)=\theta(G-x)=3\).

### All deletion colorings

The checker exhausted all labeled proper three-colorings of
\(\overline{G-x}\), not merely color partitions modulo permutation.  There
are exactly 12.

- Six use two colors on \(R_x\), so each has one color available for
  \(x\).
- Six use all three colors on \(R_x\), so none extends by assigning a
  color to \(x\).
- Each color is the omitted color in exactly two successful colorings.

The serialized sorted coloring list has SHA-256

```text
1ab13aea2213114f4a43c53cfb921fe066fd329bf4158284292117f4b3d7ec4d
```

This proves precisely the advertised sharpness: an arbitrary deletion
coloring need not work, even with equality, a greatest family, and a full
target.  Because deletion domination drops to two, it does not refute the
desired coloring-existence statement in the equality-critical deletion
branch.

## 8. Reproduction

Run:

```text
python3 -I -B -W error \
  gamma_theta_eternal_domination/reviews/all_k_extension_bridge_hostile/independent_check.py
```

The strict run is deterministic and warning-free.  Exact source, control,
checker, coloring, and manifest hashes are recorded in `evidence.json`.
