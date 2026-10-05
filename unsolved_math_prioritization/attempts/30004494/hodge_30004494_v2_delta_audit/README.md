# Accepted v2 correction for 30004494

Read DELTA_ACCEPTANCE.md for the bound acceptance and unchanged limitations. DELTA_ACCEPTANCE.json provides its machine-readable status. This sidecar supplements, and does not overwrite, the original independent audit.

Reproduce with Python 3.10+ and the system patch utility:

    python3 verify_delta.py --root /path/to/parent-folder

The parent folder must contain the pinned v1 and v2 trees, archives, exact patch, and original independent audit. Inputs are read-only. Patch reconstruction occurs in a temporary directory. Compare stdout to DELTA_VERIFICATION.json. Arithmetic and file integrity do not prove the original mathematical conjecture.
