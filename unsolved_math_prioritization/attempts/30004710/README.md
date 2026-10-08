# Completed odd volumes: corrected convention audit

Read ACCEPTANCE.md, REPORT.md, and CORRECTION_NOTICE.md. The accepted current audit repairs the MP calibration while retaining the separate OWR product-normalization and existence-scope HOLD. Proof turns remain zero. No theorem-falsity, full-solution, novelty, or author-endorsed-erratum claim is made.

This directory contains only authored audit material, public source metadata, safe exact-arithmetic checks, and verification evidence. It contains no source document bodies, dataset contents, superseded full report, private coordination records, or queue file. Historical statements in the preserved report and verification record describe their audit stage; they do not assert a fresh source retrieval, current manuscript-status search, or the state of a later draft PR.

Authenticate BOOTSTRAP.py against the SHA-256 published outside this directory before running it. The bootstrap fixes the verifier, mutation harness, and full publication manifest; that manifest authenticates every other delivered file, including acceptance and receipts. Replacing an untrusted packet's own manifest cannot replace the external trust anchor.

For validation, use UID=EUID=1000, set the packet directory to 0555 and every file to 0444, then run:

    python -I -S -B BOOTSTRAP.py .
    python -I -S -B -O BOOTSTRAP.py .
    python -I -S -B -OO BOOTSTRAP.py .

The same fixed entry authenticates the negative-control harness before executing it:

    python -I -S -B BOOTSTRAP.py --controls .
    python -I -S -B -O BOOTSTRAP.py --controls .
    python -I -S -B -OO BOOTSTRAP.py --controls .

The validator makes actual create/append attempts and requires EACCES. Controls modify only temporary copies. Fresh complete stdout/stderr must match mode-specific references exactly, with recursive exact JSON type comparison. The mathematical checker is unmodified and its output also matches CHECK_RESULTS.json. The additional guard program records mode/UID and rejects invalid inputs, output arguments, and three mathematical code mutations.

CHECK_RUNS.json records fresh reference capture. PREPARATION_CONTROLS files explicitly describe the historical pre-seal test stage. Final sealing binds those receipts as delivered files; final fixed-bootstrap validation is recorded outside this packet, with receipt hashes in the draft PR description, to avoid circular self-hashes.

Source-body replay, original-report replay, the earlier guard-harness replay, historical patch application, dataset replay, and formal proof-assistant verification are NOT_RUN. Source metadata records earlier inspection, not new source replay or journal acceptance.
