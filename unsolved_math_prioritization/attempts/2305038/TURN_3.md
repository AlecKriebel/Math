# Turn 3: removing the interior Schur-jet gap

Status: complete proposed short proof of the derivative comparison, still only one half of Problem 5.38. Total substantive author turns: 3/5. The general modulus comparison remains unresolved. No historical novelty claim; independent review pending. Completion estimate: 50% toward the intended joint simplification.

## The derivative theorem

For F∈S, g=F∘φ, φ(0)=0 and φ′(0)=a∈[0,1], one has |g′(z)|≤|F′(z)| on |z|≤ρ=3−√8. This radius is sharp.

The proof consists of the exact reduction in TURN_1.md, the boundary and small-a certificates in TURN_2.md, and the elementary defect-monotonicity lemma below. These dependencies are mathematical derivations included in this folder, not assertions of the desired conclusion. The sharpness family is reproduced below.

## Exact interior normalization

Evaluate at z=r=ρ. The a=1 case is the identity. Otherwise write φ(z)=z(a+ω(z))/(1+aω(z)), with ω(0)=0 and |ω(z)|≤|z|. Put c=ω(r), u=|c|²≤r², x=Re c, S=1−r² and B=1−a². Schwarz–Pick applied to ω(z)/z gives the exact derivative-disk bound

J=[|a+2c+ac²|+B(r²−u)/S]/|1+ac|².

The maximal possible hyperbolic derivative at these fixed data is

Q=[S|a+2c+ac²|+B(r²−u)]/[|1+ac|²−r²|a+c|²]. (1)

Let
k=(1−u)/(1+u), k0=(1−r²)/(1+r²)=2√2/3,
v=2x/(1+u), D=1+av, b=(B/2)(k/k0−1),
T=√(D²−Bk²).

Then k0≤k≤1 and |v|≤√(1−k²)≤1/3. The following two elementary identities prove that (1) becomes Q=(T+b)/(D+b):

|a+2c+ac²|²=(1+u+2ax)²−B(1−u)²,
|1+ac|²−r²|a+c|²=S(1+u+2ax)+B(r²−u).

Also (r²−u)/[S(1+u)]=(k/k0−1)/2. The denominator D+b is positive since D≥2/3.

The pseudohyperbolic displacement δ=|(r−φ(r))/(1−rφ(r))| satisfies

δ²=(1−a)²(1−v)/[32(D+b)+(1−a)²(1−v)].       (2)

This follows from δ²/(1−δ²)=|r−φ(r)|²/[S(1−|φ(r)|²)] and r²/S²=1/32. Equations (1)–(2) retain the complete interior derivative-disk contribution; it has not been discarded.

## Defect monotonicity

Fix a and v and increase k from k0 to its actual value. This path is feasible: |v|≤√(1−k²) at the final value implies the same at every smaller k. In particular T is real throughout, since the raw squared-modulus identity realizes it with u=(1−k)/(1+k) and x=v/(1+k).

For B>0 and T>0, differentiation gives

dQ/dk = B/(D+b)² × [(D−T)/(2k0)−k(D+b)/T].

Since 0<T≤D≤4/3, b≥0 and k≥k0, the bracket is at most

D/(2k0)−k ≤ 1/√2−2√2/3 = −√2/6 <0.

Thus Q is decreasing in k. If T vanishes at an endpoint, continuity gives the same nonincreasing comparison without differentiating at that endpoint. At B=0, Q=1 identically. Formula (2) shows δ is also nonincreasing in k, because b increases. Therefore

Q ((1+δ)/(1−δ))²

is nonincreasing in k. Every interior Schur jet is consequently dominated by a boundary jet with k=k0, equivalently |c|=r, and the same a,v. This is an explicit real-variable monotonicity argument; no maximum principle for the jet functional is assumed.

## Completing the derivative inequality

The sharp Koebe-transform distortion estimate gives

|g′(r)/F′(r)| ≤ Q ((1+δ)/(1−δ))².

For 0≤a≤1/6, TURN_2.md section 2 already proves the right side is at most one for arbitrary jets. For 1/6≤a<1, defect monotonicity reduces it to |c|=r. TURN_2.md section 3 proves the boundary expression is nondecreasing in v∈[−1/3,1/3], using the displayed polynomial's concavity and endpoint factorizations. At v=1/3 its value is

16(3a+1)/(a+3)³≤1,

with exact nonnegative gap numerator (1−a)²(a+11). The a=1 identity case has equality. Simultaneous rotation permits each point on |z|=ρ, and the maximum-modulus principle for holomorphic g′/F′ gives the whole disk.

For sharpness, take F(z)=z/(1+z)² and φ_a(z)=z(a+z)/(1+az). The positive real ratio H(a,r)=(F∘φ_a)′(r)/F′(r) has H(1,r)=1 and

∂H/∂a(1,r)=(r²−6r+1)/(1+r)².

For every ρ<r<1 this is negative. Thus H(a,r)>1 for a<1 sufficiently close to 1. This is the classical sharpness construction already checked exactly in turn 1.

## What this does and does not settle

The proposed derivative proof uses Schwarz–Pick, ordinary Koebe derivative distortion, one monotone defect parameter, one two-variable concavity certificate and two endpoint factorizations. It avoids an all-parameter multiregion numerical certificate. It is self-contained across TURN_1.md–TURN_3.md. Campbell and Barnard–Pearce remain the historical source of the two-point/Schur setup and angular mechanism. The full historical comparison is incomplete because Shah's original proof and Campbell III were not recovered.

The intended bundled task also asks for a simpler proof of |g(z)|≤|F(z)| on |z|≤(3−√5)/2. Only its a=0 case is proved here. Consequently this turn must not be promoted as a full candidate for Problem 5.38. The next author turn should use a materially different mechanism for that modulus half.
