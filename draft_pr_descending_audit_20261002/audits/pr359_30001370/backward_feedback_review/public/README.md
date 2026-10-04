# Backward-feedback audit package

Read REPORT.md for the scoped mathematical verdict, independent stronger inverse certificate, all-L1 transport checks and exact limits. SOURCE_FIRST.md and SOURCE_FIRST_SEAL.json record the reconstruction sealed before candidate access. PACKET_CUSTODY.json, SOURCE_CUSTODY.json, REPLAY_RECEIPTS.json and PORTABLE_CONTROLS.json record full byte/mode/schema bindings and native reproduction status.

Public mathematical replay requires only Python's standard library:

    python3 verify_controls.py

Every exact output field must match INDEPENDENT_CHECKS.json. Only the two explicitly labeled floating numerical summaries permit an absolute1e-12 tolerance, with their experiment bounds separately enforced. Complete cross-runtime streams, including the failed whole-byte numerical comparison, remain private. Author-program replay remains byte-exact under the recorded existing Python3.11/SymPy1.14 environment.

For the complete local sealed audit folder, the read-only checker is:

    python3 public/verify_audit.py

It verifies the finite enumeration of every public/private file and directory, bytes, SHA256 and modes; rejects extra root artifacts; and checks raw native receipts and the original source-first seal. Before closure, --draft checks receipt consistency without claiming a final seal. The final root MANIFEST.json binds both namespaces, and root SEAL.json binds that manifest. Neither needs nor performs network access or writes.

Raw primary PDFs, extraction/render data, native Git/API/program streams and old expected output bytes are private. No publication, PR modification, Git mutation, installation, or external communication was performed. Historical novelty is unverified. Counts alone are custody evidence, not mathematical proof.
