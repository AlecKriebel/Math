# Result-ledger field semantics

`experiments.csv` is append-only. Its `number_of_evaluations` field records
the natural primary work unit for each experiment family:

- exact edge-delta evaluations for local search and radius scans;
- checked proof records for certificate replays;
- solver nodes for bounded SAT runs and timeouts;
- emitted/checked clauses for encoding-only generation.

The experiment family and parameter configuration identify the unit. New rows
use `N/A` for graph-specific fields when no output graph exists. Early
fixed-core rows retained the base-graph edge/degree values for lineage; those
historical rows are not rewritten.
