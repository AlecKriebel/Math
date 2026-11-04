# Independent adversarial audit: one-subdivision shellability

Date: 21 October 2026. Row 1837; ID 30002123; OWR-12006-004.

## Verdict and exact accepted scope

ACCEPTED as an unresolved research checkpoint, not a solution or disproof. No blocking mathematical defect remains after checker hardening and explicit relative-neighborhood quantifiers. Accepted RESEARCH.md SHA-256: a11d8b56011bc9043f00410b97f29aed7e0084c3487e36df1c02fa0870660d4a.

The five routes establish only: a correct local-link decomposition and warning against local-to-global inference; failure of one precisely defined centroid ordering; the known shellable-input sufficient class; exact small finite positive certificates; and an unproved sufficient relative-shellability strengthening. These do not settle the original conjecture in dimension at least four. The two-simplex four-ball was already shellable before subdivision and is not a new difficult case.

## Source scope

Independently checked the recovered primary report's Problem 1 and glossary: the support must be convex, and exactly one barycentric subdivision is requested. The report's historical d+2 bound is not the current target. Inspected manuscript arXiv:1202.6606v3, Theorem A, Corollary I.2.2, Theorem I.2.4 and introduction: two subdivisions suffice generally; one suffices through dimension three; one in higher dimensions is conjectured there. Independently checked the 2020 manuscript Theorem 4.5: its conclusion is collapsibility, not shellability. This audit does not certify an exhaustive search of literature through 2026.

Public sources: https://publications.mfo.de/bitstream/handle/mfo/3305/OWR_2012_34.pdf?isAllowed=y&sequence=1 ; https://arxiv.org/abs/1202.6606v3 ; https://par.nsf.gov/servlets/purl/10169029 .

## Independent computational verification

The accompanying independent_check.py does not import either research script. It reconstructs all maximal face chains by rank-by-rank subset extension rather than trusting the submitted facet list. It checks equality and uniqueness of the entire facet set, enumerates the full face set of every simplex, intersects it with the accumulated face union, and extracts inclusion-maximal intersection faces. Every attachment must be a nonempty proper union of ridges. This is independent of the research checker's pairwise-intersection coverage implementation.

For the two four-simplices, all 240 expected distinct flags occur exactly once. All 239 attachments pass. Numbers of attachments with respectively 1, 2, 3 and 4 old ridges are 42, 132, 62 and 3. A proper nonempty union of simplex boundary facets is a ball. Since these are facets of a genuine triangulated ball, the verified shelling condition supplies the claimed shelling. The independent checker also verifies the simplex lexicographic orders in dimensions 1 through 5, with 2, 6, 24, 120 and 720 facets.

Five malformed input controls are rejected: deleting a facet, adding a duplicate, replacing a facet with an existing one, introducing an unknown face label, and repeating a vertex within a facet. A sixth control preserves the complete facet set but swaps a nonadjacent facet into second position; it is rejected for a disconnected attachment. These controls distinguish facet-completeness validation from attachment validation. They are not a claim that the script is a hardened parser for arbitrary hostile JSON types.

## Exact geometric realizations

The four common ridge vertices are 0,e1,e2,e3 in x4=0. The two apex coordinates are (1/4,1/4,1/4,1) and (1/4,1/4,1/4,-1). Both four-simplices have nonzero determinant, respectively +1 and -1. Their intersection is exactly the common ridge. The apex midpoint has strictly positive ridge barycentric coordinates (1/4,1/4,1/4,1/4). In any convex combination, equal portions of the two apex coefficients can be replaced by twice their minimum times that midpoint. Thus every point of the full convex hull belongs to one of the two simplices; their union is convex. The independent checker reads and verifies the exact coordinates and midpoint identity in realization.json.

The negative sweep input is the square triangulated from interior point (1/3,1/4). These four triangles exactly fill the convex square. The independent checker recomputes every centroid height with rational arithmetic for h=x-(14/11)y and confirms strict increase across all 24 submitted facets. The first three heights are -23/27, -955/1188, and -461/594. The third flag has exactly one maximal face in its intersection with the previous union: label 8, the original vertex v3. This is dimension zero rather than an edge. Hence the proposed order fails, even with no ties. This does not refute shellability or all geometric sweep algorithms.

## Conceptual and relative-shellability audit

The link of a vertex corresponding to nonempty sigma in sd(C) is sd(boundary sigma) * sd(link_C sigma), by splitting chains below and above sigma. Locally shellable links alone do not imply global shellability: nonshellable geometric three-balls provide the relevant warning, not counterexamples after subdivision. Shellability preservation under stellar and derived subdivisions is correctly supported by Lemma I.1.11 of the inspected manuscript. It does not imply preservation under arbitrary refinement.

Approach 5 correctly retains the extra outer subdivision in Theorem I.2.1 and distinguishes ordinary shellability from prescribed relative attachments. At audit request, its proposed missing strengthening now states the full dimension-three version of Proposition I.2.5: every subdivision of a spherical polyhedron, every general-position hemisphere meeting it, both D=empty and D=sd(boundary C), relative shellability of the derived neighborhood and a compatible relative sequence from sd(C) through that neighborhood to empty. This is only a sufficient proposed route, not a theorem established here. Ordinary three-dimensional shellability and one-subdivision collapsibility cannot replace it. The manuscript's apparent notation inconsistencies are acknowledged rather than silently repaired to manufacture a proof.

## Reproducibility and limits

Run: python -B independent_check.py

Results: INDEPENDENT_RESULTS.json, including exact input hashes. Certificate hash: 838fd8ef62af1e56abaec95907c814e281e688c26149327045a5a31407d309e4. Failed-sweep input hash: 469c0f6fb14c90221ec9ec099197b223979ed2171e068e08901fbcbb2f5337ff.

No queue changes, publication, or third-party communications were performed. This report contains authored mathematical analysis and public source pointers, not copied source documents or dataset contents.
