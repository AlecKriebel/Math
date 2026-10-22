# Source and model audit: Rolling a Die over a Labeled Board

## Verdict

The retained primary sources do not supply a classification of the fully labeled, hole-free rectangular Hamiltonian-path problem. The 2007 free-cell results and prescribed-cycle-length result concern different decision problems. De Biasi's 2012 blocked-cell hardness manuscript uses a cycle target and forbidden cells.

The older fully rectangular nonuniqueness result is independently verified here: both cycles drawn in De Biasi's Figure 4 traverse the same 30 × 9 board, match all 270 top labels, and return to the identical full orientation. They are genuinely different undirected cycles. This is verification of a known 2012 construction, not a new nonuniqueness result and not a complexity classification.

A source-annotation defect was found: all 270 orientation dashes in Figure 4 point opposite to the actual reference-face direction under the definition in the manuscript's Section 2. The labels and two paths themselves pass physical replay. Reversing each dash repairs the annotations.

## 1. Exact target and conventions

[TOPP Problem 68](https://topp.openproblem.net/p68) specifies a completely labeled rectangular lattice board and exact-once visits with the top face matching after landing. Its literal statement has no return-to-start condition. Its reference to a set B after naming the board R is read as an editorial inconsistency, not permission to use an arbitrary subset.

A precise path version used for auditing has the following data and rules:

- The input explicitly lists every label of a finite nonempty w × h rectangle. There are no free cells, blocked cells, holes, or allowed excursions outside the rectangle.
- A standard six-distinct-label die has opposite labels summing to seven. Its chirality is fixed by an explicit six-face reference tuple.
- A move tips the die over one supporting edge to an edge-adjacent cell. There are no in-place rotations, lifts, diagonal moves, or relabeling during a solution.
- The first occupied cell counts as a visit and must match the initial top face. A certificate lists wh distinct cells and wh−1 legal rolls.
- A corner start is the natural reading of the two origin-corner clauses. The exact initial orientation is not fully stated by TOPP. A fixed input orientation, or an existential choice among the four rotations matching the starting label, must be identified explicitly. This audit does not assert equivalence between arbitrary starts and corner starts or between fixed and selectable initial orientations.
- The other endpoint is unrestricted unless an explicitly different problem is defined.

The precise version is in NP: check the certificate's length, coverage, adjacencies, orientation updates, and labels in time polynomial in the explicit board size. This does not establish NP-hardness or a polynomial algorithm.

A related cycle convention lists each cell once, then includes one closing roll back to the first cell. For full-state cycles, the closing orientation equals the initial one. This closing revisit convention belongs to the cycle problem; it must not silently be imposed on the literal path target.

## 2. Source provenance and status

The source audit checked the complete PDF bytes against the identities below. The source documents themselves are not reproduced. The [source metadata](SOURCE_IDENTITIES.json) records the corresponding public URLs.

| Source | Bytes | SHA-256 |
|---|---:|---|
| Buchin et al., full version, 30 pages | 531507 | 0859cf84f2f2067621128d920b0ac67bbc7a9198a75e8406068303bea072421b |
| Buchin et al., short version, 4 pages | 195436 | fbb092f72df80517bcd0e5b9a82e5b1180a7e7c3bef008a5b1608df35149b43d |
| De Biasi, Version 0.03, 21 pages | 992617 | d035edb49ea837123596858ff4267df7397378855390491786540210f1099166 |
| Demaine–O'Rourke, CCCG 2006, 6 pages | 158204 | 3a05df691d69652dd21e027f032e0c3711827dcce4a12b63129ed8191cd6e2aa |
| Yao–Uehara, 2021 technical report, 8 pages | 1654039 | 3f8f2faffc88044819f801c68ba1234090f549d8a7fe3f2006288bbe82fb6ad3 |

The [Buchin et al. author landing page](https://erikdemaine.org/papers/DiceRolling_CCCG2007/), inspected in the 2026-10-13 source audit, gives the short proceedings version as pages 141–144; TOPP's 141–148 citation is inconsistent with that metadata. The author BibTeX explicitly contains `unrefereed = 1`, alongside the 30-page full-version length and the note about the short proceedings version. This is a precise report of the author-hosted metadata, not an independent assertion about conference review practices. The 30-page full version must not be upgraded to a refereed journal publication.

De Biasi's [author post](https://www.nearly42.org/cstheory/rolling-a-cube-can-be-tricky/) dates from November 3, 2012; the [PDF](https://www.nearly42.org/vdisk/cstheory/rollingcubenpc3.pdf) is dated May 2012 and Version 0.03. In his [October 27, 2017 MathOverflow answer](https://mathoverflow.net/questions/87437/die-rolling-hamiltonian-cycles), the author described it as a blog draft not yet cleaned up and submitted to a journal. This is evidence about its publicly stated status in 2017. No later publication status was established by this bounded audit.

## 3. What the 2007 full paper proves, and what it does not

Primary source: [On Rolling Cube Puzzles, full version](https://erikdemaine.org/papers/DiceRolling_CCCG2007/paper.pdf).

- **Proposition 1, page 8:** when repeated visits are allowed, state-graph reachability is polynomial. Repeated visits remove the exact-once constraint central to TOPP 68.
- **Theorem 2, pages 8–9:** hardness for boards with labeled, blocked, and free cells. The construction spaces vertex cells apart with free connecting cells. The target does not require every free cell to be visited once.
- **Theorem 3, pages 9–12:** removes blocked cells but still uses free cells, including free exterior maneuvering in the argument. This is not the completely labeled rectangular target.
- **Section 4.1, pages 14–17:** elimination/cutting and blob statements begin with a version specifying the full die orientation on each labeled cell. They do not themselves settle the unrestricted label-only target.
- **Observation 2 / Figure 16:** nonuniqueness with blocked cells. **Observation 3:** bounded-size uniqueness enumeration, not a general uniqueness theorem. **Proposition 7:** cycle behavior near square-board corners; it is not a theorem about unrestricted path endpoints.
- **Theorem 8, pages 19–22:** a prescribed cycle-length problem on a fully labeled board. The reduction deliberately labels all unused squares 6 and proves that a valid cycle cannot use them. It encodes a cycle of length 4n rather than a cycle or path covering all rectangle cells. The construction therefore supplies exactly the wrong behavior for obligatory filler: its filler is unvisited.

The [original CCCG 2006 formulation](https://erikdemaine.org/papers/CCCG2005Open/paper.pdf), under “Rolling a Die,” labels a finite subset of an otherwise traversable plane. Its Figure 8 has a specified start configuration. TOPP later restricts to a filled rectangle. These are not interchangeable inputs.

[Yao and Uehara's 2021 paper](https://ipsj.ixsq.nii.ac.jp/record/210290/files/IPSJ-AL21182009.pdf), Sections 1.2 and 3–4, studies minimum moves between prescribed initial/final states with free rolling. It does not require exact-once coverage of an arbitrarily labeled rectangle.

## 4. Independent Figure 4 replay

### Extraction

The pinned De Biasi PDF's fourth page contains a 900 × 648 losslessly encoded image. Two grids have 30 columns and 9 rows. Cell spacing is 28 pixels. Digit pixels take a single exact RGB color, so the six glyph patterns can be identified from visually checked seed digits without OCR. All 270 digits match between the two drawings. The red and green path colors are distinct exact RGB values. Sampling their crossings at the grid separators yields a degree-two connected graph on all 270 cells for each drawing.

No labels or edges were inferred from the claimed theorem. The extraction is pinned to the exact PDF bytes. This edition supplies the authored audit and aggregate verification metadata, not source images, extracted board tables, path orders, or intermediate orientation traces.

### Exact physical check

Tuple order is (top, bottom, north, south, east, west), with north upward on the page. For example, an east roll maps (t,b,n,s,e,w) to (w,e,n,s,t,b). The die class used by the source net is represented by:

(5,2,6,1,3,4).

Both extracted cycles begin at the upper-left corner in the same state:

(4,3,2,5,6,1).

For each fixed cycle, all 24 rotations of each chirality were tried. Exactly one initial state in the source-net chirality succeeds; no initial state from the other chirality succeeds on either of these two particular drawn cycles. This last fact does not claim that every possible path or cycle on the board fails in the other chirality.

The complete verification establishes:

- 270 distinct cells and 270 legal cycle edges in each drawing;
- all initial and post-landing top labels match;
- the closing full orientation equals the initial full orientation;
- the two cycles assign the same full orientation at every cell;
- their undirected edge sets have symmetric difference of size 18, excluding reversal or cyclic reindexing as explanations of the difference;
- a second implementation using quarter-turn rotations of three-dimensional face-normal vectors agrees at every step;
- reversing either cycle is valid;
- omitting its closing edge gives a corner-start exact-once Hamiltonian path;
- wrong initial states and a changed first label are rejected.

### Two convention hazards

First, the source says a dash locates face 1 when the top is 2–5, and face 2 when the top is 1 or 6. In Figure 4 every dash is opposite that physical direction. The upper-left cell has top 4 and a rightward dash, yet its eastward path edge lands on label 1, requiring face 1 on the west. An exact pixel extraction confirms the same 180-degree discrepancy at all 270 cells in both drawings. The independently reconstructed physical orientations repair this without changing any board labels or path edges.

Second, the explicit reference state on Buchin full-version page 21 is top 1, south 2, west 3, or (1,6,5,2,4,3). Its rotation orbit is disjoint from that of De Biasi's unfolded net. Bare “right-handed” terminology should therefore not substitute for an explicit tuple when combining the two sources. A global exchange of labels 3 and 4, including the initial state, transfers a board and its valid motions between the two chirality classes. That is a transformation of the instance, not a claim that the original unchanged labels work for both dice.

## 5. De Biasi's blocked-cell reduction: interfaces and remaining obligations

The manuscript's target requires a cycle covering every labeled cell and prohibits visits to blank/blocked cells. Its Section 5 forward construction places the die in a chosen gadget; it does not establish the corner-start fixed-orientation path target.

The proposed reduction replaces a degree-at-most-three grid-graph vertex by a 138 × 138 macrocell. Degree-three vertices use a T-gadget, degree-two vertices a link-gadget, and degree-one vertices an endpoint-gadget. The named double interfaces are L1/L2, R1/R2, U1/U2, D1/D2. Adjacent macrotiles join paired ports horizontally or vertically. A T-gadget is intended to allow at most two port pairs; a link permits its two ports or an end-to-same-port return; an endpoint closes one pair. Traversing the abstract grid path forward and back then supplies a die cycle.

The basic and choice gadgets use forbidden interior cells. The stacked boundary in Figure 9 contains candidate crossings that are eliminated by cycle-specific reasoning. Figure 19 visibly has large unoccupied areas within its bounding rectangle. Merely enclosing the gadget array in a rectangle therefore does not remove blocked cells. A no-hole reduction would need labeled, obligatorily visited filler, prove that it does not add unintended crossings, and establish both implications with the exact path and starting conventions. No such construction appears in this manuscript.

The manuscript's reported Mathematica experiments and example boundary pairings are not a complete independent certification of all interfaces. The cited GraphML address, http://www.fractalmuse.org/rollingcubenpc/t-gadget.graphml, was not recovered: bounded web-tool attempts failed and both direct HTTP/HTTPS attempts returned 502. This audit does not elevate the blocked-cell hardness claim to a verified new theorem.

Further proof hygiene matters if those gadgets are reused:

1. In a label-only state graph, the requirement is one compatible orientation-state per cell. A Hamiltonian cycle visiting every lifted orientation-state is a different problem. Any reduced one-state-per-cell graph needs a justification that all other states and transitions are excluded.
2. Degree-two forcing applies to compulsory non-endpoint vertices. Path endpoints are exceptions. The cycle-only majority argument for boundary orientations is not an unrestricted path endpoint rule.
3. Cutting a chain-closing edge is safe only when it would close a proper subtour. If the chain already covers every required vertex, its closing edge may be the solution itself. The source's short rule needs this guard when implemented.
4. A connected spanning graph of maximum degree two can be a cycle as well as a path. The reduction's converse wording overlooks that distinction; a cycle still contains a Hamiltonian path after deleting one edge, so this wording alone is not a disproof of its conclusion.
5. Sound negative interface certification must include unintended entries, orientation choices, partially traversed gadgets, cross-boundary paths, and all feasible port connectivity patterns, not just the listed positive examples.

## 6. Bounded literature conclusion and scope

At the 2026-10-13 audit, TOPP labeled the main complexity question open, while its auxiliary uniqueness discussion has not incorporated the 2012 counterexamples. The MathOverflow thread records Pálvölgyi's earlier construction and De Biasi's later acknowledgment. Pálvölgyi's separate board was not independently replayed here.

The bounded search recorded in that audit, for the exact manuscript title and combinations of “rolling cube,” “fully labeled,” “rolling die,” rectangle, complexity, and NP-complete did not recover a later primary resolution. This is a source-status report, not a worldwide openness, novelty, or priority certificate.

Acceptance is limited to the model distinctions, explicit metadata observations, and the complete Figure 4 replay above. It is separate from the [structural theorem and its independent review](INDEPENDENT_STRUCTURE_REVIEW.md). This edition records exactly one newly documented substantive pass. The prior lifetime substantive-attempt count is unknown; this audit does not reset or infer it. No new literature search is represented by the preparation of this edition.
