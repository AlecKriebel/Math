# Source and scope audit: 7200087 / AMR-071-0087

As of 3 October 2026. No novelty claim. No source PDF, screenshot, webpage copy, cached corpus, or private research history is part of the publication payload.

## Identity and access

The live `AlecKriebel/Math` queue at rank 451 names ID 7200087 / AMR-071-0087, queued at 0/5, with the at-least-one-edge wording. The pinned catalog record has the same question. Its source provenance is the Wikipedia list, revision 1366636767, Geometry bullet 87, accessed 29 July 2026.

The exact requested detail page, <https://www.unsolvedmath.com/problems/7200087>, could not be independently verified live: web retrieval failed, direct HTTP returned 403, and dot's cloud browser rendered a blocked 403 page. No bypass or authentication was attempted. The pinned Wikipedia revision could not be independently refetched either. Consequently this audit does not claim that either inaccessible page was read live or that the detail site's wording has remained unchanged.

The current [Wikipedia list](https://en.wikipedia.org/wiki/List_of_unsolved_problems_in_mathematics#Euclidean_geometry) was read on 3 October 2026 and now specifies *exactly one* shared edge. The current [Szilassi page](https://en.wikipedia.org/wiki/Szilassi_polyhedron#Complete_face_adjacency) still has an at-least-one question box alongside a one-edge discussion. These secondary pages are used for provenance and wording comparison only, not to certify the mathematics. The strengthened current list is not substituted for the pinned target.

## Primary source chain

### 2020 construction

Mizhaev's [OSF preprint](https://doi.org/10.31219/osf.io/hvtey) was retrieved using its public OSF metadata and linked primary file. OSF records publication on 25 April 2020 and file modification on 29 April 2020. Section 3, pp. 5–7, describes variant V2, explicitly states complete pairwise face adjacency, and includes coordinate and face-incidence tables. Pages 5–6 were also rendered and visually inspected. No claim is made that this audit establishes historical priority against every possible predecessor.

The original tables list face vertex sets, rather than the explicit cyclic walks used by the executable certificate. The certificate therefore uses the later integer realization, and does not silently treat the 2020 table order as a boundary order.

### 2026 integer certificate

Mizhaev's [arXiv:2609.17700v1](https://arxiv.org/html/2609.17700v1), submitted 15 September 2026, contains the exact coordinates, face cycles, and planes checked here. All required geometry and topology have been independently recomputed using newly written rational-arithmetic code.

A wording inconsistency must be disclosed: Section 2 of that preprint initially defines pairwise intersections as a single vertex or edge, but Section 5, its matrix, and its actual data explicitly allow two edges. The computed example satisfies the broader acoptic convention. The inconsistent definition cannot turn it into a non-overarching example.

### Independent later construction

Röst–Vígh [arXiv:2609.32998v1](https://arxiv.org/html/2609.32998v1), submitted 26 September 2026, Theorem 1, explicitly gives eight planar simple nonagons and genus 3, with 20 single-edge and eight double-edge face pairs. Sections 1 and 5 distinguish the at-least-one question from the still-open exactly-one case. This corroborates the relevant distinction. This audit did not independently rerun their second coordinate table.

Both 2026 sources are preprints. Their exact finite data, rather than presumed peer-review status or author authority, support the accompanying certificate.

### Definitions and older literature

Grünbaum–Szilassi (2009), introduction, permits acoptic surfaces whose pairwise face intersections have several components, each a common vertex or edge; it calls those faces overarching. This establishes that admitting doubled edge contacts is a recognized geometric convention, not a substitution of an abstract map.

Arseneva et al. (2024), Section 1, instead requires an intersection to be a single common corner or side. Their Section 2 open statement belongs to this stricter model. Its open status cannot be contradicted by the present overarching witness. Their unrestricted-graph construction in Section 2 is not automatically a closed surface; it must not be used as a shortcut for this existence problem.

The mathematical source for the seven-face torus is Szilassi, not Császár. Szilassi’s original *Regular Toroids*, Structural Topology 13 (1986), pp. 69–80, was retrieved from the UPC institutional repository and inspected: the opening fixes straight edges and planar faces, and Section 4 gives the seven-face torus and its Császár duality. The 2009 primary text and the 2026 introductions also document the distinction. The older duality is combinatorial, and no result about geometric nonrealizability of a vertex-neighborly dual is imported as a result about the face-neighborly problem.

## Disposition

Recommend a scope-qualified `already_solved` entry for the exact pinned at-least-one question, credited to Mizhaev's prior construction and exact 2026 certificate, with **0/5** original attempt turns. Keep the exactly-one/non-overarching variant explicitly unresolved. Final publication requires independent audit and the publication gate; no remote write has been performed by this author task.
