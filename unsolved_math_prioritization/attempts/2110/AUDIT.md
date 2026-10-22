# Independent audit: density-one distinct consecutive products

## Verdict and exact scope

**ACCEPT the frozen reconstruction as a complete proof of the stated density-one existence theorem, conditional only in the ordinary sense of using the explicitly identified published/standard theorems below.** No mathematical correction to the frozen candidate is required. The proof is not established by the finite checks; those are independent supplementary tests.

Target: problem ID 2110 / EP-421. There exists an increasing sequence of positive integers of natural density one such that the products of every two distinct nonempty consecutive index blocks are different. Starting the sequence at 2 is allowed by the original condition that its first term be at least 1.

The retained-prime construction, witness organization, split-product argument, and parent forest are credited to Przemek Chojecki, *Distinct Consecutive Products*, dated 13 July 2026, https://ulam.ai/research/erdos421-sol.pdf. Its first-page footnote attributes discovery of the proof to GPT-5.6 Sol, iterating on the author's previous attempts. This audit gives no novelty credit to the reconstruction, makes no peer-review-status assertion, and does not certify the sharper exponent or every argument in that manuscript. In particular, its multiscale forest summation is not needed here: the frozen reconstruction supplies a separate one-step recurrence, checked below. Li's newer prime-interval preprint is not an input to the audited proof.

The candidate and all four frozen source files were independently hashed and matched before inspection. None was modified. The exact byte counts and SHA-256 values are listed at the end and in `SOURCE_PINS.json` and `INPUT_PIN_CHECKS.json`.

## Source inspection and imported theorem scope

### Original question

Erdős and Graham, *Old and New Problems and Results in Combinatorial Number Theory* (1980), printed p.84, PDF page 80, was independently rendered and inspected. Its question is exactly density one and distinct products over all nonempty consecutive index blocks, not merely adjacent pairs, bounded block length, or unequal-length blocks. Source: https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf.

### Prime intervals

Chaohua Jia, *Almost all short intervals containing prime numbers*, Acta Arithmetica 76 (1996), 21–84, first-page theorem, printed p.21/PDF page 1, was independently extracted, rendered, and inspected. Source: https://matwbn.icm.edu.pl/ksiazki/aa/aa76/aa7613.pdf.

For a sufficiently large fixed positive constant B and sufficiently small fixed positive epsilon, all sufficiently large X have at most O(X(log X)^(-B)) exceptional **positive integers** n in (X,2X); outside that set, the interval (n,n+n^(1/20+epsilon)) contains at least 0.005 n^(1/20+epsilon)/log n primes. In particular it contains a prime once n is sufficiently large. This is a count of integer starts, not a Lebesgue-measure assertion, and directly supplies what the gap argument needs.

Choose a compatible pair of fixed constants with B>2 and 0<epsilon<1/100 sufficiently small for this theorem. Equivalently one may first select a sufficiently large B and then decrease epsilon if the theorem requires that. Put eta=1/20+epsilon<3/50. All implied constants and lower thresholds may depend on this fixed pair; they do not depend on a prime gap or on the counting parameter X. The 64-page sieve proof is imported, not re-proved in this audit.

### Uniform affine-curve points

Wouter Castryck, Raf Cluckers, Philip Dittmann, and Kien Huu Nguyen, *The dimension growth conjecture, polynomial in the degree and without logarithmic factors*, Algebra & Number Theory 14 (2020), 2261–2294, Theorem 3, printed p.2264/PDF page 5, was independently extracted, rendered, and inspected. Source: https://msp.org/ant/2020/14-8/ant-v14-n8-p09-s.pdf.

Its quantifiers provide c=c(n) for every degree d>0, every integral affine curve in affine n-space over Q, and every height bound H>=1, with integer-point count at most c d^3 H^(1/d)(log H+d). We use only n=2 and geometrically integral components defined over Q, a subclass satisfying the hypothesis. Thus c is a single absolute constant, independent of both the coefficients and d. No fixed-degree-only bound, hidden coefficient-height condition, or uniformity in an unbounded ambient dimension is being substituted. Components not defined over Q are dealt with separately by Galois conjugacy and Bézout. The published determinant-method proof is imported, not re-audited in full.

The remaining imported facts are Bertrand's postulate, unique factorization/Euclid's lemma for integers, standard factorization and Galois descent over Q, and the plane-curve Bézout inequality. The essential weighted-binomial argument is proved explicitly below.

