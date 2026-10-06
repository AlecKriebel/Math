# Target and hypothesis audit

## Catalog target

The target asks whether a translation-invariant, finite-energy, positively associated percolation process on the nearest-neighbor square lattice, having an infinite open cluster almost surely in the whole lattice, must have an infinite open cluster almost surely in each half-plane.

A half-plane restriction means keeping only the vertices and edges contained in that half-plane. A whole-plane infinite cluster intersecting a half-plane in infinitely many vertices is insufficient: its intersection may have only finite connected components.

## Primary-source qualification

Benjamini's *Coarse Geometry and Randomness*, archived author PDF, Open Problem 8.5 on PDF/printed page 57, asks the corresponding question using the word invariant. Two pages later, Definition 8.9 defines invariant percolation as a bond law invariant under all graph automorphisms. On the square lattice this includes translations, coordinate reflections and quarter turns. The catalog explicitly says translation-invariant and does not explicitly choose site versus bond percolation.

Consequently, treating the catalog as exactly equivalent to the source would require an additional interpretive justification. This packet does not supply one. It retains the translation-only catalog problem as its main target, takes the primary bond convention when discussing bond duality, and labels the separate site versions of elementary lemmas. Neither the translation-only target nor the stronger-symmetry source reading is resolved here. No reflection, rotation, ergodicity, mixing or spatial Markov property is silently added.

The source cites Häggström–Mester [HM] for background and the importance of positive association. The inherited reference to Benjamini–Liggett–Schramm was not verified and is not used as a theorem citation.

## Explicit conventions

1. Finite energy means that each coordinate's conditional opening probability, given all other coordinates, is strictly between zero and one almost surely. Uniform finite energy bounds these probabilities away from both endpoints by one deterministic positive constant. The latter is stronger.
2. Positive association, also called the FKG inequality here, means nonnegative covariance of increasing bounded observables, equivalently the event inequality for increasing events. The finite-volume lattice condition is stronger; conditional positive association is not assumed.
3. Ergodicity under the full translation group is distinct from ergodicity under one-dimensional horizontal translations. Neither is in the catalog hypotheses.
4. Mixing, finite-range dependence, stochastic domination by a supercritical product law, and Gibbs/domain-Markov specifications are additional assumptions.
5. For the elementary invariant-event lemma, each prescribed affine Euclidean half-plane is covered, including irrational slopes. It does not prove percolation in any of them.
6. “For every fixed half-plane, with probability one” and “with probability one, simultaneously for all half-planes” differ for uncountably many directions. The strong-density theorem proves the stronger simultaneous statement through a countable family of quadrants. No such simultaneous conclusion is claimed for the general target.
7. Bond planar duality and closed nearest-neighbor site connectivity are different notions. Site rectangle blocking uses closed star-connected paths (allowing diagonal steps), not closed nearest-neighbor paths.

All retained proofs state their hypotheses where used. None conditions on a discovered interface and then invokes an unproved conditional FKG inequality. No claim that positive association automatically passes to an arbitrary ergodic component is needed or made.
