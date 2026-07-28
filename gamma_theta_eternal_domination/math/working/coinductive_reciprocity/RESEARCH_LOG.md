# Research log: coinductive complementary-exchange reciprocity

## 2026-07-28 PDT — checkpoint 1

- Reconstructed the accepted C-064 cross-state exchange theorem, C-108
  vertex-star propagation, and the C-134--C-138 greatest-family boundary.
- Confirmed that static reciprocity and equality of finite deletion ranks
  cannot support an induction.
- Derived the shared-pivot repair square recorded in `NOTE.md`: a one-sided
  active edge forces an induced four-cycle, five retained local
  configurations, the same asymmetry on the opposite edge, and reciprocity
  on the other two edges.
- Strengthened the reduction using the full common-nonneighbor set
  \(W=N_{\overline G}(u)\cap N_{\overline G}(x)\): \(W\) is a \(G\)-clique,
  every state \(\{u,x,w\}\) is retained, and these states are joined by
  unique one-guard moves over \(W\).
- Identified the exact greatest-family obstruction: the omitted corner can
  fail only through an attack outside its repair square whose every legal
  successor is outside the greatest kernel.  The response lists at such an
  attack split into a shared-pivot-active case and an exact paired-singleton
  case.
- Closed the deletion-rank base case: every omitted repair-square corner
  necessarily dominates.  If it missed a vertex, replacing the active
  endpoint in the resulting independent triple would retain a state that
  can dominate the opposite completion only through the allegedly missed
  edge.
- Strengthened that base case to arbitrary independent endpoints.  If a
  reverse state \(T-x+u\) missed \(r\), extend \(\{u,r\}\) to
  \(\{u,r,a\}\).  The retained \(u\to x\) successor forces \(a\) to cover
  both untouched vertices of \(T\); attacking either one then uniquely
  moves \(a\) and exposes the other.  An independent audit agent confirmed
  the argument, including the cases where the completion \(a\) coincides
  with an endpoint of \(T\).
- For a globally minimum-rank omitted corner, derived three exact adjacency
  caps on every deleting attack.  Each cap is proved by identifying a
  legal lower-rank successor as another shared-pivot omitted corner.  This
  is a one-sided rank descent and does not assume the false equality of
  paired finite ranks.
- In the paired-singleton blocker branch with blocker nonadjacent to the
  shared pivot, proved a second propagation step: the blocker is adjacent
  to all four cycle vertices, and every completion of the blocker--pivot
  independent pair is forced to answer at the two opposite cycle vertices.
  Either forbidden responder would turn a lower-rank successor into a new
  omitted repair corner.
- Replayed `FCXfO` as a sharp control.  Its accepted proper eternal family
  realizes the repair square and omits one corner; its greatest family adds
  that corner.  Thus the square theorem alone cannot be mislabeled as
  greatest-family reciprocity.
- Falsified the stronger transformation claim that an active replacement
  \(u\to x\) maps every greatest-family state containing \(x\) to a
  greatest-family state containing \(u\).  Across the accepted complete
  order-nine equality census there are 4,108 violations among 220,086 such
  transforms; the first is `HCOeuqr`.  Its translated state is
  non-dominating, so even the weaker whole-kernel translated-domination
  premise is false under full equality.  This does not affect reciprocity,
  which concerns independent endpoint states only.  The sharp
  \(\gamma=2\) asymmetric control `GEjbug` has four more non-dominating
  whole-kernel translations, while its named complementary reverse corner
  dominates and is deleted at rank one.
- Tested the proposed rank-transport shortcut saying that the least-rank
  reverse state of an inactive orientation can always be chosen with a
  common-nonneighbor pivot.  The actual one-sided-active premise has no
  order-nine instances, but the strongest nonvacuous inactive-orientation
  surrogate fails 422 times among 16,366 oriented edges.  In the first
  control, ``HCOe`Z{`` at \((u,x)=(8,0)\), the five reverse ranks are
  \(1,1,2,0,0\), while the only shared-pivot rank is \(2\).  Therefore an
  argument transporting a global rank minimum into the repair-square class
  must use the forward-active hypothesis essentially; inactivity alone is
  insufficient.
- Time-boxed a discovery SAT check for a disjoint-endpoint order-ten
  equality countermodel using the accepted exact-kernel encoding.  The
  418,965-variable, 1,445,305-clause instance returned `UNKNOWN` when
  interrupted after 30 minutes.  No result or claim is attached to this
  timeout.
- As a separate falsification check, replacing the final reverse-survival
  condition by reverse non-domination made the same exact order-ten CNF
  return UNSAT in 2.6 seconds.  This is discovery corroboration only; the
  all-order theorem is established by the preceding human-readable proof,
  not by that unlogged solver result.

Best-guess completion toward the assigned all-order reciprocity decision:
**60%**.  The local normal form and general rank-zero base are rigorous,
and two tempting stronger coinductive shortcuts now have exact
countercontrols.  The external-blocker descent itself is not yet closed.

## 2026-07-28 — hostile correction and reciprocal third base

- Corrected the hostile review's sole required candidate edit: the
  `FCXfO` paragraph now points to the five states in (6.4), not the
  unrelated display (6.1).
- Strengthened the nonadjacent-pivot paired-singleton branch.  Its
  independent completion \(U=\{r,w,c\}\) must answer attacks at \(u,z\)
  by moving \(r\), because the only possible \(c\)-successors are the two
  lower-rank states excluded by the deleting attack.  This retains
  \(\{u,w,c\}\) and \(\{z,w,c\}\).
- Together with Lemma 5.4 and the paired-singleton responses, the three
  maximum independent bases \(S,T,U\) witness reciprocal active pairs
  \(r\leftrightarrow u,z\) and \(c\leftrightarrow a,x\).  This is a
  structural completion, not a proof that the original omitted corner
  survives.
