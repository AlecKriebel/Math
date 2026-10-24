# Relatively isolated infinite-order conjugacy classes: independent local audit

Checkpoint: 2026-10-24 17:42 UTC. Full Problem 21.136 progress estimate: **15%**. Status: rigorous subclass obstructions; arbitrary profinite case remains unresolved. No originality or publication claim.

## Exact local hypothesis

Say (G,x,U) has local isolation if G is profinite, x has infinite order, U is a clopen neighbourhood of x, and every infinite-order y in U is G-conjugate to x. No global bound on the number of infinite-order classes is assumed. In particular a counterexample to local impossibility could have continuum many classes elsewhere and need not refute the original Kourovka question.

This investigation did not read the separate construction agent's new work. An independent child first obtained a metabelian proof, then a general abelian-kernel mechanism. The parent independently supplied the simpler centralizer repair below. Both child and this reviewer checked that repair.

## 1. Elementary consequences valid in arbitrary profinite groups

### Infinite-order conjugacy classes have empty interior

If x^G contained an open coset Nx, with N open normal, then for every open normal M≤N the finite conjugacy class of xM in G/M would contain Nx/M. Thus

    |C_(G/M)(xM)| ≤ |G:N|.

The order of xM is bounded by this number. Residual finiteness then makes x finite order. Contradiction. Conjugacy classes are closed because they are compact images of G, so an infinite-order class is nowhere dense.

Consequently local isolation forces U minus x^G to be an open dense set of torsion elements. Moreover torsion orders are unbounded in every neighbourhood of x: if a smaller neighbourhood V had all finite-order elements killed by one integer m, the closed set {g:g^m=1} would contain the dense torsion subset of V and hence x, a contradiction.

This rules out local isolation whenever torsion orders are locally bounded near x. In particular it rules it out if G has an open torsion-free subgroup. Pass to its normal core N; every finite cyclic subgroup injects into finite G/N, so all torsion orders divide |G/N|. This includes the usual groups for which an independent structural result supplies such an open subgroup.

### Quotient descent when x survives with infinite order

For a continuous epimorphism π:G→B, if π(x) has infinite order, then local isolation descends to (B,π(x),π(U)). The quotient map is open and closed, so π(U) is clopen. Every infinite-order b in π(U) has a lift y in U, which is necessarily infinite order and hence conjugate to x. Its image is conjugate to π(x).

### The order of x has only finitely many prime divisors

Let C=closure(<x>) and decompose this procyclic group into its Sylow factors C_p. If infinitely many C_p are nontrivial, any neighbourhood of x in C leaves some C_p entirely unrestricted. Replace only that p-coordinate of x by 1. The resulting y is still in the neighbourhood and has infinite order because infinitely many other nontrivial prime factors remain. It is not conjugate to x, since its procyclic order has different p-part. This contradicts local isolation. Hence the supernatural order of x has finite prime support. At least one factor is then Z_p.

## 2. Abelian-kernel lemma

**Lemma.** If (G,x,U) has local isolation and A is a closed abelian normal subgroup of G, then the image of x in G/A has infinite order.

**Proof.** Write π:G→B=G/A. Suppose b=π(x) has finite order r. Every element of the clopen set π(U) is torsion: an infinite-order element there would have an infinite-order lift y in U, whose conjugacy to x would force its image to be conjugate to the finite-order b.

We first show that C=C_B(b) is torsion. Choose an open subgroup K≤C small enough that bK⊂π(U). This K is open in C; no claim that it is open in B is needed. For k∈K, both b and bk have finite order and commute, so k has finite order. Thus K is torsion. Every c∈C has a positive power in the finite-index subgroup K, and consequently c itself is torsion. Normality of K is not required.

Choose an integer n>1 with n≡1 modulo r and x^n∈U. Such an n exists: choose open normal L in G with xL⊂U, and take n−1 divisible by both r and the finite order of xL. The element x^n has infinite order, so there is g∈G with x^g=x^n. On passing to B, we get b^(πg)=b^n=b, so πg lies in C and therefore has finite order m. Hence g^m∈A.

Now a=x^r belongs to A and has infinite order. We have a^g=a^n, and iterating gives a^(g^m)=a^(n^m). But g^m and a both lie in the abelian group A, so a^(g^m)=a. This forces a^(n^m−1)=1, a contradiction. [End proof.]

### Audited failure points

