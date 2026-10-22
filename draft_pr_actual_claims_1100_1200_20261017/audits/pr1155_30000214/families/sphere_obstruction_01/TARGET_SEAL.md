# Target seal

Sealed UTC: 2026-10-18T01:21:35.307146+00:00

This seal precedes reading the candidate `inputs/PROOF.md` and every prior audit, validation, acceptance, family, and reviewer verdict body. I have read the workspace AGENTS.md, the PDF skill, the own-family allowlist, source text excerpts containing the complete target definitions and decomposition theorem, and rendered OWR PDF pages 36-37 (printed 960-961), plus preprint PDF pages 4 and 7. A file-name inventory exposed the existence of other families and old audit files, but no bodies were read.

## Original target and quantifiers

Nevo's OWR 2005 Problem 8 asks whether the pieces in Theorem 7 may be homology spheres. Its preprint equivalent is Problem 3.7 following Theorem 3.4. The theorem takes a d-dimensional 2-CM simplicial complex over a field k, d >= 1, and covers it by finitely many minimal d-cycle subcomplexes over k; each piece after the first shares a d-face with the preceding union. Every designated piece can be placed first after reordering while preserving this overlap property. The sphere question naturally retains all these assertions, replacing pieces by homology d-spheres over the relevant field. The universal claim ranges over each such finite complex, dimension, and coefficient field. A single 2-CM complex over one field containing no such sphere subcomplex suffices for a negative answer, and already obstructs a cover without any overlap requirements.

2-CM is explicitly over a fixed field k: K is Cohen-Macaulay and every vertex deletion K-v is Cohen-Macaulay of the same dimension. The preprint explicitly includes purity and vanishing of reduced homology below the dimension of every face link, including the empty face. Its input is stronger than merely nonzero top homology or a cycle supported on all facets.

The source does not supply a separate formal definition of homology sphere. The standard simplicial homology-sphere interpretation, consistent with the statement that homology spheres are 2-CM, requires for every face F (including the empty face) the reduced homology of lk(F) to equal that of S^(d-|F|) over k. This includes all ridge links being S^0, local manifold homology, and global homology. A complex with the global homology of a sphere but singular links is outside that standard target; I will explicitly distinguish it from a homology sphere. For dimension two, the local conditions imply exactly two triangles per edge and every vertex link a connected 2-regular graph, hence a cycle, over every field. They do not depend on orientation. The global sphere condition then gives Euler characteristic 2 over every field. Any successful obstruction must not silently substitute global spherical homology for these local conditions.

## Independent adversarial approach registered before candidate exposure

1. Derive in dimension two the exact local-degree and Euler requirements for a sphere subcomplex, including characteristic two and nonorientable cases.
2. Examine whether a candidate ambient quotient preserves simplicial links and girth; quotient topology must be proved at the actual finite radius needed.
3. Separate the coefficient field proving 2-CM from the field excluded for potential sphere subcomplexes. A characteristic-zero spectral argument alone does not certify 2-CM in positive characteristic, but a field-independent combinatorial sphere obstruction can exclude spheres over all fields.
4. Audit CM via all links including the empty face, deletion purity and connectivity, and deletion first homology. Verify that any real weighted cocycle calculation actually proves the exact ordinary homology vanishing claimed.
5. Check each imported construction theorem's hypotheses, dimensions, field, type preservation, torsion/freeness, and quotient radius. A named building construction does not by itself establish all desired finite quotient properties.
6. Attempt counterexamples/edge cases symbolically first; use finite diagnostics only as illustrations unless they rigorously exhaust the stated parameter domain.

## Custody

Source PDFs and text were supplied in the parent audit's private source directory and are read in place. I did not independently retrieve them. Their byte identities are pinned below and will be reconciled with the parent's retrieval receipt after the mathematical seal. All locally rendered source images are under this family's private directory. No external communication or operative edits have occurred.
