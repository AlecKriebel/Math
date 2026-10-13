# Literal full tensegrity partitions: proof and audit

Read ACCEPTANCE.md, REPORT.md, and AUDIT.md. STATUS.json contains the target disposition; the original source-interpretation hold remains. The contextual attribution patch is historical and superseded.

This directory contains only authored proof/audit material, public source metadata, exact-rational verification code, and full execution evidence. It contains no source document bodies, dataset contents, or queue file.

Authenticate BOOTSTRAP.py against the SHA-256 published outside this directory (for example the draft PR description) before running it. The bootstrap pins the verifier and the complete publication manifest, which binds all other delivered files, including acceptance and preparation receipts. An attacker replacing the packet's own manifest cannot replace that external trust anchor.

For a portable validation, place the packet in a directory owned by UID 1000, set every file to mode 0444 and the directory to 0555, and execute as UID 1000:

    python -I -S -B BOOTSTRAP.py .
    python -I -S -B -O BOOTSTRAP.py .
    python -I -S -B -OO BOOTSTRAP.py .

For negative controls, use the same externally authenticated BOOTSTRAP.py entry point with --controls before the packet directory. The bootstrap verifies the mutation harness bytes before executing them: The validator makes actual create/append attempts and requires EACCES. It does not rely only on permission bits. Test mutations occur in temporary copies, never in the delivered packet.

    python -I -S -B BOOTSTRAP.py --controls .
    python -I -S -B -O BOOTSTRAP.py --controls .
    python -I -S -B -OO BOOTSTRAP.py --controls .

CHECK_RUNS.json and reference files record fresh exact-rational check executions. PREPARATION_CONTROLS files are explicitly pre-seal test receipts whose recorded pins describe their historical stage. Final sealing binds them as ordinary delivered files; the final fixed-bootstrap tests are recorded outside the packet to avoid a circular self-hash. The final PR records their hashes.

Original-report replay, historical patch application, source-body replay, dataset replay, and formal proof-assistant verification are NOT_RUN by the portable validator.
