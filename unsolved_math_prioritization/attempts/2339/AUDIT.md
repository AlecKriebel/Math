# Independent audit: positive three-term radical blocks (EP 850 / 2339)

## Disposition

This AI-assisted, unrefereed edition records an independent internal AI audit. Acceptance is an internal mathematical assessment, not external human peer review or formal proof-assistant certification. The complete authored elementary proof and Pell/BHV completeness derivation are retained. BHV is an explicitly imported established theorem; its proof and original computations are not reproduced or independently audited here. The exact 41-smooth enumeration is a computation-dependent result supported by historical independent verification. This edition omits the 141-start inventory, raw certificates, programs and raw datasets, so it is not a self-contained computational reproduction package. Hashes authenticate bytes, not mathematical truth. Source retrieval and inspection described here occurred in the preceding candidate and audit on 11 October 2026; this editorial preparation performed no new scholarly-source retrieval, inspection or mathematical computation.

**Accept the two stated partial mathematical results, with their dependencies and scope kept separate.** No mathematical correction to the frozen report is required.

1. **Elementary result accepted.** The positive starts whose three-term product has at most three distinct prime factors are exactly 1, 2, 3, 4, 6, 7, 8, 16. Thus a pair of distinct positive blocks with positionwise equal radicals needs at least four common union primes.
2. **BHV-dependent computational result accepted.** With every prime factor at most 41, there are exactly 869 positive consecutive-pair starts and exactly 141 positive consecutive-triple starts. The greatest triple start is 212380. Every triple satisfies rad(n(n+1)(n+2)) >= 3n, with equality only at n=2. This rules out the target within that fixed prime set at all magnitudes.
3. **Final packet integrity accepted.** The final pinned verifier excludes only the exact root manifest and rejects nonregular members. A basename-only exclusion seen during the initial, pre-seal reading had already been corrected before final sealing. The final candidate needs no correction patch and passes this audit's independent closed-inventory authentication.
4. **No acceptance of a full resolution.** The unrestricted arbitrary-prime question remains open within this work. This is not a novelty certificate, a current worldwide status determination, or an audit/reproof of BHV itself.

The original candidate was not edited. No candidate Python program, downloaded author program, or external solution dataset was executed. The independent auditor read the report, inspected the candidate verifier as source, and treated the numerical certificate as data to compare against a fresh reconstruction.

## Authenticated object and source boundaries

This audit independently authenticated the candidate manifest's exact 4500 bytes and all 25 listed members against a separately pinned digest, including exact byte counts and SHA256 hashes, with no additional regular files or symlinks:

- Candidate MANIFEST.json: 98e444740b750ec5c80a4aa329db9e8f416825645d5623734a8802f29c3e128f
- Candidate external seal: bd8bbb63c26ec17815241d0a8af2f23f42659d7b70f68c76daf22ae220af9303
- Main arithmetic certificate: 26539309 bytes; 955f27b8922973813f75f252526b869de55aaed5ad189a2d368db2d16522197a

Public aggregate authentication metadata appears in VERIFICATION.json. Raw authentication receipts and artifacts are not distributed. Authentication identifies the audited input; it is not by itself proof acceptance.

