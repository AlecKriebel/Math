# Turn 2 of 5: exact first homology of the two torsion-free cyclic covers

## Strategy and result
Compute rational H_1 of the explicit comparison groups K_F and K_H from turn 1. The exact results are b1(K_F)=3 and b1(K_H)=0. This proves they are not isomorphic. It does not prove they are not commensurable. Crucially, every finite-index subgroup of K_F still has b1 at least 3, so any proposed common subgroup must be a cover of K_H with b1 at least 3. This supplies a usable rejection test for explicit common-cover candidates.

## Presentations and cover model
Use the six pairwise Artin relations for the 3-4-3 or 5-3-3 diagram, taking m_ij=2 at nonedges. Add the central relation

(s1 s2 s3 s4)^6=1 for G_F,
(s1 s2 s3 s4)^15=1 for G_H.

These are the central quotients from turn 1, using the verified central generators. For an n-sheet cyclic cover, label vertices by j in Z/n. The edge for generator si at vertex j goes to j+w_i. Use (n,w)=(12,(1,1,0,0)) for K_F and (60,(1,1,1,1)) for K_H.

For each relator and each initial vertex, lift the relator, recording signed traversals of the 4n oriented generator edges. This is the cellular boundary d2. The edge boundary gives d1. Since the weights generate Z/n, the graph is connected and rank(d1)=n-1. H1 of a presentation complex equals H1 of its fundamental group, so this calculation does not require the presentation complex to be aspherical.

Exact rational row reduction in checks/cover_homology.py gives:

- K_F: C0 dimension 12; C1 dimension 48; C2 dimension 84; rank(d1)=11; rank(d2)=34; hence b1=48-11-34=3.
- K_H: C0 dimension 60; C1 dimension 240; C2 dimension 420; rank(d1)=59; rank(d2)=181; hence b1=240-59-181=0.

The script checks that all relators lift closed and that d1*d2=0. It uses exact QQ arithmetic with SymPy 1.14.0, never floating-point ranks. Stored results are in checks/cover_homology_results.json. The computation proves only rational first homology, not integral H1, perfectness, or higher homology.

## Transfer obstruction
For a subgroup U of finite index d in K_F, restriction in degree-one rational cohomology is injective: corestriction followed by restriction in the appropriate order gives d times the identity on H^1(K_F;Q). Thus b1(U)>=3. It follows that a subgroup V of K_H with b1(V)<3 cannot be isomorphic to any finite-index subgroup of K_F, regardless of its index.

Turn 1 fixes the candidate relative indices to (42s,5s). The smallest Euler-compatible possibility has V of index 5 in K_H. The next attempt constructs a natural index-five V and computes its first homology. A failed explicit V does not exclude all index-five V, much less all s.

## Why the initial difference is insufficient
Rational first Betti number is not invariant under commensurability. Even F2 has an index-two subgroup F3. More pertinently, the pure central quotient Q_H has b1=59, and Q_H intersect K_H has finite index in both; transfer gives b1(Q_H intersect K_H)>=59. Thus K_H itself already has finite covers with positive, indeed large, first Betti number despite b1(K_H)=0. No hereditary vanishing claim is made.
