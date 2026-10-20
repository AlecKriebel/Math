# Source gate: OPG-401 / catalog ID 3227

Prepared 2026-10-20 UTC. Public-source identity and inspection record.

## Identity and exact scope

Problem identity: Open Problem Garden node 401; catalog ID 3227.

**Recovered conjecture:** Every finite simple triangle-free planar graph G with maximum degree at most three satisfies χ_c(G) ≤ 20/7.

The canonical OPG entry explicitly specifies girth at least four and maximum degree at most three. Thus “maximum degree three” is not a restriction to 3-regular graphs. Squares and degree-two vertices remain in scope. This is circular **vertex** coloring, not fractional coloring, circular edge coloring, total coloring, or signed coloring.

For proof work the target can be encoded as a map c: V(G) → Z/20Z with 7 ≤ |c(u)−c(v)| ≤ 13, using representatives in {0,…,19}, on every edge uv. Equivalently the target is the circular clique K_(20/7). This is the standard (20,7)-coloring formulation, not an assertion of a homomorphism to the dodecahedron.

## Original sources and verified locators

1. **Open Problem Garden, OPG node 401**, posted by mdevos on June 20, 2007; attributed to Mohammad Ghebleh and Xuding Zhu. Canonical URL, recovered by following the category-page link and successfully opened:
   https://www.openproblemgarden.org/op/circular_chromatic_number_of_triangle_free_planar_graphs
   The problem and explanatory paragraphs are at extracted lines 29–34. The bibliography is empty. The page still presents the question unresolved; this is a live problem-page observation, not independent certification that no later proof exists. The dodecahedron gives equality 20/7.
   Node identity is corroborated by the indexed reply page https://www.openproblemgarden.org/comment/reply/401 .

2. **Xuding Zhu, “Chi_c of triangle free planar graphs of maximum degree 3 or 4.”** Author-hosted original problem statement:
   https://www.math.nsysu.edu.tw/~zhu/open-problems/chic-k3free-planar.htm
   Search-indexed text explicitly gives the same ≤20/7 conjecture and dodecahedron motivation. It also notes the Petersen graph has circular chromatic number 3, so omitting planarity invalidates this bound. This page is historical and undated in the retrieved text; do not claim a proposal year from it. Direct HTTPS and HTTP opens returned internal fetch errors, although indexed primary-source text was available. Accordingly this is content-verified through search, not a successfully downloaded page.

3. **Mohammad Ghebleh, _Theorems and Computations in Circular Colourings of Graphs_, Ph.D. thesis, Simon Fraser University, Fall 2007.** Chapter 6, printed p. 65, Conjecture 6.1, states the exact target. Indexed primary thesis PDF:
   https://citeseerx.ist.psu.edu/document?doi=f0f701d98271ecae731d2c97ec93364305031d86&repid=rep1&type=pdf
   Indexed title-page text verifies author, institution, degree, and year. Indexed p. 65 verifies the conjecture number and statement. Direct PDF opening failed; no complete PDF, hash, byte count, or visual inspection is claimed. This establishes a primary written appearance, not chronological priority over Zhu or the June 2007 OPG posting.

## Nearby results that must not be substituted

- **High-girth subcubic planar graphs:** The thesis discusses Theorem 6.11 giving χ_c < 3 for girth at least nine. Both the stronger girth hypothesis and weaker conclusion differ from the exact OPG target. It does not prove ≤20/7 for girth four.
- **Nonplanar cubic graphs:** Petersen already has χ_c=3. Nešetřil’s separate high-girth pentagon question seeks a 5/2 bound for sufficiently high girth without planarity. It is not this conjecture.
- **General planar high-girth graphs:** Jaeger-type circular-coloring questions change both degree and girth assumptions. Their girth thresholds must be checked in their own sources rather than imported here.
- **Maximum degree four:** OPG separately lists Zhu’s size-dependent χ_c≤3−1/k question for |V(G)|<3k. It is not a proposed improvement or reformulation of the subcubic 20/7 bound.
- **Fractional coloring:** Dvořák, Lidický, and Postle’s _11/4-colorability of subcubic triangle-free graphs_ proves a fractional bound, with two exceptions in the connected general class; this does not establish a circular bound. Primary arXiv record successfully opened: https://arxiv.org/abs/2204.12683 . The record identifies the 2025 journal publication, DOI https://doi.org/10.19086/aic.2025.5 (direct DOI fetch failed). Numerically smaller fractional bounds cannot be promoted to circular bounds: χ_f≤χ_c, not the reverse.

## Status assessment and gate decision

**Exact statement and source identity: recovered. Current resolution: no resolution located; retain provisionally open, with historical-source caveat.** Targeted searches on 2026-10-20 for the exact title, “triangle-free”/“20/7”, Ghebleh/Zhu with the bound, and “subcubic planar”/“circular chromatic” found the original sources and nearby fractional, edge-coloring, and high-girth literature, but no primary paper proving or disproving the exact statement. Searching for recent 2023–2025 literature did not locate a resolution. Absence from these searches is not proof of open status.

The live OPG page and exact primary statements are sufficient to remove the missing-statement/source-identity blocker. A stricter gate requiring complete thesis retrieval remains pending; do not describe the thesis as fully inspected. No claim of exhaustively verified current open status is made.