Attempts to refresh the four source URLs with the web-reading tool did not return inspectable PDFs: Jia returned 403, the UCSD PDF timed out, Ulam was inaccessible through that tool, and MSP returned an empty HTML extraction. These failures are not treated as successful retrievals. The audit's source inspections use the existing exact, hash-verified PDF bytes, including independently generated page images. No claim about live-site status follows from the failures.

## Complete independent proof audit

Set theta=3/50, rho=1/(2-theta)=50/97, alpha=93/100. A prime gap (p,q), where p<q are consecutive primes, is short when q-p<=p^theta and long otherwise.

### 1. Construction, cancellation, and stable witnesses

Begin with A_2={2}. For the next prime q after p, tentatively adjoin every integer from p+1 through q. Keep this tentative set if its nonempty consecutive-block products are all distinct; otherwise adjoin q alone. This is a well-defined finite test at every stage. Every prime is retained; every open prime gap is retained or removed in its entirety. Future stages add only larger integers, so all earlier retention decisions and retained adjacencies remain fixed.

In an equality between two distinct block products, a containment of one index block in the other is impossible: cancellation would give a product of at least one integer >=2 equal to 1. In the remaining overlapping case, cancellation leaves two nonempty, disjoint, ordered consecutive subblocks E and R with equal products. Disjoint original blocks already have this form. Every element of E is smaller than every element of R.

The later block R cannot contain a prime t: Euclid's lemma would make t divide an earlier entry, each of which is smaller than t. Suppose a collision arises in the tentative step (p,q), while the established prefix is collision-free. If R were wholly in the old prefix, E would also be in it. If R met both old and new entries, its consecutiveness would force p into R. Both possibilities are impossible. Therefore R is a full numerical interval [m,n] inside (p,q).

If E met both the old prefix and new interior, it would contain p. Equality would then force p to divide an integer strictly between p and q. Bertrand gives q<2p, so there is no such multiple. Hence E is either a block of the established prefix or a full numerical interval inside (p,q). Writing r=|E| and s=n-m+1, we have r>s. Indeed, if r<=s, pairing the r earlier factors with any r later factors already gives a strictly smaller product, and any remaining later factors are at least 2.

If the tentative step is rejected, adjoining the single terminal prime q cannot cause a collision: its normalized later block would contain q, again impossible. Thus induction proves each A_p collision-free. Their union A is collision-free because any two finite blocks in A occur, with the same intervening elements, in a sufficiently long prefix.

Call a rejected gap raw if there is a witness whose E crosses no earlier rejected gap, where crossing means containing both boundary primes. Such E is a numerical interval. If a missing integer lay between its first and last elements, it would lie in the interior of an earlier rejected gap; since the block's endpoints are retained and it is consecutive in the established prefix, it would necessarily contain both boundary primes of that gap. This contradicts rawness. The alternative E inside the current gap is already a numerical interval.

Choose a raw witness for every raw gap. For a nonraw gap, choose any witness and one earlier rejected gap crossed by E as its parent. In this case E is necessarily a block of the established prefix, hence also of final A. Parent right endpoints strictly decrease when followed backward, so every backward chain is finite and terminates at a raw vertex. Each nonraw vertex has exactly one chosen parent. This is the precise forest used below; it does not assume all possible witnesses or parent choices form a forest.

### 2. Long prime gaps have negligible total length

For p in [Y,2Y), Bertrand gives q<4Y. Every integer a with p<a and a+(4Y)^eta<q has a prime-free interval (a,a+a^eta). At least g-O(Y^eta+1) such integers exist, where g=q-p. For a long gap, g>p^theta>=Y^theta. Since eta<theta, for all sufficiently large Y the error is at most g/2, uniformly in the gap. Thus the gap supplies at least g/2 exceptional integer starts.

Different prime-gap interiors supply disjoint starts. All these starts lie in (Y,4Y). Apply Jia to (Y,2Y) and (2Y,4Y); the possible integer start exactly at 2Y costs at most one and is harmless. The total long-gap length with p in [Y,2Y) is therefore O(Y(log Y)^(-B)).

For p<=sqrt(X), the disjoint gaps all end below 2sqrt(X), so their total length is O(sqrt(X)). Cover the remaining p<=X by dyadic bands; their logarithms are comparable with log X, and the sum of their lower endpoints is O(X). Hence

sum_{p<=X, (p,q) long}(q-p) = O(sqrt(X)+X(log X)^(-B)) = o(X).

The argument includes a gap straddling X, counts lengths rather than just the number of gaps, and absorbs the finitely many small gaps into a fixed constant.

### 3. Weighted factors and raw short-gap count

Take r>s>=1 and integer shifts, and write

F(U,V)=product_{i=1}^r(U-a_i)-product_{j=1}^s(V+b_j).

