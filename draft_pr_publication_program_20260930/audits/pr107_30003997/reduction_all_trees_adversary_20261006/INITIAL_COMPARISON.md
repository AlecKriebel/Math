# Pinned independent initial comparison

Timestamp: 2026-10-06T04:07:52.641220+00:00

This comparison was written after SOURCE_FIRST.md and after reading only the candidate PROOF.md and source_record.json, before any original review, author replay, or other current audit family's report.

## Initial result

The candidate formulation agrees with literal source Problem 2: destination-specific arc charges on every root-to-vertex path of a spanning out-arborescence. It does not substitute source Problem 1. The exact general theorem is finite binary-rational decision NP membership plus NP-hardness already on costs {0,1} and a simple four-layer DAG with consecutive arcs, universal root reachability, and nonroot indegree at most 3. The +1 transformation has a plausible fixed path-length offset 4n+3m. No immediate counterexample was found.

The all-tree mechanism is transparent: each literal marker has one forced root parent; each variable vertex has exactly one truth-marker parent; each clause vertex chooses exactly one incident variable parent. Because the graph is acyclic and strictly layered, every independent set of such parent choices is a root-spanning arborescence. This should give a bijection between all trees and (global assignment, one selected distinct variable for each clause), not merely a canonical-subfamily argument.

## Challenges to resolve formally

1. Prove that the assignment/selection characterization is exhaustive and bijective for arbitrary size, and derive the literal charge from the actual table.
2. Check all syntactic preprocessing and constant formula cases. Deleting tautologies and duplicate identical literals does not by itself remove an empty clause. The candidate acknowledges fixed yes/no handling for trivial constants but does not exhibit those instances. This looks like an expository boundary omission rather than a central failed reduction; I will produce checkable fixed instances and classify severity explicitly.
3. Derive polynomial dense encoding size in the true source input bit length, including relabeling sparse or binary-indexed variable names. Just saying n is the number of named variables could accidentally count unused declared IDs rather than actual input occurrences.
4. Provide exact rational verifier bit bounds; finite sums can be computed exactly in polynomial bit complexity even with negative rational costs.
5. Check the strong NP-hardness assertion under bounded numeric inputs, and the positive offset for every tree rather than optimum alone.
6. source_record.json's old background describes root-dependent spanning trees; the candidate proof correctly identifies the directed fixed-root target. Do not confuse stale triage prose with a theorem or priority certificate.

## Independence and status

No original review or other current family material has been read. Candidate and source-record hashes are pinned in INITIAL_COMPARISON_PIN.json. Completion estimate: 25% for verification audit. Historical priority, novelty, and literature completeness remain outside this audit's theorem-verification scope.
