# Acceptance of the conditional fixed cover criterion

## Decision

Accepted in the stated conditional fixed-cover scope for problem 20000440 / AIM-ALGEBRAIC_NUMBER_THEORY-0092. No substantive mathematical correction is required. The complete proof and audit appear in [BRAUER_LIFT_CRITERION.md](BRAUER_LIFT_CRITERION.md); this report records the exact boundary of that acceptance.

## Hypotheses and conclusion

K is a number field, X/K is a smooth projective geometrically integral Enriques surface, and p:Y→X is a specified finite étale double cover with Y a smooth projective geometrically integral K3 surface. The adelic point m of X is orthogonal to all of Br(X). Local liftability of this same m to this same cover at every place is a separate assumption.

For A=Br(Y) or A=Br₁(Y), the quotient

    B = A / (Br₀(Y) + (A ∩ image p*))

is finite. After choosing local base lifts, the global character c and the local difference characters dᵥ descend to B. The dᵥ have one finite support set S, and the attainable global characters are exactly

    {c + Σᵥ∈S εᵥdᵥ : εᵥ∈{0,1}}.

An A-orthogonal adelic lift exists if and only if this exact binary set contains zero. Algebraic orthogonality for A=Br₁(Y) is not promoted to full Brauer orthogonality.

## Mathematical checks supporting acceptance

1. The denominator is a subgroup of A. Br₀ is an image, so no injectivity of Br(K)→Br(Y) is presumed. The intersection with image p* is retained in the algebraic case.
2. Skorobogatov–Zarhin Theorem 1.2 gives finiteness of Br(Y)/Br₀(Y) under these number-field and K3 hypotheses. No rational point or conjectural Tate hypothesis is added. Finiteness then passes to B.
3. A rational point in a degree-two étale fiber splits that fiber into the two distinct local choices. Properness makes arbitrary choices, including infinitely many switches, adelic.
4. The Kummer sequence, spreading of étale cohomology after inverting the torsion order, the valuative criterion of properness, and Br(Oᵥ)=0 for henselian discrete valuation rings with finite residue field justify finite evaluation sums. Applying these inputs to finitely many chosen generators supplies one uniform S for all local points.
5. Global reciprocity and Brauer orthogonality of m annihilate the denominator for the global evaluation. Equal evaluations on the two lifts annihilate it for local differences. Individual local evaluations are not incorrectly asserted to descend to B.
6. Every adelic lift produces a binary vector on S, and every binary vector on S produces an adelic lift. Thus both directions of the equivalence are proved without replacing the binary set by a generated subgroup.
7. Changes of base lifts translate c and reverse the relevant dᵥ; the resulting expressions permute the binary choices. The proof covers base lifts differing at infinitely many places.
8. The corestriction identity p*cor_p(α)=α+ι*α makes ι* act by −1 on B and yields Σᵥ∈S dᵥ=−2c. Complementing all binary choices therefore negates the attainable character. This is an additional consistency check, not an omitted premise of the existence criterion.

## Dependencies and established examples

The finiteness input is [Skorobogatov and Zarhin, Theorem 1.2](https://arxiv.org/abs/math/0605351v4). The written proof names the standard spreading, local Brauer, properness, reciprocity, and transfer inputs it uses; the supplementary finite-group check does not prove those arithmetic-geometric results.

[AIM Question 8, page 48](https://aimath.org/WWN/qptsurface2/qptsurface2.pdf) already contains a negative update dated 25 September 2004. [Harari and Skorobogatov](https://www.ma.imperial.ac.uk/~anskor/HS.PDF) supply the established negative example and the global-twist statements discussed in the proof. The example with parameters a=5, b=13, c=2 and class (y,5) remains attributed to them. Its invariant algebraic class gives zero local differences but a nonzero global obstruction. No new example is claimed.

## Limits

This acceptance establishes a structural criterion once local liftability is known. It does not establish universal compatible lifting, automatic local liftability, an effective algorithm producing B, S and evaluation data, equivalence of the fixed cover with a union over global twists, a general semidirect-product assertion, or a new solution of the broader original AIM question. A global twist must satisfy its own global localization constraints. Independent local switches cannot repair a nonsplit fiber.

Normal Python, -O and -OO reruns each passed 8,842 exact binary base-change comparisons and the abstract cyclic-order-three nonmembership diagnostic. These are supplementary bookkeeping checks, not formal proof verification or arithmetic data for an actual surface. Recorded source PDF and input hashes were rechecked; no source-author code was executed. The source inspection history is preserved as history and does not claim that every page of every source was read again during preparation.
