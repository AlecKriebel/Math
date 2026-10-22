# Three-color hypergraph counts: OWR-14299905-035

Problem ID: 30006560. Catalogue title: *Vertex Sets Meeting Every Edge Color*.

**Status: unresolved in full after five substantive proof attempts.** These AI-assisted research notes record partial results and explicit failures of several candidate proof routes. They are not a claimed solution, and no novelty or priority claim is made for the restricted results.

## Exact question and bound

For a finite simple (r−1)-uniform hypergraph H, r≥3, whose edges each have exactly one of three colors, let R,G,B be the color-class sizes. Let T be the number of r-vertex sets S for which H[S] has at least one edge of each color, counting S once. Hans Yu's Question 8 in Oberwolfach Report 1/2026 asks for the extremal value of T. The report's Theorem 9 gives T≤√(6RGB) for every r; the sharp graph bound T≤√(2RGB) is conjectured for all r.

The exact extremal-count question is broader than the conjectural bound. Even proving the bound would not give an exact finite formula for every unequal triple (R,G,B).

There is no proper-coloring hypothesis on H and no minimum vertex-set/vertex-cover parameter. Proper coloring appears in the known K4 construction only. The coefficients 6 and 2 belong inside the radicals.

## Proven here, with full arguments in the attempts

- T≤min(RG,RB,GB). With sorted counts a≤b≤c, the target follows when ab≤2c, including a≤2.
- A common (r−3)-core reduces exactly to the known graph theorem; balanced K4 blowups attain T²=2RGB for every r after coning. The construction and graph theorem are credited to the literature.
- The conjectured inequality is closed under intersection-connected hyperedge-block unions.
- If n is the active-vertex count, the complement formulation is T=|∂F_R∩∂F_G∩∂F_B| for three disjoint families of d=n−r+1 sets. This proves the target when d²a≤2bc.
- The target holds for n≤r+2. The d=3 proof uses self-contained parity and small-trade arguments; finite checks are only corroboration.

## Explicitly unsuccessful routes

The exact link identity counts successful sets with multiplicity a_S b_S c_S. A five-vertex example disproves a proposed lossless aggregation of link bounds. A four-edge family disproves monotonicity of the natural simultaneous color-preserving shift. The same five-vertex example disproves a raw red-face squared-degree bound. Fractional ownership gives an exact convex dual and repairs that example, but the required general weighted bound remains unproved.

## Files

- [Source assessment](SOURCE_GATE.md)
- [Five-attempt log](RESEARCH_LOG.md)
- [Attempt 5 and the n≤r+2 theorem](attempts/turn_05.md)
- [Portable exact checks](verify_claims.py) and [recorded output](verification.json)
- [Author manifest](AUTHOR_MANIFEST.json)

Run `python3 verify_claims.py` from this directory using Python 3.8 or later. It uses only the standard library, performs no network access, and prints deterministic JSON. It checks exact example counts, rational ownership certificates, 2,100 disjoint-family pairs on five vertices, and 2,400 seeded instances in the proven small complementary dimensions. These bounded checks are not a proof of the unrestricted conjecture.
