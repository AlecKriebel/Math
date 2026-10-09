# Reconstruction of preliminary turn 2 candidates

**Status: unaccepted preliminary work. The original remains unresolved, 2/5 turns.** The derivations below were reconstructed and checked during recovery. This is not an independent acceptance report, a new research turn, or a full reduction. Explicit additions needed for rigor are identified, especially K != 0 in the transporter lemma.

## 1 Modular squares and sign blind relation selection

Let n be an odd squarefree composite with k>=2 distinct prime factors. Take independent uniform samples x_1,...,x_t from the unit group (Z/nZ)^*. For each i let m_i be the positive canonical integer representative of x_i^2 modulo n, and write

    C7(m_i)=(r_i,s_i), so m_i=r_i^2 s_i.

All r_i and s_i are coprime to n. Suppose a relation selector, using only the residues m_i, their deterministic C7 answers, and randomness independent of all root signs, produces a nonempty subset I such that

    product_{i in I} s_i = h^2

for some positive integer h. The selector may fail; this paragraph concerns the event that it returns such a relation. Set

    X = product_{i in I} x_i mod n,
    Y = h product_{i in I} r_i mod n.

Then X^2=Y^2 modulo n and Y is a unit. A proper factor is obtained exactly when 1<gcd(X-Y,n)<n.

### Conditional sign proof

Fix all m_i and the selector's independent randomness. This fixes I, h, and Y. At each prime p dividing n, every nonzero square has two square roots, and the Chinese remainder theorem gives exactly 2^k square roots of each m_i modulo n. Conditional on the fixed residues, each x_i is uniform on that root set, independently across i. Its k sign coordinates are independent uniform signs.

Since I is nonempty, multiplication of the selected roots leaves a uniform sign vector in {+1,-1}^k. Relative to the fixed root Y, X/Y is therefore uniform among all 2^k square roots of one modulo n. Exactly two sign vectors are trivial: all plus gives gcd(X-Y,n)=n, and all minus gives gcd(X-Y,n)=1. Every other vector gives a proper factor. Thus, conditional on any fixed selected relation,

    Pr[proper factor] = 1 - 2^(1-k) >= 1/2.

The same proof applies to integer relation exponents if at least one is odd. An all-even relation has no sign-randomness guarantee. The selector must not use the unrevealed x_i or any equivalent information about their signs; viewing residues and deterministic oracle answers alone is safe, while viewing the roots can invalidate the calculation.

Equivalently one may put t_i=x_i/r_i modulo n and compare product t_i with h. This gives the same gcd outcome because the omitted product of r_i is a unit.

### Scope and unsolved acquisition problem

This is a congruence-of-squares argument in the classical random-squares tradition; Dixon is the relevant prior credit, not a novelty claim. The exact argument above is supplied rather than inferred solely from that attribution.

Nothing here proves that a nonempty relation will be available after polynomially many queries or polynomial bit work. If the selector succeeds with probability rho, the argument yields rho*(1-2^(1-k)), not an unconditional half-success guarantee. Nor does a single proper factor automatically finish the complete-factorization task on arbitrary inputs.

Uniform unit sampling is a hypothesis of the lemma. Ordinary rejection sampling with an unbounded stopping time does not itself satisfy the target's worst-case random-tape and runtime bounds. A complete proposed reduction would need bounded sampling, failure accounting, and suitable amplification within polynomial resources. Those steps do not fix the missing relation-acquisition theorem.

## 2 Every exact square product dependency in a fixed explicit batch is accessible without C7

### Statement

Given explicit positive integers m_1,...,m_t with total binary input length L, a deterministic polynomial-time algorithm using no C7 oracle computes a basis over F_2 for the vector space

    V = {epsilon in F_2^t : product_i m_i^epsilon_i is an integer square}.

A basis describes every dependency; the algorithm does not enumerate an exponentially large set of all dependencies. For any returned vector, the product has O(L) bits, so its positive square root can be computed and checked in polynomial time.

### Elementary polynomial factor refinement

Maintain distinct integers b>1 with a nonnegative exponent column e_b=(e_{1b},...,e_{tb}) satisfying

    m_i = product_b b^e_{ib}.

Initialize with b=m_i and the corresponding unit columns, discard m_i=1, and merge equal bases by adding columns. Whenever distinct bases a,b have g=gcd(a,b)>1, remove their columns u,v and insert

    a/g with column u,
    b/g with column v,
    g   with column u+v.

Discard bases equal to one and merge any duplicates by adding columns. This preserves every m_i. It includes the cases g=a or g=b.

For termination, let P be the product of the distinct current bases. Before duplicate merging, this step changes their product from ab to (a/g)(b/g)g=ab/g. Duplicate merging can only decrease it further. Thus log_2 P decreases by at least one per step. Initially log_2 P <= sum_i log_2 m_i < L. There are fewer than L refinement steps, and at most L bases at any point, each of at most L bits. Each exponent is at most log_2 m_i, since its base is at least two. Scanning all base pairs at each step, with ordinary gcd and exact division and exponent-column additions, therefore gives a polynomial bit algorithm. No prime factorization is used.

At termination the distinct bases b_1,...,b_u are pairwise coprime. This is a gcd-free or coprime basis. Faster standard factor-refinement algorithms are due to Bach, Driscoll, and Shallit and to Bernstein; the intentionally elementary argument above suffices to verify polynomiality for this recovery.

### Exact parity constraints

Use deterministic integer square-root tests on each b_j. For each nonsquare b_j, form the row

    (e_{1j} mod 2,...,e_{tj} mod 2).

