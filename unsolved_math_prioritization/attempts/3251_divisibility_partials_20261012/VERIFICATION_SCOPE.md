# Exact verification scope

These are the previously accepted finite audit outcomes. Edition preparation is not a new mathematical research round and does not reclassify reported finite experiments as all-order proofs. Complete proofs and substantive audits are distributed separately.

## Structural graph universe

All labeled simple graphs on orders zero through six were enumerated: 1+1+2+8+64+1024+32768 = 33,868 graphs. Exactly 33,861 are nonedgeless, excluding one edgeless graph for each order. The independent checker did not import the author's implementation. Both ran in normal Python, -O, and -OO, giving the same mathematical counts:

- 2,012,232 admissible nonempty-clique precolor instances in the stated chi≤2omega−2 universe.
- 206,970 clique-separator identities, counted per graph and nonempty clique separator.
- 63,242 eligible module-coloring constructions.
- 120 blocked deletion colorings for the twelve labeled minimal indivisibles of order five, which are labeled five-cycles and are not odd-hole-free.
- Zero minimal-indivisible clique-separator instances. The separator-obstruction numerical tests are vacuous in this range; their proofs carry the general claims.

Additional independent tests checked 6,060 admissible precolorings, including the empty clique, of complete graphs of order 2k−2 for k=2,3,4,5. These cover the more general precolor lemma when the graph's clique number can exceed k. The tests also cover all four boundary assignments for two K4s sharing an edge; blocked extension for two K4s meeting in one vertex; direct antihole splits of orders 7,9,11,13; and 34 abstract swap-orbit set systems.

There were 24 integrity controls per interpreter mode: one pristine positive and 23 required rejections. Same-length mutations, missing/extra members, malformed input, symlink cases, and deliberately false authored/independent mathematical checks were included. Mathematical negative controls failed without creating a result artifact. The pre-freeze Python-assert defect had already been corrected; accepted gates use explicit failures.

## Simple labelled uniform hypergraph universe

The 11,390 cases are rank-tagged simple hypergraphs on fixed labelled vertex sets, with 0≤n≤7, 3≤r≤n and maximum incidence at most two. There are no admissible rank/order pairs below three vertices. Each empty family is counted once per admissible (n,r); isolates are allowed. The exact independently generated case set and the author's instrumented visited set agree with no duplicates, rather than merely having the same total. Exactly 6,170 satisfy the Hall union condition.

| Vertex count n | Rank r | Hypergraphs | Hall subclass |
|---:|---:|---:|---:|
| 3 | 3 | 2 | 2 |
| 4 | 3 | 11 | 11 |
| 4 | 4 | 2 | 2 |
| 5 | 3 | 86 | 56 |
| 5 | 4 | 16 | 16 |
| 5 | 5 | 2 | 2 |
| 6 | 3 | 766 | 511 |
| 6 | 4 | 136 | 136 |
| 6 | 5 | 22 | 22 |
| 6 | 6 | 2 | 2 |
| 7 | 3 | 8,506 | 3,571 |
| 7 | 4 | 1,576 | 1,576 |
| 7 | 5 | 232 | 232 |
| 7 | 6 | 29 | 29 |
| 7 | 7 | 2 | 2 |

Every case was checked by the authored Euler construction, an independent Euler construction, and a separate brute-force two-coloring oracle. Hall status was checked by exhaustive edge-subfamily tests and independent breadth-first matching.

## Additional hypergraph witnesses

- Fano: seven vertices, seven triples, twenty-one pairs, all 128 colorings, and all 35 four-sets checked.
- G(5,4): fifteen vertices, thirty-two graph edges, five maximum K4s, thirty shadow edges, and a core C5. All 32,767 nonempty vertex subsets were examined. Perfect-elimination order, explicit division, absence of induced cycles of length at least four, and strong odd incidence cycle were checked.
- Three-sun: exactly four maximum triangles and the strong incidence triangle were independently checked.
- Hall witness: twelve vertices, six edges of size six, every vertex incidence three, and all 64 subfamilies checked; a matching covers the two labelled copies of every edge.
- Repeated/nonuniform scope: all 2,921 multisets of subsets of size at least three on labelled vertex sets of size at most six, with maximum incidence two; 94 cases contain duplicate edges and 1,785 are nonuniform.
- Odd Euler parity: a seven-edge real dual component with degrees 4,4,6, no auxiliary incidence, plus an isolated hypergraph vertex.
- The four three-element stars of K4 violate the full-family Hall union condition but remain two-colorable by the incidence-two theorem.

The independent audit and original author executable each passed normal Python, -O, and -OO with mode-identical mathematical outputs. Forty-two independently authored negative cases per mode were all rejected, totaling 126 rejections. Controls cover every original packet member's omission, symlink replacement and tampering; external anchor failures; root/ancestor symlinks; extras; duplicate JSON keys; mandatory fields; malformed Fano, graph, elimination-order, hole, coloring, Hall and scope inputs; altered expected counts; and missing required arguments. Where appropriate, semantic mutants were freshly repinned to show rejection beyond stale hashes. The author's separate 36-control record and terminal evidence were independently checked.

## What these tests do not establish

The finite tests are regression evidence for the stated constructions and formulations. They do not establish all-order 2-divisibility, a general clique-cutset theorem, or a classification of all possible obstructions. The integrity checks certify the pinned static bundles and tested failure modes, not immunity to concurrent filesystem races, every malformed encoding or replacement of both trusted anchors. No raw enumeration corpus, original executable or terminal record is distributed in this prose-only edition.
