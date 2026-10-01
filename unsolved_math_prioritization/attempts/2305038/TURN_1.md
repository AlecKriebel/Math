# Turn 1: elementary endpoint proofs and an exact derivative reduction

Status: scoped partial, original intended two-proof simplification unresolved. One substantive author turn. Classical Schwarz–Pick/Koebe inputs and the Campbell–Barnard–Pearce mechanism are credited; no novelty is asserted.

Use F∈S and g=F∘φ with φ(0)=0 and a=φ'(0)∈[0,1]. The standard sharp Koebe estimates are
r/(1+r)^2≤|F(z)|≤r/(1−r)^2 and (1−r)/(1+r)^3≤|F'(z)|≤(1+r)/(1−r)^3 for |z|=r.

## 1. The zero-initial-derivative case, with exact sharp constants

Suppose a=0. Two applications of Schwarz's lemma give φ(z)=z^2h(z), |h|≤1. Consequently |φ(z)|≤r^2 and
|g(z)|/|F(z)|≤[r^2/(1−r^2)^2]/[r/(1+r)^2]=r/(1−r)^2.
Thus the first desired inequality holds up to R=(3−sqrt(5))/2. It is already sharp within a=0: take F(z)=z/(1−z)^2, φ(z)=z^2 and z=−r. This is the classical growth-theorem observation and sharpness construction, not a new resolution of the a>0 case.

For the derivative, write t=|h(z)|. Schwarz–Pick gives
|φ'(z)|≤2rt+r^2(1−t^2)/(1−r^2)≤2r
whenever r≤(sqrt(5)−1)/2, because the expression is increasing in 0≤t≤1 there. Hence
|g'(z)|/|F'(z)|≤2r(1+r^2)/(1−r)^4.
Its exact first crossing of 1 is the unique eta∈(0,1) satisfying
eta+1/eta=3+sqrt(5),
or eta=(3+sqrt(5)−sqrt(10+6sqrt(5)))/2.
Equivalently eta is the smallest positive root of r^4−6r^3+6r^2−6r+1. The expression on the right is strictly increasing, eta lies in (19/100,1/5), and is below the range where the preceding bound is valid. The same F, φ, z=−r attain this bound, so eta is the sharp derivative radius for the subclass a=0. In particular eta>3−sqrt(8); the derivative obstruction for the full problem is not at a=0. This is consistent with the classical Campbell bound at a=0 and is not presented as a historically new constant.

## 2. Exact Schur-jet region at an evaluation point

By simultaneous variable rotation of F and φ we may evaluate at z=r>0 without changing a or membership of S. For a<1, Schwarz–Pick at zero gives
φ(z)=z(a+ω(z))/(1+aω(z)), with ω(0)=0 and |ω(z)|≤|z|.
Fix c=ω(r), |c|≤r. Applying Schwarz–Pick to ω(z)/z gives the exact closed derivative disk
ω'(r) ∈ c/r + [(r^2−|c|^2)/(r(1−r^2))] closed(D).
This disk is exact: for |c|<r choose a disk automorphism or a constant interpolation for ω(z)/z with its value c/r at r; its derivative can have any modulus up to the Schwarz–Pick radius and any phase. For |c|=r, ω(z)=(c/r)z is forced and the disk is a singleton.

It follows by differentiation that, for w=φ(r)=r(a+c)/(1+ac), the exact maximum of |φ'(r)| is
J(a,c,r)=[|a+2c+ac^2|+(1−a^2)(r^2−|c|^2)/(1−r^2)]/|1+ac|^2.
Every denominator is nonzero since a≤1 and |c|≤r<1. At a=1 Schwarz's lemma forces φ(z)=z, giving equality in both comparisons directly.

## 3. Sharp two-point derivative comparison and equivalence

Set δ=|(w−r)/(1−rw)|<1. Normalize the Koebe transform
H(ζ)=[F((ζ+r)/(1+rζ))−F(r)]/[(1−r^2)F'(r)]∈S.
At ξ=(w−r)/(1−rw), the sharp derivative distortion theorem gives
|F'(w)/F'(r)|≤(1−r^2)^2/|1−rw|^2 · (1+δ)/(1−δ)^3 =: K(r,w).
For every fixed r,w this upper bound is attainable: take the Koebe rotation H whose extremal ray contains ξ, reverse the disk automorphism, and then normalize the resulting univalent function at zero. That final affine normalization changes neither derivative ratio. If ξ=0 the ratio is exactly 1.

The F and φ choices are independent once a,c,r,w are fixed. Thus the maximum over all permitted F and all Schur jets with those parameters is EXACTLY K(r,w)J(a,c,r), not merely an empirical or one-sided bound. A proof of the full derivative theorem is therefore equivalent to
K(rho, rho(a+c)/(1+ac)) J(a,c,rho)≤1
for 0≤a<1 and |c|≤rho, rho=3−sqrt(8).
A boundary-circle proof suffices for every smaller radius because g'/F' is holomorphic and F' never vanishes; use the maximum-modulus principle on the closed disk of radius rho. Conversely any strict failure of the displayed finite-parameter inequality yields an actual F and φ counterexample by the attainability constructions above.

This rederives, for S, the classical two-point-distortion/Schur reduction underlying Campbell and Barnard–Pearce. The remaining real inequality contains coupled square roots and is not proved here. Merely replacing the original analytic question with this inequality is not a completed simplification.

## 4. Exact source-radius sharpness for general a

For the derivative, take F(z)=z/(1+z)^2 and φ_a(z)=z(a+z)/(1+az), 0≤a<1. At real r the ratio H(a,r)=g_a'(r)/F'(r) is rational and positive. It equals 1 at a=1, and direct differentiation yields
∂_a H(1,r)=(r^2−6r+1)/(1+r)^2.
For rho<r<1, this derivative is negative, so H(a,r)>1 for a<1 sufficiently near 1. This is the classical sharpness family. Together with the a=0 modulus example it proves that neither requested radius can be improved if the respective lower-bound proofs are supplied. Sharpness does not establish those lower bounds.

## Remaining gap and next route

The unrestricted 0<a<1 modulus lower bound and a concise proof of the coupled derivative inequality remain. The original false real-only formulation is separately corrected in SOURCE_SCOPE.md. Next turn should attack the coupled finite-parameter inequality or a genuinely geometric replacement, rather than count this exact reduction as a solution. Completion estimate: 15% toward a jointly satisfactory simplification; this is a subjective research estimate, not a probability or theorem status.
