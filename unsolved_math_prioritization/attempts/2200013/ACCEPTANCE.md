# Release acceptance

Date: 2026-10-08. Problem 2200013 / AMR-021-0013, rank 1031.

**Accepted as a literature-derived negative resolution with an explicit reconstructed witness, supported by two independent audits.** The corrected release verifier is accepted following a narrow parser-only correction. This acceptance is an authored mathematical audit decision, not conventional journal peer review or formal proof-assistant certification. The work used extensive AI assistance.

The precise witness has strictly positive rational coefficients, actual degree 200000000000000000100, at least four distinct negative roots, and exactly three distinct binomial-weighted tropical corners. The finite exact computations support the symbolic proof. They do not enumerate its enormous support or determine every root.

The first complete audit independently checked the mathematical derivation and primary-source conventions, without running packet tests. The second independently reconstructed the arithmetic and ran 687 controls, 229 each in normal, -O and -OO modes, including 78 overflow-literal rejections. It reproduced five malformed-input acceptances by the original standalone verifier and their rejection by the corrected verifier. Its actual UID/EUID were 1000. The actual patch changes schema validation only. No arithmetic or proof correction was needed.

The original and corrected proof and certificate are byte-identical. The nine-file original slice is included solely to reproduce the historical comparison. The author control receipt is historical evidence; it is not substituted for the independent controls. The later audit acceptance supersedes the original frozen audit-pending metadata without altering historical bytes.

Attribution: Forsgård–Novikov–Shapiro's [Theorem 11](https://arxiv.org/abs/1510.03257v1) supplies the prior small-curvature obstruction. The explicit reconstruction specializes it to binomial multiplication, eliminates reliance on an unspecified constant for this witness, and supplies a full-support perturbation. [Shapiro's original formulation](https://arxiv.org/abs/1503.05295v1) is the audited target. The target's later repetition as Conjecture 1 in [the 2024 paper](https://arxiv.org/abs/2403.12200v1) remains a disclosed, historically unexplained discrepancy.

No claim is made about conventional slope-jump multiplicities, smallest possible degree, the exact total real-root count, simplicity of all roots, novelty, priority, or comprehensive literature coverage. There is no identified mathematical gap in the accepted claim. Publication remains a draft PR, with no merge, release, DOI creation, or external outreach.

Queue accounting: already_solved, 0/5; finding: literature-derived negative obstruction; explicit reconstructed witness; two independent audits. This records the prior obstruction rather than claiming a new discovery. Only the target row's Status and Findings differ; Turns remains 0/5 and all unrelated bytes, Chat and DOI are preserved.
