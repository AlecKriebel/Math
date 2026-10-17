# Cubic and quartic spline interpolation third mathematical edition

Row 1761, problem 30002861 / OWR-13678-002. Prepared 13 October 2026 UTC.

## Result and status

Every admissible realization of the specified eighteen-vertex, twenty-eight-triangle topology admits arbitrary quartic vertex first jets. This strengthens the earlier symmetric-family exclusion to the full nonsymmetric topology. Separately, no balanced closed core consists of the specified central six-vertex triangulation followed by any positive number of complete six-vertex rings, with either annulus orientation chosen independently at each layer.

The unrestricted quartic value-and-gradient assertion remains unresolved by this work. The cubic vertex-value assertion has a negative answer credited to Junkai Qiu's September 2026 preprint, as explained in the unchanged [first edition](second_edition/first_edition/README.md). **The bundled row remains unsolved.** No novelty or priority claim is made.

There are exactly **three newly documented substantive passes** in this sequence; the lifetime total is unknown. The pencil-collapse proof, nested-ring extension, cofactor analysis, and their independent audits are branches of the same third pass. Editorial preparation, correction, and publication do not add passes.

## Fixed mathematical model

A mesh is a finite conforming straight-line triangulation of a polygonal disk. Distinct mesh vertices have distinct geometric positions; every original triangle is nondegenerate. The desired quartic interpolant is globally C1 and polynomial of total degree at most four on each original triangle. Values and both first derivatives are independently prescribed at every vertex, including boundary vertices. No refinement, moved vertices, extra smoothness, or boundary condition is introduced.

The accepted reduction is Rm=Hj. A nonzero left dependency is supported on a closed balanced active component. Its induced support is convex and contains at least three original nonsingular degree-four interior vertices. The second-pass theorem shows that every such balanced component produces an actual quartic obstruction, even for a suitable pure-gradient datum. These are dependencies, not conclusions newly assumed from the third-pass examples. Their exact accepted texts are linked in [DEPENDENCIES.md](DEPENDENCIES.md).

## Reader guide

1. [THIRD_PASS_CEVA_OBSTRUCTION.md](THIRD_PASS_CEVA_OBSTRUCTION.md) proves the exact homogeneous pencil collapse of the twelve-vertex core and the boundary-sign contradiction. Its final component argument covers every possible closed component of the complete eighteen-vertex topology, including singular four-star cases. [INDEPENDENT_RING_ACCEPTANCE.md](INDEPENDENT_RING_ACCEPTANCE.md) verifies all algebraic divisions, actual exterior triangles, the finite concurrence argument, and the full-topology quantifier.
2. [THIRD_PASS_NESTED_RING_EXTENSION.md](THIRD_PASS_NESTED_RING_EXTENSION.md) propagates the same coefficient-one pencil form across any finite sequence of forward/reverse annuli. [INDEPENDENT_NESTED_RING_ACCEPTANCE.md](INDEPENDENT_NESTED_RING_ACCEPTANCE.md) checks distinctness factors, zero intermediate coefficients, both orientations, and the induction. This concerns complete closed-core topologies, not every component of every larger full mesh.
3. [COFACTOR_NORMAL_FORM.md](COFACTOR_NORMAL_FORM.md) characterizes the exact special local cofactor span. It gives a strict directional-derivative maximum, an explicit compact C1 quadratic with nonzero jumps and mixed-sign Hessian determinants, and a restricted obstruction to direct zero-boundary patch assembly. [INDEPENDENT_COFACTOR_ACCEPTANCE.md](INDEPENDENT_COFACTOR_ACCEPTANCE.md) accepts the corrected statement and independently derives the examples and their limits.
4. [CORRECTION_NOTE.md](CORRECTION_NOTE.md) explains the mandatory mathematical correction: agreement of the piecewise function with its local polynomial holds on incident edge segments. A whole-supporting-line statement about the piecewise function is false. The corrected three-ray lemma and patch-gluing argument use actual full even fans and incident segments.
5. [THIRD_PASS_CERTIFICATES.json](THIRD_PASS_CERTIFICATES.json) supplies exact authored finite coefficients, coordinates, faces, fan normalizations, edge jumps, and counterexamples to the overstrong wording. [REPRODUCTION.md](REPRODUCTION.md) fixes determinant, incidence, polynomial, and finite-geometry conventions sufficient for independent reconstruction without a particular program.
6. [SOURCE_METADATA.json](SOURCE_METADATA.json) records the bounded new primary-source inspection for the Morgan–Scott configuration. The complete inherited source review remains in [first-edition SOURCES.md](second_edition/first_edition/SOURCES.md). [CONTENT_MANIFEST.json](CONTENT_MANIFEST.json) identifies all public files except itself.

## Two different topology conclusions

For the eighteen-vertex full disk, its only original degree-four interior vertices are the three central ear vertices. Every prospective closed component must contain all three and their complete original stars. Together these force all twelve interior vertices. The excluded full core is therefore the only possible closed component, and R has full row rank. This is a theorem about every admissible realization of that full topology.

For a larger nested-ring mesh, the same three stars force the initial twelve vertices only. They do not automatically force every later ring into an arbitrary closed component. The induction excludes the complete nested core when that entire core is closed; irregular proper components remain unresolved. No full-row-rank theorem for every larger full mesh follows from the complete-core exclusion alone.

The compact quadratic has three strict boundary corners and impossible required exterior attachments. It is not a quartic counterexample. The directional-derivative example is local and has no asserted compact extension. Neither example supplies global cycle balance or a universal maximum principle. Direct macro-patch assembly is excluded only at a macro vertex with an actual full even fan, imposed quartic proportionality, and three distinct incident macro-edge supporting lines.

## Edition boundaries and remaining question

The complete accepted [second edition](second_edition/README.md), including its eight first-edition files, is retained byte-for-byte. Its two-pass and then-unresolved nonsymmetric-family language is historical. No earlier proof, source-inspection limit, or result is silently strengthened in place. The new proofs identify their precise extensions here. The lifetime count is still unknown, and no fresh claim of worldwide openness is made.

The remaining task is to construct an admissible balanced closed support of a different or irregular topology, or prove that none exists. Different degree-four layouts, higher even valences, other boundary sizes, and legal straight boundary subdivisions are not settled by the ring argument. No unaudited auxiliary nonconvex seed is included or used.

This edition contains authored proofs, independent mathematical audits, authored finite certificates, and public bibliographic metadata. It contains no programs, copied source documents or datasets, private sources, or private coordination material. The new source's dimension statement is contextual attribution; the finite compact spline and cofactor identities are checked directly. No historical novelty is claimed for the spline configuration or normal-form calculations.
