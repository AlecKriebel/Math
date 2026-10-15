# Independent full review request: k404 / 5100022

This is a one-turn full source-target candidate. Please audit the entire proof and source scope independently. No author file will change during review; record flaws before suggesting repairs.

## Exact original target

Both arXiv v11 Table 5 p. 7 and the published Table 5 p. 348 ask for the signed ratio A_F^*/A_F at either original focus, for N=2 modulo 4. Both polygons come from the original orbit: the antipedal uses lines through its vertices perpendicular to focal rays; the pedal uses feet on its side lines. The source's strict confocal ellipse pair and least-period/star conventions are material.

## Main attacks

1. Derive the antipedal formula from the actual two line equations, including the determinant (7), and retain the correct phase u=w+v. Check normalization by the caustic semimajor axis and the focal distance k.
2. Audit completeness and orders of its complex poles. In particular, apparent common Jacobi poles must be removable, zeros of L must be exactly the two adjacent-vertex translates and simple, and the area must have no poles outside their cyclic orbit.
3. Check all real/imaginary characters, reflection and traversal signs, focus switching, primitive even half-turn and Bezout quotient lattice. The odd Laurent conclusion at iK' is essential: do not accept unsupported cancellation of adjacent double poles.
4. Verify residue matching on the quotient torus, two equal nonzero residues of the dn trace and the elimination of the remaining holomorphic constant by anti-periodicity. A zero antipedal residue/identically zero numerator must remain allowed.
5. Recheck the focal pedal formula, its double-pole-to-simple-area argument, noncollision of neighbors, exact phase shift and 2-modulo-4 alignment. The earlier pedal-trace input is credited and its needed specialization is fully reproduced.
6. Challenge the strict positivity proof for every primitive star, not just convex orbits. It must use the lifted contact-normal angle and focus-inside-caustic hypothesis, with the closing edge handled. Finite antipedal vertices do not imply a nonzero numerator, and no such assertion is made.
7. Inspect both source editions and the exact Stachel input. Distinguish this original focal target from outer pedal, antipedal-focus equality and neighboring source rows. No novelty claim is requested.
8. Replay the author checker and add independently constructed controls, including complex poles, negative parity, different winding classes and any suspected zero/pole exception. Numerical controls alone cannot establish the theorem.

FROZEN_MANIFEST.json binds the portable author files. The three source PDFs/text and two table images are in the workspace's sources directory and excluded from publication; source_manifest.json gives their hashes and links. The checker uses installed sympy and mpmath and writes a deterministic JSON receipt.

Please return an exact-version verdict and any mandatory correction. A full source/domain PASS, rather than only an algebra replay, is required before publication.
