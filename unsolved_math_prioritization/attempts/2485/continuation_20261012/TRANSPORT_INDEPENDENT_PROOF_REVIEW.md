# Independent audit of the EP1095 exact transport results

Audit date: 12 October 2026 UTC.

## Decision and frozen scope

**Accept corrected candidate v2 as an exact structural partial result. Do not accept candidate v1 as written.** The quotient-lcm identity, complete smooth-part criterion, composite valuation defects, filtered boundary transport, and stated finite boundary minima are correct. V1 contained a genuine missing-domain error in its fifth first-minimum consequence. V2 repairs it by requiring the existential witness to satisfy n>K+1. No asymptotic successive-ratio theorem, new growth bound, or literature-priority claim is accepted or asserted.

The complete corrected proof is distributed as `EXACT_TRANSPORT_v2.md`: 10,445 bytes, SHA-256 `213e231e2154b56dbe3b72b889c40d02b9e4d19b60602146ec97a1b4862b375a`. The complete rejected historical proof is distributed as `EXACT_TRANSPORT_v1_SUPERSEDED.md`: 10,749 bytes, SHA-256 `3dd822b0a112e13af94a0bfb960682a0944586ef71c6cfcca2488ee36f063470`. These identities describe the public editions. Their mathematical arguments are preserved in full; diagnostic-reference redactions and the historical-version warning do not alter the reviewed arguments.

The audit read the prior `ACTUAL_MINIMUM_PARTIALS.md` and `SOURCE_CORRECTION.md`, and does not replace their distinction between full survivors and lower-digit sieve candidates. Numerical assertions about previously certified g(k) retain that provenance unless explicitly reverified below.

## Definitions and boundary cases

For n>=k>=1, A_k(n) means that every prime p<=k is absent from C(n,k). Define s_k(x) as the product of the prime powers in x whose primes are at most k, for positive x. The actual minimum is g(k)=min{n>k+1:A_k(n)}. A positive integer is k-rough when its smooth part is 1, including the integer 1 itself.

These domains matter:

- For k=1 the forbidden-prime set is empty; A_1(n) holds for every n>=1 and g(1)=3.
- At n=k, C(k,k)=1, so A_k(k) always holds.
- At n=k+1, C(k+1,k)=k+1. In particular this excluded value survives whenever k+1 is prime.
- For k=2 the first permitted survivor is 6: C(4,2)=6 and C(5,2)=10 fail, while C(6,2)=15 passes. Thus g(2)=6.
- Composite K is at least 4. Its forbidden-prime set is the same as that for K-1. This equality is essential and must not be silently used when K is prime.

## Independent proof of the quotient-lcm identity

Write c_j=k C(k-1,j), for 0<=j<k, and q_j=(n-j)/gcd(n-j,c_j). Every numerator and denominator here is positive because n>=k.

The integral identity

c_j C(n,k)=(n-j) C(n,j) C(n-j-1,k-j-1)

implies q_j divides C(n,k). Hence Q=lcm_j(q_j) divides C(n,k).

For the reverse divisibility, take P(x)=product_{i=0}^{k-1}(x-i). Its simple roots give the partial-fraction identity

