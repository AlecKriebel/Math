# Publication context for the historical audit-stage record

The following record describes the completed independent audit before this public delivery was prepared. Its preserved checker, expected output, and guarded receipt are included. The former guard-harness executable and complete earlier packet are not delivered. Current fresh replay and controls use BOOTSTRAP.py, verify_publication.py, and guard_conventions.py. Earlier original-payload preservation and source-body stages are historical evidence; this portable delivery reports their replay as NOT_RUN. The current REPORT.md and CORRECTION_NOTICE.md are preserved byte-for-byte.

---

# Exact verification record for the corrected convention audit

The current checker completed under Python 3.12.14 as UID 1000 in normal, -O and -OO modes. Every stdout result exactly matches CHECK_RESULTS.json.

## Mathematical checks

- 19 OWR coefficient comparisons.
- 824 independent ordered-composition/multiplicity comparisons.
- 12,512 finite genus/dimension/triangularity checks.
- 824 comparisons with the local prong/bottom/automorphism coefficient.
- 693 finite instances of the symbolic all-sunflower conversion identity.
- Sauvaget's exact minimal-intersection recursion through genus six; literal independent checks for genera one, two and three.
- Repaired Q(3,−1³) correction π⁴/9 and completed volume 2π⁴/3.
- Historical π⁴/18 retained only as the explicitly rejected abelian-class substitution.
- 560 direct cycle-joining versus subset-formula comparisons for two singularities, including interchange of the marked orders.
- Reconstruction of all three Q(5,3) special-star rows, their subtotal, the total table sum, and the π⁶ conversion.
- Exhaustion of six numerically compatible two-marking cases in the seven OWR displayed families, each with a known empty displayed correction core.

The one-singularity coefficient range is odd orders −1 through 41. The original finite genus/dimension grid uses signatures of length four or six with entries −1, 1, 3, 5. The direct star-count grid uses total tail genus one through six, at most four positive ordered tails, and compatible odd marked orders at least −1. These are explicitly bounded formal-signature checks, not claims of nonemptiness or proofs for unbounded families.

## Guard and integrity checks

In each execution mode:

- Five invalid order cases and three invalid signature cases were rejected.
- Command-line output arguments were rejected.
- An altered OWR coefficient was detected.
- Replacing the genus-dependent tail conversion by a constant factor two was detected.
- Adding one to every star-bottom intersection was detected by the independent cycle count.

The checker contains no assert statements, file input/output operations, subprocess calls, or network operations. The guard harness checks for assert nodes and runs the same checker copied into a read-only directory.

Current checker SHA-256:

    340bceefd26aac988554cdb530bb49a47db2ac5a7f56eabd860336eef5e7be77

The mode-0555 directory denied creation of a file, and its mode-0444 verifier denied overwriting, both with PermissionError/errno 13 under UID 1000. The copied checker remained byte-identical to its source and its pre-probe hash. These denial probes test the execution directory and payload; the checker itself has no export/write operation.

The original report remains 19,816 bytes with SHA-256:

    63cab3e68e8289630dd66978ce9217737a4701ea703c2e5f093b6ae540616ff0

All nine original pinned payload files were checked against their existing byte counts and SHA-256 values and still match. Their conclusions are historical; CORRECTION_NOTICE.md and the current REPORT.md explicitly supersede the MP calibration objection.

## Meaning of PASS

The arithmetic status is PASS_CORRECTED_CONVENTION_AUDIT_WITH_OWR_SCOPE_HOLD. It does not certify all imported geometric theorems, all infinite graph families, manuscript acceptance, or complete resolution of the original OWR application. The main Q(5,3) intersection and the nonzero sunflower row are explicitly retained source inputs; only the three star rows are independently reconstructed here.

The guard harness creates and removes its own temporary execution copy. It can be rerun as a non-root user. No denied source-access path was retried and no remote state was changed.
