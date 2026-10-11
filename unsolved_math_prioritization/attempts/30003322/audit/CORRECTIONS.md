# Precise corrections and clarifications

The original frozen package is unchanged. These edits concern exposition and hypotheses; none changes the unresolved 5/5 disposition or the conclusions of Propositions 1--5.

## C1. Required standalone saturation hypothesis

In RESULTS.md, Approach 1, replace the sentence beginning “First-order kappa-saturation of a densely ordered structure” with:

“First-order kappa-saturation of a structure whose distinguished order is dense and has no endpoints implies this order-cut property: the inequalities form a finitely satisfiable partial one-variable type over fewer than kappa parameters. The ordered groups and ordered fields considered here have no endpoints, so Proposition 1 applies to an initial image of such a saturated model.”

Reason: either side of the cut may be empty. Density alone does not make a strict bound beyond an endpoint finitely satisfiable. The actual application already has the missing hypothesis.

## C2. Recommended omitted-type precision

Specify that a partial type is principal here if some formula consistent with U implies every formula of that partial type. The formula need not be a member of the partial type. This is the convention needed for the ordinary Omitting Types Theorem.

The “inconsistent” alternative is logically harmless but cannot occur under the stated nontrivial ordered-group assumptions. Each finite fragment of p_2 is realized by a positive power-of-two multiple, so compactness makes p_2 consistent. The genuine condition is nonprincipality.

## C3. Recommended initial-hull proof precision

Before applying Proposition 2 to an initial additive overgroup of the canonical Z[1/3], intersect that overgroup with R. The intersection is initial and is a dense real subgroup containing Z[1/3], so it contains D. Alternatively, establish first that the smallest initial hull lies in R. This matters because arbitrary ordered supergroups of dense ordered groups need not themselves be dense.

## C4. Recommended canonical field citation

For Proposition 4, either cite the canonical field criterion on printed page 3357 of the Oberwolfach report or invoke Ehrlich--Kaplan Theorem 5.1 for the additive group of F, with exponent set Q and every coefficient group R. Both justify initiality of the displayed canonical field itself, not merely existence of an initial isomorphic copy.

## Additional audited limitation

The displayed groups G_A all fail the aleph_1-cut property: the finitely satisfiable inequalities 0 < y < omega^(-n), n >= 0, have no realization in G_A. Every positive member has a leading term at one finite integer exponent. This can replace the weaker “not asserted to be saturated” disclaimer if desired; it is not needed for validity of the frozen package.
