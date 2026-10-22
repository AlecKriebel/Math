# Independent derivation and falsification audit: EP421

This audit accepts the full density-one existence theorem using two authenticated published counting inputs. It does not claim a new theorem or certify the prior manuscript's stronger deletion exponent. All prime gaps below are between consecutive primes. Constants are fixed independently of the variable X, the selected witness, and polynomial coefficients/degrees unless an explicitly displayed degree factor appears.

## Exact target and imported statements

The scanned actual original, Erdős-Graham1980 printed84/PDF80, asks for 1<=d1<d2<... of density one, with injective products over every nonempty index interval [u,v]. No finite length restriction is imposed. The present construction omits1, which is permitted; retaining1 would itself duplicate a later one-term product by adjoining1. The current original-problem pageEP421 has the same quantifiers and records an affirmative answer. No conclusion is being drawn about the different arbitrary-subset-product or pair-product questions.

Jia1996, Acta Arithmetica76(1),21–84, actual first-page theorem: for a sufficiently large fixed B and a sufficiently small fixed epsilon>0, apart from O(Y(log Y)^(-B)) positive integer starts n in (Y,2Y), the interval (n,n+n^(1/20+epsilon)) contains at least .005 n^(1/20+epsilon)/log n primes. This is an integer-start exceptional-set theorem and is unconditional in the displayed statement. Choose a compatible B>2 and epsilon<1/100 small enough for that theorem. Let eta=1/20+epsilon and theta=3/50, so eta<theta<1. No particular numeric epsilon is asserted to meet an unstated lower threshold. The64-page proof is imported as published background, not rederived here.

CCDN2020, Algebra&NumberTheory14(8),2261–2294, actual Theorem3 printed2264/PDF5: for fixed ambient n>1, one constant c(n) works for every degree d>0, integral affine curve overQ, and B>=1, with at most c(n)d^3 B^(1/d)(log B+d) integer points of coordinate height<=B. In particular the geometrically integralQ-defined plane curves used below satisfy its hypotheses, with n=2 fixed. There is no coefficient-height hypothesis or hidden fixed-degree constant. The nearby coefficient-size variant is not substituted for this theorem. Its full published determinant-method proof is imported. Standard additional facts are Bertrand's postulate, Euclid's lemma, polynomial factorization overQbar, elementary Galois descent and the plane-curve Bézout intersection bound.

## Stable greedy set and collision witnesses

Start with {2}. At consecutive primes p<q, test the existing set through p together with every integer p+1,...,q. Keep all of this if every two distinct consecutive-block products differ; otherwise keep only q. Each decision is a finite test. Every prime is kept and every open gap is either retained entirely or deleted entirely. No future step inserts an integer below its current prime endpoint, so decisions and surviving adjacencies remain stable.

Normalize any collision by cancelling an overlap. Containment would leave a nonempty product of numbers>=2 equal to1, so cannot occur. Otherwise cancellation leaves nonempty separated consecutive blocks E,R, all E-elements smaller than all R-elements, with equal products. R cannot contain a prime t, since t would have to divide some earlier element strictly below t. If this is a new collision at(p,q), R cannot be wholly old, and crossing the old/new boundary would put p in R. Thus R is a full integer interval [m,n] strictly inside(p,q). If E crossed that boundary, p would divide a member of[m,n], impossible because q<2p. E is therefore either a block of the established prefix or a full current-gap interval. Its length r is greater than the right length s: if r<=s, pairing r strictly smaller factors against later ones, with remaining later factors>=2, makes equality impossible.

If the tentative gap is rejected, adding q alone remains collision-free: any new normalized later block must include the terminal prime q. Induction establishes all prefixes and the infinite union A as collision-free. Any two finite blocks of A occur with all their intervening elements already fixed in a sufficiently late prefix.

