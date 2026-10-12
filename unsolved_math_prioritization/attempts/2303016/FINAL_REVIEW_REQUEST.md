# Independent full source/method/proof review request

Problem2303016 / AMR-022-3016. Complete candidate after one author turn, proposed credited already_solved1/5. Please audit the requested *direct proof*, not just the already-known conclusion.

Read the original Problem3.16 and Update3.16 on Hayman–Lingham printed p.65/PDF p.66. Read Hedberg–Wolff Theorem2 and its Borel-set proof, pp.173–174, for credit and method overlap. Both primary PDFs are hash-bound in SOURCE_MANIFEST.json.

Proof-sensitive steps in TURN_1.md:

1. Energy-minimizer existence and first variation using normalized restrictions, with no hidden q.e. equilibrium/Kellogg assumption
2. Lower semicontinuity and density of full-measure support points, followed by the nearest-support bound U<=2^(n−2)J off support
3. Restriction-energy capacity domination with the correct mass normalization
4. Joint upper semicontinuity of the closed-ball compact capacity; Borel measurability of the tail integrals; proper use of Choquet *capacitability*, not the fine-topological Choquet property
5. Positive-mass localization to a compact K on which the tail is uniformly small and diam(K)<=delta/4
6. Tonelli layer cake, the tail bound divided by J, and the final pointwise/measure-a.e. contradiction
7. Exactly formulated power-weight and exceptional-set sharpness, including the dyadic energy proof for a line segment

The only unreproved capacity-theoretic foundations are Borel capacitability and polar-capacity-zero equivalence; confirm these are noncircular inputs relative to the source's method request. Do not silently turn an unspecified all-gauge sharpness question into a proved claim.

Run standard-library Python:

    python verify_turn1.py > /tmp/turn1.json
    cmp TURN_1_CHECKS.json /tmp/turn1.json

These finite controls cannot prove polarity. Verify all final/turn manifest hashes and both PDF hashes. The author packet is frozen and no further author search is intended before review. No raw PDFs, imported records or private material are included.
