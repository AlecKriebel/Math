# Independent audit: rank 657 / ID 30000510

Decision: pass for components and ordinary singular (co)homology with constant abelian coefficients. Credit belongs to the inspected unrefereed preprint by Alper Ferudun, DOI 10.5281/zenodo.23071801. One substantive approach was used; no novelty or whole-preprint certification is claimed.

AUDIT.md contains the detailed adversarial review, source interpretation, complete relevant proof check, boundary cases, limitations, and result. AUDIT_RESULT.json supplies the machine-readable decision. REPLAY_RESULTS.json and INDEPENDENT_RESULTS.json record finite controls. SOURCE_RECHECK.json binds fresh primary-source retrievals by public metadata and hashes. No source content is bundled.

The sibling AUDIT_MANIFEST.json binds all files in this directory and the exact author manifest/archive. After extracting audit-packet.zip into an empty directory, run:

    python3 -B audit/verify_audit.py

To also replay and verify the original frozen author packet, supply its directory containing AUTHOR_FREEZE.json, author-packet.zip, and packet/:

    python3 -B audit/verify_audit.py --author-root /path/to/author/root

Both commands require Python 3 only. They make no network requests and do not write files. The optional author replay runs the exact hash-verified local author control script. Neither command is a formal verification of the universal topology proof.

AUDIT_BINDING.json, distributed separately from the archive, binds the completed archive and both manifests. The author packet itself remains unchanged and is not duplicated in the audit archive.
