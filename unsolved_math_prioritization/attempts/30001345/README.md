# Plane-curve summed rough-M counterexample

Problem 30001345 (rank 974), `claimed_solved` in the unrestricted reduced multibranch summed formulation. The classical dual Hesse deformation preserves total delta 36 while the rough invariant `K.(K+D)` rises from 7 to 12. No claim is made for the later unibranched parametric Conjecture 3.8, fine M, or novelty. AI-authored, independently AI-audited, and unrefereed.

Start with [acceptance](ACCEPTANCE.md), [the full proof](frozen_v2/PROOF.md), and the complete [audit A](audit_a/AUDIT.md) and [audit B](audit_b/AUDIT_REPORT.md). All 18 frozen files are byte-identical to the reviewed originals. The [approach ledger](APPROACH_LEDGER.md) explains `1 verified/5`: one approach is evidenced; earlier-attempt count is unavailable after recovery.

## Reproduce

Python 3.12.14, SymPy 1.14.0 and mpmath 1.3.0 were used. Create an environment if desired and install `requirements.txt` from the standard package registry. Then run, from any working directory:

```sh
python /path/to/package/verify_publication.py
python -O /path/to/package/verify_publication.py
python -OO /path/to/package/verify_publication.py
python /path/to/package/mutation_tests.py
```

`verify_publication.py --integrity-only` checks the exact allowlist, all payload lengths and hashes, manifest checksum, and the three anchored frozen manifests without running computations. Full verification reproduces the author's normal and optimized outputs, audit A's normal output, and audit B's normal and optimized outputs. SymPy's exact pinned version is required for byte-identical saved output.

Audit A's frozen checker uses assertions: never run it directly with optimization. `run_audit_a.py` rejects `-O`, `-OO`, or inherited `PYTHONOPTIMIZE`; the main verifier launches it under normal isolated Python even when the parent is optimized. This is a separate publication guard, not an edit to the frozen audit.

The mutation suite uses temporary copies to test corruption of every payload, the package manifest and checksum, missing/unlisted/symlinked files, guard rejection, and a real audit A assertion corruption. Audit B includes four perturbed-input controls and two non-counterexample controls. No test changes the original package.

`PACKAGE_MANIFEST.json` lists every payload except itself and its detached checksum. The checksum detects accidental manifest corruption. These are integrity checks, not cryptographic authentication against someone who rewrites the whole package; obtain the expected Git commit or manifest SHA-256 from a trusted record. No source downloads or network are required at runtime.

## Contents and limits

The package contains authored proof/audit material and public source-verification metadata only. It excludes source documents/extracts, dataset contents and private material. The proofs, rather than arithmetic checks, support the analytic and source-interpretation conclusions. GitHub CI status is reported separately for the exact draft-PR head; no local pass implies configured CI.
