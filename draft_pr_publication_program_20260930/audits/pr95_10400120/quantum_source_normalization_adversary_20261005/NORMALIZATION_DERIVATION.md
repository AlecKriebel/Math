# Independent source normalization derivation

Recorded before reading the submitted proof/review (2026-10-05 20:31 UTC).

## Construction inputs from primary literature

Hansen–Takata arXiv:math/0209403v2, Eq. (12), pp. 9 and 26–27: for A4, rank l=4, |Δ+|=10, h∨=5, m=1, κ=r=10, roots of length √2, X the full weight lattice, Y∨=Y the root lattice, vol(Y)/vol(X)=5. The quantum-group parameter is q=e^(πi/10), a primitive twentieth root. Their stated modular-category construction invokes Bakalov–Kirillov Theorem 3.3.20; category existence is a cited theorem input, not something proved merely by checking finite matrices. Their label set is the entire int(C10)∩X, equivalently dominant Dynkin labels a1,…,a4≥0 with sum≤5, shifted by ρ. There are binomial(9,4)=126 labels. No restriction gcd(5,10)=1 appears in this construction.

Write x=λ+ρ and y=μ+ρ in the hyperplane sum coordinates=0. Then the normalized unitary matrix is

Sλμ = i^10/(10²√5) ∑_{w∈S5} sign(w) exp(-2πi (wx,y)/10).

The vacuum entry is positive

s=S00=1/(100√5) ∏_{j=1}^4 (2 sin(πj/10))^(5-j),

and D=1/s. The category Hopf matrix of Hansen–Takata is H=D S (it is unnormalized, with H00=1). Twist θλ=exp(πi((x,x)-(ρ,ρ))/10). Here ρ=(2,1,0,-1,-2), ρ²=10. HT Eq.(12) uses T_lin,λ=exp(πi x²/10-πiρ²/5). Its ratio to θλ is ω^-1, with central charge c=12 and ω=exp(2πic/24)=-1. Thus T_lin=-θ; this is a unit global factor. HT Δ/D=ω^-3=-1.

## Why one S00 division, for either surgery word

Guadagnini–Pilo hep-th/9612090v1 Eq.(13) uses X=a_k H and Y=θ (or mirror/conjugate convention). H00=1 gives a_k=X00=s. Eqs.(19),(20) give their S3-normalized invariant I(Lp/q)=unit_phase × s^-1 × (S θ^{z_d} S … θ^{z_1} S)00. The factor s^-1 is independent of the number of surgery-chain components. Therefore

|I(L(5,1))|²=|(Sθ^5S)00|²/s²,
|I(L(5,2))|²=|(Sθ^3Sθ^2S)00|²/s².

A direct Kirby-color check: for a link with n components, S3-normalized RT equals (unit framing phase) D^-n F(L;Ω,…,Ω), where Ω=∑ dλ Vλ. For one unknot, F=∑ dλ² θλ^5, and D^-1F=(Sθ^5S)00/s. For the two-component Hopf chain, F=∑ dλ dμ Hλμ θλ^3 θμ^2; D^-2F=(Sθ^3Sθ^2S)00/s. In the second equality H=D S is essential. Accidentally replacing H by S loses D, while adding a second s^-1 overnormalizes.

HT uses τ_HT(S3)=D^-1=s and τ_HT(S1×S2)=1. Corollary 4.2 and Eqs.(29),(30) imply τ_HT(L)=unit × vacuum matrix coefficient in normalized S,T, so τ'=τ_HT/s agrees in magnitude with GP I. All signature factors Δ/D=-1, all ω factors=-1, and all projective/framing correction factors have modulus one. Normalize τ'(S3)=1; then τ'(S1×S2)=D.

## Surgery conventions and topology

GP Eq.(16): 5/1=[5], 5/2=3-1/2=[3,2], where the listed order is z_d,…,z_1. Thus Eq.(20) gives ST^5S and ST^3ST^2S. The two-component linking matrix can be taken [[3,1],[1,2]], determinant 5 and positive definite, signature 2. The one-component matrix [5] has signature 1. Their chain eliminates to the rational unknot slope 5/2. From the Hopf link complement group Z² with meridians x,y, surgery gives 3x+y=0, x+2y=0, hence cyclic group of order5. Unknot 5 surgery gives cyclic order5 as well.

HT defines L(p,q) using slope -p/q. Its symbol L(5,q) is the orientation reverse of the positive-slope GP manifold. With a unitary category reversal conjugates the invariant; the magnitude is unchanged. Inverse-q conventions can replace q=2 by q=3 and q=1 by q=4 under reversal. Reversing the chain swaps exponents; because S is symmetric and T diagonal, the vacuum coefficient is invariant under transposition of the word. No claim of equality between q=1 and q=2 follows from these convention symmetries.

## Independent alternative exact route, not submission-derived

HT Theorem5.1 applies without gcd(r,p)=1. At p=5, κ=10 the root-lattice Gauss factor exp(πiqκν²/p)=exp(2πiqν²)=1. Character orthogonality over Y/5Y leaves only w with qρ-wρ∈5X, equivalently all five coordinates congruent modulo5. There are five such permutations for each q=1,2, and the inner sum is |Y/5Y|=5⁴=625. Put G_q=∑_(qualifying w) sign(w) exp(-2πi(ρ,wρ)/50). After discarding only unit prefactors, HT gives |τ_HT(L(5,q))|²=|G_q|²/80. Thus |τ'(L(5,q))|²=|G_q|²/(80s²). This formula will be evaluated in Q(ζ50) independently of the submitted calculation.

## Exact evaluated certificate

Let z=exp(2πi/50), u=z^10-z^15=(√5-1)/2. The five qualifying q=1 permutations have signs +1 and ρ-dot values 10,0,-5,-5,0. Thus G1=z^-10+2+2z^5. The five q=2 permutations have signs -1 and dot values 5,5,-5,0,-5. Thus G2=-1-2z^-5-2z^5=-(2+√5). Exact arithmetic modulo Φ50(z)=z^20-z^15+z^10-z^5+1 gives

|G1|²=13+4u=11+2√5,
|G2|²=13+8u=9+4√5.

The exact sine-product square is s²=(125-200u)/50000=(225-100√5)/50000=(9-4√5)/2000. It is positive because 9²>80=(4√5)². Rationalizing gives D²=1/s²=18000+8000√5 and D=100+40√5. Hence

|τ'(L(5,1))|²=(18000+8000√5)(11+2√5)/80=3475+1550√5,
|τ'(L(5,2))|²=(18000+8000√5)(9+4√5)/80=4025+1800√5.

The difference is 550+250√5>0; both are positive. In HT normalization the difference already equals (-2+2√5)/80>0. Thus no common positive/nonzero theory normalization can remove the mismatch. q=4 has the same square as q=1; q=3 the same as q=2, verified in the same exact computation.

## Convention hazard resolved

GP uses q=exp(-2πi/k_GP), with k_GP a renormalized coupling. Its k_GP corresponds to shifted r, not WZW k. HT uses q=exp(πi/r); the squared root q² is the conjugate of GP's parameter when k_GP=r. The two conventions can therefore be mirror versions. GP gives explicit signature phases only for SU(2)/SU(3); no SU(3) phase is imported for SU(5). The full SU(5) construction, anomaly magnitude, and lens formula are supplied independently by HT.
