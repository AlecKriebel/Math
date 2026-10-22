# PR786 administrative encoding-adapter audit

Read REPORT.md and OFFLINE_REPLAY.json. This is not a new whole-preprint round. It reviews only the case-bound adapter for record23418581 and exact observed paragraph entity encoding.

Run the offline regression with no credentials or external calls:

    python3 -I -B test_adapter.py --adapter ADAPTER_PATH --tool ZENODO_TOOL_PATH --frozen FROZEN_REVIEW01 --scratch OWNED_SCRATCH
    python3 -I -B -O test_adapter.py --adapter ADAPTER_PATH --tool ZENODO_TOOL_PATH --frozen FROZEN_REVIEW01 --scratch OWNED_SCRATCH

The two code pins and metadata pin are embedded in the authenticated test. It refuses altered code before import and disables network/auth/state actions. FROZEN_REVIEW01 supplies only public-safe metadata/manifest/files; no auth config/state is read.

Authenticate this packet and its exact case inputs:

    python3 -I -B verify_custody.py --case-root CASE_ROOT --tool ZENODO_TOOL_PATH --expected-manifest-sha256 MANIFEST_PIN --expected-checker-sha256 CHECKER_PIN
    python3 -I -B test_custody.py --case-root CASE_ROOT --tool ZENODO_TOOL_PATH --expected-manifest-sha256 MANIFEST_PIN --expected-checker-sha256 CHECKER_PIN --scratch OWNED_SCRATCH

CASE_ROOT is the PR786 tmp directory or a preserved equivalent containing the relative case files in INPUTS.json. The manifest inventories every flat authored file except itself; pins come from the independently retained parent receipt. No secrets, private state, third-party full bodies or publication mutations are included.
