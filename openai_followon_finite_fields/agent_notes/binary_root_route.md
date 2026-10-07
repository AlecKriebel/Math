# Optional binary-exponent root route and priority audit

Audit time: 2026-10-07 05:24:53 UTC (2026-10-06 Pacific). This is an additional research note, outside the frozen `unpublished-record-v3` package. No frozen manuscript, manifest, receipt, repository index, publication state or tracker was changed. No external individual was contacted. The upstream clone and its pinned copies were read only.

## Result and disposition

There is a rigorous elementary companion: in an explicitly represented finite field K of order q, one can decide whether x^r=a has a solution and produce one solution deterministically in time polynomial in the field encoding, log(r), and a **numeric** bound B for the largest prime factor of gcd(r,q-1), using the already justified dense factorization algorithm. Thus B bounded by a fixed polynomial in the input bit length gives a true bit-polynomial statement, even when r itself is exponentially large. No integer-factorization oracle is needed: bounded trial division suffices. This is an inherited consequence, not a newly identified contribution. Original Adleman--Manders--Miller (1977), pp.176--177, already uses primary projections, factoring gcd(n,p-1), and repeated prime-root extraction. The accepted upstream breakthrough derandomizes the required dense factorization. This route does not justify a new-solution deposit.

The result produces **one** root, not an explicit list of all roots. The number of nonzero roots is g=gcd(r,q-1), which can itself be exponentially large in its bit length. The arbitrary-exponent case with unbounded common prime factors is not established by this route. A supplied factorization certificate alone does not make a call on X^ell-a polynomial in log(ell).

## Precise algorithm

