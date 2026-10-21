# Independent pre-freeze package audit

Audit date: 21 October 2026.

## Verdict

PASS for the stated, variant-specific publication scope. No outstanding mathematical-scope or package-integrity blocker was found. This review checks the prepared package against the accepted authored mathematical audit and independently verifies the finite-check transformation and executions. It does not establish peer review, priority, exhaustive literature coverage, or a new proof of every theorem. A frozen manifest must be generated and verified after this report is written; manifest correctness is not claimed by this pre-freeze review.

## Files reviewed

Read the complete contents of README.md, VARIANT_LEDGER.md, ACCEPTANCE_AUDIT.md, SOURCE_METADATA.json, DATASET_METADATA.json, CHECK_PROVENANCE.json, CHECK_RESULTS.json, check_n1_original.py, check_n1.py, and run_checks.py. Re-read the final README and hardened harness after the changes identified below. This authored report is the only package file written by this reviewer.

ACCEPTANCE_AUDIT.md is byte-for-byte identical to the accepted source audit. The original packaged check is byte-for-byte identical to the authored check named check_n1_independent.py in that audit; the README explains the packaging name difference.

## Mathematical and attribution boundaries

The principal variant ledger has exactly four outcome rows:

1. Same fixed N, continuous loose embedding: the implication from all finite subsets is false for every positive N, by the audited countable examples.
2. Original ordinary uniform/topological embedding reading: not resolved by these examples or this audit; those countable examples uniformly embed into the real line.
3. Some possibly larger finite target dimension: not resolved; the N=1 example has a planar loose embedding.
4. Universal compact connected Riemannian finite-subset assertion: false, because every intrinsically at-least-two-dimensional flat torus fails the finite-subset hypothesis in every finite target dimension.

The longer acceptance audit also discusses subsidiary consequences and excluded infinite-dimensional scope. Those are not extra administrative resolution classifications. The README restricts its administrative already_solved label to the first and fourth variants and explicitly rejects a blanket historical resolution.

The package credits Alper Ferudun, the manuscript title, public manuscript URL, and 20 October 2026 date. It explicitly states unrefereed and AI-assisted status, disclaims a new discovery by the package authors, and does not certify priority or peer review.

Definitions preserve the all-pair equality biconditional, including disjoint and diagonal pairs, rather than order preservation or merely one-way equality preservation. Global continuity is required; the discontinuous equality-pattern injection is not misclassified as LE. A single fixed N serves every finite subset, with no common compatibility, normalization, distortion bounds, or continuity moduli assumed. The higher-dimensional argument is not used to answer the larger-target question.

Intrinsic torus dimension is distinguished from target dimension, the metric is the intrinsic flat geodesic metric, and circles are explicitly excluded from the negative theorem: their planar chord map gives LE and H_2. The package does not assert that every manifold fails, does not claim one finite witness fails in every target dimension, and claims no general explicit witness-size bound.

## Exact AST and execution checks

Independently parsed both check scripts with Python ast. Replaced each original Assert(test, msg) with If(Not(test), Raise(AssertionError(msg or the fixed failure message))) in memory, then compared the complete transformed tree with the hardened script using ast.dump with location attributes excluded. The trees are identical. Exactly four original assertions exist and no Assert remains in the hardened script. Thus every non-Assert AST node, test expression, loop, assignment, update, distance formula, point construction, statement order, and non-assert control-flow structure is preserved, with only the explicit assertion-enforcement wrapper substituted.

The four preserved conditions are:

- 2 * max(ds) <= sum(ds)
- x > 0 and y > 0
- x not in forward or forward[x] == y
- y not in backward or backward[y] == x

The script hashes match CHECK_PROVENANCE.json. Normal execution of the original succeeds. Normal and optimized (-O) execution of the hardened script both exit 0 and check all 7,140 unordered triples and 630 unordered positive-distance pairs on Y_35 with exact rational arithmetic. The inherited output calls the latter “pair classes”; the actual loop enumerates 630 pairs and verifies their complete equality partition, not 630 distinct distance values. No evidence is claimed from the optimized original, whose assertions would be removed.

Ran the final harness in a temporary copy so package results were not overwritten. Its newly produced JSON exactly matches CHECK_RESULTS.json. Baseline normal/-O runs exit 0. Replacing the nonadjacent source-distance formula with Q(100) causes the triangle check to raise AssertionError in both modes. Perturbing f(35) by one causes the forward-equality check to raise AssertionError in both modes. All four mutated runs exit 1, have no success output, and terminate with the exact exception message “AssertionError: Exact finite sanity check failed”. The triangle failure occurs at hardened-script line 22 and the equality failure at line 30.

Review finding fixed before approval: the initial harness required the expected nonzero exit but only recorded the failure type. The final harness also requires AssertionError in stderr for mutated variants. This change was inspected and independently rerun successfully. The direct exception checks above additionally verified the actual final exception and intended check location, not merely a nonzero status.

These computations are finite sanity checks, not the all-index mathematical proof.

## Metadata and publication-content inspection

Independently recomputed SHA-256 and byte length for all six retained local public-source artifacts referenced by SOURCE_METADATA.json; all match. Verified both check-script provenance hashes. DATASET_METADATA.json is structurally identical to the accepted metadata record, including exact identifier/source key and one problem-record match versus zero research-result matches. This package review did not independently reread or rehash the full corpora and does not claim to have repeated historical downloads or inspection actions.

Inspected all prepared file contents for publication scope. The package contains authored assessment and supporting authored code, variant/status documentation, and public verification metadata. It contains no copied paper PDF or extracted paper text, dataset contents, private-source contents, private personal information, or private coordination files. Public source filenames, URLs, hashes, byte counts, retrieval descriptions, and match counts remain metadata rather than source-content publication.
