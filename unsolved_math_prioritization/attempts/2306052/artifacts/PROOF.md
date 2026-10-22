# Bounded perturbations of disk surjections: partial results for Rubel's Problem 6.52

## Status and exact target

Let D = {z in C: |z| < 1}. The question is whether, for every holomorphic f:D→C with f(D)=C, there exists a bounded univalent (that is, injective holomorphic) g:D→C such that (f+g)(D)=C.

This note does **not** resolve that universal question. It proves several sufficient criteria, an obstruction to one possible omitted-value selection argument, and an exact affine-perturbation classification for a particular rational surjection. The original problem remains unresolved in this investigation. No novelty, priority, or comprehensive present-day open-status claim is made.

The question is attributed to L. A. Rubel in Hayman–Lingham, *Research Problems in Function Theory*, Problem 6.52, printed p. 137 / PDF leaf 138, [arXiv:1809.07200v2](https://arxiv.org/abs/1809.07200v2). Its 2018 update says that no progress had been reported to the authors. This historical report is not a proof of current openness.

Write H∞(D) for bounded holomorphic functions, with supremum norm ||h||∞. The standard argument principle and Rouché theorem are used explicitly: if A,B are holomorphic near a closed disk or a compactly contained Jordan domain and |B|<|A| on its boundary, A and A+B have the same number of zeros inside, counted with multiplicity. This follows because A+sB never vanishes on the boundary for 0≤s≤1, so its integer winding number around 0 is constant.

## 1. Compact sets of target values persist

**Lemma 1.** Suppose f is a nonconstant holomorphic function on D and K is a compact subset of f(D). There is δ_K>0 such that

K ⊂ (f+h)(D) whenever h∈H∞(D) and ||h||∞<δ_K.

**Proof.** For each w∈K, choose z_w∈D with f(z_w)=w. Since f−w is not identically zero, choose a small closed disk B_w compactly contained in D, centered at z_w, on whose boundary f−w is nonzero. Set m_w=min_{∂B_w}|f−w|>0. For any v with |v−w|<m_w/3 and any h with ||h||∞<m_w/3,

|h(z)+w−v| < 2m_w/3 < |f(z)−w| on ∂B_w.

Rouché gives at least one zero of f+h−v in B_w. The disks in the target plane B(w,m_w/3), for w∈K, cover K. Select a finite subcover, and take δ_K to be the minimum of the corresponding m_w/3. This is positive and works for all v∈K. □

In particular, for every integer N≥1 and every surjective f, some nonzero affine g_N(z)=a_N z preserves all target values |w|≤N. Such a g_N is bounded and univalent. The statement does not give one coefficient a that works for every N: the numbers δ_{|w|≤N} may have no positive common lower bound. No assertion that this degeneration actually occurs for every or any specific surjective f is needed for identifying the gap.

## 2. Two genuine uniform sufficient conditions

### 2.1 Contour condition

**Proposition 2.** Suppose f(D)=C. Suppose there is ε>0 such that, for every w∈C, a Jordan domain Ω_w compactly contained in D satisfies both:

1. f−w has a zero in Ω_w;
2. min_{∂Ω_w}|f−w|≥ε.

Then f+h is surjective for every h∈H∞(D) with ||h||∞<ε.

**Proof.** Apply Rouché to f−w and h on ∂Ω_w, for each w. □

This is a sufficient condition, not a characterization and not a consequence established here of mere surjectivity.

**Corollary 2.1 (large boundary-modulus contours).** Suppose there are Jordan domains Ω_j compactly contained in D, all containing a fixed z_*, such that min_{∂Ω_j}|f|→∞. Then f+h is onto C for every bounded holomorphic h, without any smallness requirement.

**Proof.** Fix w and put M=||h||∞. Choose j so that min_{∂Ω_j}|f|>max{|f(z_*)|,M+|w|}. On this contour, Rouché first compares f with f−f(z_*). The latter vanishes at z_*, so f has at least one zero inside. A second application compares f with f+h−w, showing that it also has a zero. Since w was arbitrary, the conclusion follows. □

In particular the corollary applies when min_{|z|=r_j}|f(z)|→∞ along r_j↑1 (the usual strong-annularity condition). It gives Rubel's requested perturbation for this class by taking any nonzero g(z)=az. Section 5 gives a surjective rational f for which this radial minimum instead tends to 0 along the point z=−r, so this sufficient condition does not cover all surjections.

### 2.2 Uniform inverse-branch condition

**Proposition 3.** Suppose some r>0 has this property: for every w∈C there is a holomorphic φ_w:B(w,r)→D such that f(φ_w(ξ))=ξ. Then f+h is surjective for all h∈H∞(D) with ||h||∞<r.

**Proof.** Choose r' with ||h||∞<r'<r. On |ξ−w|=r', the function h(φ_w(ξ)) has modulus less than r'. Rouché applied in the ξ-plane shows that

ξ−w+h(φ_w(ξ))

has a zero ξ_0 in B(w,r'). Then z=φ_w(ξ_0) satisfies f(z)+h(z)=w. □

This condition is stronger than necessary. For the example in Section 5, the target −1/4 has a unique preimage in D, and that preimage is critical. Consequently no holomorphic local right inverse exists there: differentiating f(φ(ξ))=ξ would give f'(φ(−1/4))φ'(−1/4)=1, an impossibility. Nevertheless that example has a uniform bounded-perturbation neighborhood of surjectivity. Thus the inverse-branch route cannot be substituted for the weaker contour argument without losing cases.

## 3. The affine-parameter route and its exact logical gap

For a fixed surjective f, set

A_N = {a∈C: {w:|w|≤N} ⊂ (f(z)+az)(D)}.

**Proposition 4.** Every A_N is open and contains a neighborhood of 0. The set of coefficients for which f+az is onto C is precisely ⋂_{N≥1}A_N.

**Proof.** The neighborhood of 0 follows from Lemma 1. If a_0∈A_N, apply that lemma to F(z)=f(z)+a_0z and K={|w|≤N}. This F is nonconstant because a constant F would make f bounded affine on D, contradicting f(D)=C. The perturbation (a−a_0)z has norm |a−a_0|, so all sufficiently nearby a belong to A_N. The intersection assertion is the definition of surjectivity, using the exhaustion of C by these closed disks. □

This Gδ description does not prove the intersection contains a nonzero point. Open neighborhoods of 0 can have intersection {0}; the abstract example A_N=B(0,1/N) demonstrates precisely why a category argument needs additional density or non-collapse input. This example is a logical warning, not an assertion that those exact A_N arise from a holomorphic f.

The same compact-target proof yields an informative necessary behavior of omitted values: if a_n→0 and w_n∉(f+a_nz)(D), then |w_n|→∞. Otherwise a bounded subsequence lies in some fixed compact target disk, contradicting Lemma 1 for sufficiently small a_n.

## 4. A holomorphic omitted-value selection cannot fill a punctured parameter disk

**Proposition 5.** Let f:D→C be holomorphic and surjective, and let u∈H∞(D). There are no r>0 and holomorphic b:{a:0<|a|<r}→C such that

f(z)+a u(z) ≠ b(a) for every z∈D and every 0<|a|<r.

**Proof.** If ||u||∞=0, this contradicts f(D)=C immediately. Otherwise Lemma 1 shows that |b(a)|→∞ as a→0: for any R, all sufficiently small a satisfy {|w|≤R}⊂(f+a u)(D), so |b(a)|>R.

Thus 1/b is holomorphic and tends to 0 in a sufficiently small punctured disk. It extends holomorphically across 0 with value 0. Its zero there has finite positive order m, since it is not identically zero. Therefore b has a pole of order m at 0.

Fix ρ∈(0,r) small enough for this description, put B=max_{|a|=ρ}|b(a)| and M=||u||∞, and choose z_0∈D with |f(z_0)|>B+ρM. Such z_0 exists by surjectivity. On |a|=ρ,

|b(a)−a u(z_0)| < |f(z_0)|.

The meromorphic function b(a)−a u(z_0)−f(z_0) has winding number 0 around 0 on that circle, since its boundary values can be deformed to the nonzero constant −f(z_0) without hitting 0. It has exactly m poles, counting order, inside, all at 0. By the argument principle it therefore has exactly m zeros inside. None is at 0, so at least one parameter a satisfies b(a)=f(z_0)+a u(z_0), contradicting the assumed omission. □

The statement is conditional on a holomorphic selection existing. It does not show that a non-surjective family f+az admits such a selection, and it does not rule out disconnected, non-holomorphic, or otherwise nonselectable omitted-value sets.

For comparison, Eremenko's *Exceptional values in holomorphic families of entire functions*, [arXiv:math/0503750](https://arxiv.org/abs/math/0503750), Theorem 2, proves holomorphicity away from a discrete set for exceptional values in a family whose functions are entire in the source variable. Its proof uses Picard's uniqueness of an omitted finite value and an entire-source pluripolarity theorem. Our source is D, so those hypotheses are absent. That theorem is not applied here. In fact a bounded disk function may omit an open set of values, making the uniqueness step unavailable. No valid selection theorem bridging this gap was established.

## 5. An exact rational test family

Define

T(z)=(1+z)/(1−z),   P(t)=t²−t,
f_0(z)=P(T(z))=2z(1+z)/(1−z)².

The Cayley transform T maps D bijectively onto H={t:Re t>0}, with inverse z=(t−1)/(t+1). Indeed Re T(z)=(1−|z|²)/|1−z|²>0, and |t−1|<|t+1| exactly when Re t>0.

For any w, the two roots of t²−t−w have sum 1. At least one therefore has real part at least 1/2 and lies in H. Hence f_0(D)=C.

### 5.1 Complete classification of affine perturbations

**Theorem 6.** For a=α+iβ∈C, set D_a=(2α−1)³−27β². Then

- if D_a<0, (f_0+az)(D)=C;
- if D_a≥0, (f_0+az)(D)=C\{−conj(a)}.

In particular every nonzero |a|<1/2 gives an admissible bounded univalent perturbation. The coefficient a=1/2 fails: f_0(z)+z/2 omits −1/2. The radius 1/2 is the largest open disk centered at 0 consisting entirely of surjective affine coefficients (the boundary point 1/2 is already bad).

**Proof.** In H the equation f_0(z)+az=w becomes

t²−t+a(t−1)/(t+1)=w.

Multiplying by t+1 introduces no change to solutions in H and gives

Q_{a,w}(t)=t³+(a−w−1)t−(a+w)=0.             (1)

The three roots of this monic cubic, counted with multiplicity, sum to zero. If none has positive real part, each real part is nonpositive and their sum is zero, so all roots are purely imaginary. Conversely, three purely imaginary roots give no solution in H.

If all roots are iy_1,iy_2,iy_3 with y_j real, their sum is zero and the coefficient of t is

−Σ_{i<j}y_i y_j = (y_1²+y_2²+y_3²)/2,

which is real and nonnegative. The constant coefficient is purely imaginary. Comparing with (1) gives Im w=β and Re w=−α, so the only possible omitted value is w=−conj(a). At that target put p=2α−1; then

Q_{a,−conj(a)}(iy)=−i[y³−py+2β].           (2)

Thus the target is omitted exactly when the real cubic q(y)=y³−py+2β has all three roots real, counted with multiplicity.

If p<0, q'(y)=3y²−p>0, so q has only one real root and the other two are nonreal. If p=0, all three are real exactly when β=0. If p>0, put s=√(p/3). The local maximum is q(−s)=2(s³+β) and the local minimum is q(s)=2(β−s³). The cubic has three real roots, allowing repeated roots, exactly when q(−s)≥0 and q(s)≤0, equivalently |β|≤s³. This is equivalent to p³≥27β². The same inequality also captures p=0,β=0 and excludes p<0. This proves the two range assertions, including the uniqueness of the omitted target.

If |a|<1/2 then α<1/2, so D_a<0. At a=1/2 it is zero. A direct factorization also checks that exceptional endpoint:

f_0(z)+z/2+1/2 = (1+z)³/[2(1−z)²],

which has no zero in D. Finally az is injective for a≠0 and ||az||∞=|a|. □

No square-root branch is chosen in the cubic proof, and the repeated-root boundary is included. The boundary cusp has rational parametrization a=(1+3s²)/2+i s³ with real s; equation (2) then has q(y)=(y−s)²(y+2s). This is a useful exact check, not a replacement for the proof.

### 5.2 Stability against arbitrary bounded perturbations

**Theorem 7.** If h∈H∞(D) and ||h||∞<3/64, then (f_0+h)(D)=C.

**Proof.** Transfer h to H by h̃(t)=h((t−1)/(t+1)); its norm is the same. Fix w. Choose either square root s of w+1/4, so

P(t)−w=(t−1/2)²−s².

If |s|≤1/4, use the circle |t−1/2|=3/8. Its closed disk lies in H, it contains both zeros, and on the boundary

|P(t)−w|≥(3/8)²−(1/4)²=5/64.

If |s|>1/4, select a root r∈{1/2+s,1/2−s} with Re r≥1/2, and use |t−r|=1/8. This closed disk lies in H. The other root r' has |r−r'|=2|s|>1/2, so the chosen disk contains exactly one root and

|P(t)−w|=|t−r||t−r'|≥(1/8)(2|s|−1/8)>3/64

on its boundary. In either case Rouché with h̃ gives at least one zero of P+h̃−w in H. This works for every w. □

The constant 3/64 is a convenient certificate, not an optimal norm-stability threshold.

### 5.3 What the example separates

The example is not strongly annular: f_0(−r)=−2r(1−r)/(1+r)²→0 as r↑1, hence min_{|z|=r}|f_0(z)| cannot tend to infinity. Also the unique preimage of −1/4 corresponds to t=1/2, or z=−1/3, and is critical because P'(1/2)=0 and T' is nonzero. So the inverse-branch condition in Proposition 3 fails even locally at this target.

Nevertheless Theorem 7 proves bounded-norm stability. Conversely Theorem 6 exhibits a bounded univalent perturbation that destroys surjectivity. Thus neither strong annularity nor unbranched covering behavior is forced by surjectivity, and the quantifier “there exists g” cannot be replaced by “every bounded univalent g.”

## 6. Remaining gap

For an arbitrary holomorphic disk surjection f, nothing here proves a positive uniform contour margin, a uniform inverse radius, a nonzero element of ⋂A_N, or a holomorphic selection from the omitted-value sets of f+az. The explicit classification in Section 5 relies on a special cubic with vanishing t² coefficient and does not extend to a general f by an argument supplied here.

A complete answer would require either a construction of one bounded injective g for every allowed f, with all complex target values verified, or one allowed f for which every bounded injective g fails. Neither has been established.

The verification script checks the exact polynomial identities, rational boundary parametrizations, and numerical constants used above. It does not certify the analytic proofs, universal quantifiers, or the original problem. This is an AI-assisted, unrefereed partial research note.
