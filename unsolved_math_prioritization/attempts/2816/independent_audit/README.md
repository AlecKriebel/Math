# Independent acceptance package: 2816 / KP-3.18

Start with ACCEPTANCE.md and ACCEPTANCE.json. The exact author archive is accepted for scoped partial results only; the problem remains unsolved with 3/5 approaches used. No correction patch is required.

MATHEMATICAL_AUDIT.md provides the independent argument audit. SOURCE_REVIEW.md and the JSON ledgers distinguish inspected source statements, local source-byte pins, bounded live checks, and inaccessible or unverified material. The complete original author archive is a separate immutable input, not embedded here.

To reproduce the finite replay, using Python 3.12 and SymPy 1.14.0 as tested:

    python replay_independent.py --archive /path/MINIMAL_FOLIATIONS_2816_AUTHOR_SAFE_FREEZE.zip --manifest /path/MINIMAL_FOLIATIONS_2816_AUTHOR_EXTERNAL_MANIFEST.json --receipt /path/MINIMAL_FOLIATIONS_2816_AUTHOR_VALIDATION_RECEIPT.json

The runner pins all three inputs before executing either author program, extracts the allowlisted ten members into a fresh temporary directory, uses a different working directory, and tests ordinary Python, -O, and -OO. It leaves the supplied files unchanged. Its expected output is REPLAY_RESULTS.json. It needs no source PDFs or dataset files. Those were checked separately in the source/corpus audit and are intentionally excluded.

Run python independent_calculations.py for the 512 independent finite rational controls. Run python verify_audit.py to compare this directory with its internal manifest. Authenticate the audit ZIP and external manifest using independently delivered digests before trusting local checks: an internal manifest alone does not establish authenticity.

All computational results have a finite scope. No script certifies geometric existence or a full solution. Frozen author metadata may still say independent review pending; the separate exact acceptance supersedes that historical label without altering it.
