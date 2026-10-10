# KP-3.77 independent mathematical and artifact audit

Accepted outcome: corrected restricted partial, unsolved, four of five approaches. Read INDEPENDENT_AUDIT.md and ACCEPTANCE.json. No full solution, general nonexistence theorem or novelty claim is made.

AUTHOR_SAFE_FREEZE.zip and its external manifest preserve the six original authored files exactly. CORRECTED_SAFE.zip and its external manifest contain the minimal Proposition 4.1 clarification; CORRECTION.patch reproduces it. All other authored member bytes are unchanged. Historical author audit-pending statements remain historical; ACCEPTANCE.json is the subsequent exact acceptance.

verify_source_pins.py takes eight explicit input paths: --catalog, --problems, --reports, --k3, --fkr, --bfs, --long-reid and --hatcher. These large source inputs are intentionally absent from the package. It rehashes complete inputs and emits metadata only.

verify_package.py takes --archive, --external-manifest and --expected-external-manifest-sha256. The expected digest must be supplied independently of the manifest being tested. Add all eight source arguments for a full source replay. Without them it explicitly reports sources not rehashed, rather than a full pass. test_integrity.py takes --root for an extracted audit directory and checks corruption controls using its exact inner artifacts and an explicitly synthetic envelope fixture. Final real-archive replay is recorded separately.

The outer external manifest identifies exact accepted audit-member bytes and the ZIP. The included verification scripts are integrity tools, not a theorem prover or mathematical proof certificate. Source PDFs/extracts, dataset contents and private coordination material are not included. No publication was performed.
