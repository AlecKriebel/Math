# Mathematical screening verdict

2026-10-24, 23:14 UTC. Screening complete; the question remains unresolved here.

## One question worth retaining

For every infinite connected locally finite simple vertex-transitive graph X, with unit conductances, is

    E deg_FUSF(X²)(o) ≤ E deg_FUSF(X)(o)?

Equivalently: **can squaring strictly increase the expected degree of the free uniform spanning forest?**

Keep this as a question, not a conjecture. The published decrease removes equality as a universal answer but does not establish a preferred direction.

A universal inequality would reveal a mechanism surviving the loss of unimodularity. An increase would show that the existing decrease is not a general direction of change. The paper-level target is a theorem explaining the sign, or an opposing construction with a genuinely different mechanism. Merely repeating the finite-certificate workflow on a slightly altered example has a weaker claim to a separate paper.

The exact gap is that Rayleigh monotonicity lowers the old-edge marginals while newly added edges contribute positively. The needed argument must compare those effects in the free boundary limit. Success requires either a proof for the full stated class or a verified reverse strict inequality, with the graph hypotheses and infinite-volume passage checked. Numerical stabilization is insufficient.

## Suggestions rejected or deferred

- An exact value for the published square is useful internal work, but too narrow alone. It becomes substantial when part of a reusable reduction and convergence theorem for a meaningful family.
- Invariance iff unimodularity is false without restrictions. Nonunimodular graphs with no nonconstant harmonic Dirichlet functions have FUSF degree 2, and their powers retain this property. Tang's Diestel–Leader examples are a prior family.
- Unimodular power invariance belongs to the existing tracial framework and should not be repackaged as new.
- No particular limit for higher powers is supported. For the binary grandparent graph, if a,b are tree distances to the common ancestor, then d_G(x,y)=ceil(a/2)+ceil(b/2), hence T^(2n−1) ⊂ G^n ⊂ T^(2n). Both tree powers have expected FUSF degree 3, but inclusion does not compare total expected degrees. The omitted boundary pairs have odd a,b and number (4^n−1)/3: exactly one ninth of all neighbors in T^(2n), asymptotically two ninths of the outer sphere. Neither 2 nor 3 is justified as a proposed limit. General power-sequence convergence could eventually be a substantial problem, but it need not appear in the current public list.

## Bounded falsification screen

The script screen.py constructs finite free networks on the oriented 3-regular tree, using common-ancestor distance types (a,b), then computes sums of root effective resistances. All computations are exploratory floating point. No new infinite-volume result is certified.

Saved results cover 14 small edge-type families at radii 6–10. No reliable increase emerged. Several apparent increases disappeared at larger depth. For example, adding grandparent and cousin edges gave finite sums 2.5585392 → 2.6721353 at radius 8 but 2.5582388 → 2.5278603 at radius 10. This demonstrates boundary contamination, not a theorem of either sign. Some tempting examples have extra unimodular symmetry: the tree plus sibling edges is a tree of triangles, despite admitting a distinguished-end action.

A final diagnostic used weighted-square conductances given off the diagonal by A+A². The finite values in weighted-square-screen.json approach the original grandparent value. A candidate harmonic-Dirichlet calculation suggests that weighted operation may preserve expected degree: on harmonic functions its energy is (1+2d) times the old energy, with a matching local-energy identity after summing an invariant orthonormal basis. This is an **unverified internal observation**, not a theorem or public follow-up recommendation. It may provide a simple control explaining why erasing path multiplicities matters.

## Sources and limits

- [BLPS, corrected author version](https://rdlyons.pages.iu.edu/pdf/usf.pdf): transitive WUSF expected degree 2 and the harmonic-Dirichlet/free–wired framework (Theorems 6.4, 7.3, 7.7–7.8).
- [Gaboriau, arXiv v3](https://arxiv.org/pdf/math/0405458): the transitive unimodular harmonic-projection invariant, especially Proposition 2.9.
- [Tang, arXiv v2](https://arxiv.org/pdf/1908.09889): Proposition 5.3 for Diestel–Leader graphs and Section 5.2 for grandparent graphs.

This is bounded screening, not a guarantee of worldwide openness or priority. The strongest verified infinite-volume finding remains the published exact base value and certified decrease. No person was contacted. Parent agent owns integration and the main-branch checkpoint.
