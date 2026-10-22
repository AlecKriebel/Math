# Complete independent mathematical audit of bounded interval Schur ratios

This is an AI-assisted, unrefereed mathematical edition. Acceptance means an independent internal AI audit of the stated partial results. It is not external human peer review, journal acceptance, formal proof-assistant certification, or a novelty or priority claim.

This is not a computational reproduction package. The full authored proof and full mathematical audit are retained in PROOF.md and AUDIT.md. Copied source documents, source text and images, executable code, raw datasets, raw search responses and private coordination material are not distributed. References to checking programs describe historical verification; those programs are not included.

Source retrieval, inspection and mathematical execution statements describe the original candidate and independent audit of October 11, 2026 UTC. Editorial preparation authenticated their sealed bytes, but performed no new scholarly-source retrieval, source-body inspection, literature survey or mathematical execution. Finite checks support exact identities only; the universal analytic and sign arguments must be read in full.

## Verdict and scope

**Accept the claimed partial results as written. No mathematical correction is required.** The audited results are the complete two-variable classification for intervals whose closure contains 1, its sharp example with threshold 1+√2, the exact three-variable classification for the single pair (5,1,1)/(4,3,0), and the two stated general-dimensional local criteria. The proof distinguishes a comparison with the reference value from an attained minimum, uses ordinary partitions consistently, and excludes zero coordinates from its domain.

This acceptance does **not** solve the arbitrary-partition, arbitrary-dimensional bounded-interval question in AIM total positivity Problem 1.45. It does not classify all three-variable pairs. It does not establish novelty or priority. In particular, neither the N=2 endpoint reduction nor the special N=3 calculation is a general rule that minima of Schur ratios occur at box vertices.

The original manuscript underlying PROOF.md is 22,127 bytes, SHA256 `38e9130b33a25f15c22edd7a38c6eb676ff7880df5e9f5a0a90de6afe937c6d8`. Its candidate manifest has SHA256 `8948c3e0c7b0b11313e8a167d695fc467e28a61a881314e024be443eddf52515`; the separately supplied candidate seal has SHA256 `a5a8c4ed1100d511d306ab83deca25fdf69240effe6471a8b93d13b3cc31c682`. Both pins and every listed candidate member were independently reauthenticated. The candidate files were left unchanged.

## Method and independence

The audit read every mathematical claim and its argument. The analytic proofs below were checked directly, including their quantified domains, endpoint limits and equality cases. The audit also constructed fresh exact computations using only Python's standard library. No candidate checker, imported-report program, or source-author program was executed or imported.

The independent computation starts with the combinatorial definition: enumerate semistandard tableaux of each relevant shape, with entries in {1,…,N}, rows weakly increasing and columns strictly increasing. Each tableau contributes its weight monomial. This independently recovers the two Schur polynomials before comparing them with the complete-homogeneous and Jacobi–Trudi expressions used in the manuscript. Fraction arithmetic then reconstructs every coefficient of the polynomial certificate and its Bernstein change of basis. The computation is an exact verification of finite identities; the universal sign and analytic arguments are provided in writing, not inferred from samples.

The auditor-owned historical exact checker gives this independent computation. The normal, `-O` and `-OO` results are identical and use explicit exceptions rather than assertions for acceptance conditions. The 36 two-variable shapes with top part at most seven are an additional finite formula check, not a replacement for the general bialternant derivation. The few exact point evaluations are diagnostics only.

## Reference value and exponent conventions

For partitions λ and μ padded to length N, the object being compared is

R(x) = sλ(x)sμ(1ᴺ) / (sμ(x)sλ(1ᴺ)).

Schur polynomials have nonnegative coefficients and are strictly positive on (0,∞)ᴺ. Thus this ratio is well defined and continuous there. Its value at 1ᴺ is 1. The statement R≥1 on Iᴺ says that 1ᴺ is a minimum point only if 1 belongs to I. If 1 is an excluded boundary point, diagonal points tending to 1 prove that the infimum is 1, whenever the comparison is valid. They do not make the absent point a minimizer. In the equal-degree case every diagonal point has value 1, so attainment can occur elsewhere even when 1 is absent. The manuscript observes this exception correctly.

