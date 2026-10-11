# Acceptance report for Fuchs Conjectures 2.3 and 2.4

Audit date: October 11, 2026, UTC.

The existing proofs are attributed to Alper Ferudun's version 1.0 manuscript dated October 9, 2026, an unrefereed AI-assisted preprint. Acceptance here is an independent internal AI audit judgment, not external human peer review, journal acceptance, formal proof-assistant certification, or a claim of new authorship, novelty or mathematical consensus.

The complete authored mathematical arguments, formulas and analytical constructions of both audits are retained. This is not a computational reproduction package: executable code, raw datasets or certificate tables, copied source PDFs/text/images, and private coordination material are not distributed. Historical finite checks are supplementary evidence; the all-n results rest on the written geometric arguments. Those historical computations cannot be reproduced from this edition alone.

Statements about source inspection and mathematical executions below describe the original audits, not new inspection or executions during preparation of this public review edition. The original audit documents remain unchanged. The first full audit is PROOF.md; the complete focused geometric acceptance is AUDIT.md.

## Target 5000002 / AMR-049-0002

Attribution: Ferudun, version 1.0, October 9, 2026, Theorem D.

Decision: the existing proof passes this audit and proves the exact type pattern in Fuchs Conjecture 2.3 for every n>=5. The stronger four-vertex criterion also passes. Fuchs's original n=6 proof is valid prior work.

## Target 5000003 / AMR-049-0003

Attribution: Ferudun, version 1.0, October 9, 2026, Theorem F.

Decision: the existing proof passes this audit and refutes both the “at least one” and “infinitely many” formulations for every n>=5. A_0 points lie on infinitely many reachable polygons; the other types lie on at most one. The explicit reachable point 2+3zeta+zeta^2 lies on none. Its n=6 instance is (5,4) in Fuchs's basis, with an exact elementary obstruction using the published lattice formulas.

## Conditions that must remain visible

- Types use the source's angle definitions, segment parity and diagonal convention together. The isolated A_0 difference-angle shortcut is not valid for all short trajectories.
- The original odd-n first-case upper bound is retained: its extra indices have no admissible nonnegative angle, so the purported typo does not change the classification.
- Reachable polygons are linear SL(2,R) images fixing the distinguished origin, in the normalized sector. Translated polygons are outside scope.
- Fuchs's paragraph headed as a proof of 2.4/2.5 for n=6 only addresses lines through A_0 unitary pairs. It gives step 3 and offset 2 and does not imply the asserted universal existence statement.
- The mathematical audit accepts the arguments. Ferudun's publication remains an unrefereed, AI-assisted preprint; no peer-review or community-acceptance claim is made.
- The accepted scope is Theorems D and F and their named dependencies. This does not accept all seven conjectures, Theorem E, later manuscript versions, translated polygons, or the n=3,4 cases.

The complete first logical audit is retained as PROOF.md. The separate focused geometric audit is retained as AUDIT.md, including its stronger n=6 lattice obstruction that does not depend on the angular-type convention or the all-n theorem. Both original audits accept the existing arguments without a mathematical correction. SOURCES.json distinguishes their source-inspection histories. The checked manuscript PDF is 380876 bytes, SHA-256 ff6b9ba5f9bac0027a39d6e06319f04ff08bf24776a47cf7070213924d454707.

## Complete retained dependencies and geometric argument

The acceptance includes Lemmas 2.1-2.12 and Theorem A as dependencies, Lemma 4.1 and all five steps of Theorem D, and Lemma 6.1 with both endpoint cases k=1 and k=n-3 and all three parts of Theorem F. The gluing, cone corners, B winding and common-offset invariant, boundary-side occurrences, triangular cylinder degeneracies, full-height crossing argument, twist gluing and finite-length descent are explicit. The four-vertex reduction, second-cylinder contradiction for every n>=5, exact endpoint-family selection, derivative reconstruction and distinguished initial-corner restriction are retained. Infinitude for A_0 includes the boundary ray. Uniqueness for other types derives the same integer on both sides from a c_1=b c_2 and treats its two boundary cases. The explicit all-n obstruction retains its actual ray tracking, three-segment geometric development, exact matrices, and incompatible integer inequalities.

## Independent original-lattice refutation

For n=6 the reachable point (5,4), in Fuchs's original xi/eta basis, lies on no fixed-origin reachable hexagon. This is stronger evidence than merely classifying its type. Side vectors u,v have determinant one; reachability of the middle vertex forces both side coordinate sums to equal 1 modulo 3, so (5,4), with sum 0, cannot occupy a side position. Its odd first coordinate excludes the middle vertex. At v+2u, the equation 4a-5b=1 has no solution in 0<=a,b<=2. At 2v+u, the only determinant-one nonnegative candidate is v=(1,1),u=(3,2), and both fail the tile-vertex sum restriction. AUDIT.md contains the full argument. This refutes the universal bare-existence claim independently of D, F, double-polygon machinery, or any resolution of the A_0 shortcut.

## Source defects and scope

The isolated A_0 difference-angle shortcut conflicts with the source's one-segment diagonal labels. Segment parity plus those explicit labels gives the coherent classification used here. The printed eta coordinate has an isolated horizontal-sign inconsistency with the actual side and n=6 basis. The odd-n first-case upper bound needs no amendment: its extra indices have impossible negative angle upper bounds. The n=6 paragraph headed as proofs of 2.4/2.5 addresses lines through A_0 unitary pairs; it does not construct a polygon through every reachable point. Its step 3 and offset 2 differ from the printed lambda+1 and lambda. These observations do not assert an all-n acceptance of Theorem E. Fuchs's separate n=6 proof of Conjecture 2.3 remains valid prior work.

## Historical verification limits

The first audit's exact checks cover 125070 angle cells for n=5..64, symbolic identities, the justified complete n=6 witness bounds, and four mathematical negative controls. The focused audit adds 18220 checks per Python mode, including exact corner/parity bookkeeping for n=5..80, exact witness matrices and rational identities, complete bounded n=6 enumeration, and finite numerical geometry for n=5..40,64,100,257,1000. These finite tests are not an all-n proof or formal geometric certification. Normal, -O and -OO receipts are separately identified in VERIFICATION.json; no mathematical program was rerun during publication preparation.
