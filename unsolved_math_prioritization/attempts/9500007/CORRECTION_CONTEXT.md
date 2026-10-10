# Contextual correction to Section 7

This audit correction belongs to the fifth existing approach. It is not a sixth approach, a resolution of Problem 7, or a change to the five-approach exhausted disposition. The original frozen packet is unchanged.

## Issue

The original Section 7 says that reflected boundary local-time terms can compensate the covariance drift. Taken as cancellation of measures in a constant-distance identity, that sentence is false in the stated C2 setting. The covariance drift is absolutely continuous with respect to time; normal-reflection local-time terms are singular with respect to time. They can offset in cumulative finite-time balances for a varying distance, but cannot cancel those two measure components in an identity that remains constant.

## Replacement clarification and corollary

For ordinary normally reflected Brownian motion in a bounded C2 domain, the set of times spent on the boundary has Lebesgue measure zero almost surely. This follows, for example, from the absence of boundary mass in every positive-time marginal and Tonelli's theorem. Each local-time measure is supported on the corresponding boundary-time set and is therefore singular with respect to dt.

Consequently the conclusion of Proposition 7 also holds across boundary visits. Suppose, under its co-adapted representation, that |X-Y| is almost surely constant throughout a fixed time interval, or throughout a stochastic interval between stopping times where the stopped semimartingale statement is valid. The continuous local-martingale part of d|X-Y|^2 then vanishes by uniqueness of the local-martingale/finite-variation decomposition. Its remaining finite-variation measure is the sum of tr(Sigma) dt and a singular signed measure. Uniqueness of the Lebesgue decomposition forces tr(Sigma)=0 almost everywhere in time on that interval. Since Sigma=(I-J)(I-J)^T+KK^T, the sum of the two squared Frobenius norms is zero, and J=I, K=0 almost everywhere.

This is an audit corollary of the existing calculation, not a lower-bound-only result. Positive-probability uniform separation does not make the distance process constant. For a varying distance, normal-local-time contributions can affect cumulative distance balances and their signs depend on geometry. No conditional change of measure or assertion that conditioning on separation preserves Brownian marginals is licensed.

## Exact preserved scope

The strengthened constant-distance statement still assumes ordinary normal reflection in a bounded connected C2 domain and a co-adapted driving representation. It does not classify every shy coupling, prove existence of a deterministic function coupling, handle every rough domain in the source, or remove the source's unspecified measurability and initial-law conventions.

## Occupation-integral convention

The corrected Proposition 4 explicitly says jointly measurable. This makes the occupation integrals in its proof well-defined. Ordinary continuous reflected-Brownian paths satisfy this convention. It is a hypothesis clarification to the abstract compact-state lemma, not an added hypothesis in the statement of Burdzy's question.
