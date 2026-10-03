# Attempt 3: exclude a symmetric spatial family and search unrestricted four-orbits

2026-10-03 08:16 UTC. Substantive author turn 3/5. Outcome: exact exclusion for a two-parameter family; numerical search does not settle general tetrahedral orbits. Estimated full-target progress: 25% (subjective).

## Symmetric skew quadrilaterals

Consider the ordered vertices

    x0=(a,b,a), x1=(a,-b,-a),
    x2=(-a,b,-a), x3=(-a,-b,a),       a,b>0.

All four sides have length 2q, where q=sqrt(a^2+b^2). The perimeter is L=8q. Direct normalization of adjacent edge differences gives reflection normals with the same sign pattern and positive-coordinate representative

    n0=(a,2b,a)/r,       r=sqrt(2a^2+4b^2).

Assume for contradiction that L<=2 and the finite completion test is feasible. Then q<=1/4 and r<=1/2. Write the antipodal points in the same sign pattern with coordinate magnitudes

    A=a(1/r-1),       B=b(2/r-1).

Among their pairwise squared distances are 8A^2 and 4(A^2+B^2). Feasibility requires A^2<=1/8 and A^2+B^2<=1/4.

Set z=b^2/q^2, so 0<z<1 and r=q sqrt(2+2z). If z<=1/8, then

    A^2=(1-z)(1/sqrt(2+2z)-q)^2
        >= (7/8)(2/3-1/4)^2
        = 175/1152 > 1/8,

already a contradiction. All factors are positive, so these monotone estimates are legitimate.

If z>=1/8, lowering q only increases A and B. At q=1/4 their squared sum is

    F(z)=(1+3z)/(2+2z) - sqrt(1+z)/(2 sqrt(2)) + 1/16.

For 0<=z<=1,

    F'(z)=1/(1+z)^2 - 1/(4 sqrt(2) sqrt(1+z)) > 0,

because (1+z)^(3/2)<=2 sqrt(2)<4 sqrt(2). Thus

    A^2+B^2 >= F(z) >= F(1/8) = 43/144 > 1/4,

again a contradiction. Consequently every realizable member of this genuinely spatial family has **L>2**. The argument uses only the YY constraints, so adding XX and XY cannot defeat it. The planar limits b=0 or a=0 were already covered by Attempt 1 (or direct degeneracy analysis).

This family has equal consecutive side lengths and equal opposite diagonals. A general tetrahedral four-orbit need not have these symmetries. No symmetrization theorem transferring general candidates to this family is asserted.

## Exploratory unrestricted optimization

`search_four.py` uses six coordinates for four points in R^3 modulo rigid motions, constructs all eight antipodal points, and minimizes perimeter subject to their pairwise squared distances being at most 1. It also imposes small positive cutoffs to avoid numerical zero edges, zero reflection differences and a degenerate coordinate gauge. These cutoffs exclude limiting configurations; no compactness conclusion is drawn from them.

With seed 30002659, 80 SLSQP starts produced 76 diagnostics satisfying the recorded constraints within 1e-7. The smallest reported perimeter was approximately 2.353276790915, with negative slack about -1.5e-12. It is therefore not an exact feasible certificate. The best coordinates approximate the above symmetric family and their four antipodes approximate a regular tetrahedron. Four runs failed the diagnostic feasibility threshold. Every run, including failures, is preserved in `search_four_results.json`.

No length<=2 candidate emerged. This is neither a global optimization certificate nor evidence excluding all tetrahedral configurations, much less all dimensions. The strongest rigorous result of this attempt is the displayed family exclusion. The finite test from Attempt 2 remains exact; this particular optimizer is only a heuristic exploration of it.
