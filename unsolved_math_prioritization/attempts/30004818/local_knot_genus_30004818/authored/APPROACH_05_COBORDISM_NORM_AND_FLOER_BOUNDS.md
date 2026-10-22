# Author approach 5: cobordism norms and a general Floer lower bound

## Attempt toward a full negative answer

The previous attempts leave surfaces with genuinely nontrivial fundamental-group image and knots with a gap between stable and ordinary four-genus. This final attempt seeks a general lower-bound mechanism, independent of the image subgroup: regard local-knot bounding genus as a norm on classical concordance classes and try to force that norm to equal g_4. Floer-theoretic functionals provide concrete lower bounds. The attempt produces a broad restricted equality, but the completion to ordinary genus fails for a specific reason, exhibited by published large-genus torsion examples.

This is author approach 5. Reading the theorems used as inputs is not a separate turn, and no novelty is claimed for their corollaries.

## A genus function on classical concordance

Fix a closed connected oriented smooth three-manifold M. For a classical knot K placed in a ball in M, define q_M([K])=g_{M×I}(K).

A compact oriented bounding surface of genus g can equivalently be viewed as a genus-g cobordism from K to a local unknot: remove a small interior disk and carry its new trivial boundary to the other end along a thin tube around an arc disjoint from the remaining surface. The arc exists by general position. Conversely, cap the unknot by a local disk.

### Local-knot propagation through a surface

If S is an embedded oriented cobordism from local knots K_0 to K_1, choose an embedded arc on S joining its two boundary components. A product neighborhood of that arc allows insertion of a knotted arc representing any classical J. Replacing the straight strip by the corresponding knotted strip ties J into both ends. This gives a cobordism of the same genus from K_0#J to K_1#J. It changes the single connected surface itself; it does not require the disjoint spectator annulus whose absence blocked approach 3.

It follows that:

