# Source and scope audit

Checked October 4, 2026. Bibliographic facts and inspection history only;
downloaded source documents and extracted text are excluded from this packet.
The mathematical statements in `analysis.md` are authored reformulations.

## Primary target

Misha Kapovich, *Problems on Boundaries of Groups and Kleinian Groups*.
Author-hosted PDF: https://www.math.ucdavis.edu/~kapovich/EPR/problems.pdf

Inspected: page 1 date and boundary definitions; page 2 CAT(0) conventions;
page 21 Problem 83 and adjacent numbering. Page 21 was also rendered and
visually checked. The PDF prints October 24, 2007; the first-page introduction
attributes the collection mostly to a 2005 workshop. The imported year 2005
is not the date of the inspected revision. Earlier mirrored versions use 84
for the same local-connectedness question. Current page 21 instead has Lewis
Bowen's dimension question numbered 82 and Kapovich's question numbered 83.

The requested catalogue URL https://www.unsolvedmath.com/problems/6200083
was attempted first and was inaccessible through the web retrieval tool. The
public author PDF independently establishes the statement and identity.

The selected imported statement agrees after Unicode compatibility and
whitespace normalization. The prior AI report supplies no proof and does not
distinguish the now-established H^3 case sufficiently. Its status is not used
as mathematical evidence.

## Affirmative special cases

1. Mahan Mj, *Cannon-Thurston maps for surface groups*, Annals of Mathematics
   179 (2014), 1-80.
   https://annals.math.princeton.edu/wp-content/uploads/annals-v179-n1-p01-p.pdf
   DOI: https://doi.org/10.4007/annals.2014.179.1.1
   Inspected introduction, Theorems 7.1/8.6 summary, Section 8.3 and Theorems
   8.8-8.9 on printed page 76; that page was visually checked. Theorem 8.9
   covers finitely generated Kleinian groups with connected limit set,
   including the general parabolic case, through the surface theorem and
   Anderson--Maskit reduction. It is not a theorem for arbitrary X or all
   higher-dimensional hyperbolic spaces. The 80-page proof was not reproduced.

2. Ashani Dasgupta and G. Christopher Hruska, *Local connectedness of boundaries
   for relatively hyperbolic groups*.
   Inspected manuscript: https://arxiv.org/pdf/2204.02463
   Version: arXiv:2204.02463v2, April 29, 2024; PDF date May 1, 2024.
   Journal record: Journal of Topology 17 (2024), e12347,
   https://doi.org/10.1112/topo.12347
   Inspected Theorem 1.1 and introductory scope qualifications on pages 1-2,
   definitions of geometrically finite convergence actions, and the relevant
   connectedness discussion. Theorem 1.1 was visually checked. It removes
   earlier restrictions on peripheral groups; it still concerns the Bowditch
   boundary of a relatively hyperbolic pair. The manuscript's complete proof
   was not reconstructed.

## Obstructions to a universal boundary-extension route

3. Yoshifumi Matsuda and Shin-ichi Oguni, *On Cannon-Thurston maps for relatively
   hyperbolic groups*, arXiv:1206.5868v1, June 26, 2012.
   https://arxiv.org/pdf/1206.5868
   Inspected Theorem 1.1 on pages 2-3, its empty-peripheral specialization and
   the preceding boundary-uniqueness conventions. Both theorem pages were
   visually checked. The source asserts nonexistence of any continuous
   equivariant map, not merely failure of an injective boundary embedding.
   The current arXiv metadata lists one seven-page version; no publication
   venue is inferred from that record. The surface-group specialization plus
   the connected-tail proof in this packet is a deduction, not a quotation
   or a claimed new theorem of Matsuda--Oguni.

4. Owen Baker and Timothy R. Riley, *Cannon-Thurston maps do not always exist*.
   https://pi.math.cornell.edu/~riley/papers/Cannon-Thurston_maps_do_not_always_exist/CT_counter.pdf
   Author-hosted manuscript dated August 13, 2013; arXiv:1206.0505.
   Inspected introduction and Theorem 1. The rank-three free-subgroup example
   motivates the obstruction but is not used by itself to assert connectedness
   or non-local-connectedness of a limit set. The proof in this packet invokes
   Matsuda--Oguni rather than reconstructing the small-cancellation argument.

## Counterexample-construction control

5. Juhani Koivisto, *Non-amenability and visual Gromov hyperbolic spaces*.
   https://arxiv.org/pdf/1505.04662
   Inspected version arXiv:1505.04662v6, June 5, 2017. The public arXiv record
   says to appear in Groups, Geometry, and Dynamics 11 (2017).
   Inspected page 2 cone metric, Section 3 and Lemmas 5-7 on pages 6-7.
   The cone is traced there to Bonk--Schramm. The metric formula is checked
   directly in this packet, including boundary identification and failure of
   naive orbit realization. No non-amenability theorem is used in our argument.

Bonk--Schramm, *Embeddings of Gromov hyperbolic spaces*, Geometric and
Functional Analysis 10 (2000), 266-306, DOI
https://doi.org/10.1007/s000390050009, is the original construction reference.
Its full text was not inspected successfully; an attempted author-site PDF
returned 404. Koivisto is the inspected source for the cone construction.

## Current-literature and duplicate checks

Targeted queries covered the exact problem number and its alternate numbering,
arbitrary Gromov-hyperbolic spaces, connected non-locally-connected limit sets,
relatively hyperbolic boundaries, and Cannon--Thurston counterexamples. No
full resolution of the arbitrary-space target was found. This is bounded
research, not a proof of present open status or historical priority.

Live repository checks found the target row at rank 647, queued 0/5, no state
entry, no existing attempt directory, no exact-ID or exact-code PR, no matching
branch, and no exact-ID code search result. The existing related-target group
file does not list this ID. Search indexing can miss differently named work.

A content scan of the pinned corpus found relevant records 1100404 and
6200065. The first concerns convergence actions with additional finiteness
hypotheses; the latter has incomplete imported context. They are recorded as
related only. Neither is counted as an independently solved duplicate, and no
status update to either is justified by this packet.

All six successfully retrieved PDF byte streams are bound by byte count and
SHA-256 in `verification_metadata.json`. Hashes certify the inspected bytes,
not truth of the mathematical conclusions.
