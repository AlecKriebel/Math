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

Checked 2026-10-01T16:40:02.253864+00:00. The original dated source audit above remains historical.

## Current independent primary-source and version qualification

The original unrestricted question is confirmed visually in OWR2005p1116 and Singh–Walther v2 p8: local cohomology vanishes for i>=3, and no homogeneity assumption is present. Original workshop2005 and publication2006 are distinct dates.

MSS complete v3 (14April2017), Proposition4.9p16 and Corollary4.10p17, was checked. The latter requires a nonzero nonpositive-degree defect; H1_m(A)=K(-1) is in degree+1. Nonseminormality excludes the former's Du Bois premise over C. These failed sufficient tests imply neither existence nor nonexistence of an unrestricted thickening.

Boix–Eghbali complete corrected v2 (12June2021), Remark5.7 and Theorem5.8p18, was checked. The regular-local conditional theorem requires a flat local endomorphism, injective Ext transition maps, cofinal families and an already CM source thickening, along with m not contained in the zero divisors of R/I. Linkage does not supply those premises. Adjacent Remark5.10 calls the toric quotient nonreduced, which conflicts with its explicit prime; that statement is not used. Both complete-intersection colons for the displayed link were independently certified directly.

Hassanzadeh complete v2 (February2025), Theorem1.2pp2–3 and actual Corollary3.19p22, was checked. The introductory summary p3 states additional hypotheses absent from the p22 corollary, but the actual SD requirement already fails here. The complete published version-of-record text was inaccessible; only publisher metadata (JLMS111(3), e70108, firstpublished6March2025) was verified, so no full published-text comparison is asserted. The theorem's every-cycle projective-dimension alternative fails at Z2, independently of proper-sequence choices. Padding with redundant local generators leaves Z2 as a summand in Z_(k+2) and the required bound1, so it cannot repair this shortcut.

Eisenbud–Sturmfels published author copy Section2/Cor2.2, and Eisenbud–Van de Ven p463, were read in full relevant scope. Arbitrary-field reducedness and the conormal frame are proved directly; no embedding of every characteristic-zero K into C is assumed. Classical inputs are credited, and no novelty, exact later-solution absence or worldwide openness certificate is claimed.

Three independent families pass the precise restrictions. Generic length one is excluded without homogeneity. Generic length two is excluded only for homogeneous b. The exact remaining class is non-binomial a-primary b with nonzero nilpotent q; homogeneous members need length>=3, arbitrary nonhomogeneous members need length>=2. A general CM-preserving homogenization/flat same-radical degeneration shortcut is false: K[x,y,z]/(x²,xy+z) is CM, while its highest-degree initial quotient by (x²,xy,xz,z²) retains a nonzero maximal-ideal socle. This validated boundary control does not resolve the Macaulay-curve question.
