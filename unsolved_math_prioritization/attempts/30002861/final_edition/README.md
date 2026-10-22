# Cubic and quartic spline interpolation: final five-pass mathematical checkpoint

Row 1761, problem 30002861 / OWR-13678-002. Prepared 13 October 2026 UTC.

## Conclusion

The cubic vertex-value assertion is false, by Junkai Qiu's September 2026 [versioned preprint](https://arxiv.org/abs/2609.06364v1). Its exact 41-vertex example, full spline-space dimension 107, evaluation rank 40, and explicit incompatible data are independently verified in the preserved [cubic proof](fourth_edition/third_edition/second_edition/first_edition/CUBIC_PROOF.md) and [audit](fourth_edition/third_edition/second_edition/first_edition/CUBIC_AUDIT.md). The example and obstruction are Qiu's.

The unrestricted quartic value-and-gradient question remains unresolved by this work. **The bundled row remains unsolved.** There are **five newly documented shared substantive passes**; the lifetime total is unknown. The fifth pass is final for this sequence. Branches, audits, corrections, editorial preparation and publication do not add passes. No sixth substantive pass is begun. No novelty, priority, worldwide-openness or external-peer-review claim is made.

Two final accepted results sharpen the remaining question:

- The [canonical-collar and boundary-chord theorem](FIFTH_PASS_BOUNDARY_COMPLETION.md) removes the exterior-placement uncertainty once the exact strict-turn inequalities hold. For a specified convex triangulated disk with the required parity, activity and interior balance, individual forced-exterior boundary equations are a necessary and sufficient finite test for a genuine closed balanced realization. Boundary chords can only form a noncrossing matching of straight boundary vertices on their forced lines; no chord touches a strict corner. Every triangle incident with a boundary edge has an interior vertex opposite that edge.
- The [additive-completion obstruction](FIFTH_PASS_ADDITIVE_OBSTRUCTION.md) proves that the exact fifteen-vertex nonpencil disk from the fourth pass has no convex balanced completion retaining all its old triangles and coordinates, even if its old nonzero weights may be reassigned. Its internal equations fix those weights up to scale, and forced lines at both reflex vertices miss their entire available sectors. This is a theorem about that candidate. Retriangulation, subdivision of old faces, moved vertices and other candidates remain outside its scope.

The construction obstruction supplies neither a quartic counterexample nor a universal quartic interpolation theorem. The finite completion criterion does not supply a disk satisfying all its tests.

## Fixed model and final unresolved statement

A mesh is a finite conforming straight-line triangulation of a polygonal disk. Distinct vertices have distinct geometric positions, every triangle is nondegenerate, and two triangles intersect only in a common face. A quartic spline is globally C1 and has total degree at most four on each original triangle. Values and both Cartesian first derivatives are prescribed independently at every vertex, including boundary vertices. There is no refinement, vertex movement or imposed boundary condition.

The remaining issue is the existence of a finite convex conforming triangulated disk K with:

1. Even interior degrees; even strict-corner induced degrees at least four; odd straight-boundary induced degrees at least five.
2. The strict adjacent-turn inequalities. Writing the strict corners counterclockwise as A_i and e_i=A_(i+1)-A_i, these are det(e_(i-1),e_(i+1))>0. They force the exterior points Q_i specified in the [completion proof](FIFTH_PASS_BOUNDARY_COMPLETION.md).
3. Nonzero endpoint determinant coefficients on every edge of K and a full-support nonzero weighting x_v satisfying a_vw x_v+b_vw x_w=0 on every edge. Interior edges use their two actual old opposite vertices. Every boundary subedge uses its actual old opposite vertex and the forced Q_i of its strict side.

If such a disk exists, its canonical collar gives an actual original mesh and the accepted reduction yields incompatible quartic vertex jets, including suitable pure-gradient data. Conversely, every quartic failure supplies such a balanced closed support. Thus constructing one or excluding all of them decides the quartic question. No such disk or universal exclusion is supplied here. The complete theorem and its precise hypotheses are in [Section 4 of the final theory report](FIFTH_PASS_BOUNDARY_COMPLETION.md#4-a-finite-necessary-and-sufficient-completion-test).

Any prospective example must also satisfy all accepted consequences: at least five strict corners, a proper three-coloring, an even number s of straight boundary vertices, and at least 3+s/2 degree-four interior support vertices with their full original nonsingular stars. With no straight boundary vertices, the strict-corner count is divisible by three and at least six. Three distinct concurrent color lines are already excluded. The boundary-chord matching and forced-line order provide further restrictions. These consequences narrow the target; they are not extra hypotheses silently assumed to settle it.

## Reading the complete progression

The [five-pass progression](PROGRESSION.md) explains what each pass established and what changed. The [accepted dependencies and edition boundaries](DEPENDENCIES.md) link every proof and audit, separate the full eighteen-vertex theorem from the complete nested-ring-core theorem, and preserve the published baseline's status. The corrected fourth edition is retained once, including its already nested earlier editions. Its historical pass counts describe those editions rather than the final total.

The [correction record](CORRECTIONS_AND_SCOPE.md) preserves the incident-segment cofactor correction and the exact fourth-edition phrase correction. It also distinguishes newly accepted conclusions from historical acceptance.

The final [theory acceptance](INDEPENDENT_BOUNDARY_COMPLETION_ACCEPTANCE.md) and [construction acceptance](INDEPENDENT_ADDITIVE_OBSTRUCTION_ACCEPTANCE.md) state their independent mathematical review scope. The [reproduction guide](REPRODUCTION.md), [additive obstruction certificate](ADDITIVE_OBSTRUCTION_CERTIFICATE.json), and [collar certificate](BOUNDARY_COMPLETION_CERTIFICATE.json) give exact conventions and authored finite witnesses. The [content manifest](CONTENT_MANIFEST.json) identifies the included public files; identity is not mathematical proof.

The earlier bounded [source review](fourth_edition/third_edition/second_edition/first_edition/SOURCES.md) and [source metadata](fourth_edition/third_edition/second_edition/first_edition/SOURCE_METADATA.json) remain unchanged. No new literature search or expansion of their inspection limits is claimed.
