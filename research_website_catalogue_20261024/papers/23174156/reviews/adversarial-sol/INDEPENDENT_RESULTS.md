# Independent source-first adversarial derivations — 23174156

Completed after reading the actual manuscript but BEFORE foreign mathematical bodies, native support/code/results/priority/README or current peer/root findings. The main calculation below is conditional on the exact full-category HT formula printed in the manuscript; no actual external-interface acceptance is claimed yet. No scientific computation was run.

## 1. Lie/lattice constants and the annihilator trap

Use α_j=e_j−e_(j+1), j=1,…,4 in the sum-zero subspace of R⁵. The Gram matrix is tridiagonal with diagonal 2 and adjacent entries −1. Its principal determinants satisfy d_n=2d_(n−1)−d_(n−2), d₀=1,d₁=2, hence det A₄=5. Therefore vol(Y)=√5 and vol(X)=1/√5 for the dual lattice X=Y*. The positive roots e_i−e_j, i<j, number 10 and give Weyl vector ρ=(2,1,0,−1,−2), with norm²10. The highest root has (ρ,θ)=4, giving h∨=5 in the simply laced normalization; dim SU(5)=25−1=24 and rank4.

The map a↦ν(a)=Σa_jα_j is an integral-basis isomorphism, so a∈{0,…,4}⁴ gives exactly all 625 classes in Y/5Y, without repeats. At r=10,p=5 the quadratic phase exp(πi·2q|ν|²) is 1, since ν has integral coordinates and integer norm² (indeed even). There is no floating cancellation or dependence on a sampled representative.

For any v∈Y, (ν(a),v)=Σa_j(v_j−v_(j+1)). Each finite geometric sum Σ_(a=0)^4 exp(2πia m/5) equals 5 if 5 divides m and 0 otherwise. Thus the entire inner sum is 625 precisely when all v_i have one common residue modulo 5, otherwise 0. This is v/5∈X, or v∈5X, not v∈5Y.

A concrete adversarial witness is v=(1,1,1,1,−4)=5ω₄. It lies in Y but not in 5Y. Its simple-root pairings are 0,0,0,5, so EVERY character value in the sum is 1 and the sum is 625. A checker selecting only coordinatewise multiples of 5 would incorrectly discard it. Equivalently the Cartan pairing is rank3 modulo 5; its radical has five elements. The order-five discriminant is material, not an ignorable generic-lattice convention.

## 2. Complete Weyl enumeration without a 120-row program

ρ exhausts all residues in F₅. If q is nonzero modulo 5, v=qρ−wρ has common residue c iff each component of wρ is the unique member of {2,1,0,−1,−2} congruent to qρ_i−c. For each c there is exactly one permutation; hence all five and only five survive, for EACH target q. This exhausts the entire Weyl sum and all 625 characters analytically.

For q=1 the five c=0,…,4 give respectively:

|c|wρ|sign|ρ·wρ|
|---:|---|---:|---:|
|0|(2,1,0,−1,−2)|+|10|
|1|(1,0,−1,−2,2)|+|0|
|2|(0,−1,−2,2,1)|+|−5|
|3|(−1,−2,2,1,0)|+|−5|
|4|(−2,2,1,0,−1)|+|0|

Every nontrivial translation of five residues is a 5-cycle, so its sign is +1. For q=2, multiplication by 2 fixes 0 and cycles 1→2→4→3→1, sign −1. Composing with any translation preserves that negative sign. The independently residue-ordered table is:

|c|wρ|sign|ρ·wρ|
|---:|---|---:|---:|
|0|(−1,2,0,−2,1)|−|0|
|1|(−2,1,−1,2,0)|−|−5|
|2|(2,0,−2,1,−1)|−|5|
|3|(1,−1,2,0,−2)|−|5|
|4|(0,−2,1,−1,2)|−|−5|

For example the c=2 row has qρ−wρ=(2,2,2,−3,−3) and dot product 4−1+2=5. The c=0 row has dot product −2+2+2−2=0. These independently check the nontrivial signs and exponents rather than copying a dot-product total.

Put z=exp(2πi/50), t=z⁵=exp(πi/5). The tables give B₁=t⁻²+2+2t and B₂=−(1+2t⁻¹+2t). If the WRONG v∈5Y selector were used, only c=0 would survive: the resulting B₁=t⁻² and B₂=−1 both have norm1. Thus that concrete error would falsely erase the discrepancy. Correct full-category/source conventions are indispensable.

## 3. Exact norms and the chosen embedding

