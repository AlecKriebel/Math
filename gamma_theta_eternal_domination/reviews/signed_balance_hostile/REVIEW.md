# Hostile review: exact-two-list signed balance

Date: 2026-07-28 PDT

## Verdict

**PASS, unconditional relative to the named accepted dependencies.**

The frozen candidate proves:

> Let \(\mathcal F\) be an eternal family of dominating triples, let
> \(S=\{a,b,c\}\in\mathcal F\) be independent, assume
> \(\gamma(G)=3\), and suppose every outside response list at \(S\) has
> size exactly two.  Then \(\overline G\) is three-colorable and
> \(\theta(G)=3\).

Every type incidence, family-membership premise, one-guard attack,
blocked move, domination miss, transversal-witness collision, signed
parity step, and final coloring bound survives hostile reconstruction.
No missing family response is used as a graph nonedge.

The scope is exact and important.  This closes only the
**exact-two-list branch at one independent retained state**.  Singleton
lists, full lists, the complete \(k=3\) theorem, higher parameters, and
the universal gamma--theta conjecture remain open.

## Frozen byte binding

| artifact | SHA-256 |
|---|---|
| candidate `NOTE.md` | `fed9c26bd094347eb19f9cecc0f98aa29420a210a14e96b457ac106a47e59175` |
| candidate `verify_symbolic.py` | `96764c9b1dec42c24610e9f1cbd5d19574c73fabcf132272d719d99256d7d941` |
| candidate `MANIFEST.sha256` | `c42169d2ad3c82f999aae3b49d2d597a182d21c39db69d804b1cfeb0b870e026` |
| candidate `RESEARCH_LOG.md` | `e9edd6f52e46d77f774eb11bc42223422f1f71a0f3a131c8f04c6a119f913536` |
| independent `independent_check.py` | `cdc73dbb22584dc385055c89c1283c1232bf6ba8dfd6b768de4ae2cf9e89883f` |

The candidate manifest itself contains the correct hashes of its note
and checker.  Its strict checker output has 23,135 bytes and SHA-256
`da17105109964985501a0bd36aef4013f90b01db2f88d1542d2ed9b18138015e`.

The prerequisite statements were reread at these exact bytes:

| accepted dependency | SHA-256 |
|---|---|
| C-111 physicality, `dynamic_type_sparsity/NOTE.md` | `f3309daa2497a10c978fac28286959d6ec2fb52e8438c727cdf2eafce89aa1a7` |
| C-063 frozen projection, `k3_cross_state_attack.md` | `3e87ca4e7c04987c2f56576c4e8b0f28113e254fdb1a024b4da7a3e0d6bf4c68` |
| C-079 odd fan, `k3_long_bicycle_connectors/NOTE.md` | `d3a23bb0171a047a85f2a05c5ccb5faeef0c0c7ceb6d7bb139c6a7a86b8b1f10` |
| C-086 side-purity source, `k3_side_purity_cap_cycle/NOTE.md` | `64312289f6d3d87a4c302692c92901caeb9788b16354493e07be01920549f11b` |
| C-114 shortening source, `physicality_bicycle_endgame/NOTE.md` | `b282d96e1582ff9100bbdf6a81d9f1b29d2d76a3565e4a0d3cfbbb08886d0d91` |

## Hypotheses and physical types

The theorem's hypotheses already place it at common parameter three.
The independent retained triple gives \(\alpha(G)\ge3\), while the
eternal triple-family gives \(\gamma^\infty(G)\le3\).  The accepted
chain \(\alpha\le\gamma^\infty\), together with \(\gamma(G)=3\), gives
\(\alpha=\gamma^\infty=3\).

C-111 is invoked with exactly its hypotheses and yields

\[
 L_S(x)=N_G(x)\cap S
 \qquad(x\notin S).
\]

Thus a type-\(t\) vertex has precisely one anchor neighbor in
\(H=\overline G\), namely \(t\), and is adjacent in \(G\) to the other
two anchors.  Every direct root in Section 4 removes an anchor that is
in the attacked vertex's exact response list.  The only successors
rejected solely by family membership are:

- \(S-b+u\) in `0012`, where \(u\) has type \(b\); and
- \(S-a+p\) in `00121`, where \(p\) has type \(a\).

These are exact direct-response absences.  All other rejected successors
are rejected because they provably fail to dominate.

## Mates, side-purity, and transversal witnesses

