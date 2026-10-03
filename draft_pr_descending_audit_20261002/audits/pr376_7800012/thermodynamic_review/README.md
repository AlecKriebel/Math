# Thermodynamic review artifacts

Independent source-first audit of frozen PR376 / problem7800012 at head9a92b6a0bd7cff3a8c11bf66ff9338264ab012d1.

- REVIEW.md: sealed scoped PASS, exact deductions and remaining global gap.
- independent_derivations.md and independent_seal.md: source-first normalization, boundary/density/holonomy derivations and falsifiers.
- verdict_seal.md: own verdict bound before other-review access.
- sources_receipt.md: exact primary-source URLs/hashes; raw source files are ignored.
- checks/source_first_checks.py: exact q=4 determinant and finite normalization (requires SymPy).
- checks/thermodynamic_checks.py: self-contained standard-library exact canonical controls and rigorous bulk energy enclosure (17,809 assertions).
- checks/author_streams/: complete individual author stdout/stderr and regenerated exact Hessian Fourier certificate.
- checks/author_replay_sources.stdout.txt: 102,005 assertions,157 bindings,3 independently fetched source identities.
- post_seal_comparison.md and corresponding streams: subsequent corroboration; existing-review controls are separately labeled.
- research_log.md: checkpoints, completion estimates, evidence status and exact remaining gap.
- PUBLIC_MANIFEST.json: bounded byte/hash manifest excluding private raw sources and private copied input.

Portable independent checks:

    python checks/thermodynamic_checks.py
    python checks/source_first_checks.py

The capture script is a private-input receipt generator and requires the ignored copied frozen packet; its full outputs are public. No candidate, Git, remote, release or outside-person write/contact occurred in this audit.