1/P(x)=sum_{j=0}^{k-1} 1/[P'(j)(x-j)],

where P'(j)=(-1)^(k-1-j) j! (k-1-j)!. This identity also follows by multiplying by P(x): the resulting degree-at-most-k-1 polynomial is 1 at each of the k roots. Evaluating at n and multiplying by k! gives

1/C(n,k)=sum_{j=0}^{k-1} (-1)^(k-1-j) c_j/(n-j).

Each rational c_j/(n-j) has reduced denominator q_j. Consequently Q/C(n,k) is an integer. This proves C(n,k) divides Q, and therefore

C(n,k)=lcm_{0<=j<k} (n-j)/gcd(n-j,c_j).

This proof is independent of the candidate's maximum-valuation argument, Lucas's theorem, and any numerical testing. The alternating sign is part of the identity; omitting its k-dependent orientation would be wrong for even k.

The candidate's proof also checks out. For fixed p, choose j maximizing a=v_p(n-j). Since any p^(a+1) consecutive integers contain a multiple of that power, k<p^(a+1). Therefore v_p(i-j)<=a for i!=j. When that valuation is below a, the valuation of n-i equals it. When it equals a, the valuation of n-i is at least a and cannot exceed the chosen maximum, so it is exactly a. Summing gives v_p(C(n,k))=a-v_p(c_j), a nonnegative number. Every other reduced quotient has valuation at most that number, proving the same lcm identity prime by prime. This includes primes absent from the interval, k=1, and n=k.

## Full smooth-part equivalence and coefficients

The lcm is k-rough if and only if each q_j is k-rough. At any prime p<=k this says v_p(n-j)<=v_p(c_j), which is equivalent to s_k(n-j) dividing c_j. Thus the criterion is genuinely necessary and sufficient for every factor. Equivalently, n must avoid j modulo p^(v_p(c_j)+1), for every j and p<=k. These are full valuation conditions, not only lower-digit conditions.

The coefficient bound c_j|L_k is correct. For Q=p^r the corresponding Legendre summand is

floor(k/Q)-floor(j/Q)-floor((k-1-j)/Q).

Writing k=j+(k-1-j)+1 shows that this is 0 or 1; it vanishes for Q>k. Hence its sum is at most floor(log_p k). The stronger identity lcm_j(c_j)=L_k is the established binomial-row lcm identity of Farhi, and is correctly credited rather than claimed as new. None of these coefficient facts turns a density into an estimate for the first survivor.

For k=1 the sole coefficient is 1 and the sole quotient is n, exactly C(n,1). At n=k the lcm is 1; equivalently, k-j divides c_j because c_j=(k-j) C(k,j). No zero valuation or undefined binomial coefficient appears at this boundary.

## Endpoints and composite valuation defects

The endpoint coefficients are both k, yielding d=s_k(n)|k and e=s_k(n-k+1)|k. A prime dividing both d and e would divide k and the difference k-1, which is impossible. Thus gcd(d,e)=1. Dividing the endpoints by their full smooth parts gives the stated k-rough u and v and d*u-e*v=k-1.

These endpoint restrictions alone are not sufficient. At (k,n)=(3,5), the endpoints have smooth parts 1 and 3, but the middle factor has smooth part 4, which does not divide c_1=6; C(5,3)=10 fails. At (4,10), the endpoint smooth parts are 2 and 1, yet C(10,4)=210 fails.

Now let K be composite and assume A_K(n). In the two exact identities

C(n-1,K-1)=K C(n,K)/n,
C(n,K-1)=K C(n,K)/(n-K+1),

the small-prime valuations of C(n,K) vanish. Taking each prime p<=K-1 yields the exact smooth parts K/d and K/e. Both quotient values are integers by the endpoint restrictions. The first predecessor survives precisely when d=K, and the second precisely when e=K. These are equivalences under the explicit hypothesis A_K(n), not unconditional assertions about arbitrary n.

When K=p^a with a>=2, d=p^r and e=p^s for 0<=r,s<=a, with min(r,s)=0. Thus the exact predecessor defects are p^(a-r) and p^(a-s); at least one equals the full p^a. This remains correct at n=K: the predecessor binomial coefficients are 1 and K. It also shows why transporting the prime argument unchanged to a composite parameter is invalid.

## Exact composite boundary transport

Let m>=K-1 satisfy A_{K-1}(m). Since every prime factor of composite K is <=K-1, integrality of

C(m+1,K)=(m+1) C(m,K-1)/K

forces v_p(m+1)>=v_p(K) for every p|K. Hence K|(m+1). This lattice fact is already in the cited literature and is not new here.

For m=Kt-1 and t>=2, the exact identities are

C(Kt-1,K)=(t-1) C(Kt-1,K-1),
C(Kt,K)=t C(Kt-1,K-1).

The factors are positive integers, so the product is K-rough exactly when both factors are. Because K is composite, the old and new forbidden-prime sets agree. These observations prove both directions of both claimed equivalences, including the necessary roughness tests on t-1 and t. The old-survivor hypothesis cannot be omitted, and the roughness filters cannot be omitted. For example, K=6,m=23,t=4 has an old survivor, but neither 23 nor 24 survives at K=6 because the multipliers 3 and 4 fail.

The restriction t>=2 ensures these boundary candidates are past the excluded small values: Kt-1>=2K-1>K+1 for composite K>=4. For an arbitrary admissible boundary candidate n>K+1, the associated old point is m=n if n is -1 modulo K, and m=n-1 if n is 0 modulo K; both satisfy m>K and so are in the actual defining domain for g(K-1).

## Every first-minimum consequence checked

Let b(K) be the least actual K-survivor in residues 0 and -1 modulo K. Its existence can be proved directly using the all-factor criterion. Put M=L_K product_{p<=K}p and n=hM-1 for sufficiently large positive h. For 0<=j<K and p<=K, the valuation of n-j equals that of j+1, since v_p(hM)>v_p(j+1). As c_j=(j+1) C(K,j+1), the smooth part of n-j divides c_j. Thus A_K(n), n is -1 modulo K, and n>K+1.

1. Every boundary survivor yields an actual old survivor m<=n. Therefore b(K)>=g(K-1).
2. The lattice result makes t0=(g(K-1)+1)/K an integer at least 2. If t0-1 is K-rough, the old minimum itself survives at K. Therefore b(K)<=g(K-1), and the first inequality forces equality. In particular g(K)<=g(K-1).
3. If t0 is K-rough, g(K-1)+1 is a permitted boundary K-survivor. Hence b(K)<=g(K-1)+1 and g(K)<=g(K-1)+1.
4. If g(K)<g(K-1), this new minimum cannot be in the two boundary residues by point 1. For any K-survivor, d=K is equivalent to K|n: one direction is immediate; for the other, K|n and d|K imply d=K because every prime factor of K is small. Likewise e=K is equivalent to n=-1 modulo K. Thus interior residue is equivalent to both endpoint smooth parts being proper divisors of K. This is not a converse asserting that every interior survivor is smaller than the old minimum.
5. Fix real R>=1. If g(K)<g(K-1)/R, then its value is an interior survivor by point 4 and satisfies K+1<g(K)<g(K-1)/R. Conversely, an interior K-survivor satisfying K+1<n<g(K-1)/R is a permissible competitor, so g(K)<=n<g(K-1)/R. This proves v2's exact equivalence. The lower inequality is indispensable.

The parity observation after these consequences is correct: for t0>=3 one of t0-1 and t0 is an even integer at least 2, so at most one boundary filter passes. At t0=2 the integer 1 passes while 2 fails; retaining 1 as rough creates no invalid candidate. None of these facts provides an unconditional small bound on how far one must search for a filtered old survivor.

For prime q, the same predecessor identities instead have v_p(q)=0 for p<q. Nonnegativity forces both endpoints to be free of primes below q and both old binomial coefficients to survive. For n>q+1, n-1>q is a permitted competitor for g(q-1), proving g(q)>=g(q-1)+1. Conversely, the left old-survivor and endpoint conditions settle exactly the primes p<q; the separate q-adic condition n modulo q^2>=q is still needed. No leading-digit filter has been suppressed. The case q=2 also satisfies the inequality, with the old forbidden-prime set empty.

## Frozen correction history

V1's consequence 5 permitted an interior A_K-survivor below g(K-1)/R without requiring n>K+1. Set K=4, R=1, and n=5. Then C(5,4)=5 is 4-rough, 5 is 1 modulo 4, and 5<g(3)=7. Nevertheless g(4)=7, so g(4)<g(3) is false. The two actual minima are independently exact: for k=3 the permitted n=5,6 fail and n=7 passes; for k=4 the first permitted n=6 fails and n=7 passes. This is a counterexample to the frozen text, not merely an editorial preference.

The author preserved v1 and produced a separate v2. The proof diff consists of the explicit lower bound in consequence 5 and the verification-record count increasing from six to seven negative controls. The mathematical core is unchanged. The audit accepts only this corrected full v2. `TRANSPORT_CORRECTION_HISTORY.md` records the actual counterexample, correction and decisions.

## Independently written finite checks

An independent exact-arithmetic checker was written for this audit without importing, executing, or copying the author's search or verification implementation. Its reference survival test uses Python's exact `math.comb` and gcd with the primorial. It uses explicit exceptions rather than assertions, so optimization cannot remove its checks.

In normal, -O, and -OO modes, the checker produced byte-identical diagnostic results:

- 260,128 complete pairs n>=k, 1<=k<=64, n<=4096, checking the quotient-lcm identity, full smooth-part equivalence, and forbidden congruence system
- 483,644 independently evaluated maximum-valuation witness equations
- 2,796 exact rational partial-fraction identities
- 8,623 endpoint tests, 1,521 composite-defect survivors, and 1,060 prime-power survivor checks
- 73,209 prime-transport equivalences, 1,130 old-survivor lattice tests, and 16,506 composite boundary equivalences
- 50 corrected first-minimum ratio equivalences, nine boundary-minimum consequences, seven prime first-minimum comparisons, and all 64 coefficient rows
- Thirteen exhaustive boundary-minimum certificates, rejecting every one of 135,564 smaller integers in the specified boundary classes and accepting all thirteen reported minima
- Seven negative controls, including endpoint-only shortcuts, dropped multiplier filters, the actual-minimum exclusion, the frozen-v1 defect, and altered boundary minima

The boundary values are 7, 71, 143, 269, 319, 719, 3374, 2096, 17819, 395225, 88479, 2239, 1507967 for K=4,6,8,9,10,12,14,16,18,25,27,28,32 respectively. Exact boundary enumeration uses neither a Lucas criterion nor the quotient-lcm theorem. This independently supports their minimality, not just admissibility.

All 46 prior g(k) witnesses were independently retested by exact binomial gcd, and all 21 actual minima found completely within the audit's n<=4096 grid agree with the prior file. This audit does not freshly recertify the global minimality of the other prior g(k) entries; those retain their earlier separate certificates. The selected table's g-values match those prior data and its b-values are independently certified here.

## Primary-source credit and limitations

The audit independently opened the primary [Lukes, Scheidler and Williams paper](https://cspages.ucalgary.ca/~rscheidl/Papers/es.pdf) and inspected printed p.1715, including a local rendered image. It states the composite lattice and attributes its speed-up to earlier work. The candidate's credit is appropriate. The prior filter correction is not used to discredit that lattice, the implementation, or the numerical tables. No source-author software was run.

[Farhi's binomial-row lcm paper](https://arxiv.org/pdf/0906.2295v2), Theorem 1, gives the coefficient-row identity after reindexing. [Farhi's interval-lcm paper](https://arxiv.org/pdf/0803.0290), Theorems 11-12 and the latter proof on preprint pp.14-15, contains related interval divisibility and an integral product-of-binomials argument. These are relevant antecedents, correctly distinguished from the complete quotient-lcm identity proved in this packet.

This was a targeted check of those sources. It is not a comprehensive priority search and cannot establish that the exact identity or its application is new. No copied source document, page image, or source-text excerpt is included in the public audit materials; the source-inspection record contains bibliographic facts and retrieval/inspection metadata only.

## Accepted result and remaining problem

The corrected packet supplies an exact all-factor obstruction system and separates the composite boundary layers from potential new interior minima. It also gives valid finite demonstrations that a first boundary survivor can be much later than the actual first survivor. These are structural and computational partial results. They neither imply the unbounded upper successive-ratio conjecture nor the vanishing lower successive-ratio conjecture, and do not compare first hits to reciprocal density. No proof of the original open problem is present.
