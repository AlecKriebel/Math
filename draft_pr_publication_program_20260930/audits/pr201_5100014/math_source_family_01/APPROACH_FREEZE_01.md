# Independent source and area-identity approach freeze

Frozen 2026-10-16 05:40:17 UTC, before reading any candidate proof, review, or mathematical result. Workflow estimate: 8% (source contract obtained; no submitted mathematics inspected).

## Literal primary-source contract

Primary source inspected: Reznik, Garcia, Koiller, *Eighty New Invariants in the Elliptic Billiard*, arXiv:2004.12497v11 [math.DS], 29 October 2020; cached primary text only. Section 1 restricts EB to two confocal ellipses. Section 2 assumes a>b>0, and defines every polygon area as signed shoelace area (Equation 1). Figure 1 and Section 3.1 define the outer polygon by the tangent lines to the outer ellipse at the N-periodic bounce points. Section 3.4 defines its pedal by orthogonal feet from M onto those lines. Table 4 row k303,a says the product A' A'_m is invariant over the billiard family for N congruent to 2 modulo 4 and every fixed M. The row is experimentally observed and has '?' in the 2020 proof column. This historical '?' does not establish current openness.

Scope to verify: any nondegenerate periodic trajectory in this ellipse-caustic model, including star winding and reversal; determine whether conventional N means primitive or permits repetition, and what is actually needed. N=2 is outside nondegenerate nested-ellipse trajectories. The circle is outside a>b but can be checked as a limiting case. A hyperbolic caustic is outside the source. Degenerate caustics and infinite tangent intersections require explicit handling rather than silent inclusion. Signed area must be retained; no conclusion about ordinary union area follows automatically.

## Prospective independent derivation (not a conclusion)

Write a tangent line as n_i dot X=h_i with outward unit normal n_i and support h_i>0. Its foot from M is Q_i=M+r_i n_i, r_i=h_i-n_i dot M. With cyclic order and Delta_i the oriented turn from n_i to n_{i+1}, the pedal area is

 A'_m = (1/2) sum_i r_i r_{i+1} sin Delta_i.

For finite consecutive tangent intersections, the outer signed area can independently be computed as

 A' = sum_i [h_i h_{i+1} - (h_i^2+h_{i+1}^2) cos Delta_i/2]/sin Delta_i.

I will check these identities from shoelace/line intersection, not assume convexity. Expand the first as a quadratic in fixed M. For an even primitive orbit, central symmetry should cancel its linear term. The central proof burden is to establish that all remaining quadratic coefficients, after multiplication by A', are phase-independent for N=2 mod4. An admissible route is an explicit elliptic parametrization followed by a finite-sum identity proved independently, or an actual geometric area identity reducing these coefficients to independently established invariant products. Replacing this burden by another unproved invariant or by finite numerics is a blocked transfer, not a proof.

Adversarial checks: normal orientation; which pedal and which outer polygon; signed versus ordinary area; reference M fixed in the plane; dependence on winding, primitive period, repetition; zero product and zero denominators; a to b circular limit; caustic degeneration; consistency of all normalization constants. Numerical diagnostics will never be treated as proof or publication clearance.

All work remains in this family folder. No Git actions, outside messages, external writes, installations, or large downloads.
