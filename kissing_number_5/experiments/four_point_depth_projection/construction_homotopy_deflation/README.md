# Construction homotopy, deflation, and thermal escape round

Status: **NUMERICAL EVIDENCE ONLY — NOT A KISSING-NUMBER CERTIFICATE**

This isolated round challenged the current numerical records for
\(N=41,42,43,44\) by three deliberately different asymmetric mechanisms:

1. cardinality homotopy obtained by splitting points of four exact,
   pairwise non-isometric 40-point codes;
2. direct \(N\times5\) factor optimization with per-edge slacks, dual/IRLS
   weights, and active-set deflation/re-entry; and
3. history-biased high-temperature population escape followed by all-pair
   epigraph polishing.

The preceding directory
`../construction_active_search/` was used read-only as the source of the
incumbent arrays.  This round did not modify it.

## Outcome

No run reached maximum inner product \(1/2\), and no run improved the
incumbent numerical record.

| \(N\) | Incumbent retained | Split-homotopy best | Best fresh deflation start | Best non-inherited thermal quench |
|---:|---:|---:|---:|---:|
| 41 | 0.5149946525121660 | 0.5208561441862484 | 0.5198598268736591 | 0.5170891098968629 |
| 42 | 0.5182411558622624 | 0.5239828168088867 | 0.5259930035292503 | 0.5241712212676627 |
| 43 | 0.5247096018290193 | 0.5322613968039385 | 0.5300476975776088 | 0.5273411070040114 |
| 44 | 0.5274577123235322 | 0.5382614322685925 | 0.5374852549898422 | 0.5368719389365934 |

For thermal escape the table gives the better of the mild and strong regimes.
Every thermal run attained zero Jaccard overlap with the inherited
near-maximum graph before quenching.  Thus the population left the labeled
incumbent graph basin, but this finite diagnostic does not establish global
search coverage.

The failed searches imply neither nonexistence nor any upper bound on
\(\tau(5)\).  All stored candidate arrays violate the kissing constraint by
margins far larger than binary64 rounding uncertainty, so exact-coordinate or
interval reconstruction was not triggered.

## Reproducible artifacts

- Split homotopy: [`split_report.md`](split_report.md)
- Factor/slack deflation: [`deflate_report.md`](deflate_report.md)
- Thermal population escape: [`thermal_report.md`](thermal_report.md)

Each report gives the exact seed rule or seed list, command line, software
versions, artifact hashes, solver scope, verifier scope, and safe-to-stage
manifest.  Discovery and verification programs are separate.  The split
verifier rescans all stored arrays with NumPy; the deflation and thermal
verifiers use only the Python standard library.

The independently checked regression suites contain 6 split tests, 7
deflation tests, and 7 thermal tests.  Their verification artifacts certify
binary64 storage and manifest consistency only; they do not certify solver
optimality or an exhaustive search.