Let h=gcd(r,s), u=r/h, v=s/h. Then u>v, gcd(u,v)=1, and u>=2. Give U weight v and V weight u. The highest weighted form of F is

U^r-V^s = product_{zeta^h=1}(U^u-zeta V^v).

Each binomial is irreducible over C. One explicit proof works in the Laurent ring C[U^±1,V^±1]: the exponent vector (u,-v) is primitive, so an integral change of monomial coordinates takes U^u V^(-v)-zeta to a variable minus a nonzero constant. That element is irreducible. A polynomial factor becoming a Laurent unit would be a monomial, but no nonconstant monomial divides U^u-zeta V^v. Thus irreducibility also holds in C[U,V]. Distinct h-th roots give distinct factors, so the displayed weighted form is squarefree.

Weighted initial forms multiply. Consequently every absolute irreducible factor H of F has initial form, up to a nonzero scalar, equal to a product of e>=1 distinct displayed binomials. No nonconstant factor can have constant initial form because both weights are positive. This also shows F is squarefree. The initial form of H contains U^(ue), with nonzero coefficient. Every monomial U^i V^j in H satisfies vi+uj<=uve. As u>v>0,

v(i+j)<=vi+uj<=uve,

so i+j<=ue. Together with the pure U monomial this proves deg H=ue>=u>=2. This conclusion does not require any classification of the lower-order shifts or of genus.

All absolute components can be taken over Q-bar, and their degrees d_i sum to r, since F has total degree r and is squarefree. For each component defined over Q, apply CCDN with n=2. For a component not defined over Q, normalize a defining polynomial and choose a Galois automorphism taking it to a distinct component. Every rational point on the first is fixed by the automorphism and therefore lies on both. Their degrees are equal; Bézout bounds the number of their intersection points by d_i^2. Summing this valid overcount over all non-Q components gives at most sum_i d_i^2<=r^2. This is uniform even if the components vary with r,s or the shifts.

For X>=2, sum_i d_i^3<=r^3, sum_i d_i^4<=r^4, and X^(1/d_i)<=X^(1/2). The non-Q contribution is absorbed by the same bound. Therefore, uniformly in every shift,

# {integer (x,y) in [-X,X]^2 : F(x,y)=0}
<= C X^(1/2)(r^3 log X+r^4).

For a raw short rejected gap ending at most X, both witness blocks are full numerical intervals. Represent them by their earlier right endpoint x, later left endpoint y, and lengths r>s:

product_{i=0}^{r-1}(x-i)=product_{j=0}^{s-1}(y+j).

Here x,y<=X, s<=X^theta, and 2^r<=X^s, hence r<=L=ceil(X^theta log_2(2X)). Sum the preceding estimate over s<r<=L. This is an overcount, since most such pairs do not encode separated positive intervals or short prime gaps. It yields

R(X)<=C X^(1/2)(L^5 log X+L^6)
<=C X^(1/2+6theta)(log(2X))^6.

A right interval lies in at most one prime gap, so choosing one raw witness per gap gives an injection into the witness collection being counted. No lower bound on the number of witnesses is needed.

### 4. Parent-edge estimates

Let the chosen parent be (p,q), g=q-p, and let the child's right witness be [m,n], length s. Both primes p,q occur in E and q<m. Euclid's lemma provides a,b>=2 with ap,bq in [m,n]. Classify the edge as equal precisely when some j>=2 has both jp,jq in [m,n]; otherwise classify it unequal. Fix one such j for each equal edge, for example the smallest one.

For an unequal edge every chosen a,b is unequal and |ap-bq|<=s-1. If a>b, then

p<=(a-b)p=(ap-bq)+bg<=s-1+bg<=s+ng/p.

If a<b, then bq-ap=(b-a)p+bg>=p, and thus p<=s-1<s. Either case gives

p^2<=ng+ps.                                                     (A)

This proof does not assume the sign of ap-bq in the a>b case.

For children ending at most X, four consequences follow.

1. Fixed-parent out-degree. For a short child, s<=X^theta and r=|E|<=L. The parent primes p,q are adjacent in final A: their open gap was rejected and no later operation inserts integers there. A consecutive r-block of A crossing that adjacency has at most r-1 possible starting indices. Fix one such E and s. The product of m,m+1,...,m+s-1 is strictly increasing for positive integer m, so equality with product(E) permits at most one m. Its interval lies in at most one child prime gap. Thus the number of short children of the fixed parent ending at most X is at most C X^theta L^2<=C X^(3theta)(log(2X))^2. This counts witnesses in a single stable final sequence, not unrelated changing prefixes.

