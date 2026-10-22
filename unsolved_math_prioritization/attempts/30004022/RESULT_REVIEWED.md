# Reviewed disposition: free commutators, 30004022

**Original problem remains unsolved after 5/5 substantive author turns. Independent full scoped review: PASS, no mandatory mathematical revisions.**

The source seeks extensions of particular positive-factor and scalar analytic descriptions to nonsymmetric input laws. This packet proves that two unchanged extensions fail, and gives a controlled matrix-valued alternative using credited pre-existing theory. It does not resolve the broader revised scalar/positive-factor goal.

## Retained scoped results

- Projection inputs paired with a free centered Bernoulli exclude the unchanged arcsine positive factor, through a negative shifted moment determinant
- The unchanged imaginary-axis scalar mapping class forces symmetric input laws, even without moments
- The only positive fixed factors that divide every sufficiently small-trace example are nonzero Dirac laws; a compact-factor lemma justifies the moment argument for initially arbitrary positive factors
- An explicit self-adjoint three-by-three pencil and its regularization error handle all bounded input laws through credited Belinschi–Mai–Speicher subordination
- Affiliated-operator rank control and strict spectral clipping extend this larger matrix construction to arbitrary Borel laws, with explicit tail and regularization bounds

The matrix representation supplies no finite fixed-point stopping error and no uniform real-axis density approximation. Exact finite matrices check deterministic identities only; they are never assumed free. Existing positivity obstructions and the general matrix method are credited, without novelty certification.

## Evidence and reproduction

The complete 46-file author freeze and 11-file independent review are preserved byte-for-byte. Read `RESULT.md`, `SOURCE_SCOPE.md`, and all five `TURN_n.md` files for the full author arguments. Read `independent_review/ADVERSARIAL_REVIEW.md` for the separate source, coefficient, domain and limit audit.

All five author scripts replay byte-exact, totaling 10,364 assertions. The independent checker derives moment formulas from R/S-transform series and uses different exact Hermitian matrices, passing 125 assertions. These finite controls supplement analytic proofs and credited theorems; they are not formal proof-assistant certification.

From this directory run:

    python verify_turn1.py
    python verify_turn2.py
    python verify_turn3.py
    python verify_turn4.py
    python verify_turn5.py
    python independent_review/independent_checks.py
    python verify_publication.py

Python with SymPy is required. Compare mathematical checker outputs with their recorded JSON files. The final command verifies frozen byte lengths and hashes, not mathematical truth.

Earlier checkpoint state files remain unchanged and describe their original dates. This reviewed disposition supersedes their pending-review status without rewriting historical evidence. AI-assisted authorship and independent AI review are disclosed; neither human peer review nor novelty certification is claimed.
