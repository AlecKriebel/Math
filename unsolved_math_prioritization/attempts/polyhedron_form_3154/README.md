# Frozen existing attributed solution: row 1875 / ID 3154

Disposition: already_solved / 1. Local-only frozen verification package; no publication or QUEUE edit.

The existing authored audit and independent review accept the fixed-edge uniform-unlabelled combinatorial-type target: for beta=V/(e+2), beta tends in probability to 1/2 and sqrt(e)(beta-1/2) tends in distribution to N(0,1/32). Exact mean V=(e+2)/2 and Var(V)~e/32 are included. The proof uses uniform enumeration, full-support tail bounds, lattice normalization for both parities, and moment uniform integrability; weak convergence alone does not imply the variance statement.

The exact-scope result is attributed to Lachlan Bridges's September 2026 preprint, arXiv:2609.22402v1. The audit is conditional on the published Bender–Wormald classical enumeration theorems, not an independent reproof of those papers. No novelty or journal-certification claim is made. Stronger preprint assertions outside the stated target are not accepted by this package. The earlier SOURCE_STATUS_GATE.md is retained as historical provenance: its recommendation for an acceptance audit is superseded by ACCEPTANCE.md and independent_clt_review.md.

Only nine allowlisted authored/public-metadata source files were copied. No source PDF, extracted source text, dataset record/corpus, private rendering, or coordination file is included. Source hashes, titles, sizes, public URLs and inspection history are metadata, not copied source content. The source artifacts are preserved byte-for-byte.

Run from any working directory, passing the separate external receipt:

    python verify_frozen.py /path/to/frozen_polyhedra_1875_20261021_RECEIPT.json
    python -O verify_frozen.py /path/to/frozen_polyhedra_1875_20261021_RECEIPT.json

Verification inventories the entire package before opening any payload, rejects symlinks/FIFOs/special files/unexpected subdirectories, checks exact receipt and manifest file sets and byte hashes, pins the whole check_constants.py module AST, and replays every check with assertions transformed into explicit runtime checks unaffected by -O. The original script is preserved, but directly running it with -O would suppress its assertions; use this verifier instead. Full outputs are compared with saved results. Mathematical negative controls bypass provenance deliberately and must still fail, while whole-module AST provenance independently rejects them. Proxy weights are not exact polyhedron counts; computation does not prove the CLT.

Socket operations are prohibited by an audit hook, with no socket creation used to test the prohibition. Replay results and the external freeze receipt are stored outside this directory to avoid changing the frozen payload. The external receipt is the trusted freeze record; this is an integrity/reproducibility check, not protection against an attacker able to replace both verifier and receipt. Python/SymPy installation and classical theorem proofs are outside the source-provenance boundary.
