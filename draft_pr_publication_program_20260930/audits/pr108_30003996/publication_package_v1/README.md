# Aggregate root-dependent spanning-tree cost

This source package accompanies Alec Kriebel's research note, **NP-completeness of aggregate root-dependent spanning-tree cost**. The note proves NP-completeness for one common undirected spanning tree, with every independently supplied root cost charged over its entire induced orientation, even for costs in `{0,1,2}`. Uniform shift gives `{1,2,3}`. The finite checks supplement the proof.

The note answers Problem 1 in Volker Kaibel's November 2018 workshop contribution, whose Oberwolfach report was published on 17 December 2019. The classical formulation is credited through actually inspected primary expositions. No earlier proof was located in the bounded audit completed on 6 October 2026; no absolute-first or continued-open-status claim is made.

This folder is a **source-preparation snapshot**, not a certificate that the eventual PDF, archives or entire publication package are ready. The parent workflow must compile and render the paper and conduct fresh whole-package adversarial review rounds. AI tools were used extensively in solving, drafting, source checking, code generation, verification and adversarial audits. The manuscript has not received conventional human peer review or refereeing.

Files:

- `root_dependent_spanning_trees.tex`: self-contained current note; main parameter is `B=2`.
- `verify_exact.py`: Python 3.10+ standard-library exact diagnostic, explicitly using all roots and all selected arcs.
- `run_checks.py`: normal/optimized runner and six mandatory negative controls. It writes only a temporary directory unless an output path is explicitly supplied.
- `example_full_cost_instance.json`: all 208 root-arc entries of the eight-vertex, thirteen-edge four-clause example, with 384 trees, exact minimum 11 and threshold 10.
- `PROOF_BINDING.json`: exact current TeX and historical proof hashes used by the portable verifier.
- `PRIORITY_PROVENANCE.md` and `AUDIT_SUMMARY.md`: scope, attribution, historical limits, verification and status.
- `historical/`: exact copied audited proof and diagnostics, retaining their original `B=n+1` basis. The wrapper explains their superseded status prose.
- `verification_results/actual_run_receipt.json`: actual PID/UTC/exit/hash records for the successful adapted and historical replays and failing controls.
- `intended_zenodo_metadata.json` and `zenodo-deposit.json`: identical intended metadata and planned PDF/support-archive names. These are preparation files; neither planned upload artifact exists yet in this snapshot.
- `SOURCE_PREPARATION_MANIFEST.json`, `SHA256SUMS`, `SEAL.json`: authored-file byte/hash inventory and source-preparation seal.

Run from any working directory, substituting the package directory as needed:

```sh
python3 /path/to/package/run_checks.py
python3 /path/to/package/run_checks.py --include-historical
```

For a retained new receipt, choose an external output path:

```sh
python3 /path/to/package/run_checks.py --output /path/to/scratch/new-receipt.json
```

These commands preserve the sealed files. `verify_exact.py` also prints a JSON receipt without writing by default. Its `--output` and `--export-fixture` options write exactly their chosen paths; use a scratch directory to preserve a published snapshot. Direct invocation of the historical scripts would write receipts into their own copied directory, so use the temporary-copy runner for those scripts.

The suite normalizes repeated literals, discards tautologies, handles empty clauses and formulas, and relabels occurring integer symbols densely, including sparse labels. It tests all small trees for the audited structural identity, clause costs, decision equivalence, complete-cost cut/BFS agreement, transpose and shift. It checks single- and two-vertex cases and the 16 spanning trees of `K4`. Malformed literals are rejected. It makes no planarity, total-degree, fixed-active-root-count, approximation, neighboring Problem 2 or unrestricted global-optimum identity claim.

No third-party PDF, source extract, screenshot, raw web response or credential is included. The supporting source pins and URLs identify privately inspected originals without redistributing them. Retained preparation writes stayed in this folder; verification used disposable system-temporary scratch directories, removed on exit. No editor tab, external service or Git/index/queue state was changed during this preparation; no human contact or outreach was initiated or prepared.
