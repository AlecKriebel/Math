# A free-chain counterexample to a Nash-intersection conjecture

Alec Kriebel · ORCID https://orcid.org/0009-0001-9320-500X

Original publication: 22 October 2026 · Version 1.0.0 · Unrefereed preprint

## Original abstract

We compute the intersection of the closed Nash sets of the complete family of prime divisors obtained by n successive free point blowups over (ℂ²,0), after fixing a prefix of k centers, where 2≤k<n. In suitable coordinates the intersection is {ord x≥⌈n/k⌉, ord y≥n}. For five blowups, fixing two or three centers gives the thresholds (3,5) or (2,5). Neither is q(1,j) for positive integers q,j. These examples disprove the specified-reference-multiple assertion in Conjecture 1 of Fernández de Bobadilla, Pe Pereira and Popescu-Pampu, under each contact and indexing convention explicitly treated here. The source's bare equivalence symbol is undefined and its indexing is inconsistent; no unique author-intended correction is asserted. The intersections are themselves maximal divisorial sets for other toric divisors. Thus the result does not disprove an assertion allowing an arbitrary divisor, or solve the generalized Nash problem.

## Overview

An arc is a parametrized curve near a point, described here by two formal power series. Blowing up a point replaces it with an exceptional curve that records directions. A sequence of blowups produces divisors, and each divisor determines a closed set of arcs called its Nash set.

This note varies every free continuation of a fixed initial sequence of centers and computes the arcs belonging to every resulting closed Nash set. Five blowups give intersections that cannot be the claimed contact multiple of any divisor in the fixed reference chain.

The conclusion concerns a specified reference divisor. The same intersections do come from other toric divisors, so the result does not rule out an arbitrary-divisor formulation.

## Central result

Work in the centered complex formal arc space 𝒜={(x(t),y(t)):x,y∈tℂ[[t]]}, with ord 0=+∞. The sets below are Zariski-closed sets of arcs, equivalently reduced supports.

For every n≥3 and 2≤k<n, fix the first k centers c₁,…,cₖ of the length-n free chain following y=0. Let 𝓕ₙ,ₖ be the complete family of final prime divisors with that all-free combinatorial type and fixed prefix. In regular coordinates every member is represented by P(x)=Σᵢ₌ₖⁿ⁻¹aᵢxⁱ and y=P(x)+xⁿw, with every coefficient tuple (aₖ,…,aₙ₋₁)∈ℂⁿ⁻ᵏ allowed. This is the entire free family, not a selected subfamily. Smooth curvettas and further free blowups are included; no restriction to minimal embedded resolutions of singular branches is imposed.

For its final divisor E_P, the closed Nash set is N̄_Eₚ={ord x≥1, ord(y−P(x))≥n}. Taking the intersection over all coefficients gives Iₙ,ₖ=⋂_{E′∈𝓕ₙ,ₖ}N̄_E′={ord x≥⌈n/k⌉, ord y≥n}. Requiring exactly k common centers means aₖ≠0 and gives the same closed intersection.

Let Dⱼ be the divisor created at the jth center of the zero reference chain, continued further if necessary. For every positive j and q, the closure of exact-contact-q arcs is Cont̄^q(Dⱼ)={ord x≥q, ord y≥jq}. Closing the at-least-q contact locus gives the same formula.

For n=5,k=2 the intersection is {ord x≥3, ord y≥5}; for n=5,k=3 it is {ord x≥2, ord y≥5}. Neither threshold pair is (q,jq) for any positive integers j,q. The exclusion is for all reference indices and multiplicities, not a bounded computation.

For the specified reference Dₖ, equality Iₙ,ₖ=Cont̄^q(Dₖ) holds exactly when k divides n, with q=n/k. This does not say that every nondivisible pair excludes every other Dⱼ: for example n=6,k=4 gives thresholds (2,6), matching q=2,j=3.

## Why the calculation works

Each newest exceptional curve has one point meeting the older exceptional locus. That point is the satellite intersection; all other choices are finite free centers in the displayed polynomial chart. The two final charts are (x,y−P(x))=(x,xⁿw) and (x,y−P(x))=(vh,vⁿ⁻¹hⁿ). They account for the complete family and its satellite limits.

The Nash cylinder is irreducible, and the locus ord x=1 is dense. The deformation xε=x+εt, yε=P(xε)+y−P(x) includes arcs with x=0 and the constant arc in the closure. Raw transverse loci are not substituted for their closed Nash sets.

The two family members P=0 and P=xᵏ force ord y≥n and ord xᵏ≥n; these conditions also suffice for every coefficient tuple. For exactly k common centers, the members xᵏ and 2xᵏ give the same conclusion. Finally, two independent order thresholds agree only when both thresholds agree, so 3j=5 or 2j=5 would be required in the five-blowup examples.

## Scope and limitations

