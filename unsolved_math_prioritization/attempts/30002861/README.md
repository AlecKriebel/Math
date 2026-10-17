# Cubic and quartic spline interpolation on fixed triangulations

First mathematical edition for row 1761, problem 30002861 / OWR-13678-002. Prepared 13 October 2026 UTC.

## Conclusions and review status

The cubic vertex-interpolation assertion has a negative answer. Junkai Qiu's September 2026 preprint supplies the counterexample; the [cubic proof](CUBIC_PROOF.md) and [independent audit](CUBIC_AUDIT.md) verify that exact construction. The example and obstruction are credited to Qiu. This collection makes no novelty or priority claim.

The separate quartic value-and-gradient assertion remains unresolved by this work. The quartic documents contain an independently accepted exact reduction and partial positive results. The [quartic audit](QUARTIC_AUDIT.md) states the accepted scope. **The bundled row remains unsolved.** This is the first newly documented substantive pass. The lifetime pass count is unknown; separate source checks, proof branches, and audits do not count as additional passes.

## The precise questions

Let Δ be a fixed finite conforming straight-line triangulation of a polygonal disk in the plane. Its triangles have positive area and intersect only in common faces. Let S¹_d(Δ) consist of globally continuously differentiable functions whose restriction to every triangle is a polynomial of total degree at most d.

All vertices participate, including boundary vertices. The mesh is not subdivided, vertices are not moved, and no boundary conditions are imposed.

1. The cubic question asks whether every assignment of scalar values at all vertices is realized by some spline in S¹_3(Δ), for every such Δ. Gradients are free. Qiu's counterexample gives a negative answer.
2. The quartic conjecture asks whether some such Δ admits a collection of scalar values and both first derivatives at every vertex that no spline in S¹_4(Δ) realizes. A positive interpolation result on selected meshes does not decide this existential question.

These are Alfeld's report items 16 and 18, respectively. They are distinct from the cubic dimension conjecture and from stability, approximation-order, or refined-mesh interpolation questions.

## Reading guide

- [CUBIC_PROOF.md](CUBIC_PROOF.md) reconstructs the full cubic space, proves the exact obstruction, and computes dimension 107 and vertex-evaluation rank 40 on Qiu's 41-vertex, 56-triangle mesh.
- [CUBIC_AUDIT.md](CUBIC_AUDIT.md) independently checks geometry, the full-space parameterization, orientation, all boundary cancellations, and exact rank certificates. These two cubic documents are reproduced unchanged from their accepted editions.
- [QUARTIC_REDUCTION.md](QUARTIC_REDUCTION.md) derives the finite compatibility system Rm=Hj, gives its exact weighted-graph criterion, proves quartic surjectivity on Qiu's mesh, and gives a positive eighteen-vertex collinear family with a symbolic determinant certificate. These partial results are independently accepted.
- [CONVEX_SUPPORT.md](CONVEX_SUPPORT.md) proves that a closed component of R induces a convex polygon triangulation and contains at least three nonsingular degree-four interior vertices. It derives quartic surjectivity whenever the original mesh has at most two such vertices. These partial results are independently accepted.
- [QUARTIC_AUDIT.md](QUARTIC_AUDIT.md) independently checks the exact reduction, geometric hypotheses, full and reduced systems, symbolic family, convex-support theorem, and the publication edition’s explicit certificate conventions.
- [SOURCES.md](SOURCES.md) distinguishes primary claims, exact source versions, inspection limits, and the bounded literature-status check.
- [SOURCE_METADATA.json](SOURCE_METADATA.json) records public PDF URLs, byte counts, SHA-256 identities, and dated retrieval and inspection history. File identity is separate from mathematical acceptance.

## What remains to be proved

The quartic reduction isolates the remaining issue: construct a geometrically admissible closed component whose edge ratios are cycle-balanced and whose supported local jet form is nonzero, or prove that no such component exists. The collinear family shows that closed supports themselves can occur; its exact certificate shows that this particular family does not obstruct quartic interpolation.

The bounded literature review did not establish a complete resolution of the quartic assertion. This does not certify worldwide openness. No minimality, arbitrary-perturbation, or general fixed-mesh quartic theorem is claimed.

## Reproduction and content limits

This edition contains authored mathematical proofs, audits, and public bibliographic metadata. The source PDFs, copied source text, source coordinate and triangle arrays, author programs, and full computational matrices are not redistributed. To reproduce Qiu's numerical construction, obtain its specification from the [versioned preprint](https://arxiv.org/abs/2609.06364v1). The eighteen-vertex family and sparse minors in the quartic note are authored mathematical constructions and certificates, given directly in the text.

The cubic counterexample and the stated quartic partial results have independent mathematical acceptance. Neither the partial quartic results nor their acceptance resolve the full problem.
