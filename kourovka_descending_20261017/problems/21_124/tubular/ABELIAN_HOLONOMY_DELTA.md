# Pell candidate: obstruction to every abelian finite linear holonomy

UTC: 2026-10-24T22:26:00Z. **New partial claim, not yet independently audited.** This strengthens the elementary abelian2 filter in the frozen PELL_CANDIDATE.md. It does not exclude nonabelian finite holonomy and does not settle21.124.

## Claim

For the CAT(0) F₅-by-Z candidate G in PELL_CANDIDATE.md, no homomorphism to R^N⋊Q with **Q finite abelian** can inject both vertex groups, in any N. In fact the translation vectors of suitable powers of a,b must vanish. The conclusion concerns a class of witnesses, not arbitrary finite-index RAAG embeddings.

As in the frozen note, let A,B,T be the translation vectors of the common powers a^M,b^M,t^M, where M kills their linear parts. For each stable letter sᵢ, its orthogonal action Sᵢ gives

    Sᵢ(pᵢA+T)=qᵢB+T,

with (pᵢ,qᵢ)=(3,2),(20,14),(119,84). If Q is finite abelian, complexify and simultaneously diagonalize the three commuting Sᵢ. On one simultaneous character space with inverse eigenvalues x,y,z, all roots of unity, the coefficient matrix has rows

    [pᵢ, −λᵢqᵢ, 1−λᵢ], (λ₁,λ₂,λ₃)=(x,y,z).

Its determinant divided by2 is

    D(x,y,z)=−99x+812y−714z−714xy+820xz−105yz.       (1)

The only root-of-unity triple satisfying D=0 is (1,1,1), as established below. For that triple, rows [3,−2,0] and [20,−14,0] force A=B=0. All other character spaces have nonsingular coefficient matrix, also forcing A=B=0. Thus A=B=0 globally, contradicting vertex injectivity.

## Root-of-unity reduction, with proof of the needed Mann lemma

A minimal rational relation ∑_{i=1}^k cᵢωᵢ=0 means cᵢ are nonzero rationals, ωᵢ are roots of unity, and no nonempty proper subsum vanishes. Then every quotient ωᵢ/ωⱼ has order dividing the product of the primes at most k. This is the classical elementary Mann bound; its original source is H.B.Mann, *On linear relations between roots of unity*, Mathematika12(1965),107–117, DOI https://doi.org/10.1112/S0025579300005210. A self-contained argument for the bound follows.

Normalize ω₁=1 and let N be the least common multiple of the ωᵢ orders. If p^e exactly divides N, decompose roots into p-primary and prime-to-p parts. If e≥2, the extension Q(ζ_N)/Q(ζ_{N/p}) has degree p. Grouping terms according to the p-primary exponent modulo p gives a relation in the basis1,ζ_{p^e},...,ζ_{p^e}^{p−1}, hence each residue-class subsum vanishes. Minimality forces every term into the same residue class, which is0 since ω₁=1. This contradicts minimality of N, since then N/p suffices. Thus N is squarefree.

For p|N, group terms by exponent of ζ_p over K=Q(ζ_{N/p}). The minimal polynomial is1+X+...+X^{p−1}: its degree is p−1 because the cyclotomic extension degree is φ(N)/φ(N/p)=p−1. Hence either all p grouped coefficients are equal or all are0. If p>k, some group is empty and has coefficient0, so all are0. Minimality again forces all terms into one residue class and removes p from N, a contradiction. Therefore p≤k. This proves the bound. The cyclotomic degree formula and φ(N)=[Q(ζ_N):Q] are the standard defining degree property of cyclotomic polynomials.

Apply this lemma to a decomposition of the six terms of(1) into minimal vanishing subsums. A two-term subsum requires equal coefficient magnitudes, so the only possible pair is the two coefficients of magnitude714. A three-term subsum is impossible: the Mann bound gives relative phases in μ₆, and three nonzero rational-length vectors in these six directions can sum to0 only if their magnitudes are all equal or one is the sum of the other two. Neither occurs among any triple of99,812,714,714,820,105. This last finite arithmetic fact is checked exactly by the script; the elementary six-direction classification follows by resolving coefficients in the rational basis1,ζ₆ and inspecting the three unoriented lines.

There are consequently only two possibilities:

1. All six terms form one minimal relation. Their root ratios belong to μ₃₀. Comparing x with xy, x with xz, and y with xy shows x,y,z∈μ₃₀.
2. There is the two-term714 pair and a minimal four-term remainder. The pair forces z=−xy. For the four remaining roots x,y,xz,yz, the Mann bound gives all ratios in μ₆, so z∈μ₆ and x/y∈μ₆. Together with xy=−z∈μ₆ this gives x,y∈μ₁₂.

Partitions containing a singleton are impossible; three-plus-three has just been excluded; three pairs would require more equal-magnitude pairs. Thus these cases are exhaustive, and in both x,y,z∈μ₆₀.

## Exact cyclotomic certificate

The standalone standard-library script check_abelian_holonomy.py enumerates all60³ triples in Q(ζ₆₀), using the integral polynomial

    Φ₆₀(X)=X¹⁶+X¹⁴−X¹⁰−X⁸−X⁶+X²+1.

Each power of ζ₆₀ is represented by its exact16 integral coordinates modulo this monic polynomial. It evaluates(1) without floating point. The only zero triple has exponents(0,0,0). See abelian_holonomy_certificate.json. The reduction above is essential: finite enumeration alone would not establish the arbitrary-order claim.

## Exact residual obstruction

Finite nonabelian holonomy permits simultaneous eigenspace mixing, so the determinant and Mann argument do not apply. A search through all transitive permutation representations of degree≤5, up to simultaneous conjugacy, found no nonzero horizontal solution; see finite_holonomy_results.json. This is bounded evidence only. The unbounded nonabelian finite-holonomy problem remains the central unsupported claim; treating it as solved by this calculation would merely transfer the difficulty.
