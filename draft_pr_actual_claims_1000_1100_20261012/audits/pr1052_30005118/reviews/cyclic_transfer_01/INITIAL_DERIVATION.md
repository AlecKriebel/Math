# Initial derivation frozen before older audit and provenance labels

Original head: `b7e55279707ce2c720304ca98111088d7d037371`.

Read scope at this checkpoint: the complete submitted `CYCLIC_SUMSET_CERTIFICATE.md`, the eight-file pin metadata, repository instruction file, and read-only Git metadata/body pinning. The bodies of `ACCEPTANCE.md`, `INDEPENDENT_AUDIT.md`, `PROVENANCE.md`, `STATUS.json`, `SOURCE_LEDGER.md`, `README.md`, and `MANIFEST.json` have not been inspected. Pinning their bytes is not treating their labels as mathematical evidence.

## Exact language and evidence standard

For each positive integer n let G_n = Z/nZ, with canonical representatives 0,...,n-1. Define A+A = {a+a' : a,a' in A}; the two summands may coincide. The target language consists of encodings of (n,B) for which B=A+A for some subset A of this same G_n. Here n varies without a fixed bound. Two representations are considered: a dense indicator with exactly n bits, and a sparse list of binary canonical residues together with binary n. A claimed affirmative certificate must prove exact equality, including that it creates no additional residue.

The strong restricted target family has n odd, B nonempty, 0 in B, and every canonical representative b in B satisfying 2b<n. Encoding validity can be checked separately and invalid strings rejected. Duplicate sparse entries can either be rejected by a canonical-language convention or collapsed by a set-list convention; either convention has the same complexity claim and the reduction emits distinct elements.

The mathematical conclusion to audit is NP-completeness in both representations under deterministic polynomial-time many-one reductions. The transfer and NP membership are to be verified here. Hardness is conditional on the correctly identified established external integer theorem. I do not claim to reconstruct its reduction gadgets. The required interface is a uniform polynomial reduction from 3SAT to finite integer ordinary self-sumset recognition, whose output S for a formula with N=v+c>=1 is in [0, 2^57 N^4]. Sparse hardness can alternatively use the integer NP-hardness statement alone, when its source language is finite sets of signed binary integers. The bounded-universe interface is essential to the dense composition.

## Integer facts, including all boundary cases

Let S be a finite integer set. If S is empty, it has the empty self-sumset root. No nonempty R can have R+R empty, since r+r is a member whenever r is. Thus empty cases cause no hidden quantifier issue.

If S is nonempty and S=R+R, R is nonempty. It is necessarily finite even if an initial definition allowed an arbitrary integer root: choose r0 in R; the injective map r -> r+r0 sends R into finite S. Write m=min R and h=max R. Every sum lies between 2m and 2h, while m+m and h+h occur. Therefore min S=2m and max S=2h.

Write t=min S. If t is odd, S is NO. This includes negative odd t. If t is even, let B={s-t : s in S} and M=max S-t. Then B is finite nonempty, contains 0, lies in [0,M], and M is a nonnegative integer. The integer t/2 exists even for negative t. Translation establishes the equivalence exactly: R+R=S implies (R-t/2)+(R-t/2)=B; T+T=B implies (T+t/2)+(T+t/2)=S. A root T of B is finite nonempty, with min T=0 and max T=M/2. Consequently it is in [0,M], indeed [0,M/2], and necessarily M is even. Rejection for odd M is optional and unused in the total reduction.

A singleton S={t} is affirmative exactly when t is even, in which case its only integer root is {t/2}. For normalized M=0, B={0} and T={0}. These facts independently cover all singleton and zero-diameter cases.

## Independent proof of the transfer lemma

Assume B is nonempty, 0 in B, B subset [0,M], n is positive odd, and n>2M. Treat B as its injective image in G_n.