Call a rejected gap raw if some normalized witness E crosses no earlier rejected gap, where crossing means containing both boundary primes of that earlier gap. Such E is a full numerical interval. Indeed, an old missing integer between E's endpoints belongs to a wholly deleted gap, whose retained boundary primes must both occur in the consecutive block E. A witness inside the current gap is already numerical. For a nonraw gap, E must instead be an old block, and it crosses some earlier rejected gap; choose one as its parent. Parent right endpoints strictly decrease backwards. Each nonraw vertex has exactly one chosen parent, so ancestry is finite and ends at a raw vertex. Raw E need not survive the rejection of its own current gap; only nonraw E is used as a stable final-A block. This distinction avoids an invalid universal witness-stability premise.

## Long gaps: integer starts control total length

Take p in[Y,2Y) and g=q-p>p^theta. Bertrand gives q<4Y. Every integer a in(p,q) except the last O(Y^eta+1) satisfies a+a^eta<q. Those disjoint per-gap starts have prime-free intervals and therefore belong to Jia's exceptional set. Since eta<theta, a long gap supplies at least g/2 such starts uniformly for all sufficiently large Y. They all lie in(Y,4Y); apply Jia on(Y,2Y) and(2Y,4Y), absorbing the at-most-one boundary integer. Thus the total length of long gaps on this scale is O(Y(log Y)^(-B)). This estimates lengths, not only the number of gaps, and it never replaces integer counts by a real-measure estimate.

Gaps starting below sqrt(X) have disjoint interiors and end before2sqrt(X), so their total length is O(sqrt(X)). Sum the remaining dyadic bands: their logarithms are comparable to log X and their Y-values sum to O(X). Hence all long gaps with left endpoint<=X have total length

    O(sqrt(X)+X(log X)^(-B)) = o(X).

Small gaps, integer endpoints and a gap straddling X are included by fixed constants and the same length bound.

## Raw short gaps: every absolute component has degree at least two

Let r>s>=1 and let

    F(U,V)=product_(i=1..r)(U-a_i)-product_(j=1..s)(V+b_j),

with arbitrary integer shifts, not necessarily distinct. Set h=gcd(r,s), u=r/h, v=s/h. The weights wt(U)=v, wt(V)=u give initial form U^r-V^s. OverC this is the squarefree product of the h binomials U^u-zeta V^v, zeta^h=1. Since gcd(u,v)=1, the vector(u,-v) is primitive: a GL2(Z) monomial change in the Laurent ring sends U^u V^(-v)-zeta to a variable minus a nonzero constant. It is irreducible there and hence inC[U,V], since no nonconstant monomial divides the binomial. Coprime reduction is essential.

Weighted initial forms multiply, and all weights are positive. Thus the initial form of any nonconstant absolute irreducible factor H is a scalar times a product of e>=1 distinct such binomials. It contains U^(ue), has weighted degree uve, and every monomial U^i V^j in H satisfies vi+uj<=uve. As u>v, v(i+j)<=vi+uj, giving i+j<=ue. The pure U monomial attains that degree. Therefore deg H=ue>=u>=2. A repeated factor of F would give a repeated nonconstant factor of its squarefree initial form, so F itself is squarefree. Its total degree is r; absolute component degrees d_i therefore sum to r.

Apply CCDN to each absolute component defined overQ. For a component not defined overQ, normalize a defining polynomial overQbar. Some Galois automorphism moves it to a distinct component; every rational point on it also lies on that conjugate, because its coordinates are fixed. Bézout gives at most d_i^2 such points for that component. Summing these valid overcounts gives <=sum d_i^2<=r^2. No assumption that every absolute factor is rational is hidden here.

For X>=2, every d_i>=2, sum d_i^3<=r^3 and sum d_i^4<=r^4. The uniform coefficient/degree result therefore yields

    #{integer (x,y) in[-X,X]^2:F(x,y)=0}
      <= C X^(1/2)(r^3 log X+r^4),

