# Reproducing the audit controls

The frozen release and this audit are separate. Do not run either program with an output destination inside the frozen release.

From this safe audit directory, run:

    python3 ../../release/verify.py --sp4 --output /tmp/classical_30001860_author_replay.json
    cmp ../../release/verification_results.json /tmp/classical_30001860_author_replay.json
    python3 independent_controls.py --frozen ../../release --output /tmp/classical_30001860_independent.json

Only the Python standard library is required. Matrix checks use prime fields 3, 5, and 7. Prime powers in the torus checks require no implementation of extension fields because those checks depend on the exact cyclic-factor orders.

The independent mathematical outputs are deterministic; its elapsed_seconds field and timing line are runtime measurements and may differ on replay. The main proof must still be audited mathematically: none of these commands proves an infinite asymptotic theorem.

AUDIT_MANIFEST.json binds every safe audit file other than itself. BINDING.json separately binds the unchanged eight-file release and its manifest. The safe package contains no primary PDFs, extracted source text, page images, raw catalog/prior-AI records, or private coordination.
