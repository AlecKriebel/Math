# Turn 2: a hyperbolic proof on two substantial derivative subcases

Status: partial, not a full candidate for Problem 5.38. Total substantive author turns: 2/5. The full general modulus comparison and the interior Schur-jet derivative case for a>1/6 remain. Completion estimate: 25%, a subjective measure of progress toward a substantially simpler joint proof, not a probability.

## Scope and provenance

Use the corrected normalization and notation from SOURCE_SCOPE.md: F is normalized univalent on the unit disk, g=F∘φ, φ(0)=0, and a=φ′(0)∈[0,1]. Write ρ=3−√8. This turn proves |g′|≤|F′| on |z|≤ρ in either of the following cases:

1. 0≤a≤1/6, with no restriction on the disk self-map φ.
2. φ(z)=z(a+κz)/(1+aκz), with 0≤a≤1 and |κ|=1.

The second family is the degree-two Blaschke boundary of the exact Schur-jet region from turn 1. These are classical subcases of the known theorem. The present algebra is a proposed shorter presentation of the boundary calculation, not a claim that the inequalities or subcases are new.

The live working branch was checked at commit 2ef4976e3d15c535ec0e65c0db2a58fb72c4ea3d on 2026-10-02. Saved TURN_STATE.json recorded one substantive turn. The web page https://www.unsolvedmath.com/problems/2305038 remained inaccessible. The full original entry and update were rechecked in Hayman–Lingham, arXiv:1809.07200v2, PDF pages 99–100. The Barnard–Pearce author manuscript https://kjpearce100.github.io/mathwebsite/papers/bp1.pdf was recovered (190884 bytes, SHA-256 as in source_manifest.json), and pages 1–5 were read. Its summary of Campbell's general proof uses two a-regions and an angular polynomial; the polynomial below is the α=2 boundary specialization of that mechanism. The original Shah and full Campbell III proofs remain unavailable here, so no complete historical simplicity or priority comparison is claimed.

## 1. Hyperbolic form of the exact derivative reduction

By simultaneous rotation evaluate at z=r>0. Put w=φ(r),
δ=|(r−w)/(1−rw)|, and
Qφ(r)=(1−r²)|φ′(r)|/(1−|w|²).

The sharp two-point derivative distortion bound from turn 1 becomes

|g′(r)/F′(r)| ≤ Qφ(r) ((1+δ)/(1−δ))².                 (1)

Indeed 1−δ²=(1−r²)(1−|w|²)/|1−rw|², which converts the turn-1 Koebe-transform bound to (1). This uses only ordinary univalent derivative distortion.

All subsequent estimates are at r=ρ. A bound on this circle gives the entire closed disk by the maximum-modulus principle, since g′/F′ is holomorphic. At a=1, Schwarz's lemma forces φ(z)=z; that case is handled separately.

## 2. All self-maps with 0≤a≤1/6

Write ψ(z)=φ(z)/z, so ψ maps the disk to its closure and ψ(0)=a. For t=|ψ(r)|, Schwarz–Pick and the triangle inequality give

Qφ(r)
 ≤ ((1−r²)t+r(1−t²))/(1−r²t²)
 = (r+t)/(1+rt)
 ≤ (a(1+r²)+2r)/(1+r²+2ar).

The last step uses t≤(a+r)/(1+ar). At r=ρ, 1+r²=6r, so

Qφ(r)≤(3a+1)/(3+a).                                  (2)

For completeness, the maximum of δ over permitted values of ψ(r) occurs at c=−r in the Schur representation ψ(r)=(a+c)/(1+ac), |c|≤r. Here is a direct disk proof. For a<1, the function

u(c)=(r−w)/(1−rw)=r(1−a)(1−c)/(1−ar²+(a−r²)c)

is holomorphic on |c|≤r. Its maximum modulus is on |c|=r. On that circle its squared modulus is

r²(1−a)²(1+r²−2r cosθ) /
[(1−ar²)²+(a−r²)²r²+2(1−ar²)(a−r²)r cosθ].

This is decreasing in cosθ. To see the sign without assuming a−r²≥0, the negative derivative has the sign of

(1−ar²+(a−r²))(1−ar²+(a−r²)r²)
=(1+a)(1−r²)(1−r⁴)>0.

Thus c=−r maximizes δ. Substitution and (1+r)/(1−r)=√2 yield

(1+δ)/(1−δ) ≤ (3−a)/2.                               (3)

Equations (1)–(3) imply

|g′(r)/F′(r)| ≤ (3a+1)(3−a)²/[4(a+3)].

