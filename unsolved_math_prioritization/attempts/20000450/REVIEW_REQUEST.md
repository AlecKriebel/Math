# Independent full review requested: 20000450

This candidate is frozen after one genuine substantive author turn. Source retrieval and imported-report inspection preceded that turn. Start with FINAL_RESULT.md and TURN_1.md; the exact source and primary dependencies are recorded in SOURCE_GATE.md and SOURCE_THEORY.md.

Please audit the full original compute-5-torsion target, not just the infinity line. Highest-risk points:

1. Match the source's affine pencil to the homogeneous side-line product, chosen field K=Q(sqrt(5)), scaling and origin. The source omits these conventions; the result must not imply a field-independent rational-torsion statement.
2. Verify the quotient square cancellation, birational cubic coordinates and origin correspondence. All denominator-zero points are handled on smooth projective normalizations, not by evaluating undefined affine formulas.
3. Check the exact discriminant and every excluded parameter. The additional cuspidal plane-vertex parameter still has elliptic normalization and is intentionally included.
4. Verify the actual quadratic-twist isomorphism, including signs and scalings, rather than accepting the j-invariant calculation alone.
5. Reconstruct the fifth-division polynomial and check the ten remaining x-roots and paired y-values account for exactly the other twenty torsion points.
6. Most importantly, check the primary Fisher Lemma 3.4 full-level cover, its geometric base change to K(zeta_5), absence of pointed automorphisms, and its finite étale specialization fibers. The exact field equality must hold on every noncuspidal fiber, not merely be a sufficient splitting extension or a generic equality.
7. Check the Kummer class, required quadratic/cyclotomic subfields, degree-four versus degree-twenty criterion, Galois matrices and rational-torsion claims. Do not infer a split Galois extension merely from the two composition factors.
8. Preserve the distinction between the normalized curve with a rational origin and arbitrary arithmetic twists or the Tate–Shafarevich motivation. Historical novelty is unestablished.

Local-only primary sources are in the author's source directory: qptsurface2.pdf (printed p.51, version 2004 of the 2002 workshop), fisher_jems.pdf (printed pp.172–173 and 194–195), and their rendered images/text. The complete imported report is also there. They are excluded from the public author packet. The sole public checker verify_turn1.py is self-contained and uses SymPy plus the standard library.

All public files are bound by AUTHOR_MANIFEST.json. No final disposition or new author turn should be inferred before the full audit.
