# Independent audit: mirror-quintic orbifold coefficients

Date: 2026-10-21. Scope: a normalization-sensitive mathematical audit, not a complete solution of the unqualified AIM question.

## Accepted mathematical checks

Let u be the Dwork parameter, Ψ=u^5, and θ=Ψ d/dΨ. The operator Ψθ^4−∏_{j=1}^4(θ−j/5) agrees with HKQ §3. The solutions ω_k=u^k A_k(u^5), A_k(0)=1, obey

 a_{k,n}/a_{k,n−1} = (n−1+k/5)^4 / ∏_{j=1}^4(n+(k−j)/5).

The denominator is nonzero for n≥1 and k=1,…,4. Substitution proves this recurrence, rather than merely fitting coefficients. The coefficient ratio tends to one, so A_k converges for |Ψ|<1. The normalized ratio s=ω_2/ω_1=u A_2/A_1 extends across u=0 with derivative one and has a local analytic inverse.

The independently recomputed coefficients are

- s=u+13u^6/360+110069u^11/9979200+O(u^16).
- u=s−13s^6/360−31991s^11/9979200+O(s^16).
- C_sss=5+5s^5/3+5975s^10/6048+O(s^15).
- F_1=−s^5/9−163s^10/18144+O(s^15).

The Yukawa expression used is 5 A_1(u^5)^(−2)(1−u^5)^(−1)(ds/du)^(−3). This includes the HKQ period rescaling ω̂=5^(3/2)ω. Three integrations with vanishing degree-at-most-two terms give F_0=5s^3/6+5s^8/1008+5975s^13/10378368+O(s^18).

For Guo–Ross genus one, t=5u, τ=5s and I_0=A_1(u^5), hence dτ/dt=ds/du. Their formula becomes −31 log(A_1)/3−log(1−u^5)/12−log(ds/du)/2. Logs are the local branches vanishing at u=0; this fixes F_1(0)=0. These low-genus formulas define genuine local analytic germs, not only formal coefficients.

The separate exact_checks.py was inspected and executed successfully. It checks 16 recurrence equations, the inverse to order (s^5)^4, four HKQ coefficients in each of genera zero and one, 24 listed support residues, and the elementary remaining-index count for genera 2–53. Its higher-genus table is a transcription, not an independent computation of higher-genus amplitudes. The additional F_0 coefficient at s^23 is a consequence of the stated Yukawa formula and carries no novelty claim.

## Conditional support statement and limitations

In the fixed orbifold polarization and Hodge frame, assume the amplitude is regular on the u-cover and satisfies F_g(ζs)=ζ^(2g−2)F_g(s), where ζ^5=1. Then each nonzero power s^n has n≡2g−2 modulo five. This follows coefficientwise and does not prove that the least allowed exponent has a nonzero coefficient. Regularity alone does not supply this character. Genus one allows a constant before its additive normalization is fixed; genus zero has integration ambiguities before normalization or covariance is imposed.

For g≥2 the common rescaling of the period frame matters: the normalized genus-g expression contains ω̂_0^(2g−2). Genus one is separately fixed using its logarithmic formula; its normalization should not be inferred from an exponent-zero frame weight. The holomorphic limit at the orbifold uses the continued polarization and antiholomorphic boundary limit. Merely substituting a new algebraic coordinate into the large-radius holomorphic free energy is not sufficient.

HKQ §3.4 supplies the displayed genus 0–5 coefficients; genera 2–5 were source-checked, not rederived here. Its leading coefficients are 155/18, 488305/9072, 48550/567, and 1237460905/224532 at powers 2,4,1,3 respectively. The source describes the higher-genus orbifold expressions as predictions. Do not turn this transcription or its support check into a theorem identifying all-genus FJRW/GW potentials.

No coefficient table proves convergence of the sum over genera. No formal support calculation classifies arbitrary analytic singularities. Fixed-genus analyticity can follow from convergent period expressions with controlled denominators, but an unspecified all-genus amplitude has not been established by these computations.

## Literature status

The September 2026 Chang–Guo–You–Zhang preprint claims a proof of the quintic conifold gap: Theorem 1 is a transfer criterion and Theorem 2 verifies its hypotheses for the quintic MSP theory. Its Definitions 1.1–1.2 use an admissible differential-ring substitution into formal Laurent series. This audit inspected the statements, not the complete proof, and establishes no peer-review status. The result is about the conifold; it does not itself provide all-genus orbifold leading coefficients or an all-genus quantized LG/CY correspondence.

All eight locally recovered primary-source PDF byte counts and SHA-256 hashes were independently checked against public_pdf_manifest.json and passed. Source documents are not reproduced in this audit.

Sources: HKQ https://arxiv.org/abs/hep-th/0612125, Guo–Ross https://arxiv.org/abs/1611.08876, Chang–Guo–You–Zhang https://arxiv.org/abs/2609.13921. Further source distinctions are recorded in SOURCE_STATUS_GATE.md.

## Acceptance disposition

Accept the bounded coordinate, normalization, low-genus computation, source-attribution and conditional-support audit. Do not claim a new arbitrary-genus coefficient formula, all-genus LG/CY proof, full original AIM solution, or independent validation of the entire 2026 preprint.

## Additional fixed-genus obstruction verified

For every fixed g≥4, within HKQ's polynomial BCOV ansatz and with lower genera held fixed, put m=ceil(3(g−1)/5) and δP_g=X(X−1)^m, where X=(1−Ψ)^(−1). Its degree m+1≤g−1, and δP_g(0)=0. The X-only perturbation preserves the genus-g anomaly equation and the large-radius constant-map coefficient. The factor (1−Ψ)^(g−1)δP_g=Ψ^m(1−Ψ)^(g−m−2) is regular at the conifold because g−m−2≥0. Multiplication by a nonvanishing conifold period frame and Ψ^(1−g) does not introduce a conifold pole. Thus it preserves the prescribed conifold principal part, not just its leading pole.

In the stated orbifold frame the perturbation is 5^(2g−2)u^r A_1(u^5)^(2g−2)(1−u^5)^(g−m−2), where r=5m−3(g−1) lies in {0,1,2,3,4}. It is regular with the required character and changes the coefficient of the least allowed s-power by 5^(2g−2). Arbitrary scalar multiples give the corresponding arbitrary shift. This directly proves nonuniqueness of that coefficient under the listed fixed-genus constraints. It is not a simultaneous all-genus construction, does not preserve unspecified enumerative inputs, and says nothing against uniqueness of the actual geometric theory. No novelty claim is made.