The conclusion is about the specified reference multiple under the explicitly treated source conventions. The intersections with weights (3,5) and (2,5) are themselves maximal divisorial sets for other primitive toric divisors. Allowing a different arbitrary divisor removes this particular obstruction. No result about Conjecture 2 or a solution of the generalized Nash problem is claimed.

Equality is equality of closed sets or reduced supports. It is not equality of nonreduced coefficient schemes. The closures include constant arcs, zero-coordinate arcs and satellite limits.

The claim is tied to the inspected arXiv:1501.06898v3 and 2016 workshop formulations. The v3 source defines a relation with “at least i” shared centers but prints an undefined bare subscripted relation in its conjecture, and its selected-point indexing is inconsistent. No unique author-intended correction, erratum or intended new hypothesis is asserted; the publisher-typeset body is not silently identified with that v3.

The note treats the listed prefix, selected-point, indexing and contact readings explicitly. It does not claim to refute an unspecified replacement of the source conjecture. Historical firstness, continuous openness and completeness of the literature search are not established.

Divisible cases can satisfy the reference equality. Fixing the final center gives a singleton divisor. Varying all tangents gives {ord x≥n,ord y≥n}=Cont̄^n(D₁), a positive boundary rather than a counterexample.

## Prior work

The specified-reference assertion comes from Fernández de Bobadilla, Pe Pereira and Popescu-Pampu, On the generalized Nash problem for smooth germs and adjacencies of curve singularities, in the inspected author v3 (2017), and Pe Pereira’s joint-work contribution to Oberwolfach Reports 46/2016, Conjecture 1 on page 2679. Both inspected displays use an intersection.

The maximal-divisorial/contact framework and toric description are established prior work, including Shihoko Ishii’s Maximal divisorial sets in arc spaces. Combinatorial invariance and finite cylindrical intersections are results of the original authors. The contribution here is the complete free-family computation and its obstruction to the reference ray.

The 2018 survey by Fernández de Bobadilla and Pe Pereira discusses the conjectures in Section 8. That historical discussion does not establish present worldwide openness. The original paper’s journal DOI below is a prior-work reference; this note’s own publication DOI is 10.5281/zenodo.23578599.

## Collaboration

Independent verification of the free-family and arc-closure arguments, a careful comparison with the cited primary formulations, or substantive work toward journal submission would be welcome. Authorship would be discussed in relation to actual contributions.

## Research status

Unrefereed preprint. AI tools were used extensively for mathematical exploration, proof development and reconstruction, exact computation, source review and writing. Internal AI-assisted checks are not independent human peer review, journal acceptance or formal proof-assistant certification.

## Explicit source conventions

| Normalization | Intersection | Reference |
|---|---|---|
| Last-shared-divisor convention; prefix c₁,c₂ | I₅,₂ | D₂ |
| Zero-based p₀=c₁,p₂=c₃; contact at least 2 | I₅,₂ | D₃ |
| Fix the selected free c₃ as well | I₅,₃ | D₃ |
| One-based p₃=c₃; contact at least 3 | I₅,₃ | D₃ |
| Conditional exact contact 2 or 3 | I₅,₂ or I₅,₃ | Every Dⱼ |

## Paper and materials

Read the complete unchanged five-page version 1.0.0 paper below, or open or download its PDF. The complete original ZIP includes the TeX source and authored verification materials. Its README gives optional standard-library reproduction instructions for Python 3.10 or later; the finite diagnostics supplement the universal proof.

The authored manuscript, notes and prose are licensed under CC BY 4.0. Authored software is MIT licensed. Referenced third-party works retain their own rights; the paper’s license does not relicense them.

## Links and citation

[Zenodo DOI](https://doi.org/10.5281/zenodo.23578599) · [Open PDF](candidate/assets/free-chain-nash-intersections.pdf) · [Original source and verification ZIP](candidate/assets/free-chain-nash-intersections-source-and-verification.zip) · [BibTeX](citation.bib)

Kriebel, Alec. (2026). *A free-chain counterexample to a Nash-intersection conjecture* (Version 1.0.0). Zenodo. https://doi.org/10.5281/zenodo.23578599. Unrefereed preprint.

- [Original authors: inspected arXiv:1501.06898v3, pages 30–32](https://arxiv.org/abs/1501.06898v3)
- [Original authors: journal bibliographic DOI; typeset body not equated with inspected v3](https://doi.org/10.1016/j.aim.2017.09.035)
- [Pe Pereira and collaborators: Oberwolfach 46/2016, pages 2678–2681](https://ems.press/content/serial-article-files/46651)
- [Ishii: Maximal divisorial sets in arc spaces, author version](https://arxiv.org/abs/math/0612185)
- [Ishii: published bibliographic DOI](https://doi.org/10.2969/aspm/05010237)
- [Fernández de Bobadilla–Pe Pereira: 2018 survey, Section 8](https://arxiv.org/abs/1805.01418)
