# Independent audit of connected sum ropelength, problem 2733

Exact author freeze accepted as a partial formulation audit; intended (a) and (b) remain unresolved. Read ACCEPTANCE.md and ACCEPTANCE.json first. MATHEMATICAL_AUDIT.md gives the independent proof review. SOURCE_REVIEW.md and SOURCE_INSPECTIONS.json disclose source scope and access limits. The four verification-result JSON files record the exact artifact, full corpus, source-PDF and executable checks. AUDITOR_SELF_TESTS.json records optimized replays of the independent runner.

No source documents, extracts, datasets or private coordination material are included. The original author artifact is not embedded or changed.

## Integrity-only replay

Run python3 verify_audit.py in the extracted audit directory. The same command supports -O and -OO. This checks this audit's member manifest and acceptance invariants; it is not a geometry prover or an authenticity signature. Trust the separately supplied external audit ZIP pin.

## Independent author replay

Run replay_independent.py with --archive pointing to the frozen author ZIP, --external-manifest pointing to its frozen external manifest, and --output pointing to a separate empty output directory. This reruns artifact verification, six relocated baselines and 42 negative mutation runs. Test directories are temporary. Never set --output to a frozen author or audit package.

For the full input checks, additionally provide --catalog, --problems and --research-results for the three complete pinned datasets, and --source-dir for the five original PDFs named k3.pdf, cks02.pdf, cks02_arxiv.pdf, clr12.pdf and milnor50.pdf. These inputs are deliberately excluded. Python standard library and pdfinfo are required for the full check. Without those optional inputs, corpus and PDF validation are skipped, not inferred from a clean author replay. The accepted stored run supplied all inputs.

The independent runner and the author verifier both use explicit checks that remain active under optimization. Mutation tests check the behaviors listed in REPLAY_RESULTS.json; they are not a proof of resistance to every possible alteration.
