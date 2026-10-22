# Source contract fixed before author proof

Fixed at 2026-10-15T11:22:27.356140+00:00. This contract follows direct primary reading. The log discloses exposure to the native prior report before this memo; no author argument or old audit has been read.

## Exact target and success criterion

The complete native record PID 9900008 / AMR-098-0008 points to Thorisson, *Some Open Probability Problems*, Problem 4.1 (printed p. 6; setup and formula (4.1) on p. 5). The question is the implication from invariance under **every measurable preserving allocation derived from the joint state (X, ξ)** to mass-stationarity, assuming ξ is diffuse. The reverse implication is already supplied by the Palm/invariant-transport results. A negative solution needs one admissible pair for which the complete allocation test holds but mass-stationarity fails. It need not settle every group, smooth density case, or stationary-background variant.

The group in the setup is locally compact, second countable, Abelian (2009 definitions also explicitly Hausdorff). Problem 4.1 does not inherit `G = R^d` from the separate Theorem 4.3 unless stated as a specialized subquestion. A counterexample on R^d is nevertheless inside the advertised domain. `X` is an arbitrary random element in a measurable G-space; no nontriviality, freeness of the action, or auxiliary randomness is required. Thus constant X with a trivial action is permitted.

## Allocation quantifiers

For a measurable state function π, the source defines τ_z(s) = s + π(θ_s z) for z = (X, ξ), and tests θ_{π(z)}z having the same law as z whenever (τ_z)_* ξ_z = ξ_z. Equivariance is exact in the 2009 definition (Example 3.4, printed reprint p. 9). Any measurable π on the stated state space induces such an equivariant allocation; extra ambient randomness must not be silently made accessible to π. A canonical pair-state counterexample may choose its own underlying measurable space.

The basic preserving definition is pointwise in all states and all Borel sets (2009 (3.3), Example 3.4/(3.6), pp. 8–9). The same paper explicitly defines a Q-a.e. balancing variant. A proof must state which convention it uses. For a negative example, verify the strongest relevant class or show why almost-every-state preservation does not create an escape. Preservation is equality of measures, so constraints hold ξ-almost everywhere in s; that alone need not determine τ at the origin. A claim about τ(0) requires an additional argument (typically covariance/stabilizers), especially for diffuse ξ where ξ{0} = 0.

The source tests all measurable allocations, not only bijections, continuous maps, support-preserving maps pointwise, transports with densities, local maps, or a specified selection rule. Mass preservation permits a spatial exceptional set of ξ-mass zero. Any hidden reduction in this class must be justified. Joint measurability of the G-action and of τ, π is part of the mathematical setup.

## Random-measure and mass-stationarity boundary

Last–Thorisson (2009), pp. 4–5, uses locally finite Borel measures, finite on compact sets, with the evaluation σ-field. On an LCSC Hausdorff group these are Radon and σ-finite. Diffuse means absence of point masses; it does not mean absolute continuity with respect to Haar measure. Neither the Thorisson question nor the 2009 formulation imposes positive stationary intensity, absolute continuity, full-dimensional convex hull, full Haar support, a free action, finite total mass, or nonperiodicity. Such additional hypotheses define a narrower theorem and cannot be imported into the source problem.

Definition 6.1 (2009, reprint p. 18, (6.2)) works for σ-finite Q and requires Q(ξ(G)=0)=0. For probability Q its joint resampling test is (θ_V z, U+V) equal in law to (z,U), where U is Haar-uniform on a relatively compact Borel C with positive Haar measure and Haar-null boundary, independent of z, and V conditional on (z,U) samples normalized ξ on C−U. Formula (6.1), p. 17, supplies a probability fallback when ξ(C−U)=0. Under a genuine Palm law the origin lies in supp ξ; an alleged counterexample should preferably ensure nonzero ξ and 0 in supp ξ so failure is substantive rather than a degenerate excluded case. The abbreviated open-problem note suppresses these technical qualifications; the 2009 definition controls interpretation.

## Backgrounds and kernels are distinct questions

Thorisson Theorem 4.3, p. 6, uses every independent stationary shift-measurable background Y and tests the enlarged state (X,Y,ξ), on R^d. Problem 4.1 explicitly asks whether that addition can be removed. A proof may not omit Y by calling it latent information already available in X or in the ambient sample space. Conversely a negative background-free counterexample is not required to remain allocation-invariant after arbitrary independent backgrounds are adjoined.

Thorisson Theorem 4.4/(4.2), p. 6, and Last–Thorisson Theorem 7.2, p. 23, concern bounded invariant ξ-preserving **weighted** kernels. Markov kernels can split mass; deterministic allocations are Dirac kernels. Problem 4.2 / 2009 Problem 7.3 concerns Markov kernels and is separate from Problem 4.1 / 2009 Problem 7.5. No negative allocation example may be described as a negative answer for every Markov kernel without proving that stronger assertion.

## Falsifiable checks after the author proof is opened

1. Confirm the claimed example belongs to the full source domain, with its actual X, ξ, law, state space, action, support, and local finiteness.
2. Test arbitrary measurable allocations, including spatial ξ-null-set modifications and state-a.e. preservation conventions.
3. Verify the law is invariant under their origin shifts, not merely that ξ is preserved as a measure.
4. Exhibit a qualifying C and a measurable event/statistic showing failure of the full joint mass-stationarity identity; validate every normalization and support assertion.
5. Check whether a restriction (singularity, stabilizers, nonfree action, low-dimensional support) is explicit and admissible, rather than silently excluded by the real source.
6. Read central antecedents and credit their exact role; distinguish source resolution from claims in later restricted transport problems. No new priority campaign or central proof search is included in this bounded audit.
