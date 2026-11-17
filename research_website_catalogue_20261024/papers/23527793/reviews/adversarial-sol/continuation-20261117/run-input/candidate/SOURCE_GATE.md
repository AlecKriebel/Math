# Public source and attribution summary

Numeric identity: 9700002 / AMR-096-0002, *Analytic toy model for a percolation-fragmentation congestion transition*.

The [primary problem](https://www.stat.berkeley.edu/~aldous/Research/OP/congestion.html) studies maximum admitted multicommodity demand under shared capacities and its marginal response to increasing traffic. It asks for an analytically tractable toy model coupling a rapid marginal decline with fragmentation of the spare-capacity graph. Cheapest capacity enlargement for doubled demand is one suggested mechanism. The [index](https://www.stat.berkeley.edu/~aldous/Research/OP/index.html) treats the question as conceptual rather than a uniquely formulated conjecture. Both pages were checked on 2026-10-03.

The present response is the explicitly specialized construction defined in turn 2. Its independent source-fidelity acceptance does not certify a uniquely correct model or historical novelty. See `CURRENT_DISPOSITION.md` for all retained limitations.

## Dataset provenance

Dataset: ulamai/UnsolvedMath, immutable revision `37e53eabe540fb458758e198be61634bd02ee008`.

Both complete files were rehashed against the repository provenance manifest before research:

- problems.json: 68,931,837 bytes, SHA256 `04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf`.
- research_results.json: 80,334,822 bytes, SHA256 `8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b`.

Review hash: `c12e014313d9b6f81187874ebb443cca7ea19deeb4461b7cb35b52bbb5e18f42`.
Statement hash: `324296be68f2f55c57e960fc869a3be4816989fb64bb2b9654670bb7a3b4d0b8`.

The imported report supplied unsuccessful source/literature triage, not a model or proof. It is prior credit, not an author turn. No raw dataset or third-party document is republished here.

## Prior work

- [Hassin-Zemel (1988)](https://pubsonline.informs.org/doi/10.1287/moor.13.1.80): random capacitated transportation feasibility. The independent review inspected the original formulation and first theorem; it does not assert theorem-by-theorem equivalence with the shrinking-window bound here.
- [Karp-Motwani-Nisan (1993)](https://pubsonline.informs.org/doi/10.1287/moor.18.1.71): probabilistic flow algorithms and random capacitated transportation.
- [Aldous-McDiarmid-Scott (2009)](https://www.stat.berkeley.edu/~aldous/Papers/me122.pdf): uniform multicommodity flow in a random-capacity complete graph.
- [Khandwawala-Sundaresan (2010)](https://doi.org/10.1239/jap/1269610826): asymptotically optimal utility for random-capacity multicommodity flow.
- [Hamedmoghadam et al. (2021)](https://www.nature.com/articles/s41467-021-21483-y): demand-weighted percolation and bottlenecks.
- [Di Meco et al. (2024)](https://arxiv.org/html/2405.16100v1): analytical and numerical random-walk congestion models.
- [Chen-Wu (2024)](https://www.mdpi.com/2227-7390/12/20/3247): transportation congestion propagation and capacity upgrades through percolation algorithms.

The literature search is bounded, not exhaustive. Standard transport feasibility, min-cut arguments, and concentration are not claimed as new; novelty of the combined model is not established. The frozen candidate's older incomplete identification of the Northwestern antecedent is corrected additively by the Hassin-Zemel citation above.