* π(U) is clopen even when U is not saturated, because compact images are closed and quotient maps of compact groups are open.
* The selected K is a subgroup of the centralizer, so commutativity needed for the product of torsion elements is justified.
* A finite-index torsion subgroup makes the whole group torsion even if it is not normal: use the action of the cyclic subgroup <c> on its finitely many cosets to obtain a positive power in K.
* The choice of n imposes the finite congruence n≡1 mod r in addition to the ambient neighbourhood condition.
* The conjugator g need not be small; its image is torsion because it centralizes b, not because of an unsupported general assertion about the quotient B.
* The final contradiction uses the abelian kernel A. The same argument does not work with an arbitrary nonabelian kernel.

## 3. Consequence: no local isolation in virtually soluble profinite groups

**Theorem.** No virtually soluble profinite group has a relatively isolated infinite-order conjugacy class.

**Proof.** Choose an open normal soluble subgroup N of finite derived length d. Its closed derived series is characteristic in N and hence normal in G. The last nontrivial term A=N^(d−1) is closed abelian normal in G. By the lemma, an allegedly isolated infinite-order x has infinite-order image in G/A; by quotient descent, that image is again locally isolated. The quotient has an open normal soluble subgroup of smaller derived length. Repeating eventually gives an isolated infinite-order element in the finite group G/N, impossible. The case N=1 is already finite. [End proof.]

This theorem allows finite nonsoluble quotients G/N; the soluble subgroup N, rather than G itself, is used in the finite induction. It applies to arbitrary cardinality or rank and needs no finite-generation hypothesis. It is a restricted mathematical deduction only; no priority assessment has established novelty.

## 4. Why the general question remains open in this audit

The abelian-kernel lemma is an extension principle, not an argument through an infinite inverse limit of soluble quotients. Pro-p groups are inverse limits of finite soluble groups whose derived lengths and element orders can grow without bound. A finite-order image of x in each finite quotient does not imply a uniform order bound on x. The proof must not replace finite derived length by prosolubility.

The alternative small-conjugator route yields relations resembling x^(x^g)=x^k after choosing a normalizer element inducing a power automorphism. A single such relation has not been shown impossible. Generalized Higman pro-p constructions are a control against making that unsupported inference; the abelian-kernel proof above uses the full neighbourhood hypothesis and centralizer torsion instead.

No actual profinite group with a locally isolated infinite-order class has been constructed here, and no proof excludes such a class in arbitrary profinite groups. The remaining case includes pro-p groups of unbounded derived length and no suitable finite abelian-kernel reduction.

## 5. Subsequent extension: abstract locally nilpotent kernels

Checkpoint: 2026-10-24 17:42 UTC. Full-problem progress estimate remains **15%**; the subclass obstruction is stronger, but the arbitrary pro-p gap persists.

The abelian-kernel lemma extends to a closed normal subgroup A that is abstract locally nilpotent. Retain the quotient-centralizer argument exactly, obtaining a=x^r of infinite order and h=g^m in A with a^h=a^k, where k=n^m>1. The finitely generated abstract subgroup <a,h> is nilpotent, of some finite class c. With right conjugation and [u,v]=u^(-1)u^v, induction gives

    [a,_j h] = a^((k−1)^j).

The c-fold iterated commutator has weight c+1 and is therefore trivial. This forces the infinite-order element a to satisfy a^((k−1)^c)=1, contradiction. No uniform bound on c is required. This argument uses abstract local nilpotence; being pro-p or pronilpotent does not supply that hypothesis.

A closed torsion kernel also preserves the infinite order of x directly: if xA had finite order r, then x^r in A would have finite order and x itself would be torsion. Combining quotient descent with these two kernel rules excludes local isolation whenever G admits a finite series of closed G-normal subgroups whose successive factors are torsion or abstract locally nilpotent. Finite quotients are included as torsion factors. This is still only a restricted theorem and carries no novelty certification.

## 6. Restricting conjugators to an open subgroup

If local isolation holds and H is an open subgroup containing x, it holds after shrinking the neighbourhood with H-conjugacy in place of G-conjugacy. Indeed x^G is a finite union of H-orbits, each compact and hence closed. Distinct H-orbits are disjoint. Delete the finitely many H-orbits other than x^H from a sufficiently small clopen neighbourhood of x, and intersect with H. All remaining infinite-order elements are H-conjugate to x.

Consequently the normalizer of C=closure(<x>) cannot be open in G. If it were, restrict to H=N_G(C) as above. Its closed normal abelian subgroup C contains x, so the abelian-kernel lemma would force xC to have infinite order in H/C, while xC=1. Contradiction. This deduction does not require any additional assertion about the automorphism group of C.
