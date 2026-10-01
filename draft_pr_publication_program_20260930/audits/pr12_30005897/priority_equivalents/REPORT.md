# Equivalent-mechanism priority audit of PR12 / problem 30005897

Final conclusion: **the full target is a checkable corollary of older equivalent Banach-lattice machinery**. The narrowed mathematical translation passed a fresh independent adversarial check. Treat the candidate as a credited known-method corollary or alternative elementary proof, rather than promoting broad theorem novelty. Novelty of its elementary proof or explicit density criterion is a separate, unconfirmed question.

The exact target is shadowing iff generalized hyperbolicity for bounded invertible dissipative scalar composition operators on all real/complex `L^p`, `1<=p<infinity`, on a sigma-finite space with a finite positive wandering generator. The target includes arbitrary measurable `W` and complementary measurable support bands, not only a single scalar fiber, bounded distortion, separable Hilbert spaces, or a weaker pseudo-hyperbolic description.

## The decisive equivalent route

The decisive imported theorem is [Kitover–Orhon, arXiv:2009.09303v2 (2020), Theorem 2.26](https://arxiv.org/html/2009.09303v2). It states and attributes to [Kitover 2011, Theorem 3.29](https://doi.org/10.1007/s11117-010-0106-4) a global clopen-transition decomposition for a bounded-below scalar weighted difference operator on an aperiodic Stonean space. Its compact global tail conditions directly yield a clopen one-step split and uniform exponential weight products. Those products are exactly the primal `L^p` norm ratios after the integer-coordinate change. This supplies the difficult measurable support splitting across arbitrary fibers.

The rest of the implication is now proved directly in the certificate, without relying on a blanket claim of old spectral-transfer proof validation. A finite-average bounded-forcing argument gives `I-B*` bounded below from shadowing. A geometric coordinate cutoff transfers central `L^infinity` approximate vectors to the concrete dual `L^q`, so the central `I-C` is also bounded below. At `p=1` the dual is already central. Coordinate residue partitions exclude periodic Stone points; real shadowing complexifies and the real indicator split restricts back. If 1 lies in the central resolvent, gauge rotation and Riesz projections invariant under all multipliers give a clopen split independently. No separability or bounded distortion enters.

The independent falsifier found a real algebra failure in K20 proof 5.2 equation (33): powers of `wU^-1` and `wU` have different directed weight products. It gave an explicit countercheck and two independent minimal-transfer proofs, verified the direct necessary estimate and resolvent case, and passed all global-tail, endpoint, empty-band, uniformity, measurability, and support-orientation checks. The final certificate excludes full spectrum equality and reverse transfer entirely. See [EQUIVALENT_TRANSLATION.md](EQUIVALENT_TRANSLATION.md) and [the independent falsification artifact](kitover_translation_falsifier/FALSIFIER.md).

The global structural mechanism is documented in the inspected K20 version dated **2020-12-19**, with earlier credit to the 2011 paper (online 2010-12-08). This audit establishes a derived corollary of older machinery; it does not locate an earlier printed statement of the exact no-bounded-distortion composition theorem or the date someone first recognized this combination. Historical context includes Dragičević–Pituk's July 2026 duality theorem, restated in Pituk's August 2026 primary preprint, but the final certificate needs no inaccessible duality proof.

The candidate's displayed density-drop condition is also a consequence of these older bands: choose a common large `d` so that both primal operator bounds are below one, and use the exact norm identities to bound `rho_(n-d)/rho_n` on the stable support and `rho_(n+d)/rho_n` on its complement. A countable union yields one common base null set. The certificate records this formula corollary without claiming its literal earlier printing.

## Other families and why they do not independently certify the full target

| Family/source | Verified mechanism and scope | Exact missing translation if used alone |
|---|---|---|
| D’Aniello–Darji–Maiuriello 2021 baseline | Composition/weighted-shift equivalence with bounded distortion | Removal of bounded distortion |
| CDV 2024 baseline | General shift representation and finite-dimensional fiber Corollary 2.16 | Infinite measurable fibers and uniform band splitting |
| Bernardes–Messaoudi scalar shifts / Pinto 2026 Theorem 18 | Scalar coordinate Banach sequence spaces | Passing from individual fibers to a uniform measurable splitting |
| Pinto 2026 Theorem 22 / Remark 23 | Sufficient product estimates on continuous-function spaces; partition multipliers | Necessity; closed direct invariant splitting is explicitly not automatic |
| Pinto 2026 Theorem 32 | Metric base, distance-preserving map, uniformly continuous weight, admissible continuous-function space | Arbitrary measurable `W` and weights |
| Latushkin–Montgomery-Smith–Randolph 1999 Theorem 4.1 | Evolutionary operator hyperbolicity iff uniform invertibility of fiber difference operators iff exponential dichotomy | Assumes genuine invertibility/unique bounded solutions and topological cocycles, while generalized hyperbolic shifts may have nonunique bounded solutions |
| Dragičević 2015 admissibility | Official metadata/abstract inspected; original PDF export failed | No positive full-theorem certificate can be issued from inspected scope |
| Pituk 2026 Theorem B | Separable complex Hilbert shadowing iff generalized hyperbolicity | General `p`, real case, nonseparable measure spaces; old lattice route supplies these |
| Messaoudi et al. 2026 | General Banach counterexamples and Hilbert pseudo-hyperbolicity | Pseudo-hyperbolicity does not supply the required direct invariant generalized split |
| BDM 2026 aggregate-mass examples | Aggregate tests can fail outside bounded distortion | Negative aggregate examples do not settle pointwise-band mechanism |
| Wu–Wang 2026 | Weighted shifts on the product Fréchet topology have shadowing | Different topology; no Banach `L^p` conclusion |
| Menet–Papathanasiou 2025 operator shifts | Official preview concerns dynamics of `l^p` and `c_0` operator sums | Fulltext inaccessible; inspected preview supplies no shadowing equivalence |

## Source and proof-access limits

The positive structural certificate uses the official version-pinned **primary full text** and the exact printed global-tail theorem, together with independent proofs of the remaining steps. Original Kitover 2011 proofs remain subscription-restricted; K20 states the theorem and attributes it to K11. Without the original, no literal-text identity between the two versions is asserted. The scalar theorem itself is not independently reproved in this audit. This is a source-proof access limit, not a failed hypothesis match or an equivalent unsupported version of the composition problem.

Dragičević–Pituk's original publisher PDF returned 403 and is not a premise. The broader K20 equation (33) algebra issue is recorded and excluded. Official old HTML re-rendering inserts a 2026 internal typesetting date; arXiv version headers and histories establish the version date. The K20 PDF has the header 19 December 2020 and internal date 22 December 2020. All retained third-party content is in ignored `tmp/priority_equivalents`; `SOURCE_MANIFEST.json` records versions and hashes.

This is a bounded search, not an assertion that every historical equivalent result has been located. The verified old global mechanism is sufficient to defeat a claim that the central measurable support splitting is a wholly new discovery. Exact-statement first publication and novelty of the candidate's proof presentation remain unconfirmed. Audit completion: **100%**, final checkpoint 2026-10-01 13:36 UTC. No external individual was contacted, and no canonical or Git mutation was made.