The primary source for the target is Shorey and Tijdeman, *Arithmetic properties of blocks of consecutive integers*, [arXiv:1612.05438v1](https://arxiv.org/abs/1612.05438). The auditor independently extracted and visually inspected PDF page 13, containing all of Section 9, Conjecture 9.1, and Theorem 9.1 with its proof. Its theorem explicitly assumes the stated explicit abc conjecture. The page does not give an unconditional proof. The candidate's complete PDF has 213552 bytes and SHA256 eb14b189fad3cd6a5db56cbdb4b80dd4ae14ed871ea13d41a1f00895371993a3. Earlier-original access and a complete literature search were not undertaken by this audit.

The imported primitive-divisor result is Bilu, Hanrot and Voutier, *Existence of primitive divisors of Lucas and Lehmer numbers*, J. reine angew. Math. 539 (2001), 75-122, [DOI](https://doi.org/10.1515/crll.2001.080). The auditor independently opened the [primary author-uploaded manuscript](https://www.researchgate.net/profile/Paul_Voutier/publication/2397582_Existence_of_Primitive_Divisors_of_Lucas_and_Lehmer_Numbers/links/559999c308ae99aa62cc6983/Existence-of-Primitive-Divisors-of-Lucas-and-Lehmer-Numbers.pdf): Section 1's Lucas-pair and primitive-divisor definitions, the meaning of totally non-defective, and Theorem 1.4 on manuscript page 4. This was a 36-page manuscript presentation. Web-extracted text was available; attempted screenshots returned only textual references, so this audit claims no BHV visual-page inspection, raw-PDF retrieval, or raw-PDF hash. BHV's full proof and its original computations were not audited or rerun. It is an explicit imported established theorem.

The audit does not use Najman's paper, an external catalogue, or the candidate's 31/37 exploratory computations to establish its result. Attribution to classical Størmer/Pell methods is appropriate; no novelty is inferred.

## 1. Target and elementary consequences

Let rad(m) denote the product of the distinct primes dividing a positive integer m, with rad(1)=1. The target is positive a<b with

    rad(a+i)=rad(b+i), i=0,1,2.

It is positionwise, not simply equality of the two product radicals. Put d=b-a and R=rad(b(b+1)(b+2)). Every prime dividing b+i also divides a+i, hence d. Squarefreeness gives R|d, so R<=d<b. The triple contains a multiple of 2 and a multiple of 3, whence 6|R|d. These statements include starts involving 1 and do not rely on a factorization of 1 into primes.

For fixed positive d, let S(d) be its set of prime divisors. The target with b=a+d is equivalent to all six positive integers in the two blocks being S(d)-smooth. Forward: equality of supports forces each prime into d. Reverse: any prime of either corresponding entry divides d, and the two entries are congruent modulo it. Therefore it divides the other entry as well. Primes of d absent from the six entries do not matter.

For each i, some common-support prime must have a larger exponent in b+i than in a+i; otherwise b+i would divide a+i. If its smaller exponent is e, subtraction of p^e times a p-adic unit from a higher power gives v_p(d)=e. Therefore p^(v_p(d)+1) divides b+i. Such an increasing prime cannot occur at two positions: that power would divide their nonzero difference of absolute value at most 2. Because p divides both corresponding entries and hence d, v_p(d)>=1 and the power is at least 4. Thus each of the three positions needs a distinct increasing prime. This validates the candidate's valuation claim, while the classification below strengthens its support obstruction.

## 2. Complete elementary classification

### 2.1 Adjacent powers of 2 and 3

For positive u,v, the only pairs (2^u,3^v) differing by 1 are (2,3), (4,3), (8,9).

If 2^u-3^v=1 and u>=3, then 3^v is 7 modulo 8, impossible since its possible residues are 1 and 3. Values u=1,2 yield only (4,3). If 3^v-2^u=1 with u>=3, then 3^v is 1 modulo 8, so v=2w. The factors 3^w-1 and 3^w+1 are positive powers of 2 differing by 2. Writing them as 2^h and 2^j with h<j gives 2^h(2^(j-h)-1)=2, so h=1,j=2. This gives w=1,u=3. The cases u=1,2 give only (2,3). No Catalan-type theorem is needed.

### 2.2 Exhaust the prime allocations

Suppose n(n+1)(n+2) has at most three distinct prime factors. Two of them are 2 and 3. Starts 1 and 2 qualify directly.

For odd n>=3, the two odd endpoints exceed 1 and are coprime. They therefore require the two available odd primes in disjoint positions; each endpoint is a pure prime power. The middle has no odd prime available and is a power of 2. One endpoint is a power of 3. The adjacent-power list makes the middle 4 or 8, hence n=3 or 7. This argument also excludes supports with fewer odd primes: they cannot supply the two coprime odd endpoints.

For even n>=4, the odd middle is coprime to both endpoints. If it used both available odd primes, both endpoints would be pure powers of 2, impossible since the only powers differing by 2 are 2 and 4. Thus n+1=r^s for one odd prime r. At most one odd prime q is available to the endpoints, and it cannot divide both since gcd(n,n+2)=2. Hence one endpoint is 2^u and the other is 2^c q^v, with v>0. Both endpoints cannot be pure powers of 2. The block's multiple of 3 forces r=3 or q=3.

If r=3, the middle is a power of 3 adjacent to a pure power of 2. The list above permits middle 3 or 9. Middle 3 would give n=2, already excluded; middle 9 gives n=8.

If q=3, the pure-power endpoint is at least 4, so the other endpoint, which differs by 2, has exactly one factor of 2. Dividing the endpoint difference by 2 gives |2^(u-1)-3^v|=1. The auxiliary list gives endpoint pairs (4,6), (6,8), (16,18), hence n=4,6,16. All allocations have been covered, including a missing third prime.

Direct factorization of the eight starts gives union radicals, in increasing start order,

    (1,6), (2,6), (3,30), (4,30), (6,42), (7,42), (8,30), (16,102).

Every displayed radical exceeds its start. A putative target pair using at most three common primes would place its larger start b in this list, contradicting R<b. This proves the first accepted result entirely independently of BHV or any computation.

## 3. Why a finite Pell computation covers every magnitude

Fix a finite prime set S containing 2, let P=max(S), and Q be its prime product. If t,t+1 are positive S-smooth integers, uniquely write

    t(t+1)=D w^2

with D squarefree. The strict inequalities t^2<t(t+1)<(t+1)^2 show D!=1. Every prime of D and w lies in S. Thus D is a nontrivial squarefree divisor of Q. With X=2t+1 and Y=2w,

    X^2-DY^2=1, X odd, Y>0 and S-smooth.

This includes t=1 and does not lose the D=1 case: that case is impossible.

### 3.1 Correct ring and generator

Work in Z[sqrt(D)], not necessarily in the full ring of integers of Q(sqrt(D)). Let epsilon=x1+y1 sqrt(D)>1 be its least positive integral norm-one solution, y1>0. Every positive integral norm-one solution z=X+Y sqrt(D)>1 is epsilon^k with positive integer k. Indeed, choose k>=0 so epsilon^k<=z<epsilon^(k+1). The quotient z epsilon^(-k) belongs to Z[sqrt(D)] because epsilon^(-1)=x1-y1 sqrt(D), has norm 1, and lies in [1,epsilon). If greater than 1, its conjugate is its positive reciprocal less than 1. Its sqrt(D) coefficient is then a positive integer, contradicting minimality. It is therefore 1. Since z>1, k cannot be 0.

This argument uses no half-integral unit. For example, D=5 is normalized to (x1,y1)=(9,4); the smaller half-integral units in the full ring are irrelevant. Norm minus-one units are likewise not the generator unless squared to norm plus one.

### 3.2 First norm-plus-one convergent really is fundamental

For a Pell solution, gcd(x,y)=1 and

    0 < x/y-sqrt(D) = 1/[y^2(x/y+sqrt(D))] < 1/(2y^2).

Here is an explicit proof of the continued-fraction approximation fact used. Let p_j/q_j be the regular convergents of an irrational alpha, and choose the largest j with q_j<=q<q_(j+1). Adjacent convergent vectors form an integer basis since their determinant is +/-1; their errors e_j=q_j alpha-p_j have opposite signs. Write any vector (p,q) as A(p_j,q_j)+B(p_(j+1),q_(j+1)), A,B integers. If B=0, its error has magnitude at least |e_j|. Otherwise the restriction 0<q<q_(j+1) forces A,B to have opposite signs: zero A or same positive signs would make q too large, and same negative signs would make it negative. Their two error terms then have the same sign, also giving |q alpha-p|>=|e_j|. This is the needed best-approximation property.

If p/q is distinct from p_j/q_j and |alpha-p/q|<1/(2q^2), the nonzero integer p q_j-q p_j satisfies

    |p q_j-q p_j|
      <= q_j |p-q alpha|+q |p_j-q_j alpha|
      <= (q_j+q)|p-q alpha| < (q_j+q)/(2q) <= 1,

a contradiction. Hence a Pell ratio x/y is a convergent. Convergent denominators are nondecreasing (strictly after the initial possible repetition), and sqrt(1+D y^2)+y sqrt(D) increases strictly with positive y. Therefore the first norm-plus-one convergent is the least positive integral norm-one solution. Existence can be taken from the classical periodic continued fraction of a nonsquare square root; the finite certificate independently exhibits such a convergent for every D actually used.

The new verifier generates its own continued fractions; it does not start from a certificate-supplied fundamental pair or trust the supplied stopping point. Its complete-quotient states are M_0=0,Q_0=1,a_0=floor(sqrt(D)), then

    M_(j+1)=a_j Q_j-M_j,
    Q_(j+1)=(D-M_(j+1)^2)/Q_j,
    a_(j+1)=floor((a_0+M_(j+1))/Q_(j+1)).

With forward continuants, the identity

    p_j^2-D q_j^2 = (-1)^(j+1) Q_(j+1)

identifies exactly every norm-plus-one index. To see it, the complete-quotient relation gives p_j=q_j M_(j+1)+q_(j-1)Q_(j+1) and Dq_j=p_j M_(j+1)+p_(j-1)Q_(j+1). Subtract after multiplication by p_j and q_j respectively, and use the determinant identity. The implementation checks the first relation at every step, exact divisions, and the final large-integer Pell identity. Thus it can test earlier norms without millions of large squarings. It separately brute-forces all smaller positive y for the 18 enumerated D<=30, including D=5, as a redundant check.

### 3.3 Exact BHV input and Lucas hypotheses

The imported BHV result guarantees a primitive prime divisor for every Lucas term of index greater than 30. For this purpose a Lucas pair has algebraic-integer entries alpha,beta with nonzero coprime rational-integer sum and product, and alpha/beta not a root of unity. A primitive prime of U_k=(alpha^k-beta^k)/(alpha-beta) divides U_k but not (alpha-beta)^2 times any earlier positive-index term.

Take alpha=epsilon, beta=epsilon^(-1). Both are roots of T^2-2x1 T+1. Their sum is 2x1 and product 1, so the required coprimality holds even though the sum is even. Their ratio is epsilon^2>1, hence not a root of unity. Also alpha-beta=2y1 sqrt(D), and writing epsilon^k=x_k+y_k sqrt(D) gives U_k=y_k/y1. The recurrence U_0=0,U_1=1,U_(k+1)=2x1 U_k-U_(k-1) confirms integral U_k. Therefore y1 divides every y_k. Discarding a D for which y1 has a non-S prime cannot discard an eligible solution. No other discard based on the fundamental solution is used.

### 3.4 Primitive rank and the bound

Suppose k>30 and y_k is S-smooth. BHV gives a primitive prime q|U_k, so q is in S. Primitivity excludes divisors of (alpha-beta)^2=4D y1^2. Consequently q is odd and does not divide D y1.

If D is a square modulo q, choose a square root s in F_q. Otherwise use F_(q^2)=F_q[s] with s^2=D. In either field set u=x1+y1 s and v=x1-y1 s. They are nonzero since uv=1, and distinct since q does not divide 2D y1. The reduction of U_j is (u^j-v^j)/(u-v), so q|U_j if and only if (u/v)^j=1. As no earlier U_j has q as a divisor, the order of u/v is exactly k.

In the split case it divides q-1. In the nonsplit case Frobenius interchanges s and -s, thus u^q=v and (u/v)^q=v/u, so its order divides q+1. Hence k<=q+1<=P+1. Combining this with the untouched small indices yields

    1<=k<=max(30,P+1).

In particular P=41 permits k=1,...,42. Every one of these indices was enumerated for every eligible fundamental solution. No small-index classification, defective-pair table, strengthened real-Lucas theorem, or presumed primitive prime at an exceptional index is used. This explicitly covers 1,2,3,4,6,12,30 and every other index <=30.

### 3.5 Exact pair and triple inventories

Each positive smooth pair gives one D and one power index by the reduction and norm-one generator. Conversely, each enumerated odd x_k is retained only if t=(x_k-1)/2 and t+1 are both positive and S-smooth. This final test prevents spurious solutions irrespective of parity details. For squarefree D an odd x_k also forces y_k even, and the verifier explicitly checks this and t(t+1)=D(y_k/2)^2 at each retained pair.

A triple starts at t exactly when t and t+1 are in the complete pair-start inventory. This intersection is both necessary and sufficient. Thus there is no independent size cutoff hiding in the triple stage. The all-magnitude conclusion comes from the proved index bound and complete D enumeration, not from a bounded integer search.

## 4. Independent exact computation and controls

The auditor authored an independent verifier without importing or executing any candidate code. It constructs the primes through 41 with a sieve, D values from every nonzero 13-bit subset, all fundamental pairs from integer complete quotients/continuants, and all powers from second-order Lucas and trace recurrences. This differs from the candidate checker's matrix continuants and polynomial-pair binary powers. Prime exponents and cofactors are reconstructed by direct division; radicals use lcm of separately reconstructed position radicals.

All candidate equation objects, continued-fraction lists, fundamental pairs, cofactors, exponent vectors, hit lists, pair lists, block records and collision lists agree exactly with the independent reconstruction. Header values are also compared. Normal, -O and -OO runs all passed; required guards are explicit exceptions, not removable assertions.

Exact results:

- 8191 distinct D values, covering every nontrivial divisor of the product of the 13 primes through 41
- 1832120 continued-fraction coefficients through first norm +1
- 881 S-smooth y1 values and 7310 exclusions by y1 divisibility
- 37002 Pell powers checked, exactly 42 per eligible D
- 869 pair starts, maximum 63927525375
- 141 triple starts, maximum 212380
- zero equal positionwise radical signatures among distinct triples
- every union radical at least 3n, equality only n=2
- pair-hit indices: 707 at k=1, 127 at k=2, 20 at k=3, 9 at k=4, 1 at k=5, 5 at k=6; zero at every index 7 through 42

The separate smooth-number check directly enumerates all 2026471 S-smooth integers up to 63927525376 and finds exactly the same 869 pair starts. It uses no Pell equations and is valuable algorithmic redundancy, but cannot by itself justify that no larger pairs exist. The Pell/BHV proof supplies that global coverage. A separate radical sieve through 1000000 returns the eight elementary starts; it is regression evidence rather than the elementary proof. Two-term examples (2,8), (6,48), (75,1215) are confirmed to fail at the third position, guarding against solving the wrong target.

Canonical independently rebuilt inventory hashes are:

- Pair starts: e0558c7b9bf1c31908a92b25b824940d80eaaa07bd34c396daeabdcde6f2e819
- Full triple records: 8166c56872fdca01d65bf518a0dbcdb0c40cd7cd9f84489fa0b12145be8e4be3
- Full equation records: 9669cae83b93d1507d472985a2824f92501001523539b18dd97b6168ad2671ba

Canonical means JSON with sorted keys and compact separators, followed by one newline. Exact pair and triple inventories were retained in the independently sealed audit and are omitted from this public edition. The inventory hashes and aggregate counts do not reproduce the computation. The complete mathematical reduction is published, but the numerical classification remains dependent on the historically verified, omitted arithmetic artifacts; these files are not a self-contained computational reproduction package.

Each normal/-O/-OO reconstruction also rejected twelve independently constructed adverse certificates: omitted D; duplicated D; changed CF coefficient; a later norm-one Pell solution falsely substituted as fundamental; false nonsmooth cofactor; omission of a genuine k=6 hit; fabricated hit; changing the bound to 30; omitted pair; omitted triple; changed union radical; fabricated signature collision. These are validation controls, not proof that every possible implementation bug has been excluded.

## 5. Integrity review and closure

The auditor initially read a pre-seal verifier using a basename-only exclusion for MANIFEST.json. That predicate would fail to count an unlisted nested file with the same basename. Inspection of the final pinned verifier showed that the author had already corrected it before sealing: it compares the full root-relative path and excludes only the exact root manifest. It also rejects nonregular filesystem members. The apparent correction patch was therefore unnecessary and is not included. No defect is attributed to the final authenticated verifier.

The independent authenticator uses a separately authored strict inventory traversal, checks safe ordered unique paths, rejects duplicate JSON keys, rejects symlinks and special files, pins the manifest externally, and hashes each member. Its normal/-O/-OO adverse controls reject an extra ordinary file, nested MANIFEST.json, equal-size payload corruption, omitted payload, symlink and changed manifest. An isolated fixture compares the historical and corrected manifest-exclusion predicates without running candidate code or mutating the candidate. The actual final candidate passed strict authentication before acceptance and is rechecked on closure.

The original audit's separately pinned manifest covers its complete 19-member inventory, and its seal records normal/-O/-OO closure checks. The candidate and audit were authenticated again during this editorial preparation without executing their mathematical programs. The public MANIFEST.json instead inventories exactly the eight files in this edition and hashes the seven non-manifest files; its own digest is separately pinned in the draft publication description. These content identities do not prove mathematical correctness.

## 6. Accepted consequences and unresolved gap

For any putative target pair, all the following necessary conditions are accepted:

- at least four common union primes, including 2 and 3
- at least one common prime >=43
- R|d with R<=d<b
- one increasing exponent at a different prime for each position, with the stated valuation identity
- R>=2*3*5*43=1290, hence d>=1290
- a>=41, since a<=40 would confine every prime of its triple to at most 41
- b>=1331

These are obstructions, not a construction and not a claim of a sharp search frontier. The abc discussion is also correctly qualified: applying ordinary abc to 1+b(b+2)=(b+1)^2 gives only a bound depending on its unspecified constant; it does not exclude every positive exception. The stronger explicit conjectural bound used by Shorey--Tijdeman would give a contradiction, but it is not available unconditionally here.

The remaining gap is uniformity over unbounded prime supports. A decision procedure for each finite S, even at all magnitudes, cannot settle an infinite union of possible supports without another argument. No general inequality rad(n(n+1)(n+2))>=n has been established by this audit. The mathematical scope remains unchanged: no full resolution, novelty or external publication-acceptance claim. The original candidate's pending-audit wording is updated to reflect this subsequent internal acceptance of the two partial results only.
