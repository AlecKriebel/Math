# 7200087: qualified prior-literature answer for mutually adjacent faces

**Result:** already solved for the pinned **at-least-one-edge** question under the acoptic convention that allows overarching faces. **Original attempt count: 0/5.** This is a credited verification of published constructions, not a new discovery.

Mizhaev's construction has eight simple planar nonagonal disk faces, 24 vertices, 36 edges, and genus 3. Every face-pair shares an edge. **Eight pairs share two disjoint collinear edges.** No face has a hole, disconnected boundary, or self-crossing, and the surface is embedded without unintended intersections.

**The exactly-one-edge/non-overarching variant remains unresolved here.** Neither this packet nor its queue disposition is an unqualified solution claim about the strengthened modern question. The inaccessible live UnsolvedMath detail page and pinned historical Wikipedia page are not claimed to have been independently read; the available pinned record and live queue identify this target.

## Proof and independently reproduced evidence

- [Full mathematical certificate](author/CERTIFICATE.md)
- [Author source and scope audit](author/SOURCE_AUDIT.md)
- [Independent audit: qualified PASS](independent_audit/AUDIT.md)
- [Integer witness and exact verifier](author/verify_witness.py), with [all 28 face-pair intersection results](author/VERIFICATION.json)
- [Independent triangulation checker](independent_audit/check_triangulation.py), with [1,540 triangle-pair checks and ten controls](independent_audit/triangulation-results.json)
- [Independent reconstruction of the 2020 tables](independent_audit/check_2020_tables.py), with [recovered walks and exact results](independent_audit/2020-results.json)
- [Publication byte manifest](PUBLICATION_MANIFEST.json)

The frozen author and audit manifests preserve their prepublication states; pending-review and no-remote-write fields in the author snapshot describe when it was frozen. The later independent audit and this publication note record the qualified PASS.

## Credit and source cautions

Credit belongs to **Ruslan Mizhaev**, [April 2020 construction](https://doi.org/10.31219/osf.io/hvtey) and [2026 integer realization](https://arxiv.org/html/2609.17700v1). The independently reconstructed 2020 coordinate data pass the same exhaustive geometric tests. [Röst and Vígh's 2026 preprint](https://arxiv.org/html/2609.32998v1) supplies a different example and corroborates the distinction between at-least-one and exactly-one adjacency. Its second coordinate table was not independently certified in this packet. The 2026 sources are preprints; peer-reviewed acceptance is not asserted.

Two source errors are explicitly retained as cautions:

1. The 2026 integer preprint's Section 2 defines a single-edge intersection, while its actual witness and later multiplicity matrix allow doubled intersections. The data validate the broader declared acoptic convention, not that strict definition as written.
2. The 2020 Section 3 prose describes one doubled neighbor per face. The exact tables, independently reconstructed here, instead give **two doubled neighbors per face**, hence eight doubled face-pairs in total. This is a prose typo, not a defect in the certified coordinate data.

The convex maximum is four, attained by a tetrahedron. Császár's seven-vertex torus is vertex-neighborly; Szilassi's seven-face torus is its combinatorial dual and is face-neighborly. Neither combinatorial duality nor an abstract surface map alone certifies a geometric embedding.

## Reproduce without third-party dependencies

Use Python 3 with assertions enabled:

```sh
python3 author/verify_witness.py
python3 independent_audit/check_triangulation.py
python3 independent_audit/check_2020_tables.py
```

The two geometrical methods contain the complete mathematical data. The author checker uses exact polygon/line sections; the independent checker ear-triangulates all faces and checks every triangle pair with a different intersection algorithm. No numerical tolerances or random searches are used.

The optional `independent_audit/check_source_tables.py` compares the literal coordinate data against a separately downloaded copy of `https://arxiv.org/html/2609.17700v1`, placed at `local_sources/mizhaev-v1.html` beside these directories. It is a source-integrity check, not a prerequisite for rerunning the geometric certificates. Its inspected source hash is recorded in the audit.

Only original explanatory text, attributed mathematical data, verification code/results, and manifests are included. No original source PDFs, screenshots, webpage copies, corpus dumps, or private history are republished.