For \(x\in W_t\), the pair \(\{t,x\}\) does not dominate.  Its common
complement neighbor \(x'\) cannot be either other anchor because both
are \(G\)-adjacent to \(x\).  Hence \(x'\) is outside.  The literal edge
\(tx'\in E(H)\), combined with C-111, makes \(x'\) type \(t\).  It is
distinct from \(x\) and is a literal same-type complement mate.

For an outside hub \(x\) of a different type, that mate is positive in
the omitted color under consideration and is a distinct complement
neighbor of the hub.  Every distinctness and positivity premise of the
accepted C-079/C-086 side-purity theorem therefore holds.  If the hub is
already in the projection, ordinary bipartiteness gives the same
conclusion.  Universal side-purity is valid for every outside hub and
every component of every type projection.

For a cross-type edge \(xy\), \(\gamma(G)=3\) supplies a common
complement neighbor.  No anchor is common because each endpoint has
exactly one, and the two anchor types differ.  A common neighbor of
either endpoint type would make the other endpoint see both sides of a
same-type projection edge, violating universal side-purity.  Therefore
every common neighbor is outside and has the third type.  In particular,
every cross edge has a literal transversal-triangle witness.

The collision audit is complete:

- in `00102`, the only cycle vertex of the witness's third type is
  \(z\), but the witness must see \(y\) in \(H\), whereas \(zy\) is an
  induced-cycle chord and lies in \(G\); the witness is therefore new;
- in `00101`, no cycle vertex has the third type, and the two outside
  witness roles have exactly the two set partitions \(t=s\) and
  \(t\ne s\).

No other anchor, endpoint, cycle-vertex, or witness collision is
possible.

## Exact signed-coloring equivalence

Fix the three anchor colors cyclically.  A type-\(t\) outside vertex can
use exactly \(t-1\) or \(t+1\); encode these as the two chiralities.

- A same-type complement edge is proper exactly when its endpoint
  chiralities differ.
- A cross-type edge lies in a transversal triangle.  Exhausting the
  eight chirality assignments of that triangle shows that it is properly
  colored exactly when all three chiralities agree.

Conversely, a chirality flip on a same-type edge and chirality agreement
on a cross-type edge always give different endpoint colors.  The anchor
spokes are proper because a type-\(t\) vertex avoids anchor color \(t\).
The independent checker exhausts all 12 same-type rows, all 48 ordered
transversal-triangle rows, and all three anchor-list rows.

Consequently three-colorability is exactly consistency of

\[
 \chi(x)\oplus\chi(y)
 =
 \begin{cases}
 1,&\tau(x)=\tau(y),\\
 0,&\tau(x)\ne\tau(y).
 \end{cases}
\]

There is no one-way implication hidden here.

## Shortening and orbit coverage

A shortest unbalanced cycle is chordless: a chord splits it into two
strictly shorter cycles, and the xor of their signed parities is the
original parity.

If distinct-type vertices \(x,y\) have both cycle arcs of length at
least three, their common complement neighbor is outside \(S\).  It is
also outside the cycle: on a chordless cycle, both incident complement
edges would otherwise be cycle edges and make one \(x\)-\(y\) arc have
length two.  Adding the genuine two-edge path \(xzy\) to each cycle arc
therefore gives two simple, strictly shorter cycles.  Their parities xor
to the original parity because both shortcut edges occur twice.

Thus a shortest unbalanced cycle contains no such distinct-type pair.
At length six, opposite types repeat and every edge sign occurs in an
opposite pair, so the parity is even.  At every length at least seven,
the distance-three and distance-four equalities force consecutive
vertices to have the same type.  An unbalanced constant-type cycle is
odd, contradicting bipartiteness of that type projection.

Independent first-occurrence/dihedral enumeration gives precisely:

\[
\begin{array}{c|l}
3&000,\ 001\\
4&0012\\
5&00000,\ 00001,\ 00011,\ 00101,\ 00102,\ 00121.
\end{array}
\]

A separate semantic projection test removes `000`, `001`, `00000`, and
`00001`, leaving exactly the five claimed skeletons.  This does not rely
on a hard-coded removal list.

## Six one-guard attack reconstructions

The clean-room checker uses a maximal-response convention: every
unspecified template pair is treated as a \(G\)-edge, so every
potential guard move is allowed.  All blocked moves and domination
misses use displayed literal \(H\)-edges.  Extra \(H\)-edges can only
delete moves, never repair a rejected successor.

| skeleton | retained root and attacks | decisive rejected successors |
|---|---|---|
| `0012` | \(\{a,c,p\}\), attack \(u\) | misses \(v\), misses \(q\), or exact direct response absent |
| `00011` | \(\{a,b,p\}\); attacks \(v,r,a\) | forced states \(\{b,p,v\}\), \(\{p,r,v\}\); terminal shape misses \(q\) |
| `00121` | \(\{b,c,v\}\); attacks \(p,q,b\) | forced states \(\{c,p,v\}\), \(\{p,q,v\}\); terminal successors miss \(u,w,a\) |
| `00102` | \(\{a,c,z\}\); attacks \(x_0,y,q,a\) | forced states \(\{a,x_0,z\}\), \(\{x_0,y,z\}\), \(\{y,z,q\}\); terminal successors miss \(c,x_1,x_2\) |
| `00101`, \(t=s\) | \(\{a,b,v\}\); attacks \(r,q,u\) | the only final successor shape \(\{q,u,r\}\) misses \(t\) |
| `00101`, \(t\ne s\) | \(\{a,b,v\}\); attacks \(r,q,u,c\) | forced \(\{a,r,v\}\), \(\{a,q,r\}\), \(\{q,u,r\}\); terminal successors miss \(s,a,t\) |

Every attack is at an unoccupied vertex and every actual move changes
exactly one guard along one \(G\)-edge.  A displayed complement edge
blocks rather than permits a move.  The clean-room checker emits the
detailed response-by-response record; `EVIDENCE.md` binds that
deterministic output by byte count and SHA-256.

One harmless presentational subtlety occurs in the collided `00101`
case.  The candidate checker first records the only successor shape as
“forced,” then immediately proves that shape nondominating.  The
clean-room semantic checker instead ends the attack at \(u\): all legal
successors are already invalid.  These are the same reductio and do not
change the proof.

## Final bounds and exact scope

Signed balance makes chirality propagation path-independent in every
component of \(H-S\), producing a proper three-coloring of all of \(H\).
Hence \(\theta(G)=\chi(H)\le3\).  Since the independent set \(S\) is a
triangle in \(H\), \(\chi(H)\ge3\).  Therefore

\[
\boxed{\theta(G)=3}.
\]

This is a theorem for the exact-two-list branch only.  In particular,
the audit does **not** promote any claim about singleton lists, full
lists, all \(k=3\) equality graphs, higher \(k\), or the universal
conjecture.
