# Verification scope and logical bridge

## Hypotheses and evidence

The target includes complex scalars, a separable Banach space, bounded
linear time maps, strong continuity, real nonnegative time, hypercyclicity,
and dense semigroup-periodic vectors. Every requested chaotic time map
has strictly positive time. The printed OWR problem was visually inspected.

The resolving publisher abstract confirms the existence/nonexistence
quantifier pattern, but omits the space, scalar field, continuity, and time
domain. It cannot alone certify those omitted details.

Mangino–Peris (2011), pp. 227–228 and 235, supplies the separable-Banach,
linear, continuous, real-parameter C0 framework and explicitly attributes
the no-chaotic-time-map phenomenon to Bayart–Bermúdez. Its reference [4]
matches the resolving paper's bibliographic metadata.

Conejero–Lizama–Murillo-Arcila–Peris (2017), Definition 0.1, Definition 1.3,
and p. 762, corroborates the strong-continuity and Devaney interpretation.
This is a survey, not the original counterexample. Its general setting
permits scalar-field choices; the exact complex-space construction in the
2009 paper was not inspected. Zaplana's thesis, p. 24, reports the different
mixed-chaotic/nonchaotic example on a separable Hilbert space. That theorem
does not by itself establish the stronger no-chaotic-time example, and it
is not used to fill the gap.

## Elementary logical consequence, conditional on the cited theorem

Write C(S) for chaos of a semigroup and C(T_t) for chaos of a time map.
An example with C(S) and not C(T_t) for every t > 0 refutes both assertions:

1. Every chaotic S has C(T_t) for every t > 0.
2. Every chaotic S has C(T_t) for at least one t > 0.

This implication needs no numerical test or new construction. The issue
is whether the cited example meets all target hypotheses.

## Nearby statements kept separate

Hypercyclicity of positive time maps does not imply dense periodic vectors.
The 2011 paper explains hypercyclic inheritance on p. 228. Its Proposition
2.6 proves chaos at every positive time under its specific Frequent
Hypercyclicity Criterion. That criterion is not an OWR hypothesis.

Mixing also cannot substitute for periodic-point density. Directly from
the definition, if a real-parameter semigroup is mixing, each T_t with
t > 0 is mixing: for nonempty open U,V choose R with T_s(U) meeting V for
every s >= R; then T_t^n(U)=T_(nt)(U) meets V for every n >= R/t. This
proves only mixing, not the missing periodic-point condition.

No conclusion is asserted about Li–Yorke or distributional chaos,
complex-sector time, or arbitrary commutative operator algebras.
