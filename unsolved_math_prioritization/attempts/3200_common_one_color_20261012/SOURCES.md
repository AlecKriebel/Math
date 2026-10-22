# Source inspection ledger

Inspection date: 2026-10-12 UTC. This is a bounded context check, not an exhaustive literature review or a claim of priority.

## Sources used in the mathematical note

1. **Open Problem Garden, “List colorings of edge-critical graphs.”**
   https://www.openproblemgarden.org/op/list_colorings_of_edge_critical_graphs
   Reopened directly on the inspection date. The displayed conjecture has the intended nonconstant-list direction and defines criticality using the maximum degree and every single-edge deletion. This is the operational target adopted in the note.

2. **Bojan Mohar, “Edge-critical graphs and list colorings,” July 2001.**
   https://www.sfu.ca/~mohar/Problems/P7ListEdgeCriticalGraphs.html
   Reopened directly. Its displayed equivalence has the direction reversed. Equal lists cannot work under its own criticality definition, so the note records the wording issue without treating it as a mathematical counterexample.

3. **Hemanshu Kaul and Jeffrey A. Mudrock, “Criticality, The List Color Function, and List Coloring the Cartesian Product of Graphs,” arXiv:1805.02147v2, 7 August 2018.**
   https://arxiv.org/pdf/1805.02147v2
   Reopened the actual 27-page PDF and inspected Conjecture 6 and its preceding paragraph on printed page 11 (zero-indexed PDF page 10). It expresses Mohar's conjecture using strong chromatic choosability of the line graph. The indexing convention differs from the OPG convention. The preceding compressed definition, read literally, omits an explicit assertion that the graph is not already maximum-degree-edge-colorable; this note therefore states its own complete operational hypotheses and does not rely on that sentence alone.

No mathematical lemma in this packet is imported from these sources without proof. They establish the problem context; Sections 1–5 give a self-contained argument for the restricted theorem.

## Bounded search screen

Additional searches on the inspection date included:

- `"edge-critical" "lists" "common color"`
- `"edge-critical" "lists" "common colour"`
- `"subcubic" "list" "nonconstant" coloring`
- `"Mohar" "critical" "common" "lists"`
- `"critical" "subcubic" "odd cycle" matching`

The inspected results did not identify a directly applicable published common-one-color theorem. Many results concerned different notions of criticality, strong edge coloring, or maximum-degree-plus-one lists. This does **not** establish that the present restricted theorem is historically new, nor does it establish a current worldwide status for every case of the original conjecture. No such claim is made.

## Authored fixture provenance

The seven finite test graphs are previously authored local fixtures from earlier bounded checks: the seven-edge subdivision-of-K4 fixture, four ten-edge critical fixtures, the twelve-edge Petersen-minus-a-vertex fixture, and the thirteen-edge fixture containing a K2,3 support. The graph data were copied with vertex labels normalized and edge order preserved. The new Python and C++ checks independently recheck non-three-colorability and every edge deletion; they do not assume criticality from the fixture labels.

Fixture preparation used only two earlier authored fixture collections. No third-party paper text, private sources, or remote data were copied into the research packet. This prose edition excludes the implementations and raw collections; it preserves the authored source discussion and mathematical check scope.
