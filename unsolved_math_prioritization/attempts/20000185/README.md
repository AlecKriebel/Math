# Reviewed partial result for AIM Algebraic Vision 1.25

**20000185: unsolved, five substantive approaches completed.**

The frozen author packet proves scoped divisor-overlap formulas for fixed-camera curve reconstruction. For integral reduced images over an algebraically closed characteristic-zero field and nonconstant epipolar pencil maps, a component's world degree is N+deg max(A,B), and the baseline's cycle multiplicity is alpha beta+sum deg min(A,B). The operations on divisors are coefficientwise. This does not settle the broad real/physical or general scheme-theoretic target, and no novelty claim is made.

- `submission/` contains exactly the eleven unchanged author artifacts.
- `FREEZE_MANIFEST.json` is their unchanged external binding.
- `audit/` contains the full independent AI-assisted audit and its unchanged nine artifacts.
- `CLARIFICATIONS.md` adopts three nonblocking editorial clarifications separately.
- `REPLAY_VALIDATION.json` records final-layout replay and negative controls.
- `PUBLICATION_MANIFEST.json` and `verify_publication.py` bind this complete layout strictly.

The independent review found no blocking error in the scoped theorems. It is not human peer review or formal proof certification. The author controls pass 8,625 assertions over 1,225 rational image pairs; independent controls pass 7,305 assertions, including resultant lengths, ramified covers, multiple epipole branches and component-dependent overlap. The clean gcd mechanism and other prior results are expressly credited.

Run from this directory, with Python 3 and SymPy 1.14:

    python verify_publication.py
    python submission/verify_manifest.py
    python submission/verify.py
    python audit/independent_checks.py submission

The scripts are local and deterministic. No source PDFs, source-page copies, corpus contents or private coordination files are included.
