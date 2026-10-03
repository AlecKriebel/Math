# Martingale for practical purposes: five scoped attempts

Problem 9700001 / AMR-096-0001, David Aldous's [Martingale, for practical purposes](https://www.stat.berkeley.edu/~aldous/Research/OP/fields.html).

## Disposition

**The general source question remains unsolved in this packet after five substantive attempts.** These are fully proved special-case answers and limitations, not a canonical definition of practical martingales or a universal impossibility theorem. No historical novelty or exhaustive literature-status claim is made. The standard conditional-expectation, linear-algebra, optimal-stopping and concentration methods retain their classical credit.

## Results and proof map

1. [Finite filtrations](TURN_01_FINITE_FILTRATIONS.md): n-1+sum m_t stopping equalities exactly characterize fairness against every stopping time in a specified finite observation filtration. Includes explicit witnesses, quantitative bounds, and a coarse-information counterexample.
2. [Feature coverage](TURN_02_FEATURE_COVERAGE.md): a survival-indicator approximation inequality with explicit residual and coefficient costs. A four-path counterexample separates adjacent current-state fairness from full-history fairness.
3. [Fixed-library obstruction](TURN_03_FIXED_LIBRARY_OBSTRUCTION.md): fewer than 2^n-1 fixed stopping maps cannot characterize all martingales on an n-bit tree. The missed process can have a polynomial-size rational description, reveal all information through its prices, and have a simple nonzero witness. The theorem is restricted to maps fixed before the process, with no inverse-polynomial advantage guarantee.
4. [Finite-state Markov models](TURN_04_MARKOV_MODEL.md): polynomial stopping certificates and exact optimal deviation with constructed policies, given a fully observed explicit rational Markov model. This is a credited classical-model answer.
5. [Statistical access](TURN_05_STATISTICAL_ACCESS.md): simultaneous finite-library sampling certificates at a specified tolerance, and a rare-event lower bound excluding uniform exact-zero decisions from a bounded sample budget.

## What remains

One must still specify and justify a generally useful observation/computation/access model for the source's word 'practical', and show that its allowed stopping rules can be detected or certified efficiently. Neither arbitrary succinct processes nor the full class of polynomial-time stopping algorithms is covered by the polynomial certificate results. Restricting the filtration, assuming a small fully observed Markov state, and checking a chosen finite library are different hypotheses. The fixed-library obstruction does not rule out adaptive or law-dependent choices, approximate notions, or classes larger than all martingales.

## Reproduction

Use Python 3.9 or newer, with the standard library only:

    python verify.py > reproduced.json
    cmp VERIFICATION.json reproduced.json
    python verify_bundle.py

The supplied receipt records 109,255 exact rational assertions. The checker exhausts small adapted processes and small history policies, tests rational nullspace constructions with price decoding, compares Markov recursions against all stopping policies on small trees, and checks statistical threshold algebra and rare-event inequalities. Finite controls supplement the analytic proofs; they are not a formal proof assistant or a mathematical completeness test.

Read [source scope](SOURCE_GATE.md), [attempt log](ATTEMPT_LOG.md), and [disposition metadata](DISPOSITION.json). MANIFEST.sha256 fixes the author packet bytes. This is AI-assisted mathematical work awaiting separate review; it is not human peer review. No primary-source PDFs, source images, or full source reproductions are distributed in this packet.
