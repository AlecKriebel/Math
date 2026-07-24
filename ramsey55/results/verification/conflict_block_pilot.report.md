# Conflict-hypergraph ProbSAT block pilot

Evidence label: **REPRODUCIBLE COMPUTATIONAL OBSERVATION**

No valid order-43 \(R(5,5)\) construction was found.  The best independently
verified objective was \(E=C_5+I_5=2\).  This report describes a bounded
constructive search and does not establish nonexistence, basin exhaustion, or
local optimality.

## Concrete hypothesis and degree-switch diagnosis

The preregistered hypothesis was that the prior degree-switch pilot failed
because its exact labeled-degree invariant confined each run to a fixed-degree
fiber separated from other \(E=2\) states by objective barriers.  That pilot
performed 162,000 accepted moves and evaluated 2,099,473 candidates, including
317,654 compound candidates, but every final graph was the original start:
there was no positive-Hamming \(E\leq2\) state and no \(E\leq1\) state.

This is evidence for a search-neighborhood obstruction, not a formal proof of a
barrier.  The deliberately different test was therefore:

1. allow arbitrary edge flips and transient labeled-degree changes;
2. represent every monochromatic five-set as a conflict hyperedge;
3. use ProbSAT selection among all ten single-edge repairs, sampled two- and
   three-edge blocks within a conflict, paired edges from two conflicts, and
   global two-edge blocks;
4. use multi-conflict perturbations and breakout weights after stagnation.

The production criterion predicted at least one positive-Hamming \(E\leq2\)
final from the three \(E=2\) starts, and strict final-objective reductions from
both the catalog-derived \(E=104\) start and global \(E=231\) start.

## Correctness and preregistration

Before production:

- 150 sampled candidate blocks and 50 multi-conflict perturbations were checked
  against full recomputation over every five-set; weighted deltas, degree
  energy, rollback, and periodic full-objective audits also passed.
- Two 500-step calibration runs with seed 20260810 were semantically
  deterministic and produced byte-identical graphs.  Their retained graph
  stayed at \(E=2\) but was 35 edges from the start, demonstrating behavior not
  observed in the degree-switch pilot.
- Five starts were independently checked by direct Python enumeration and the
  separately compiled C++ recursive-bitset graph/complement verifier.
- The plan fixed production seeds 20260811 and 20260812, two 7,500-step
  restarts per start/seed, ten runs, and 150,000 selected moves total.

The frozen plan is
`results/benchmark_plans/conflict_block_multistart_v1.json`, SHA-256
`16e7a147f2cb5461796a930547e7dc1f3e7838fdc05b77a34bc1d0150247dabf`.

## Results

| Start | Seed | Initial \(E\) | Final \(C_5,I_5;E\) | Edge Hamming | Strict records |
|---|---:|---:|---:|---:|---:|
| exoo | 20260811 | 2 | 0,2;2 | 38 | 0 |
| exoo | 20260812 | 2 | 0,2;2 | 38 | 0 |
| incident | 20260811 | 2 | 0,2;2 | 37 | 0 |
| incident | 20260812 | 2 | 0,2;2 | 37 | 0 |
| core_kick | 20260811 | 2 | 0,2;2 | 37 | 0 |
| core_kick | 20260812 | 2 | 0,2;2 | 37 | 0 |
| catalog_line1 | 20260811 | 104 | 2,0;2 | 53 | 31 |
| catalog_line1 | 20260812 | 104 | 2,0;2 | 53 | 30 |
| global_baseline | 20260811 | 231 | 127,104;231 | 0 | 0 |
| global_baseline | 20260812 | 231 | 127,104;231 | 0 | 0 |

All ten runs completed their registered budgets: 150,000 selected moves,
3,490,007 evaluated move candidates, 219 multi-conflict shakes, and
329.376386 aggregate search seconds.  Every final graph passed:

- direct Python enumeration of every five-set and all ten pairs;
- the separately compiled C++ graph/complement verifier; and
- an independent audit of the objective, degree penalty, edge Hamming
  distance, graph6 payload, improvement trace, and step budget.

The output directory contains 50 small files totaling 55,601 bytes, below the
registered 20,000,000-byte limit.

## Evaluation

The cross-fiber mobility prediction passed strongly: all six production runs
from the three \(E=2\) starts retained positive-Hamming \(E=2\) graphs at
distance 37 or 38.  The incident and core-kick starts began with two clique
conflicts and ended with two independent-set conflicts.  In contrast, the
fixed-degree pilot never retained any positive-Hamming \(E\leq2\) graph.

The catalog reduction prediction also passed twice: \(E=104\) fell to \(E=2\)
in 30 or 31 strict records.  The global reduction prediction failed twice:
both \(E=231\) runs retained the original graph even after 712,175 evaluated
candidates and 44 multi-conflict shakes.  Thus the composite hypothesis is
only partially supported.  The experiment shows substantially better
cross-basin mobility and strong catalog-seed descent, but no improvement below
\(E=2\) and no universal descent from the global seed.

No \(E=0\) graph occurred, so the immediate canonical export and adversarial
construction audit were not triggered.  The runner was configured to write an
\(E=0\) graph immediately, stop the active and all later runs, repeat both
direct verifiers and the structural audit, then launch canonical export and
the adversarial artifact audit.

## Follow-up boundary

After this plan was frozen and production had begun, a separate audited corpus
of 22 structurally diverse \(E=2\) catalog-search outputs became available.
They were not added post hoc.  A clean follow-up can preregister a diverse
subset of that corpus and reuse this conflict-block method, preferably with a
targeted mechanism for escaping the persistent \(E=2\) plateau.  This report
does not preregister or launch that follow-up.

Machine-readable results are in
`results/verification/conflict_block_pilot_summary.json`, SHA-256
`1c275399e22479f1cebdd1f1d04718530d16ece85936980bd5e516b9e29ecec2`.
