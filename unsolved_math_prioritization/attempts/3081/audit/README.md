# Independent audit of problem 3081 / OPG-2435

Verdict: accept the unchanged pinned author packet as an unresolved two-approach obstruction audit. No new asymptotic bound and no asymptotic counterexample are established. No correction derivative is needed.

Read AUDIT_REPORT.md for the complete independent mathematical and source review. ACCEPTANCE.json binds the exact author ZIP and external manifest. INDEPENDENT_NORMAL.json and INDEPENDENT_OPTIMIZED.json record independent rational geometry, complete corpus checks, and source-byte checks. AUTHOR_REPLAY.json records actual isolated, relocated normal/optimized replay and adversarial results. SOURCE_AUDIT.json contains public-source retrieval/inspection metadata only.

Reproduce with Python 3 standard library:

    python3 -I -B independent_check.py
    python3 -I -B -O independent_check.py
    python3 -I -B replay_author.py

Private full-input checks are optional; no private files are bundled:

    python3 -I -B independent_check.py --corpus-dir /authorized/corpora --source-dir /authorized/sources
    python3 -I -B replay_author.py --corpus-dir /authorized/corpora --source-dir /authorized/sources

The corpus directory must contain catalog.json, problems.json, and research_results.json with exactly the pinned bytes. The source directory must contain the eight metadata-named files in the nested author's SOURCE_VERIFICATION.json. replay_author.py copies supplied inputs to fresh temporary paths and tests them there. Do not place extra files into the separately extracted original author's directory because its exact-member check will reject them.

For this audit package, validate MANIFEST.json against the external audit manifest and trusted external archive hash before running code; internal hashes are not an authenticity guarantee. All validation uses explicit exceptions and remains active with -O. The audit's immutable original ZIP pin remains mandatory even when a purported replacement archive has newly recomputed hashes.
