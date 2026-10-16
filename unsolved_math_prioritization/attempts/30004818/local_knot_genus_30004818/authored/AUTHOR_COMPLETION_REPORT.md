# Author completion report: problem 30004818

## Outcome

Five substantive author approaches have been completed. No full proof or verified counterexample has been obtained for the existence of a local classical knot K in an orientable smooth three-manifold M with g_{M×I}(K)<g_4(K). The author disposition is **unresolved, with partial results pending independent review**. This document is not an acceptance report, and the partial propositions should not be represented as independently certified.

The target uses compact connected orientable smoothly properly embedded bounding surfaces with one local boundary knot. Source reconstruction and current-literature searches were performed separately and were not counted as author approaches.

## The five approaches

1. **Finite-image covering.** If a genus-g surface has fundamental-group image of finite order d, its connected pullback has genus 1+d(g−1) and d boundary components. Merging those boundaries gives g_4(#^dK)≤dg, hence g_st(K)≤g. This excludes finite-image savings when stable and ordinary genus agree. Infinite image and stable-genus gaps remain.
2. **Image-subgroup covers.** For an abelian-image surface in an orientable complete hyperbolic three-manifold, the image cover is R³, S¹×R², or T²×R. Embedding that cover in S³ preserves the original genus. In particular, no genus-one saving is possible in a complete hyperbolic ambient manifold. Nonabelian image and other geometries remain.
3. **Equivariant/relative construction.** A slice #²K does not provide the required free orientable quotient surface. A precise disjoint companion-link concordance would give a genus-one product surface; an ordinary absorbing annulus with r spectator intersections yields only genus at most 1+r. No construction with sufficient control was obtained.
4. **Surgery/product intersection.** Every local-boundary surface in M×I has zero integral class in H₂(M×I,∂), and the product has zero absolute intersection form. Direct algebraic-dual-sphere and intersecting-tori transfers fail. Vanishing algebraic intersection does not construct Whitney disks or rule out every other method.
5. **Cobordism norm/Floer lower bounds.** The product genus defines a definite integer-valued group norm on classical concordance. A local filtered-complex calculation and conjugate Spinᶜ relative adjunction inequalities give |τ(K)|≤g_{M×I}(K). Thus τ-sharp knots cannot save genus in any orientable ambient M. Neither norm injectivity nor additive functionals determine ordinary four-genus on torsion.

Each approach has its own full authored file and a separate verification record. Numerical checks certify only their stated arithmetic identities, not the geometric arguments.

## Current source boundary

Park–Wu–Yang's March 2026 preprint explicitly presents the full question as open and proves a substantial partial theorem for ν⁺-sharp knots in rational homology spheres: https://arxiv.org/abs/2603.18619 .

The adjacent McDonald–Miller constructions are in punctured four-manifold fillings, not the required product collars: https://arxiv.org/abs/2511.15900 .

A final bounded literature check also identified Hedden–Raoux's July 2026 publication of Relative Thom conjectures, symplectic and beyond, whose author preprint is https://arxiv.org/abs/2512.03250 . The abstract concerns almost-complex/symplectic surfaces under extra geometric hypotheses; it does not state a general local-knot genus theorem. Only its abstract/publication metadata were checked in this final pass, so no stronger claim about its contents is made. No general resolution was found in the searches, which is not proof that no later work exists.

## A surviving, concrete mathematical avenue

Miller's strongly negative amphichiral order-two knots have arbitrarily large ordinary four-genus and stable genus zero: https://doi.org/10.1112/blms.12588 . They demonstrate that the gap left by approaches 1 and 5 is large. To obtain an actual counterexample, one still needs an embedded product surface, such as the correctly equivariant surface or disjoint relative-link concordance specified in approach 3. Rational sliceness and four-manifold filling examples do not supply it.

## Review priorities

- Check the precise compact punctured-manifold compression input in approach 1 and the boundary-orientation/band accounting.
- Check the explicit elementary hyperbolic quotients and genus-one boundary relation in approach 2.
- Check the pair-of-pants orientation conventions, spectator requirement, and intersection-smoothing cost in approach 3.
- Check relative versus absolute homology throughout approach 4.
- Check the local-knot propagation and inverse-norm construction, local Alexander normalization, nonzero conjugate Floer classes, and retained cap-class correction in approach 5.

No repository, queue, branch, or PR was changed during this author work. Downloaded source PDFs and extracted text are not included in the authored deliverables or authorized for publication by this report.
