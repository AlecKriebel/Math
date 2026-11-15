# A symmetric ideal chain with periodic Lefschetz behavior in positive characteristic

Alec Kriebel · ORCID https://orcid.org/0009-0001-9320-500X

22 October 2026 · Version 1.0.0 · Unrefereed preprint

## Original abstract

For each fixed field of positive characteristic p, we construct a single compatible symmetric chain of Artinian ideals in two rows of variables, generated from width three. At every width n ≥ 2, its quotient has both the weak and strong Lefschetz properties exactly when p ∤ n − 1. The quadratic quotient is free over the integers, and a determinant for an arbitrary linear form gives the classification over every field extension. In particular, over the fixed infinite field 𝔽ₚ(t) both properties hold and fail at unbounded widths. This gives a negative answer to the unrestricted eventual dichotomies posed by Römer. It gives no negative answer in characteristic zero or in one row.

## What this means

The weak Lefschetz property asks whether multiplication by one linear form has the largest possible rank between consecutive graded pieces of an Artinian algebra. The strong property asks for the same behavior for every positive power of that one form.

This note gives a single symmetric family whose answer keeps changing as its width grows. Over a field of positive characteristic p, the obstruction recurs whenever n − 1 is divisible by p. The field and the defining rule stay fixed throughout the family.

## The construction and exact classification

Fix any field K. For width n ≥ 1, let Rₙ = K[x₁,…,xₙ,y₁,…,yₙ] and 𝔪ₙ = (x₁,…,xₙ,y₁,…,yₙ). Define the homogeneous ideal

Iₙ = 𝔪ₙ³ + (xᵢxⱼ : i ≠ j) + (yᵢyⱼ : 1 ≤ i,j ≤ n) + (xᵢyᵢ : 1 ≤ i ≤ n) + (xᵢyⱼ − xᵢyₖ : i,j,k pairwise distinct).

Here 𝔪ₙ³ includes every cubic monomial, including repeated variables; an empty index condition contributes no generators. The quotient Aₙ = Rₙ/Iₙ is Artinian. Every injection of column sets respects the ideals, so the chain is compatible with simultaneous column permutations in both rows. For every n ≥ 3, Iₙ = (Sym(n)I₃)Rₙ: the entire chain is generated from width three.

For every field K and every n ≥ 2, the Hilbert function is (1,2n,2n), and Aₙ has SLP if and only if it has WLP if and only if (n − 1)1_K ≠ 0. The same classification holds after every field extension, including extensions of finite fields. Width one is a separate case: its Hilbert function is (1,2,1), and it has SLP.

For each prime p, work over the single fixed infinite field K = 𝔽ₚ(t). Among n ≥ 2, exactly the widths n ≡ 1 (mod p) are bad. In particular, both properties hold at n = 2 + kp for every k ≥ 0, and both fail at n = 1 + kp for every k ≥ 1. Both sequences are unbounded. This disproves the unrestricted eventual alternatives in Römer’s question for one fixed field and one fixed two-row chain.

## Why the pattern occurs

The quadratic quotient is already free over the integers. For n ≥ 2 it has degree-two basis uᵢ = [xᵢ²] and vᵢ = [xᵢyⱼ], where any j ≠ i gives the same vᵢ. For each fixed i, the relations identify these mixed terms without introducing torsion, so this basis survives base change to every field.

For an arbitrary linear form ℓ = Σᵢ(aᵢxᵢ + bᵢyᵢ), multiplication from degree one to degree two has determinant (−1)ⁿ⁻¹(n − 1)∏ᵢaᵢ². At a bad width this vanishes for every choice of coefficients, not just for a symmetric test form. Independently, the nonzero degree-one element Σⱼyⱼ is then killed by every linear form.

At a good width, ℓ = x₁ + ⋯ + xₙ gives an invertible middle-degree map. Its square is Σᵢuᵢ ≠ 0, including in characteristic two. These maps cover all powers with nonzero source and target needed for SLP. The proof uses standard integral linear algebra, rank, determinant and socle methods; the contribution is this explicit chain and its complete classification.