Let u=√5>0 and x=t+t⁻¹=(1+u)/2. Then x²=x+1, t²+t⁻²=x²−2=(u−1)/2, and t³+t⁻³=x³−3x=−(u−1)/2. Expanding B₁ times its complex conjugate gives

|B₁|²=9+4(t+t⁻¹)+2(t²+t⁻²)+2(t³+t⁻³)=11+2u.

Also B₂=−(1+2x)=−(2+u), hence |B₂|²=(2+u)²=9+4u. Both are positive; their difference is2(u−1)>0. Complex conjugation t↦t⁻¹ fixes u. A different Galois embedding taking u to−u would change the stated real values/order and is NOT an orientation reversal. The specified unitary root/positive real embedding must therefore be checked against the actual primary conventions.

The cyclotomic relations are Φ₁₀(t)=t⁴−t³+t²−t+1=0 and Φ₅₀(z)=z²⁰−z¹⁵+z¹⁰−z⁵+1=Φ₁₀(z⁵). For ζ=exp(2πi/100), Φ₁₀₀(ζ)=ζ⁴⁰−ζ³⁰+ζ²⁰−ζ¹⁰+1, and z=ζ²,t=ζ¹⁰. This is a valid larger exact working field, not a claim of minimality.

## 4. Denominator, sign and vacuum normalization

At p=1 the inner quotient is trivial, and the Dedekind sum is zero. In the Weyl denominator the positive-root heights j=1,…,4 have multiplicities5−j. With exponent −2πiρ/10, each factor contributes −i times a positive 2sin term; ten factors give (−i)¹⁰=−1. Thus A=−P, not +P.

Write a=2sin18°=(u−1)/2, c=2sin54°=(u+1)/2, b=2sin36°, d=2sin72°. Then ac=1, bd=u, a²=(3−u)/2 and b²=(5−u)/2. Hence

P=a⁴b³c²d=a²b²u=[(3−u)(5−u)/4]u=(5−2u)u=5u−10>0.

Therefore A=10−5u, A²=225−100u=25(9−4u)>0. Positivity is exact: u>2 and 9>4u because81>80. With i¹⁰=−1, the quoted HT formula at p=1 gives

s=τ(S³)=−A/(100u)=(5−2u)/100>0,
s²=(9−4u)/2000,
D=1/s=100+40u.

At p=5 the scalar is −1/(2500u), and the inner sum contributes625. Thus the RAW invariant from the quoted formula is

τ(L(5,q))=−exp(πi·12s_D(q,5)) B_q/(4u),
|τ(L(5,q))|²=|B_q|²/80.

Here s_D denotes the Dedekind sum, avoiding confusion with vacuum s. Dividing by the SAME τ(S³) gives

τ̂(L(5,q))=25exp(πi·12s_D(q,5)) B_q/A,
|τ̂|²=625|B_q|²/(225−100u)=25(9+4u)|B_q|².

The last equality follows from (9−4u)(9+4u)=1. Expanding now gives

25(9+4u)(11+2u)=3475+1550u,
25(9+4u)²=4025+1800u,
difference=550+250u>0.

These are algebraic identities and sign proofs, not decimal decisions. The raw squared magnitudes are less than1 (11+2u<16, 9+4u<18), consistent with the anticipated unitary-vacuum-word scale, though that bound is only a control and not independent proof of the imported category.

## 5. Exact phases and boundary/convention controls

Directly at p=5 the sawtooth values for n=1,…,4 are−3/10,−1/10,1/10,3/10. Thus s_D(1,5)=1/5. For q=2 the four products are3/100,−3/100,−3/100,3/100, sum0. Negating q negates the Dedekind sum, so s_D(4,5)=−1/5 and s_D(3,5)=0. The phase at q=1 is exp(12πi/5)=t²; q=2 has phase1.

Conditional on the quoted exact formula, τ̂(L(5,2)) itself is the positive real45+20u, whose square is the asserted second value. At q=1 the same formula gives25(1+2t²+2t³)/A. Its numerator has real part1 and imaginary part4sin72°, with squared norm11+2u. These are extra exact checks of phase/prefactor consistency, not new theory claims.

For q↦−q, multiply w on the right by the longest Weyl element w₀, which sends ρ to−ρ and has sign(−1)¹⁰=+1. The outer exponent changes to its conjugate; the linear phase becomes the negative of its original argument, while the quadratic phase and Dedekind factor also conjugate. The leading i¹⁰=−1 is real. Thus the entire quoted invariant conjugates. At fixed p=5 it is periodic in q modulo5: the quadratic term is1, the linear extra factor pairs ν with integralρ, and the Dedekind symbol is periodic.

