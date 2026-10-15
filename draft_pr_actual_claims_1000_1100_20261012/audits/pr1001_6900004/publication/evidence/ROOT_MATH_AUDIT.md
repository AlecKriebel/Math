# Root mathematical audit of the full partition theorem

Claim: for all positive n,d and simple graphs G,H on the same labelled [n],
the full connected coordinate-sign-equivalence partitions of (R^d)^n are equal
if and only if the edge sets agree. All configurations, including collisions,
are retained. This is exact equality of subsets of the common configuration
space; it does not classify arbitrary abstract or ambient equivalences.

## Independent matrix derivation

Orient the edges of a graph H arbitrarily. Let C_H be its vertex-edge incidence
matrix, with +1 at the initial vertex and -1 at the final vertex. For a
collinear configuration p_i=x_i a with a nonzero vector a, put
delta_e=x_v-x_u for an oriented edge e=(u,v). The equilibrium operator is the
incidence operator with its edge columns multiplied by delta_e, followed by
the injective map sending a scalar vertex force to its vector multiple of a.
Thus, when no H-edge collapses,

    W_H(P) = diag(delta_e)^(-1) ker(C_H).

This proves the submitted transport formula without constructing a kernel
basis or assuming a generic-rank theorem. Along a continuous collinear path
without collapsed H-edges, every delta_e has constant nonzero sign. Multiplying
edge coordinate e by delta_e(0)/delta_e(t) is therefore a positive diagonal
linear homeomorphism from W_H(P(0)) onto W_H(P(t)). The formula has a genuine
inverse. All vertex equations hold term by term, including the opposite sign
at the other endpoint. The construction preserves zero coordinates as well
as positive and negative ones.

The entire configuration path belongs to one fibre-equivalence class. A
connected subset of a topological space is contained in a connected component;
therefore the path lies in one H-stratum. Endpoint equivalence alone would
not suffice, and is not being used.

## Distinguishing an arbitrary missing edge

For e={i,j} in E(G) minus E(H), take x_i(t)=t, x_j(t)=0, and pairwise distinct
fixed x_k>=2 for the other vertices, for -1/2<=t<=1/2. Then H has no collapsed
edge on the entire path, even though the missing pair collides at t=0.

At t=0, a G-stress positive only on e satisfies every equilibrium equation.
At t=1/4, no such stress exists: its endpoint force is a nonzero scalar
multiple of p_j-p_i. A coordinate-sign-preserving homeomorphism would preserve
the existence of that support/sign pattern. Hence the two G-fibres are
inequivalent. The two points are in the same H-stratum and different G-strata,
so the full partitions differ. This argument works for every differing graph
pair, after interchanging G,H if needed. The converse is immediate.

## Boundary and scope checks

- n=1 has only the empty simple graph and is immediate.
- n=2 reduces to a single edge versus the empty graph; the empty diagonal map
  is the unique isomorphism of zero stress spaces.
- The construction works in every d>=1, by any nonzero a. Collinearity is a
  witness inside the full space, not a restriction of the stated theorem.
- Stress-space dimension alone cannot substitute for sign equivalence. For
  K3 on the line, pair collision and separation both have nullity one, but
  their stress supports differ. The submitted narrow source arithmetic note
  follows directly from the three symmetric-edge equilibrium equations.
- Nonedge coordinates are fixed zero in the source's redundant array notation;
  the edge-coordinate representation is equivalent, with the same scaling
  applied to both symmetric entries.
- d=0 would invalidate the distinguishing construction and is excluded by the
  source's positive-dimension definition. Loops, parallel edges, removed
  collisions, generic-only spaces, and arbitrary ambient homeomorphisms are
  different problems; no conclusion is asserted for them.
- Vertex permutations give the stated corollary by reindexing both points and
  edge weights. This does not silently extend to arbitrary homeomorphisms.

Root found no mathematical gap in the precise literal theorem. Fresh independent
adversarial review and priority review remain required before acceptance for
publication. The source's unstated alternative interpretations are preserved
as limitations, not filled in by assumptions about author intention.

## Computation evidence

Both submitted exact-rational programs were inspected before execution and
ran successfully in normal, -O and -OO modes. All mathematical output fields
match their pinned references. The original references report UID1000; fresh
root executions report UID501. This difference is expressly recorded as
execution identity, and no claim is made to have replayed the historical
UID1000 permission-control harness. Complete fresh raw outputs are retained
in root_reproduction/. Finite computations corroborate the formulas, not the
universal proof, source intention, or novelty.
