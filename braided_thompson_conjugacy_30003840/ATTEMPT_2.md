# Attempt 2 — A finite linking-pattern obstruction for the kernel

**Aim.** Keep enough of the pure-braid information to distinguish allowed conjugators, while removing dependence on arbitrary strand cloning. **Outcome:** a computable necessary condition, complete for the linking-data orbit; an explicit T_br obstruction; and an exact demonstration that the invariant cannot decide conjugacy by itself.

Let C={0,1}^N be the Cantor set in lexicographic order. A finite rooted binary tree T partitions C into its ordered leaf cylinders I_1,...,I_n. Write k=(T,p,T) in K, with p in PB_n.

## 1. The invariant before taking orbits

Define a symmetric function lambda_k:C x C -> Z by

    lambda_k(x,y) = L_ij(p) if x is in I_i, y is in I_j and i != j;
    lambda_k(x,y) = 0 if x,y lie in the same leaf cylinder.

In particular its value on the diagonal is zero. This is a locally constant, finite-step function.

**Lemma 2.1.** It is independent of the chosen representative of k; lambda is a homomorphism from K into the additive group of such functions. For h in V_br and f=pi(h),

    lambda_(h k h^(-1))(x,y)
       = lambda_k(f^(-1)(x), f^(-1)(y)).                 (2.1)

**Proof.** Cloning strand i replaces its cylinder by two child cylinders. The two parallel clones have mutual linking zero and each has the old strand's linking with every other strand. Thus all values of the function stay unchanged. Any two diagrams for k have a common expansion, so independence follows. After a common expansion, multiplication of elements of K is multiplication of pure braids at the same tree. Pairwise linking is additive there. For (2.1), refine the diagrams so h matches a tree carrying k. In the finite braid conjugation the pairwise-linking homomorphism is relabeled by h's permutation. Changes of its endpoint trees merely implement the prefix-replacement homeomorphism f. Independence under further cloning gives the asserted formula on C. ∎

For orientation, this is the direct-limit version of pure-braid abelianization. It discards nonabelian braiding. No claim of a new literature theorem is needed for the elementary construction and proof above.

## 2. A terminating classification of its F and T orbits

The function is encoded by the n x n symmetric integer matrix M of pairwise linking, with zero diagonal. Strand lengths and tree shape are irrelevant for the orbit problem, but linear/cyclic order is not.

Call two rows twins if they are equal as full n-entry vectors. Such rows necessarily have zero mutual entry. Replace each maximal **consecutive run** of twin rows by one row and its matching column. For the F orbit retain the resulting linear matrix, called R_F(M). For the T orbit combine a run across the last/first boundary too and identify results up to simultaneous cyclic rotation of rows and columns, called R_T(M). If every row is zero, the result is the one-by-one zero matrix.

**Proposition 2.2.** For finite-step linking functions lambda and mu:

- they are carried to each other by an element of F iff their R_F matrices agree;
- they are carried to each other by an element of T iff their R_T matrices agree.

**Proof, necessity.** The intrinsic equivalence relation on points is

    x ~ y iff lambda(x,z)=lambda(y,z) for every z in C.

Its classes are exactly unions of leaf cylinders with equal matrix rows. Maximal linearly convex pieces of these classes correspond to consecutive twin runs. For the circular version use circularly convex pieces. An order-preserving, respectively cyclic-order-preserving, bijection preserves these pieces and the values between them. Hence it preserves the reduced matrix with the stated allowed rotations. Deleting duplicate rows does not create new equality: every deleted column has an identical representative among the retained columns.

**Proof, sufficiency.** Suppose the reduced matrices match. Each corresponding run is a nonempty finite union of consecutive cylinders. If a source run contains r cylinders and its target run s cylinders, subdivide cylinders inside them until both have the same number N >= max(r,s). This is always possible since one binary subdivision increases the number by one. Do this independently for every corresponding pair of runs. Pairing all refined leaves in order defines an element of F carrying lambda to mu. In the cyclic case choose boundaries between runs as the starting points, refine in the same way, and pair the leaves cyclically; the resulting tree-pair permutation is a cyclic rotation and defines an element of T. A run that crosses the original cut is handled by the cyclic enumeration. The identically zero case is immediate. ∎

The procedure terminates on finite matrices. Together with (2.1), unequal reduced matrices certify nonconjugacy in the appropriate braided subgroup for elements of K. Equal matrices mean only that the **linking patterns** can match.

## 3. T_br does not inherit ambient conjugacy either

Choose a four-leaf tree T, let p=sigma_1^2 sigma_3^2 and h=sigma_2 in B_4, and put q=h p h^(-1). These give elements of K conjugate in V_br. The linking pattern of p has the edges {1,2},{3,4}; that of q has the edges {1,3},{2,4}, all with label 1 and all other pairs zero.

Every row is distinct, so neither matrix collapses. No cyclic rotation takes the first pattern to the second: its edges join adjacent vertices of the cyclic four-point order, whereas those of the second join opposite vertices. Proposition 2.2 therefore proves that the two kernel elements are **not conjugate in T_br**. This obstruction survives arbitrary cloning and arbitrary T_br conjugators; it is not merely a fixed-four-strand observation.

Equivalently, the second pattern has four cyclically ordered points whose nonzero linking pairs alternate, while the first does not. The finite-matrix proof avoids any ambiguity introduced by repeated points within a cylinder.

## 4. Why the invariant still cannot finish the problem

In PB_3 set c=[sigma_1^2,sigma_2^2], with [x,y]=xyx^(-1)y^(-1). Since linking is additive, lambda_c=0=lambda_1. But c is not the identity. A direct check uses the representation of B_3 into SL_2(Z) given by

    sigma_1 -> U = [[1,1],[0,1]],
    sigma_2 -> L = [[1,0],[-1,1]].

The matrices satisfy ULU=LUL. The image U^2 L^2 U^(-2) L^(-2) is not the identity (the exact entries are reproduced by verify.py). Thus c is a nontrivial braid. The fixed-tree PB_3 subgroup injects in K; alternatively, each cloning map is injective because deleting one clone recovers the original pure braid. Therefore (T,c,T) is nontrivial in K and cannot be conjugate to the identity in any group.

This pair passes both reduced-linking tests and has identical quotient in F or T, yet is nonconjugate. The attempted replacement of conjugacy by the finite linking-pattern orbit is therefore definitively incomplete.

**Substantive result:** a finite algorithm for the abelian linking-data orbit, explicit ambient-conjugate/T_br-nonconjugate elements, and an exact nonabelian failure witness for the algorithm's completeness.
