# Attempt 1: isolate the finite-decomposition bottleneck

Time: 2026-10-03T13:18:00Z. Budget: 1/5.
Outcome: a conditional, quantitative finite-presentation lemma; the general
subgroup decomposition remains unproved. Completion estimate for the full
question: 10%, a subjective planning estimate, not a probability of truth.

## Mechanism

Try the classical proof using a finite graph of groups for each finitely
generated subgroup. Rather than assume that such a graph exists in the pro-p
category, separate the finite-presentation implication from its existence.
All amalgams and finite graphs below are proper.

Let K be a finitely generated pro-p group with a presentation as the fundamental
pro-p group of a finite connected graph of pro-p groups (A, Delta). Suppose:

- each edge group A_e is finitely generated;
- each vertex group is isomorphic to a closed subgroup of a coherent pro-p
  group (for our application, a conjugate of G1 or G2).

The conclusion is that K is finitely presented, even though finite generation
of the vertex groups was not an initial assumption.

## Proof of finite generation at the vertices

Write d(P) = dim_Fp H^1(P,Fp), possibly infinite. The continuous
Mayer–Vietoris sequence of this finite proper graph gives an exact segment

H^1(K,Fp) -> direct_sum_v H^1(A_v,Fp) -> direct_sum_e H^1(A_e,Fp).

The outer spaces have finite dimensions d(K) and sum_e d(A_e). For a linear
map B -> C, B has dimension at most dim ker + dim C. Exactness therefore gives

sum_v d(A_v) <= d(K) + sum_e d(A_e).

This uses only a finite direct sum, so no unproved interchange of cohomology
with an infinite product is involved. In particular every d(A_v) is finite.
For a pro-p group finite d is equivalent to finite topological generation.
Since each A_v lies in a coherent group, A_v is finitely presented.

## Explicit finite presentation

Choose presentations A_v = <X_v | R_v>_pro-p with |X_v| = d(A_v), and
choose topological generators z_e,1,...,z_e,d_e for each A_e. Fix a maximal
subtree D of Delta. Use the union of all X_v and one stable letter t_e for
each edge outside D. For an edge in D add the d_e relations identifying the
two images of z_e,j; for an edge outside D add the conjugacy versions.
The maps out of A_e agree on a dense generated subgroup once they agree on
the z_e,j, hence by continuity on all of A_e. Thus these finitely many
relations have the universal property of the fundamental pro-p group.

Consequently there is a presentation of K with

number of generators = sum_v d(A_v) + b1(Delta),
number of relations <= sum_v |R_v| + sum_e d(A_e).

In particular this proves finite presentability without requiring a
presentation for A_e itself. Alternatively, the next cohomology segment gives

dim H^2(K,Fp) <= sum_v dim H^2(A_v,Fp) + sum_e d(A_e),

which is the same finiteness conclusion. These bounds are upper bounds on
this construction; they are not assertions that the presentation is minimal.

## Apply to the exact target

If H has a finite subnormal series with procyclic factors, every closed
subgroup of H has a series obtained by intersection, again with procyclic
factors. Such subgroups are finitely generated (induction through extensions).
Therefore any finite subgroup decomposition of K with vertex groups inside
conjugates of Gi and edge groups inside conjugates of H satisfies the lemma.

For a faithful K-action with finitely many maximal vertex stabilizers up
to K-conjugacy, Chatzidakis–Zalesskii Theorem 5.1 supplies the finite
decomposition required above. For a nonfaithful action, first factor out
its kernel N. If the action fixes a vertex, K is already finitely presented
by coherence of that stabilizer. Otherwise the tree has an edge and N lies
in a polycyclic edge stabilizer; hence N is polycyclic and finitely presented.
The vertex stabilizers of K/N are the former vertex stabilizers modulo N
and are coherent by Lemma Q of Attempt 2. Maximal vertex stabilizers and
their conjugacy classes correspond under this quotient, while quotient
edge stabilizers remain polycyclic and finitely generated. Apply Theorem
5.1 and the finite-decomposition criterion to K/N. Lemma E of Attempt 2
then lifts finite presentability to K. These elementary permanence facts
are proved in Attempts 2–3. The unresolved step is still to establish the
requisite stabilizer finiteness, or another suitable decomposition, for
every finitely generated K. It is not enough that G itself has a one-edge
decomposition.

This audited clarification asserts the finite-presentation consequence for
the nonfaithful action; it does not assert an unproved lifted finite graph
decomposition of K. It is a correction within Attempt 1, not a new attempt.

## Attempted shortcut and exact failure

One might take a finite generating set for K, join a base vertex to its
translates, and take the K-orbit of that finite subtree. In a pro-p tree the
geodesic between two vertices need not be an ordinary finite edge-path.
Therefore the proposed fundamental domain is not proved finite. Likewise,
the profinite quotient K\T is not automatically an ordinary graph with a
liftable maximal subtree. The source papers explicitly distinguish these
points from abstract Bass–Serre theory. This route is blocked at the finite
subgroup decomposition, not at the elementary presentation calculation.

## Result carried forward

Finite-decomposition criterion and its two explicit bounds are proved above,
subject only to the standard continuous Mayer–Vietoris exact sequence for
finite proper graphs. No general coherence conclusion has been reached.
