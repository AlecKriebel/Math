# Independent graph NLS audit release

Read `INDEPENDENT_AUDIT_AND_ACCEPTANCE.md` for the mathematical decision and scope.
The quadratic graph NLS-approximation problem remains unsolved.

The original author freeze and its historical receipt are preserved. The corrected
release changes only the finite checker guard and the external replay bootstrap.
The unified patch records those changes. The three mathematical, source-metadata,
and status members are byte-for-byte unchanged.

All six original/corrected release inputs are externally pinned by
`replay_adversarial_controls.py`. Run that script with Python `-I -S` from this
folder to reproduce the 46 finite integrity controls. These controls include the
confirmed failure of the old bootstrap under `-O`; that expected failure is not a
successful integrity guarantee for the old bootstrap. The corrected release
passes all expected checks. Layer-specific diagnostic mutations explicitly repin
test copies of higher layers and are never release artifacts.

The outer independent-audit archive must itself be checked against its separately
pinned external manifest before executing any archived code. Its external
bootstrap performs this check and then runs the controls in a fresh directory.

The payload contains authored work and public verification metadata only. It
contains no third-party source documents, datasets, or private coordination.
