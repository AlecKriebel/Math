# Turn 5: a uniform hyperbolic bound with no parameter split

2026-10-02. Fifth substantive author turn for Problem 2305038. This is a new proof simplification of the derivative half, not merely source retrieval or repackaging. It replaces turn 2's small/large-a split and angular monotonicity argument by a single nonnegative polynomial identity valid on the entire parameter rectangle.

Both corrected sharp comparisons have complete proposed proofs, with the four-turn version independently audited. The original qualitative goal of a substantially simpler proof relative to the historical literature remains unverified; this fifth-turn version requires a fresh scoped audit. No novelty claim is made. Original-target disposition after five turns: exhausted, unresolved as a historical/qualitative simplification claim.

## 1. A stronger disk-map estimate

Let φ map the unit disk holomorphically into itself, φ(0)=0, and a=φ′(0)∈[0,1]. At r=ρ=3−√8, set

w=φ(r),
δ=|(r−w)/(1−rw)|,
Q=(1−r²)|φ′(r)|/(1−|w|²).

We prove the uniform estimate

Q ≤ (1−2δ)/(1+2δ).                                   (1)

The numerator on the right is positive. The proof below also shows δ≤1/4. Rotating the input and output simultaneously permits any evaluation point of modulus ρ.

This estimate is sufficient for the derivative comparison because the ordinary sharp Koebe derivative theorem, applied after a disk automorphism taking 0 to r, gives

|(F∘φ)′(r)/F′(r)|
 ≤ Q ((1+δ)/(1−δ))²                                  (2)

for every F∈S. Moreover

(1−δ)²(1+2δ)−(1−2δ)(1+δ)²=4δ³≥0,

so (1)–(2) imply the desired ratio is at most one.

## 2. The exact Schur-jet reduction

At a=1 Schwarz's lemma gives φ(z)=z, so (1) is equality. For a<1 write

φ(z)=z(a+ω(z))/(1+aω(z)),   ω(0)=0, |ω(z)|≤|z|.

Put c=ω(r), u=|c|², x=Re c, S=1−r² and B=1−a². Applying Schwarz–Pick to ω(z)/z gives

|ω′(r)−c/r|≤(r²−u)/(rS).

Differentiating φ, taking the maximum on this disk, and using the formula for |w|, gives the upper bound

Q≤Q*=[S|a+2c+ac²|+B(r²−u)]/
        [|1+ac|²−r²|a+c|²].                          (3)

No assumption that φ or ω is univalent is used.

Let

k=(1−u)/(1+u), k0=S/(1+r²)=2√2/3,
v=2x/(1+u), D=1+av,
b=(B/2)(k/k0−1), T=√(D²−Bk²).

Then k0≤k≤1, |v|≤√(1−k²)≤1/3, and direct identities turn (3) into

Q*=(T+b)/(D+b),                                      (4)
δ²=(1−a)²(1−v)/[32(D+b)+(1−a)²(1−v)].               (5)

For (4), the two identities are

|a+2c+ac²|²=(1+u+2ax)²−B(1−u)²,
|1+ac|²−r²|a+c|²=S(1+u+2ax)+B(r²−u).

Also (r²−u)/[S(1+u)]=(k/k0−1)/2. For (5), use δ²/(1−δ²)=|r−w|²/[S(1−|w|²)] and r²/S²=1/32.

## 3. Removing the interior defect

Fix a,v and increase k from k0 to its given value. This stays within the feasible region: its endpoint satisfies |v|≤√(1−k²), hence so does every smaller k. In particular T is real throughout.

Where B>0 and T>0, differentiation of (4) gives

dQ*/dk
 = B/(D+b)² [(D−T)/(2k0)−k(D+b)/T]
 ≤ B/(D+b)² [1/√2−2√2/3] <0,

because 0<T≤D≤4/3, b≥0 and k≥k0. Continuity covers a possible T=0 endpoint, while B=0 gives Q*=1. Formula (5) makes δ nonincreasing in k as well.

The function (1−2δ)/(1+2δ) is decreasing in δ. Thus (1) follows at every interior jet if it holds at the boundary k=k0, with the same a,v: Q* only decreases and the required upper bound only increases as k increases. This is an explicit monotonicity proof, not an assumed maximum principle for a jet functional.

## 4. One uniform boundary certificate

At k=k0 define

K=8(1−a²)/(9D²),  M=(1−a)²(1−v),  W=32D+M.

Equations (4)–(5) become

Q*=√(1−K),   δ²=M/W.

Here 0≤K≤1: D≥1−a/3 and
(1−a/3)²−8(1−a²)/9=(a−1/3)²≥0.
Also D≥2/3 and M≤4/3, so δ²≤1/16.

