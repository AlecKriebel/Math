# Source and current-literature audit

Checked 2026-09-30. This is a bounded audit, not certification that the full
problem remains open worldwide. No verified complete resolution was found.

## Exact original

1. Anurag K. Singh, “Remarks on F-pure rings,” joint work with Uli Walther,
   in [Kommutative Algebra, Oberwolfach Report 19/2005](https://ems.press/content/serial-article-files/45993?nt=1),
   pp.1115–1116. The final question on p.1116 was read and visually checked.
   It names the same ring, parametrization, kernel, and arbitrary ideal b.
   The workshop is from 2005; the publisher page records publication in 2006.
   [Publisher metadata](https://ems.press/journals/owr/articles/824),
   DOI [10.4171/OWR/2005/19](https://doi.org/10.4171/OWR/2005/19).
2. Anurag K. Singh and Uli Walther,
   [Local cohomology and pure morphisms](https://arxiv.org/abs/math/0701524),
   Example3.5 and Question3.6. The same characteristic-zero question appears.
   Their example records vanishing of local cohomology with support in a in
   degrees at least three, and attributes the positive-characteristic
   set-theoretic complete-intersection result to Hartshorne.

## Relevant later results and exact limits

3. Linquan Ma, Karl Schwede, Kazuma Shimomoto,
   [Local cohomology of Du Bois singularities and applications to families](https://arxiv.org/abs/1605.02755),
   Proposition4.9 and Corollary4.10. The first rules out set-theoretic CMness
   for non-CM Du Bois quotients. The cone here is not seminormal, so its
   hypotheses fail. The graded criterion concerns nonpositive-degree defects;
   the present defect is in degree one. Neither criterion settles this target.
4. Alberto F. Boix and Majid Eghbali,
   [Vanishing of local cohomology and set-theoretically Cohen-Macaulay ideals](https://arxiv.org/abs/1806.04405),
   Remark5.7 and Theorem5.8. The rational quartic is linked to two skew lines;
   the stronger linkage statement has explicit flatness/injectivity/cofinality
   hypotheses. Linkage alone is not a solution mechanism.
5. S. Hamid Hassanzadeh,
   [Set-Theoretically Perfect Ideals and Residual Intersections](https://arxiv.org/abs/2409.05705),
   v2 (2025), Theorem1.2 and Corollary3.19;
   [published article](https://doi.org/10.1112/jlms.70108), JLMS111(2025), e70108.
   We checked the theorem's two alternatives. The skew-line source has four
   generators but residual codimension two. Its first Koszul homology has a
   socle and the second cycle module has projective dimension two, so the
   alternative depth/projective-dimension hypotheses also fail.
6. David Eisenbud and Bernd Sturmfels,
   [Binomial Ideals](https://arxiv.org/abs/alg-geom/9401001), Section2;
   [published author copy](https://eisenbud.github.io/papers/pdfs/1996-002.pdf).
   Laurent binomial ideals are reduced in characteristic zero. The note gives
   a short direct group-algebra argument in the coefficient-one case needed
   here. This is classical input, not an original discovery.
7. David Eisenbud and Antonius Van de Ven,
   [On the Normal Bundles of Smooth Rational Space Curves](https://eisenbud.github.io/papers/pdfs/1981-001.pdf),
   Math.Ann.256(1981),453–463, especially p.463 on rational quartics.
   The note independently supplies an explicit cubic frame proving the
   conormal splitting in this parametrized example.

## Searches and verification boundaries

Search families included exact numeric ID/code, the curve parametrization,
set-theoretic Cohen–Macaulayness in characteristic zero, Macaulay-curve
thickenings, rational-quartic double structures, and the newest
residual-intersection literature. MathOverflow discussions from 2022 and
2025 were useful discovery leads, but no theorem in the note depends on them.
The source papers and explicit computations supply the mathematics.

The restriction to homogeneous double structures is deliberately separate
from the original target. No theorem allowing homogenization of an arbitrary
CM thickening was found or assumed. No source found in this pass proves or
excludes a non-binomial, transversely nonreduced, higher-multiplicity thickening
in the full scope required.

## Duplicate and prior-attempt check

- Repository base:01358d66fc67d1c462bddf31c0d4ee5b120e6737
- Queue rank31, queued0/5, blank prior Chat/Findings/DOI fields
- No target folder in the recursive tree; exact-ID/code searches only found
  catalog and desk-review metadata
- No exact-ID or Cohen-related PR found; no matching remote branch existed
- No related-target-group entry or matching second dataset statement found
- Pinned dataset revision37e53eabe540fb458758e198be61634bd02ee008
- The problem code has one occurrence. No prior AI research report is present

These checks establish no located prior attempt in the accessible records,
not the absence of unpublished work elsewhere.