Every finite positive missing endpoint can be supplied by continuity when testing the inequality. No evaluation at 0 or ∞ is needed or valid in this argument. For an interval whose closure does not contain 1, the normalized comparison still makes sense; only the special N=3 theorem claims to classify every such interval as well.

For the increasing strict exponents associated to λ, the correct conversion is

nⱼ = λₙ₋ⱼ + j,  0≤j<N,

with the subscript on λ ranging from 1 to N. Equivalently λᵢ=nₙ₋ᵢ−(N−i). The manuscript uses precisely this reversal plus staircase. If V denotes the ordinary Vandermonde on the exponents, the dimension formula is sλ(1ᴺ)=V(n)/V(0,1,…,N−1). Consequently normalization of the Schur ratio agrees with normalization of the generalized Vandermonde determinants by V(n), with continuous extension across repeated x-coordinates. It is not a quotient of two directly evaluated zero determinants at 1ᴺ.

When comparing the largest j components, the common staircase contributes the same sum on both sides. It also cancels for comparisons of the smallest j components, which are the relevant sums after negating and reordering. Thus the transfer of the usual majorization conventions is valid. Adding a common rectangle (rᴺ) multiplies both Schur polynomials by the same positive monomial and changes neither ratio.

## Complete two variable classification

Write λ=(a,b), μ=(c,d), with nonnegative decreasing parts, and set D=a+b−c−d, p=a−b+1 and q=c−d+1. All p and q are strictly positive. The ordinary Schur formula is

s(a,b)(x,y) = (xy)ᵇ Σⱼ₌₀ᵖ⁻¹ xᵖ⁻¹⁻ʲ yʲ.

At (1,1) the dimension is p. Substituting x=eᵘ⁺ᵛ, y=eᵘ⁻ᵛ and t=|v| gives the exact separation

R(x,y)=eᴰᵘ H(t),  H(t)=q sinh(pt)/(p sinh(qt)),  H(0)=1.

For A=inf(log I), B=sup(log I), feasible means satisfy A+t≤u≤B−t and 0≤t≤(B−A)/2, using limits when endpoints are omitted. This exhausts every pair in I²; there is no unexplained reduction to selected pairs.

Let F=log H. Direct differentiation yields

F′(t)=p coth(pt)−q coth(qt),
F″(t)=q²/sinh²(qt)−p²/sinh²(pt).

For fixed t>0, r coth(rt) increases strictly with r: its derivative has numerator sinh(rt)cosh(rt)−rt, positive because its derivative in rt is 2sinh²(rt). Also r/sinh(rt) decreases strictly with r, since sinh(s)−s cosh(s)<0 for s>0. Therefore p>q makes F strictly positive and increasing from zero; p=q makes F identically zero; p<q makes F strictly negative, decreasing and strictly concave. The limits F(0)=F′(0)=0 follow from the regular Taylor expansion of sinh. All sign directions in the manuscript are correct.

Diagonal homogeneity gives R(z,z)=zᴰ. Hence an interval extending rightward from 1 requires D≥0, one extending leftward requires D≤0, and an interval containing values on both sides requires D=0. On a right interval the minimal feasible mean for D≥0 is u=t, so the worst value at spread t has logarithm Dt+F(t). On a left interval the maximal feasible mean for D≤0 is u=−t, giving |D|t+F(t).

If p≥q these functions are nonnegative. If p<q they are strictly concave and vanish at t=0. On a finite range [0,T], the endpoint value is nonnegative if and only if every value is nonnegative: sufficiency follows from the chord bound and necessity from continuity at T. Therefore the manuscript's finite right criterion is D≥0 together with eᴰᵀH(T)≥1, T=(log sup I)/2. Its finite left criterion is D≤0 together with e⁻ᴰᵀH(T)≥1, T=−(log inf I)/2. The criteria still apply when one or both finite endpoints are excluded.

For p<q, the derivative of |D|t+F(t) decreases to |D|+p−q, while the function itself is

(|D|+p−q)t + log(q/p) + o(1).

