# KP-3.55: direct-summand diagnostics and an unresolved geometric gap

Status: **unsolved**, both original parts unresolved by this attempt. This is an elementary algebraic diagnostic and a source audit, not a new Floer theorem. Separate review is pending.

## Exact target and source boundaries

Problem 2853 / KP-3.55, [K3, printed pp.170–171](https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf), asks whether (a) every nontrivial knot in S³ has an F₂ direct summand in HFK⁻ as an F₂[U]-module, and (b) every rational homology sphere with nonzero HF_red has such a summand. A submodule killed by U is not enough: it must split.

The pinned statement matches the original. K3 records affirmative cases for fibered knots and single-parity top knot-Floer groups, attributing them to Baldwin–Vela-Vick and Ni. [Ni, Theorem 1.1](https://www.its.caltech.edu/~yini/Published/SecondTerm.pdf) has an explicit single-parity hypothesis; it cannot be dropped. Its stated rank inequality is not, by itself, a proof about the full minus module. We do not reconstruct the additional Floer arguments behind K3's stated consequence.

[Lin's theorem](https://arxiv.org/html/2309.01222v1) proves the reduced-module assertion for rational homology spheres with a coorientable taut foliation, using nontrivially paired U-annihilated contact classes. Lin also explains the implication from the foliation part of the L-space conjecture and the connected-sum reduction. Assuming that conjecture is not an unconditional resolution.

[Alfieri–Binns, arXiv:2404.00490v1](https://arxiv.org/html/2404.00490v1), Theorems 1.7–1.8, proves the stronger tower-length restriction for knot surgeries in S³ and large link surgeries. “Large” is essential. Their Corollary 1.13 gives integral homology spheres not realizable as large link surgeries, so the general link surgery presentation theorem does not remove this hypothesis. Related dataset record 30005951 concerns this same geography problem; it should not be treated as an independent resolution opportunity for part (b).

A newer [Binns–Wan preprint, arXiv:2608.03900v1](https://arxiv.org/html/2608.03900v1), Theorem 1.3, gives a next-to-top hat-homology statement for knots with w-avoiding exterior. Its restrictive exterior hypothesis and its hat-homology conclusion are retained. No general minus-module conclusion is inferred here, and the full analytic construction has not been independently certified.

## 1. A necessary and sufficient algebraic test

Let F=F₂, R=F[U], and T be a finite-dimensional F-vector space with nilpotent U action A. Write

T ≅ ⊕_{j≥1} (R/(U^j))^{m_j}.

For r_k=rank_F(A^k), including r_0=dim_F(T), one has

m_1 = r_0 − 2r_1 + r_2.

Proof: on a block of length j, the three ranks are j, max(j−1,0), max(j−2,0). Their second difference is 1 precisely when j=1, and zero otherwise. Direct sums add ranks. More generally m_j=r_{j−1}−2r_j+r_{j+1}. Thus a desired summand exists exactly when the indicated second difference is positive. For a module with free part, apply this test to its U-torsion submodule T, not to the infinite-dimensional whole module.

Equivalently,

m_1 = dim_F(ker A / (ker A ∩ im A)).

Indeed, a length-one block contributes a kernel vector outside im A, while every longer block's kernel is contained in its image. This proves why nonzero kernel alone is insufficient.

This is a computable equivalence, not a proof of positivity for Floer groups. No matrix from a previously uncomputed knot or manifold is supplied.

## 2. Duality alone does not force a length-one block

Put the dual action on T*=Hom_F(T,F): (A*φ)(x)=φ(Ax). Evaluation restricts to a pairing ker A × ker A* → F. Its rank is exactly m_1.

Proof without a choice of Jordan basis: ker A* consists precisely of the functionals vanishing on im A. The left radical of the restricted pairing is therefore ker A ∩ im A. Taking the quotient gives the rank stated above. Consequently a pair x,φ with Ax=A*φ=0 and φ(x)=1 exists if and only if an F summand splits off.

This restates the algebraic mechanism in Lin's proof. Perfect duality of T with T* is not enough to produce such a pair: take T=R/(U²). The pairing on the full spaces is perfect, but the pairing restricted to the two kernels is identically zero. More generally T=R/(U^k) for k≥2 is an obstruction to any argument relying only on finite generation, nilpotence, and duality.

These are abstract module counterexamples, NOT knot or manifold counterexamples. Even adding a rank-one free part does not fix the algebraic obstruction: the free R-chain complex with generators a,b,c and differential d(a)=U²b, d(b)=d(c)=0 has homology R[c]⊕R/(U²)[b]. After inverting U, only the free rank-one homology remains. One can give this complex a compatible Maslov grading by setting deg U=−2, deg b=0, deg a=−3, deg c=0. This does not establish the filtered structures, geometric realization, conjugation constraints, or any other Floer axioms needed to realize a counterexample.

## 3. Why the available geometric routes stop

- Pure module theory permits the obstructing modules above. It does not prove either original universal assertion.
- Lin's route requires a geometrically produced pair of U-annihilated classes with nonzero pairing. Assuming such a pair for every nonzero reduced group simply assumes an equivalent algebraic form of the desired conclusion.
- Surgery geography settles substantial known subclasses. General surgery descriptions neither turn an arbitrary manifold into knot surgery nor ensure the link framing is large relative to its link Floer polytope. Replacing the large-surgery hypothesis by no hypothesis is the open step.
- For part (a), next-to-top hat ranks alone do not supply the missing minus-module U action. The parity/exterior assumptions in the inspected results cannot be silently removed.

## Exact remaining gap and verification scope

A complete affirmative proof must force m_1>0 for every actual nontrivial knot's torsion module and every nonzero reduced module in the target, using geometric input beyond the algebra above. A negative answer requires a realized knot or rational homology sphere with an audited Floer module having all torsion lengths at least two. Neither is provided.

The verifier exhausts all strictly upper-triangular binary matrices through dimension six, checking the rank diagnostic against the kernel/intersection criterion and the restricted dual pairing. It also includes zero, one-dimensional, length-two and mixed-block controls. These finite tests check implementation and elementary identities; they do not resolve Floer realization or certify a new theorem.

Three substantive approach families were tested: module structure, paired geometric classes, and surgery transfer. All are blocked at the stated gaps. Best estimate of completion toward full original resolution: 0%; diagnostic/source audit complete. No novelty claim. Runtime metadata: inherited runtime, exact model identifier not exposed to this worker; no model or reasoning switch made.
