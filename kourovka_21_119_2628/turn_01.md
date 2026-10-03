# Turn 1/5: normalize the witnesses and test finite-index flexibility

## Attempt

Try to turn the many virtual maps in the question into a coherent nested family and exploit common finiteness constraints. This is a proof attempt, not a literature-review turn.

Write F_m for the existence of a K(H,1) with finite m-skeleton; F_∞ means F_m for every m. We use the standard finite-index invariance of F_m, and that an extension of two F_m groups is F_m. For an extension by Z the latter also follows by constructing a mapping torus of a classifying-space self-homotopy equivalence. Neither assertion says that arbitrary subgroups inherit F_m.

## 1. The ambient group necessarily has type F_∞

Suppose the requested witnesses exist. Fix m. The exact sequence

1→K_m→G_m→f_m(G_m)→1

has F_m kernel. Its quotient is trivial or infinite cyclic, hence F_∞. Therefore G_m is F_m, and finite-index invariance implies G is F_m. Since m was arbitrary, G is F_∞.

This also rules out zero characters. If f_n=0 then K_n=G_n, which is F_∞ because G is F_∞, contradicting the required failure of F_{n+1}. Thus each image is d_n Z with d_n>0. Dividing f_n by d_n gives an epimorphism onto Z with exactly the same kernel. Allowing homomorphisms rather than epimorphisms does not enlarge the existence problem.

## 2. The family may be chosen nested and normal

Let core_G(H)=∩_{g∈G}gHg^{-1}. For a finite-index H this is a finite intersection, is normal, and has finite index in G. Define

C_n=∩_{i=1}^n core_G(G_i).

Then C_1≥C_2≥⋯ are finite-index normal subgroups of G and C_n≤G_n. The restricted character f_n|_{C_n} has nonzero image, because a finite-index subgroup has finite-index image in f_n(G_n). Its kernel is K_n∩C_n. The index [K_n:K_n∩C_n] is at most [G_n:C_n], hence finite. Therefore K_n∩C_n has exactly the same F_m properties as K_n. Rescaling the restricted image gives a surjection C_n→Z with exact finiteness length n.

So nested normal witnesses are equivalent to the original problem. This is not a construction: nothing shows that characters for different n are compatible, or that one extends another.

## 3. The obstruction belongs to a commensurability class

For a group H define its virtual fiber spectrum to be the set of n≥0 for which some finite-index J≤H has a nonzero map J→Z whose kernel is F_n and not F_{n+1}. If L≤H has finite index, every witness J intersects L in finite index; the preceding restriction argument transfers the same exact finiteness length to J∩L. Conversely a finite-index subgroup of L is finite index in H. Thus H and L have the same spectrum, and isomorphic finite-index subgroups give the same spectrum as well.

This prevents a proposed solution from changing the answer merely by passing to a finite cover. In particular, taking successive finite-index subgroups of one fixed fiber does not improve that fiber's finiteness length.

## 4. Virtual first Betti number one cannot work

Assume every finite-index subgroup H≤G has dim_Q Hom(H,Q)≤1. Take any two virtual nonzero integral characters f_i on G_i and f_j on G_j. On L=G_i∩G_j both restrictions are nonzero, so are proportional over Q. Their kernels in L are consequently identical. Each is finite index in the original corresponding kernel. Finite-index invariance forces those two original kernels to have identical finiteness properties.

Therefore such a G has at most one finite value in its virtual fiber spectrum. A hypothetical solution must have a finite-index subgroup of rational first Betti number at least two. This does not prove that virtual first Betti numbers must be unbounded: a two-dimensional character space already contains infinitely many rational directions, and no uniform bound on their finiteness lengths has been established here.

## Outcome and exact gap

Necessary conditions proved: G is F_∞, all maps can be surjective, witnesses can be nested normal finite-index subgroups, the spectrum is commensurability invariant, and virtual first Betti number one is excluded. The original existence question remains unresolved. The next attempt tests the familiar product-of-free-groups construction and its behavior when the number of factors is frozen.
