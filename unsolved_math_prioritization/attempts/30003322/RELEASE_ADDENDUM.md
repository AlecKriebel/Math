# Controlling release addendum: initial surreal set models

Problem 30003322 / OWR-15181-014, rank 664. Current disposition: **unsolved, 5/5**.

This addendum is controlling for the present draft. Read the unchanged author package together with the independent audit and this addendum. It adopts all four corrections C1–C4 from `audit/CORRECTIONS.md` and the audit's additional saturation limitation. The frozen author and audit bytes are historical records and are preserved without rewriting. Their historical references to a pending audit, a proposed exhausted status, or no remote writes describe the time of those records; the current draft has the completed independent audit and the queue disposition above.

Neither universal set-model converse is proved or refuted. No novelty, independence, consistency-strength, or worldwide-current-openness claim is made. The five approaches are exhausted; the mathematical target remains unresolved. No additional search turn is represented by these publication clarifications.

## C1. Saturation requires a dense order without endpoints

The standalone saturation sentence in `author/RESULTS.md`, Approach 1, is to be read as follows:

First-order kappa-saturation of a structure whose distinguished order is dense and has no endpoints implies the kappa-cut property: the inequalities form a finitely satisfiable partial one-variable type over fewer than kappa parameters. The ordered groups and ordered fields considered here have no endpoints, so Proposition 1 applies to an initial image of such a saturated model.

The no-endpoints hypothesis is essential when either side of the cut is empty. Density alone does not ensure finite satisfiability of a strict inequality beyond an endpoint. The target ordered groups and fields already satisfy this hypothesis.

## C2. Partial-type principality and the genuine omission condition

In Approach 2, a partial type is principal if some formula consistent with the complete theory U implies every formula of that partial type. The witnessing formula need not belong to the partial type. This is the convention used for the countable Omitting Types Theorem.

Under the stated nontrivial ordered-abelian-group assumptions, p_2 is always consistent: each finite fragment is realized by a positive sufficiently large power-of-two multiple, and compactness applies. The original inconsistent alternative is therefore vacuous. Nonprincipality is the genuine condition in the conditional reduction. It is not automatic and fails, for example, when positivity isolates the type in a 2-divisible theory.

## C3. Apply the dyadic argument to the real intersection

For the initial additive hull of the canonical Z[1/3] in Approach 5, let G be any initial additive overgroup and first consider G intersect R. This intersection is initial, contains Z[1/3], and is a dense subgroup of R. Proposition 2 gives D within this intersection. Bezout's identity then gives D + Z[1/3] = Z[1/6]. Conversely Z[1/6] lies in R, contains D, and is initial. This proves the asserted smallest initial additive hull without assuming the false general claim that every ordered supergroup of a dense group is dense.

## C4. Initiality of the displayed canonical field

For Proposition 4, use the canonical field criterion on printed page 3357 of the Oberwolfach report (https://doi.org/10.4171/OWR/2016/60), or apply Ehrlich–Kaplan Theorem 5.1 to the additive group of F, with exponent set Q and every coefficient group R. Along with the proved truncation closure and cross-section, this establishes initiality of the displayed canonical subfield F itself, not just existence of some isomorphic initial copy. The source URLs, inspected locations, and exact PDF hashes are recorded in `audit/SOURCE_CHECK.json` and `author/SOURCE_VERIFICATION.json`.

## Additional audited limitation: none of the displayed Hahn groups has the aleph_1-cut property

For every displayed G_A, the countable inequalities 0 < y < omega^(-n), for all n >= 0, are finitely satisfiable but have no realization in G_A. A positive member has a leading term c t^k with c > 0 and finite k, so t^n is smaller once n > k. These groups are therefore not aleph_1-saturated examples. Their coefficient and tail defects do not answer either universal set-model converse.

## Byte-level binding and verification limits

- Frozen author manifest SHA-256: `4a0a5cece35d143c2ebdf3683f0a7a115588f2a42b5730af77ac21aee7a84a54`.
- Frozen audit manifest SHA-256: `0d32cc832178f02c733816134d0d5f1b04dbc89c44ba049bd11cce5d11094992`.
- Audit corrections SHA-256: `71e40d236f727d5975c6f3c65dfc9bfca9a098e00597bb5d5cea5e5c9a165333`.

The release manifest and verifier bind this controlling addendum as well as every frozen file. The exact finite controls support the specified examples only; they do not formalize NBG, surreal arithmetic, infinite supports, or the two universal model-theoretic claims. Published embedding criteria and the ordinary completeness/Omitting Types results remain stated external dependencies.
