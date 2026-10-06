# Audit of the affirmative answer to Function Theory Problem 7.28

## Attribution and conclusion

Guo and Xiao's [2026 preprint](https://arxiv.org/abs/2608.04540v1), Theorem 1.1 and Corollary 1.2, supplies the result. The following verification uses their primitive-to-mean-value route, with an explicit check of the harmonicity step. This is a reconstruction and audit of existing mathematics, with no novelty claim.

Write ∂=(∂x−i∂y)/2 and ∂̄=(∂x+i∂y)/2. For a continuous g define

J_g(a,r)=∮_{|z−a|=r} g(z) dz,

M_g(a,r)=(1/(2π))∫₀^{2π}g(a+r exp(it)) dt.

Every closed disk below is compactly contained in the relevant open set. This removes any ambiguity about evaluating the boundary values and permits a slightly larger disk when mollifying.

## Continuous local primitive

Fix any open V relatively compact in D. Choose W with closure(V) ⊂ W and closure(W) compact in D, and choose a smooth compactly supported cutoff χ in D equal to one near closure(W). Extend χf by zero. For K(z)=1/(π conjugate(z)), define F=K*(χf).

The kernel is locally integrable. On a compact set of evaluation points, translations of K are continuous in L¹ over a fixed bounded integration region. Multiplication by the bounded function χf therefore shows F is continuous. The distributional identity ∂K=δ₀ gives ∂F=χf, hence ∂F=f on W. The identity follows also by integrating by parts outside a disk of radius ε: the inner boundary contributes the angular average of a test function, which tends to its value at zero; the omitted disk term tends to zero by local integrability. No regularity of f beyond continuity is used.

## Circular identity under weak differentiation

For a smooth F, at z=a+s exp(it),

∂F=(exp(−it)/2)(∂sF−(i/s)∂tF),   dz=i s exp(it) dt.

Multiplication and integration give J_{∂F}(a,s)=iπs ∂s M_F(a,s); the angular derivative integrates to zero. Consequently

M_F(a,R)−F(a)=−(i/π)∫₀ᴿ J_f(a,s)/s ds.  (1)

This remains true for the continuous weak primitive. To see this without assuming a limit interchange, choose a slightly larger disk and smooth F and f with the same mollifier there. Their weak identity becomes a classical identity, and both approximations converge uniformly on the closed smaller disk. If f_ε is the smoothed f, then

|J_{f_ε}(a,s)−J_f(a,s)|/s ≤ 2π ||f_ε−f||∞

for 0<s≤R. Its integral is at most 2πR||f_ε−f||∞, which tends to zero. The left side of (1) also converges uniformly. Endpoint convergence poses no problem: subtraction of f(a) gives |J_f(a,s)|/s ≤ 2π sup_{|z−a|≤s}|f(z)−f(a)|, a bounded function tending to zero.

For each fixed a and each η>0, the hypothesis supplies δ(a,η)>0 such that |J_f(a,s)|≤ηs² for 0<s<δ(a,η). Equation (1) then gives

|M_F(a,R)−F(a)| ≤ ηR²/(2π)

when R is sufficiently small. Thus M_F(a,R)−F(a)=o(R²) at every a in V. No common δ over different centers has been used.

## Independent verification of the mean-value input

The needed classical assertion is also stated as Theorem 1.6 in [Kuznetsov's survey](https://arxiv.org/abs/1904.08312v2), for every dimension m≥2. Here is a direct planar verification.

Suppose real continuous u satisfies M_u(a,r)−u(a)=o(r²) at every center. Take any closed disk B(c,R) in its domain. Let h be the Poisson solution with boundary values u, continuous on the closed disk and harmonic inside, and put w=u−h. Then w is zero on the boundary and inherits the pointwise o(r²) condition.

For ε>0 set v(z)=w(z)+ε|z−c|². At any interior center a,

M_v(a,r)−v(a)=o(r²)+εr²>0

for all sufficiently small r. Such a center cannot be a local maximum of v. A global maximum exists on the compact disk, so it must occur on the boundary, where v=εR². Hence w(z)≤ε(R²−|z−c|²). Sending ε to zero proves w≤0. Repeating the argument for −w proves w≥0. Thus u=h on every such disk, proving harmonicity. The small radius is selected only at the hypothetical maximizing point; uniformity is unnecessary.

Apply this assertion to the real and imaginary parts of F. Both are harmonic on V, so F is smooth there and ∂̄∂F=ΔF/4=0. Therefore ∂F is holomorphic. The distributions f and ∂F agree, so these continuous functions agree pointwise. Because V was arbitrary, f is holomorphic on D. Exact local vanishing implies the limit hypothesis and gives the other alternative immediately.

## Sanity checks and exclusions

- F(z)=|z|² gives ∂F=conjugate(z), J_{∂F}(a,r)=2πi r² and M_F(a,r)−F(a)=r². Equation (1) has exactly that value and fixes both its sign and constant.
- The continuous function f(z)=conjugate(z) shows why an O(r²) bound cannot replace o(r²).
- An o(r²) assertion only almost everywhere is not the hypothesis proved here. Nor is an assertion only along center-dependent subsequences of radii.
- The proof does not require D to be simply connected, bounded, or to have a regular boundary. All primitives and Poisson comparisons are local.
- The potentially invalid step of moving pointwise normalized-circle limits through an integral over centers is never used.

The checks establish a complete, source-credited affirmative answer at the mathematical level. They do not establish journal publication or institutional acceptance of the preprint.
