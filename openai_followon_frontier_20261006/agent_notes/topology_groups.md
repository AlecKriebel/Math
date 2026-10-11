# Topology, groups, and operator algebras frontier scan

Checkpoint: 2026-10-06; candidate-identification work 100%, research proofs 0%. No external contacts and no research execution. Source: local OpenAI release at /Users/alec/Desktop/math; conclusions conditional on upstream correctness.

## Highest-impact target in this area: Wall's PD3 conjecture

Target: every integral Poincare duality group of dimension three is the fundamental group of a closed aspherical topological three-manifold. Do not quietly assume finite presentability: establishing needed finiteness is part of the unrestricted formulation. A finitely presented version is a meaningful first stage. Estimated impact 9.3–9.5 if fully resolved, but no credible short route was identified.

New bridge: #246 Cannon plus Bestvina–Mess solves the hyperbolic PD3 case, since the boundary of a hyperbolic PD3 group is S2. Cannon also implies toral relative Cannon by Groves–Manning–Sisto, Boundaries of Dehn fillings, Corollary 1.4 (https://arxiv.org/abs/1612.03497; primary PDF https://homepages.math.uic.edu/~groves/Papers/RelativeCannon.pdf). Their Theorem 1.2 makes sufficiently long cyclic peripheral fillings hyperbolic with S2 boundary, then compactness of Kleinian representations recovers the relatively hyperbolic group. Consequently, proving suitable toral relative hyperbolicity/JSJ geometric decomposition of the remaining PD3 pieces would now finish a much larger part of Wall's program.

Primary context: Michael Davis, Poincare duality groups, Corollary 6.3 and Conjecture 6.4, https://people.math.osu.edu/davis.12/pdgroup.pdf; Bruce Kleiner ICM survey, https://math.nyu.edu/~bkleiner/icm.pdf. CAT(0) atoroidal PD3 groups are already hyperbolic: https://math.uchicago.edu/~shmuel/FLW,%20StableCC.pdf . Thus merely adding CAT(0) does not reach the hard new cases.

Exact gap: no mechanism was found to force arbitrary atoroidal PD3 pieces to be hyperbolic or relatively hyperbolic, or to prove the missing finiteness. Calling this a routine consequence would transfer the central difficulty to an unsupported geometric-recognition theorem. First milestone should be a precise maximal known algebraic JSJ reduction and an explicit class of residual pieces, followed by one new criterion forcing hyperbolicity. Do not launch the unrestricted problem solely because Cannon is now available.

A useful lower-risk follow-on is the relative Cannon conjecture itself, but its implication from Cannon is already explicit in the literature and so it is not the highest-risk/highest-impact independent program. The source Cannon paper and catalogue do not list a relative-Cannon companion.

## Assembly route: high ceiling, major unresolved bridge

#307 (Failure of rational injectivity for maximal coarse assembly, October 5) constructs an infinite-order alpha in KX_1(X), for a bounded-degree finite graph union, with maximal coarse assembly zero. Source introduction is preprints/Failure-of-rational-injectivity-for-maximal-coarse-assembly-October-5-2026/build/sections/01-introduction.tex.

The concrete new mechanism uses three-torus bases, congruence quotients of SL3(Z), line bundles with increasingly divisible roots to preserve topological classes, and Kazhdan averaging to split analytic pushforward. Its alpha is a difference of endpoint torus classes; the universal-norm transfer and long-collar sliding kill the maximal coarse index. This is stronger material than the reduced group kernel of #285.

Potential ambitious next target: a coefficient-free maximal group assembly kernel, ideally a finite-support class for a finitely presented group. First milestone would be a faithful equivariant realization of the endpoint-difference class with its topological detector and the analytic averaging homotopy both preserved. A graphical small-cancellation embedding alone does not establish this; an arbitrary coarse kernel need not come from compactly supported K-homology of BG. Even such a maximal K-theory kernel would not automatically give a counterexample to classical Novikov, which concerns rational L-theory assembly / higher signatures. Thus this is speculative, not a selected highest-impact path with an identified proof mechanism.

Crucial veto: #285 reduced injectivity counterexample cannot simply be promoted to classical Novikov. Its own introduction, subsection Maximal assembly and the Novikov conjecture, proves that its degree-two-detected torus class has nonzero maximal assembly. The exact same candidate class is therefore blocked for a maximal-assembly counterexample. Classical higher-signature failure is not claimed upstream.

## Duplicates and dead ends excluded

- #287 free-group-factor isomorphism already includes failure of generator-invariance for delta, delta0, delta-star, and delta-starstar, and all interpolated factors/fundamental group consequences. Those are not new targets.
- #197 already includes a finitely presented torsion-free nonsofic group, Gottschalk-surjunctivity counterexamples, and Determinant Conjecture failure; asking only for the first nonsofic group duplicates upstream.
- #305 already contains the Wall PD4 counterexample and free-group non-goodness; #320 already supplies nonhomeomorphic homotopy-equivalent aspherical four-manifolds with common hyperbolic fundamental group.
- #320 does not refute high-dimensional Borel: products increase dimension into established Farrell–Jones rigidity regimes and can erase four-dimensional distinctions.
- #252 non-residually-finite hyperbolic group alone does not imply a hyperbolic group without surface subgroups or nonsoficity; those require additional new theorems.
- #315 Singer dimension four gives no evident induction across arbitrary dimensions. Slicing general PD complexes would reintroduce the unsolved central difficulty.

## Recommendation to root

None of these topology routes has both a 9.5+ impact ceiling and a new explicit bridge comparable to a genuine route to a major arithmetic/geometric conjecture. PD3 is the strongest named target; maximal-coarse-to-group realization is the most concrete new mechanism but still has a large unsupported transfer step. Prefer a candidate from another domain if its central gap can be formulated as a specific new estimate or construction actually supported by the released proofs.
