# Completed adversarial derivations

These extend the immutable pre-primary OWN_DERIVATIONS.md. No earlier result is rewritten and no current peer/root findings are used.

## Exact convention interface

Let b_ab count arrows a→b minus arrows b→a. The actual primary X-mutation is X'_a=X_a(1+X_k^(-sgn b_ak))^(-b_ak), a≠k, with X'_k=X_k^(-1). Setting y=X^(-1) gives:

- b_ak≥0: y'_a=y_a(1+y_k)^(b_ak).
- b_ak<0: y'_a=y_a y_k^(-b_ak)(1+y_k)^(b_ak).
- y'_k=y_k^(-1).

Thus the source and native formula use the same PRE-mutation matrix. No implicit transpose or arrow reversal has been inserted. The actual GKS reduced-word edge rule includes Cartan adjacency for inclined arrows; the abbreviated KS printed definition omits that condition. The note explicitly uses the former standard convention. The removed negative-index vertices belong to the graded, higher-dimensional seed; the KS reduced-cell specialization sets those and the weight coordinates to 1. The reviewed cone has 12 coordinates, not 16.

For a monomial y^e, this substitution gives new y_k exponent -e_k+Σ_(b_ak<0)(-b_ak)e_a and binomial power Σ_(a≠k)b_ak e_a. This derives the native pullback implementation directly. Clearing a common (1+y_k)^D and exact division over Z is an identity procedure, not a numerical approximation. Exactness is checked separately in each fixed-other-exponent group; a nonzero remainder is rejected. Optimized frozen rows are nonpositive toward mutable vertices, precisely the actual primary definition. All four selected final rows are -e_10.

## Canonical reconstruction and coefficient attack

The complete exact pullbacks from optimized inverse frozen coordinates have 14,5,2,1 terms for frozen positions 7,9,11,12. They equal the factored expressions in the original source and my source-first support expansion. Distinct frozen markers prevent cancellation or collisions among summands. Inside the 14-term group the source-first partition 2+3+6+3 separates all terms. Every coefficient is one. The only squared y_6 terms are rows 21 and 22. Their X exponents are -2 at the same mutable position, so reciprocal notation preserves the asserted absolute-exponent violation. No arbitrary basis change or user-created Laurent polynomial is substituted for the canonical reduced-word coordinates.

The exact verification does not establish canonicality merely by finding a pleasing polynomial. It starts from the primary-defined optimized frozen inverse coordinates, follows valid mutable seed mutations, checks optimization, and performs the complete algebraic pullbacks. Well-definedness of that canonical potential is the cited standard cluster-potential input. Rational evaluations at three positive points per route check implementation consistency only; they do not prove a general rational identity or path independence.

## Full-dimensional, pointed cone and genuine facets

Write C={z in R^12 : a_i·z≥0 for every i=1,…,22}. The switch z=-t converts canonical-X tropical inequalities exactly; no nonnegative-orthant assumption is imposed on z. Let u=e_7+e_9+e_11+e_12. Each a_i has exactly one frozen marker of coefficient one, hence a_i·u=1. A finite open neighborhood of u lies in C, proving full dimension 12.

Each displayed z_j satisfies a_j·z_j=-1 and a_i·z_j≥0 for i≠j. Thus dropping inequality j admits z_j and changes C. This proves irredundancy directly, without invoking the disputed later proof. More strongly p_j=z_j+u satisfies a_j·p_j=0 and a_i·p_j≥1 for every i≠j. For sufficiently small h in a_j-perp, all other inequalities stay strict. Therefore C∩a_j-perp contains a relatively open 11-dimensional neighborhood and is a facet. No special assumption about extreme rays or finite sampled cone points is required. The source-first explicit row-difference basis proves rank 12 and hence lineality is zero: if z and -z lie in C, all a_i·z vanish and z=0.

The ordinary native run checks both complete separating tables (2×22×22=968 integer products) and all relative-interior inequalities, plus 11 tangent ranks for every face. These are exhaustive finite certificates for these explicitly listed rows. They do not constitute a search over all type-D words, an automated proof of arbitrary cluster theorems, or a proof-assistant build.

## Coordinate-invariance attack

The chamber map exponent matrix is K with K_kk=K_(k,k+)=1 and intermediate entries the D4 Cartan entries; all other entries zero. It is upper triangular with diagonal one, so det K=1. The source-first hand list of every a_i K is preserved in OWN_DERIVATIONS.md and agrees with the native exact output. In particular:

- a_21 K=e_2+e_4+e_6-e_7.
- a_22 K=e_1.

Every transformed coordinate exponent has absolute value at most one. An integral invertible monomial map preserves the support's distinctness, coefficients and facet/irredundancy structure, while the coordinate exponent bound changes. This is precisely why the historical canonical-W assertion is refuted while the later varsigma-coordinate converse is not. Coefficient-one criteria are not refuted. No contradiction of the conclusion of KS Theorem 2, or replacement proof for its general argument, has been established or claimed.

## Earlier data comparison, by actual bodies

The entire actual pinned Case 267 was read after INITIAL. Its leaf-1 support, in its displayed progression, matches transformed row indices 22,21,20,19,16,18,12,15,17,10,14,9,8,7. Its other groups are row 1 (central root), rows 13,11,6,5,4 (leaf 3), and rows 3,2 (leaf 4). This accounts for every one of the 22 transformed monomials, with no missing or extra support. Thus the older primary computation is substantial prior input, not just a coincidentally matching reduced word. This comparison establishes finite pinned content, not a date of public availability, correctness of the old generating program, or current priority. No old program was run.

## Attempted failures and boundary conclusions

Attacks at the shortest optimized routes, frozen-frozen arrow deletion, inverse-coordinate signs, merged support, doubled exponents, lineality and the distinction between redundant and nonfacet inequalities did not expose a candidate mathematical defect. The finite word is reduced and gives -I on the D4 root space; the independent Cartesian calculation precedes the native Cartan-based check. The proposed example lies inside the historical simply-laced/simply-connected complex setup. Changing to the later chamber coordinates removes the exponent violation rather than yielding a second counterexample. That is an exclusion in the original claim, not a narrowed repair introduced by this review.
