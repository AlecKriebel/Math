# Function Theory 1.39: partial investigation

**Unsolved, 5/5. Neither sharp constant is determined.**

This packet proves exact reciprocal and differential parametrizations, checks the essential multiple-pole distinction, and excludes bounded-quotient, polynomial-exponential Cayley and specified rational modular families as sources of a positive-index admissible example. All exclusions are scoped; none is a universal solution.

- `PROOF.md`: complete main arguments and precise remaining gap
- `MODULAR_OBSTRUCTION.md`: independent construction-family obstruction, with explicit classical-formula dependencies
- `SOURCE_GATE.md`: original question, attribution, prior-attempt checks and unavailable-source qualifications
- `RESEARCH_LOG.md`: five substantive approach records
- `STATUS.json`: frozen author disposition; independent audit pending at freeze

From this directory, with Python 3 and SymPy installed:

    python verify.py
    python verify_modular_obstruction.py
    sha256sum -c SHA256SUMS

The two expected outputs are `VERIFICATION.json` and `MODULAR_VERIFICATION.txt`. These are finite symbolic controls, not formal verification of the analytic proofs. Both scripts reproduced their stored outputs byte-for-byte in the author checks, using SymPy 1.14.0.

The historical bounds 2 and 7 are attributed from the original question; the underlying 1986 proof was not retrieved. The exact boundary of every imported and uninspected dependency is recorded. No originality, priority, full resolution, human peer review, or formal proof-assistant certification is claimed. OpenAI tools were used extensively in research, writing and checking.

Source PDFs, full source extracts and catalogue corpora are excluded. The frozen files must remain unchanged during independent review; any correction requires a separately recorded revision and a new manifest.
