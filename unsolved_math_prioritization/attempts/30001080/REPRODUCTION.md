Current administrative status as of 2026-10-06T06:45:26.412290+00:00: published preprint 10.5281/zenodo.23180194 (https://zenodo.org/records/23180194); actual tracker 1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20 / sheet 1254632077 (Math Puzzles), row 30, range 'Math Puzzles'!A30:D30, read back and ROOT-accepted. Two sequential whole-preprint reviews are completed for immutable candidate03 content. The administrative successor requires separate ROOT ancestry/parity and source-guard acceptance; native merge is not certified here. Exact22 public payloads and all mathematics are unchanged; unrefereed, extensive AI assistance, no human peer review or formal machine proof.

The entire retained candidate03 text below is historical as of its frozen preparation03 checkpoint, including earlier pending, DOI-none, review-request and workflow statements. Frozen original/rejection/checkpoint records remain historical evidence.

---

# Reproduction and literal source binding

Use Python with the existing SymPy dependency for the original/discrete controls. This package performs no install. `-E -B` ignores Python environment overrides and avoids bytecode writes. From this attempt directory, run:

    python -E -B checks/turn1_checks.py
    python -E -B checks/turn2_checks.py
    python -E -B independent_review/independent_check.py

Their complete stdout must match checks/turn1_output.json, checks/turn2_output.json and independent_review/INDEPENDENT_CHECKS.json literally, including newline. Counts remain 18,814 / 75,172 / 186,869. The sources and expected outputs are unchanged original bytes. AUTHOR_REPLAY.json is the unchanged historical record; the preparation's ORIGINAL_CONTROL_REPLAY.json separately records the current exact native replay.

The scoped turn-3 controls are:

    python -E -B checks/turn3_poisson_controls.py
    python -E -B checks/turn3_poisson_independent_controls.py
    python -E -B checks/turn3_discrete_controls.py
    python -E -B checks/turn3_class_separation_controls.py

The first output matches turn3_poisson_recorded_output.json (293,748 assertions), the third matches turn3_discrete_recorded_output.json (13,159 controls), and the fourth matches turn3_class_separation_recorded_output.json. The independent probability script prints its 21,136 exact-fixture result. C's copied control has exactly one packaging adaptation: its frozen-candidate hash check reads turn3/POISSON_OBSERVATION_PROOF.md, removes the explicit assembly preface at the first newline-delimited separator, then hashes the unchanged 9,919-byte family body against bd5eb9048439f6e6cac903e0b44b0277180e360dc94439f8eab34fac19efeeef. Control mathematics and all other copied program bytes are unchanged. No external family directory is required for these seven programs.

Every manifest hashes complete literal stored bytes using SHA256. FROZEN_INPUT_MANIFEST.json excludes itself, its compatibility wrapper and independent_review/ to avoid self/cross cycles. FROZEN_MANIFEST.json binds the same author bodies plus FROZEN_INPUT_MANIFEST.json. The separate REVIEW_MANIFEST.json binds current editorial/scoped review material and the unchanged historical finite controls, while marking the new global review pending. Source PDF hashes are for distinct acquired source bytes and editions, not a normalized DOI or text hash. No primary-source PDFs are distributed in this tree; the authored preprint PDF is included under preprint/.

For the full local preparation, INPUT_MANIFEST.json binds all 21 original attempt files plus the entire original queue and credited scope/proof/priority inputs. PROPOSED_TREE_MANIFEST.json binds every proposed repository body and PR/diff sidecar. FILE_DELTA.json and WHOLE_CANDIDATE.diff specify every exact original/proposed body; only queue line317 changes. DETERMINISTIC_REPRODUCTION.json records a complete literal rebuild. FULL_CATALOG.json, outside this publication tree, catalogs every owned preparation body except itself; its hash is verified externally, and VERIFY_CLOSED.py checks all catalogued bodies and 0444/0555 closure. These byte checks and finite controls supplement the credited analytic proofs and never establish global mathematical/source/priority/publication acceptance by themselves.

Integration02: the exact ROOT-selected A-only preprint is under preprint/. Its standard-library verifier is preprint/verification/verify_package.py and its exact original assertion totals sum to280,855. Main-paper metadata is copied literally: preprint/record_metadata.json equals the metadata object in preprint/zenodo-deposit.json. The PDF and ZIP must match PREPRINT_BINDING.json. Root priority preparation is now bounded-accepted with gaps; fresh whole-preprint/publication readiness stays pending. Selected verification documentation's historical candidate/family language is preserved as exact ROOT payload, while the current integrated author-tree status is recorded in CLAIM_STATUS.json and PRIORITY_ACCEPTANCE.json. Preparation01 is untouched.
