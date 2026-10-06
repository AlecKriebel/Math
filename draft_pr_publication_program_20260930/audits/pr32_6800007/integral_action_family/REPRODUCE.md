# Reproduce the original-stage integral family

Use the existing Python 3.9.6 interpreter and existing SymPy1.14.0; no installation, network, Git or external contact is required.

```sh
/usr/bin/python3 /Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr32_6800007/integral_action_family/reproduce.py
```

The reproducer verifies all fifteen original snapshot hashes, the frozen exact diff, the early independent seal and every closed first-party manifest member. It executes the new stdlib controls in an ignored copy and compares stdout byte-for-byte with integral_results.json; runs the deliberately wrong ordinary-c2 mutant and requires exit1 with EXPECTED_FAILURE; then replays both unchanged original programs in separate ignored copies and compares their recorded outputs. All newly generated output goes beneath this family's ignored tmp/reproduce/. Closed evidence is read only.

Expected summary: 3,256 new assertions; eleven explicitly rejected mutants; both original stdout files byte-identical; corrected controls exit0/empty stderr; intentional ordinary-c2 failure exit1. Finite counts and algebra tests supplement the universal REPORT proof and do not prove the h-principle, stability or novelty.

Three earlier accidental harness failures are preserved in failures/. They are not run by this normal reproduction command and are not PASS: cochain_shape_v1 used mismatched absolute/relative matrix shapes; reid_zero_relator_v2 wrongly required every relator have nonzero abelianization; protected_schema_v1 used the wrong key for the immutable PR30 manifest. Their frozen code/stdout/stderr/receipts identify the exact corrections. To examine any, read its code first and run only an isolated copy under ignored tmp/.

The primary reference copies and complete relevant PDF pixels are also ignored research files in tmp/primary/. primary_sources_receipt.json gives URLs and hashes for independent re-retrieval. These copyrighted foreign texts/PDFs are not redistributed as first-party evidence. The manifest deliberately excludes itself, tmp/** and **/__pycache__/** and explicitly lists every other first-party member with size and SHA256.
