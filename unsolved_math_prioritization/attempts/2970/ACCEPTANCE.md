# Reconciled acceptance: KP-4.94 / 2970

Date: 2026-10-08. **Partial results accepted; main questions unsolved, five approaches.** This publication review adds no mathematical approach and claims no novelty priority.

## Frozen evidence and exact correction

The original nine-file public slice is preserved at 67,843 bytes. Its MANIFEST.sha256 digest is `a8cd4866d04bba62d53083e3e3f353e90974d955f09218f59244687f6d9152e4`. The independent ten-file audit slice is preserved at 65,226 bytes, with manifest digest `a1e8bdf42fbe2fcb4042b10fce98626c70b0a8c0a12cca84fa9a3ea02adbe668`.

The complete authored report, complete independent audit, original executable, and actual OPTIONAL_ORBIT_GUARD.patch were reviewed. No mathematical correction is required. The audit's optional exact-orbit guard is adopted in a separate `corrected_v1` slice. Regenerating the unified diff from original to corrected bytes gives the supplied patch exactly: two added lines and no other change. Corrected code, unchanged saved output, and adoption metadata have a new separate manifest. The original and audit remain independently pinned in the publication wrapper.

## Mathematical reconciliation

1. The pullback-lattice saturation distinction concerns the specified branched-cover marking. No arbitrary diffeomorphism is proved to preserve it. The characteristic-fiber obstruction excludes only maps identifying the displayed fiber classes, and the nonconjugate deck involutions do not classify the unmarked manifolds.
2. The Lagrangian-sphere rational-span hypothesis would distinguish complement discriminants 4 and 1. Its geometric antecedent remains unproved. Numerical constraints or algebraic vanishing cycles do not supply it.
3. The PSL(2,F3) partial-conjugation example genuinely disproves a general cancellation shortcut. Independent permutations on P1(F3), the SL(2,F3) central extension, complete braid/conjugation closure, and enumeration of all 360 relevant generating identity quadruples confirm the disjoint orbit sizes 216 and 144. No actual Horikawa-monodromy quotient has been produced, and a single low-degree pencil obstruction would not suffice for the canonical-symplectic question.
4. The nodal-grid construction gives a smooth -3 sphere pairing 1 with the canonical class on X3, matching Y3's simple sphere data. No canonical-symplectic representative or matching -r sphere at r>3 is claimed. The formal lattice calculation proves only compatible arithmetic.
5. MNU's T-singularity hypotheses are retained. Its precise F0-component statement cannot be replaced by a non-spin distinction when both odd-r components are non-spin. The AEHK normal smoothable moduli result provides the exceptional r=3 normal bridge, not a diffeomorphism or symplectomorphism. Odd r>=5 remain disconnected in that normal locus according to the inspected preprint. The r=4 semi-smooth common-degeneration example refutes an unrestricted shortcut but lies outside the homotopy-equivalent target. Relative fillings and boundary attachments, and additional symplectic gluing data, remain missing.

Thus neither requested equivalence has a positive or negative solution for any odd-r target pair in this work.

## Fresh executable acceptance

REPLAY_RESULTS.json records nine complete baseline executions: original, corrected, and independent scripts under normal, -O, and -OO. Every valid candidate output matches the original 23,969-byte saved output exactly; independent output matches its separately saved exhaustive result. All three mathematical scripts use always-active checks rather than Python assert.

Twenty-four mutation cases run under all three modes, for 72 executions. They comprise the original audit's nine candidate and six independent cases, plus all nine candidate mutations against the corrected script. The original truncated-closure mutation emits a false PASS in every mode and is rejected only by the strict saved-output comparator. This is explicitly retained in full output. The corrected truncated-closure mutation directly raises the intended cardinality RuntimeError in every mode. The other mutations are also directly rejected.

Executed scripts have mode 0444, their execution directory has mode 0555, and UID=EUID=1000 is required. A subprocess verifies PermissionError on attempted file creation and lack of directory writability. Before/after hashes show no state creation or changes. Replays retain complete stdout and stderr; only disposable directory names in tracebacks are normalized. These deterministic records are themselves pinned, and fresh replay must reproduce them exactly.

The publication wrapper is protected by an externally authenticated bootstrap that pins its own verifier and manifest inputs before execution. Exact accepted-evidence pins prevent a substituted report, patch, executable, or receipt from becoming accepted merely by regenerating a manifest. Recursive inventories reject unlisted files/directories, links, FIFOs, and missing members. Strict JSON rejects duplicate keys, nonfinite/overflowing numbers, Boolean-as-integer substitutions, extra fields, and ambiguous paths. The adversarial harness tests these boundaries, hostile Python import environments, and read-only relocation under normal, -O, and -OO.

## Source and publication boundary

This is a source-free computational replay. Fresh retrieval, inspection, and PDF-byte comparison are NOT_RUN. Historical source metadata and statuses are preserved as historical evidence; the wrapper does not convert them into fresh verifications or claim exhaustive literature coverage.

Only authored mathematical analysis, authored verification code and output, the authored correction patch, and public bibliographic/integrity metadata are included. No source bodies, source PDFs, screenshots, external datasets, private sources, personal data, or coordination files are part of the packet. The existing full QUEUE is separately preserved except the target row's Status, Turns, and Findings cells; existing unrelated content and links remain unchanged.
