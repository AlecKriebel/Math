# Three terminal distance interdiction

Problem identifier: 30000347 / OWR-1111-001.

The authored reduction proves NP-completeness of the decision problem for
simple undirected unit-length graphs, even with unit deletion costs and all
three original terminal distances exactly 3. The optimization problem is
NP-hard. The positive rational-cost version follows immediately.

Read PROOF.md for the full argument. SOURCE_AND_MODEL.md explains the exact
source match, the correction concerning the directed case, and the bounded
literature-search limit. SOURCE_MANIFEST.json records public-source metadata.
The checks directory contains a reproducible standard-library exact checker
and its passing results.

Manuscript state: author-complete proof, awaiting independent mathematical
review. This packet is not an acceptance report. It makes no priority claim.
One completed mathematical approach was needed: a vertex-cover reduction with
an exact optimum identity. Source inspection and computational checking are
not counted as additional research turns.

To repeat the checks, run Python 3 on checks/check_reduction.py. The output
replaces checks/check_results.json and records its execution time.

The packet contains authored text, an authored checker, check summaries, and
public verification metadata. It contains no copied source PDF or source text,
dataset contents, or private coordination material.
