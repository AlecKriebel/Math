# Vanishing of the cellularization map for non-p-nilpotent component groups

Alec Kriebel · [ORCID](https://orcid.org/0009-0001-9320-500X)

17 October 2026 · Version 1.0.0 · Unrefereed preprint

The manuscript prints version 1.0.0 and 17 October 2026, matching the Zenodo version and declared publication date.

## Original abstract

Let G be a compact Lie group whose component group is not p-nilpotent, and let k be any field of characteristic p. For R=C_*(Ω((BG)^∧_p);k), we prove that the canonical k-cellularization map ΓₖR→R induces zero in every homotopy degree. This answers Greenlees's Question 2.2 in Oberwolfach Report 9/2026. No adjoint-orientability, component-action, or spectral-sequence-collapse assumption is needed. The proof combines classical proxy-smallness and the finite-ideal theorem for Hopf algebras: each homotopy class in a cellular source factors through a module with finite total homology, whose image in an infinite-dimensional graded Hopf algebra must vanish.

## What the result means

Cellularization is a standard way to approximate a module by objects assembled from the coefficient field. It comes with a canonical map back to the original module. This note proves that, for the completed loop-chain algebras in the theorem, that full map sends every homology class to zero.

The result applies to every prime and every field of that characteristic, including infinite field extensions. It includes both finite and positive-dimensional compact Lie groups with the stated component-group condition. The conclusion concerns induced homology maps; it does not assert that the map itself is zero in the derived category.

## The full result

Fix any prime p and any field k of characteristic p. Let G be any compact Lie group whose finite group of connected components π₀G is not p-nilpotent. A finite group is p-nilpotent when it has a normal subgroup of order prime to p and index a power of p.

Set X=(BG)^∧_p using Bousfield–Kan p-completion, then R=C_*(ΩX;k). Completion is taken before looping. We work with left modules over this augmented differential graded k-algebra, equivalently with Hk-linear modules. Their homotopy groups π_n are the homology groups of the associated chain complexes.

Theorem 1. For the full canonical k-cellularization map ν:ΓₖR→R, the induced map π_n(ν):π_n(ΓₖR)→π_nR is zero for every integer n. No adjoint-orientability, nilpotent component-action or spectral-sequence/tensor-collapse assumption is imposed. The conclusion is not restricted to a degree range or to a projection into component-group homology.

The note also proves a general cellular vanishing criterion. Let A be an augmented differential graded k-algebra and let Loc_A(k) be the smallest localizing subcategory of left A-modules containing the augmentation module k. Suppose k is proxy-small over A and the multiplication on H_*(A) admits a graded Hopf-algebra structure over k, with Koszul signs, of infinite total dimension. Then every A-linear map f:M→A from every M∈Loc_A(k) induces zero on homology in every degree.

Proxy-smallness means that there is a compact proxy K with K∈thick_A(A)∩thick_A(k) and k∈Loc_A(K). Here thick means finite construction by shifts, finite sums, cones and retracts. Only K is required to be compact; compactness of k is not assumed. Infinite total dimension is distinct from a statement about the dimension of each separate degree.

## Why the map vanishes on homology

The algebraic input is the classical finite-ideal theorem: an infinite-dimensional graded Hopf algebra with Koszul signs has no nonzero finite-dimensional graded left or right ideal. The paper recalls the ordinary argument and treats graded signs by forgetting them in characteristic two or using parity bosonization otherwise. No bijectivity assumption on the antipode is needed.

Proxy-smallness gives a finite approximation for each homology class separately. If M is k-cellular, each class in H_n(M) comes from some P∈thick_A(K), whose total homology is finite-dimensional. Compact Morita theory and filtered finite constructions supply these stages. This does not say that the whole cellular module has finite homology, or that all its classes pass through one common finite stage.

For an A-linear map f:M→A, the composite P→M→A has a finite-total-dimensional image in H_*(A). A-linearity makes that image a graded left ideal. The Hopf theorem forces it to vanish, so f kills the chosen class. Applying this argument to every class proves the all-cellular-source, all-map criterion.

For completed loop chains, the existing Dwyer–Greenlees–Iyengar proxy-smallness result applies to every compact Lie group. Extending chains and a compact proxy from the prime field F_p to k preserves the required finite constructions and homotopy colimits. The argument does not interchange an infinite cochain dual with scalar extension.

Loop multiplication, diagonal and inversion give H_*(ΩX;k) its graded Hopf structure, with the field Künneth identification. In this application, p-compactness of BG means finite total mod-p homology of Ω((BG)^∧_p). Ishiguro's necessary implication BG p-compact ⇒ π₀G p-nilpotent therefore gives infinite total homology by contraposition under the theorem's hypothesis. Field extension preserves that infinite dimension. The general criterion then applies to the full canonical map ΓₖR→R.

The proof is analytic and uses the credited classical inputs. The supporting exact finite tests check the graded sign conventions; they do not establish an infinite or topological theorem by sampling.

## Scope and limitations

The coefficient is a field of characteristic p and G is compact Lie with the specified non-p-nilpotent component group. No general coefficient-ring or noncompact-group extension, converse, or transfer to uncompleted loop chains is asserted. Completion before looping is part of the statement.

The theorem gives a homology ghost: all induced homology maps vanish. It does not assert a null morphism in the derived category, and it is not replaced by a statement only about component-group homology. No orientability, component-action or collapse hypothesis is added to the full result.

The general criterion retains its proxy-smallness and infinite-total-dimensional Hopf hypotheses. For example, when A=k the cellularization is the identity, so the infinite-dimensional hypothesis cannot simply be deleted. The approximation is class by class and does not impose finite total homology on arbitrary cellular sources.

The prior-source comparison uses the actual pinned Greenlees v3 and Lomp author-version interfaces and the cited published DGI, BIS and Ishiguro interfaces. It does not claim that every final journal body or the earlier Sweedler, Dwyer–Greenlees and Ishiguro original proofs were freshly read. Historical firstness, exhaustive literature absence and present worldwide openness are not certified.

## Background and credit

Greenlees's Question 2.2 in Oberwolfach Report 9/2026, printed page 594, asks the full cellularization-map vanishing question for positive-dimensional compact Lie groups. The note answers that stated question in the non-p-nilpotent component-group setting and also includes finite groups.

The finite-group result is already in Greenlees's arXiv:2504.03050v3, Lemma 6.2. Its Section 6 also contains restricted compact-Lie conclusions with orientability context, nilpotent-action or restricted-image conditions, and an additional tensor-collapse condition in the relevant statements. Those prior results and their ranges remain credited. The inspected author v3 is not silently identified with final journal bytes.

The Hopf finite-ideal input is classical, credited to Sweedler through Lomp's Section 2.4. Compact proxies and Morita machinery are due to Dwyer, Greenlees and Iyengar. Briggs, Iyengar and Stevenson give related filtered finite-construction arguments. The note supplies the class-by-class step explicitly and does not take an unrestricted compactness conclusion from that source. No novelty is claimed for these constituent results.

The topological application uses Ishiguro's published 2007 Proposition 1.3(a), which supplies the necessary p-compactness implication. The cited earlier original proof is treated as prior input rather than claimed to have been newly reproduced. The contribution is the combination giving the stated full-map result, without a worldwide first-priority or continued-open-status claim.

## Contribution and collaboration

Independent verification of the algebraic or topological argument, a well-supported primary-source comparison, or substantive work toward journal submission would be welcome. Authorship would be considered in relation to actual contributions.

## AI and review disclosure

AI tools were used extensively in developing and checking the argument, inspecting sources, preparing reproducibility materials and drafting the note. This is an unrefereed preprint. Internal AI reviews are not human peer review, and no formal proof-assistant certification is claimed.

## Read and download

Read the complete unchanged four-page version 1.0.0 paper below, or open or download the original PDF. The complete original source and verification ZIP includes an identical embedded copy of the paper. Cited third-party source bodies are linked separately. Follow the README with Python 3.10 or later and assertions enabled for the optional convention tests.

- [Open original PDF](assets/cellularization-vanishing.pdf)
- <a href="assets/cellularization-vanishing.pdf" download>Download original PDF</a>
- [Download the complete original ZIP](assets/cellularization-vanishing-source-and-verification.zip)
- [Download BibTeX](assets/citation.bib)
- [Zenodo record and DOI](https://doi.org/10.5281/zenodo.23439582)

<iframe src="assets/cellularization-vanishing.pdf#view=FitH" title="Vanishing of the cellularization map for non-p-nilpotent component groups — complete four-page PDF" width="100%" height="850" loading="lazy"></iframe>

## Citation

Alec Kriebel. Vanishing of the cellularization map for non-p-nilpotent component groups. Version 1.0.0, 17 October 2026. Zenodo. doi:10.5281/zenodo.23439582.

## Primary background

- [Greenlees, Oberwolfach Report 9/2026 — Question 2.2, page 594](https://doi.org/10.4171/owr/2026/9)
- [Greenlees, actual author v3 — Section 6 finite and restricted prior results](https://arxiv.org/abs/2504.03050v3)
- [Greenlees, journal bibliographic record — final-body access limit stated above](https://doi.org/10.1112/blms.70405)
- [Dwyer–Greenlees–Iyengar, Duality in algebra and topology](https://doi.org/10.1016/j.aim.2005.11.004)
- [Lomp, author v1 — Section 2.4 and classical Sweedler attribution](https://arxiv.org/abs/math/0307046v1)
- [Ishiguro, 2007 — Proposition 1.3(a)](https://doi.org/10.2140/gtm.2007.10.195)
- [Briggs–Iyengar–Stevenson, published filtered-approximation interface](https://nyjm.albany.edu/j/2025/31-26.html)

## Rights

The paper, source, authored verification materials and code are licensed under Creative Commons Attribution 4.0 International (CC BY 4.0), as stated in the deposited LICENSE.txt and Zenodo metadata. Cited third-party works retain their own rights and are not included as source bodies.
