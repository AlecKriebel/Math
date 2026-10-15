# First independent candidate assessment

Timestamp: 2026-10-14T05:21:32.625738+00:00. Completion estimate: 45% of this audit. Read both submitted proof bodies completely (PROOF_V2.md 94 lines; CANDIDATE_PROOF.md 72 lines). No original independent_review, saved PASS output, other family assessment, or root opinion read.

## Provisional finding
The submitted geometric mechanism matches the independently selected source-only family: double-pentagon involution yields a physical edge midpoint, its physical half-turn exchanges endpoints, and a unique-common-neighbor obstruction excludes graph distance2. I find no apparent geometric counterexample to the precise restricted theorem: edge trajectories, plus even-N trajectories whose transported-terminal angles satisfy beta-alpha=2*pi/5, cannot have distance2 endpoints. This is not yet a verdict that the source conjecture or original queue claim has been resolved.

## Independently checked algebra
Let P have p_j=sum_{a=0}^{j-1}r^a, r^5=1, sum r^a=0, Q=conjugate(P). Then 1-P=Q as an unlabeled set; h(z)=1-z swaps polygons and h(p0)=q1. P side j has vector r^j, its translated glued Q side has index -j (mod5), and h reverses the side parameter. Thus exactly the five edge midpoints are regular fixed points of h. For an even-N terminal corner in Q, the source transported-clockwise convention gives theta=alpha-beta modulo2*pi, so beta-alpha=2*pi/5 identifies outgoing Q edge q1->q2. Hence h(reverse sigma) starts in the same P corner with the same initial ray, not merely the same developed direction at the singularity. This is the load-bearing prong check; cone-angle6*pi makes direction alone insufficient.

The candidate does not assert that h lifts to the unfolding or that an arbitrary affine symmetry descends to D. Instead it projects to the double pentagon and separately uses an actual physical half-turn at the physical midpoint. This avoids the usual unjustified lift/descent obstruction. Its germ uniqueness argument is parameterized and tolerates self-intersections.

## Exact current gap and next checks
The declared parity-aware type is narrower than the bare p.506 angle shorthand at exceptional direct diagonals. Both candidates explicitly admit this mismatch. Even if the restricted geometry is fully correct, queue-level claimed_solved is only justified if the intended target is the source's parity-selected type rather than its literal shorthand/extracted dataset sentence. Source Definition2.1 uses non-strict boundary inequalities, so this is a real formulation audit gate; the candidate's claim that Fuchs states parity is *used to select* the type must be distinguished from the source's statement that a relation is divisible. The literal source adversary owns that semantic issue; I will not treat this first assessment as a proof that it is resolved.

Next: derive a complete coordinate/gluing and graph proof artifact, analyze odd/even exceptional branches and cover singularities, and record exact hypotheses for all classical dependencies. Do not rely on existing finite checker outputs.
