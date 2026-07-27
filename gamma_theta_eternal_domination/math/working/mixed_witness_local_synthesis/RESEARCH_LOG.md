# Mixed-witness local synthesis — research log

## 2026-07-26 16:55 PDT — scope fixed

Read the mixed-\(P_4\), frozen-color, and cross-state exchange notes and
their hostile reviews.  Fixed a labeled full-graph model on
\[
\{a,b,c,x_0,x_1,x_2,x_3,w\}
\]
and its one-vertex extension by an arbitrary \(y\).  The model keeps
\(S=\{a,b,c\}\) independent, makes \(x_0x_1x_2x_3\) an induced path in the
complement, and fixes \(w x_1,w x_2\notin E(G)\).

The exact-list family requirement is encoded literally: six positive
one-swap states must belong to the same dominating family, six negative
one-swap states must not, and every attack at every unoccupied vertex must
have a one-edge, one-guard successor in the family.

Best-guess completion: **30%**.

## 2026-07-26 17:08 PDT — independent preliminary exhaustion

There are 11 free edges at order eight and 19 at order nine, hence only
\(2^{11}=2,048\) and \(2^{19}=524,288\) labeled graphs.  A preliminary
standalone enumeration found:

- order eight: 62 graphs with \(\gamma=\alpha=3\), but no nonempty eternal
  family after the six negative swaps are banned;
- order nine: 8,985 graphs with \(\gamma=\alpha=3\), but again no nonempty
  safe family;
- among the unrestricted eternal-equality subpopulation, 9 order-eight and
  1,150 order-nine graphs survive, but none contains all six required
  positive swaps in its greatest family.

Because a proper family is a subset of the greatest family, the last fact
already prevents an exact realization.  The stronger banned-state fixed
point independently reaches the same zero.

Best-guess completion: **55%**.

## 2026-07-26 17:18 PDT — hostile strengthenings and scope mismatch

A complete cube-state CEGAR search was added for the open disjoint-triple
base-ordering question.  It branches on one omitted interior state of every
live base cube and recomputes the greatest safe family.  Preliminary output
found no counterexample among all 1,159 unrestricted eternal-equality
graphs in the local orders.

The permissive named-closure models supplied for comparison use a weaker
scope.  Every one of their eight order-eight masks has the dominating pair
\(\{a,x_1\}\), hence \(\gamma=2\).  Their \(y\)-extension has
\(a y\in E(G)\), so the same pair continues to dominate.  They are useful
local stress models but are not survivors of the full equality search.

After the independent setup, graph `HDzruf]` was supplied as a stress
test.  Direct decoding and literal recomputation give
\(\gamma=2,\alpha=\gamma^\infty=3\), a 46-state safe family, and the exact
mixed-\(P_4\) lists together with \(L(w)=L(y)=\{a,b\}\).  It confirms that
the equality hypothesis, rather than closure alone, is essential.

Best-guess completion: **75%**.

## 2026-07-26 17:30 PDT — full runs frozen

Completed all \(2^{11}\) order-eight masks and all \(2^{19}\) order-nine
masks.  Final exact-list realization counts are zero at both orders.

The decisive stage counts are:

| condition | order 8 | order 9 |
|---|---:|---:|
| \(\gamma=\alpha=3\) | 62 | 8,985 |
| all required states also dominate | 0 | 96 |
| nonempty safe family after six bans | 0 | 0 |

At order nine, 42 of the 96 static candidates have an unrestricted eternal
family, but closure retains at most four of the six required positive
swaps.  Every exact safe kernel becomes empty in two or three waves.

The proper-family base-ordering falsifier found no counterexample over the
9 + 1,150 unrestricted eternal-equality graphs.  A separate hostile probe
did find a useful limitation: 18 order-nine graphs have a jointly
unavoidable six-state negative set but no individually unavoidable member.
The exemplar `HCxrs`c` shows that a family-independent choice of one extra
response cannot be assumed.

The projection-gluing Theorem 2 and the `HDzruf]` scope were sanity-checked.
No defect was found; the 2-SAT edge case split is exhaustive under the
no-full-list hypothesis, and the graph is correctly scoped as a
\(\gamma=2\) countermodel only.

Source, checkpoints, JSON results, logs, and the synthesis note are frozen
under `mixed_witness_local_synthesis` paths.  No central registry was
edited.  No large job was run; the order-nine run took about 22 seconds on
the local machine.

Best-guess completion: **100%** for the requested bounded synthesis and
falsification task.  The universal analytic problem remains open.
