# SOURCE_FIRST_BASELINE

Sealed UTC: 2026-10-03T10:42:07.335115+00:00. Completion estimate: 25% of this independent family audit. The estimate concerns audit work, not a solution of Question 4.

No candidate TURN proof, verifier, checks, state, final-result file, historical review, parent verdict, or sibling findings were read before this seal. Only the frozen snapshot inventory and SOURCE_HASHES / addenda were inspected as routing. Primary PDFs were independently fetched; extracted text and rendered pages remain ignored in private/. Read scopes are recorded below.

## Original question and success criteria

OWR 41/2024, Louf's contribution, printed 2404-2406, Question 4 on 2405 asks: “Is there a nice geometric adaptation of Chapuy’s bijection to construct random surfaces?” The question does not define a unique formal target, specify that edges must remain geodesic, or prohibit additional geometric parameters. Its surrounding proposal seeks a controlled hyperbolic polygon law and an asymptotic parametrization of moduli. The preceding results compare normalized Weil-Petersson closed hyperbolic surfaces with Lebesgue metric-map surfaces of genus g, one face, perimeter 12g, using matching short-curve Poisson intensities (cosh t - 1)/t. Matching one statistic does not establish equality of models or existence of a geometric coupling. Any narrower obstruction must be labelled with its assumptions; it cannot by itself settle this open-ended question negatively.

For a proposed positive construction, I require a specified domain and probability law, a map from tree decoration and geometric data to an actual surface, local and global metric compatibility, verified topology, and a justified law of the output. For a proposed negative result, I require a stated construction class and an explicit contradiction valid throughout that class.

## Source model and conventions

The OWR reference [4] is Chapuy, PTRF 147 (2010), “The structure of unicellular maps ...”, arXiv:0804.0546; it is not arXiv:1006.5053. The former treats fixed genus and dominant maps (cubic schemes), opens intertwined nodes, and associates ordered disjoint triples of nonsingular tree vertices with opened maps. Opening retains edges while splitting vertices. A genus-g dominant map has 2^g g! opening sequences. Fixed-g dominance is not a uniform theorem for all growing g.

CFF, arXiv:1202.3252v5, Sections 2.1-2.5, uses rooted orientable unicellular multigraph maps and signed odd-cycle permutations on n+1 tree vertices. Their theorem provides 2^(n+1) copies of maps in graph-preserving bijection with signed C-decorated trees. The existence proof extracts a perfect matching after induction; the effective version is fractional. It does not supply a naive rotation-system concatenation for an arbitrary odd permutation. Rooting and the constant multiplicities matter for laws. Removing the fixed number n+1-2g of cycle signs gives the familiar 2^(2g) map-to-unsigned-tree multiplicity. Graph preservation permits transport of an edge-length assignment along a specified graph correspondence, but does not identify an ambient two-dimensional metric.

Janson-Louf, arXiv:2111.11903v2, Sections 1.3-1.4 and 2.4-2.5, studies uniformly rooted maps with n edges, g -> infinity and g=o(n). The graph distance is scaled by sqrt(12g/n), and the result concerns graph simple-cycle lengths. Their coupling conjecture explicitly seeks a polygon interpretation after removal of the fractal part; it remains a conjectural target in the source. Its regime must not be confused with g proportional to n or an arbitrary metric ribbon-graph Lebesgue law.

## Independent starting deductions and boundaries

A connected one-face orientable graph has V-E+1=2-2g and first graph Betti number E-V+1=2g. For g>=1 it contains graph cycles; for g=0 the graph is a tree. Attaching the sole face disk yields the surface, but keeping only a vertex quotient of the tree yields a one-dimensional graph. Identifying vertices without cyclic-order data cannot define the surface embedding. A specified positive edge metric defines a compact graph length space, including loops and parallel edges; it is distinct from the surface path metric, which may use face interiors. Smooth curvature -1 closed surfaces require g>=2 by Gauss-Bonnet; genus 1 and 0 demand different conclusions. A polygon gluing must have angle 2pi at every smooth vertex and compatible orientation-reversing side pairings. Cone-surface obstructions require the cone-angle and allowed-polygon hypotheses to be stated separately.

## Sources and read receipt

- OWR: https://publications.mfo.de/bitstream/handle/mfo/4255/OWR_2024_41.pdf?isAllowed=y&sequence=1 ; full Louf contribution printed 2404-2406; visual 2404 and 2405.
- Original Chapuy: https://arxiv.org/pdf/0804.0546 ; Sections 2.1, 3.1, 3.3, 4, 5 (including construction and inverse).
- Trisection refinement: https://arxiv.org/pdf/1006.5053 ; Sections 2.1-2.4, gluing/slicing and trisection counting proof. This independently fetched PDF differs from the candidate's 2010-PTRF hash, as expected because it is a separate paper.
- CFF: https://arxiv.org/pdf/1202.3252 ; full Sections 2.1-2.5.
- Janson-Louf: https://arxiv.org/pdf/2111.11903 ; full Sections 1.3-1.4, 2.4-2.5.

Primary-byte and extracted-text hashes are recorded in SOURCE_RECEIPTS.json; no source bytes are public artifacts.