An elementary rational majorant for the square root is

√(1−K)≤(4−3K)/(4−K),   0≤K≤1,

because both sides are nonnegative and

(4−3K)²−(1−K)(4−K)²=K³.

Consequently

(1−Q*)/(1+Q*) ≥ K/(4−2K).                            (6)

It remains to prove K/(4−2K)≥2δ. All quantities and denominators are nonnegative, and

K²−4δ²(4−2K)²
 =64(1−a)² P(a,v)/(81D⁴W),

where

P(a,v)=(1+a)²W−(1−v)[9D²−4(1−a²)]².                 (7)

The following identity certifies P≥0 on the entire rectangle 0≤a≤1, −1/3≤v≤1/3. Put t=(3v+1)/2, so 0≤t≤1. Then

P(a,(2t−1)/3)
 = Σ_{i=0}^4 binom(4,i) a^i(1−a)^(4−i) q_i(t),        (8)

with

q_0(t)=16t,
q_1(t)=(2/3)(30t²−43t+50),
q_2(t)=(4/9)(46t³−48t²−35t+110),
q_3(t)=(16/3)(3t⁴+t³−9t²−t+12),
q_4(t)=(32/3)(1−t)(1+t)(6+t−2t²−t³).

Every coefficient polynomial is nonnegative by inspection. The brackets in q_1,q_2,q_3 are respectively at least 7, 27 and 2, using 0≤t≤1 and discarding positive terms. The last bracket is at least 3. All Bernstein weights in (8) are nonnegative.

Thus (7) is nonnegative, so (6) gives
(1−Q*)/(1+Q*)≥2δ,
which rearranges to (1) on the boundary. Section 3 proves it for every permitted map.

The certificate has five explicit one-variable coefficient polynomials. There is no numerical subdivision, grid, solver, angular optimization, or a-dependent case split.

## 5. The derivative theorem and sharpness

Equation (2) follows, for example, by applying derivative distortion to

H(ζ)=[F((ζ+r)/(1+rζ))−F(r)]/[S F′(r)]∈S

at ξ=(w−r)/(1−rw), using 1−|ξ|²=S(1−|w|²)/|1−rw|². This is the same ordinary Koebe-transform calculation recorded explicitly in turn 1.

By (1) and the identity after (2), |g′(z)|≤|F′(z)| on |z|=ρ. Since g′/F′ is holomorphic, the maximum-modulus principle gives the full closed disk.

For sharpness take F(z)=z/(1+z)² and φ_a(z)=z(a+z)/(1+az). At a=1, the positive real derivative ratio is one, and its a derivative is

(r²−6r+1)/(1+r)².

For any ρ<r<1, this is negative; taking a<1 sufficiently close to one gives a ratio greater than one. Thus the classical radius is sharp.

## 6. The modulus proof and a review clarification

The modulus proof in TURN_4.md remains valid with one wording correction identified by the independent review. For a fixed purely imaginary Z and fixed q, the minimum absolute argument of Z/q need not equal γ. Every argument does have absolute value at least γ, which is precisely the inequality used. MODULUS_PROOF_REVIEWED.md preserves the argument with that sentence corrected; the original frozen TURN_4.md and its manifest remain unchanged.

Its proof uses a Grunsky-derived odd-function bound, a phase lower bound from two elementary geometric factorizations, and a strict scalar separation at R=(3−√5)/2. No new modulus theorem or historical priority is claimed.

## 7. Honest final scope and the qualitative goal

This fifth turn supplies a genuinely shorter derivative proof relative to the four-turn artifact: the earlier split at a=1/6 and the angular derivative certificate are completely absent. It also proves the stronger disk-map estimate (1), which was not a statement of that earlier argument.

The corrected sharp inequalities are therefore established by complete explicit mathematical arguments, subject to review of this new certificate. But the source asks for simpler proofs of historically known inequalities. Duren's 1977 survey already describes the odd-function backbone for modulus, and Campbell/Barnard–Pearce supply the derivative two-point/Schur setup. Their use is fully credited.

The original Shah papers and complete Campbell III proof have not been compared. Neither mathematical correctness nor shorter length relative to our previous draft establishes historical novelty or substantial simplification relative to all known proofs. After five substantive turns, the original qualitative research target is recorded as exhausted/unresolved, with reviewed or review-pending alternative proofs retained as precisely scoped output. This status must not be converted to a claim that the sharp inequalities themselves were new or previously unproved.

Completion estimate: 90% toward a checked alternative-proof package, not toward a certified historical-priority or universal simplicity claim. No sixth substantive search is included in this checkpoint.

