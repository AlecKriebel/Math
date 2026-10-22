# Attempt 4: determinant rigidity for derived words

Date: 2026-10-03 UTC. Fourth substantive proof attempt.

## Targeted family and a new mechanism

Take w=delta_k, the k-th derived word, with k>=2. Use Attempt 1 to quotient the finite torsion kernel T of H=G^{(k)}, so H is a finitely generated free abelian normal subgroup and G acts on H through a finite matrix group. We use a repeated-commutator family that consists of actual delta_k-values, together with determinant one, to constrain this action.

## Lemma: finite-order determinant-one matrices

Let M be a finite-order rational matrix with det(M)=1. If rank((M-I)^j)<=1 for some positive integer j, then M=I.

Proof. In characteristic zero a finite-order matrix is semisimple: its minimal polynomial divides t^e-1, which has no repeated roots. Therefore rank((M-I)^j)=rank(M-I). If this rank is one, the nonfixed complement is a one-dimensional rational invariant space. On it M acts by a nonidentity rational root of unity, necessarily -1. All other eigenvalues are 1, so det(M)=-1, a contradiction. Rank zero gives M=I.

The finite-order hypothesis is indispensable: the unipotent matrix [[1,1],[0,1]] has determinant one and rank(M-I)=1 without being the identity.

## Constructing actual derived values

Fix a delta_{k-1}-value v in G. For h in H set c_0=h and recursively c_j=[c_{j-1},v], 1<=j<=k. Every delta_{k-1}-value is also a delta_i-value for i<=k-1, by substituting deeper derived values into the leaves of the shallower word. Therefore induction gives that c_j is a delta_j-value: c_{j-1} is a delta_{j-1}-value, and so is v, and the two sets of variables in delta_j are independent.

In particular c_k is an actual delta_k-value. Let M be conjugation by v on H, using h^v=v^{-1}hv. Since H is abelian, [h,v]=(M-I)h in additive notation, and

  c_k = (M-I)^k h.

As h varies, these values fill the subgroup (M-I)^k H. Its image in V=H tensor Q has dimension at most one. To see this directly, a rank-two subgroup contains independent vectors a,b and the elements a+n b occupy infinitely many rational lines, whereas a finite cyclic cover permits only finitely many.

Since k>=2, v is itself a commutator. The determinant of its action on H is therefore 1: determinant composed with the conjugation representation is an abelian character, and kills every commutator. The action is finite by Attempt 1. The matrix lemma forces M=I.

Thus every delta_{k-1}-value centralizes H, and those values generate G^{(k-1)}. We have proved

  [G^{(k)},G^{(k-1)}]=1

in the quotient by T. Since (G^{(k-1)})'=G^{(k)}, the subgroup G^{(k-1)} has nilpotency class at most two there. In the original group its third lower-central subgroup is contained in the finite normal subgroup T. This is a genuine structural reduction for all ambient groups satisfying the cyclic-cover hypothesis for delta_k.

## Complete special case: virtually abelian ambient groups

Suppose G is finitely generated and virtually abelian. Choose an abelian normal subgroup A of finite index. It can be chosen torsion-free by first choosing a finitely generated abelian finite-index subgroup, taking a finite-index torsion-free subgroup, and then its core.

Repeat the construction above with h in A, without quotienting H. Conjugation by v on A has finite order since A is abelian and has finite index in G. It has determinant one since v is a commutator. The image (M-I)^k A consists of delta_k-values and hence has rank at most one. Therefore all delta_{k-1}-values centralize A.

Put K=G^{(k-1)}. The group K centralizes A, so K intersect A lies in Z(K); and K/(K intersect A) embeds in the finite group G/A. Schur's theorem gives K'=G^{(k)} finite.

Consequently, for delta_k with k>=2, a finitely generated virtually abelian ambient group satisfying the hypothesis has a finite verbal subgroup, stronger than finite-by-cyclic. Finite groups are included. This is not a result for every solvable ambient group.

## Why the general derived-word case is still not finished

In the general reduction K=G^{(k-1)} is class-two nilpotent, but the cyclic cover is known only for commutators [a,b] where a and b are individual delta_{k-1}-values. It is not given for all a,b in K. Replacing individual word values by arbitrary products of them changes the hypothesis.

The bilinear commutator map of the class-two group K does allow products of these values, but sums of two covered directions need not themselves be covered by the original assumption. Applying Attempt 2 to K would therefore require a new argument that its whole commutator set has a finite cyclic cover. That unproved step would essentially reinstall the rank-collapse difficulty. We do not make it.

## Outcome

Proved a finite-by-class-two reduction one derived level above the target, and a complete finite-verbal-subgroup theorem for derived words of height at least two in finitely generated virtually abelian groups. General delta_k and arbitrary multilinear words remain unresolved.

Best-guess completion: 30%, heuristic. No novelty or full-resolution claim.
