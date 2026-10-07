# Scope and self-review

This is author self-review, not independent review, peer review, or a proof-assistant certificate.

- Exact source: OWR 32/2022, contribution by Kristin DeVleming (joint with David Stapleton), Conjecture B, printed page 1822. The conjecture is restated in the published JEP paper, page 685.
- Prime degree means degree of the general plane curve. The special curve is initially an abstract smooth curve. A singular plane equation with that genus is not that special curve without a stable-replacement argument.
- Hacking-Prokhorov supplies the ambient classification. A quotient surface with K^2=9 alone is not treated as an actual Q-Gorenstein degeneration.
- A smooth Weil curve can meet a surface quotient singularity. Smoothness alone is not substituted for the Cartier condition.
- The Cartier-index proposition assumes the Cartier embedding; it is not used circularly to prove its existence.
- The limiting-net proof retains the fixed divisor and allows H^0 to jump. It only proves planarity when the actual three-dimensional limiting net is base-point-free.
- The hyperelliptic test objects are not claimed to lie in the closure of the plane locus. Degree seven shows that the tested conditions are insufficient.
- The nodal theorem assumes reduced nodal central curve entirely inside the smooth surface locus. It does not apply to all Calabi-Yau divisors.
- The degree-11 theorem is restricted to irreducible rational unicuspidal curves in P2. Its twelve-case exhaustion is proved without relying on the program's output. No extrapolation of the JEP degree-five/seven graph casework is used.
- The semigroup convention is [0,11j+1), including zero and excluding the upper endpoint. The program computes explicit witness sets using both dynamic programming and coefficient tuples.
- Characteristic gcd chains, not arbitrary Puiseux terms, are enumerated. Positive later increments consume the conductor budget, and each gcd strictly drops. The manuscript explains why the threshold forces multiplicity at most seven and hence at most two characteristic exponents.
- Existing DeVleming-Singh classification already yields the degree-11 cusp obstruction; independent rederivation has no priority claim.
- Literature status is a bounded primary-source check through 7 October 2026, not an exhaustive publication search.
- Independent mathematical audit is still required before any acceptance claim.

Replay: python3 verify_math.py and python3 -O verify_math.py. Both produced identical output. Three deliberate negative controls reject a missing candidate, a false count, and a half-open/closed interval confusion. Numerous arithmetic cases are supporting regression checks, not a substitute for the geometric proofs.
