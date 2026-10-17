# Prior-art and clean-case monodromy audit

## Bottom line

The cone/minimal-prime/Jacobian procedure is an explicit necessary-and-sufficient finite algebraic criterion for the adopted complex fixed-camera problem, once its exceptional common-plane family is separated. Its ingredients are established algebraic geometry and computational algebra. Neither the criterion's existence nor its standard subroutines should be advertised as a newly discovered general reconstruction theorem. A contribution can be described conservatively as a scope-complete synthesis, including a precise exceptional split, admissibility filter, degree bookkeeping, and embedded smoothness test. An exhaustive priority or open-status claim has not been established.

## Primary-source verification

1. Kaminski–Fryers–Teicher, JEMS 7 (2005), 145–172, section 3.4, Theorem 2, printed pp.155–156, https://ems.press/content/serial-article-files/31537. The theorem and proof were inspected from the recovered full PDF/text. The paper explicitly works under generic configurations (printed p.146). In its reconstruction setting, generic monodromy is the full symmetric group on a degree-d cover; the diagonal action on ordered pairs has diagonal and off-diagonal orbits, producing degrees d and d(d-1). This is direct prior art for the fiber-product/monodromy approach. The simple-ramification genericity used in the proof must be retained; the result is not an arbitrary-image or arbitrary-center theorem.

2. Rydell–Sundelius, Projections of Curves and Conic Multiview Varieties, arXiv:2404.03063v1, https://arxiv.org/pdf/2404.03063v1. The full recovered text was searched and section 3 and its context inspected. Proposition 3.1 identifies irreducibility of an image with irreducibility of its cone and preserves degree. The conic multiview results work with closures of parameterized curve families, so membership in the closure alone must not be promoted to exact existence of an integral prescribed-curve lift. Low-degree cones and their residual intersections are established context.

3. Agarwal–Pryhuber–Thomas, Ideals of the Multiview Variety, arXiv:1812.09470v2, https://arxiv.org/pdf/1812.09470v2. The complete served 20-page PDF was newly retrieved. The introduction, p.2, directly describes Jacobian-rank smoothness and Hilbert-polynomial degree computations from the vanishing ideal. Theorem 3.7 gives ideal generation by bifocals and trifocals for distinct foci; Corollary 3.9 identifies center-related boundary tuples added by closure. Sections 4–5 distinguish determinantal ideals and saturated multiview ideals. These results support the ideal-theoretic methodology, but a point multiview-ideal theorem is not alone a prescribed-image-curve reconstruction theorem. The entire proof chain of the paper was not audited.

4. Agostini–Markwig–Nollau–Schleis–Sendra-Arranz–Sturmfels, Recovery of Plane Curves from Branch Points, arXiv:2205.11287v2, https://arxiv.org/pdf/2205.11287v2. The recovered source confirms multiple plane covers over branch data, including the plane Hurwitz counts 40 and 120. Thus equal degrees, genera, or branch supports do not specify a cover or its paired monodromy. For quartics, the relevant branch data lie on the discriminant image hypersurface; do not describe arbitrary twelve-point configurations as arising from a plane quartic.

5. Ballico, On the Algebraic Geometry of Multiview, Foundations 4 (2024), 306–323, DOI 10.3390/foundations4030020, https://www.mdpi.com/2858222. Primary publisher search text confirms discussion of known-camera cones, multiple components, ghosts, and low-degree families. Direct full-text/PDF retrieval again returned errors. This remains a search-index primary-source check, not a full-text audit. No novelty clearance is inferred from it.

6. Standard computation: Macaulay2's PrimaryDecomposition documentation explicitly supplies radicals, minimal primes, associated primes and primary decompositions, https://macaulay2.com/doc/Macaulay2/share/doc/Macaulay2/PrimaryDecomposition/html/index.html. The software's degree documentation gives the quotient-ring degree, https://macaulay2.com/doc/Macaulay2/share/doc/Macaulay2/Macaulay2Doc/html/_degree_lp__Ideal_rp.html. Singular's maintained primdec.lib source separately documents absolute prime components, https://github.com/Singular/Singular/blob/spielwiese/Singular/LIB/primdec.lib. Absolute decomposition is essential when the supplied field is not algebraically closed. A specific implementation's domain and termination limitations must not be mistaken for a theorem over every coefficient type.

7. Normalization and Bertini: Greuel–Laplagne–Seelisch, Normalization of Rings, https://arxiv.org/abs/0904.3561, supplies established effective normalization algorithms. Stacks Project Lemma 33.43.8, https://stacks.math.columbia.edu/tag/0A22, identifies normal/regular local rings of curves and smoothness over perfect fields. Stacks Lemma 37.32.3, https://stacks.math.columbia.edu/tag/0G4C, supplies a precise Bertini irreducibility statement sufficient for the two-assigned-multiplicity plane family. These sources were checked at the indicated statements/abstract, not their entire surrounding literature.

