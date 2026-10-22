# Attempt 5 — Power and invariant-partition methods for T_br

**Aim.** Reduce additional T_br inputs to kernel data by taking powers, then exploit finite invariant dyadic partitions. **Outcome:** exact reductions for elements with finite-order quotient, and a concrete counterexample to discarding the root information. Neither this nor the preceding attempts proves a terminating algorithm for the full target.

Let H=T_br. Suppose x,y have finite-order projections f=pi(x),g=pi(y) in T. Quotient conjugacy is an immediate necessary condition. In particular, their orders and oriented cyclic dynamics must agree. If their common quotient order is m, then x^m,y^m lie in K.

## 1. Powers give a necessary test, not an equivalence

H-conjugacy of x,y implies H-conjugacy of x^m,y^m. The converse can fail even when the powers are equal.

**Explicit witness.** At a three-leaf tree T put

    x=(T,sigma_1 sigma_2,T),
    y=(T,sigma_2 sigma_1,T).

Both braids induce cyclic permutations and hence define elements of T_br. With Delta=sigma_1 sigma_2 sigma_1=sigma_2 sigma_1 sigma_2, the braid relation gives

    (sigma_1 sigma_2)^3 = Delta^2
                       = (sigma_2 sigma_1)^3.

Thus x^3=y^3 in K. But their quotient maps cyclically move the three leaf intervals in opposite directions. One has rotation number 1/3 and the other 2/3, with the assignment depending only on the convention for stacking. They are not conjugate by any orientation-preserving circle homeomorphism, hence not by any element of T. Consequently x,y are not conjugate in T_br.

The rotation assertion can be checked without choosing slopes: pick a point in any leaf interval and follow its three-point orbit. A conjugacy preserving circular order cannot turn the successor order of this orbit into its reverse. The unequal widths of the three dyadic leaf intervals do not affect this argument. Both elements nevertheless are conjugate in B_3, since sigma_1 y sigma_1^(-1)=x. The permitted permutation of a conjugator matters again.

This example does not refute a method that also checks quotient conjugacy. It refutes only the stronger and unjustified replacement of root conjugacy by power conjugacy alone.

## 2. The exact residual root problem

Suppose an allowed d has been found with y^m=d x^m d^(-1). Set y'=d^(-1) y d and c=x^m=(y')^m.

**Proposition 5.1.** x and y are conjugate in H iff x and y' are conjugate inside C_H(c).

**Proof.** Conjugating by d already relates y and y'. If e x e^(-1)=y', raising to the mth power gives e c e^(-1)=c, so e lies in C_H(c). Conversely a conjugacy in that centralizer is certainly an H-conjugacy. ∎

The actual leftover is conjugacy of mth roots of c in its H-centralizer. Nothing in the ambient theorem or the fixed-strand braid theorem automatically supplies a terminating solution for that infinite braided-Thompson centralizer. Moreover, the first step would already require deciding the kernel-input problem from Attempt 3; we have only a positive semidecision for its general case.

## 3. A finite-order quotient admits a fixed-tree braid representative

**Lemma 5.2.** Given f in T with a verified finite order m, every finite dyadic cylinder partition has a computable finite dyadic refinement P invariant under f.

**Proof.** Refine the starting partition by the finitely many prefix-replacement domains of 1,f,...,f^(m-1). Each image f^i(I) of each resulting cylinder I is then a cylinder. For each i, f^i sends the partition to a cylinder partition. Take the common refinement of these m partitions. It is finite and again consists of cylinders: any two cylinders are nested or disjoint. Applying f permutes the collection of m partitions, since f^m=1, and hence permutes their common refinement. All operations involve finitely many binary words and are effective. ∎

Apply the lemma to a partition refining both the source and target trees in a diagram for x. Expand that diagram at its source to the invariant partition P. The target is the image f(P)=P, so x is represented as (S,b,S) at one tree S. Its braid b need not be pure; its permutation is cyclic. The same applies to y.

Thus finite-order quotient elements, though of infinite order themselves when nontrivial, can be treated as finite braids at invariant trees.

## 4. Exact extension of the finite-stage search

**Proposition 5.3.** For inputs with finite-order quotient, x,y are conjugate in T_br iff there are invariant refinements of their fixed-tree representatives with equal leaf count n at which the resulting braids are conjugate by a cyclically permuting braid.

**Proof.** A finite-stage witness gives a T_br-conjugator by joining its two trees, as in Attempt 3. For the converse, start with a T_br-conjugator h. Refine the x-side so it refines x's tree, h's source tree, and the pullback under pi(h) of y's tree. Use Lemma 5.2 to make this refinement f-invariant. Its image under pi(h) refines the y-side and is g-invariant, because pi(h) f = g pi(h). After these expansions, the equality h x h^(-1)=y is a fixed-strand braid equality. The conjugator's leaf permutation is cyclic because h belongs to T_br. ∎

For each n there are finitely many n-leaf refinements to test. Invariance is effectively checked by applying the finite prefix-replacement map to the leaf cylinders. The constrained braid-conjugacy test is exactly the finite permutation-centralizer test of Attempt 3; it works for nonpure braids too, since its transporter identity used no purity assumption.

This expands the positive semidecision from all kernel inputs to all inputs whose quotient has finite order. It does not produce a computable upper bound on the necessary invariant refinement. When the quotient has infinite order, no power lands in K; the power route then does not even reach the kernel case. In F_br, a power lands in K only when the original element already lies in K, because F is torsion-free.

## 5. Final assessment after five mathematical attempts

The surviving results are exact reductions, explicit nonconjugacy certificates, a complete finite classifier for linking-data orbits, and positive semidecision procedures. None proves general decidability or undecidability for F_br or T_br. The unresolved steps are effective termination for refined braid witnesses and the nonabelian twisted/centralizer orbit problems. The source's Question 48 therefore remains **unresolved by this work**. No negative finite experiment, literature-search absence, or failed approach is promoted to a theorem about undecidability.

**Substantive result:** a finite-order quotient invariant-partition construction, an exact constrained-braid characterization in that larger class, and a three-strand equal-powers witness showing why root information cannot be discarded.
