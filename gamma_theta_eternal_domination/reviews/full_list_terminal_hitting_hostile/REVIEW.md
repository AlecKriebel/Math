# Hostile review: full-list terminal hitting, Kempe ears, and cap locations

## Verdict

**PASS.**

Every statement labeled `PROVED` in the reviewed target is valid at its
stated conditional boundary.  I found no quantifier change, unsupported
family-to-greatest-family replacement, occupied attack, omitted one-guard
response, graph/complement reversal, or conversion of a missing family
response into a graph nonedge.

The exact reviewed target is:

| artifact | bytes | SHA-256 |
|---|---:|---|
| `math/working/full_list_terminal_hitting/NOTE.md` | 25,273 | `d91fe6087283f92a6ca295f5b9a2a43e7d8ad0a34e89a811490d22bc729595ce` |

The repository `HEAD` at the audit snapshot was
`dda39ca4812d7131eb6274a273a56ff55c8c814c`.  The target was untracked at
that snapshot, so the SHA-256 above, rather than the repository commit, is
the decisive byte binding.

This verdict accepts only the conditional reductions stated in the target.
It does not prove that one of the three augmented formulas is satisfiable,
exclude the base-unsatisfiable branch, identify a terminal-cube move with a
2-SAT or Kempe connector, finish the single-full slice, or resolve the
gamma--theta conjecture.

## Dependency and claim-status audit

I read the exact C-072--C-084 entries in `CLAIMS.md` and the proof-bearing
parts of their dependencies.  The decisive current target hashes are:

| prerequisite | SHA-256 |
|---|---|
| `math/working/k3_projection_gluing.md` | `fc7f817aa611751b9bedbb9ddebd5830d81f02719f2d8aafe914db34f4c64907` |
| `math/working/k3_full_list_slice/NOTE.md` | `ebcf7a6ef902889e5d70a657baf7e79613b3dd0e278be01263cf0882033d23be` |
| `math/working/k3_twosat_bicycle/NOTE.md` | `8a934a8194913633821223b070a013dda8e0cd8c0d6870616b32a882e8b2fd59` |
| `math/working/full_list_deletion_dichotomy/NOTE.md` | `3273c1e4a1b042bcaa2ebdda416d2591ec83c93be535e14ff2c585932c2b5ee1` |
| `math/working/k3_long_bicycle_connectors/NOTE.md` | `d3a23bb0171a047a85f2a05c5ccb5faeef0c0c7ceb6d7bb139c6a7a86b8b1f10` |
| `math/working/dynamic_connector_edge_caps/NOTE.md` | `185e29a4b8e231aa5e90126f7fd16be32c696cd3f99e46c00f90cb61f27548e7` |
| `math/working/gamma3_port_identification_proof/NOTE.md` | `0b852592548e72face4eb8944909c1dd24c4fbedd31e1a468d118ceb9b0d1487` |
| `math/lemmas/k3_structural_day1.md` | `00d6fb851a3cb50ed907a593b0379376571251f8604974b5b67e05e2b0705d6e` |

The target uses C-073, C-075, C-079, C-080, C-082, and C-083 only within
their proved scopes.  It treats C-074 and C-076 as finite controls, C-077
and C-084 as bounded observations, and C-081 as a refuted strengthening and
gamma-two boundary example.  It does not promote any of those finite or
negative records to a universal theorem.  C-072 and C-078 are contextual
accepted results and are not silently used to strengthen a proof.

The three especially important imported results match the target exactly:

1. deletion of \(x\) preserves the same arbitrary specified family lists
   on all remaining vertices and leaves no full vertex when
   \(F_3(S)=\{x\}\);
2. a normalized inclusion-minimal unsatisfiable 2-CNF has at most two unit
   clauses, with the stated two-unit, one-unit, and unit-free terminal
   forms; and
3. in the critical deletion branch every deletion coloring saturates the
   complement link, has all three pairwise Kempe linkages, and has the
   distinct-spoke dominating-pair/\(Z\)-witness fork.

No longer physical bicycle, common-port recurrence, or family-preserving
Kempe swap is imported.

## Fixed-core hitting and rainbow selection

Fix one inclusion-minimal unsatisfiable core
\(M_w\subseteq\Phi\wedge U_w\) before considering any satisfying
assignment of \(\Phi\).  Since \(\Phi\) is satisfiable, \(M_w\) must contain
at least one marked augmentation clause.  After the accepted normalization,
every nonconstant clause contributed by \(U_w\) is a unit forbidding the
port event \(\kappa(r)=w\), and the terminal trichotomy gives at most two
unit clauses in \(M_w\).

