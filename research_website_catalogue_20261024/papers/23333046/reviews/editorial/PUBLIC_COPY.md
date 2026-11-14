# A characteristic-two counterexample to dévissage for local deformation functors

Alec Kriebel · Independent researcher · [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X)

12 October 2026 · Zenodo version 1.0 · [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

Unrefereed research note, Zenodo version 1.0. Extensive AI assistance; no external human peer review, journal acceptance or formal proof-assistant certification.

Manuscript and declared publication date: 12 October 2026. Zenodo records version 1.0; the manuscript prints no version number.

## Overview

Dévissage asks whether deformations of a group action can be assembled from deformations of a subgroup and its quotient. This note gives a characteristic-two action for which the proposed formally smooth fibre-product factorization fails.

The obstruction rules out every prorepresentable recipient in the stated category, regardless of tangent dimension. It combines a known involution deformation pathology with an injective tangent restriction map. The precise coordinate-equivalence category is essential.

## Original abstract

We give a negative answer to the unrestricted fibre-product question for local deformation functors posed by Byszewski. For the weakly ramified action of the additive group of F₄ given by t↦t/(1+at), and its subgroup F₂, restriction–induction cannot be formally smooth over any prorepresentable recipient, regardless of its tangent dimension. The proof combines the known involution deformation pathology with an exact calculation showing that restriction has injective tangent map. The variant assuming prorepresentability of the subgroup and quotient deformation functors is untouched. The involution pathology and additive action are established prior ingredients; the contribution is their use to obstruct the proposed factorization.

## The result

Let k=F₄=F₂[u]/(u²+u+1), G=(k,+), N=(F₂,+), Q=G/N, and ρ(a)(t)=t/(1+at). This is the standard weakly ramified additive action on k[[t]].

Work with local Artinian W(k)-algebras with identified residue field k. D_H consists of lifts of the given local action modulo all coordinate changes reducing to the identity, including changes with nilpotent constant terms. D_N^Q is the actual fixed subfunctor of D_N.

There is no prorepresentable recipient F=h_R, with R a complete Noetherian local W(k)-algebra with residue k, and no choice of natural maps f:D_N^Q→F←D_Q:g that makes the actual restriction–induction map D_G→D_N^Q×_F D_Q formally smooth. This holds for every tangent dimension of F, including the one-dimensional recipient prescribed in the refined question.

The theorem uses the actual deformation functors and their fixed subfunctor. It does not replace either component by a versal hull or assume a formula for the tangent maps of arbitrary natural transformations.

## Why the proof works

The invariant parameter y=t²/(1+t) identifies the subgroup-fixed ring with k[[y]], and the quotient acts by σ(y)=y/(1+y). A nonzero quotient tangent is represented by (y+ε)/(1+y) over k[ε]/ε². The known involution conjugacy, or the known collision under an injection of coefficient rings, forces every natural map to a prorepresentable Hom-functor to send this tangent to the residue basepoint.

Separately, invariant derivations restrict precisely to M=y k[[y]]∂y. With z=y²/(1+y), the quotient action on the complete module M=y k[[z]]∂y⊕y²k[[z]]∂y has kernel equal to image for its characteristic-two cohomology differential. Thus H¹(Q,Θ^N)=0, giving injectivity of tangent restriction. This is a full formal-series argument.

For any proposed recipient maps, the pair (0_N,v) is therefore a genuine point of the fibre product over the dual numbers, with v nonzero. Formal smoothness would lift it to a G-deformation with zero restriction and nonzero induction. Injective restriction forces that deformation to be zero, whose induction is zero, giving a contradiction already over k[ε]/ε²→k.

## Scope and limits

The statement concerns this specific F₄ additive action and its F₂ subgroup in the original unframed category. Fixing the zero section, choosing a framed category, replacing actual functors by hulls, using global deformation functors, or allowing arbitrary nonprorepresentable recipients changes the problem.

The separate variant assuming that both the subgroup and quotient deformation functors are prorepresentable remains unaddressed. The example uses the exceptional nonprorepresentable involution component and does not contradict the conditional obstruction-space theorems.

The additive action, involution parameter-shift conjugacy, failure to preserve injections and resulting all-recipient tangent collapse are established antecedents. The note combines them with the restriction-kernel calculation to obstruct the proposed factorization. Historical first priority and continued worldwide openness through 2026 are not certified.

Finite exact calculations support explicit identities. The all-formal-series and all-natural-transformation quantifiers depend on the written proof; they do not follow from finite-jet experiments.

## References and credit

[J. Byszewski, Dévissage for local deformation functors, Oberwolfach Reports 54/2008, pp. 3038–3040](https://ems.press/content/serial-article-files/46200). The unrestricted question on page 3039 is distinct from Theorem 3, which adds component-prorepresentability hypotheses.

[J. Byszewski, Cohomological aspects of equivariant deformation theory, Utrecht Ph.D. thesis (2009)](https://dspace.library.uu.nl/handle/1874/33749). Question 6.4.4 and the separate conditional result provide the thesis formulation of the same question.

[J. Byszewski, Deformation functors of local actions, arXiv:1112.0352v1 (2011)](https://arxiv.org/abs/1112.0352v1). Supplies the deformation-category, actual fixed-functor, restriction/induction and tangent-cohomology framework. Question 4.4 and Remark 4.5 keep the unrestricted and conditional formulations separate.

[J. Byszewski and G. Cornelissen, Which weakly ramified group actions admit a universal formal deformation? (2009)](https://doi.org/10.5802/aif.2450). The additive action and exceptional involution pathology are prior work. Proposition 4.1 gives the parameter-shift conjugacy; Proposition 6.1 gives the injection collision, from which all-recipient tangent collapse follows by naturality.

## AI and review status

AI tools were used extensively in research, proof development, code, literature work and writing. This is an unrefereed research note without external human peer review, journal acceptance or formal proof-assistant certification; the named author is responsible for the work.

## Collaboration

Substantive proof checks, counterexamples and precise comparisons with prior work are welcome. Authorship and acknowledgments would reflect actual research contributions and mutual agreement. Citations credit prior work and imply no participation or endorsement.

## Read the paper and source

Read the complete 5-page deposited paper in the on-page PDF reader.

[Open PDF](/research/characteristic-two-local-devissage/characteristic_two_counterexample_local_deformation_devissage.pdf)

[Download PDF](/research/characteristic-two-local-devissage/characteristic_two_counterexample_local_deformation_devissage.pdf)

[Download original PDF from Zenodo](https://zenodo.org/api/records/23333046/files/characteristic_two_counterexample_local_deformation_devissage.pdf/content)

[Download complete ZIP](/research/characteristic-two-local-devissage/local_deformation_devissage_source_verification_v1.zip)

[Download original complete ZIP from Zenodo](https://zenodo.org/api/records/23333046/files/local_deformation_devissage_source_verification_v1.zip/content)

[Download BibTeX](/research/characteristic-two-local-devissage/citation.bib)

## Citation

Alec Kriebel (2026). A characteristic-two counterexample to dévissage for local deformation functors. Zenodo version 1.0, 12 October 2026. https://doi.org/10.5281/zenodo.23333046.

```bibtex
@misc{Kriebel2026CharacteristicTwoDevissage,
  author = {Kriebel, Alec},
  title = {A characteristic-two counterexample to dévissage for local deformation functors},
  year = {2026},
  month = {oct},
  day = {12},
  date = {2026-10-12},
  version = {1.0},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.23333046},
  url = {https://zenodo.org/records/23333046},
  note = {Unrefereed research note; extensive AI assistance; no external human peer review or formal proof-assistant certification},
  orcid = {0009-0001-9320-500X}
}
```
