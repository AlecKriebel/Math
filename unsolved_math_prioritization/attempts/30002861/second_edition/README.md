# Cubic and quartic spline interpolation second mathematical edition

Row 1761, problem 30002861 / OWR-13678-002. Prepared 13 October 2026 UTC.

## Result and status

The cubic vertex-value assertion has a negative answer, credited to Junkai Qiu's September 2026 preprint and verified in the [immutable first edition](first_edition/README.md). The general quartic value-and-gradient assertion remains unresolved by this work. **The bundled row remains unsolved.** No novelty or priority claim is made.

There are exactly **two newly documented substantive passes** in this sequence. The lifetime total is unknown. The theory branch, construction branch, their independent audits, and editorial preparation all belong to the same second pass; none adds another pass.

The quartic results now identify a precise unresolved target: an admissible closed active component with exact cycle balance exists if and only if some vertex first jets cannot be interpolated. If it exists, data with zero values and a single nonzero coordinate derivative at one nonsingular degree-four support vertex already witness failure. No such component is produced here, and no universal exclusion is proved.

## Fixed mesh model

The mesh is a finite conforming straight-line triangulation of a polygonal disk with nondegenerate triangles. Splines are globally C1 and polynomial of total degree at most four on each original triangle. Values and both first derivatives are prescribed independently at all vertices, including boundary vertices. There is no subdivision, vertex movement, boundary condition, or additional smoothness assumption.

The cubic question prescribes only vertex values and permits free gradients. Its negative answer does not settle the quartic question. [First-edition sources](first_edition/SOURCES.md) distinguish these questions from dimension, stability, approximation, and refined-mesh interpolation problems.

## Second pass reading guide

- [SECOND_PASS_THEORY.md](SECOND_PASS_THEORY.md) proves local pure-gradient nonvanishing, the automatic obstruction criterion, full row rank after adjoining gradient columns, the signed-Ceva equivalence for exact balance, and the one-way construction of a compactly supported C1 quadratic spline from a balanced component. It also recovers the known dimension formula dim S¹₄ = 6V − 3 + σ. That formula is known and is not claimed as new.
- [THEORY_AUDIT.md](THEORY_AUDIT.md) gives the complete independent mathematical acceptance, including boundary conventions, the projective point at infinity, and a separate incidence-matrix proof of the quadratic integration step.
- [SECOND_PASS_CONSTRUCTIONS.md](SECOND_PASS_CONSTRUCTIONS.md) proves the strict five-corner lower bound, gives an authored rational sign-balanced but magnitude-unbalanced disk, and excludes every admissible member of a larger three-parameter symmetric family, including possible proper closed components.
- [CONSTRUCTION_AUDIT.md](CONSTRUCTION_AUDIT.md) gives independent acceptance of the geometry, exact signs and ranks, full quartic system, and all family quantifiers.
- [SECOND_PASS_CERTIFICATE.json](SECOND_PASS_CERTIFICATE.json) gives the exact authored rational coordinates, triangles, edge ordering, reduced matrices, sign witness, unequal cycle product, and verification results. [FINITE_WITNESSES.json](FINITE_WITNESSES.json) supplements it with exact positive doubled areas, fans, incidences, a spanning tree, and individual cycle ratios. [FINITE_AUDIT_CERTIFICATE.json](FINITE_AUDIT_CERTIFICATE.json) includes independent verification outcomes and the exact nonzero full-system minor.
- [REPRODUCTION.md](REPRODUCTION.md) specifies a mathematical reproduction procedure independent of any particular program. The closed connected support and one unequal cycle already give a short exact full-row-rank proof.
- [DEPENDENCIES.md](DEPENDENCIES.md) links the exact accepted baseline and identifies the byte-preserved first edition. [CONTENT_MANIFEST.json](CONTENT_MANIFEST.json) identifies every public file except itself.

## What the partial results do and do not imply

Every closed support must have at least five strict convex boundary corners; straight subdivisions do not evade the result. This is a necessary condition, not a construction with five corners.

The authored 18-vertex disk has a closed 12-row support whose sign matrix has rank 11. The actual rational matrix has rank 12, with positive cycle product 683875575/3191327216 rather than 1. Thus sign balance does not imply exact balance. The mesh admits arbitrary quartic vertex jets.

The three-parameter alternating-radius family also admits arbitrary quartic vertex jets throughout its admissible geometric parameter set. This family exclusion is not a theorem about arbitrary perturbations or every mesh with a hexagonal support.

The compact quadratic interpretation is one-way. An arbitrary compactly supported C1 piecewise quadratic does not supply the required proportionality to the prescribed quartic compatibility row at each vertex.

The bounded source review in the first edition did not establish a complete resolution of the quartic assertion. Its dated inspection limits remain in force. This edition makes no new assertion of worldwide openness and does not claim a fresh literature survey or inspection of the historical 1987 dimension proof.

## Edition and content boundaries

The eight documents in [first_edition](first_edition/README.md) are preserved byte-for-byte. Their first-pass status and remaining-question language are historical. The new theory supersedes only their need to separately require a nonzero supported local jet form; it does not alter the first-edition files or invalidate their conditional conclusions.

This edition contains authored mathematics, independent audits, finite authored certificates, and public bibliographic metadata. No source PDF, copied third-party source text or coordinate dataset, program, private source, or private coordination material is included. Qiu's construction remains attributed to the [versioned preprint](https://arxiv.org/abs/2609.06364v1); reproducing its source coordinates requires that preprint. The rational second-pass mesh is authored here and is included in full.
