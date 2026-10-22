## Accepted restricted results

This authored proof/audit edition preserves complete analytical arguments
for weighted edge coloring with arbitrary real weights in [0,1]. The local
parameter b is the maximum optimal unit-bin count at a vertex, not the
ceiling of weighted degree. Adjacent edges may share a feasible color.

Simple forests have exact index b for b>=1. Multigraphs with forest
support, with arbitrary finite parallel multiplicity, admit 2B-1 colors
from supplied feasible local B-bin packings. Taking B=b is existential;
efficient computation of optimal bin packings is not claimed.

A cycle-breaking matching gives B+1 colors for simple cacti, including
non-bipartite ones. If b=1, one color suffices. The retained bipartite
unicyclic family proves the exact worst-case value b+1 for every b>=2.
A separate parallel forest-support family has exact index b+1 for every
b>=2; it attains 2b-1 only at b=2, not at all b.

The complete eleven-edge b=3 construction has exact index four. Its
specified frozen optimal root packing requires five colors to extend,
while recoloring gives four. This is a local-method obstruction, not a
counterexample to the Chung–Ross five-color target for b=3.

Empty graphs have index zero. Nonempty all-zero graphs use one color
under the convention that every edge is assigned. Disconnected components
reuse a palette, isolated vertices impose no constraint, and supplied
packings need not be optimal. All proof steps, parameterized construction
formulas and the full frozen construction are retained.

## Historical verification and reproduction boundary

The independent audit accepted the restricted results without a
substantive proof correction. It verified all seven central graph
instances, all 224 stored rejection assignments, 10,976 support-path
colorings on 2,744 graphs, 2,187 fixed-shape cactus weight-grid colorings,
and 59,377 rooted matching checks on the 10,026 cacti among all 33,868
labeled simple graphs through six vertices. The structural grid used
unit weights; it was not an exhaustive weighted grid on all those shapes.
Separate cross-checks covered 210 local-weight multisets and 1,536 palette
decisions. Nineteen semantic negative controls and edge-case controls
passed under normal Python, -O and -OO with identical substantive results.
Candidate programs were neither imported nor executed by the auditor.

The original generator's merge-event count was not reproduced because
it depends on local-packing tie-breaking. Independent graph/root counts,
feasibility, invariants and mathematical certificate conclusions agreed.
The counter is not a mathematical certificate or acceptance dependency.

The seven central graphs are specified mathematically by the retained
families and frozen example. Raw assignment tables, detailed graph and
load records, certificate packages, generated grid/control realizations,
code, copied source documents and images are excluded. The omitted
computational realizations cannot all be reconstructed from this edition
alone. It is not a complete computational reproduction package. Historical
checks support the written proofs and establish no unrestricted quantifier.
Preparation performed editorial and byte-integrity checks only, with no
new mathematical runs or scholarly-source retrieval/inspection.

## Sources and precise limits

Khan and Singh, [*On Weighted Bipartite Edge Coloring*](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.FSTTCS.2015.136)
(FSTTCS 2015), states the exact bin-packing target and general asymptotic
20b/9+o(b) progress. Feige and Singh,
[*Edge Coloring and Decompositions of Weighted Graphs*](https://www.microsoft.com/en-us/research/wp-content/uploads/2008/09/edgecoloring.pdf)
(2008), distinguishes bin-count and weighted-degree formulations.

Sannyasi, [*Improved Approximation Algorithms for Weighted Edge Coloring
of Graphs*](https://arxiv.org/abs/2012.15056v1), was directly inspected for
Theorems 10 and 11: b+1 for simple edge-disjoint-cycle graphs and
1.693b+12 for multigraph trees. No full-paper proof audit is claimed.

Huc, [*Weighted-Edge-Coloring of k-degenerate Graphs and Bin-Packing*](https://doi.org/10.1142/S0219265911002861)
(2011), has an [indexed abstract](https://sonar.ch/global/documents/62885)
with the formula missing and a total-weight parameter in prose. Primary
publisher access returned HTTP 403. Its exact theorem and proof remain
UNVERIFIED. No denied origin was bypassed. No precise Huc theorem is
imported, and no result is claimed novel. SOURCES.json records public
URLs, retained PDF hashes/sizes and the exact historical inspection limits.

The unrestricted Chung–Ross target remains unresolved by this work.
No novelty, priority, comprehensive literature or current-openness claim
is made. This AI-assisted manuscript is unrefereed. Acceptance means an
independent internal AI audit, not external human peer review, journal
acceptance or formal proof-assistant certification.

Exactly eight authored proof/audit/acceptance/provenance/verification
files are added under unsolved_math_prioritization/attempts/3000088.
QUEUE.md and unrelated paths are unchanged. Private coordination and
private personal data are excluded.

Base commit: `4b27092a448d53b61408355ce44ec38d103a1ce4`.

## Exact public-file identities

- `ACCEPTANCE.json`: 3,144 bytes; SHA-256 `8f037730738ba04531f15c0765327bb2b95dac996f1de1b816d01b20e07052fc`.
- `ACCEPTANCE.md`: 4,702 bytes; SHA-256 `6bcaae124daa11762cc5e6aadf9031e02238276e8f107f00dbe67094d05cd56f`.
- `AUDIT.md`: 13,350 bytes; SHA-256 `470d001582696dbdfe4a72c95702f9f628f970bdec03e89389c0ccd55dbb50f1`.
- `MANIFEST.json`: 1,347 bytes; SHA-256 `e0d17b18b1c16619e99110e2adf0335ae6f5cc9af27765cc95d3dfe342b670ad`.
- `PROOF.md`: 16,669 bytes; SHA-256 `3a17ec26eca0236a3f537da1410945c1749e2fbf49e35808b23049657d25b2b2`.
- `README.md`: 3,066 bytes; SHA-256 `6e3a41245a24ed62d0e9b55944c4c92cdcca2df8fbd5dbd1696ab5762a9b9cc3`.
- `SOURCES.json`: 5,586 bytes; SHA-256 `842372fa886e4d3df6570dbc178b40bf5b1b8f8c27502293f40034a23f094b7c`.
- `VERIFICATION.json`: 4,593 bytes; SHA-256 `ac03d07fd71c7d9c378b6cebc93d537bde6b0353a8b0e4c3865da7383c26f08c`.

MANIFEST.json lists all eight members and hashes the other seven; this body independently pins its digest.
