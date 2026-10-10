# Mathematical resolution of AMR-065-0014

## 1. Exact scope

The source is Faustin Adiceam's *Open Problems and Conjectures Related to the Theory of Mathematical Quasicrystals*, Arnold Mathematical Journal 2 (2016), 579–592, §2.6, Problem 2.6.1. The same problem is on page 8 of arXiv:1604.06280v2. Its mathematical content, restated here, is:

For a Delone subset D of the Euclidean plane that admits a bi-Lipschitz bijection to Z², does there exist a bi-Lipschitz map of the whole plane carrying D exactly onto Z²?

Here a Delone set has constants r,R>0 such that different points have distance at least r and every point of the plane lies within R of D. The collection explicitly uses “BL” for existence of a bi-Lipschitz **bijection**. All distances in this note are Euclidean. A map f is α-bi-Lipschitz, α≥1, when

    α⁻¹ |x−y| ≤ |f(x)−f(y)| ≤ α |x−y|

for all domain points x,y.

The problem has dimension exactly two. It assumes neither repetitivity nor linear repetitivity; neither finite local complexity nor periodicity; neither a bounded-displacement matching nor the Burago–Kleiner condition. It imposes no homogeneity, prescribed origin, translation equivariance, orientation, or optimal-constant requirement on the ambient map. It asks for existence of some ambient rectification, rather than extension of a specified bijection.

The historical paragraph following the question gives linear repetitivity and the Burago–Kleiner condition as sufficient special cases. They are not additional hypotheses of the question. The inaccessible live catalogue page is not used as the authority for these quantifiers.

## 2. Published theorem used

Michael Dymond and Vojtěch Kaluža, *Planar bilipschitz extension from separated nets*, Journal of the London Mathematical Society 113(4) (2026), e70540, DOI [10.1112/jlms.70540](https://doi.org/10.1112/jlms.70540).

Theorem 1.1, on published page 3, supplies an ambient bi-Lipschitz extension for each bi-Lipschitz map from Z² into R², with a bound depending polynomially on its distortion. Theorem 1.5, on page 7, makes the bound explicit: an α-bi-Lipschitz input has an extension of distortion at most

    C = 10^20000 α^6000.

In particular the input need not satisfy a small-distortion condition or any symmetry. The paper's introduction, published page 2, expressly identifies its result as a complete positive answer to Adiceam's Problem 2.6.1. The source theorem is an external published result; this package does not purport to reprove or independently audit its 34-page proof.

## 3. Auxiliary surjectivity fact

**Lemma.** Every C-bi-Lipschitz map H:R²→R² is onto and is a C-bi-Lipschitz homeomorphism.

**Proof.** The lower inequality makes H injective, and the upper inequality makes it continuous. By invariance of domain, H(R²) is open. It is also closed: if H(x_j) converges, then

    |x_j−x_k| ≤ C |H(x_j)−H(x_k)|,

so (x_j) is Cauchy, converges to some x in the complete space R², and continuity gives H(x_j)→H(x). Thus the image contains every limit of its convergent sequences. Since R² is connected and the image is nonempty, open, and closed, the image is all of R². Interchanging domain and image points in the two metric inequalities shows that H⁻¹ is C-bi-Lipschitz, hence continuous. ∎

The only topological theorem used in this lemma is the standard invariance-of-domain theorem. The argument does not silently identify a general embedding of a proper subset with a surjective ambient map.

## 4. Complete deduction for the original problem

Let D satisfy the original hypotheses. Choose an α-bi-Lipschitz bijection b:D→Z². Then g=b⁻¹:Z²→D⊂R² is also α-bi-Lipschitz: substitute x=b⁻¹(u), y=b⁻¹(v) in the inequalities for b and rearrange them.

Apply Dymond–Kaluža Theorem 1.5 to g, obtaining a C-bi-Lipschitz H:R²→R² whose restriction to Z² is g, with the C above. By the lemma, H is onto and has a C-bi-Lipschitz inverse A=H⁻¹. For every d∈D, put z=b(d). Then H(z)=g(z)=d, so A(d)=z=b(d). Consequently

    A|D = b,        A(D) = Z².

This is the ambient map requested in Problem 2.6.1. It actually extends the arbitrarily chosen input bijection b. No separation or covering constants of D are needed in the resulting distortion bound because the extension theorem was applied on the fixed domain Z². The Delone hypothesis remains part of the original question; it has not been replaced by a claim that all Delone sets are rectifiable. ∎

## 5. Accounting and limits

This settles the exact planar statement by a credited prior result. The current published theorem is stronger than the original existence question, so further original proof attempts are stopped. Campaign accounting is one verified prior-result approach, **1/5**, and **zero original-proof credit**.

No all-dimensional extension theorem, optimal bound, bounded-displacement rectification, homogeneous rectification, or equivariant rectification is claimed. The explicit constant is supplied only as a verified consequence of the published theorem, not as a practical numerical estimate.
