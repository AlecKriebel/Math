# Audit of prior interval matching results for Erdos Problem 711

## Edition and review statement

This AI-assisted authored audit is unrefereed. “Accepted” means a prose proof
check in an independent internal AI audit of the identified prior results,
conditional on the explicitly cited established inputs. It does not mean
external human peer review, journal acceptance, or formal proof-assistant
certification. The underlying van Doorn result is published; Kominers v1 and
Chen--Korsky v2 are arXiv manuscripts whose journal acceptance was not verified.
The results belong to their credited authors. No novelty, priority, exhaustive
literature survey, or current-best-bound certification is claimed.

This edition preserves the complete authored general derivations and substantive
mathematical qualifications. Historical source retrieval, visual inspection,
version checks and finite diagnostics below refer to the October 10, 2026
audit. Edition preparation performed only byte-integrity and publication-
structure checks, with no new scholarly-source retrieval or inspection and
no new mathematical computation. Standard analytic inputs are dependencies,
not reproved here. The minor auxiliary-constant correction in Kominers's
Proposition 4.1 is retained; it is not a main-theorem failure.

Executable code, copied source documents or text, images, raw certificates,
numerical witnesses, datasets and private coordination material are omitted.
Aggregate counts, hashes, match results, public citations and inspection
history are verification metadata. Finite diagnostics are not asymptotic
proof certificates. This is not a formal or executable replay package.

## Conclusion and exact scope

The published proof of Wouter van Doorn's Theorem 1 is accepted: for every sufficiently large positive integer n,

    F(n) - f(n,n) > 0.36 n log n / log log n.

The main theorem of Scott Duke Kominers's arXiv:2607.10431v1 is also accepted as a manuscript theorem, using the verified Hildebrand--Tenenbaum theorems as established analytic inputs:

    liminf [F(n)-f(n,n)]/(n log n) >= 1/e.

The three main theorems of Kaizhe Chen and Samuel Korsky's arXiv:2607.26450v2 are accepted as manuscript theorems:

    F(n) <= n^(4/3) exp(O(log n/log log n)),
    h_P(n) << n^(4/3)/(log n)^(1/3),
    F(n) >= h_P(n) >= n exp(((log 2)/2-o(1)) log n/log log n).

Acceptance here means an independent prose check of the complete proof chains specified below, with the standard cited theorems explicitly identified. It is not a formal proof, journal-referee certification, or claim that every cited analytic theorem has been reproved. The finite tests are diagnostics only.

The divergent-gap part of Problem 711 is a published prior result. The uniform upper-bound question F(n)<=n^(1+o(1)) remains unresolved by these results. The fixed-start asymptotic question in Problem 710 is separate. Nothing in this audit establishes that asymptotic or claims mathematical novelty. In particular, the exponent 4/3 in the current located upper bound does not approach 1.

## Definitions and normalization

For positive integers n and an integer m, let I(m,H)={m+1,...,m+H}. Define f(n,m) to be the least nonnegative integer H such that I(m,H) contains pairwise distinct integers a_1,...,a_n with i dividing a_i for every 1<=i<=n. Define F(n)=max_m f(n,m). The analogous prime-only maximum, with the indices restricted to primes at most n, is h_P(n).

These extrema are well defined. Consecutive disjoint blocks of lengths n,n-1,...,1 each supply a multiple of the corresponding index, so f(n,m)<=n(n+1)/2. Translation by M=lcm(1,...,n) preserves every divisibility relation and every matching. Thus f(n,m+M)=f(n,m), and the maximum is attained on a finite residue system. Allowing all integers m, as Chen--Korsky do, instead of only positive m does not change F(n). The same argument applies to the prime version.

The original Erdős--Pomerance paper defines its one-variable f(n) as an absolute right endpoint. In this audit's notation that function is

    f_original(n)=n+f(n,n).

