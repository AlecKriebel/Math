# Turn 1: reduce the arbitrary pedal point to two scalar invariants

2026-10-01 04:50–04:52 UTC. Status: partial; target unresolved.
Estimated completion toward full source target: 30%.

The exact target is k203,a in Table 3 of both arXiv:2004.12497v11 and the
published 2021 paper: A times the signed area of the pedal to the orbit's
sides, for every fixed point M, with primitive period N divisible by four.
The source uses a nondegenerate elliptical caustic and signed shoelace area.
No previous exact-target Alec attempt or PR was found in local all-ref logs,
remote branch/PR searches, or target-directory commit history. The imported
third-party report is not a prior author attempt. The related-target ledger
was inspected; its central-inversion and four-period groups do not list this
ID. Related k107/k108, k110, k114, and k120 work is credited, not transferred.

## Proved elementary reduction

For any centrally symmetric ordered even polygon P, choose unit vectors t_i
along its sides, and let Δ_i be their consecutive oriented direction changes.
Let q_i be the projection of O onto side i, and T_i=t_i t_i^T. The projection
of M onto this line is q_i+T_i M. Opposite sides satisfy q_(i+N/2)=-q_i and
T_(i+N/2)=T_i. In the signed shoelace formula, all terms linear in M cancel.
The remaining quadratic contribution is

  (1/2) sum_i det(T_i M,T_(i+1) M).

Writing M=ρ(cos φ,sin φ) and t_i=(cos α_i,sin α_i), each determinant equals
ρ² cos(φ−α_i) cos(φ−α_(i+1)) sin Δ_i. Product-to-sum decomposes this into
ρ² sin(2Δ_i)/4 plus
ρ²[sin(2φ−2α_i)−sin(2φ−2α_(i+1))]/4.
The latter terms telescope. Thus, for signed pedal area,

  A_M = A_0 + |M|²/8 sum_i sin(2Δ_i).

This argument uses ordered sides, not convexity, so crossing polygons are
included. Even primitive confocal elliptic billiard orbits are centrally
symmetric, as in Stachel's canonical parametrization.

Consequently the exact target is equivalent to constancy of both

  A A_0 and A sum_i sin(2Δ_i)

through the fixed billiard family. Necessity follows by evaluating M=0 and
one fixed unit M; sufficiency follows from the displayed formula. This
reduction does not itself prove either required scalar invariant.

## Exploratory evidence and next route

`explore.py` is newly authored numerical code using installed mpmath. It
uses Stachel's canonical coordinates with caustic semiaxes (2,1), checks
primitive periods 4,8,12,16,20 and their admissible odd turning numbers, and
computes signed projections/areas at three phases and three fixed M.
The target agrees to roughly 55 decimal digits. These are exploratory
checks, not a proof or validated interval certificate.

Further probes suggest A_0/A_inner and
(sum sin(2Δ_i))/A_inner are separately phase-independent for N divisible
by four. Since A A_inner has the credited Chavez-Caliz area-product
reduction used in campaign k110, proving these two proportionalities would
complete the target. Exact gap: prove these proportionalities for general
primitive N divisible by four; numerical agreement does not settle them.
