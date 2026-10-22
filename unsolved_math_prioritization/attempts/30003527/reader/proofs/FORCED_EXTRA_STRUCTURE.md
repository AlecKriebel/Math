# What non-isolation actually forces

Problem 30003527, shared substantive pass 2, 13 October 2026 UTC. This is a short consequence and scope clarification for SATELLITE_ISOLATION_OBSTRUCTION.md. It does not establish a movable invariant enlargement.

Let X=Σ∪⋃C_n be the explicit pass-1 compactum, with winding(C_n)=3·2ⁿ in the fixed open solid torus O. Suppose a continuous full flow makes X invariant. The obstruction theorem says X is not isolated.

## 1. Complete extra trajectories approach X

For every compact neighborhood N of X and every open neighborhood V of X there exists

p∈(V∩Inv(N))\X.

Indeed, if some V failed this statement, choose a compact neighborhood N' of X contained in V∩int N. Then Inv(N')⊂Inv(N)∩V=X, while invariance of X gives X⊂Inv(N'). Hence Inv(N')=X⊂int N', contradicting non-isolation.

Thus a full trajectory outside X remains in N and passes arbitrarily close to X. Because X is invariant, the trajectory through p never meets X. Its closure may meet X. Taking N⊂U gives complete extra trajectories confined to any prescribed neighborhood U of X.

This is stronger than the existence of nearby points whose trajectories may leave U. It still does not identify the extra trajectories as periodic, nor determine the topology of their closures.

## 2. What an isolated enlargement must change

Suppose K is an isolated invariant compactum with X⊂K⊂O. The finite-winding theorem implies that only finitely many of the circles C_n can remain clopen components of K. Their nonzero winding magnitudes are all distinct, so an infinite such subfamily is impossible.

Consequently, for all but finitely n, every neighborhood of C_n contains a point of K\C_n. Otherwise C_n would be open as well as closed in K; since it is connected, it would be a clopen component. When K=Inv(N), those points lie on full trajectories confined to N. This may mean that C_n lies in a larger connected component of K or that other components accumulate on it. Neither alternative by itself supplies a movable enlargement.

## 3. A small extension with the same proof

The finite-winding theorem does not actually require that each clopen component C_n be homeomorphic to a circle. It holds for pairwise disjoint clopen connected compacta A_n⊂K with Ȟ¹(A_n;Z)≅Z, defining |w_n| by restriction of u to a generator of this cyclic group. The proof uses only Ȟ⁰(A_n)=Ȟ¹(A_n)=Z, the stable clopen decomposition, and Čech continuity; the entry traces again have annular neighborhoods and carry the same degree.

In particular, replacing each satellite circle by a compact clopen component obtained by attaching finitely many contractible whiskers, with the same cyclic first cohomology and ambient degree, does not evade the obstruction. This does not cover arbitrary infinite-cohomology components or non-clopen components.

## 4. Exact remaining inference

To settle the original target affirmatively from the forced extra trajectories, one would still need to construct a compact invariant B inside the prescribed U and verify the full neighborhood-homotopy movability quantifiers. To use the pass-1 compatible-core lemma, one would need invariant circles that are actual cores of suitable defining tori (or another explicitly sufficient homotopy property), confinement of their whole orbits to U, and compactness of the resulting union.

None of those topological properties follows merely from the extra-trajectory conclusions above. The finite-entry-surface argument does not classify the additional invariant structure and does not prove it contains compatible core circles. The full flow problem therefore remains unresolved.
