# Archived degree-three search model

This experiment was a failed search for an obstruction. Its output is **not a certified computation of the arrangement's fundamental group, a nilpotent quotient, or its integral E-infinity structure**.

The program constructs a real wiring order, truncated noncommutative Magnus polynomials, and finite-field linear systems for degree-two corrections to prescribed degree-one generator permutations. It compares both choices of half-twist convention. Critical-value and initial-height comparisons are exact in Q(sqrt(5)).

All24 finite systems were consistent: four primes, three permutations and two signs. This does not assert that a group lift exists. Even consistency in a certified finite truncation would not imply an integral lift through every stage or an automorphism of the complete group.

Reproduce with Python3 and SymPy:
    python class3.py

The command prints its diagnostics and replaces the adjacent class3_results.json. No external data is downloaded. The matrices are a reproducible formal model only. Mathematical claims in the main artifact are confined to the explicitly proved finite geometry and source qualifications; none relies on this screen.

The presentation-to-topology and truncation-to-group validation was not completed, and no low-degree inconsistency was found to motivate expanding the computation. This limitation is the stopping reason for the second approach.
