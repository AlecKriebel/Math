# Independent locality audit for Problem 21.136

Checkpoint: 2026-10-24 17:24 UTC. Estimated completion toward the full research problem: **8%**. Status: partial obstruction and positive subclasses; no resolution or publication claim.

This audit was begun independently from the cached primary source `../sources/wilson2023.txt`, without reading the parent or other approach notes. Source: J. S. Wilson, *Profinite groups with few conjugacy classes of elements of infinite order*, Archiv der Mathematik 120 (2023), 557–563, DOI https://doi.org/10.1007/s00013-023-01851-4. Definitions below concern arbitrary pro-p groups and are not interchangeable with the actual few-conjugacy-classes hypothesis.

## 1. Two hypotheses that must remain distinct

Write T(G) for the set of finite-order elements. Consider:

* W: T(G) is dense and at least one open normal coset has bounded exponent.
* P: every nonempty open coset contains an open subcoset of bounded exponent.

Wilson Theorem C says that a **topologically finitely generated** pro-p group satisfying W is finite. Wilson Corollary 2.3 supplies P under the relevant few-conjugacy-classes hypothesis. P implies W, but W is substantially weaker.

P is equivalent to density of the interior of T(G). The forward implication is immediate. Conversely, if int(T(G)) is dense, any nonempty open set contains a compact open coset C consisting of torsion elements. The closed sets {x in C : x^(p^n)=1}, n≥0, cover C. Baire gives one such set with nonempty relative interior; since C is open, this contains an ambient open coset of bounded exponent. This is a deduction, not a literature priority claim.

P passes to open subgroups and continuous quotients. For quotients use that a continuous surjective homomorphism of compact groups is open; the image of an open bounded-exponent coset is an open bounded-exponent coset. Inheritance by arbitrary closed subgroups is **not proved**: a bounded-exponent subcoset selected in an ambient neighbourhood can miss the chosen closed subgroup entirely.

## 2. Explicit counterexample to removing finite generation from W, for every prime

Fix a prime p. For n≥1 let

    V_n = { (x_0,...,x_(p-1)) in (Z/p^n Z)^p : sum_i x_i=0 }

as an additive finite abelian p-group. Let σ rotate the p coordinates. Put A=∏_(n≥1) V_n with the product topology, and let

    G = A ⋊ <t>,  t^p=1,  t a t^(-1)=σ(a).

All assertions have direct proofs:

1. G is pro-p: it is the inverse limit of (∏_(n≤N)V_n)⋊C_p, finite p-groups.
2. The subgroup D=(⊕ V_n)⋊C_p is locally finite and dense in G. Any finite subset of D lies in one of the displayed finite subgroups.
3. Consequently T(G) is dense.
4. On V_n, the operator 1+σ+...+σ^(p-1) is zero: each output coordinate is the sum of the input coordinates. For j=1,...,p−1, σ^j has the same norm operator. Thus (a t^j)^p=1 for every a in A. In particular the open normal coset At has exponent p.
5. Let a_n=(1,−1,0,...,0) in V_n, and a=(a_n)_n. Each a_n has order p^n, so a has infinite order.

Thus G satisfies W and is neither torsion nor locally finite. For p=2 this is simply (∏ C_(2^n))⋊C_2 with inversion. This is a control construction, not a claimed original result.

This G does **not** satisfy P. Any nonempty open subset of A leaves an unrestricted product of all V_n beyond finitely many coordinates. It therefore contains an element of infinite order, by placing a_n in every sufficiently large coordinate. Thus no nonempty open subset of A is contained in T(G); int(T(G)) misses the open subgroup A.

The example also does not refute the original few-conjugacy-classes question. For each infinite subset S of the positive integers, form a^S with n-th coordinate a_n when n∈S and 0 otherwise. It has infinite order. Conjugacy in G preserves its support because A is abelian and conjugation by t only rotates the entries within each V_n. Distinct S therefore give distinct conjugacy classes, and there are 2^aleph_0 such S.

## 3. Exact Lie locality failures

The first finite-generation dependence occurs before Zelmanov's theorem: without finite generation, Zassenhaus terms need not be open. Hence density of torsion does not guarantee a torsion representative in an arbitrary coset G_(k+1)u used for a homogeneous Lie element.

