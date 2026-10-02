# Full five-turn review request

Please audit the exact source match and all five scoped proofs before accepting the proposed disposition **unresolved 5/5**. No further author search is requested. The packet is frozen by FINAL_AUTHOR_MANIFEST.json.

Read SOURCE_GATE.md, SOURCE_MANIFEST.json, all SOURCE_ADDITION files, RESULT.md and TURN_1.md through TURN_5.md. Historical manifests retain their original bytes. The primary PDFs are identified by URL/hash; they are retained in the sibling source directory for this audit but are not redistributed in the public packet.

Priority checks:
- Turn 1: visually recheck the printed prefactor, source recurrence and outgoing phase; do not treat an editorial correction as a complete resolution.
- Turn 2: Banach-space block decomposition, nonzero rank-one normalization, constants, excitation, and all-iterate bounds. Verify the strong-norm hypothesis is not claimed for the source PDE.
- Turn 3: holomorphic logarithm/product, Schwarz contraction, Gaussian moments, Cauchy buffer, Taylor remainder and multiplier correction. The exact analytic model must remain distinct from a physical contour representation.
- Turn 4: exact signs and indices of eta_j=B M^j f_0; fixed-frequency compactness; boundary Cauchy uniqueness and the dense-open observation lemma; resolvent-power constants and the high-frequency threshold; paraxial matrix and resonance sign conventions.
- Turn 5: source Assumption C, stabilized illuminated set and incidence lower bound; diagonal quantifiers; absence of an effective reflection scale; exponential-envelope balance; the compact clock example's spectral and frequency-dependence limitations.

Audit every conclusion against RESULT.md. The original remains unresolved: no uncontrolled uniform remainder, analytic-space identification, physical excitation, global shadow or denominator claim is permitted. Abstract examples are not scattering counterexamples. Pre-existing sources and standard methods are credited; no novelty certification is requested.

Run python checks/replay_packet.py from this directory. It requires Python 3 and SymPy for the first checker; all later checkers use the standard library. Compare its output byte-for-byte with checks/replay_output.json. Independent controls should not import these checkers. Report mandatory corrections before a final verdict, preserving this freeze.