Input: prime p (promise), monic irreducible h in F_p[t] of degree m>=1 (promise or the project's deterministic check), K=F_p[t]/(h), a in K in the power basis, integer r>=1 in binary, and numeric B>=2. Put Q=p^m-1. Assume every prime divisor of g=gcd(r,Q) is at most B. The weaker promise on g suffices; no smoothness of the part of r coprime to Q is required.

```
root(K, a, r, B):
    if a == 0: return 0
    Q = p^m - 1
    g = gcd(r, Q)
    M = Q / g
    if a^M != 1: return NO_ROOT
    if M == 1: return 1
    u = inverse_mod(r/g, M)
    c = a^u
    D = g
    factor a separate copy of g through 2,...,B, recording multiplicities
    if a residual factor remains: return OUTSIDE_SMOOTHNESS_SCOPE
    for each recorded prime ell, with multiplicity:
        factor X^ell - c over K
        choose any linear factor X-z
        c = z
        D = D / ell
    verify c^r == a
    return c
```

The scope rejection is not `NO_ROOT`; membership was already decided independently. For g=1 the list is empty. The M=1 branch covers q=2 and cases where r is divisible by Q; successful membership forces a=1. The zero branch is valid because r is positive. Each ell divides Q and hence differs from p, so every called binomial is separable. In fact it is completely split, because it has a root and K contains all ell-th roots of unity. Root choice may be by the lexicographically first linear factor for a fully specified deterministic procedure, although the proof permits every choice.

## Correctness, including arbitrary choices

Let G=K* be cyclic of order Q and use a generator only in the proof; the algorithm never finds one. The image of the r-th power map is G^g. Writing a=gamma^k shows that a belongs to this image exactly when g divides k, equivalently a^(Q/g)=1.

The valuations of r/g and Q/g cannot both be positive at any prime, so gcd(r/g,M)=1. For M>1 the modular inverse u therefore exists. Since a^M=1, (a^u)^(r/g)=a. Also c=a^u remains in G^g. It suffices to find a g-th root of c.

Here is the invariant that prevents stranding. Suppose D divides Q, c belongs to G^D, and ell divides D. Write c=gamma^(Dk). Every ell-th root z of c has exponent

    (D/ell)k + j(Q/ell) modulo Q,  j=0,...,ell-1.

Both terms are divisible by D/ell because D divides Q. Thus **every** root belongs to G^(D/ell). The invariant persists while the product of extracted primes is g. At termination x^g=a^u, so x^r=(a^u)^(r/g)=a. The proof also shows that the order of the prime-root calls is immaterial after reduction to g.

For comparison, extracting the prime factors of the entire r without this repair can fail. In F_3, x^4=1 has solutions. A first square-root call on 1 may return -1=2, which has no square root in F_3. The correct algorithm has Q=2, g=2, M=1 and returns 1 immediately. More generally excess valuations e>v_ell(Q) cannot be included in an arbitrary-choice chain. A primary-component formulation projects onto the ell-Sylow subgroup using the exponent (Q/ell^s)*inverse_mod(Q/ell^s,ell^s), with s=v_ell(Q); when e>=s the image there is {1}, so it is tested and assigned root1. The gcd algorithm obtains the same bypass without constructing every projector.

## Full parameter accounting

Let L=ceil(log2(p)), R=ceil(log2(r+1)), H=mL, and t be the number of prime factors of g counted with multiplicity. Then t<=log2(g)<=H. Computing Q uses integers of at most H+1 bits; gcd, division, modular inversion and all exponent encodings have bit length O(H+R+log(B+1)). These are ordinary deterministic integer operations. Bounded trial division uses at most B candidate divisions plus O(H) successful divisions, on numbers of at most H bits. A discovered divisor is prime because all smaller candidate prime divisors have already been removed. Alternatively, a supplied complete factorization of g can be checked by multiplication and primality checks; the numeric maximum factor B must still be charged.

Each factorization input has degree ell<=B, at most B+1 coefficients, and coefficient encoding length at most mL bits. The quotient dimension is ell over K (m*ell over F_p); a Berlekamp matrix has ell rows and columns over K. Using the project's trace implementation, there are at most m*ell calls to the prime-field split-root procedure per binomial, each on a polynomial of degree at most ell. Across the entire root chain, this gives at most t*m*B calls and summed oracle degrees at most t*m*B^2. These bounds deliberately charge numeric B. The direct p-fixed variant can remove the leading m from the oracle-call count, at the cost of its m*ell dimensional F_p matrix.

If T_K(n) is the validated deterministic bit complexity of degree-n factoring over the supplied K, total work is bounded by

    O(t*T_K(B)) + poly(B,H,R),

including building the binomials, extracting linear factors, membership testing, field exponentiation, final verification, and the promised representation check. More explicitly, membership and u exponentiation require O(H) field multiplications each; direct final exponentiation uses O(R) multiplications (or first reduces r modulo Q). Schoolbook K multiplication costs O(m^2*(L+1)^2) bits. All intermediate field coefficients have at most m coordinates of L bits. The existing factorization theorem supplies a polynomial T_K(B), with its enormous fixed upstream exponent retained; there is no practical-efficiency claim. If B<=S^c for a fixed c and total input size S including the field, a, r and B, this bound is polynomial in S. A mere binary encoding of arbitrarily large B does not give that conclusion.

No factorization of Q, p-1, or the entire r is performed. Trial division of the bounded common part is an actual algorithm, not an integer-factorization oracle. Characteristic-p factors of r occur in its part coprime to Q and are handled by the modular inverse. Thus characteristic two and exponents divisible by p do not need an inseparable degree-r polynomial call.

## Independent finite falsification checks

An in-memory Python3 check on 2026-10-07 tested the invariant for every cyclic additive group order 1<=Q<=160, every D dividing Q, every prime ell dividing D, every member of D*G, and **all** possible ell-root choices: 37,856 root branches passed. A second check tested Q<=80, r<=200, and every solvable a, taking the largest available root at each extraction step: 473,806 full cases passed. The mathematical proof above, rather than this finite test, establishes the unbounded claim. No field enumeration occurs in the claimed algorithm; these deliberately small cyclic-group tests use enumeration only to attempt falsification.

Reproduction uses the following standard-library check (Python3, no files required):

```
from math import gcd
isprime = lambda n: n > 1 and all(n % d for d in range(2, int(n**0.5)+1))
branches = cases = 0
for Q in range(1, 161):
    for D in range(1, Q+1):
        if Q % D: continue
        for ell in range(2, D+1):
            if D % ell or not isprime(ell): continue
            for a in range(0, Q, D):
                roots = [x for x in range(Q) if (ell*x-a) % Q == 0]
                assert roots and all(x % (D//ell) == 0 for x in roots)
                branches += len(roots)
for Q in range(1, 81):
    for r in range(1, 201):
        g = gcd(r, Q); M = Q//g
        for a in range(Q):
            if a % g: continue
            if M == 1:
                x = 0
            else:
                c = (a*pow(r//g, -1, M)) % Q; D = g; ell = 2
                while D > 1:
                    if D % ell: ell += 1; continue
                    roots = [v for v in range(Q) if (ell*v-c) % Q == 0]
                    assert roots
                    c = roots[-1]; D //= ell
                    assert c % D == 0
                x = c
            assert (r*x-a) % Q == 0
            cases += 1
assert (branches, cases) == (37856, 473806)
```

## Exact check of the 2017 zero-free route

Primary source: Bhargava--Ivanyos--Mittal--Saxena, arXiv:1702.00558v1, submitted 2017-02-02 07:20:18 UTC; Section6.2, Conjecture6.3 and Theorem6.7. The conjecture has a **common** epsilon<1/2 and a two-sided open strip for nontrivial Dirichlet zeros. Its least-prime-field-nonresidue conclusion is a fixed logarithmic power with exponent 4/(1-2*epsilon). This is positive earlier attribution for the nonresidue mechanism; the paper does not justify replacing polynomial dependence on a prime root degree by dependence on its logarithm.

The accepted family029 Theorem1.2 is enough. Take F=Q(mu_12). For any Dirichlet character chi, pullback by the idele norm gives a finite-order Hecke character eta. Abelian base change expresses its Hecke L-function as the product of the Dirichlet L-functions L(s,chi*psi), with psi ranging over the characters of Gal(F/Q), up to harmless finite Euler factors. In Re(s)>1-delta, delta=10^-6, these factors are holomorphic except for permitted principal poles at s=1. A zero of L(s,chi) away from1 would therefore be a zero of the Hecke product, contrary to029. Classical nonvanishing at1 treats the remaining point. Finite removed Euler-factor zeros have real part0. Functional equations, applied to all conjugate characters, give the other side. Choosing epsilon=1/2-delta/2 handles the strict interval, including a possible zero on Re(s)=1-delta, and yields the coarse exponent4/delta=4,000,000. This implication uses the accepted mathematical theorem; it is not a new verification of its analytic proof or a Lean claim.

One displayed estimate in BIMS Lemma6.4 should not be copied literally: at truncation height sqrt(x), the ordinary explicit formula includes an O(sqrt(x)*log^2(px)) truncation term rather than merely O(log^2(px)). The corrected term is absorbed by x^(1/2+epsilon)*log^2(px), so the nonresidue conclusion still follows by the same argument. Also identify finite-field roots of unity with complex roots of unity before treating chi_r as a complex Dirichlet character. In the weighted difference S(M), real parts of 1-chi_r are nonnegative; a zero sum forces every contributing prime power to have character1, and multiplicativity then gives the same property for every integer up to M. These checks do not introduce an unsupported binary-prime root bound.

## Priority evidence and exact gap

1. Adleman--Manders--Miller, *On taking roots in finite fields*, FOCS1977, pp.175--178, DOI10.1109/SFCS.1977.18. I visually read all four pages of the author-hosted primary scan. TheoremsIII--IV p175 are conditional on ERH; the displayed bound in IV is O(n^n*log^(c+1)(p)+a), not poly(log n). LemmaIV p176 gives coprime component projection. The first paragraph p177 explicitly reduces through factoring gcd(n,p-1) and repeated prime roots. Its compressed final-cofactor wording should not be used as justification for arbitrary choices with excessive valuations; the cofactor-inverse-first proof above supplies the exact invariant. The mechanism is nevertheless explicit prior work.
2. Cao--Sha--Fan, *Adleman--Manders--Miller Root Extraction Method Revisited*, arXiv:1111.4877v1, 2011-11-21. Section5 Table4 uses an order-r subgroup discrete logarithm; Section6 charges brute-force O(r*log^2(q)) per such logarithm, for its stated total O(log^4(q)+r*log^3(q)). The randomized nonresidue search can be derandomized under an appropriate zero-free input, but the numeric r term remains. This is an exact earlier warning against conflating r with log(r).
3. BIMS2017 Section1 already reduces composite exponents to repeated prime extraction; Section6.2 explains fixed zero-free strips and nonresidue search. Combined with the classical group decomposition and the core dense factorization consequence, bounded-prime binary exponents are an immediate companion. No independent first-priority or new-solution assertion is warranted.

The unresolved gap for unrestricted binary r is the potentially very large prime divisor ell of gcd(r,q-1). Calling degree-ell factorization or brute-force order-ell discrete logarithms simply transfers this difficulty into numeric ell; it is not a bit-polynomial repair. The optional route supplies no genuinely new in-scope core theorem and must not delay or reopen the inherited-core publication disposition on the basis of a cosmetic stronger parameter statement.

## Sources and redistribution boundary

Search/inspection date: 2026-10-06 Pacific / 2026-10-07 UTC.

- BIMS exact HTML: https://arxiv.org/html/1702.00558v1 ; primary PDF https://arxiv.org/pdf/1702.00558 . Research-only downloaded PDF SHA256 `2d6a885ba03f9be2f1ceeb7d7841a97f40c6ba930696e71335406320385c77c5`, 210070 bytes.
- AMM author primary scan: https://www.cs.cmu.edu/~glmiller/Publications/AMM77.pdf ; SHA256 `934ea272c596c56ac1598295802853ca5c066e3c1faf481b3b124dc32af87aeb`, 1598993 bytes.
- Cao--Sha--Fan primary preprint: https://arxiv.org/html/1111.4877 ; https://arxiv.org/pdf/1111.4877 . Exact Sections5--6 inspected through primary HTML/PDF extraction; no redistributed PDF is claimed.
- Family029 exact introductory statement: pinned `sources/pinned/preprints/Primitive-roots-for-every-admissible-integer-base-October-4-2026/build/sections/01-introduction.tex`, lines37--63. Commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`; hashes already recorded by the project manifest. Family003's earlier explicit quadratic-nonresidue/square-root consequences were checked and are not relabeled as new.

Downloaded third-party sources and rendered AMM pages are confined to `sources/root_audit_research_only/` for local research. They are not part of an authorized upload kit or an owned publication artifact and must not be staged or redistributed by default. A temporary disk-space error blocked one attempted independent proof-only agent spawn and a source-download heredoc; after space became available, downloads and the in-memory checks completed. No files were deleted and no independent subagent review is claimed.
