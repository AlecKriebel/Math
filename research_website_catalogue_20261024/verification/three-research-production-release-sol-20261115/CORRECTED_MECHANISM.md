# Corrected installation mechanism

Use install_three_corrected.py with INSTALL_PLAN_CORRECTED.json. The original17,965-byte helper, original plan, INITIAL and actual first preflight remain intact as history; no previous approval or execution claim is rewritten. CORRECTED_CODE.diff records the exact change.

All transaction directory links and the journal entry are fsynced through their parents before website moves. All19 candidate buffers are fully written, checked and fsynced; the staged directory is then fsynced before any website directory creation or file move. The existing order remains16 new leaves followed by3 replacements.

A single fixed ACTIVE_INSTALL.lock in this owned folder is created exclusively at0600 and contains authorization SHA and PID. Its contents, held inode and parent are checked and made durable. Different serialized authorization bodies cannot bypass it. The lock remains after failure or verified success until root explicitly releases it; the helper never unlinks it. On failure, partial/uncertain state and backups remain without automatic recovery.

The default remains read-only preflight and --verify-installed remains a separate read-only filesystem-postinstall phase. The corrected default passed against631/96/97 and the original58571-entry5f9c0600 index, with absent authorization, absent active lock and zero writes. The install path, exclusive moves, crash behavior and postinstall mode have not been executed here. Bounded race checks are not isolation from external writers.

AUTHORIZATION_REQUIREMENTS_CORRECTED.json specifies the exact new code/plan bindings required in the separate root-owned authorization. No installation, Git, deployment, browser, network or spreadsheet authority is created by these preparation files.
