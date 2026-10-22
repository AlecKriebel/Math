# Integral skyline bases: audited corrected partial results

Problem 30001525 / OWR-4413-009, rank 977. **Unsolved, 5/5 approaches used.**

Accepted scope: a cyclic skyline basis for S_n, n <= 7, in all degrees; and a single-skyline third-Bockstein family on S8 with exact order eight in degrees 8a+8. The full S8 basis and the arbitrary-n conjecture remain unresolved. No novelty claim is made. An artificial preferred-basis obstruction is not a counterexample for symmetric groups.

Read the [corrected proof](independent_audit/patched/PROOF.md), [independent acceptance report](independent_audit/INDEPENDENT_AUDIT.md), [full mathematical supplement](independent_audit/MATHEMATICAL_SUPPLEMENT.md), and [actual correction patch](independent_audit/PATCHES.diff). Original files are preserved under `packet/`; the full audit and separately corrected packet are preserved under `independent_audit/`.

## Corrections and limitations

The original verifier has 20 assert guards, which Python removes in optimized execution. Four genuine mathematical mutants falsely pass under both -O and -OO. Such original optimized runs are reproducibility diagnostics, not successful mathematical validation. The corrected verifier explicitly checks every unchanged condition and rejects all four mutants in all three modes. The proof clarification supplies compatible integral lifts and distinguishes four-letter support from combinatorial column width two.

The audit independently computes S4 through degree 100, checks every C8 Mackey orbit and all 70 cosets, and tests cyclic carry cocycles and the preferred-basis obstruction. These are finite exact checks, not a proof assistant or a substitute for the all-degree written arguments. The imported published Hopf-ring and cochain theorems remain dependencies.

## Portable source-free replay

Python 3.10+ standard library only. Obtain PUBLIC_MANIFEST.json's SHA-256 from the draft PR description or a separately trusted receipt, then run:

    python3 -I -B verify_publication.py --manifest-sha256 EXTERNAL_SHA256
    python3 -I -B -O verify_publication.py --manifest-sha256 EXTERNAL_SHA256
    python3 -I -B -OO verify_publication.py --manifest-sha256 EXTERNAL_SHA256
    python3 -I -B mutation_tests.py --manifest-sha256 EXTERNAL_SHA256

Each wrapper invocation runs the audit, actual patch generator and corrected verifier as genuine normal/-O/-OO child processes in relocated temporary copies with different working directories. It preserves the frozen reports, reproduces the actual patch, verifies all 30 audit child tests, and requires twelve corrected mathematical-mutant rejections and eight historical original optimized false passes. Separate controls execute 51 corrupted-copy child processes, including altered bytes, missing/extra members, symlinks and self-consistently rewritten unpinned manifests.

The external manifest pin is essential: deriving it anew from an untrusted package cannot authenticate that package. Exact inventory rejects unexpected files/directories and links. The wrapper changes no publication file and rechecks integrity after execution. Only temporary copies receive regenerated output.

No PDFs, source extracts or datasets are included. Public titles, URLs, hashes, sizes and inspection history remain in the frozen source metadata. Original source-byte verification is preserved as historical evidence. A source-free replay explicitly marks all six PDFs absent and performs 6,480 checks, rather than claiming the six additional source-byte checks in the original 6,486-check audit.

## Checkpoint

2026-10-07: Five mathematical approaches and independent audit complete; corrected partial package accepted. Estimated completion toward the unrestricted discovery goal: 25% (subjective, not a probability or a measured fraction of a proof). The exact remaining gap is a compatible cyclic skyline basis for the full S8 cohomology and then arbitrary n. No extra proof-search turn is added by packaging or verifier hardening.
