# Author attempt 3: six explicit planes and a certified reconstruction radius

2026-10-03 UTC. Goal: make finite-model rigidity explicit and quantitative, then test whether it extends globally. Outcome: a proved six-parameter chart theorem; no global conclusion.

Let Sym₃ be the six-dimensional space of real symmetric 3×3 matrices, with Frobenius norm. Fix R>0 and define
ρ_A(u)=R+uᵀAu, u∈S².
This is the even harmonic band of degrees 0 and 2. Use the six unit plane normals
e₁,e₂,e₃,(e₁+e₂)/√2,(e₁+e₃)/√2,(e₂+e₃)/√2.
Let Φ(A) be the vector of the six corresponding section perimeters, in that order.

## Exact linear inverse
For q_A(u)=uᵀAu, averaging uuᵀ over the circle θ⊥ gives
Fq_A(θ)=π(tr A−θᵀAθ).
Let p_i and p_ij denote these six linearized values. Then
A_ii=(p_j+p_k−p_i)/(2π), {i,j,k}={1,2,3},
A_ij=(p_i+p_j)/(2π)−p_ij/π, i<j.
If max|p|≤δ, each diagonal entry has absolute value at most 3δ/(2π) and each off-diagonal entry at most 2δ/π. Hence
||A||_F ≤ C₀ ||DΦ(0)A||_∞, C₀=√123/(2π).
This is an explicit bound, not an optimized inverse norm.

## Uniform nonlinear estimate
For ||A||_F≤r<R, on each selected circle write a=R+q_A and b=q_A'. Then a≥R−r and |b|≤2r. For H∈Sym₃, |q_H|≤||H||_F and |q_H'|≤2||H||_F. The first variation before integration by parts is
DΦ_θ(A)H=∫[a q_H+b q_H']/sqrt(a²+b²) ds.
Using |a/sqrt(a²+b²)−1|≤b²/(2a²) and |b|/sqrt(a²+b²)≤|b|/a gives
||[DΦ(A)−DΦ(0)]H||_∞≤L(r)||H||_F,
L(r)=4πx²+8πx, x=r/(R−r).

Set r=R/100. Because √123<12,
C₀L(r)=2√123/99²+4√123/99 <24/9801+48/99=4776/9801<1/2.
For any A,B in the closed Frobenius ball of radius R/100, their segment stays in that ball, and the fundamental theorem of calculus implies
||Φ(A)−Φ(B)||_∞ ≥ (1/C₀−L(r))||A−B||_F
≥ π/√123 ||A−B||_F.
Thus six explicit planes determine every body in this entire chart ball, with the quantitative stability bound
||A−B||_F ≤ √123/π ||Φ(A)−Φ(B)||_∞.

The proof is uniform on the stated closed ball; it is not merely an unspecified inverse-function neighborhood. Positivity is automatic. The bodies are also strictly convex: Hess_{S²}q_A has operator norm at most 4||A||_F, and
ρ_A²I+2∇ρ_A⊗∇ρ_A−ρ_A Hessρ_A
is positive definite because ρ_A≥99R/100 and ||Hessρ_A||≤4R/100. Convexity is extra, not required by the target.

## Number of measurements
Six is minimal for continuous local injectivity on a nonempty open subset of this six-dimensional chart when measurements are real scalars. If a continuous injection U⊂R⁶→Rᵏ existed for k<6, composing with the standard inclusion Rᵏ→R⁶ would contradict invariance of domain, since its image would lie in a proper subspace and have empty interior. This is a dimension lower bound, independent of perimeter formulas; no lower bound is claimed for discontinuous encodings.

## Global route failure
Outside the small chart ball, the derivative-remainder estimate no longer stays below the linear inverse bound. It neither proves a collision nor excludes one. Moreover, finite measurements only determine a fixed finite-dimensional model, not arbitrary nearby radial functions. The next attempt tests that obstruction explicitly.

The underlying fixed-band inverse-function idea was already present in the imported UnsolvedMath report; the explicit six normals, inverse formulas, certified R/100 radius and constants are the present derivation. Historical novelty has not been established.
