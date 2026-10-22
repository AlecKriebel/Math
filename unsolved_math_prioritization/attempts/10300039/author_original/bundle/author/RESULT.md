# Asymptotic separation: five scoped routes

Problem 10300039 / AMR-102-0039; catalog rank 1007. Author checkpoint, 8 October 2026.

**Disposition: unsolved, five substantive mathematical approaches.** No counterexample satisfying the question's hypotheses, full proof, novelty, exhaustive literature-status, human-review, or proof-assistant claim is made. Source inspection and package construction are not counted as approaches. Independent review is pending.

## Target and conventions

Calegari's 2002 Question 10.1 asks whether two-sided branching of a taut foliation on a hyperbolic three-manifold forces a lifted leaf to leave a geodesic halfspace in each complementary component. The printed formulation does not itself say “closed.” The results below that use cocompactness or the cited dichotomy explicitly assume a closed manifold. They do not silently resolve a broader noncompact reading.

For a properly embedded plane L in H^3, let Lambda(L) be its accumulation set on the visual sphere. Its complementary components in H^3 are U_+ and U_-. Define Omega_+(L) to consist of sphere points with a neighborhood in the closed-ball compactification whose interior part lies entirely in U_+; define Omega_- similarly. Thus these are domains belonging to a specified side, not merely the two largest components of the boundary complement.

## Results proved here

1. A side contains a geodesic halfspace exactly when its Omega-domain is nonempty. A horosphere shows that a proper limit set alone does not imply this on both sides for arbitrary planes.
2. A compact leaf whose stabilizer has a proper limit set supplies a proper leaf limit set. If that stabilizer is quasifuchsian, its limit set is a Jordan curve. In the closed taut two-sided setting, Calegari's credited dichotomy gives asymptotic separation. No such compact leaf is supplied for an arbitrary foliation.
3. A leafwise continuous boundary extension with Hölder exponent greater than 1/2 has proper image, by an explicit covering estimate. This would close the target in the closed setting. The required quantitative regularity is not established.
4. For a proper flow-saturated plane made from uniformly quasigeodesic lines with a common endpoint p and continuous opposite-endpoint map, its limit set is {p} union the closure of those opposite endpoints. Under the stated orbit-space hypothesis that map is proper away from p. Neither statement prevents sphere filling.
5. Finite covers of the specified foliation and lifted ambient isotopies preserve the relevant data. Standard countable ordered product blow-ups of an R-covered foliation still have leaf space R. These operations cannot construct the requested two-sided counterexample from a fiber foliation.

Each proof and its remaining gap appears in APPROACH_01.md through APPROACH_05.md. The elementary arguments are credited as standard where appropriate; the combination is not claimed new.

## Exact remaining gap

In the closed case, the source-verified Calegari alternative is: either every lifted leaf has full visual-sphere limit set, or asymptotic separation occurs. The missing implication is exclusion of the first alternative under two-sided branching, without imposing compact-leaf, quasifuchsian, quantitative boundary-map, or special-flow assumptions. None of the five approaches proves that implication. No constructed object here is a negative instance of the original problem.

## Current primary-source checkpoint

Fenley's arXiv:2210.09238v2 (27 February 2026), p.85, item E, still formulates the full-sphere/R-covered question and discusses non-R-covered Anosov foliations as a test case. The publisher dates the related article 23 March 2026. This is dated primary evidence, not a worldwide current-openness certificate.

The AMS abstract of Fenley's 1998 local/global limit-set article appears stronger for quasigeodesic Anosov foliations than that 2026 question suggests. Its full original could not be retrieved in this investigation. This potentially relevant discrepancy is retained as an unresolved source lead; no claimed Anosov resolution is built on an abstract alone.

All computations are finite diagnostics or artifact integrity checks. They do not prove the geometric dependencies or the unresolved universal assertion.