An integer root T of B has minimum 0 and maximum M/2, as just proved. Reducing its elements modulo n gives a group root. No root elements or pair sums wrap, because they lie in [0,M] and M<n. Equivalently, taking residues preserves the integer equality T+T=B.

For the reverse and stronger every-root statement, let A+A=B in G_n. A is nonempty because B is nonempty. Since 0 is a sum, choose a,c in A with a+c=0. Then c=-a. Repeated summands give both 2a and 2c=-2a in B. Let p,q be their canonical representatives. They satisfy 0<=p,q<=M, p+q congruent 0 modulo n, and 0<=p+q<=2M<n. The only multiple of n in that interval is 0, so p=q=0. Thus 2a=0 in G_n. Since gcd(2,n)=1, multiplication by 2 is injective (Bezout's identity gives its inverse), and a=0. We have proved 0 in A, not merely the existence of an anchored alternative root.

For every x in A, x+0 lies in B. Hence the set T of canonical representatives of A satisfies T subset B subset [0,M]. For x,y in T their ordinary integer sum lies in [0,2M], strictly below n. Since its residue belongs to B and its representative is itself, x+y belongs to B. This proves T+T subset B.

Conversely, for every b in B choose a,a' in A whose group sum is b. Their representatives x,y in T have x+y in [0,2M] subset [0,n-1]. The numbers x+y and b both lie in that complete representative interval and are congruent, so x+y=b. Thus B subset T+T. Equality follows. Every canonical cyclic root is an integer root. No missing root branches or wrap cases remain.

The proof uses both diagonal sums 2a and -2a. It does not transfer unchanged to the distinct-summand operation. It relies on a sum representing the zero anchor; an arbitrary small positive target is insufficient. For example, {1} has no integer ordinary root because its minimum is odd, but in G_5 the root {3} has self-sum {1}.

The odd hypothesis is necessary for the stronger claim about every canonical root: in G_4, B={0}, M=0, and A={2} is a cyclic root whose ordinary integer self-sum is {4}, not {0}. The proof of YES/NO equivalence can be extended to even n by translating any chosen root by its order-two anchor; that extension is not required by the submitted odd-order theorem and does not weaken it. The strict no-wrap bound is indispensable to this every-root proof; fresh checks will supply boundary controls rather than assume all hypothesis weakenings fail in exactly the same way.

The edge n=1 allowed by the lemma is sound: n>2M implies M=0 and B={0}; the sole nonempty group root has representative {0}, an integer root. The total reduction below uses n>=3.

## Total many-one construction

For an explicit finite signed-integer set S, parse it and remove duplicate entries. On S empty, output (3,empty) for the unrestricted target; if reducing to the nonempty restricted target, output (3,{0}). Both are affirmative and require constant output. On S nonempty with odd t=min S, output (5,{0,1}). This target is NO: the transfer proof with M=1 forces an integer root T subset {0,1}. Producing 1 would require 1 in T, which produces 2 from 1+1, contradicting the target. Equivalently, the maximum of an integer self-sum must be even. The fixed NO lies in the restricted family.

Otherwise use t even, B=S-t, M=max S-min S, and n=max(3,2M+1). This n is odd, positive, and >2M. Normalization and the transfer lemma give exact source/target equivalence. Every output B contains 0, and b<=M<n/2 for all b. When M=0 the output is (3,{0}), affirmative as required. Negative source coordinates do not affect translation or parity. The construction performs arithmetic, sorting/comparison, and set output; it uses neither prime search nor factorization.

If a source language requires syntactically invalid strings to be NO, emit the same fixed NO after a polynomial syntax check. This makes the map total on binary strings as well as total on valid finite-set instances. There is no assumption that the source theorem's final S is already zero-anchored or has a particular minimum parity.

## Sparse polynomiality and NP verifier

For a sparse integer source of length L, each integer has magnitude less than 2^O(L). Subtraction of the extrema, translation of at most the input number of elements, and doubling M increase bit length by at most a constant over the largest source coordinate length. Thus n and all B members have polynomial bit length. Sorting, comparison, subtraction, parity, and emitting the sparse target all take polynomial time in L. Even exponentially large magnitudes do not force dense output in this argument.

For a valid sparse target of length ell, a nonempty affirmative B has a nonempty root A. Fix a0 in A. Translation a -> a+a0 is injective in every group, hence injects A into A+A=B. Therefore |A|<=|B|, for every positive n, odd or even. Guess at most |B| binary representatives in [0,n-1]. This certificate has O(|B| log(n+1)) bits, polynomial in the input size. The verifier first checks syntax and canonical bounds, collapses or rejects duplicate root entries according to its set convention, computes all at most |B|^2 modular sums including diagonal pairs, sorts or deduplicates them, and compares the resulting distinct list with B for exact equality. Binary addition, reduction modulo n, and sorting all have polynomial bit complexity. Empty B uses the empty root certificate; a nonempty root would fail equality. For n=1 the arithmetic and cardinality proof remain valid. Thus sparse target membership in NP does not impose oddness or a bounded numerical universe.

## Dense composition and NP verifier

An arbitrary binary integer source may have enormous M, so its n-bit output need not be polynomial in that source's bit length. That invalid route is not used. Instead apply the established bounded-universe 3SAT reduction first. Its output S subset [0,U], U=2^57(v+c)^4, has diameter M<=U. The normalizing map gives n<=max(3,2U+1), unless it emits a constant exception. For N=v+c>=1 this is O(N^4), with a fixed large multiplicative constant. Writing the n-bit indicator and binary n is therefore polynomial in formula length. The 3SAT family with no variables/clauses can be evaluated in constant time and mapped to a fixed YES or NO as its syntax convention requires; it cannot cause failure of a total reduction. A canonical empty conjunction is YES and maps to (3,{0}) in the restricted version.

A dense affirmative certificate is an n-bit indicator for A. Its length is at most the dense input length. Compute all n^2 potential ordered pairs whose two indicators are 1, mark the modular sum positions, and compare all n bits with B. This uses O(n^2) pair operations; bit-level arithmetic introduces at most a polynomial log n factor. A standard index-based array implementation can obtain O(n^2) elementary operations. Invalid n<=0, a vector with a length other than n, nonbinary vector entries, or malformed integer fields are polynomially rejectable. Dense NP membership is again for all positive n.

The sparse and dense hardness arguments are materially different and cannot be interchanged. With the stated source interface validated, each representation is NP-hard and in NP, hence NP-complete under deterministic polynomial-time many-one reductions. Hardness persists under the nonempty restricted family by choosing its constant YES replacement. The target has a deterministic polynomial-time algorithm if and only if P=NP. Nothing here proves P!=NP or establishes randomized, oracle, circuit-encoding, approximation, average-case, or distinct-summand hardness. There is no new gadget or novelty claim.

## Falsifiable checks and residual source obligation

Fresh finite checks should enumerate every cyclic root for small n and every eligible anchored target, checking the stronger canonical-root conclusion rather than only equality of YES/NO counts. Independent checks should enumerate small signed integer inputs and compare reduction outputs, including emptiness, singleton parity, negative minima, and odd diameter. Explicit controls should refute transfer without the anchor, refute the every-root statement for even n, and refute a too-weak modulus bound. A huge-bit sparse example should illustrate that sparse output bit length remains small while dense output would be enormous. Optimized Python must not erase validation: use explicit conditional exceptions, not assert statements.

These computations are corroboration; the universal mathematical proof is above. The remaining external interface obligation is that the cited AFWS theorem really is about ordinary repeated integer self-sums with integer roots, supplies a uniform 3SAT reduction, and supplies the explicit polynomial numerical universe bound on its final output. It must be checked against the primary pinned version, not inferred from audit labels or from a fixed-characteristic vector-group result.