2. Short-parent scale contraction. If an unequal parent is short, (A) gives p^2<=X p^theta+p X^theta. For p>2X^theta, absorb the second term and obtain p^(2-theta)<=2X. For p<=2X^theta, use theta<rho. Bertrand then gives q<=C_0 X^rho, with a fixed C_0 (C_0=4 suffices for X>=1). Neither the contraction exponent nor the constant depends on the witness.

3. Number of possible long unequal parents. All parents have p<X. Those with p<=2X^theta number O(X^theta), which is O(X^(1-rho)) because theta<1-rho. For the others, (A) gives g>=p^2/(2X), and longness gives g>p^theta. On a dyadic band p in [P,2P), all these disjoint gaps lie in [P,4P), so their number is at most C min(P^(1-theta),X/P). If P<=X^rho use the first term; if P>=X^rho use the second. Both are at most C X^(1-rho), using rho(1-theta)=1-rho. There are O(log(2X)) bands. Hence at most C X^(1-rho)log(2X) long parents can be involved. It is harmless that this overcounts gaps not actually chosen as parents.

4. No equal edge from a long parent to a short child. If the child gap is (P,Q), equalness gives P<jp<jq<Q. Therefore Q-P>j(q-p). If q-p>p^theta, then

Q-P>j p^theta=j^(1-theta)(jp)^theta>P^theta,

contradicting child shortness. This exclusion is exact; it does not need a bounded-endpoint exception.

### 5. Equal-chain compression and complete recurrence coverage

Fix a rejected gap (p,q), length g. Along a path of equal edges multiply the fixed edge labels to obtain the positive integer J. Inductively, the terminal prime gap contains Jp and Jq. For the induction, if an intermediate gap (P,Q) contains Jp,Jq, and the next equal edge has label j, then its right interval contains jP,jQ and all intermediate integers, hence contains jJp,jJq.

For a fixed J, at most one prime gap contains both Jp and Jq. Thus different terminal vertices have different J, regardless of possible branching or different multiplicative factorizations of J. If a terminal vertex is short and ends at most X, its gap length is greater than Jg and at most X^theta. Consequently there are at most floor(X^theta/g) such nonempty-path endpoints. Including the starting vertex when relevant, its equal closure has at most 1+X^theta/g<=2X^theta vertices for X>=1. Using a weak floor bound only overcounts an endpoint-equality case.

Let N(X) count all short rejected gaps ending at most X. For each such terminal vertex v, follow its unique parent chain backward through the maximal final run of equal edges, stopping at w. Include the empty run, so w=v is allowed. Every vertex in this run is short, because a long parent cannot have a short equal child. Also q_w<=q_v<=X.

Exactly one of the following three covering cases holds:

- w is raw and short;
- w has an unequal edge from a short parent, which ends at most C_0 X^rho;
- w has an unequal edge from one of the long parents just counted.

There is no missing case: a nonraw w has a parent, and if that edge were equal the backward run would not have stopped. The finite ancestry of the forest rules out an infinite backward run. Raw long roots cannot be followed exclusively by equal edges to v.

Count possible w in these cases using respectively R(X), the fixed-parent short-child bound times N(C_0 X^rho), and that bound times the long-parent count. Multiply by the bound 2X^theta for the equal closure after each w. Enlarging a single fixed constant C and writing l=log(2X), this proves

N(X)<=C X^(1/2+7theta)l^6
      +C X^(4theta)l^2 N(C X^rho)
      +C X^(1-rho+4theta)l^3.                                  (B)

Multiple representations only overcount. No independence among branch choices, bounded forest depth, or control of products of scale-dependent constants is used.

### 6. The recurrence closes

The exact exponent calculations are

- 1/2+7theta=23/25, so alpha-(1/2+7theta)=1/100;
- 4theta+rho alpha=3489/4850, so alpha-(4theta+rho alpha)=2043/9700;
- 1-rho+4theta=1757/2425, so alpha-(1-rho+4theta)=1993/9700;
- rho=50/97<1 and alpha+theta=99/100<1.

All three margins are strictly positive. Choose an integer threshold X_0 large enough that C X^rho<X for X>=X_0, that the first and third terms of (B) sum to at most X^alpha/2, and that

C^(1+alpha) X^(4theta+rho alpha-alpha)(log(2X))^2<=1/2.

These simultaneous choices are possible because powers with strictly negative exponents dominate any fixed logarithmic power. Choose K>=1 large enough to bound N(n)/n^alpha for the finitely many positive integers n<X_0; N(n) is finite even without any estimate.