Let \(A_w=M_w\cap U_w\).  For any satisfying assignment of \(\Phi\), all
clauses of \(M_w-A_w\) are already satisfied.  If every physical support
chosen for \(A_w\) avoided color \(w\), all clauses in \(A_w\) would also be
satisfied, contradicting unsatisfiability of \(M_w\).  Hence the same fixed
one- or two-vertex set hits every satisfying assignment of \(\Phi\).

The physical-support count is sound even under logical duplicate removal.
An inclusion-minimal core retains at most one occurrence of a duplicate
unit.  One may retain its marked physical origin; if several augmentation
origins induce the same literal, their port events are the same Boolean
event, so any one origin is a valid representative.  Thus normalization
does not inflate the support set beyond the one or two selected units.

An immediate singleton conflict is handled separately: its unique list
color forces that support to have color \(w\) in every compatible deletion
coloring.  The core is never reselected as the coloring changes.

Applying the fixed-core argument separately for \(a,b,c\) gives three fixed
sets whose union has at most six vertices.  For one common deletion
coloring, choose a color-\(u\) hit from each \(T_u\).  The selected vertices
are necessarily distinct because one vertex receives only one color.  The
corollary correctly does not claim that the transversal itself is fixed
independently of the coloring.

## Terminal cube and singleton exclusion

For distinct \(r_a,r_b,r_c\in R\) with \(u\in L(r_u)\), every first-level
state \(S-u+r_u\) is in the same family \(\mathcal F\), and the move edge
\(ur_u\in E(G)\) is forced by that membership.  In any ordering, the next
attacked terminal is unoccupied and its same-label anchor is still
occupied.  Every earlier accepted same-label move leaves exactly one guard
associated with each original label.

The all-terminal state has three guards in \(R=N_H(x)\), so it does not
dominate \(x\) in \(G\) and cannot be retained.  The first same-label
failure is therefore at level two or three.  Closure is applied to a
retained current state and an unoccupied attack; after the same-label
successor is excluded, any retained response must move one of the other two
occupied guards.  This proves the cross-label conclusion without assuming
an \(H\)-edge.

The rainbow-singleton attack proof exhausts every occupied guard:

- If \(D_{ab}\notin\mathcal F\), attack \(r_b\) from
  \(D_a=\{r_a,b,c\}\).  The \(b\)-successor is \(D_{ab}\); an \(r_a\)-move,
  if its graph edge exists, is the absent direct state
  \(S-a+r_b\).  Closure therefore forces the \(c\)-successor
  \(E=\{r_a,b,r_b\}\).  Attacking the unoccupied anchor \(a\) from \(E\)
  leaves no response: \(b\) is blocked by independence of \(S\), and the
  other two possible successors are the absent states \(S-c+r_b\) and
  \(S-c+r_a\).
- If \(D_{ab}\in\mathcal F\), attack the unoccupied \(r_c\).  The
  \(c\)-successor fails to dominate \(x\).  A retained \(r_a\)-successor
  is killed by the subsequent unoccupied attack at \(b\), and a retained
  \(r_b\)-successor is killed by the subsequent unoccupied attack at \(a\).
  In each case the anchor guard is blocked by independence and the other
  two successors are excluded by exact singleton-list nonmembership.

Statements such as “if that graph edge exists” are used in the right
direction: a missing list entry excludes a successor from \(\mathcal F\),
not the move edge from \(G\).  If the move edge is absent, there are simply
fewer candidate responses.

Consequently three failed augmentations cannot all be immediate singleton
constants.  The accepted terminal trichotomy then gives at least one marked
one-unit lollipop or two-unit chain.  The target does not shorten that
logical core to an unproved physical connector.

## Spoke consequence

For a selected two-list terminal \(r_w\notin A_\ast\), write
\(L(r_w)=S-\{\tau(w)\}\) and \(r_w\in A_{\tau(w)}\).  Since the compatible
coloring assigns \(w\in L(r_w)\), \(\tau(w)\ne w\).  The three values of
\(\tau\) cannot all equal one anchor, since evaluating at that anchor would
give \(\tau(u)=u\).  Thus two selected terminals lie on distinct spokes.

The imported fork then has the exact complement sign: such a pair has no
common \(H\)-neighbor in \(R\), so it either dominates \(G-x\) or has a
common complement neighbor in \(Z\).  The first option is impossible when
\(\gamma(G-x)=3\).  The target explicitly leaves singleton and
\(A_\ast\) terminals outside this corollary.

