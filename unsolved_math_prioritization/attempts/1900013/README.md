# Cubic Klein continued fractions: historical partial result

Status: **PARTIAL** for Karpenkov's historical eight-sail Klein model, with a fixed totally real cubic field and equivalence under GL(3,Z). The complete geometric face and decorated-torus classification remains unresolved by this work.

This is an **unrefereed AI-assisted mathematical exposition**, accompanied by an independent **internal AI mathematical, source, and computational audit**. “Accepted” in the review documents means acceptance within that stated internal scope. No external human peer review, journal acceptance, formal proof-assistant certification, novelty, priority, or exhaustive current-literature-status certification is claimed.

## Proven results and boundaries

The complete proof in PROOF.md and its summary in RESULT.md are preserved verbatim from the accepted manuscript. The eight-sail union determines its three defining planes via the rays that miss the union. These planes recover a rational multiplication algebra and an integral multiplier order. The recovered order's trace discriminant is invariant under integer-linear equivalence.

For every fixed totally real cubic field K, the full lattices Z + f O_K, for positive integers f, have pairwise distinct recovered-order discriminants f^4 disc(K). There are countably infinitely many integer-linearly inequivalent objects in this historical model. Every full lattice is realized by an irreducible integral determinant-one operator with three distinct positive eigenvalues. The exact arithmetic equivalence relation is J = a tau(I), with a in K× and tau a genuine field automorphism.

Every fixed multiplier-order stratum is finite, and only finitely many classes have bounded recovered-order discriminant. The conductor sandwich uses all full lattices, including noninvertible ideals of nonmaximal orders. It must not be replaced by the invertible ideal classes of one chosen order, or by arbitrary permutations of embeddings.

The explicit example has a shared characteristic polynomial t³ − 57t² + 570t − 1 but recovered-order discriminants 81 and 6561. The polynomial discriminant is a different quantity. Independent exact tests support the displayed identities, realization examples, field-automorphism action, and finite quotient calculations; finite testing does not establish the arbitrary-field geometric theorems.

The conductor quotient is a structural reduction. Given a maximal-order basis, complete ideal-class representatives, the conductor, generators for the required unit images, and field automorphisms, it reduces the arithmetic quotient to finite subgroup enumeration and finite orbit computation. This manuscript supplies no turnkey implementation or certification of general class-group and fundamental-unit computations. It gives no full classification of sail faces, angles, adjacency, integer distances, or decorated torus decompositions, and no general combinatorial realizability criterion. It makes no claim about every generalized sail model in the 2017 survey. No mathematical correction to the accepted proof was required.

## Contents

- PROOF.md: complete accepted proof, unchanged.
- RESULT.md: complete accepted result summary, unchanged.
- AUDIT.md: complete substantive mathematical audit, including the geometric recovery proof checks, lattice criterion, realization, conductor reduction, all computational findings, and limitations. Only a final private administrative paragraph is replaced by a source-exclusion sentence, and the internal AI review framing is added.
- ACCEPTANCE.md: complete mathematical acceptance and computational/source-verification findings; private package authentication and operational statements are omitted, and the review framing is added.
- CORRECTIONS.md: no required correction; the optional algorithmic clarification and all mathematical scope guardrails are retained. One private operational sentence is omitted.
- SOURCE_METADATA.json: the candidate's public source identities and recorded inspection metadata, unchanged.
- SOURCE_VERIFICATION.md: the independent audit's source-verification report, with only its closing private-authentication paragraph removed.
- VERIFICATION_SUMMARY.json: the audit's public verification metadata, with four private package-authentication fields removed and the internal AI framing added.
- MANIFEST.json: exact ten-file membership and byte counts/SHA-256 digests of the other nine members. Its own digest is recorded separately to avoid self-reference.

These editorial changes do not alter any mathematical statement, proof inference, computational result, source identity, source-inspection scope, acceptance boundary, or unresolved limitation.

## Sources and verification scope

The historical formulation is [Karpenkov's 2004 Problem 3](https://arxiv.org/pdf/math/0411054), with its eight-sail and integer-linear definitions, and [2017 Problem 13](https://arxiv.org/pdf/1712.01450), whose wider survey setting requires the explicit historical qualification. The number-theoretic dependencies are [Conrad's order-level unit theorem](https://kconrad.math.uconn.edu/blurbs/gradnumthy/unittheorem.pdf) and [Weston's integral-basis and maximal-order ideal theory](https://kconrad.math.uconn.edu/math5230f08/weston.pdf).

The recorded independent audit retrieved all four complete public PDFs, matched their byte counts and SHA-256 hashes, independently extracted their text with exact matches, and visually inspected the stated decisive pages. SOURCE_METADATA.json records the candidate's inspection scope; SOURCE_VERIFICATION.md records the independent audit's scope. Neither implies that every page was read or that current literature was comprehensively searched. Publication preparation performs byte-integrity and package checks; it does not constitute another source retrieval, source inspection, mathematical search, or literature-priority review.

The independent arithmetic rebuild passed in normal, -O, and -OO modes with byte-identical results: 32 conductor cases, 90 unimodular basis/conjugation cases, exact symbolic identities and root checks, a genuine field automorphism, six rejected false arithmetic claims, and exhaustive finite-module tests modulo 2 and 3. The accepted audit explains which full-span subspaces have exact or larger multiplier orders and how the actual units generate the tested finite unit groups. The candidate's arithmetic tests were also replayed successfully during the audit. These are recorded audit findings, not a claim that this publication package includes executable reproduction materials.

The distribution contains authored mathematical prose and public verification/source metadata only. It contains no copied third-party source bodies, dataset contents, executable code, computational certificates, raw data, private sources, private personal data, or private coordination material.
