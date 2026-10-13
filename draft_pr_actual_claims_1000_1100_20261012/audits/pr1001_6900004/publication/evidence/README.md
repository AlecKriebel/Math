# Evidence provenance and portable locations

The review records here are preserved byte-for-byte from their original
stages. Machine-local absolute paths, former filenames and references to
research folders inside those records describe historical working locations;
they are **not** a claim that those paths exist in this archive. This index
provides the portable counterparts. The current proof and scope are in
[the manuscript](../research_note.tex) and [the supplement](../SUPPLEMENT.md).

| Historical record or name | Included counterpart and role |
| --- | --- |
| Submitted head, delivery-file pins | [SUBMITTED_PINS.json](SUBMITTED_PINS.json) binds the original 44-file PR snapshot; it is not the present package inventory. |
| Original `REPORT.md`, `ACCEPTANCE.md`, `STATUS.json` | [REPORT](submitted/REPORT.md), [ACCEPTANCE](submitted/ACCEPTANCE.md), [STATUS](submitted/STATUS.json): original theorem and retained interpretation hold, preserved as stage history. The fresh reconciliation does not rewrite these historical claims. |
| Root independent matrix proof | [ROOT_MATH_AUDIT.md](ROOT_MATH_AUDIT.md): root derivation and stage-specific remaining gates. |
| Fresh mathematical reviewer `REVIEW.md`, `VERDICT.json`, `MANIFEST.json` | [review](INDEPENDENT_MATHEMATICAL_REVIEW.md), [verdict](INDEPENDENT_MATHEMATICAL_VERDICT.json), [input pins](INDEPENDENT_MATHEMATICAL_INPUT_PINS.json). Their original report path is the submitted report above; their checker is [independent_exact_check.py](../checks/independent_exact_check.py), with [expected output](../expected/independent_exact_check.json). |
| `FINITE_REPRODUCTION.json`, `SOURCE_MUTATIONS.json` | [root baseline comparison](ROOT_FINITE_REPRODUCTION.json), [actual source mutations](ROOT_SOURCE_MUTATIONS.json). Full fresh baseline stdout/stderr are in [root_reproduction](root_reproduction/); original UID1000 reference stdout/stderr are in [original_reference](original_reference/). These records do not claim replay of the historical permission-control harness. |
| Source reviewer `RECONCILIATION.md`, `RECONCILIATION.json` | [source reconciliation](SOURCE_SCOPE_RECONCILIATION.md), [decision](SOURCE_SCOPE_RECONCILIATION.json). Historical `inputs/pr1001` REPORT/ACCEPTANCE/STATUS passages refer to the submitted counterparts above. |
| Source reviewer `SOURCE_RETRIEVAL.json` | [ORIGINAL_SOURCE_RETRIEVAL.json](ORIGINAL_SOURCE_RETRIEVAL.json) gives journal/manuscript URLs, retrieved-byte identities, extraction hashes and inspection extent. |
| Priority reviewer `REVIEW.md`, `VERDICT.json` | [PRIORITY_AUDIT.md](PRIORITY_AUDIT.md), [PRIORITY_VERDICT.json](PRIORITY_VERDICT.json): bounded priority outcome, credit and limits. |
| Priority reviewer `QUERY_LOG.md`, `SOURCE_AUDIT.json`, `MANIFEST.json` | [PRIORITY_QUERY_LOG.md](PRIORITY_QUERY_LOG.md), [PRIORITY_SOURCE_AUDIT.json](PRIORITY_SOURCE_AUDIT.json), [PRIORITY_REVIEW_PINS.json](PRIORITY_REVIEW_PINS.json). Former names appearing in the audit refer to these unchanged files. |
| Fresh portable-runner receipt | [PACKAGE_REPRODUCTION.json](PACKAGE_REPRODUCTION.json) contains full raw outputs for 9 baselines and 18 actual source mutations, with separately identified execution metadata. Reproduce with [run_checks.py](../run_checks.py). |
| Current whole-package review gate | [CURRENT_REVIEW_STATE.json](CURRENT_REVIEW_STATE.json) describes the current stage; fresh package-review records are added when completed. |
| First fresh whole-package review | [report](package_review_01/REVIEW.md), [verdict](package_review_01/VERDICT.json), [independent derivation](package_review_01/INDEPENDENT_DERIVATION.md), [boundary checker](package_review_01/independent_boundary_check.py), [receipt](package_review_01/INDEPENDENT_BOUNDARY_RECEIPT.json). These pins bind the earlier package before the navigation fix; they are stage history, not the corrected archive inventory. |
| Second fresh whole-package review | [report](package_review_02/REVIEW.md), [verdict](package_review_02/VERDICT.json), [input pins](package_review_02/INPUT_PINS.json). The theorem and all 27 executions passed; its P3 finding identified the POSIX execution prerequisite, subsequently documented. These are unchanged stage records. |

Raw third-party PDFs, extracted full text and page images are **not bundled**.
The absolute source paths and extraction-line links in historical reports
identify material inspected at that time. Their public primary URLs and
hashes remain in the retrieval/source records; those hash entries are source
provenance, not promises of included files. Source statements and limitations
are summarized in the supplement. The original bootstrap, permission controls
and other omitted PR delivery files are likewise historical records, not part
of this portable verification package and not executed by its runner.

The current [PACKAGE_MANIFEST.json](../PACKAGE_MANIFEST.json) is the exact
inventory for this archive, listing every included file except its own hash.
It is distinct from all stage-specific input/reviewer manifests above.