This is explicit on printed page 147, PDF page 1. Its Theorems 2 and 3 bound the absolute endpoint. Subtracting n gives the same leading asymptotic constants for the length because sqrt(log n/log log n) tends to infinity.

Erdős's 1992 article, printed page 36, PDF page 3, uses the open interval (m,m+f(n;m)) and explicitly sets the one-variable quantity to the diagonal length. For integer endpoints its open-right length is exactly f_open(n,m)=f(n,m)+1. Therefore F_open(n)=F(n)+1, and the difference F_open(n)-f_open(n,n) is exactly F(n)-f(n,n), not merely equivalent up to an asymptotic error. The separate uniform upper-bound conjecture is unaffected by this one-unit change. The original endpoint notation must not be substituted directly into that difference.

All logarithms in the audited arguments are natural logarithms. Statements with o(1), O(...), or sufficiently large n do not supply an explicit numerical threshold.

## Van Doorn published proof

Source: Wouter van Doorn, *On the length of an interval that contains distinct multiples of the first n positive integers*, Integers 26 (2026), A7, published January 5, 2026, DOI 10.5281/zenodo.18154085. The full three-page publisher PDF was read, and the proof page was visually inspected. [Publisher PDF](https://math.colgate.edu/~integers/aa7/aa7.pdf).

### The transfer inequality

For positive integers k,n, the asserted inequality is

    kn+f(kn,kn) <= k^2 n+f(n,k^2 n).

Take a distinct-multiple system for indices 1,...,n above k^2 n. For each additional index n<i<=kn assign the integer ki. Those added integers are pairwise distinct, are divisible by their assigned indices, and lie in (kn,k^2 n]. The original system lies strictly above k^2 n, so it cannot collide with the added integers. Their union is an admissible system for 1,...,kn in (kn,k^2 n+f(n,k^2 n)]. Taking the least possible endpoint proves the inequality. For k=1 the additional set is empty and the conclusion is equality. There is no endpoint or multiplicity defect.

### The analytic inputs

The only non-elementary inputs to this short proof are the Erdős--Pomerance diagonal estimates

    f(N,N) >= (2/sqrt(e)-o(1)) N sqrt(log N/log log N),
    f(N,N) <= (2+o(1)) N sqrt(log N).

They correspond to Theorems 2 and 3 in the 1980 paper, printed pages 150 and 153, with the absolute-endpoint conversion above. Both theorem statements were visually checked in the complete original PDF. The upper-bound proof also has the familiar valid disjoint-block construction and degree form of Hall's theorem. The full original smooth-number lower-bound argument is not recertified from first principles here; its published theorem is an explicit dependency. [Original paper](https://math.dartmouth.edu/~carlp/PDF/matching.pdf).

### Constants and limiting transitions

Put L=log n, ell=log log n, k=ceil(0.6 sqrt(L/ell)), and epsilon=0.01. Then k/sqrt(L/ell)->0.6, log(kn)/log n->1, and log log(kn)/log log n->1. Applying the lower estimate at N=kn gives

    liminf f(kn,kn)/(k^2 n) >= 2/(0.6 sqrt(e)) > 2.01.

The last inequality has a genuine fixed margin: the lower-limit constant is approximately 2.0217689. Consequently f(kn,kn)>2.01 k^2 n eventually. Applying the diagonal upper estimate at n gives

    f(n,n)/(epsilon k^2 n) = O(ell/sqrt(L)) -> 0.

Thus epsilon k^2 n>f(n,n) eventually. The transfer inequality now yields

    F(n) >= f(n,k^2 n)
         >= kn+f(kn,kn)-k^2 n
          > (1+epsilon)k^2 n
          > f(n,n)+0.36 n L/ell,

because the ceiling ensures k^2>=0.36 L/ell. Dropping the positive kn is harmless and the strict inequalities have adequate slack. This proves exactly the stated eventual bound and hence the divergent-gap conjunct.

## Kominers manuscript audit

Source: Scott Duke Kominers, *Long Intervals Without Distinct Multiples of the First n Positive Integers*, arXiv:2607.10431v1, July 11, 2026, 19 pages. The complete extracted text was read, including the proof of the main theorem, later scope remarks, and references. During the recorded audit, the arXiv submission history was checked and listed only v1. No journal acceptance was verified. [Versioned source](https://arxiv.org/abs/2607.10431v1).

### Smooth-number obstruction

Let Psi(x,y) count positive y-smooth integers at most x. Suppose E>m and

    Psi(n,y)-Psi(E/y,y) > Psi(E,y)-Psi(m,y).

The right side is nonnegative, so E/y<n. Every y-smooth index i in (E/y,n] would need a distinct multiple a_i in (m,E]. Its positive integer cofactor a_i/i is strictly less than y, hence is y-smooth. The assigned multiple is therefore y-smooth. The displayed inequality says that there are more such indices than available smooth target integers, which is impossible. Thus f(n,m)>E-m. Real E is allowed; later E and m are floored to integers. This is a sound Hall obstruction, with no assumption that all indices are smooth.

### Analytic dependency verification

The two inputs used in Sections 3--5 were checked against the primary author-hosted corrected copy of Hildebrand and Tenenbaum, *On integers free of large prime factors*, Transactions of the AMS 296 (1986), 265--290. Printed pages 268--269, PDF pages 4--5, contain the required Theorem 2(i) and Theorem 3:

    alpha(x,y) = [log(1+y/log x)/log y]
                 [1+O(log log(1+y)/log y)],

    Psi(cx,y)/Psi(x,y) = c^alpha(x,y)
                        [1+O(1/u+log y/y)],  u=log x/log y,

uniformly for x>=y>=2 and 1<=c<=y in the second formula. The saddle-point definition is identical. The complete corrected source was retrieved; these two theorem pages were visually inspected. The analytic proofs of those standard theorems are dependencies, not independently reproduced in this audit. [Author-hosted corrected paper](https://tenenb.perso.math.cnrs.fr/PPP/Psi%2B.pdf).

For fixed d>0 and y=dL, with x between fixed positive multiples of n and nL, these inputs give alpha=(log(1+d))/ell+o(1/ell). The relative error in the ratio formula is O(ell/L)=o(1/ell). This is sufficiently small for subtracting nearby smooth counts whose relative size is 1/ell. An error merely o(1) would not suffice; the manuscript correctly uses the sharper error.

### Three parameters and the order of limits

Fix 0<a<b<d and set m=floor(anL), E=floor(bnL), lambda=log(1+d). Applying the ratio formula with base and dilation pairs (E/y,ny/E), (m,E/m), and (n,m/n) gives, respectively,

    [Psi(n,y)-Psi(E/y,y)]/Psi(n,y)
        = lambda log(d/b)/ell+o(1/ell),
    [Psi(E,y)-Psi(m,y)]/Psi(m,y)
        = lambda log(b/a)/ell+o(1/ell),
    Psi(m,y)/Psi(n,y) = 1+d+o(1).

All bases exceed y eventually and all dilation factors lie in [1,y]; for the growing third factor this uses a<d. Floor errors do not affect the limits. Therefore the obstruction works whenever

    log(d/b) > (1+d) log(b/a).

It supplies F(n)> (b-a)nL+O(1). For fixed d,b this condition is exactly a>b(b/d)^(1/(1+d)). On setting r=b/d, the supremal coefficient is d r(1-r^(1/(1+d))). Differentiation gives the maximizing r=((d+1)/(d+2))^(d+1) and coefficient

    C_d = [d/(d+2)] [(d+1)/(d+2)]^(d+1) -> 1/e.

Given any C<1/e, choose a fixed large d with C_d>C and then fixed a,b with b-a>C and strict obstruction slack. Only then let n tend to infinity. Since f(n,n)=O(n sqrt(L))=o(nL), this proves the liminf statement. There is no unjustified use of a growing d(n) in a fixed-parameter estimate.

One harmless bookkeeping issue occurs in the proof of Proposition 4.1: it names common constants c1=b/(2d), c2=2b for Lemma 3.1, whose statement asks c1<c2. This particular inequality need not hold if d<=1/4. The asserted asymptotic range itself is valid, and replacing c2 by max(1,2b) satisfies the stated lemma hypotheses without changing any formula. The main theorem takes d arbitrarily large, so even this adjustment is unnecessary for its actual parameter choices. This is not a gap in Theorem 1.1.

### Limits on adoption

Kominers's numerical 1/e is a supremum within that fixed three-parameter family. It is not an asymptotic formula for F(n), and the paper's final question F(n)<<n log n is not a proved upper bound. Chen--Korsky v2 later answers that question negatively: its lower bound implies F(n)/(n log n)->infinity. The manuscript's explicit remark that the exponent-one uniform upper bound remains open is consistent with all audited results.

Sections 6.1--6.3 were read for scope and deductions. The transfer optimization (1/e-o(1))nL/ell uses the known diagonal inputs and says nothing about arbitrary future methods. The polynomial-height bound max_{m<=n^C}f(n,m)<=n^(1+o(1)), for each fixed C, is also compatible with the lower construction at height comparable to n log n. It cannot be promoted to a maximum over all starts, since the period lcm(1,...,n) has superpolynomial size. The side discussion is not needed for acceptance of the main lower bound.

## Chen and Korsky version two audit

Source: Kaizhe Chen and Samuel Korsky, *Improved Bounds for Distinct Multiples in Intervals*, arXiv:2607.26450v2, revised August 13, 2026, 10 pages. The title page itself bears August 4, 2026; the revision date comes from the arXiv version stamp and submission history. The whole manuscript text was read, and the central path-counting and lower-construction pages were visually inspected. No journal acceptance was verified. [Versioned source](https://arxiv.org/abs/2607.26450v2).

Version 1 is historical, not the adopted version. Its one-author title page and exponent approximately 1.4031 and lower exponent coefficient 1/50 are superseded by the two-author v2 main theorems. The weaker Katz--Tao appendix in v2 is not a dependency of the bounds accepted here. Its cited projection theorem has not been independently source-audited in this report.

### The progression union lemma

Consider one L-term progression S_d of difference d for each distinct positive d in a finite nonempty set D. Let L=2ell>=4 and assume all progressions lie in an integer interval of length H. Put U=union S_d and kappa=max_{1<=t<=H} #{d in D:d divides t}. The key lemma says that |U|<=|D| implies L^3<=C kappa^2 |D| for an absolute constant C.

Split each progression into its even- and odd-index subsequences. Treat these as labeled left vertices, even if some sets happen to coincide, and U as the right vertex set of the incidence graph. Each left vertex has degree ell. An oriented three-edge path consists of two distinct left vertices incident to u, followed by a different right point w incident to the second left vertex. The exact count is

    T=(ell-1) sum_{u in U} deg(u)(deg(u)-1).

Since the graph has |D|L edges, Cauchy--Schwarz and |U|<=|D| imply T>=3|D|L^3/16. The constants here are only an explicit check of the paper's absolute-constant notation.

For a path beginning at a subsequence of S_d, its second progression S_e contains x=(u+w)/2. The same-parity split makes x an integer point of the original S_e. Map the path to (d,x,w). This determines u=2x-w. It also determines the parity label for S_d. The second difference e must divide the nonzero integer w-u, whose absolute value is at most H. Thus there are at most kappa possible e, each with a unique parity label. No zero-difference term is inadvertently charged to kappa.

Writing m_d(c)=#{z in U:z=c mod d}, the image tuples satisfy w=2x-a_d mod d, so

    T <= kappa sum_d sum_c m_d(c)m_d(2c-a_d).

The doubling map modulo d has at most two preimages, including when d is even. Cauchy--Schwarz bounds the inner sum by sqrt(2)sum_c m_d(c)^2. Separating equal-point pairs from unequal-point pairs gives

    sum_d sum_c m_d(c)^2 <= |D||U|+kappa |U|(|U|-1)
                         <= 2 kappa |D|^2.

Here kappa>=1 since each progression has positive difference d<=H. Consequently T<=2sqrt(2)kappa^2|D|^2. The two estimates imply the lemma, for example with the harmless absolute choice C=16. Each injection, parity case, and diagonal contribution is valid.

### Uniform all integer upper bound

Let Delta_n=max_{t<=n^2} tau(t). Splitting prime factors at sqrt(log n) proves Delta_n<=exp(O(L/ell)): small primes contribute at most O(sqrt(L) log L)=o(L/ell) to log tau(t); exponents on larger primes sum to at most 4L/ell, and a+1<=2^a bounds their divisor contribution.

Partition 1,...,n into dyadic sets D_k={d:2^(k-1)<d<=2^k}. Choose

    L_k=2 ceil(A(1+Delta_n^(2/3)|D_k|^(1/3))),
    H_k=2^k L_k,

with fixed A>=2 and 8A^3>C. Allocate disjoint target blocks of lengths H_k above the arbitrary given start m. Every d in D_k has at least L_k multiples in its block, and L_k consecutive multiples can be selected.

A Hall-deficient subfamily S within one block would have a union U with |U|<|S|. Uniformly in k, H_k<<n^(4/3+o(1))<n^2 eventually, so all nonzero differences in that block have at most Delta_n divisors. Applying the lemma gives L_k^3<=C Delta_n^2|S|<=C Delta_n^2|D_k|, contrary to the choice of L_k. This is not circular: the divisor estimate is first established up to n^2, and that independently bounds the preselected block lengths below n^2.

Hall matchings inside disjoint blocks combine without collisions. Their total length is

    sum H_k << n+Delta_n^(2/3)sum 2^(4k/3)
             << Delta_n^(2/3)n^(4/3).

The start m never enters the bound. This proves exactly the claimed uniform theorem. There is no loss from the partial top dyadic class, and small n are absorbed into the implicit constants.

### Prime upper bound

Split the large primes into dyadic classes P_j contained in (X_j/2,X_j]. Allocate a block of length ceil(X_j L_j), with L_j=2ceil(A|P_j|^(1/3)); handle the finitely many small primes separately by disjoint blocks of length p. For sufficiently large X_j the allocated length is less than X_j^2/4. Two distinct primes in the class have product greater than X_j^2/4, so no nonzero difference in the block can be divisible by two of them. Thus kappa=1. The same lemma rules out Hall deficits.

Summing the block lengths gives H<<n+n pi(n)^(1/3), because sum X_j<=2n and |P_j|<=pi(n). The prime number theorem supplies pi(n)<<n/log n, yielding h_P(n)<<n^(4/3)/(log n)^(1/3). Single-prime classes cause no exception: their block contains multiples, so kappa=1 remains valid.

### Lower bound and exact interval endpoints

Fix eta in (0,1), take r=floor((1-eta)L/ell), and let Q be the product of the first r odd primes q_i. Put delta=2^(-r) product(1+1/q_i). Completing the square modulo each odd prime shows that d^2+jd occupies (q_i+1)/2 residues. The Chinese remainder theorem therefore bounds its image modulo Q by Q delta. This compression is valid for every integer j, including j divisible by a factor of Q.

The prime number theorem and Mertens' estimate imply

    log Q=(1-eta+o(1))L,
    log delta=-(log 2+o(1))r.

Choose K=floor(1/(4sqrt(delta log n))) and D=floor(n/(4K)). The square root covers the entire product delta log n; this was checked in the rendered PDF. Then

    log K=((1-eta)(log 2)/2+o(1))L/ell,
    K=n^o(1), D=n^(1-o(1)), D=o(n), Q=o(D).

Partitioning almost all of [n/2,n) into intervals of the integer length D and averaging the prime count gives one interval [v,v+D) containing a set P of at least D/(2log n) primes. This requires only the ordinary prime number theorem over the large covered interval; it does not assert primes in every prescribed short interval.

For p in P let b_p be the representative of p^2 modulo Q in [1,Q). This is nonzero because p>q_r and hence p is coprime to Q. For 0<=j<K, the set T_j={b_p+jp:p in P} occupies at most Q delta residue classes modulo Q and has diameter less than Q+jD. Therefore |T_j|<=(2Q+jD)delta. Its total union T satisfies

    |T| <= 2KQ delta+K(K-1)D delta/2
         <= 3K^2 D delta <= 3D/(16log n) < |P|.

Use CRT on the distinct primes p to choose m=-b_p mod p for every p in P, and take H=Kv. Add a multiple of product_{p in P}p if a positive start is desired. We have Q+KD<v eventually, since KD<=n/4, Q=o(n), and v>=n/2. For each p,

    b_p-p<0<b_p,
    b_p+(K-1)p < Q+(K-1)(v+D) < Kv=H,
    H < b_p+Kp.

Consequently the multiples of p in the closed-right interval I(m,H) are exactly m+b_p+jp for 0<=j<K. No omitted endpoint multiple or extra progression term repairs the Hall deficit. Their combined neighborhood has |T|<|P|, so h_P(n)>H>=nK/2.

For each fixed eta the resulting lower coefficient is (1-eta)(log 2)/2. Taking the liminf and then allowing eta to decrease to zero proves the asserted (log 2)/2-o(1) exponent. It does not require an unproved estimate uniform in eta tending to zero with n. The bound holds for all sufficiently large n in the asymptotic sense, not just along a subsequence.

## Consequences and audit boundaries

The strongest accepted lower bound grows faster than n(log n)^A for every fixed A, because (log n/log log n)/log log n tends to infinity. In particular, together with the diagonal upper bound it implies [F(n)-f(n,n)]/(n log n)->infinity. This is a direct consequence of the attributed Chen--Korsky theorem and is stronger than the earlier Kominers liminf bound. It still has the form n^(1+o(1)), so it is fully compatible with the unresolved exponent-one upper conjecture.

The proof audit uses established Hall matching, unique factorization, CRT, the prime number theorem, Mertens' estimate, the published diagonal estimates, and the two verified Hildebrand--Tenenbaum theorems. It does not certify finite numerical thresholds, survey all possible later literature, or prove the open target. The recorded audit verified the identified source versions on October 10, 2026. Historical authored finite diagnostics exercised normalization, transfer, path fibers, residue compression, and exact endpoint enumeration. Their aggregate results are reported in VERIFICATION.json; code and detailed numerical outputs are omitted. Those diagnostics cannot certify the asymptotic theorems by themselves.

## Source references

1. Erdős and Pomerance, *Matching the natural numbers up to n with distinct multiples in another interval*, 1980, pp. 147--161. [Complete PDF](https://math.dartmouth.edu/~carlp/PDF/matching.pdf).
2. Erdős, *Some of my forgotten problems in number theory*, Hardy--Ramanujan Journal 15 (1992), pp. 34--50. [Complete PDF](https://hrj.episciences.org/125/pdf).
3. van Doorn, Integers 26 (2026), A7. [Published PDF](https://math.colgate.edu/~integers/aa7/aa7.pdf).
4. Kominers, arXiv:2607.10431v1. [Version record](https://arxiv.org/abs/2607.10431v1).
5. Chen and Korsky, arXiv:2607.26450v2. [Version record](https://arxiv.org/abs/2607.26450v2).
6. Hildebrand and Tenenbaum, Transactions of the AMS 296 (1986), 265--290, author-hosted copy marked with corrections by G.T. [Corrected PDF](https://tenenb.perso.math.cnrs.fr/PPP/Psi%2B.pdf).
