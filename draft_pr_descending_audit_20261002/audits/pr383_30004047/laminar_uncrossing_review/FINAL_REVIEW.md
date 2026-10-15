# PR383 Turn 5 independent structural audit

**Result: PASS_SCOPED for the disjoint-maximal/laminar theorem, conditional deletion stability, and specified local uncrossing obstruction. Mandatory repairs found in this assigned scope: 0.**

The audit binds all 49 frozen files (48 target files plus QUEUE) to Git head `967e8e489aa4599f712d5ddcde62e591827f7e38` by exact bytes, length and SHA-256. No Git index, branch, queue, PR, service or remote state was changed. All new files are confined to this review folder. The independent result is established by the written reconstruction and new controls, before comparison with the old review.

## Source-first target

Independently fetched [the original EMS 46780 contribution](https://ems.press/content/serial-article-files/46780) and visually checked printed pp.46–47, physical pp.42–43. Independently resolved [DOI 10.37236/8451](https://doi.org/10.37236/8451), fetched [the published EJC 29(2) (2022), P2.47 PDF](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v29i2p47/pdf/), and visually checked p.4 definitions, p.8 weighted framework and p.21 Conjecture 5.1 before reading candidate proofs or prior verdicts.

The source target has all real x,y in (0,1], all integer k>=1, strict x+ky>1 and weak kx+y>=1; it asks for a C vertex reaching at least 1/k of distinct A vertices. There are only two forward degree conditions. The diagonal half-reach assertion at x>1/3 is a special case. The two reverse degree conditions belong to psi and are unavailable here. The primary paper DOI identifies the source paper, not a DOI for this research packet.

## Analytical findings

`RECONSTRUCTION.md` provides the independent complete proof. Its mechanism is a partition of A by maximal neighborhood blocks, then the two complementary degree inequalities. Negating the conclusion yields mx<=1, m>=k+1 and y<1/k. For m>=k+2, the weak condition is contradicted by kx+y<k/(k+2)+1/k<=1, with the strict inequality preserved when k=2. For m=k+1, each pair of blocks has combined mass strictly above 1/k, forcing disjoint C-neighborhoods for maximal representatives and hence (k+1)y<=1. Combining this with (k+1)x<=1 contradicts x+ky>1.

The proof retains arbitrary positive probability weights on all three finite parts, places no upper size bound on any part, allows positive-weight empty middle types, and does not assert that every C-reach is a union of whole maximal blocks. A laminar family has disjoint maximal members, so the laminar corollary follows directly. The broader disjoint-maximal class can contain crossing nonmaximal subsets.

The deletion theorem is exactly conditional on the existence of the stated exceptional middle set. Its retained parameter x'=(x-epsilon)/(1-epsilon), positivity requirement 0<=epsilon<x, strict epsilon<(x+ky-1)/(ky) and weak epsilon<=(kx+y-1)/(k+y-1) are correct. The denominators are positive for k>=2, y>0. At the weak boundary kx+y=1, epsilon must be zero for this proof. No small-exception existence theorem or optimality of the deletion bounds follows.

Turn 5 is analytically independent of Turns 3–4. Their whole proofs and checkers were read to check scope: their cardinality mechanism retains equally weighted A, strict x,y>1/(k+1), and a finite |A|<=5k range. The ordinary diagonal half-reach counterexample lower bound of eleven first vertices is a necessary size restriction, not a universal bound on potential counterexamples or on weighted support. Those finite cardinality theorems are not silently converted into unrestricted weighted-mass results.

## Materially new finite controls

`independent_controls.py` imports no author or reviewer code. It builds actual adjacency families, evaluates Boolean distinct reach, and uses exact rational arithmetic. It passed:

- 2415 actual finite graphs, including 1949 laminar and 464 disjoint-maximal nonlaminar structural graphs; 8512 qualifying graph/k pairs were checked.
- Sharply unequal A weights up to a 10^18 ratio, empty middle types, and extremely asymmetric x or y on the weak boundary. A k=1000003 control exceeds the author enumerations and is an actual weighted graph.
- Five ordinary disjoint-path negative controls at x+ky=1, demonstrating why the strict condition cannot be relaxed to equality.
- An actual nonlaminar exceptional-middle deletion graph and 10009 exact deletion equivalence/boundary controls, including both sides of strict and weak epsilon endpoints.
- A raw reconstruction of all 396 vertices in the overlap graph. Its actual A degree is 21/55, at least the stated lower parameter 4/11; B-to-C degree is 4/11. Each C has 45 distinct reached A vertices and 2520 two-edge paths. The graph is excluded from the structural class and is not a source counterexample.
- All 108900 ordered pairs of four-neighbor reassignments for the union and intersection middle vertices. Since further neighbors can only increase reach, this establishes the exact optimum over every legal reassignment with at least four neighbors: **the minimum possible maximum reach is 51/55**, compared with the original 45/55. The intersection vertex's legal degree is checked too. This is a sharper finite control than merely proving that a single union edge increases reach.

The uniform union/intersection replacement preserves A degree because the two altered middle weights are equal, namely 1/330. It does not justify this preservation for arbitrary unequal middle weights. All other 328 middle vertices remain fixed in this local experiment. The minimum 51/55 conclusion does not prohibit global rearrangements or reweightings and does not produce universal laminarization.

## Replay and old-review comparison

After source-first reconstruction and new controls, verified-source copies of the complete Turn 3–5 checkers were executed in `private_B/`. Their declared output files agree byte for byte, length for length and SHA-256 for SHA-256: Turn 3 has 12,105,108 assertions, Turn 4 has 164,794, and Turn 5 has 299,628. This is 12,569,530 author assertions in this assigned replay scope. Author code was read before execution. The older review and its code were read only afterward. They agree with this independently reached scoped conclusion; they were not a proof dependency.

## Strongest result and remaining gap

The strongest statement verified here is the complete asymmetric integer-k source implication on the finite disjoint-maximal first-neighborhood class, with arbitrary positive weights and no size bound, plus its conditional deletion stability. The strongest new local computation is the exact 51/55 reassignment optimum.

Arbitrary overlapping maximal neighborhoods of unbounded finite size remain unhandled. No justified global rearrangement, support reduction or universal laminarization is supplied. Both original threshold assertions remain **unsolved, 5/5 substantive author turns**, with no sixth author proof search, historical novelty certification, human peer-review claim or new paper DOI.

This assigned scope is ready for incorporation into the root audit's evidence. It is not a ready-to-merge disposition or a service action. The root review must complete its required PR385 then PR384 dispositions before disposing of PR383.
