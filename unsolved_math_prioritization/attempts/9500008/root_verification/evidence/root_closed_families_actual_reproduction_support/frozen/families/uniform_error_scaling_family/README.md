# Uniform error and scaling audit

Read PROOF_AUDIT.md and VERDICT.json for the independently reconstructed probability argument and precise unresolved random-origin gap. INITIAL_SCOPE_SEAL.md and INDEPENDENT_MECHANISM_SEAL.md predate candidate/old-review exposure; read_ledger.json records coverage and quarantine.

Reproduce original programs with `/usr/bin/python3 replay_originals.py` (SymPy 1.14.0 already present). Run `/usr/bin/python3 run_adversarial_controls.py` for the exact baseline and eight prose/two original-program mutations. Run `/usr/bin/python3 run_manifest_controls.py` for five actual integrity corruptions. These commands intentionally regenerate private receipts; after any regeneration rebuild the family manifest with `/usr/bin/python3 manifest_integrity.py --build`. Read-only final validation is `/usr/bin/python3 manifest_integrity.py`.

All original scripts, full JSON receipts, executed mutant sources/prose, stdout/stderr, initial dependency failure and authored harness failures are retained. Only foreign_primary_cache/ is ignored by the local ignore rule and omitted from the recursive manifest. No source_snapshot, shared state, canonical attempt, branch, commit, remote, paper or DOI was edited by this family.