Induct on integer X>=X_0. Let t=floor(C X^rho), which is less than X. Since prime right endpoints are integers, N(C X^rho)=N(t). The induction hypothesis bounds it by K t^alpha<=K C^alpha X^(rho alpha). Thus the recursive term costs at most K X^alpha/2. The other terms cost at most X^alpha/2<=K X^alpha/2. This proves N(X)<=K X^alpha. Taking integer parts extends the bound to real X. This floor-based presentation also makes the candidate's harmless ceiling/constant convention explicit.

Every short rejected gap ending at most X has length at most X^theta. Therefore their total length is at most X^theta N(X)=O(X^(99/100))=o(X).

### 7. Natural density and all block lengths

Any prime gap meeting [2,X] begins at p<=X and ends at q<2p<=2X. The integers omitted from A in [1,X] consist of 1 and the omitted interiors of rejected gaps. Bound the short rejected gaps by their total full lengths with q<=2X, and bound the long ones by all long-gap lengths with p<=X. Sections 2 and 6 give

|[1,X] intersect (N minus A)|
<=1+O(X^(99/100))+O(sqrt(X)+X(log X)^(-B))=o(X).

This handles the final partially intersecting gap without assuming X is prime or a construction boundary. The floor in the size of [1,X] has no effect on the density limit. Hence A has natural density one. The stable construction in Section 1 proves distinct products for every pair of nonempty consecutive blocks, with no restriction on their lengths. This is the exact affirmative target.

## Independent finite checks and their limitations

An independent exact-check program was written for this audit without importing or executing source-author code or any Lean artifact. It uses exact integer products and rational arithmetic; failures raise exceptions rather than relying on Python assertions.

A full implementation of the tentative whole-gap test through prime 503 retained 391 integers. Of the 95 processed prime gaps, 74 were accepted and 21 rejected. Exhaustive tentative block-product comparison found 46 equality pairs. Normalizing all of them checked the claimed witness locations, numerical-interval right blocks, r>s, no crossing of the current boundary, and the raw-interval characterization. For the deterministic selected forest there were 12 raw vertices and 9 nonraw vertices, all 9 selected edges unequal. The fallback prefix and final prefix were each checked collision-free. Every prime was retained and every rejected boundary pair remained adjacent in the final prefix.

Separately, all numerical intervals inside prime gaps through 503 were compared with every earlier prime gap when both parent primes had multiples in the interval. This produced 3,944 necessary parent-edge configurations: 131 equal and 3,813 unequal. Every unequal configuration satisfied (A), and all common multipliers in the equal configurations satisfied the exact containment/length inequality. These necessary configurations are not falsely claimed to be actual multiplicative witnesses.

There is **one** short prime gap for theta=3/50 through 503: (2,3). Its interior is empty and it is accepted, so there are **no eligible short child gaps** in this range. Consequently the finite no-long-to-short-equal test is vacuous; the algebraic proof above, not that test, establishes the exclusion. There were also no selected equal chains in this particular finite forest. The general compression proof is not inferred from this experiment.

Exact weighted-monomial bounds were checked for all 2<=r<=80, 1<=s<r and all 1<=e<=gcd(r,s), totaling 7,884 cases. This is only a check of the numerical inequalities; the absolute factorization claim is supplied by the Laurent-ring/weighted-initial-form proof. All displayed exponent identities and positivity margins were verified with exact rational arithmetic. All five frozen file pins matched. Aggregate results are recorded in `CHECK_SUMMARY.json`. Detailed retained sets, witnesses, and forests are not part of this public packet.

## Frozen inputs

- Candidate reconstruction: 13,989 bytes; SHA-256 `9b0ffbd4052b58d66aef59de5875e0afe6790adacecbea3d75a294284e9f8a86`.
- Chojecki manuscript PDF: 99,090 bytes; SHA-256 `658fadb960cd8d480a817db5ca425ee5a0c5e2cb701fcf77181cf8efb6ea7508`.
- Jia 1996 PDF: 410,255 bytes; SHA-256 `2e41b7bcfafff731804a5c88210a3d3522a9f9e37e04eecc98aad10aba23cbc5`.
- CCDN 2020 PDF: 1,461,626 bytes; SHA-256 `308b9f1160e3aa7effb74987521a7ad3dd1cab3cbc7d48a5bd7feb922da2111d`.
- Erdős–Graham 1980 PDF: 5,253,644 bytes; SHA-256 `0cbf0c32f0ab1e1c71db5121a88bac905bf976c4a6ab6bb6d7d9cf9ddd184ed3`.

This audit certifies only the authored density-one reconstruction using the stated external theorems. It does not claim manuscript-wide certification, novelty, human review, peer review, or external scholarly acceptance.
