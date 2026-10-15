# Independent source-first record

Recorded before reading CURRENT_PROOF_V4, publication_package_v1, review inputs, Root gates, or earlier review verdicts. The assignment itself disclosed the intended credited scope and listed mathematical attack areas; this is source-first independence, not ignorance of the task description.

## Sources actually inspected
ROOT_EXACT_UPSTREAM_TARGET_01.json in full; full-page visual Fuchs printed pp.501–506 and510–512, including Figs6–9,13–14 and both type tables (504–505,511). No supplied solution has yet been opened.

## Claim and conventions
Regular n-gon n>=3 has O at a vertex, lower adjacent side on positive x-axis, interior sector 0<=alpha<=(n-2)pi/n. A short trajectory ends at the FIRST vertex and has no vertex in its interior; development is a chain of reflected polygons. Endpoint angle beta is the angle drawn in Fig8, not a freely reduced direction. Types are residues modulo N=n-2; n=3 therefore has one type. Fig9 gives A_k for chord OX_(k+1), k=0,...,N, including both side representations k=0 and k=N for the same residue. A0 means beta-alpha=2pi/n. N in the sentence before Def2.1 is the number of polygonal segments, so its even/odd sign statement must not be identified silently with the number of reflections (one fewer). For even n, only even ell is allowed.

The target is: for every existing short trajectory of type A_k and slope alpha, every transformed actual admissible unwrapped angle alpha'=ell*pi/n+epsilon*alpha has a parallel first-hit short trajectory, of type A_(epsilon*k-ell). Angles outside [0,N*pi/n] are not rays in the original polygon and cannot be made admissible just by residue reduction. Existence in each parallel germ is part of the result, not justified by endpoint bookkeeping alone. Original source pp510–511 motivates finite slope families from a small seed interval. Boundary slopes and coincidences need a consistent interpretation.

## Source quirks / potential gaps to test
Fuchs odd-n first inequality on503 visibly says k<=m+1, while the following conditions and tables encode the admissible branches; cannot call this an author-authenticated correction. Need exact equivalence on REAL angle pairs, including equality branch overlaps. Tables at504–505 present branch cutoffs, not evidence of existence. The even hexagon proof printed511–512 gives arithmetic examples; a p.511 type label and p.512 modulus visibly invite checking rather than blind reuse. Length-ratio Conj2.7 is separate and not the imported target.

## Independent test plan
1. Derive a robust type encoding from endpoint-angle branches with reflection parity and unwrapped sector, and verify residues for all actual branches, both sides and n=3,4,6.
2. Seek counterexamples in first-return/existence: nonperiodic parallel germ despite another saddle connection, unequal germ lengths, two cones unsynchronized for n=2 mod4, regular marked vertices and torus cases.
3. A positive route would require a verified global mechanism, e.g. lattice-surface periodic decomposition plus an affine involution controlling vertex germs. Matching a few polygon diagonals cannot establish universality.
4. Audit any reduction of a saddle connection to a model direction for finite termination and equality cases; do not accept an equivalent unproved orbit classification. On actual even double, establish cylinder shear constants simultaneously and check full affine, not derivative-only, commutation.
5. Check endpoint arithmetic modulo 2N before any division by2. Confirm model first hits independently of a supposed endpoint reflection identity.
6. Check every imported theorem from actual bodies and distinguish stable/current versions, limitations, priority and date evidence. A fixed-byte current retrieval does not establish historical awareness or priority.
7. Inspect frozen manuscript all pages, TeX reproduction, ZIP safety/privacy/inventory and hardened verifier under both ordinary/optimized modes plus mutations. Computational finite checks remain controls, not analytic proof.

## Current judgment
OPEN pending proof/package/source dependency audit. No universal proof or counterexample has been established from the source alone. The imported statement matches Conj2.6 with the even-ell restriction; its imported open-status flag cannot be adopted as present fact. Estimated completion toward this whole-package review: 12%.
