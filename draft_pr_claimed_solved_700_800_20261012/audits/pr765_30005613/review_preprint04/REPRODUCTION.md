# Read-only root replication

From any directory, use the absolute review path R:

    R=/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr765_30005613/review_preprint04
    python3 -B "$R/verify_closure.py"
    python3 -O -B "$R/verify_closure.py"
    python3 -O -B "$R/verify_closure.py" --current-inputs
    python3 -B "$R/exact_controls.py"
    python3 -O -B "$R/exact_controls.py"

The closure checker never writes. Default verifies authored historical closure only; optional current-input checking compares adjacent live six. exact_controls emits JSON only and uses explicit checks active under optimization. Compare its stdout with EXACT_CONTROLS.json. No command creates bytecode with -B.

Full physical-suite reproduction writes receipts and scratch and must run in a disposable copy at a corresponding review path with the original preprint/original/closed family siblings available. Extract source-and-verification.zip to that copy's tmp/source, run reproduce.py, copy paper.tex into owned tmp, compile/render as recorded, then run supplementary_checks.py. The latter expects the original/fresh six rasters and primary rendering observations recorded in COMPILE_RENDER_RECEIPT. Primary source retrieval and visual judgments require the described independent read/view procedure; no claim is made that running a receipt writer recreates human-style inspection. Do not run writing drivers in this closed authored record.

Bundle replay/build commands, Python versions, raw-stream checks, all failed launches/writes and exact fixture results are in their respective receipts. Historical optional full-corpus and whole-queue modes were not run. No external contact, publication or Git mutation is part of replication.
