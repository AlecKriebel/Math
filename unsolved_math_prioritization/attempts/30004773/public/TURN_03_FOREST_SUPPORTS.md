# Attempt 3: solve all degrees for forests, test support-only extension

Let nu(H) denote the maximum size of a matching in a graph H. If Gamma is a forest, then

N_i(Gamma;q)=sum_{A subset E, nu((V,A))=i} (q-1)^|A|.          (4)

Consequently

ch(Gamma,i;q)=q^(n-2i) sum_{A subset E, nu((V,A))=i} (q-1)^|A|. (5)

These are integer polynomials and have nonnegative coefficients in q-1. Empty sums are zero; the empty support contributes N_0=1.

## Proof by leaf elimination

For any weighting y, let H be its support graph, keeping precisely those edges whose weights are nonzero. H is again a forest. If H has no edges, its alternating matrix has rank zero and nu(H)=0. Otherwise take a leaf u with neighbour v. After ordering u,v first, the matrix is

[ 0   a   0 ]
[-a   0   b ]
[ 0 -b^T  C ],                    a != 0.

Adding suitable multiples of the u row and the u column eliminates b and -b^T while leaving C unchanged. These are invertible congruence operations. Thus the rank is 2+rank(C).

There exists a maximum matching containing uv. If a maximum matching omits uv and matches v elsewhere, replace that edge by uv; u was unmatched. If v also is unmatched, adding uv would contradict maximality. Therefore nu(H)=1+nu(H-{u,v}). Induction yields rank B_Gamma(y)=2nu(H). Each support A has exactly (q-1)^|A| nonzero edge weightings, proving (4) and (5).

One may compute the sum by a finite support enumeration, or by a tree dynamic program. The formula itself is the symbolic answer for this entire family; no large numerical search is needed.

## Decisive failure outside forests

Take C4 with ordered vertices 1,2,3,4 and edges 12,14,23,34. Write their nonzero weights as a,b,c,d. The matrix determinant is (ad+bc)^2. For example over F_3, weights (1,1,1,1) have rank four, whereas (1,-1,1,1) have rank two. The support graph is the same C4, whose matching number is two, in both cases.

Thus maximum matching determines the largest possible rank but not the rank of each nonzero weighting on a graph with cycles. In particular the forest formula cannot simply be used for all graphs. This is a counterexample only to the attempted support-only extension, not to the source problem or to polynomiality of character counts. Both C4 rank counts are polynomial, as follows already from Attempt 2 and total mass.
