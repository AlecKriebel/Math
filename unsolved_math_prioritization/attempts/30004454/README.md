# Coxeter automorphism quotients: five accepted partial results

Read ACCEPTANCE.md, the five numbered proofs and INDEPENDENT_MATHEMATICAL_AUDIT.md. The target remains unresolved after the 5/5 substantive-approach budget. These are scoped sufficient conditions, a reduction and two mechanism obstructions, not a solution or a novelty claim.

The five proofs, SOURCE_AUDIT.md and the safe hardened and independent checkers are unchanged. The full independent mathematical audit and correction note follow labeled portable-context preambles. Historical acceptance and retrieval metadata are clearly distinguished from fresh portable execution. The obsolete assertion-only original checker, original README/status, old harness/full packet, source documents, datasets, private coordination and QUEUE are excluded.

Authenticate BOOTSTRAP.py against a SHA-256 supplied outside this delivery before running it. It fixes the manifest and executable validation/control code. The manifest binds every other delivered file, including acceptance and pre-seal receipts. Replacing an untrusted packet's own manifest cannot replace the external trust anchor.

Use actual UID=EUID=1000. Set this directory to 0555 and all files to 0444. Run in normal, -O and -OO modes:

    python -I -S -B BOOTSTRAP.py .
    python -I -S -B BOOTSTRAP.py --controls .

Add -O or -OO before BOOTSTRAP.py. Only Python's standard library is required. Actual create/append attempts must fail with EACCES. Controls use temporary copies. Whole stdout/stderr must match mode-specific externally bound references exactly; JSON outputs also receive recursive type-exact comparison. No output normalization is performed.

CHECK_RUNS.json records fresh reference capture. PREPARATION_STAGE and PREPARATION_CONTROLS describe the pre-seal stage. Final sealing binds those receipts, then a separately fixed external bootstrap tests the whole final delivery. Final receipts are kept externally and pinned in the proposed draft PR description to avoid self-reference. VERIFICATION.md explains the precise boundaries and NOT_RUN stages.