A negative limiting slope forces eventual failure. A nonnegative limiting slope makes the function increasing from zero; even at limiting slope zero its derivative is strictly positive at every finite t. This validates both unbounded cases. The right conditions are D≥0 and D≥q−p, equivalently a≥c and a+b≥c+d. The left conditions are D≤0 and −D≥q−p, equivalently b≤d and a+b≤c+d.

On any two-sided interval, D=0 is necessary, and then the sign of H−1 depends only on p−q. Thus the condition is exactly p≥q. The singleton {1} is trivial. These cases cover every nondegenerate interval whose closure contains 1, but make no general claim for intervals away from 1.

The equality claims also pass. For D=0, p>q gives precisely all diagonal points, while p=q gives a constant ratio. For D≠0 on a valid finite one-sided interval, a strict endpoint test leaves only (1,1), if present. An equality endpoint test necessarily has p<q, and strict concavity makes the interior spreads strictly positive; its additional equality pairs are the two ordered opposite endpoints, present only if both endpoints belong to the interval. Valid infinite one-sided intervals with D≠0 have no finite nonzero spread of equality. When 1 is absent, equality configurations requiring it disappear.

Finally, for p<q, strict concavity and F(0)=0 imply that F(t)/t strictly decreases for t>0. Its limits are 0 and p−q. For 0<|D|<q−p this proves exactly one positive cutoff T*, with allowable logarithmic width at most 2T*. It establishes uniqueness analytically and requires no numerical optimization.

### The example with threshold 1 plus square root of 2

For λ=(3,3), μ=(4,1), the dimensions are 1 and 4. Cancelling a positive xy factor gives

R(x,y)=4x²y²/(x³+x²y+xy²+y³).

The classification reduces [1,B]², B>1, to R(1,B)≥1. The numerator after subtraction factors exactly as

4B²−(1+B+B²+B³)=−(B−1)(B²−2B−1).

The other root of the quadratic is 1−√2<0. The comparison is therefore valid exactly for 1<B≤1+√2. Since 3<4 in the largest-part comparison, weak majorization fails. At the cutoff the two opposite corners are additional equalities. Both the formula and factorization were independently recovered from tableaux. This example and the two-variable reduction were already in the imported report; this audit makes no new-priority claim for them.

## Sharp three variable theorem

The relevant ordinary partitions have size seven and crossing initial sums:

λ=(5,1,1): 5,6,7;  μ=(4,3,0): 4,7,7.

Their strict increasing exponent tuples are (1,2,7) and (0,4,6). The Vandermonde values are 30 and 48, giving dimensions 15 and 24 after division by 2. Thus neither the normalized orientation nor the majorization comparison is reversed.

Direct tableau enumeration gives

sλ=xyz h₄,  sμ=h₄h₃−h₅h₂,

where hⱼ is the complete homogeneous polynomial in three variables. The dimension values are independently 15 and 24. The inequality is equivalent to P≥0 for

P=24sλ−15sμ.

The positive denominator introducing this equivalence cannot change signs. P is symmetric, homogeneous of degree seven, and zero at diagonal triples.

Every positive nondiagonal triple can be sorted, divided by its smallest coordinate, and written uniquely as (1+d,1+td,1), where d>0 and 0≤t≤1. After substitution P has a factor d². The fresh tableau calculation verifies coefficient by coefficient that

P(1+d,1+td,1)/d² = Σₖ₌₀⁵ Bₖ(d) binom(5,k)tᵏ(1−t)⁵⁻ᵏ,

with the six coefficients

B₀=6(4d³+18d²+24d+5),
B₁=(3/5)(8d⁴+74d³+204d²+193d+40),
B₂=(3/2)(4d⁴+26d³+56d²+49d+14),
B₃=−(3/2)(d+1)(d⁴+5d³+7d²−7d−14),
B₄=−(3/5)(d+1)(15d⁴+85d³+135d²+33d−40),
B₅=−6(d+1)²(5d³+15d²+9d−5).

The audit both derives these coefficients from the expanded power-basis polynomial and expands them back into that polynomial, checking the change of basis in both directions. The identity is exact and not a floating-point fit.

