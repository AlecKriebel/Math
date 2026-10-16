# KP-1.66: failure of antisymmetry is already established

Status: source-corrected known negative answer; independent source review pending. No new mathematical discovery is claimed.

## Target and source correction

Problem 2725 / KP-1.66 asks whether exact Lagrangian cobordism defines a partial order on Legendrian links in standard contact three-space. The relevant equivalence is Legendrian isotopy, as is conventional for this question. Even on knots, antisymmetry fails.

The pinned database labels this open and its August 2026 literature note says no resolution was verified. That assessment is stale. The original problem is confirmed on page 63 of the [K3 problem list](https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf). The dataset's AIM URL points to a four-page workshop report rather than the full problem list.

## Existing theorem and direct consequence

Dimitroglou Rizell and Golovko's [paper, arXiv:2409.00290v4](https://arxiv.org/html/2409.00290v4), Theorem 1.4 / 5.7 and Corollary 1.5, provides mutually Lagrangian-concordant knots in standard contact R³ with different smooth knot types. One endpoint is a sufficiently positively and negatively stabilized decomposably fillable representative of the mirror of 9_46; the other is the correspondingly stabilized standard unknot. The first version dates to 2024. The arXiv record reports acceptance in Advances in Mathematics; the author's [publication list](https://sites.google.com/site/ragolovko/publications) lists volume 502 (2026), article 111133, DOI 10.1016/j.aim.2026.111133. Publisher full text was not independently retrieved.

Here is the precise logical implication for the queued target. Let A and B be that pair. A concordance is a cobordism, so the two concordances give A≼B and B≼A. Stabilization leaves the underlying smooth knot type unchanged. Consequently A remains a nontrivial smooth knot and B remains an unknot. A Legendrian isotopy would be a smooth isotopy, which is impossible. Thus [A]≠[B] as Legendrian isotopy classes and antisymmetry fails. Since knots are one-component links, this already disproves the relation's partial-order property on the larger link class.

There is no exactness loophole in passing from these concordances to the problem's relation. The existence theorem expressly gives exact Lagrangian concordances. Independently, for a Lagrangian cylinder L in the symplectization, the pullback of e^tα is closed. Its period on an end circle vanishes because the end is Legendrian. That circle generates H₁(L), hence all periods vanish and the form has a primitive on L. On a cylindrical end the form vanishes pointwise, so the primitive is constant on each connected end. This is the required exact-cobordism boundary behavior.

## Boundaries of this conclusion

- The examples use stabilizations of both signs and a nonregular direction. No assertion about a restricted relation requiring regular or decomposable cobordisms is made.
- The conclusion is existential. The cited construction requires sufficiently many stabilizations; this note does not calculate a smallest or explicit numeric stabilization count.
- This is an applicability check of an existing theorem, not an independent reconstruction of its h-principle dependencies or a new explicit parametrized concordance.
- Failure of symmetry alone would not disprove a partial order. The argument uses mutual comparability of distinct isotopy classes, which is the relevant failure of antisymmetry.
- The result is already in the literature. A campaign classification should credit the authors and use `already_solved`, subject to independent source review.

## Reproducible evidence

The sibling source manifest records primary URLs, PDF hashes, theorem locations, the pinned record, and access limitations. The complete paper was downloaded outside the public-safe attempt folder. Only this original audit, metadata, checks and the supplied dataset record belong in the proposed repository package.

Research completion: 100% of the source-status audit and theorem-to-target implication; no novel-solution claim. Independent review remains pending before a PR.
