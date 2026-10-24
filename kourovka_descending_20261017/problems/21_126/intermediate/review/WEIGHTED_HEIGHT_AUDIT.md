# Independent adversarial audit: weighted nonzero Artin kernels

## Verdict and exact scope

**PASS for the revised derived partial theorem.** For a finite defining graph whose flag complex is simply connected, a homomorphism of its RAAG to Z that is nonzero on every standard generator has finitely presented kernel with intrinsic Dehn function bounded above, coarsely, by n^4. This is a polynomial obstruction to one proposed construction route. It does not settle Kourovka 21.126, give an upper bound on arbitrary subgroups of that kernel, cover zero weights, or establish novelty.

This reviewer did not author the proof. I read only the submitted note and the cached primary pushing-map source for this audit before checking the coordinate construction independently. I actively checked whether different weights break sign flips, agreement across cells, or homotopical filling. No counterexample to the stated restricted theorem was found. Reviewer acceptance is not an independent human peer review or a replacement for proof.

## Primary-source scope checked

Abrams–Brady–Dani–Duchin–Young, *Pushing fillings in right-angled Artin groups*, cached text dated September 27, 2011: Theorem 4.2 constructs the height-pushing retraction, Lemma 4.5 extends it over the required skeleton under connectivity of L, Remark 4.6 explicitly permits homotopical admissible fillings, and Theorem 5.1 gives the standard Bestvina–Brady bound. Their displayed model uses unit heights. The submitted note supplies its own rectangular-coordinate adaptation; it does not claim that their printed theorem explicitly states arbitrary weights.

## Independent mathematical checks

1. Inverting negatively weighted generators is a RAAG automorphism. Dividing the weights by their common gcd does not change the kernel. Positive integral weights therefore suffice.
2. Assigning length m_i to i-labelled edges preserves the all-right links; the simply connected rectangular Salvetti cover remains CAT(0). Weighted l1 length and Euclidean length have uniform comparison constants because the dimension is bounded. The affine height gradient has all positive coordinate slopes one in weighted l1 coordinates.
3. Radius epsilon<1/4 vertex balls are disjoint and miss level zero: distinct vertices are at least one apart, and a nonzero vertex height is a nonzero integer. Each boundary is the same finite combinatorial signed link with fixed metric constants.
4. In one complete coordinate flat, with integer coordinate vertex p and height h(p), let t_i>=0 satisfy sum_i m_i t_i=1. After changing all link signs toward zero the proposed image is p-h(p)(t_i)_i. Its height is exactly zero and its coordinate support stays in the complete flat determined by the link simplex. This verifies the crucial image constraint without presuming unit weights.
5. Along an i-edge from p to p+e_i, both endpoint constructions give p-h(p)e_i/m_i. Thus the maps agree on the whole-edge target even when an endpoint already has height zero. Faces have contained standard flats, so coning over a truncated higher cell is compatible with the maps previously constructed on its faces.
6. The truncated source cells, additionally cut by level zero, have finitely many shapes: weights are fixed, and a level-intersecting rectangle has only a bounded finite set of possible integer vertex heights. Each target is a convex slice of the corresponding Euclidean standard flat. Coning therefore adds dimension-dependent fixed constants, and local Lipschitz constants in a height strip grow at most linearly with strip height. This local bound suffices for the area estimate.
7. Extending pos/neg over the cone's 2-skeleton requires paths and disk fillings in L and no higher connectivity. Since L is a fixed finite simply connected complex these finitely many extensions can be chosen Lipschitz. Their compositions with the ray maps keep the linear height bound. There is no unsupported contraction of all of L, and no assertion that L is contractible.
8. The revised proof now supplies the previously omitted boundary detail. The level polyhedral 1-skeleton lies in X^(2). A general loop may first be homotoped within Z to that skeleton; relative cellular approximation into X^(2) is then legitimate. The domain of the extended retraction is connected, so Z is path connected, as well as having every loop null homotopic. These two clarifications remove the original presentation gaps.
9. A cube meeting Z has a vertex height in a fixed bounded interval. Vertices of a given height form a single kernel orbit, and cube types are finite. Hence the kernel action on Z is free, proper, and cocompact. The simply connected finite-quotient level cell complex supplies a finite presentation.
10. A loop of length n can be moved to the induced level 1-skeleton with O(n) annular area. The ambient CAT(0) disk has O(n^2) area and O(n) height excursion; relative cellular approximation preserves these estimates up to constants. Pushing multiplies area by O(n^2). Reattaching the level annulus gives a homotopical disk of area O(n^4). At no point is a homological chain substituted for the required disk.

## Adversarial boundary cases

- One-generator RAAG: kernel is trivial and the level set is a point; no exception.
- Complete defining graph: the level set is an affine Euclidean slice; the quartic upper bound is compatible with its stronger quadratic/linear bounds.
- A tree flag complex, with arbitrarily unequal fixed positive weights: no failed compatibility was found; varying constants do not produce a varying asymptotic scale.
- A simply connected but noncontractible flag complex needs only the cone 2-skeleton extension. Possible higher homotopy does not invalidate the disk argument.
- Zero weights, infinite defining graphs, and arbitrary finitely presented subgroups of the kernel are outside the theorem and cannot inherit its conclusion without new arguments.

## Exact reproducible local checks

`verify_rectangles.py` uses only Python's standard library and exact rational arithmetic. It tests every ordered triple of weights in {1,...,6}, every integer base height from -12 through 12, every rectangle corner, and five rational link directions. It independently checked 207,640 link image/flat support constraints and 64,800 edge compatibilities. `rectangle_checks.json` records the result. These finite tests check formulas, not the general topology or asymptotic theorem; those are justified in the mathematical audit above.

## Corrections requested and resolved

The first version tried to put an arbitrary boundary loop in X^(2) by relative cellular approximation, although a loop in Z need not already lie there, and did not explicitly prove Z connected. The author added the level 1-skeleton homotopy and connected-domain argument. The revised final bytes were reread before this PASS. No substantive objection remains for the restricted derived result.
