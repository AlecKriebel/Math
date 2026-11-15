# Proof assessment of the original claim

This document uses the exact actual continuous input audited in DERIVATIONS.md; it is not a proposal to replace the target by an unchecked conditional theorem. The local proof below was already reconstructed before foreign/code exposure in PREEXPOSURE_PROOF.md. The foreign proof reconstruction was separately frozen before native code/opinions. The ordinary AI-review conclusion is that the original full chain has no identified substantial gap, subject to the explicit nonformal limits in REPORT.md.

Let p=3/2 and r>2. The actual annular input gives ||W_r(F,G)||_p≤C_r||F||_3||G||_3 for complex inputs and a pointwise supremum over all finite positive rational endpoint lists. It is not a fixed-list norm estimate. Endpoint continuity and a common countable truncation set make that definition legitimate. The full actual source proof and its support/heat/frequency/rough/completion mechanisms are assessed in DERIVATIONS.md.

For finite arrays A,B on Z² let h=1/8,q=1/16 and place their constant values in disjoint squares of half-side h. At u=i+a,v=j+b, |a|,|b|<q, moving windows with different integer indices cannot overlap: |k-l|≤2h+|a-b|≤3/8<1 would be required. Their common same-index offset is I=[-h-min(a,b),h-max(a,b)], length ℓ∈[1/8,1/4], with |s|≤3/16. The zero window is below1/2. For every signed nonzero k, |k+s| lies strictly between |k|-1/2 and |k|+1/2. Thus annulus(M+1/2,N+1/2) selects exactly M<|k|≤N, with its signed denominator intact.

K_k=∫_I(k+s)^(-1)ds=ℓ/k+δ_k and the exact reciprocal identity gives

    |δ_k|/ℓ ≤ (3/16)/(|k|(|k|-3/16)) ≤ 3/(13k²).

For each increasing integer endpoint list, shells are disjoint. Therefore the error increments' ℓr norm is at most the sum of the absolute coefficient contributions. After the supremum,

    V^r(E)/ℓ ≤ (3/13)Σ_(k≠0)|A(i+k,j)B(i,j+k)|/k²=:e(i,j).

Translation invariance, Hölder with3,3,3/2 and Minkowski give ||e||_p≤π²/13||A||_3||B||_3. The exact embedded sequence is ℓD_N+E_N. Every endpoint list maps to positive rational radii, so

    V^r(D)(i,j) ≤ 8W_r(F,G)(i+a,j+b)+e(i,j).

This holds on a full measure subset of each positive-area phase square; countably many lattice indices and lists suffice for one exception set. Integrating over disjoint output squares of area1/64, and using ||F||_3||G||_3=(1/16)^(2/3)||A||_3||B||_3, proves

    ||V^r(D)||_(ℓp) ≤ [8·4^(2/3)C_r+π²/13]||A||_3||B||_3.

For infinite ℓ3 arrays, first fix a finite endpoint menu; support truncations eventually agree at each output site. Fatou then monotone exhaustion preserve the constant. No shrinking-width limit or null-phase evaluation is used.

Choose measurable finite representatives f,g. The null sets of changes, commutation/inverse failures if defined modulo null sets, and their preimages under all finite words in S,S^-1,T,T^-1 form a countable null union. Its complement is invariant and supports all orbit identities simultaneously. For a fixed finite cutoff M and L≥0, define A_x(i,j)=f(S^iT^j x)1_(Q_(L+M)), and B similarly. For (i,j)∈Q_L and N≤M,

    D_N(A_x,B_x)(i,j)=H_N(f,g)(S^iT^j x),

where T^nS^iT^j=S^iT^(j+n) is exactly the commutation use. Apply the lattice estimate to the finite maximum V_M, raise to p, restrict the output sum to Q_L and integrate. Invariance on the left and Cauchy–Schwarz on the right give

    |Q_L| ||V_M||_p^p ≤ D_r^p |Q_(L+M)| (||f||_3||g||_3)^p.

The right side is finite, establishing integrability. At fixed M let L→∞; the ratio tends to1. Only then let M→∞ by monotone convergence. This retains point-dependent endpoint menus. No ergodic theorem, freeness or topological model is required.

Set r=3 for convergence. If a scalar sequence with finite3-variation were non-Cauchy, choose indefinitely many ordered disjoint late pairs separated by one ε>0. A partition through J pairs would have variation at least εJ^(1/3), a contradiction. Hence H_N→H almost everywhere. Since H0=0, H*=sup_N|H_N|≤V^3 and H*∈Lp. The measurable tail sup_(N≥m)|H_N-H| tends to0 almost everywhere and is bounded by2H*. Dominated convergence gives its Lp norm tending to0, including ordinary norm convergence. Norm limits of the exact finite bilinear identities give a complex bilinear limit on L3 equivalence classes.

The failure alternatives were actually examined: maximal/dyadic bounds alone, fixed-partition norm bounds, null-set point evaluation, one-sided harmonic divergence, noncommuting orbit identities, signed-window reflection, zero/identity/periodic cases, fixed-M order of limits, supported Gram differentiations, complex phases, small-variance frequency cost, and square-integral rather than frequency-supremum summation. Each relevant actual mechanism is recorded in the immutable initial/results and primary reconstruction. Finite controls support these interfaces but do not replace universal arguments. No endpoint r=2 or broader action/exponent theorem is inferred.

Attribution correction: Demeter2006v1 Remark1.3 says 1/p+1/q<3/2, not2/3. Thus L3,L3 belongs to the older opposite-power convergence comparison. The target's arbitrary commuting variation conclusion remains a distinct statement. The immutable earlier note is preserved with the explicit correction in RECONCILIATION.md.