A completely explicit illustration is B=∏_(n≥1) C_(p^n), additively. T(B) is dense. But B_2=pB is closed and not open, and the coset b+pB with b=(1 mod p^n)_n contains no torsion: every representative has a unit in every coordinate and hence coordinate orders p^n. The quotient B/pB is an infinite product of C_p. This directly disproves the inference “dense torsion => every homogeneous class has a torsion representative” for arbitrary pro-p groups.

Even if one establishes ad-nilpotence of a suitable collection of homogeneous elements, Zelmanov's PI theorem is applied to a finitely generated Lie algebra. At best a local application gives nilpotence for each finitely generated Lie subalgebra, with bounds depending on that subalgebra. This does not supply a global dimension, nilpotence, rank or analytic bound.

A further independent obstruction is that nilpotence of an associated ordinary Lie algebra alone cannot imply finite rank or p-adic analyticity without finite generation: for B above the associated Lie algebra is abelian, while B has infinite-dimensional B/pB and contains infinite-order elements. Ordinary Lie nilpotence must also be distinguished from finite-dimensionality and from control of all restricted p-powers.

These observations do not prove that P fails to repair the difficulty. The exact remaining task is to exploit P, beyond W, to obtain either suitable torsion lifting in the relevant closed subgroups/filtration terms or an entirely different group-theoretic argument. Simply assuming P passes to those closed subgroups transfers the central issue into an unproved inheritance claim.

## 4. A rigorous positive subclass for P

If G is virtually nilpotent of finite abstract nilpotence class and satisfies P, then G has finite exponent and is locally finite.

Proof. Choose an open nilpotent subgroup H, replacing it by its normal core if desired. P supplies a bounded-exponent coset aU contained in H. In a nilpotent group, torsion elements form a subgroup. Indeed, two torsion elements generate a finitely generated nilpotent group with finite abelianization; its lower central quotients are finitely generated abelian groups generated by multilinear commutators of bounded exponent, so they are finite, and the whole subgroup is finite. Since a and au are torsion for every u∈U, all of U is torsion. A finite extension of a torsion group is torsion, so H and G are torsion.

For completeness, a compact nilpotent torsion group of finite class has bounded exponent. In the abelian case Baire applied to the closed p^n-torsion subgroups gives one open bounded-exponent subgroup, and the finite quotient bounds the whole group. In class c>1, apply this abelian result to the closed center and induction to the quotient by the center; multiply the resulting exponent bounds. Thus H, and then its finite extension G, has bounded exponent. Local finiteness follows from Zelmanov's theorem for compact torsion groups. This argument covers the virtually abelian case in particular.

If G is p-adic analytic, P forces G finite: an open torsion-free subgroup intersects the dense torsion set only in the identity, contradicting density unless that open subgroup is trivial. No extension of this argument to arbitrary pro-p groups is claimed.

P also rules out infinite topologically finitely generated continuous quotients by Wilson Theorem C, since such quotients inherit P and hence W. This condition by itself does not resolve the arbitrary-group problem.

## 5. Printed Corollary 3.1 scope caution

The cached published Corollary 3.1, read literally, omits finite generation while concluding that a pro-p group with few infinite-order conjugacy classes is finite. The infinite elementary abelian group ∏ C_p contradicts that literal reading (it has no infinite-order elements). The preceding paragraph explicitly discusses finitely generated pro-p groups, and the proof invokes Theorem C, whose finite-generation assumption is explicit. Therefore this corollary must not be used outside the finitely generated scope without an independently justified correction. This is a transcription/scope caution, not a rejection of Theorem C.

## 6. Remaining research gap

No counterexample to P with infinite-order elements has been constructed here. No proof that P implies torsion in arbitrary pro-p groups has been obtained. The original conjugacy hypothesis is stronger still; no converse from P to that hypothesis is asserted. The weak-condition route is definitively blocked by the explicit semidirect products above, while the stronger locality route remains genuinely open in this audit.

## 7. Subsequent stronger partial theorem

2026-10-24 17:28 UTC: the independently delegated subclass check found and wrote a self-contained proof that P0 (every open subgroup contains a bounded-exponent open coset) forces finite exponent and local finiteness in virtually metabelian pro-p groups. Full proof: `strong_subclass/metabelian_locality.md`. My adversarial audit: `metabelian_adversarial_audit.md`. The mechanism uses V=closed G' tensor Q_p and a finite abelian two-operator character argument to lower the conjugation action exponent on successive open subgroups. It avoids inheriting P to arbitrary closed subgroups. No general solvable or arbitrary pro-p resolution and no originality claim.