## Scope and limitations

The counterexample uses two rows in fixed positive characteristic. In characteristic zero this particular construction has SLP at every width. It gives no negative answer for arbitrary characteristic-zero chains or for the one-row variant. The width-one exception must not be folded into the n ≥ 2 congruence rule.

The universal written proof establishes the infinite-width and all-field statements. The archive’s finite exact computations supplement that proof. Neither those computations nor bounded literature checks certify exclusive firstness, exhaustive novelty or the present worldwide open status of other variants.

## Context and credit

Tim Römer’s original contribution, “Asymptotic properties of invariant chains,” fixes an arbitrary field and an arbitrary fixed number of rows c ≥ 1. Its Artinian-chain question asks whether WLP or SLP eventually always holds or eventually always fails. That contribution is on printed pages 1594–1596 of Oberwolfach Report 31/2020. The separate working-group discussion on pages 1544–1545 focuses on one-row monomial ideals; it is a different scope.

Alexandra Seceleanu and Liana Şega’s “General symmetric ideals,” arXiv:2506.15459v1, gives positive results for general symmetric ideals in one row. Its Theorem B assumes an infinite field of characteristic zero or characteristic greater than n, positive integers d,r, and n ≥ max{d + 1, 1 + (1/r)Σᵢ₌₀ᵈ⁻¹P(i)}, where P(i) is the number of integer partitions of i. Under these hypotheses a general (r,d)-symmetric ideal has WLP. Its chain Theorem 9.2, summarized in Theorem C, assumes characteristic zero, positive d,r with r ≤ P(d), a general starting ideal at a width m sufficiently large for Construction 6.8, and n ≥ m. These hypotheses differ from the fixed-positive-characteristic two-row chain here. The v1 arXiv header is dated 18 June 2025; the PDF’s internal date is 19 June 2025.

David Cook II’s work provides standard background on characteristic-sensitive Lefschetz properties. None of these external theorems is needed in this note’s self-contained proof. The earlier project proof in PR1337 is unpublished. The Oberwolfach DOI identifies the original question; this preprint’s solution DOI is 10.5281/zenodo.23570763.

## Collaboration

I welcome researchers interested in independently verifying the integral quotient and arbitrary-form determinant, developing a substantive extension, or preparing a journal submission. Any eventual coauthorship would reflect actual mathematical or writing contributions agreed together.

## Authorship and review status

Published Zenodo preprint, version 1.0.0, originally dated 22 October 2026. Unrefereed.

AI tools were used extensively in planning, mathematical exploration, proof development and reconstruction, computation, literature investigation, writing, editing and adversarial checking. Alec Kriebel is the named human author. This preprint has no conventional independent human peer review, journal acceptance or formal proof-assistant certification.

## Primary background

- [Tim Römer, Asymptotic properties of invariant chains, OWR31/2020, printed1594–1596](https://doi.org/10.4171/OWR/2020/31)

- [Alexandra Seceleanu and Liana Şega, General symmetric ideals, arXiv:2506.15459v1](https://arxiv.org/abs/2506.15459v1)

- [David Cook II, The Lefschetz properties of monomial complete intersections in positive characteristic](https://doi.org/10.1016/j.jalgebra.2012.07.015)

- [Unpublished earlier project proof, PR1337](https://github.com/AlecKriebel/Math/pull/1337)

## Read the paper

Read the complete unchanged four-page published PDF below, or open and download it directly. The full original source and verification ZIP includes the manuscript, exact checker and offline reproduction instructions.

- Local unchanged PDF: assets/periodic-lefschetz.pdf

- Complete original ZIP: assets/periodic-lefschetz-source-and-verification.zip

- Citation: assets/citation.bib

- Zenodo DOI: https://doi.org/10.5281/zenodo.23570763

## Rights

Authored paper, mathematical prose, metadata and source text are licensed CC BY 4.0. Authored verification and packaging code is separately MIT licensed. Third-party works retain their own rights.
