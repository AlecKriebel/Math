# Simple Young modules with nonprojective polynomial injective hulls

16 October 2026 · Version 1.0 · Unrefereed preprint

## The idea

A simple module has no proper nonzero submodule. Its top is its largest quotient that is a direct sum of simple modules. Injectivity and projectivity are different extension and lifting properties. Miyachi’s printed question asks whether a simple top of a Young module forces its associated polynomial injective hull to be projective at some permitted rank.

This note assembles classical representation theory into a family where the Young module itself is simple, but the associated injective hull is never projective. One example occurs in characteristic 3 with the partition (4,1).

## Original abstract

For every odd prime p, the Young module labelled by λ = (2p−2,1) in characteristic p is simple, whereas its corresponding polynomial injective hull I_n(λ) is nonprojective for every n≥2. At parameter q=1, this gives a negative answer to the unrestricted formulation of Miyachi’s Conjecture 7 in the 2009 Oberwolfach report. The proof combines classical representation theory with a labelled rank-truncation argument. We include explicit proofs of the local calculations and reproducible supporting checks. Historical priority remains unresolved; no firstness claim is made.

## The result

Let p be any odd prime, let k be algebraically closed of characteristic p, and take q=1. Put r=2p−1 and λ=(2p−2,1). In the stable Schur convention Y^λ = F I_N(λ), with N≥r, the Young module Y^λ is simple of dimension 2p−2. Its corresponding injective hull I_n(λ) in degree-r polynomial GL_n(k)-modules, equivalently for the Schur algebra S(n,r), is nonprojective for every integer n≥2.

The broad displayed Conjecture 7 asks for an equivalence between simplicity of top(Y^λ) and projectivity of I_n(λ) for some n≥ℓ(λ). Here ℓ(λ)=2. Simplicity of Y^λ gives a simple top, while the theorem excludes projectivity at every permitted rank. This answers that printed proposal negatively.

The separate stronger proposal uses the constructed Λ_n^i index families. Membership already suffices for projectivity; the theorem therefore excludes membership at every permitted rank and also gives a negative answer to that stronger simple-top criterion. No completeness assertion about the sufficient family is assumed.

## Why it works

Since p does not divide r=2p−1, the natural permutation module k^r splits into its constant line and the augmentation module A=ker(sum). A nonzero vector in a submodule of A has two unequal coordinates; subtracting its image under the corresponding transposition gives a nonzero coordinate difference. Permuting that difference spans A, so A is simple of dimension r−1.

The label is checked at stable rank, rather than inferred at rank two. Sym^(r−1)(k^N)⊗k^N has the two injective summands labelled (r) and λ. Multiplication onto Sym^r(k^N) splits because polarization satisfies mδ=r·id. Its kernel is I_N(λ); on multilinear weight spaces multiplication is coordinate summation. Exactness of F identifies the correctly labelled Young module with A.

At rank two, I_2(λ)=det⊗Sym^(2p−3)(k²). The symmetric power is a nonsplit extension of distinct simple modules: its socle has highest weight (2p−3,0) and dimension 2p−4, and its top has highest weight (p−1,p−2) and dimension 2. After the determinant twist, the labels are (2p−2,1) and (p,p−1). They remain distinct when p=3, even though both dimensions are 2. Thus this injective is not contravariantly self-dual and cannot be projective.

If I_n(λ) were projective at any n≥2, the classical projective-injective theorem would identify it with an indecomposable tilting module T_n(μ). Dominance leaves only μ=(r) or λ, both with at most two parts. Exact truncation of these labelled injective and tilting modules would make I_2(λ) an injective tilting module and hence projective, contradicting the rank-two calculation. This uses the labelled truncation theorems, not preservation of arbitrary projectives by an idempotent functor.

## Scope and limits

The result concerns algebraically closed characteristic p for odd primes and parameter q=1. Rank one cannot carry this two-part label, and p=2 is outside the theorem. The coefficient argument is for rational algebraic-group modules over the infinite field k, not merely the finite group GL₂(𝔽_p).

The characteristic-zero assumption in the later subsection 0.5 of Miyachi’s contribution belongs to a different method for simple Specht modules; it is not attached to the displayed Conjecture 7. This note does not address a characteristic-zero variant with a nontrivial root-of-unity parameter or refute the separate De Visscher–Donkin classification.

Row p-regularity is different from p-restrictedness, also called column p-regularity here. No projectivity inference from row regularity is used. The theorem supplies the stated all-prime, all-rank conclusion; the accompanying finite computations are supporting evidence rather than a proof of those universal quantifiers.

## Classical inputs and priority

The natural permutation/augmentation calculation, rank-two structure and Schur-algebra inputs are classical. De Visscher–Donkin supply reciprocity, injective multiplicities, tilting and labelled truncation; Cox–Parker record the stable F I convention. Erdmann–Law’s classical analogue of Proposition 3.1 and Theorem 3.3 give published local-structure antecedents. The contribution here is their explicit assembly into a counterexample to the broad printed proposal.

Historical priority remains unresolved. Coverage of older two-row papers, tables and later work is incomplete. No firstness, certified novelty, new local classification or current worldwide openness is claimed.

## Read the paper

Read the complete unchanged four-page paper below, open or download its original searchable PDF, or download the unchanged original source-and-verification ZIP.

[Open PDF](paper.pdf) · [Download PDF](paper.pdf) · [Source and verification ZIP](source-and-verification.zip) · [BibTeX](citation.bib)

If the PDF viewer is unavailable, open the original PDF.

## Related reading

[Miyachi, Dipper’s hypothesis and self-injective endomorphism rings](https://doi.org/10.4171/OWR/2009/17). Oberwolfach contribution, printed pp. 944–948; Conjecture 7 at p. 946.

[De Visscher–Donkin, On projective and injective polynomial modules](https://doi.org/10.1007/s00209-005-0805-x). Classical structural inputs; the note’s detailed locators use the 12 January 2005 institutional manuscript, printed pp. 7–12.

[De Visscher–Donkin institutional manuscript](https://openaccess.city.ac.uk/id/eprint/969/1/prinjjan12.pdf). Exact manuscript edition used for the structural page locators.

[Cox–Parker, Homomorphisms and higher extensions for Schur algebras and symmetric groups](https://doi.org/10.1142/S0219498805001460). Stable Young-module convention; detailed locators use the accepted manuscript.

[Cox–Parker accepted manuscript](https://openaccess.city.ac.uk/id/eprint/373/2/coxparker2final.pdf). The stable F I convention and regularity distinction.

[Erdmann–Law, Torsion pairs and Ringel duality for Schur algebras](https://arxiv.org/abs/2104.05317v1). Version 1, pp. 5–6: Proposition 3.1’s classical analogue and Theorem 3.3.

## Status and collaboration

AI tools were used extensively in the research, literature investigation, computations, checking and writing of this note and its supporting materials. This is an unrefereed preprint without external human peer review or proof-assistant certification; AI checks do not supply either.

Independent verification, a substantive comparison with earlier work or work toward a journal submission would be welcome. Collaboration and authorship would reflect actual contributions.

The note and original authored companion materials, including supporting code, are licensed under Creative Commons Attribution 4.0 International (CC BY 4.0). Cited third-party works retain their own rights.

## Citation

Alec Kriebel. Simple Young modules with nonprojective polynomial injective hulls. Version 1.0. Zenodo, 16 October 2026. doi:10.5281/zenodo.23418581.

[Download BibTeX citation](citation.bib)
