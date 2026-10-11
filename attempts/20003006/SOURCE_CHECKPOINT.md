# 20003006: exact source gate (before author turn 1)

## Source and category

The original is AIM's *Discrete and combinatorial homotopy theory* workshop list, Digital topology, Problem 1.3, **Topological realization**, following Gregory Lupton's Problem 1.1 on constructing higher groups and Anton Dochtermann's Problem 1.2 on loop spaces. The workshop took place March 13–17, 2023. The source asks for a functor from digital images to topological spaces realizing their invariants, with higher homotopy groups as the example; it explicitly assumes those higher groups have been constructed. The live page still labels it open. The imported title mentioning clique and cubical nerves is a later descriptive title, not the original question.

Primary page: http://aimpl.org/combhomotop/1/ . A full HTTP response was read on 2026-10-01; the HTTPS endpoint returned 502. No login or access-control bypass was involved. The source does not specify a unique list of homology theories or impose a single higher-group definition.

For the Lupton–Oprea–Scoville / Lupton–Musin–Scoville–Staecker–Treviño-Marroquín program, digital images are finite reflexive symmetric graphs (with digital lattice realizations), maps preserve adjacency and may collapse edges. Products have **categorical/strong** adjacency: all coordinate pairs must be adjacent. Thus a unit n-cube is a clique on 2^n vertices. Homotopies are maps on the categorical product with a finite interval. This differs from the box-product convention of A-theory and of much older digital topology.

## Verified literature and precise limitations

1. Lupton–Scoville, *Digital Fundamental Groups and Edge Groups of Clique Complexes*, published 2022, author preprint arXiv:1910.08189v1, Theorem 4.6: the subdivision-based digital fundamental group is the edge group of the clique complex. Theorem 4.4 supplies the classical realization comparison.
2. Lupton et al., *A Second Homotopy Group for Digital Images*, published 2024, DOI 10.1007/s10801-024-01352-9. Definitions 2.1–2.3, 2.9 and 4.1 fix finite images, strong homotopy, rectangular basepoint extension and digital pi_2. Its first page explicitly credits working sessions at this same AIM workshop.
3. Lupton–Scoville–Staecker, *The Face Group of a Simplicial Complex*, arXiv:2503.23651v2 (21 May 2025), Theorem 8.1 proves the face-group realization comparison. Section 9 announces the digital pi_2 comparison, postpones its proof, and describes the rectangular all-degree extension as future work. Its bracketed citation for digital pi_2 points to [8], while the actual second-group paper is [9]; we identify the paper by title and definition rather than inheriting that cross-reference typo.
4. Grandis, *An intrinsic homotopy theory for simplicial complexes, with applications to image analysis*, Applied Categorical Structures 10 (2002), 99–155, DOI 10.1023/A:1014326730784; complete arXiv:math/0009166v1 read. Sections 2.1–2.8 and 6.2 use finite-support integer nets with categorical products, delays and fixed-face homotopies. Theorem 6.6 (author version pp. 39–40) gives a natural realization isomorphism in every degree. The finite-rectangle versus integer-net comparison still has to be proved before using this as an exact answer for the chosen digital model.
5. Lupton–Scott, *The Simplicial Loop Space of a Simplicial Complex*, arXiv:2504.11223v2 (16 July 2025), Theorem 8.3 gives a realization/loop-space equivalence, relying on Stone. The introduction acknowledges Grandis and distinguishes their finite-path model. This is background, not a substitute for the exact grid comparison.
6. Carranza–Kapulkin, *Cubical setting for discrete homotopy theory, revisited*, Compositio Mathematica 160 (2024), 2856–2903; current arXiv:2202.03516v3 revised 20 December 2025. Theorem 5.1 realizes the A-groups by the one-nerve; this is a separate box-product theory. Their arXiv:2602.19293v1 (February 2026) extends the A-theory homotopy hypothesis to n-types. Neither paper identifies the strong digital groups with A-groups.
7. Milićević–Scoville, *A McCord-type theorem for pseudotopological spaces and directed graphs*, JACT 10, article 14 (29 June 2026), DOI 10.1007/s41468-026-00246-y. Theorem 24 realizes closure-space homotopy groups, and Theorem 21 transfers their singular homology. **Example 2 still conjectures comparison with all higher digital groups.** Its result alone cannot be promoted to the answer for the present strong-grid conventions.

## Prior campaign gate

All-state GitHub PR searches for 20003006 and AIM-TOPOLOGY-0094 returned zero; both possible target-path commit histories were empty; the dedicated branch did not exist. The local all-ref target history and related-target list likewise had no entry. The upstream imported partial research report is not an earlier Alec/campaign attempt, and is treated as an unreviewed lead only. Current source work consumes zero substantive author turns.

## Research target

Check whether Grandis's integer-supported groups are naturally identical to the all-degree extension-homotopy construction using finite strong rectangles, including negative support, a common finite homotopy box, delays, boundary collars and group operations. Then verify degree 1 against the published subdivision model and degree 2 against the published rectangular model. A realization theorem for this specified model does not, by itself, identify every incompatible invariant called digital in the literature.

No source PDFs, extracted full texts, page images or full imported records belong to the public packet. No new discovery or maximal convention-independent result is claimed.