including the non-Q exceptional contribution in the same bound. This is why a nonuniform fixed-degree Bombieri-Pila citation would be insufficient, but the authenticated CCDN theorem suffices.

For a raw short gap ending at mostX, both witness sides are full numerical intervals. Write their product equality as

    product_(i=0..r-1)(x-i)=product_(j=0..s-1)(y+j),

where positive x,y<=X. Shortness gives s<=X^theta. Since all earlier entries>=2 and all later entries<=X, 2^r<=X^s, hence r<=L=ceil(X^theta log_2(2X)). Summing the last bound over s<r<=L overcounts all possible witnesses and gives

    R(X) <= C X^(1/2)(L^5 log X+L^6)
          <= C X^(1/2+6theta)(log(2X))^6.

Each numerical right interval is contained in at most one prime gap. Choosing one raw witness per gap therefore injects gaps into the counted witness data; witness multiplicities cannot invalidate the upper bound. No irreducibility, genus or exceptional-shift classification is left unsupported.

## Parent edges and contraction

Suppose parent(p,q), length g, is crossed by an old witness E for a child, with right interval[m,n] and length s. Both primes p,q divide productE and hence product[m,n]. Thus ap,bq lie in[m,n] for integers a,b>=2. Call the edge equal when some common multiplier j has jp,jq both in[m,n]; fix one such label. Otherwise every such a,b is unequal and |ap-bq|<=s-1. If a>b,

    p<=(a-b)p=(ap-bq)+bg<=s-1+bg<=s+ng/p.

This uses no unjustified sign for ap-bq. If a<b, bq-ap=(b-a)p+bg>=p, so p<=s-1. Both cases give

    p^2 <= ng+ps.                                             (A)

For children ending<=X, the following bounds use only fixed constants.

* A fixed rejected parent has at most C X^(3theta)(log(2X))^2 short children. Its p,q are adjacent forever in final A. A consecutive r-block crossing that adjacency has at most r-1 positions. Once E and s are fixed, the product of m,...,m+s-1 is strictly increasing in positive integer m and determines at most one right interval, hence at most one child. Sum over r<=L and s<=X^theta. Counting all these blocks in one stable A is legitimate for nonraw witnesses.
* If parent and child are short and their edge unequal, (A) gives p^2<=X p^theta+pX^theta. Either p<=2X^theta, or absorb the latter term to obtain p^(2-theta)<=2X. With rho=1/(2-theta)=50/97 and Bertrand, q<=C0 X^rho, C0 fixed. There is no witness-dependent contraction constant.
* Possible long unequal parents number O(X^(1-rho)log(2X)). The p<=2X^theta cases contribute O(X^theta), absorbed since theta<1-rho. Otherwise(A) gives g>=p^2/(2X), and longness gives g>p^theta. For p comparable toP, disjoint gaps lie in an interval of length O(P), so their number is at most C min(P^(1-theta),X/P). Split at P=X^rho, where rho(1-theta)=1-rho, and sum O(log X) bands. This overcounts all possible long parents and so covers selected ones.
* Equal edges cannot go from long to short. For child gap(P,Q), P<jp<jq<Q, so Q-P>jg. Longness would imply Q-P>jp^theta=j^(1-theta)(jp)^theta>P^theta, contradicting the child's shortness. The exclusion is exact, not a finite-data observation.

## Compress equal chains, including branching

Fix a starting gap(p,q), g=q-p. Multiply the integer labels on a path of equal edges to get J. Inductively the final gap contains both Jp,Jq: an equal edge contains multiples of its parent's two endpoints and thus all integers between those multiples. For fixedJ, at most one prime gap can contain Jp,Jq. Distinct terminal vertices can therefore be assigned distinctJ even if many paths/factorizations have the same product. Independent branching is neither assumed nor multiplied.

A terminal short gap ending<=X has length>Jg but <=X^theta. Thus its nonempty equal-chain endpoints number at most floor(X^theta/g), and including the start the closure has at most1+X^theta/g<=2X^theta. No depth bound is needed for this compression.

