# Reading and replay guide

Start with RESULT.md, SOURCE_SCOPE.md, and CORRECTION_CONE.md. Read TURN_1.md through TURN_5.md in order. The original research question remains unresolved after five substantive author turns; retrieval, correction, testing, review and packaging are not additional author turns.

Run, from this directory:

    python verify_turn1.py
    python verify_turn2.py
    python verify_turn3.py
    python verify_turn4.py
    python verify_turn5.py

Each program uses the Python standard library and emits the exact corresponding TURN_n_CHECKS.json receipt. The assertion counts are 5,797; 44,500; 3,999; 151,666; and 51,582, totaling 257,544. They contain no stochastic Monte Carlo results. The deterministic point sets in turns 3 and 5 validate finite algebraic logic, not empirical Poisson fractions.

Every historical manifest is retained and should continue to verify against its named files. FINAL_AUTHOR_MANIFEST.json binds the complete final public packet other than itself. SOURCE_MANIFEST.json and SOURCE_ADDITION_T1.json bind the separately retrieved primary PDFs; those PDFs are not redistributed. The source documents' authoritative URLs, edition, pages and reading scope are recorded there.

TURN_1's cone aperture must be read with the additive correction. The limits claimed are L1 unless explicitly justified otherwise. The turn-5 confidence intervals are fixed-sample statements, not sequential stopping guarantees. The source's sampling convention is not silently identified with point-Palm or volume-weighted sampling.
