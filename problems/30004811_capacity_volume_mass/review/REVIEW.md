# Independent full review: capacity–volume and ADM mass

PASS, with the two formulations kept separate. Recommended disposition: credited already_solved1/5 for the standard physical-class conjecture, accompanied by the verified counterexample to the unrestricted all-AF reading. No novelty certification.

## Exact source and prior chain

The OWR printed2257 conjecture and surrounding curvature/mass hypotheses were visually inspected. Jauregui's full-paper p4 explicitly limits the conjecture to nonnegative scalar curvature and empty/minimal boundary. Its normalized capacity, compact-exhaustion definition and equivalence of deficit formulas were checked. The short report's missing energy prefactor is shorthand, not a different target.

For that standard smooth one-ended AF class, the credited chain m_ADM<=m_CV<=m_iso=m_ADM is valid. Jauregui Theorem5 needs nonnegative scalar curvature only outside a compact set; the stated class satisfies it. The isoperimetric/ADM equality has the cited empty/minimal boundary scope. The middle inequality follows from SIGMA2023 Theorem5.6 at p=2, with its proof through Theorem5.5 and equations5.6–5.12 checked. Published Theorem1.3 has an extra H2 hypothesis and is not used to silently remove it. The sign-sensitive substitution is legitimate because m_iso=m_ADM>=0 in the claimed class; choose a strictly positive upper m before taking its limit at zero. The later correction is appropriately qualified. No all-sign or all-p statement is inferred from this restricted chain.

The p=2 normalization and conversion via Jauregui Lemma10/SIGMA Proposition5.2 agree. Approximating compact sets by smooth supersets increases volume and changes capacity by an arbitrarily small chosen error, so the smooth-domain comparison covers the exhaustion supremum. The standard positive-mass, isoperimetric-mass, capacity regularity and geometric-analysis theorems remain credited external inputs; this is not a foundational re-proof of them.

## Complete negative example for the literal broader reading

Every step of TURN_1 was checked. The smooth cutoff u=1-chi(r)/r is identically1 near the origin and uniformly lies between1/2 and1; g=u^4 delta is smooth, complete, boundaryless and one-ended. Its end is exactly the mass−2 Schwarzschild conformal end. The ADM integrand reduces to−2r²u³u_r and has limit−2. Scalar curvature is smooth and compactly supported, hence integrable, but is not asserted nonnegative. Thus this is a source-admissible all-AF metric, without a hidden singularity.

The displaced balls B((R/2)e1,R) are smooth, nested and exhaust all of R3; their exterior lies wholly in the unmodified harmonic end. The conformal Laplacian identity shows that the quotient of the Euclidean capacitary potential by u is genuinely metric harmonic. It has the correct boundary values and finite energy; uniqueness and normalized flux give capacity exactly R−1. The actual energy density is u² times Euclidean gradient energy. This identity is both directly verified and credited to Jauregui equation41, whose derivation precedes the nonnegative-mass volume estimate.

The compact filling changes the volume expansion only by a bounded constant. The exterior binomial remainder is O(r^-2), whose integral over these balls is O(R). Independent angular integration gives the solid-ball Newton potential2pi(R²-d²/3); at d=R/2 it is11piR²/6. Therefore volume=(4pi/3)R³−11piR²+O(R), and its normalized radius is R−11/4+O(R^-1). Subtracting the exact capacity yields limit−7/4. The supremum over all exhaustions is at least that number, strictly larger than ADM−2. No claim that the exhaustion is optimal or that m_CV is exactly−7/4 is needed or made.

The negative example does not contradict the standard nonnegative-curvature conjecture or its credited resolution. It diagnoses precisely the broader literal wording.

## Reproduction

The frozen author-manifest entries and all seven primary PDFs were verified. The author's5,529 supplementary SymPy checks replay byte-exact. Independent check.py derives the angular primitive, shell integral, volume-radius coefficient, flux and ADM coefficients and conformal divergence identity, with additional exact strict-gap/exhaustion controls. CHECKS.json records the totals. Scalar controls supplement the complete all-R argument; they are not the proof of capacity minimization or a literature theorem.

## Publication requirements

Keep both conclusions prominent: affirmative credited standard physical class; negative unrestricted all-AF formulation. Preserve source definitions, raw-source exclusion and frozen author bytes. One genuine turn was used for the negative example, even though the positive prior-resolution check itself was a source gate. No further author search is necessary for this frozen scope.
