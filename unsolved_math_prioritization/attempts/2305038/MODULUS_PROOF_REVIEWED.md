# Reviewed modulus proof: non-substantive wording clarification

This copy incorporates the independent review correction to the argument-distance sentence. The original TURN_4.md is preserved unchanged in this package. No mathematical inequality or proof mechanism is altered.

# Turn 4: a Grunsky phase-separation proof of the modulus comparison

Status: full proposed proof of the modulus half. Together with TURN_1.md–TURN_3.md this is a complete candidate for both corrected inequalities of Problem 5.38, found within substantive author turn 4/5. Independent verification and the historical simplicity assessment are pending. No new sharp inequality or priority claim is made.

## Theorem

Let F be holomorphic and injective in the unit disk, with F(0)=0 and F′(0)=1. Let g=F∘φ, where φ is a holomorphic disk self-map, φ(0)=0, and φ′(0)∈[0,1]. Then

|g(z)|≤|F(z)| for |z|≤R=(3−√5)/2.

The radius R is sharp. The derivative half and its sharpness are proved in TURN_1.md–TURN_3.md.

Write L(t)=log((1+t)/(1−t)) for 0≤t<1.

## 1. A standard Grunsky consequence for odd functions

If h is odd, normalized, holomorphic and injective on the unit disk, then

|log{[(h(u)−h(v))/(h(u)+h(v))] [(u+v)/(u−v)]}|
 ≤ sqrt(L(|u|²)L(|v|²)).                               (1)

The logarithm is the analytic branch which vanishes when v=0; the apparent singularities at u=±v are removable. In the use below u≠±v and u,v≠0.

Here is a derivation, included to fix the constant and branch. Put G(ζ)=1/h(1/ζ), an odd normalized univalent exterior-disk function. Define its Grunsky coefficients by

log[(G(ζ)−G(η))/(ζ−η)]=−Σ_{m,n≥1} b_mn ζ^(−m)η^(−n).

The classical Grunsky inequality says, for finite complex vectors q,

|Σ b_mn q_m q_n|≤Σ |q_n|²/n.                           (2)

The normalization and precise form (2) were checked in P. L. Duren and M. M. Schiffer, “Grunsky inequalities for univalent functions with prescribed Hayman index,” Pacific J. Math. 131 (1988), printed p.105, including the page image:
https://msp.org/pjm/1988/131-1/pjm-v131-n1-p06-p.pdf .
Only its recalled classical inequality is used, not its stronger Hayman-index theorem.

Because b_mn=b_nm, polarization of (2), after normalizing two vectors separately to norm one in Σ|q_n|²/n, gives

|Σ b_mn p_m q_n|
 ≤ sqrt[(Σ|p_m|²/m)(Σ|q_n|²/n)].

Indeed 4B(p,q)=B(p+q,p+q)−B(p−q,p−q), and the parallelogram identity proves the unit-norm case.

Oddness makes b_mn=0 when m+n is odd. Subtracting the kernel at (u,−v) from that at (u,v), after the substitution ζ=1/u, η=1/v, yields the analytic logarithm in (1) as

−2Σ_{m,n odd} b_mn u^m v^n.

Apply the bilinear estimate to the odd-index vectors and pass from finite truncations to the limit. Since

Σ_{n odd} t^n/n = (1/2)L(t),

the bound is exactly (1). The series converge for |u|,|v|<1. This is the classical odd-function two-point mechanism associated with Lebedev; it is not claimed as a new inequality.

## 2. The value-region constraint

Fix 0<r<R and rotate simultaneously so that the evaluation point is r. Let w=φ(r), s=|w|, X=Re w and S=1−r². Schwarz's lemma gives s≤r.

For a=φ′(0)<1, write φ(r)=r(a+c)/(1+ac), |c|≤r. The inequality |(w/r−a)/(1−aw/r)|≤r is equivalent to

(s²−r⁴)−2arS X+a²r²(1−s²)≤0.                         (3)

If s>r², this implies a>0 and X>0. Nonpositivity of this quadratic for some a implies its discriminant is nonnegative, so

X≥X0:=sqrt[(s²−r⁴)(1−s²)]/S.                         (4)

Equivalently,

X≥0,  |Im w|≤(r²−s²)/S.                              (5)

The a=1 case forces w=r. Only the containment (4)–(5) is needed; no sufficiency claim about this value region is required. This is the familiar Rogosinski value-region geometry.

At a fixed argument θ with Re w≥0, condition (5) reads

|sin θ|≤(r²/s−s)/S.

Its right side increases as s decreases. Therefore the radial segment from any such w with r²<s<r down to modulus r² stays in the region (4)–(5).

## 3. An elementary phase estimate

Suppose r²<s<r and w satisfies (4). Set u=√r>0 and choose v=√w with Re v>0. Then

q=(u−v)/(u+v)

has positive real part. Define its angular distance from the imaginary axis by

γ=π/2−|arg q|.

If w is positive real, γ=π/2 and the estimates below are immediate. Otherwise,

tan²γ=(r−s)²/[2r(s−X)]
 ≥ S²(s+X0)/[2r(r+s)²].                              (6)

For the equality on the right after replacing X by X0, use

s²−X0²=(r²−s²)²/S².

We now prove

2r²(s+X0)≥s(r+s)².                                   (7)

First X0≥(s−r²)/(1−r). Squaring this nonnegative comparison and cancelling s−r² reduces it to