Square bases contribute no row. For a subset vector epsilon, put E_j=sum_i epsilon_i e_{ij}. Because the b_j are pairwise coprime, the product of all b_j^E_j is square if and only if each b_j^E_j is square. If b_j is square, this is automatic. If b_j is nonsquare, at least one of its prime exponents is odd, so b_j^E_j is square exactly when E_j is even. The unknown prime factorization is needed only to justify this equivalence; the square-root test identifies the relevant bases without it.

Therefore V is exactly the kernel of the displayed binary matrix. Gaussian elimination computes its basis in polynomial time. Omitting the perfect-square tests and requiring even exponents for every gcd-free basis element would be wrong: a square basis such as 4 imposes no condition.

For example, the batch (12,75) refines to bases 3,4,25. Only the base 3 contributes a parity condition, so the vector (1,1) is detected; 12*75=900 is a square.

### Consequence and boundary

Since m_i=r_i^2 s_i, a subset product of the m_i is square exactly when the same subset product of the s_i is square. Thus C7 does not add access to the exact square-product dependency space of a fixed, already explicit batch.

This observation does not reconstruct every C7 answer, eliminate adaptive uses of C7 in generating a later batch, or rule out exploitation of answer magnitudes, additions, modular reductions, or other bit operations. It isolates the gap in treating oracle normalization alone as a new polynomial relation-acquisition mechanism.

## 3 Equal norm representations and the reduced transporter denominator

### Exact hypotheses and convention

Let n be odd and squarefree, s a positive integer, and x,r,x',r' integers such that

    x^2 - s r^2 = x'^2 - s r'^2 = K,
    n divides K,
    K != 0,
    gcd(2 s r r',n)=1.

In the squarefree-oracle application s is squarefree, but that is not needed for this algebraic lemma. The nonzero-norm requirement K!=0 is essential and is made explicit here; it was missing from the compressed preliminary statement.

Work in the quadratic algebra Q[T]/(T^2-s), so the convention also makes sense for s=1. Put z=x+rT and z'=x'+r'T. Both are invertible because their norm K is nonzero. The transporter from z to z' is

    z'/z = (A+B T)/K,
    A = x x' - s r r',
    B = x r' - x' r.

Let h=gcd(|A|,|B|,|K|), and choose

    a=sign(K) A/h,
    b=sign(K) B/h,
    c=|K|/h.

Then c>0, gcd(|a|,|b|,c)=1, and the reduced transporter is (a+bT)/c. Direct multiplication gives

    a^2-s b^2=c^2,
    a x+b s r=c x',
    b x+a r=c r'.

Using the inverse transporter replaces B by -B and leaves c unchanged. Conjugating exactly one of the two representations is a different operation and interchanges the relevant local sign convention; it must not be silently substituted.

### Denominator theorem

For each prime p dividing n, all of s,r,r',x,x' are units modulo p. In particular, the slopes y=x/r and y'=x'/r' are defined modulo p and have equal nonzero squares s. Therefore y'=y or y'=-y, and these are distinct because p is odd.

The claim is

    gcd(c,n) = product_{p|n, y'=-y modulo p} p.

Here is the prime-adic proof, including arbitrary valuations of K.

If y'=-y modulo p, then

    B=x r'-x' r = 2 x r' modulo p,

which is nonzero. Thus p does not divide h, and v_p(c)=v_p(K)>0.

If y'=y modulo p, put C=x r'+x' r. Then C=2 x r' modulo p is a unit. The exact identity

    B C = (x r'-x' r)(x r'+x' r)
        = K(r'^2-r^2)

shows that p^v_p(K) divides B. This includes the case r'^2=r^2, when the product identity and the nonzero C force B=0. Also

    r A = -x B + K r',

so, since r is a p-adic unit, p^v_p(K) divides A. Hence h cancels the entire p-power in K, and p does not divide c. This proves the formula. Merely observing A=B=0 modulo p would not have sufficed when v_p(K)>1.

As a direct check, since B vanishes exactly at the same-sign primes,

    gcd(c,n) = n/gcd(B,n).

Only the squarefree intersection gcd(c,n), not c itself, equals that divisor. The full reduced denominator c may also contain primes outside n and higher prime powers. For example, n=15, s=1, (x,r)=(11,4), and (x',r')=(-11,4) give K=105 and c=105, while gcd(c,n)=15.

Thus the squarefree intersection of the denominator with n is another expression for the standard sign-separating gcd of the supplied representations. It gives a proper factor only if the sign pattern changes at some but not all primes. It gives 1 if all signs agree and n if they all flip.

### Limitations

The algebra is polynomially computable from the supplied integers. It gives no method to find a second representation with the same nonzero K, appropriate unit conditions, and a mixed sign pattern in polynomial worst-case time. No general reduction follows.

When K=0, division by z is not justified in the quadratic algebra and the displayed transporter construction is undefined. When 2srr' is not coprime to n, the two distinct local signs and cancellation proof can fail. Removing either hypothesis would require a separate treatment.

## 4 Verification and status

The accompanying script tests 45,000 squarefree-input normal forms, 509 explicit batches against exhaustive subset square tests, complete root-sign counts for small odd squarefree composites, and 71,332 equal-norm transporter instances, including high valuations of K and both local sign cases. These tests support error detection; the proofs above provide the general derivations. They do not establish independence of review or the missing complexity and acquisition assertions.

Turn 2 remains preliminary and unaccepted. The original problem remains unresolved.