Let N(X) count all short rejected gaps ending<=X. From each terminal vertex trace backwards through its maximal final run of equal edges, allowing an empty run, to a vertex w. Every vertex of this run is short by the no-long-to-short exclusion. Exactly one case applies: w is raw; w has an unequal short parent ending<=C0 X^rho; or w has one of the long unequal parents just counted. There is no missing long raw root followed only by equal edges, nor an infinite backward run, since ancestry endpoints strictly decrease. Multiply the bounds for each possible w by its equal closure. Writing l=log(2X) and increasing one fixedC gives

    N(X) <= C X^(1/2+7theta) l^6
          + C X^(4theta) l^2 N(C X^rho)
          + C X^(1-rho+4theta) l^3.                            (B)

This one-step recurrence covers all histories and safely overcounts multiple representations, without the source manuscript's variable-depth multiscale estimate.

## Close the recurrence and handle boundary gaps

Set alpha=93/100. Exact exponents are

    raw with equal closure =23/25 < alpha,
    recursive =4theta+rho alpha=3489/4850 < alpha,
    long-parent =1-rho+4theta=1757/2425 < alpha,
    alpha+theta=99/100<1,   rho<1.

The three margins are respectively1/100,2043/9700,1993/9700. Choose a fixed large threshold where C X^rho<X, the nonrecursive terms divided by X^alpha sum to<=1/2, and C^(1+alpha)X^(4theta+rho alpha-alpha)l^2<=1/2. Strict negative powers absorb the logarithms. Increase the threshold if needed for an integer rounding margin. Choose K>=1 to bound the finitely many earlier N(n)/n^alpha. Strong induction on integerX, with t=floor(C X^rho)<X and N(C X^rho)=N(t), gives N(X)<=K X^alpha. This avoids any ambiguity from ceiling the recursive argument. RealX follows from integer endpoints. Constants are fixed before induction.

Each short rejected gap ending<=X has length<=X^theta, so their total length is O(X^(99/100))=o(X). A gap meeting[2,X] has p<=X and q<2p<=2X, so partially intersecting boundary gaps are controlled by applying the short bound at2X and the long bound with left endpoints<=X. Apart from1, A omits only rejected interiors. Thus

    #[1,X]\A <=1+O(X^(99/100))+O(sqrt(X)+X(log X)^(-B))=o(X).

A has natural density one, is infinite and has a strictly increasing positive-integer enumeration. Its all-block injectivity was proved separately for every finite pair, without bounded lengths or computational extrapolation.

## Prior scope and diagnostic limits

Chojecki's public Ulam5-page manuscript states this exact full theorem and supplies the construction/witness/curve/forest mechanisms. The authenticated arXivv1 body supplies the same result and mechanisms. This audit verifies the weaker deletion rate using Jia and(B), so it does not certify the source9/10 exponent, Li's newer prime theorem, every source sentence, or any Lean artifact. The stronger source rate is unnecessary to identify its full density-one result as prior. No exclusive first-priority claim among the other independently credited contemporary solutions is made.

Independent finite checks use actual greedy construction through211, exact witness cancellation, every finalized prefix, stable parent blocks, prime-multiple interval configurations, primitive weighted-degree data and exact exponent margins. Actual small prime gaps have no nonempty short child, and the actual selected forest has no equal chain. A separately labelled nonvacuous synthetic disjoint-integer-interval model tests equal-chain containment/multiplier merging; it is not asserted to consist of prime gaps or actual multiplicative witnesses. Concrete mutations reinserting an old rejected gap and retaining1 restore collisions; polynomial and parameter counterexamples test missing hypotheses. Finite evidence supplements the analytic proof and does not prove the asymptotic bound or external theorems. This AI-assisted audit is not formal proof-assistant certification or independent human peer review.
