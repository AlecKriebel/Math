# Greedy spanning trees: accepted partial results, general question unresolved

Problem **30001934**; associated aggregate **30001932**. The existing research budget is **5/5**, with zero new research approaches. This packet does not claim an all-graph solution, a counterexample to the original existence question, novelty, current openness, or journal acceptance.

## Mathematical result

Read the complete, unchanged [mathematical report](author/authored/MATHEMATICAL_REPORT.md) and [independent audit](audit/authored/AUDIT_REPORT.md). The audit requires no correction and accepts:

- the exact maximum-coefficient formula;
- a positive integral maximum for every 0–1 integer-decomposition polytope when k≤4;
- an integral maximum for every connected multigraph with at most four vertices;
- an integral maximum for K5 and its nonempty parallel extensions, with loops allowed.

All statements use the report's **explicitly repaired domain λ∈[0,k] and 0P={0}**. This is not silently identified with the source's literal lower bound λ≥0. A maximum of zero counts as integral. The all-k positive-step statement is stronger and unproved here. The K5 construction uses completeness and does not establish the result for arbitrary five-vertex graphs.

The three fixed examples reject auxiliary selection rules: choosing one arbitrary tree, choosing a globally maximum coefficient, or choosing a maximum-total-weight tree. Each example still has integer-maximizing trees and is **not a counterexample to the original question**.

## What is preserved

- The full accepted report, original verification report, exact author model/core checker, fixed selection certificates, fixed K5/K6/K7 adversarial records, and search-status summary.
- All **19** files in the independent audit allowlist, byte-for-byte, plus that audit's public manifest. This includes the complete audit, its acceptance and source-inspection metadata, original checker code, and every mode-specific audit output.
- Two current copies with **path-only** adaptations: the independent audit reads the packet-relative author inputs; the saved-record checker reads the packet-relative fixed records. Their cumulative patches are provided and were checked with zero fuzz. Original copies remain preserved.

The audit manifest describes its original public audit inputs. It is historical evidence; the authoritative inventory of this complete delivery is PUBLICATION_MANIFEST.json. The historical author manifest is not included because this deliberately narrower packet omits discovery scratch files and redundant logs. Its public hash remains in the unchanged audit as an identifier of the accepted original packet.

Source text/PDF bodies, external datasets, private sources, private coordination and their identifying metadata, unrelated work, and QUEUE changes are excluded. The JSON certificate vectors here are our authored fixed mathematical examples, not an imported external dataset.

## Verification boundary

The current replay has four explicitly identified suites in each of normal Python, -O and -OO:

1. Author core: 2,680 points, including 1,680 feasible K4 inputs at k≤4 and 1,000 seeded K5 inputs.
2. Saved adversarial points: exact Fraction replay of all 125, 1,296 and 16,807 trees, with respectively 54, 623 and 6,909 integral endpoints.
3. Independent fixed-certificate audit: every one of 157 recorded selection endpoints, every binding witness, 44 small connected labeled graphs, 60 K5 triple/crossing choices, 24 parallel-extension trees, and boundary fixtures. Membership and endpoints use graph traversal and every edge-subset rank inequality, independently of the author's vertex-subset implementation. Nine false-claim controls are rejected with their exact exception types and reasons.
4. Actual source-mutation suite: five distinct in-memory edits to the author's exact model are compiled and rejected on fixed fixtures. Omitted facets, rounded endpoints, omitted selected-coordinate bounds and replaced zero endpoints disagree with the independent endpoint oracle. Omitting the mass bound fails closed on the rank-zero fixture with the exact expected ValueError. These are actual source edits, not merely claimed negative examples.

The suite dispatcher loads only explicit authenticated absolute files; it never adds cwd or a source directory to sys.path. The independent rejection wrapper records the exception already raised by the original fixture and invokes the original rejection handler unchanged. It does not alter mathematical predicates. FINITE_CONTRACT.json fixes complete expected raw outputs independently from the accepted historical outputs and explicit reason contracts. Every fresh suite must match all stdout/stderr bytes, exact recursive JSON types, identities, counts and reasons. No output normalization, skipped suite, empty success, XFAIL, PASS-only result or bool-as-integer equality is accepted.

The discovery searches are **NOT_RUN**. In particular the historical bounded-box/sampling totals are not freshly reproduced, floating-point MILP infeasibility statuses are not exact certificates, and the interrupted K7 discovery run remains interrupted. The output-writing certificate generator is **NOT_RUN**; the entire existing certificate is independently verified instead. The original snapshot-building audit harness, source retrieval, source bodies, external datasets and formal proof-assistant verification are **NOT_RUN**. None is a prerequisite for this fixed-certificate replay. Universal partial theorems rest on the written proofs and independent audit; finite checks do not prove the remaining all-graph assertion.

## Fixed external trust and noncircular sealing

Obtain BOOTSTRAP.py from this delivery, then authenticate its SHA-256 against the separately published review/PR receipt before running it. Keep that authenticated copy outside the packet. The bootstrap hardcodes the complete publication manifest hash and authenticates both verifier and control harness before either can execute. The manifest commits to every other delivered member except itself and the bootstrap; the external bootstrap pin closes that chain without circular self-hashing. A freshly resealed attacker manifest cannot replace the fixed external pin.

Verification requires Python 3.12 as tested, real UID=effective UID=1000, files 0444 and every packet directory 0555. The verifier attempts actual creation in every directory, append-open of every file, and deletion of an existing file, requiring physical PermissionError errno 13 throughout. This is byte immutability for the tested run, not a claim that an owner cannot later chmod its own files.

After setting those read-only modes, run the external copy with the absolute packet path:

    python -I -S -B /absolute/trusted-bootstrap.py /absolute/packet
    python -I -S -B -O /absolute/trusted-bootstrap.py /absolute/packet
    python -I -S -B -OO /absolute/trusted-bootstrap.py /absolute/packet

Run the authenticated publication controls using:

    python -I -S -B /absolute/trusted-bootstrap.py --controls /absolute/packet

Repeat that command with -O and -OO. The controls distinguish inventory/integrity mutations, direct schema/scope mutations, and direct output-comparator mutations. They also run the full positive baseline in a hostile cwd and environment containing fake source/standard-library modules and require complete raw output equality plus an untouched import sentinel. Every mode records the complete before/after file-hash inventory.

CHECK_RUNS.json and the mode-specific reference files are pre-seal capture evidence. Final sealed controls and relocated-diff replay receipts live outside the delivered inventory, are pinned in the review/PR body, and do not feed a circular acceptance assertion back into the packet.

## Public sources

- [Combinatorial Optimization, Oberwolfach Report 53/2011](https://ems.press/content/serial-article-files/46369), Dion Gijswijt with Guus Regts, Question 3 on printed page 3027.
- [Dion Gijswijt and Guus Regts, Polyhedra with the Integer Caratheodory Property](https://www.math.ucdavis.edu/~deloera/TEACHING/READINGSEMINAR/PAPERS/gijswijt%2Bregts.pdf), Journal of Combinatorial Theory, Series B 102 (2012), 62–70.
- Chaourar's [publisher abstract](https://www.sciencedirect.com/science/article/pii/S0195669802906049) was inspected historically; its full body was not retrieved and no uninspected excluded-minor theorem is imported.

Public hashes, byte counts and inspection history appear in the preserved source metadata and audit. They are historical source checks, not a new publication-stage literature survey.
