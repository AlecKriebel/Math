# Turn 5: the exact saturated-model obstruction and the failed ultraproduct route

Fifth and final author turn. The original finite-axiomatizability question remains unresolved. This turn identifies precisely what a separating-model construction must accomplish, and why the natural compactness/ultraproduct use of the known parameter hierarchy does not accomplish it.

Continue writing A_n=PWin^0_n and T_N=IOpen+A_N. In the following, all game lengths are ordinary finite integers in the metatheory, not elements whose length is encoded internally in a model.

## 1. Whole bad intervals, not individual bad responses

By the credited game recursion,

not A_m is equivalent over IOpen to

there exists a>0 such that for every u, [u≤a<2u -> not PWin^1_m(u)].

Thus a failure of the closed game sentence requires one first challenge whose *entire legal-response interval* is losing by that horizon. Producing a single losing parameter u, even one with arbitrarily large finite survival time, does not meet this condition.

**Exact criterion.** TEIP is not finitely axiomatizable over IOpen iff for every N there exist m>N and a countable recursively saturated model M of T_N containing a>0 for which all legal u≤a<2u satisfy not PWin^1_m(u).

The reverse direction directly contradicts each possible finite-fragment axiomatization from Turn1. For the forward direction, if no A_N axiomatizes TEIP, completeness gives a model of T_N+not A_m for some m>N. Downward Löwenheim–Skolem gives a countable elementary model including a witness a. It has a countable recursively saturated elementary extension, which preserves T_N, not A_m and the displayed interval failure.

For completeness, the last standard model-theoretic step can be obtained by repeatedly adjoining realizers of all recursive types over finite tuples that are finitely satisfiable in the current countable elementary model, using compactness with its elementary diagram, then taking a countable elementary chain union. A recursive type over parameters in the union appears at some stage; finite satisfiability in the union already holds at that stage by elementarity. Repeating the construction therefore realizes every such type. This is an existence construction, not an effective test for finite satisfiability.

The criterion only reduces the class of candidate countermodels; no such M has been constructed here for unbounded N.

## 2. What recursive saturation can and cannot supply

For a fixed a>0 in a recursively saturated model, consider the recursive type

Gamma_a(u)={u≤a<2u} ∪ {PWin^1_m(u):m≥1}.

If the model satisfies every A_m, this type is finitely satisfiable: any finite subset is controlled by the largest horizon in it. Recursive saturation supplies a single u in that interval surviving every finite horizon. Continuing with types over finite histories gives the credited expansion theorem for recursively saturated models of TEIP.

But T_N supplies only the initial finite portion. Applying recursive saturation to Gamma_a without proving *all* finite subsets satisfiable would assume the missing later axioms. Saturation cannot turn N-round survival into unlimited survival merely because the desired type is recursive.

Likewise, even a finite axiomatization of the reduct theory would not automatically provide a definable power predicate. Existence of external expansions and first-order definability are different properties. Turn4's automorphism obstruction therefore remains a barrier to one construction route, not a negative answer to the target.

## 3. The obvious ultraproduct of hard standard parameters stays inside TEIP

The primary paper's quantitative game analysis supplies positive integers u_j divisible by3 whose fixed-parameter survival lengths tend to infinity; this is the sequence used in its Theorem6.4. Credit that result. Form a nonprincipal ultraproduct of copies of the ordinary arithmetic structure, with distinguished element u=[u_j].

By Łoś's theorem, the underlying model satisfies Th(N), and hence every A_m and TEIP. For every fixed m, almost all u_j satisfy PWin^1_m(u_j), so the ultraproduct satisfies PWin^1_m(u), as well as3 dividing u. The element u is nonstandard: each particular standard non-power-of-two has finite losing complexity by the credited Lemma5.3, whereas u survives all standard finite horizons.

After passing to an appropriate recursively saturated elementary extension, the credited expansion construction can place u in an external power predicate, despite its divisibility by3. This recreates the source's noncanonical-predicate phenomenon; it does not produce a reduct violating TEIP.

More broadly, all models constructed in Turns2–3 already satisfy TEIP. Ultraproducts and elementary substructures/extensions of them still satisfy TEIP. Those operations alone cannot yield the required bad interval. A new construction must start with suitably long surviving finite fragments outside the full theory, not obtain a bad parameter by taking limits inside true arithmetic.

## 4. Final status and sharp remaining gap

The packet establishes exact finite-fragment reformulations, strictness of the natural oddless finite upper bound, explicit valuation-construction barriers, and a no-parameter-free-definable-predicate/strategy result in a credited TEIP model. None implies that arbitrary finite extra sentences cannot axiomatize TEIP.

The missing decisive step is either:

- exhibit one finite sentence or finite list whose consequences over IOpen are exactly all A_m, with a valid uniform proof, or
- construct the countable recursively saturated bad-interval models in Section1 for arbitrarily large N

The known strict fixed-parameter hierarchy, lack of definable expansions, and finite polynomial/game scans do neither. Five genuine author turns are exhausted. No sixth search or full-resolution claim is included.

`verify_turn5.py` checks the finite logical quantifier patterns used to distinguish one losing response from an entirely losing interval. Its toy response sets are explicitly not arithmetic structures or models of IOpen.
