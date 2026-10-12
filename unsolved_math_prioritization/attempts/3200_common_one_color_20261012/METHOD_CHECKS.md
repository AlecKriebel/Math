# Complementary matching checks and their limits

This complement is part of the same fifth and final research round. The complete mathematical text is in METHODS.md and the full substantive independent audit is in AUDIT_METHODS.md. These checks are distinct from the primary seven-fixture suite: here the last fixture has 25 vertices and 37 edges, replacing the primary suite's nine-vertex, thirteen-edge fixture. Counts from the two suites overlap and must not be added as disjoint coverage.

The author exhaustively scanned all labeled ordinary deletion colorings and admissible labels. Its separate certificate verifier did not itself re-enumerate all colorings. The independent mathematical auditor did independently re-enumerate them all, reconstruct the triangle-port expansion, enumerate all covering matchings and compare every recorded bounded census. No search cutoff, random sampling or timeout-to-impossibility inference was used.

## Complete numerical strata

For each stratum, the fields are vertices/edges; labeled deletion colorings; admissible color-class instances; distinct critical cycles; all degree-three-covering matchings; incident-edge stored-cycle-pair checks; stored first-deletion witnesses; and histogram of covering matchings by number of odd residual components.
- Stratum 0: 5/7; 48; 60; 2; 2; 24; 7; 1 odd: 2.
- Stratum 1: 7/10; 96; 120; 3; 3; 51; 10; 1 odd: 3.
- Stratum 2: 7/10; 108; 120; 3; 3; 53; 10; 1 odd: 3.
- Stratum 3: 7/10; 72; 84; 2; 2; 34; 10; 1 odd: 2.
- Stratum 4: 7/10; 144; 168; 4; 4; 140; 10; 1 odd: 4.
- Stratum 5: 9/12; 360; 468; 8; 8; 336; 12; 1 odd: 8.
- Stratum 6: 25/37; 864; 888; 8; 16; 636; 37; 1 odd: 12, 3 odd: 4.

Totals are 1,692 labeled deletion colorings, 1,908 admissible color-class instances, 30 distinct critical-cycle witnesses, 38 covering matchings, 1,274 incident-edge cycle-pair checks and 96 stored first-deletion witnesses. The expanded graph also has 37 separately stored deletion witnesses. Six fixtures are overfull; the Petersen-minus-one-vertex fixture is independently non-three-colorable and has an exhaustively checked 232-node, 36-dead-end negative decision tree.

The expanded graph has 25 vertices, 37 edges and 24 degree-three vertices. Its exhibited covering matching has 12 edges and residual cycle lengths 3,3,19. Among all 16 covering matchings, 12 leave one odd cycle and four leave three odd cycles. The special deletion-color-class construction supplies eight distinct cycles: four triangles and four Hamilton cycles. The family is connected under edge intersection even though the triangles are pairwise edge-disjoint.

On the seven-edge fixture, all 2,187 common-zero four-palette list assignments are tested with both covering matchings, giving 4,374 pairs. Exactly 3, 48 and 2,136 assignments have respectively zero, one and two successful matchings; the three failures are precisely the constant assignments. The complete positive vector for the nonconstant one-common-color example is (2,1,1,0,0,3,2), with its ordered graph and lists fully stated in METHODS.md and AUDIT_METHODS.md.

There are 3,267 exhaustive two-list path cases and 3,267 exhaustive two-list cycle cases at lengths three through seven. On the actual three-odd-cycle example, making zero, one or two residual odd components nonconstant fails the fixed-matching strategy; making all three nonconstant succeeds. This is a fixed-matching criterion, not general list uncolorability.

## Modes, controls and reproduction

The independent auditor ran normal Python, -O and -OO with identical results. All four author programs were independently replayed in each mode, for 12 executions, and every generated result exactly matched its frozen original. Twenty-seven fail-closed corruption controls in each mode gave 81 rejections. The complete audit preserves the control categories and the distinction between semantic checks and digest checks. The private audit also verified original input inventory and immutable pins; those excluded-input identities are not distributed.

The symbolic theorem, matching criterion and connectivity argument do not depend on a finite census. The explicit negative examples were validated by exact finite computation, with construction details retained in prose. Raw graph/fixture/certificate/coloring collections, all deletion-coloring and cycle witnesses, implementations and run outputs are excluded. The raw records cannot be reconstructed or computational suites rerun from this prose alone. Fresh implementation and fresh input generation are required. No mathematical suite was rerun during edition preparation.