Put p₀(d)=5d³+15d²+9d−5. For d≥0 its derivative is positive. Its values at 1/3 and 7/20 are −4/27 and 323/1600. It has exactly one nonnegative root d*, with 1/3<d*<7/20. Setting ρ=1+d* gives 5ρ³−6ρ−4=0. This is also the unique positive root: the cubic is negative for 0<ρ≤1 and strictly increasing for ρ≥1. The exact arithmetic additionally brackets it between 134045265506422/10¹⁴ and 134045265506423/10¹⁴; the rational bracket, not its decimal display, is what has been certified.

For 0≤d≤d*, B₀, B₁ and B₂ have visibly positive coefficients. For B₃ the inner polynomial is bounded above by discarding −7d and evaluating its remaining nonconstant positive terms at 7/20. The result is exactly −2066099/160000<0. For B₄ the inner polynomial is strictly increasing on d≥0, and its value at 7/20 is exactly −257377/32000<0. Thus B₃ and B₄ are strictly positive throughout the required range. B₅ is nonnegative exactly when p₀(d)≤0 and vanishes there only at d=d*. Every Bernstein basis factor is nonnegative on 0≤t≤1. This proves P≥0 for all triples of coordinate ratio at most ρ.

The sharpness specialization was checked independently as

P(r,r,1)=−6r²(r−1)²(5r³−6r−4).

It is strictly negative for every r>ρ. Therefore the special-pair comparison holds throughout I³ if and only if (sup I)/(inf I)≤ρ, interpreting a zero lower endpoint or infinite upper endpoint as infinite quotient. Necessity for open intervals is genuine: when the endpoint quotient exceeds ρ, there are actual positive a′<b′ in I with b′/a′>ρ. The triple (b′,b′,a′) lies in the domain and violates the inequality after homogeneous scaling. The argument never substitutes zero or infinity into a Schur ratio.

For equality away from the diagonal, if t<1 then the k=0 Bernstein summand is strictly positive. If t=1 then only B₅ remains, and it vanishes precisely when d=d*. Hence the only positive off-diagonal equality triples are permutations of (ρc,ρc,c). Within a valid interval I, such a triple forces its endpoints to be a=c and b=ρc, both present. The manuscript's sharp-endpoint equality statement is consequently exact. If the interval has smaller quotient, only diagonals give equality. This also correctly covers singleton intervals at any positive value.

The common-rectangle pairs (6,2,2)/(5,4,1) give the identical ratio; the independent tableau calculation checks the multiplication by xyz directly. The claims about [1,4/3], [9/10,11/10], and failure for [1,3/2] follow from exact rational comparisons. In particular the two-sided example disproves necessity of ordinary majorization on every fixed bounded neighborhood of 1, even for equal degrees. It does not undermine the unbounded orthant theorem, whose necessity proof uses unbounded scaling.

## General dimensional one sided radius

The weight-vector construction is legitimate because the tableau coefficients are nonnegative and their sum is sν(1ᴺ)>0. For a shape of size k, its finite random weight vector Aν has nonnegative integer entries summing to k. Symmetry forces E Aν=(k/N)1. Consequently

fν(y)=log E exp(Aν·y)

has directional first derivative equal to the tilted mean and directional second derivative equal to the tilted variance.

For X supported in [m,M], E[(X−m)(M−X)]≥0 implies

Var X≤(EX−m)(M−EX)≤(M−m)²/4.

This remains true under every exponential tilt. If l=|μ|, the variable Aμ·y lies in [l min y,l max y]. Applying the variance bound to h(t)=fμ(ty) and integrating h″ against 1−t from 0 to 1 gives

fμ(y)≤lȳ+(l²/8)(max y−min y)².

Jensen's inequality gives fλ(y)≥|λ|ȳ. Subtraction yields precisely the manuscript's global lower bound for log R. No independence among the weight coordinates is assumed or needed.