The difference between the denominator and numerator is

4(a+3)−(3a+1)(3−a)²=(1−a)(3a²−14a+3).

On 0≤a≤1/6, the quadratic is decreasing and is at least 3/4. The desired upper bound is therefore ≤1. This proof uses no information about an interior Schur jet beyond Schwarz–Pick. In fact the same calculation works up to a=(7−2√10)/3, but 1/6 is sufficient for the boundary calculation below.

## 3. All degree-two Blaschke boundary maps

Let φ(z)=z(a+κz)/(1+aκz), |κ|=1, and take a∈[1/6,1). Put κ=e^{iθ}, v=cosθ/3, and D=1+av. At r=ρ one has v∈[−1/3,1/3]. Direct calculation gives

Qφ(r)²=1−8(1−a²)/(9D²),                              (4)
δ²=(1−a)²(1−v)/[32D+(1−a)²(1−v)].                   (5)

For (4), before specializing r, the hyperbolic derivative equals
|a+2rκ+ar²κ²|/(1+r²+2ar cosθ), and the difference between squared denominator and squared numerator is (1−a²)(1−r²)². Equation (5) follows from δ²/(1−δ²)=|r−w|²/[(1−r²)(1−|w|²)].

Define H=Qφ(r)((1+δ)/(1−δ))², the right side of (1). We prove H is nondecreasing in v. Away from Qφ=0, differentiating log H shows that its v derivative is nonnegative if and only if

(4/9)a(1−a)(1−v)
 ≥ δ[D²−(8/9)(1−a²)].

Both sides are nonnegative: the bracket is D²Qφ². Squaring and using (5), followed by cancellation of (1−a)²(1−v), reduces this exactly to P(a,v)≥0, where

P=16a²(1−v)[32(1+av)+(1−a)²(1−v)]
  −[9(1+av)²−8(1−a²)]².

This two-variable polynomial has a short certificate. Its second v derivative is

P_vv=−4a²[243a²v²+64a²+486av+272a+163]<0,

because v≥−1/3 makes the bracket at least 64a²+110a+163>0. Consequently P is concave in v and is bounded below by the smaller endpoint value. These values factor as

P(a,1/3)=−(19a²−38a+3)(35a²+74a+3)/9,
P(a,−1/3)=−(43a²−98a+3)(11a²+62a+3)/9.

The first quadratic factor in each line is negative throughout a∈[1/6,1]: each is convex, and its two endpoint values are negative (respectively −101/36 and −16; −437/36 and −52). The other factors are positive. Hence P≥0.

The only possible zero of Qφ in this rectangle is at a=1/3, v=−1/3. Monotonicity extends there by continuity from the interior; no logarithm at zero is used. It follows that H≤H(a,1/3). At the positive endpoint, direct substitution gives

H(a,1/3)=16(3a+1)/(a+3)³≤1,

since

(a+3)³−16(3a+1)=(1−a)²(a+11)≥0.

Together with section 2 and the a=1 identity case, this proves the stated derivative comparison for every degree-two Blaschke boundary map.

## 4. An attractive but insufficient unrestricted bound

A separate geometric attempt kept only t=|ψ(r)|. The union of attainable ψ(r) values as a varies over [0,1] obeys, for t>r,

Re ψ(r) ≥ sqrt((t²−r²)(1−r²t²))/(1−r²).              (6)

This follows by minimizing over a the condition
(t²−r²)−2a(1−r²)Re ψ+a²(1−r²t²)≤0.
The discriminant proves (6); it is attained by a boundary Schur map. Combining (6) with Qφ≤(r+t)/(1+rt) does NOT prove the target inequality. If t=1−ε and r=ρ, the resulting upper bound has expansion

1+(3/4−1/√2)ε+O(ε²),

whose linear coefficient is positive. The route loses the angle between ψ and rψ′ in the triangle inequality. This failure is analytic, not just numerical. Repeating that scalar t-bound without preserving the angle cannot settle the target.

## Remaining gap and next mechanism

The full derivative reduction involves |c|<ρ and an extra attainable derivative-disk radius (ρ²−|c|²)(1−a²)/(1−ρ²). The boundary theorem does not remove that term. No maximum principle in the Schur value is asserted; its applicability is precisely unproved.

A useful next mechanism is to parameterize the interior jet by its defect d=ρ²−|c|² and try to show the boundary angular certificate persists after including the exact defect, rather than repeating the failed t-only relaxation. The general modulus inequality still needs an independent idea. No full proof of either bundled intended target, and no full candidate, is claimed.

