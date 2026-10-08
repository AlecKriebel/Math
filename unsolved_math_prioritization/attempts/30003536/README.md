# Intermediate Riesz maximum principle: five scoped partial approaches

Problem 30003536 / OWR-15577-004, rank 1001. **Unsolved, 5/5.**

Read PUBLICATION_ACCEPTANCE.md, corrected/REPORT.md, and independent_audit/AUDIT_REPORT.md. original/ and independent_audit/ are unchanged frozen records. The corrected report adopts only the explicit inner principal-value cutoff clarification from independent_audit/REGULARIZATION.patch. Its manifest is rehashed separately; all other author files remain unchanged.

## Reproduction and trust

Python 3 standard library suffices. No network, source documents, datasets, installations or downloaded executables are used. Run as an ordinary unprivileged user: actual read-only write denial is required. Baseline files use mode 0644 and directories 0755. Read-only copies use 0444 and 0555.

Obtain the publication manifest and BOOTSTRAP.py SHA-256 digests independently, for example from the draft PR's pinned verification metadata. Authenticate BOOTSTRAP.py and copy it outside the packet. It authenticates VERIFY_PUBLICATION.py before execution. Then run:

    python -I -B /trusted/BOOTSTRAP.py --packet /absolute/path/to/packet --expected-manifest <publication-manifest-sha256>

The default performs normal, -O and -OO replays, preserving packet bytes and modes. --mode=normal, --mode=-O or --mode=-OO selects one. --filesystem-profile readonly accepts only the read-only mode profile. --check-only checks strict identity, JSON, inventories, frozen anchors and exact patch application without executing control suites.

VERIFY_PUBLICATION.py validates strict regular-file inventories, safe paths, mode profiles, exact integer/Boolean distinctions, all nested hashes, the frozen audit acceptance scope, and exact correction application before executing delivered scripts. It runs the original and corrected native verifiers and hostile controls, plus the independent audit against the unchanged original. Genuine read-only relocated replays run from an unrelated directory and must deny both append and file creation attempts.

Authenticate and copy TEST_MUTATIONS.py and BOOTSTRAP.py outside the packet before hostile testing. TEST_MUTATIONS.py invokes the external bootstrap for malformed schema, inventory, path, mode and content cases, rehashed mutations and malicious verifier replacement in all three modes. MUTATION_RESULTS.json records actual outcomes.

A strict local maximum away from support is not a global counterexample. All accepted results are scoped partial mathematics, with no formal proof, peer review, priority or exhaustive literature-status claim.
