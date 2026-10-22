# Independent audit: zero-entropy two-atom sorting

## Verdict

The restricted exact-algorithm theorem is valid. For every integer n≥1, either initial staggered partition phase, and arbitrary fractions in [0,1], alternating exact local updates sort globally in at most n partition updates. In the source convention, each partition update takes time 1/n, so the universal stabilization time is t=1. This is not a solution of the general continuum-limit optimality question, nor a theorem for arbitrary sequences with n ε_n→0.

## Setting and local minimizer

Take source points x_i=(i−1/2)/n, i=1,…,n, each of mass 1/n; two distinct real target points a<b; target upper-atom mass p∈[0,1]; cost |x−y|²; and ε_n=0 exactly. Write u_i=n π({x_i}×{b})∈[0,1], with total M=np. Each paired block preserves s=u_i+u_{i+1}. Its cost, as a function of the left upper-target fraction u_i, has strictly positive slope 2(b−a)(x_{i+1}−x_i)/n. Therefore its unique local optimum is u_i=max(0,s−1), u_{i+1}=min(1,s). A singleton is unchanged. Distinct target points and distinct source positions ensure uniqueness even when fractions or the prescribed target mass are nonintegral. At p=0 or 1 the coupling is already unique and unchanged.

Use staggered pair partitions (1,2),(3,4),… and (2,3),(4,5),…, leaving all unmatched endpoints singleton. This definition works for odd and even n; the paper itself restricts n to even for convenience. Both starting phases obey the result.

## Complete sorting proof

Set S_i=Σ_{h≤i}u_h, with S_0=0 and S_n=M. The unique globally sorted profile has

S_i*=max(0,M−n+i),  u_i*=S_i*−S_{i−1}*.

Every admissible prefix satisfies S_i≥S_i* and S_i≤min(i,M). A pair update at edge i replaces S_i by max(S_{i−1},S_{i+1}−1), leaving the other prefixes unchanged. The active edges alternate parity. The profile S* is fixed by this recursion.

For n≥2, fix i∈{1,…,n−1} at time n. Its last active update is at time ℓ=n or n−1. Repeatedly expand the max recursion. Since neighboring edges were active in the preceding half-step, every unabsorbed expansion moves spatial index by ±1 and time backward by 1. A path either hits an endpoint, where its contribution is bounded by S_i* because S* satisfies the same recursion, or reaches time zero after ℓ moves at an index j. If q moves were to the right, then q=(ℓ+j−i)/2, and its contribution is S_j^0−q.

Let r=n−i. For every M∈[0,n],

min(j,M)−max(0,M−r) ≤ min(j,r).

Consequently the excess of an initial-data path above S_i* is bounded by

min(j,r)−(ℓ+j−i)/2 = (n−ℓ−|j−r|)/2.

If ℓ=n this is nonpositive. If ℓ=n−1, the walk parity gives j≡i+n−1 (mod 2), whereas r=n−i, so j and r have opposite parity and |j−r|≥1. This also makes the bound nonpositive. Thus S_i^n≤S_i*. Admissibility supplies the reverse inequality. All prefixes equal S*, and the coupling is globally optimal. The case n=1 is immediate. Subsequent updates leave it fixed.

## Continuum claim and its exact scope

The source defines physical time t=k/n, not k/(2n): an A+B cycle takes 2/n. Thus the discrete couplings at floor(nt) are the unique discrete global optima for every t≥1. As n→∞ they converge weakly to the unique increasing coupling from Lebesgue measure on [0,1] to (1−p)δ_a+pδ_b: send x<1−p to a and x>1−p to b. The point x=1−p has zero source measure. A possible split midpoint atom has mass ≤1/n and does not affect the limit. The conclusion also works for p_n→p.

The paper's composite-cell reconstruction moves source location by at most O(1/n), so it has the same weak limit. Hence any actual subsequential continuum trajectory is optimal after time 1 in the sense of its chosen convergence topology. Weak spacetime convergence alone identifies only an almost-everywhere-in-time equivalence class. To claim pointwise optimality for every t≥1, use the direct convergence of the exact optimal discrete tails or the continuous representative of the limiting trajectory. No formal PDE stationarity or uniqueness of a PDE solution is used.

No extra regularity/BV assumption on initial fractions is required for this tail theorem. Such assumptions may still be required to establish existence of a complete subsequential trajectory on [0,1]. The sorting theorem does not prove that earlier trajectories converge, nor identify their unique early-time limit.

## Excluded overclaims

- ε_n=0 cannot be replaced in this proof by n ε_n→0: positive entropy changes the exact update and prevents exact finite-grid sorting.
- A finite positive η local PDE or stationary condition does not establish selection by actual discrete iterates.
- This treats uniform one-dimensional midpoint source measures and two target atoms only. It does not establish a claim for arbitrary continuous within-cell source measures, general target measures, higher dimensions, or nonuniform cell masses.
- Pairing must be the two alternating nearest-neighbor staggered partitions; an arbitrary or repeatedly fixed partition does not satisfy the proof.

## Evidence and reproducibility

Source inspected: the published 2023 paper, Definition 1/setup items 2–6 and 11–12, and its time discretization paragraph. Public PDF URL and hash are in SOURCE_METADATA.json. It explicitly permits midpoint approximations, ε_n=0, singleton boundary blocks, and the scale Δt=1/n. No third-party source text is reproduced here.

Independent exact-integer enumeration script: check_zero_entropy.py. It enumerates binary states through n=13, half-unit fractional states through n=9, and quarter-unit fractional states through n=7, with both starting phases, testing exact global equality by step n. Results are in ZERO_CHECKS.txt. These checks supplement the proof rather than replacing it.