Therefore q=4 matches q=1 in magnitude and q=3 matches q=2. Inverting 2 modulo5 gives3, whereas1 stays1, so inverse-denominator conventions do not remove the difference. Complex conjugation, framing anomaly and signature phases have modulus1; a fixed nonzero theory-wide scalar rescales both squared magnitudes by the same positive number. None can turn unequal nonzero values into equal ones.

At p=1 the same formula is exactly the S³ boundary above. A normalized result must have τ̂(S³)=1. The p=0 case is excluded from HT's quoted formula and is not silently used. These boundaries can detect an extra division by the vacuum scalar.

## 6. Full-weight matrix route: actual necessary checks, not assumed replay

The allowed labels are the nonnegative quadruples with sum≤5, counted by stars-and-bars as C(9,4)=126. S₅ has120 elements and126·127/2=8001 symmetric entries. These are finite cardinalities, not independent scientific-result counts.

The printed S formula has scalar −1/(100u) multiplying an integral Weyl numerator. Consequently S₀₀=s is NOT itself an algebraic-integer claim in Z[ζ₁₀₀]. Exact arrays can store integral unscaled numerators and track the scalar separately. Any supplied program must do so consistently; the phrase “matrix entries in Z[ζ₁₀₀]” cannot justify discarding those scalar factors. A larger cyclotomic field is valid even when a particular entry belongs to a smaller subfield.

The negative continued fractions are5=[5] and5/2=3−1/2=[3,2], not3+1/2. The corresponding canonical normalized words are Sθ⁵S and Sθ³Sθ²S if the cited convention applies. Categorical Hopf entries are D S, so replacing one matrix by the other without the prescribed component factors creates a NON-unit scalar error. The number of word factors differs and makes this a serious falsification target.

The expected normalization is |F₀₀|/s, once, for either canonical word. As an abstract boundary check, the modular relation for the unit-framing S³ word gives |(SθS)₀₀|=s up to its unit anomaly; the normalized magnitude is1. For the zero-framing S¹×S² word S²=C, F₀₀=1 and its normalized value has magnitudeD. These use standard modular/surgery identities as CONDITIONAL inputs at this stage, not a fresh proof of their precise HT implementation.

The central charge computed from these parameters is k·dimG/r=5·24/10=12. Thus the usual linear-T central scalar is exp(−2πic/24)=−1; the stated anomaly at c=12 is likewise−1. Such phases are harmless to magnitudes only after the category/root and surgery normalization are authenticated. The full126-label matrix evaluation has not been computed by hand or run before this freeze; only its exact structural requirements and boundaries are established here.

## 7. Independent topological controls

The unknot exterior is a solid torus with fundamental group generated by the knot meridian μ; the preferred longitude is nullhomotopic in that exterior. Dehn filling slope−5μ+qλ imposes μ⁵=1, giving Z/5 for q=1,2, both coprime to5. This is an ordinary connected closed oriented filling, with no link insertion retained in the manifold invariant.

A second control uses the surgery chains. The one-component linking matrix is[5], with cokernel Z/5. The two-component Hopf-chain matrix is[[3,1],[1,2]], determinant5 and Smith factors1,5. The Hopf complement meridians commute; the relations3μ₁+μ₂=0 and μ₁+2μ₂=0 eliminate to5μ₂=0. Thus it too has Z/5, not merely the same homology order by a misleading determinant. Both matrices are positive definite (principal minors positive), so their signatures1 and2 differ only through the explicit unit-modulus signature corrections. A sign/orientation convention does not change the group or magnitudes.

No homotopy-equivalence assertion is required by the stated fundamental-group conjecture. No all-G or all-level classification is proved: one permitted fixed theory and two nonzero values suffice, IF the actual printed conjecture and imported full-category theorem have the stated scope.

## Actual result and precise remaining gates

The complete finite arithmetic reduction and all displayed constants, parities, denominator/sign/positivity and topological controls above have actual independent hand derivations. The important attempted falsifiers (wrong annihilator, incorrect continued fraction, root/shift/Galois confusion, Hopf-normalized matrix confusion and vacuum divisions) have concrete failure mechanisms, not just a checklist.

The unresolved external interfaces are exact: HT v2 must supply the ordinary FULL SU(5) category at r=10 and the general p=5 surgery formula without an excluded coprimality hypothesis, the stated S/T/Hopf normalization must match, and Ohtsuki's actual printed conjecture must include this case. The native code/full-weight route and contextual/prior-source statements remain unread/unexecuted. A missing theorem interface is not repaired by finite arithmetic. Any substantive mismatch must defer the full original claim without changing level/category/target. No final scientific disposition or historical priority conclusion is issued at this source-first checkpoint.