## Independent check of the clean-case assertions

Assume the two image curves X,Y are smooth, integral, and avoid their epipoles. The pencil maps X→T and Y→T are finite separable covers of degrees m,n. Here the full cone intersection avoids the baseline and centers, and triangulation identifies it with the fiber product X×_T Y. The latter is a Cartier divisor in a smooth surface, generically reduced by separability, hence reduced. The complete intersection has degree mn and arithmetic genus 1+mn(m+n-4)/2.

### Orbit components and projection degrees: valid under the clean hypotheses

Remove the branch values and use the resulting finite unramified covers. Connected components of their fiber product correspond to orbits of the paired action on the product of the two fibers. An orbit O projects onto both individual transitive fibers, with constant fiber sizes, so the component degrees to X,Y are |O|/m and |O|/n. The epipolar hyperplane pencil has no base divisor on the world component in this clean case, so its world degree is |O|. All lifts occur because a nonbaseline pair of image points has unique triangulation. Thus the orbit classification is correct and is standard covering-space mathematics; the special self-product instance is already in KFT.

The divisibility partition follows: each |O| is a multiple of lcm(m,n), all orbit sizes sum to mn, and the number of orbits is at most gcd(m,n). Divisibility alone does not determine which sizes occur for a fixed pair.

### Genus formula: valid

For a local monodromy permutation sigma_t restricted to O, its cycle count c_O(sigma_t) is the number of normalization points above t. Their ramification contribution is |O|-c_O(sigma_t). Riemann–Hurwitz therefore gives

2g(Ctilde_O)-2 = -2|O| + sum_t (|O|-c_O(sigma_t)).

This is the genus of the normalization. It is not an embedded smoothness assertion.

### Disjoint branch supports and smooth full intersection: valid

Completed local maps have equations t=u^p and t=v^q, hence the fiber product is u^p-v^q=0. It is singular exactly when p,q>1. Therefore the full intersection is smooth precisely when the branch supports are disjoint. It is then integral: the Galois closures have disjoint branch supports, their intersection is an everywhere-unramified cover of P1, and Riemann–Hurwitz forces that common subextension to be trivial. This proves linear disjointness. Alternatively a projective complete-intersection curve is connected, and a connected smooth curve is integral.

### Simple-overlap node budget: valid under its explicit definition

If each branch value of each cover has exactly one index-two ramification point, a shared branch value produces exactly one node, locally u²-v². All other points over it are smooth. Thus s shared branch values give s nodes. The normalization exact sequence for the connected nodal complete intersection gives

sum_i g_i = p_a - s + r - 1.

Together with r<=gcd(m,n), this yields s<=p_a+gcd(m,n)-1. A selected component is smooth at such a node precisely when it contains just one analytic branch. This is an elementary normalization/genus calculation. No global novelty claim is supported.

### General ramification local test: valid only for smooth image branches

With d=gcd(p,q), u^p-v^q has d analytic branches. Each is parametrized by u=s^(q/d), v=lambda*s^(p/d), so it is smooth exactly when p divides q or q divides p. A selected global component is smooth at the point exactly when it contains one local branch and that branch is smooth. If it contains several local branches, it is singular there. This local equation does not by itself model singular embedded image branches, center contraction, or baseline identifications; those require the actual triangulated prime ideal or the normalization map's local embedding data.

### Corrections beyond the clean case: valid but insufficient alone

Resolved image-pencil degrees are m-mult_epipole(X) and n-mult_epipole(Y). Their equality after multiplication by the two projection degrees is necessary. The center formulas delta-mult_cP(C)=ma and delta-mult_cQ(C)=nb are valid with Hilbert-Samuel multiplicity. Neither numerical relation classifies the actual components or their embedded smoothness. Outside the clean case, orbit size measures the resolved epipolar-pencil degree, not automatically the world degree.

## What the finite criterion adds and does not add

The finite criterion replaces the unfinished singular/epipole smoothness analysis by a certified operation on the finitely many actual embedded primes; it handles the one infinite exceptional family separately. It does not infer smoothness from normalization, use a degree divisibility condition as sufficiency, or treat a raw cone scheme as a selected reduced component. This is a complete effective route in the adopted algebraic universe, with an independent adversarial audit of the assembled algebraic criterion completed in this pass. The audit prompted a clarification that product saturation happens to retain the same candidates in the neither-epipolar-line case, although it is not the correct general geometric operation and fails as a uniform rule across the exceptional plane case. It does not settle real visibility, arbitrary camera models, positive characteristic, reducible input curves, or every reading of the original informal question.
