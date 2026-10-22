# Logarithmic deletion in higher dimension: scoped investigation

Problem 30003081 / OWR-14222-009, queue rank 992. Research date: 7 October 2026.

**Disposition: unresolved, five substantive approaches used.** The primary question has a source mismatch in the catalogue. A natural unrestricted short exact sequence is false; conditional exactness and defect criteria are proved. These are substantially AI-assisted, unrefereed notes, with no novelty, independent-audit or human-peer-review claim.

## 1. The actual target

The official OWR report, printed pp. 687–689, presents Schenck's logarithmic-vector-field contribution. Its Theorem 1 concerns deletion of a smooth curve from a locally quasihomogeneous arrangement on P^2:

0 -> D(A)(-C) -> D(A+C) -> O_C(-K_C-R) -> 0,
where R is the reduced intersection and D denotes the actual logarithmic tangent sheaf. Question 1 ends: “Is it possible to prove a higher dimensional version of Theorem 1 using these methods?” The preceding context identifies logarithmic Chern classes, Chern–Schwartz–MacPherson classes and the Segre class of the Jacobian scheme as those methods.

The catalogue's unexpected-curve characterization and multiplicity-index wording are not in that question. Related plane-curve results occur elsewhere in the report, notably Migliore's pp. 680–683 contribution. This investigation follows the primary deletion question and treats unexpected hypersurfaces separately. No source dataset or queue fields were edited.

## 2. Results and their exact scope

1. [Product/SNC case](APPROACH_1.md): the natural quotient in dimension n is D_H(R), of rank n-1, and the deletion sequence is exact in explicit product coordinates. The original line bundle describes the one-dimensional section case.
2. [Credited counterexample](APPROACH_2.md): in P^3 the seven-plane arrangement of Abe–Kawanoue has a logarithmic section field x(x-y) partial_x that does not lift. An elementary homogeneous-degree-two argument proves the obstruction at a projective point. Smooth components and local quasihomogeneity alone do not give the natural short exact sequence.
3. [Local defect](APPROACH_3.md): lifting is obstructed by an explicitly defined class in z-torsion of the Tjurina module of the deletion. Its image is exactly the restriction cokernel. A non-zero-divisor cut is sufficient, not necessary, for exactness.
4. [Characteristic-class test](APPROACH_4.md): on P^n, the full Chern-character defect of the three specified sheaves vanishes exactly when restriction is surjective. This uses the constructed map, GRR and Hilbert positivity. Low Chern data alone can miss a skyscraper defect.
5. [Homological criterion](APPROACH_5.md): local freeness of both ambient logarithmic sheaves, together with codimension-one surjectivity, promotes exactness everywhere by depth and reflexive extension.

These are five distinct routes: coordinates; a homogeneous-jet countermodel; Jacobian algebra; characteristic classes; and depth/reflexivity. The general request for a satisfactory higher-dimensional theorem derived by the proposed Chern/Segre methods is not completed. The counterexample excludes one explicit blanket formulation, not all meaningful analogues.

## 3. Subsequent literature and the separate unexpected-hypersurface issue

Abe–Denham's revised 2026 paper establishes free-surjection and defect results for hyperplane multiarrangements, including an Ext continuation of the Euler sequence. This is credited progress in the relevant direction, but does not cover arbitrary smooth hypersurface components under quasihomogeneity alone.

Trok's 2020 preprint gives a duality for a finite point set Z in P^n and a general codimension-two linear space Q. Its Corollary 4.15 identifies

dim[I_Z intersect I_Q^(d-1)]_d = sum_i max(0,d-a_i),

where (a_1,...,a_n) is the generic-line splitting type of the reduced logarithmic derivation sheaf of the dual arrangement. This is an imported theorem, not independently proved in full here. For d>=1, elementary monomial counting gives dim[I_Q^(d-1)]_d=nd+1. Hence, conditional on that duality, ordinary unexpectedness for this Q is equivalent to

sum_i max(0,d-a_i) > max(0, h^0(I_Z(d)) - binom(n+d,n) + nd+1).

Thus the catalogue's broad suggestion of a connection already has substantial credited content. It is essential that Q has codimension two. For n>2 it is not a general point: in P^3 a double line imposes ten cubic conditions whereas a double point imposes four. Trok's stronger 'very unexpected' notion and its matroid classification are not substituted for ordinary fat-point unexpectedness. We do not rely on his Theorem 5.27; its displayed inequality and subsequent dimension-count bound have opposite directions in the inspected v1, and that later argument has not been audited here.

The 2025 Janasz–Malara–Tutaj-Gasińska preprint develops higher-order syzygy constructions with multiplicity along a general codimension-two space. Its stated sufficient criterion is relevant subsequent progress, not a verified unrestricted equivalence or a solution of Schenck's deletion question. The selected HTML sections, not its entire proof, were inspected.

## 4. Verification and limitations

The source-free packet includes all authored proofs, five-route chronology, source/gate qualification, rational finite diagnostics and strict integrity controls. The finite program checks the seven-plane restriction profile through degree five, product controls, 35 monomial counts and a point's Chern character. It supports the proofs but does not establish their universal geometry or certify literature completeness.

Only exact read-only source/gate checks were made remotely. No queue mutation, branch creation, commit, push, PR, publication or outside communication occurred in this research task. This is an authored research packet awaiting independent review, not an acceptance report.
