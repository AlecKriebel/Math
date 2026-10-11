# Acceptance report: representation-sphere closure

Problem 20000157 · AIM Problem 2.5 · 11 October 2026

## Decision

Accept the full [proof](PROOF.md) and [mathematical audit](AUDIT.md) as a **partial result**, under the finite-group, genuine-equivariant, complete-universe, compact and ordinary-thick conventions stated there. Acceptance here records an AI-assisted mathematical review. It is not independent human referee review, formal proof-assistant certification or acceptance by a journal.

## Accepted mathematics

1. **Equality criterion, Theorem A.** Both the actual-representation-sphere closure and the RO(G)-sphere closure are the entire compact genuine category if and only if G is an elementary abelian 2-group, including the trivial group. For every other finite group, the free orbit is excluded by its rational regular representation.
2. **Complete rational closure, Theorem B.** In each subgroup-conjugacy factor H with Weyl group W_H, the closure consists of finite sums and retracts of integer shifts of the rational orientation lines det(alpha^H) realized by global virtual representations alpha. The compact rational algebraic model and semisimplicity justify both inclusions. Actual and virtual generators yield the same rational closure.
3. **Rationally invisible obstruction, Proposition C.** For a finite group outside the elementary abelian 2-case, smash its free orbit with the mod-ell Moore spectrum, where ell is odd and does not divide the group order. This compact object is rationally zero but lies in neither integral closure. Its mod-ell regular homology supplies the obstruction.
4. **Internal smash lemma.** Each closure is closed under smashing two of its own objects, by a two-stage thick-closure argument starting from the sphere generators. This is not tensor-ideal closure under arbitrary compact spectra.
5. **Exact orbit criterion, Proposition D.** G/H-plus belongs to either integral closure if and only if H is normal and G/H is elementary abelian of exponent two. The necessity uses the faithful transitive action image of its rational permutation module; sufficiency uses quotient sign characters, Euler triangles and the proved internal smash lemma.

The equality criterion and rational description were present in the inherited result. The other conclusions are elementary consequences established in this audit. No novelty or priority claim accompanies any of them.

## External dependencies retained

- Barnes, *Classifying Rational G-Spectra for Finite G*: rational algebraic model and rational Burnside-idempotent factor isolation. The inspected source is arXiv:0812.0317v1, with publication in Homology, Homotopy and Applications 11(1) (2009), 141–170.
- Greenlees and Quigley, *Ranks of RO(G)-graded stable homotopy groups of spheres for finite groups G*: geometric-fixed-point invariants and fixed-space determinant lines. The published 2023 version is used, including the hypothesis in Theorem 2.1 that both objects are rational and the orientation discussion in Sections 3.2–3.3. The 2022 preprint pin is retained as version provenance.
- Mathew, Naumann and Noel, *Nilpotence and descent in equivariant stable homotopy theory*: complete-universe genuine-category conventions and compact orbit generators, using Definition 5.10 and Example 5.11 on page 25 of the inspected 2015 author version. The work was published in Advances in Mathematics 305 (2017), 994–1084.

Exact public URLs, source identities and inspection limits are in [PUBLIC_SOURCE_METADATA.json](PUBLIC_SOURCE_METADATA.json). The imported papers' entire proofs are not re-proved or certified by this packet. Standard Maschke semisimplicity, genuine-spectral constructions and semisimple derived-category facts are used as stated in the proof.

## Exact remaining gap

For non-elementary-abelian finite groups, a necessary-and-sufficient integral membership criterion for arbitrary compact genuine spectra remains unproved here. The rational factorwise criterion is sufficient within the rational compact category, not integrally. Neither all torsion cases nor the effects of integral lattices and attaching maps are classified. Equality of actual and virtual integral closures for every such group is not established.

The unrestricted AIM question is not declared solved. No classification is given for compact Lie, profinite, naive-equivariant or other group-category interpretations. Compact Lie orbit compactness is not the obstruction; the finite rational factor model and related arguments do not simply extend. The remaining-gap statements describe the limits of this report, not an exhaustive claim about the contemporary literature.

## Verification and binding

The complete mathematical body of the proof, including Section 6, and all protected mathematical audit regions are byte-identical to their accepted originals. Every editorial replacement is enumerated in [EDITORIAL_PROVENANCE.json](EDITORIAL_PROVENANCE.json). [ACCEPTANCE_SCOPE.json](ACCEPTANCE_SCOPE.json) binds those public bytes to the accepted original proof, audit and audit manifest.

The frozen eight-file audit and 81-file supporting input inventory match their seals. All five inspected source captures match their recorded sizes and SHA-256 hashes. The finite checks pass identically in normal, -O and -OO modes: sign-cell models through quotient rank eight, elementary character checks through rank four, four regular-module witnesses, all 37 subgroups in five test groups, 26 admitted orbit-product bijections, and 289 determinant-parity pairs. Three mathematical negative controls are rejected. These are finite sanity checks, not proof of the general statements or formal certification.

Only authored reports and public verification metadata are included. No source documents, source extractions, dataset contents, raw group/subgroup/face data, executable scripts or private coordination material accompany the public packet.