On 0≤yᵢ≤B, put r=max yᵢ. If r>0 then ȳ≥r/N and range(y)≤r≤B. For D=|λ|−|μ|>0, the lower bound is at least r(D/N−l²B/8), strictly positive when l>0 and 0<B<8D/(Nl²). On −B≤yᵢ≤0 with D<0, the same calculation uses r=max(−yᵢ) and Dȳ≥|D|r/N. This proves the stated left radius with l² still the denominator-degree factor. If l=0 and D>0, Jensen alone proves positivity on the entire right orthant away from 1ᴺ. The impossible degree signs follow immediately by testing constant vectors.

These radii are strictly sufficient bounds. No optimality is established, and the manuscript does not claim optimality. Equality at the excluded numerical radius bound is not needed for its statement.

## Equal degree covariance criterion

For equal size k and N≥2, permutation invariance forces the covariance matrix of Aν to have a common diagonal entry and a common off-diagonal entry. The constant sum of its coordinates makes the row sums zero. Hence it is cν(I−11ᵀ/N), with cν equal to its trace divided by N−1, exactly as defined in the manuscript.

The Hessian of fν at zero is that covariance matrix. For g=fλ−fμ, equal degrees give exact invariance under y↦y+t1, and the gradient at zero vanishes. On the centered subspace, therefore,

g(z)=(cλ−cμ)||z||²/2+O(||z||³).

Finite exponential sums are positive and analytic near zero, so the third-order remainder is uniform in direction. Positive cλ−cμ yields a sufficiently small centered ball on which every nonzero z has g(z)>0; a negative difference yields g(z)<0. Exact shift invariance extends the first conclusion to arbitrary means, not just means near zero. A sufficiently small logarithmic interval width makes every centered vector in its box small. Conversely every nondegenerate interval with 1 in its closure admits nonconstant points with centered logarithms arbitrarily close to zero, proving the claimed obstruction when cλ−cμ<0.

When the difference is zero the second-order argument is inconclusive. The audit accepts no additional claim in that case. For the sharp N=3 pair, direct tableau moments give cλ=7/3 and cμ=25/12, so their difference is 1/4 and the centered quadratic term is ||z||²/8. This confirms the local direction but does not replace the exact finite-width proof.

## Literature and limits of source inspection

The original AIM Problem 1.45 wording was checked in its retained archived page. It asks about replacing the familiar orthant domains by other positive intervals. The manuscript's explicit normalization, tuple convention and requirement for literal attainment at 1 are appropriate clarifications. The direct AIM page again returned HTTP 502 during this audit; the archived wording was authenticated locally rather than presented as a successful live-page retrieval.

The selected text of Khare and Tao, *On the sign patterns of entrywise positivity preservers in fixed dimension*, was independently read on PDF pages 51–54. Theorem 10.1's necessity proof scales selected coordinates by t→∞ to recover the relevant partial sums. Remark 10.2 concerns neighborhoods of infinity, and Corollary 10.4 uses reciprocal variables. This validates the manuscript's stated limitation of those converse arguments for fixed finite boxes. It is not a complete reproof of all prerequisites of Khare–Tao. [Public source](https://arxiv.org/abs/1708.05197v6)

Theorem 1.4 and Theorem 1.5 of Belton, Guillot, Khare and Putinar were inspected in the retained text. Their coordinatewise domination hypothesis is explicit and is not a classification of all fixed bounded boxes. Their complete proofs were not audited. [Public source](https://arxiv.org/abs/2310.18020)

The first three pages and current metadata of Chen, Khare and Sahi were inspected for scope. The public version is v2, revised 13 February 2026, and concerns majorization questions for Jack and Macdonald polynomials. This limited inspection establishes neither an exhaustive absence claim nor priority for any result here. [Public source](https://arxiv.org/abs/2509.19649)

The three public arXiv metadata records were freshly checked. Existing PDF and text bytes were authenticated, but no whole-PDF reading or new visual inspection is claimed. Source text and PDFs are not copied into the audit packet.

## Final acceptance boundary

The finite identities, analytic reductions, sign arguments, equality characterizations, normalization, domains and provenance limitations all support acceptance of the exact partial scope stated above. No correction patch is warranted. The general AIM interval question, arbitrary N≥3 pair classification, the zero-covariance case, any general vertex reduction, and all novelty assertions remain outside acceptance.
