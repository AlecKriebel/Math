# Separately authored portable review prototype

`portable_profile.py` is source-free and confined to this review folder. Its only successful status is `PASS_PORTABLE_FINITE_REVIEW`. It is not the immutable submission's verifier, an acceptance decision, or a substitute receipt for its Linux whole-filesystem read-only run. It requires independent full-package adversarial review before use in a new public package.

Authenticate this review's explicit MANIFEST.json SHA-256 and the profile's listed hash against the external delivery record before running it. Colocated mutable hashes do not authenticate themselves. Use the trusted installed Python with isolated execution, no site imports and no bytecode writes:

    python3 -I -S -B portable_profile.py --packet /absolute/path/to/submitted/10400145 --work-dir /absolute/path/to/owned/writable/work

The work directory must already exist outside the submitted packet. Repeat with `-O` and `-OO`. This profile uses only Python's standard library, not SymPy or an installed new dependency. The current tests used CPython 3.14.6 on macOS 26.6.2. Its path and version are recorded in fresh receipts; the actual installed executable, standard library/hash implementation, OS and account are trust roots, not authenticated payload. A future supported-runtime statement requires its own verification, rather than assuming all Python builds behave alike.

Before any original payload code executes, the profile authenticates a fixed 33-file inventory against the independent original-payload pin file. It checks bytes, hashes, exact 0644 file modes, no symlink root/ancestor/member, regular members, sizes, and exact file/directory namespace. It checks its independently authored math checker against a fixed hash. It then runs that checker and the supported original author/algebra stages in cold normal/-O/-OO children, recording actual output hashes, results, runtimes and interpreter/host metadata. Original algebra-audit semantic negatives have their own child-mode limitations; the independent direct all-mode negatives are in this review's separate adversary receipt. The packet is rehashed after execution. This assumes no concurrent replacement of checked inputs and is not a race-resistant verifier.

Always emitted limitations are:

- `whole_filesystem_readonly: NOT_TESTED_BY_THIS_PROFILE`
- `linux_bwrap_EROFS_errno30: NOT_RUN`
- `primary_source_inspection: NOT_RUN`
- `quantum_topology_reproof: NOT_RUN`
- `literature_priority_audit: NOT_RUN`
- `full_paper_acceptance: false`

The old full profile requires real Linux namespace/mount support, a trusted working bubblewrap installation, an unprivileged account, and its exact whole-filesystem read-only launch plus errno-30 write probe. Do not put a bwrap-shaped replacement in PATH, reinterpret chmod or EACCES as EROFS, remove that test, or amend old receipt bytes to claim the original profile passed. A future new package may keep the old profile unchanged and offer this separately scoped one; that packaging is outside this route.

Fresh prototype tests pass in all three modes and reject mode changes, symlink ancestry/root/member, unexpected files/directories/FIFOs, stale bytes, a work directory inside the packet and launch without required isolation flags. Those are source-free review controls, not a new host-security claim. Stable findings REQ-COMP-01/02 and OPT-COMP-01/02/03 are in COMPUTATION_REVIEW.md and FINDINGS.json.
