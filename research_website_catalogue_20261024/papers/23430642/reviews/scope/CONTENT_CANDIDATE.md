# Draft explanatory content — awaiting mathematical clearance

## Complete technical abstract candidate

For explicitly listed rational two-player payoff matrices of variable positive dimensions with exact rank(A+B)=1, this preprint claims that deciding uniqueness of the entire mixed-strategy Nash equilibrium pair is coNP-complete, and that deciding nonuniqueness is NP-complete. Arbitrary degeneracy is permitted. The reduction maps a nonempty positive-integer PARTITION instance to a game with a known strict pure equilibrium and produces an additional equilibrium exactly when the instance has a partition. It connects the Disser–Skutella signed flow counter to the Adsul and coauthors auxiliary zero-sum representation. A comparison-preserving rational perturbation isolates the minimum-cost flow at every real demand, an injective simplex encoding translates diagnostic bridge flow into the scalar equilibrium condition, and a uniform exact penalty of polynomial bit length controls every auxiliary minimizer. Rational support-polytope certificates cover membership even when equilibrium sets have positive dimension. The reduction has polynomial binary size and does not execute the exponentially long flow trajectory used in its correctness proof. It does not claim hardness under a nondegeneracy promise, at fixed dimensions, for equilibrium payoffs, or in the strong numerical sense. The preprint is unrefereed, was developed with extensive AI assistance, and does not establish worldwide priority.

## Plain-language candidate

A Nash equilibrium is a pair of strategies from which neither player benefits by changing their own strategy alone. Some games have one such pair; others have several. For rank-one games—a special algebraic class defined by the sum of the two payoff tables—earlier research gives an efficient method to find one equilibrium.

This paper addresses a different task: deciding whether that equilibrium is the only one. Its claimed result says that this decision problem is coNP-complete, even when a strict pure equilibrium is already supplied. The construction turns a number-partition problem into a game whose supplied equilibrium has a companion exactly when the numbers can be split equally. It uses an earlier network-flow construction and an earlier representation of rank-one equilibria, with additional arguments intended to cover every equilibrium, including degenerate cases.

The surprising distinction is that finding an equilibrium can be efficient while certifying that no other equilibrium exists can be computationally hard. This is a worst-case complexity claim about games of growing size, not a claim that every particular game is difficult.

## Status and collaboration wording candidate

Unrefereed preprint, version 1.0, 13 October 2026. Developed with extensive AI assistance; no conventional external human peer review is claimed. Current independent programme review is pending.

Researchers with expertise in computational game theory, parametric network flows, or complexity reductions are welcome to examine the proof and discuss substantive collaboration. Any coauthorship would reflect an actual intellectual contribution and agreement among the contributors.

## Follow-up

None proposed at this stage. The review has not established a follow-up that clears the requested high bar for novelty and paper-level value.