1. q_M is well-defined on the smooth classical concordance group C. Stack a local classical concordance with a bounding surface; doing this in both directions proves equality for concordant representatives.
2. q_M(K#J)≤q_M(K)+q_M(J). Propagate J through a genus-q_M(K) cobordism K→U to obtain K#J→J, then stack a genus-q_M(J) cobordism J→U.
3. q_M(−K)=q_M(K), where −K is the concordance inverse. Propagate −K through K→U to get K#−K→−K. Prepend a classical genus-zero concordance U→K#−K and reverse the resulting cobordism. This gives q_M(−K)≤q_M(K); interchange K and −K for the reverse inequality.
4. q_M(K)=0 precisely when K is classically slice, by the Boden–Nagel local-knot theorem and the local embedding of a classical slice disk.
5. q_M(K)≤g_4(K), by placing a classical surface in the local ball product.

Thus q_M is a definite integer-valued group norm on C, bounded above by g_4. The question is exactly whether this inequality can ever be strict.

### Why the norm argument alone does not close

Injectivity and equality of zero sets do not force equality of norms. On Z, both |n| and ceil(|n|/2) are definite symmetric subadditive integer-valued norms, and the second is strictly smaller at n=2. On a cyclic group of order two, assigning the nonzero element any positive integer gives a group norm. Thus even torsion norms can differ while preserving precisely the same zero element.

Stabilizing gives q_{M,st}(K)=lim_n q_M(nK)/n by subadditivity, but stabilization loses all torsion information. This is a structural loss, not an inequality that can be repaired by dividing a finite-cover estimate more carefully.

## A general lower bound: classical τ survives every orientable product

For every local classical knot K in a closed connected oriented M,

    |τ(K)| ≤ q_M(K) ≤ g_4(K).

In particular, if |τ(K)|=g_4(K), then q_M(K)=g_4(K) for every such M. This has no restriction on the surface's fundamental-group image, no rational-homology-sphere assumption, and no assumption that the capped surface is absolutely null-homologous.

### Published inputs

We use the usual nonvanishing of hat Heegaard Floer homology for a closed oriented three-manifold, its conjugation symmetry, the connected-sum filtration formula, and Hedden–Raoux's relative adjunction inequality (Theorem 1). Conjugation symmetry is Theorem 2.4 of Ozsváth–Szabó, Holomorphic disks and three-manifold invariants: properties and applications. Hedden–Raoux's Proposition 2.6 records the τ connected-sum formula. These results are invoked, not reproved.

### The local filtered-complex calculation

Choose a nonzero α∈HFhat(M,s), and normalize the knot filtration using a Seifert surface for K inside its local ball. As a based knot, (M,K) is the connected sum (M,U)#(S³,K). The unknot filtration on CFhat(M,s) is concentrated at level zero under the local disk normalization. Consequently the connected-sum formula gives

    τ_α(M,K)=τ_α(M,U)+τ(K)=τ(K),
    τ_α(M,U)=0.

The same equalities hold for every nonzero Floer class, including a nonzero conjugate class in HFhat(M,s̄). In elementary filtered-complex terms, the local Alexander filtration is entirely on the classical knot factor, so selecting a different nonzero homology vector in the M factor does not raise its detection threshold.

### Keeping the absolute homology correction

Let F be any genus-g bounding surface in M×I. Puncture and tube it as above to form a genus-g cobordism S from a local unknot U to K. Cap the two boundaries with the chosen local Seifert surfaces to obtain a class A∈H₂(M×I;Z). We do NOT assume A=0. Approach 4 gives only zero intersection form, so A²=0.

The product cobordism induces the identity on HFhat(M,s). Apply the relative adjunction inequality using the pulled-back Spinᶜ structure and α. With the local normalization this gives

    ⟨c₁(s),A⟩ + 2τ(K) ≤ 2g.

Apply the same theorem in the conjugate Spinᶜ structure, whose first Chern class is −c₁(s), using a nonzero conjugate Floer class. Its local τ value is still τ(K), so

    −⟨c₁(s),A⟩ + 2τ(K) ≤ 2g.

Adding these two inequalities yields τ(K)≤g. Reverse the surface cobordism to run from K to U and repeat the argument. Its τ difference is −τ(K), and conjugation again removes its Chern pairing. Hence −τ(K)≤g as well. Therefore |τ(K)|≤g for every admissible F. Taking the minimum proves the bound. ∎

The conjugation step is important. An unqualified application of a displayed τ slice-genus bound can hide a Seifert-surface/homology-class normalization. Here the cap class is retained until its contribution is explicitly canceled.

### An exact test case

For a sum K of n equally handed trefoils, |τ(K)|=n and a classical genus-n surface realizes the upper bound. Therefore q_M(K)=n for every orientable M. The nonorientable trefoil-pair construction cannot be reproduced with those same knots in any orientable three-manifold, including manifolds not covered by approaches 1 or 2. This rules out that direct family without answering the existence question for other knots.

## Attempt to maximize over all Floer classes

One might hope that taking the maximum over α∈HFhat(M) would recover g_4(K). The local calculation prevents this: all of these τ values are the same classical τ(K). Enlarging M or choosing a different Floer class adds no information for this particular local-knot functional.

More generally, any real-valued additive concordance invariant v satisfies v(K)=0 on torsion, because d[K]=0 implies d v(K)=0. Even access to every such invariant cannot recover the ordinary four-genus of a non-slice torsion knot. Passing to the rationalized concordance group or using dual functionals on a stable norm has the same limitation.

## A concrete large-gap family, not a counterexample

Allison N. Miller's published theorem constructs strongly negative amphichiral knots of concordance order two with arbitrarily large topological four-genus, hence arbitrarily large smooth four-genus. For those knots,

    g_st(K)=0,     τ(K)=0,     g_4(K) can be arbitrarily large.

The first equality follows directly from #²K being slice; the second from additivity of τ. This is much stronger than using the genus-one figure-eight merely to show that stable genus can differ from ordinary genus.

The Miller family therefore survives the additive-functional strategy and is a concrete family to test against the equivariant construction of approach 3. Its rational slice disks, and the Spin(RP³) realizations discussed there, still do not establish a surface in RP³×I. Neither a free equivariant product surface nor a sufficiently low-intersection relative companion concordance has been constructed in these five attempts.

## Disposition after five approaches

The attempted general norm proof stops at the distinction between norm injectivity and isometry, and at the inability of additive invariants to detect the ordinary genus of torsion. The Floer calculation proves a substantial restricted equality, but it does not resolve all classical knots.

After five genuine author approaches, there is no full proof that genus savings are impossible and no verified orientable-product counterexample. The correct author disposition is unresolved with partial results, pending independent mathematical review. This is not a claim that all future avenues are exhausted.

## Public references

- M. Hedden and K. Raoux, Knot Floer homology and relative adjunction inequalities, Theorem 1 and Proposition 2.6. https://arxiv.org/abs/2009.05462 ; https://doi.org/10.1007/s00029-022-00810-1 .
- P. Ozsváth and Z. Szabó, Holomorphic disks and three-manifold invariants: properties and applications, Theorem 2.4. https://annals.math.princeton.edu/wp-content/uploads/annals-v159-n3-p04.pdf .
- A. N. Miller, Amphichiral knots with large 4-genus, Theorem 1.1 and Corollary 1.2. Bulletin of the London Mathematical Society 54 (2022), 624–634. https://doi.org/10.1112/blms.12588 ; https://arxiv.org/abs/2011.09346 .
- H. U. Boden and M. Nagel, Concordance group of virtual knots. https://arxiv.org/abs/1606.06404 .