(s+r²)(1−s²)−(s−r²)(1+r)²
=(r−s)(r³+r²s+2r²+rs+2r+s²)≥0.

Next put y=s/r∈[r,1]. The lower bound (s−r²)/(1−r) is at least s[(r+s)²/(2r²)−1], because, after multiplying by positive factors, the latter comparison becomes

2(y−r)−(1−r)y[(1+y)²−2]
=(1−y)[(1−r)y²+3(1−r)y−2r]≥0.

The bracket increases in y≥0 and at y=r equals r(1−2r−r²)>0, since r<R<√2−1. This proves (7).

Combining (6)–(7), followed by concavity of arctan on [0,∞), gives the useful estimate

γ≥arctan[(S/(2r))√(s/r)]
 ≥√(s/r) arctan[S/(2r)].                              (8)

The two displayed positive factorizations are the elementary geometric part of this proof.

## 4. Phase separation rules out equal moduli

For F∈S, its square-root transform

h(ζ)=ζ sqrt(F(ζ²)/ζ²)

is odd, normalized and univalent on the unit disk. The analytic square root exists since F(z)/z has no zeros. To check injectivity: h(ζ1)=h(ζ2) implies F(ζ1²)=F(ζ2²), hence ζ1=±ζ2; oddness and the unique zero at zero then give ζ1=ζ2.

Suppose for contradiction that r²<s<r, (4) holds, and |F(w)|=|F(r)|. Then |h(v)|=|h(u)|, so

Z=(h(u)−h(v))/(h(u)+h(v))

is nonzero and purely imaginary. Its denominator and numerator cannot vanish because h is injective and u≠±v. Every argument of Z/q has absolute value at least γ; for a fixed sign of the purely imaginary Z, the minimum can be larger than γ. Consequently the analytic logarithm appearing in (1), whatever integer multiple of 2π its imaginary part contains, has modulus at least γ.

On the other hand, (1) gives

γ≤sqrt(L(r)L(s))≤√(s/r)L(r),                          (9)

because L(t)/t=2Σ_{n≥0}t^(2n)/(2n+1) is increasing.

But (8) contradicts (9). Indeed arctan[(1−r²)/(2r)] is decreasing and L(r) is increasing in r, and at R one has

(1−R²)/(2R)=√5/2,
(1+R)/(1−R)=√5,
arctan(√5/2) > (1/2)log 5.                            (10)

For an entirely rational check of the strict separation in (10), √5/2>11/10 and π>31/10 imply

arctan(√5/2)
 >31/40+1/21−1/(3·21³)>81/100,

using arctan x≥x−x³/3 for x≥0. Meanwhile
Σ_{n=0}^7 (81/50)^n/n!>5 proves (1/2)log5<81/100.
These loose rational bounds suffice; no floating-point comparison is part of the proof.

Thus equality |F(w)|=|F(r)| is impossible in the outer region r²<s<r.

## 5. Completing the modulus theorem and sharpness

For |w|≤r², ordinary Koebe growth estimates give

|F(w)|/|F(r)|
 ≤ [r²/(1−r²)²]/[r/(1+r)²]
 =r/(1−r)²<1,

because r<R. If some allowed outer point had |F(w)|>|F(r)|, the radial segment described after (5), starting at modulus r², would by continuity contain an outer point with equal moduli, contrary to section 4. The only allowed point with s=r is w=r, where equality is harmless. Therefore |F(φ(r))|≤|F(r)| for every 0<r<R.

Simultaneous rotation proves the inequality on every circle of radius r<R. Continuity of F and φ extends it to the closed disk |z|≤R, including z=0.

For sharpness take F(z)=z/(1−z)² and φ(z)=z². At z=−r,

|F(φ(−r))|/|F(−r)|=r/(1−r)²>1

whenever r>R. The normalization a=0 is permitted.

## Scope, comparison, and source limitations

This proof retains the classical square-root/Grunsky–Lebedev mechanism rather than claiming a new analytic tool. Its proposed simplification is the explicit phase-separation argument: an equality obstruction, two positive geometric factorizations, and one strict scalar comparison replace a detailed optimization of the two-point bound.

P. Duren's 1977 survey “Subordination,” Lecture Notes in Mathematics 599, pp.22–29, especially pp.25–27, sketches Shah's use of the odd-function inequality and records the request for a more conceptual proof. The bibliographic identity and official chapter reference were verified at https://doi.org/10.1007/BFb0096821 . Its text was inspected through an indexed copy at https://www.scribd.com/document/614333951/Lecture-Notes-in-Mathematics-599-Lars-v-Ahlfors-Auth-James-D-Buckholtz-Teddy-J-Suffridge-Eds-Complex-Analysis-Proceedings-of-the-Confe . The OCR of its displayed Lebedev formula is incomplete; the proof here does not rely on that OCR, because section 1 derives the needed inequality from the separately verified Grunsky theorem.

The original Shah papers and full Campbell III were not recovered. A claim that this is historically new, or objectively simpler than every prior proof, is therefore not justified. The claim ready for independent checking is narrower and complete: these artifacts give proposed short checkable proofs of both known sharp inequalities under the corrected nonnegative derivative normalization. Whether this satisfies the source's qualitative request is a separate assessment.

The literal real-only source formulation remains false, as shown in SOURCE_SCOPE.md. Correcting that omission is not itself the intended contribution.