## Kempe-ear dichotomy

For a fixed color pair \(i,j\), the imported criticality lemma supplies a
bichromatic component meeting \(R_i\) and \(R_j\).  A shortest path between
the two endpoint sets is induced: any chord shortens the path, while a
proper bichromatic coloring already forbids equal-colored chord endpoints.

The ordered list of its \(R\)-vertices begins in color \(i\) and ends in
color \(j\), so some consecutive pair \(r,s\) in that list has different
colors.  The intervening subpath \(Q\) has no internal vertex in \(R\).
If \(Q\) is one edge, it is the asserted \(i\)-\(j\) edge of \(H[R]\).
Otherwise bichromatic alternation makes its length odd and at least three.

Now \(x\) is adjacent in \(H\) exactly to the two endpoints among the
vertices of \(Q\): the endpoints lie in \(R=N_H(x)\), while every internal
vertex lies outside \(R\).  The shortest-path choice excludes an endpoint
chord.  Hence \(Q+x\) is an induced cycle of odd length at least five.
The accepted odd-wheel obstruction rules out any external vertex complete
to this rim, giving the stated hub-free odd hole.  No family-preserving
Kempe swap, common witness for different color pairs, or membership of the
ear endpoints in \(T_w\) is claimed.

## Dynamic-cap location trichotomy

For an all-dynamic omitted-\(a\) complement edge \(yz\), C-082 gives a
nonempty \(G\)-clique of outside \(a\)-positive caps.  The graph edges
\(ay,az\in E(G)\) exclude the anchor \(a\) itself, while the dead-state
argument excludes the other anchors.

If a cap \(t\ne x\), then both \(t\) and the full vertex \(x\) lie in
\(P_a\).  C-083's positive-completeness theorem applies with four distinct
vertices and gives \(tx\in E(G)\).  When \(y,z\) are not both in \(R\),
\(x\) is not a cap.  Since \(\gamma(G)=3\), the pair \(\{x,t\}\) is not
dominating and therefore has a common complement neighbor
\(w\in N_H(x)\cap N_H(t)\).

Every such \(w\) lies in \(R\).  If it were \(a\)-positive, it could not
equal \(y\) or \(z\), which are \(a\)-omitting, and cap completeness would
give \(tw\in E(G)\), contradicting \(tw\in E(H)\).  Thus every escape lies
in \(R\cap W_a\).

The three location cases are exhaustive because \(y,z\notin S\), neither
can equal the full \(a\)-positive vertex \(x\), and every outside
non-\(R\) vertex lies in \(Z\):

1. if both endpoints lie in \(R\), \(x\) itself is a positive cap;
2. if exactly \(y\) lies in \(R\), then \(y\) is a common complement
   neighbor of \(x\) and every cap \(t\);
3. if both lie in \(Z\), any escape \(w\) is distinct from them because
   \(xy,xz\in E(G)\), and \(w\) cannot see both in \(H\), since
   \(\{t,w,y,z\}\) would then be an \(H\)-\(K_4\), contradicting
   \(\omega(H)=\alpha(G)=3\).

All six edges in the last \(K_4\) check have the stated source.  The target
correctly observes that the \(R\)--\(R\) and \(R\)--\(Z\) cases do not force
a new \(Z\)--\(Z\) connector, so cap propagation does not yet iterate
universally.

## Quantifiers, graph signs, and stopping boundary

All analytic arguments retain the original arbitrary specified eternal
family \(\mathcal F\).  The greatest eternal family appears only in named
finite controls where it is explicitly stated.  Deletion uses
\(\mathcal F^{-x}\), not a replacement by the greatest family of \(G-x\).

Positive list membership is used to infer both direct-state membership and
the necessary move edge in \(G\).  Negative list membership is used only to
exclude the corresponding direct state from \(\mathcal F\).  Complement
edges block guard moves or certify independence, and common complement
neighbors encode failure of domination.  These directions are consistent
throughout.

The final branch split is exact.  If \(\theta(G-x)>3\), satisfiability of
\(\Phi\) would give a forbidden three-coloring of \(H-x\).  In the
\(\theta(G-x)=3\), base-satisfiable branch, all later conclusions remain
conditional and the target lists the unresolved identification, singleton,
\(A_\ast\), separated-port, longer-chain, and base-unsatisfiable branches.
No claim in the note crosses that stop gate.
