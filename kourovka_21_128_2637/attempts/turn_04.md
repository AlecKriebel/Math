# Turn 4 of 5: full finite quotients versus virtual finite quotients

## Strategy and outcome
Try to promote the very different smallest finite quotients to a commensurability obstruction. The full groups are indeed separated, but the proposed virtual obstruction fails decisively: both groups virtually surject onto every finite group. Both also have infinite virtual first Betti number. The proof below gives explicit general constructions, rather than simply warning that an invariant may change.

## An elementary full-group separation
G_F surjects onto S3 by sending (s1,s2,s3,s4) to ((01),(12),1,1). The length-three relation on s1,s2 is satisfied, the length-four relation with s3=1 is automatic, and all other relations hold. The central word maps to ((01)(12))^6=1.

Every homomorphism G_H->S3 has cyclic image. All generators in the 5-3-3 path are conjugate, as follows from each odd braid relation. Their images have the same cycle type. If they are 3-cycles, they belong to the single cyclic subgroup A3, and odd braid relations force equality. If they are transpositions, two distinct ones have product of order 3 and cannot satisfy the length-five braid relation; hence the first two images agree. The first and third images commute because those generators are nonadjacent. Commuting transpositions agree, so the third image agrees. The same argument with the first and fourth images gives equality of all four. The identity case is trivial.

The exact enumeration checks/small_quotients.py tests all 6^4 generator assignments for each central quotient and independently checks all seven relators, including the central word. It records the image-order distributions and a surjection witness. It does not assert any theorem about larger finite targets.

This is consistent with two newly located September 2026 preprints: Gavazzi–Haladjian–Paris (arXiv:2609.25940v1) and Hughes–Ng–Ragosta–Scherich–Verberne (arXiv:2609.27171v1). The latter's Theorem A gives smallest nonabelian quotients S3 and W(H4)/Z(W(H4)), of orders 6 and 7200. Their rigidity results concern isomorphic full profinite completions within specified classes. They do not say that arbitrary isomorphic open subgroups force the parent Artin groups to be isomorphic or noncommensurable. The first preprint allows a broader comparison class for its irreducible input; that distinction likewise does not produce commensurability rigidity.

## A quotient F2 of each pure central quotient
Each of the two real reflection arrangements contains a rank-two localization of type A2: take the two terminal generators joined by a length-three edge. The three hyperplanes through the corresponding codimension-two flat form a subarrangement B with complement

M(B) homeomorphic to (C^2 minus three central lines) x C^2.

The inclusion M(A)->M(B) is surjective on pi1. To see this, take a based loop in M(B). Perturb it slightly, fixing the basepoint, so that it avoids each of the finitely many additional complex hyperplanes in A. Such hyperplanes have real codimension two, while the loop has real dimension one. The perturbed loop lies in M(A) and represents the original pi1 class.

The scalar C* loop maps to the scalar C* loop under inclusion. Dividing the induced epimorphism by those central cyclic subgroups yields

Q_F ->> F2 and Q_H ->> F2.

Here the target is pi1(P^1 minus three points). The projective complement of B has a contractible affine-space factor, which does not change its fundamental group. This is only a surjection, not a claim that the ambient groups split as free products or that the map is an injection.

## Consequences at finite index
For every d>=1, F2 has an index-d subgroup F_{d+1}. Pull it back along either epimorphism above. The pullback has index d in Q_X and surjects onto F_{d+1}. Consequently both groups have finite-index subgroups with b1 at least d+1, proving virtual b1 is infinite.

Given any finite group J, choose a finite generating set of size r, enlarge r to at least two, and take an index-(r-1) subgroup F_r of F2. Its pullback in Q_X has finite index and surjects onto F_r and then onto J. Thus both A[F4] and A[H4], as well as their central quotients, virtually surject onto every finite group.

Therefore a strategy using only whether a finite group occurs somewhere as a quotient of a finite-index subgroup cannot distinguish this pair. This does not imply that the complete profinite systems of all finite-index subgroups agree. It only kills this coarse existential virtual-quotient test. The exact open-subgroup compatibility problem remains untouched.
