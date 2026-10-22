# Independent adversarial audit: exceptional-unit prefixes

Problem 30002048 / OWR-11784-007, rank 622. Audit date: 2026-10-04 UTC.

## Verdict

**The scoped mathematics passes independent exact verification:** e(7)=5, e(8)=7, e(9)=6, and E0(alpha)<[Q(alpha):Q] for every root of unity alpha. No fatal defect or hidden coefficient-height restriction was found in these proofs.

**One false ancillary sentence must be corrected**, in ROUTES.md Route 2. A second correction removes ambiguous polynomial notation in PROOF.md Section 5. Both are supplied as an unapplied patch. Neither changes the scoped theorem or any computed certificate.

**The source conjecture remains unresolved by this packet.** Its quantifier is every exact algebraic degree d>=7. The surviving gap is non-root-of-unity algebraic integers of exact degree at least 10. Five substantive routes were recorded; their number is not evidence of completeness of the global conjecture. No historical-priority claim is certified.

## 1. Frozen identity, preservation, and independence

The initial and final author manifest checks passed for every entry. The audited frozen identifiers are:

- MANIFEST.sha256: `4a4a0478c91311606382e2ae00aa891d93272992593724e976589ab9ef65cf6c`
- PROOF.md: `daec8f3b2c6b91a7ea00f243c1e19454f542c3c1393c074d3174f4e404e615ba`
- results.json: `e37ca1501357df7094f28c5c73f5e8ed44ed74266787b12f1134d53af848848c`

The independent implementation was written and passed before either author program was inspected or run. It reads no author program and can reproduce its mathematical results without any author file. The optional JSON comparison is performed only after reconstructing all results.

Algorithmic differences from the author implementation:

1. CRT uses polynomial extended Euclid and rational CRT idempotents, not inversion of an 8-by-8 coefficient matrix.
2. Fixed resultants use the Sylvester matrix with exact Fraction elimination, not a quotient-ring multiplication determinant with Bareiss elimination.
3. Degree-nine quartics are expanded symbolically by all 24 permutations of a 4-by-4 polynomial matrix, not recovered by interpolation.
4. All integer roots are found within a coefficient-derived Cauchy root bound, not by enumerating divisors of the constant term.
5. Irreducibility is proved by testing every monic divisor through half the degree over a finite field, not by the Frobenius criterion.

All arithmetic is exact and uses only Python's standard library. No floating-point result is used. No helper agent, remote write, source-document redistribution, or retry of the denied OWR PDF download occurred. Existing lawful web-rendered OWR text and the two available Stewart PDFs were inspected. Fresh PDF text extractions exactly matched the supplied text files. The author directory was not modified.

## 2. Exact source, hypotheses, and provenance

The primary [Oberwolfach report](https://ems.press/content/serial-article-files/46395?nt=1), printed pp. 1334-1335, attributes the contribution to Cameron L. Stewart. It begins with a nonzero algebraic integer, takes K=Q(alpha), and defines the consecutive positive-exponent prefix in the full ring of integers. It then asks for the strict bound in all degrees at least seven. Report 22/2012 and DOI 10.4171/OWR/2012/22 are consistent; the catalogue's 2013 report label is incorrect.

Both linked mathematical papers are by C. L. Stewart, not Hare--Mossinghoff:

- [Exceptional units and cyclic resultants](https://uwaterloo.ca/pure-mathematics/sites/default/files/uploads/documents/aa155-4-05.pdf), Acta Arithmetica 155 (2012), 407-418, especially Section 9, pp. 415-417. Its explicit conclusions include e(7)<7 and e(8)>=7. Its larger class of monic polynomials includes reducible polynomials. The degree-seven prefix-six examples have a factor x; they are not degree-seven algebraic-number witnesses.
- [Exceptional units and cyclic resultants, II](https://uwaterloo.ca/pure-mathematics/sites/default/files/uploads/documents/exceptional_units-5_0.pdf), Sections 5-6 and Table 1. The table contains all three lower-bound witnesses used in the packet. It restricts coefficients to {-1,0,1} and the constant coefficient to +/-1, so its maxima alone are not unrestricted upper bounds for e(d). The publication data, Contemporary Mathematics 587 (2013), 191-200, are independently confirmed by [Stewart's institutional publications page](https://uwaterloo.ca/pure-mathematics/cameron-stewart/refereed-conference-proceedings).

Hare is acknowledged for computational assistance. Mossinghoff appears in related references. Their names cannot replace Stewart's authorship.

The nonzero hypothesis matters for degree one: alpha=0 would give an infinite prefix. It does not narrow any degree-7/8/9 assertion. Exact degree means the degree of an irreducible minimal polynomial, not merely the degree of a polynomial having alpha as a root. Alpha itself is not assumed to be a unit. The source's effective general bound justifies finiteness of the maxima; the displayed witnesses attain the scoped values.

Targeted searches using the paper titles, exceptional units, e(7), e(8), e(9), and the conjectural inequality did not establish a later resolution or historical priority for the scoped equalities. Search failure proves neither novelty nor that no later theorem exists. This audit validates the mathematics and attribution, not a comprehensive literature-history claim.

## 3. Unit criterion and signs

Let f be the monic minimal polynomial of alpha, of degree d. Define A_n=Res(Phi_n,f), B_n=Res(x^n-1,f). Then exactly

- N(alpha^n-1)=Res(f,x^n-1)=(-1)^(dn) B_n;
- N(Phi_n(alpha))=Res(f,Phi_n)=(-1)^(d phi(n)) A_n;
- B_n=product of A_m over m|n, with no sign in this displayed order.

An algebraic integer is a unit in O_K if and only if its field norm has absolute value one. This does not require Z[alpha]=O_K. Because all the resultants are integers, the consecutive norm conditions through N are equivalent to |A_1|=...=|A_N|=1. There is no dropped divisor or sign hypothesis.

For n>=3, primitive roots occur in nonreal conjugate pairs; their f-values multiply to nonnegative real numbers. Thus A_n>=0 and |A_n|=1 means A_n=1. For n=1,2, A_n is respectively f(1), f(-1); both signs must be allowed. The independent verifier checks both resultant orders and cyclic factorization at all 21 witness indices, explicitly including the odd-degree sign reversals at 1 and 2. Every signed author value agrees.

## 4. CRT completeness and integrality

For S={1,2,3,4,6}, P=product Phi_m=x^8+x^6-x^2-1. Division by the monic P preserves integral coefficients.

A remainder ax+b at the three quadratic moduli has norm a^2-ab+b^2, a^2+b^2, or a^2+ab+b^2. Completing the square bounds each integer coefficient to {-1,0,1} when the norm is one. Direct enumeration therefore gives exactly 6, 4, and 6 possibilities, alongside 2 at each linear modulus. No unit-group assumption beyond these elementary norm forms is required.

For every one of the 576 tuples, the verifier constructs its rational CRT solution and rechecks all five remainders. The common-denominator histogram is:

- denominator 1: 24 tuples;
- denominator 2: 120;
- denominator 3: 72;
- denominator 6: 360.

The 24 integral remainders are exactly +/- (x^j mod P), 0<=j<=11, and are distinct. This explicitly rejects the invalid shortcut of treating the moduli as comaximal over Z[x]. Since P is monic, every admissible integral f has the unique form Pq+r with integral q and one of these r. There is no imposed bound on the coefficients of f or q.

## 5. Degree-by-degree upper bounds

### Degree seven

For a monic degree-seven f with a prefix of at least six, q=0. Precisely three integral residues have degree seven and leading coefficient one:

x^7; x^7+x^5-x; x^7-x^3-x.

All have a factor x. This excludes all irreducible degree-seven f and gives e(7)<=5. The zero-root polynomial x^7 cannot be admitted as a degree-seven minimal polynomial.

### Degree eight

The monic quotient is 1, so all possibilities are P+r, with 24 choices. A_5=1 leaves exactly seven, and A_7=1 leaves exactly x^8, F, G, where

F=x^8+x^7+x^6+x^5-x^2-x-1,
G=x^8+x^7+x^6-x^3-x^2-x-1.

The first is reducible. Both others have A_8=9. Therefore a prefix of eight is impossible at exact degree eight. The independent data include all seven intermediate polynomials and their complete signed A_1,...,A_8 lists, matching the author table.

### Degree nine

Write unambiguously f(x)=P(x)(x+a)+r(x), a in Z. For each of the 24 r, Q_r(a)=A_5(f)-1 is an exactly computed quartic. Its leading coefficient is Res(Phi_5,P)=5, so none is identically zero.

The audit expands each determinant symbolically. It then uses the bound |z|<=1+max_{i<4}|q_i/q_4| for every complex root of Q_r. The largest resulting integer bound among these 24 quartics is 10. This is a proved root bound derived after the unrestricted reduction, not a heuristic coefficient-height cutoff. Every integer in the derived interval is tested exactly. All 24 quartics and all their integer roots agree with the author data; 16 distinct quartic coefficient lists occur.

There are precisely 15 pairs (r,a) satisfying A_5=1. After A_7=1, only x^9, xF, and xG remain. Each has zero constant coefficient and is reducible. Thus e(9)<=6. In particular there is no residual infinite one-parameter family hidden behind the calculation.

## 6. Lower witnesses and exact degree

The witnesses, already in Stewart II, have the following audit-certified data:

- f_7=x^7+x^6+x^5+x^4-x^2-x-1. A_1,...,A_6=(1,-1,1,1,1,7).
- f_8=F. A_1,...,A_8=(1,-1,1,1,1,1,1,9).
- f_9=x^9+x^8+x^7+x^6+x^5-x^3-x^2-x-1. A_1,...,A_7=(1,-1,1,1,1,1,8).

Irreducibility is independently proved by exhaustive division over F_2, F_2, and F_5 respectively. Every reducible monic degree-d polynomial over a field has a monic divisor of positive degree at most floor(d/2). The tests exclude all 14, 30, and 780 such polynomials respectively. No unverified factorization-oracle result or mere absence of linear roots is substituted for irreducibility. Monicity ensures reduction preserves degree, so irreducibility over the finite field implies irreducibility over Q. Thus these are witnesses at exact degrees 7, 8, and 9, attaining prefixes 5, 7, and 6.

## 7. All roots of unity

For a primitive m-th root with m>=2, set Q=max_{p^a || m} p^a. If alpha^j has order h>1, its norm obstruction is Phi_h(1) raised to phi(m)/phi(h). Phi_h(1) equals a prime when h is a prime power and equals one otherwise. Order one gives zero.

If h is a power of p, every other full prime-power factor of m divides j. Hence j>=m/p^a>=m/Q. At j=m/Q, the order is exactly Q and the first nonunit occurs. Consequently E0(alpha)=m/Q-1. The possible order-one failure cannot occur earlier. For m=1, alpha=1 has E0=0.

If ell is the largest prime divisor of m,

m/phi(m)=product_{p|m} p/(p-1) <= product_{k=2}^ell k/(k-1)=ell<=Q.

Thus E0<=phi(m)-1<phi(m), in every order, with no asymptotic assumption. As controls rather than the proof, direct cyclic resultants were independently checked through the first failure for all orders 2 through 80: 225 exact resultants. The edge case m=1 is checked separately. This establishes only the root-of-unity branch.

## 8. Ancillary routes and required corrections

### C1. False single-cyclotomic-resultant equivalence

ROUTES.md, Route 2, says that |A_j(f)|=1 forces f and x^j-1 to be coprime modulo every prime. As written this is false.

Exact counterexample: f=x-1 and j=6. A_6=Phi_6(1)=1, whereas B_6=0 and x-1 divides x^6-1 over every finite field. This counterexample is also evaluated by the independent script.

Replace the sentence with:

"Equivalently, |B_j(f)|=1 holds if and only if f and x^j-1 are relatively prime after reduction modulo every rational prime; this is also equivalent to |A_m(f)|=1 for every m dividing j."

For the single quantity |A_j|, the correct comparison polynomial is Phi_j. The theorem proof always uses the full consecutive family and is unaffected by this isolated error.

### C2. Ambiguous degree-nine notation

PROOF.md writes f=P(x+a)+r. Since P(x+a) conventionally denotes composition, its literal reading has degree eight. Replace it with f(x)=P(x)(x+a)+r(x). The derivation and both programs already use the product, so this changes notation, not the computation.

### Remaining route checks

- The local prime-ideal order obstruction E0<=t-1<=N(p)-2 is valid when alpha is nonzero modulo that prime ideal. For a nonunit alpha, primes dividing alpha cannot provide that obstruction.
- The squarefree-M construction x^d+M H, with deg H<d, is correctly Eisenstein at each prime dividing M. H(0)=-1. It passes the stated finite-prime coprimality tests and has the stated shorter exact prefix. It is not a global-conjecture counterexample and does not show that a sieve supplemented by stronger global conditions could never work.
- The archimedean route lacks the asserted uniform near-unit-circle control needed at some exponent n<=d. The quoted general estimate does not imply the coefficient-one bound.
- The substitution identity B_n(f(x^k))=B_{n/g}(f)^g, g=gcd(n,k), is exact with the stated resultant order. Independent direct Sylvester computations recover the eight displayed prefixes 5,8,7,8,5,10,5,8. No irreducibility or extrapolation to arbitrary k follows from these controls.

## 9. Reproduction and release boundary

From this audit directory, run:

    python3 independent_verify.py > fresh.json

This uses only the standard library and needs no source files. To perform the optional all-field comparison with the frozen author JSON, run:

    python3 independent_verify.py --author-json ../author/results.json > fresh-with-comparison.json
    cmp fresh-with-comparison.json independent_results.json

Run without Python's -O option: assertions are part of the certificate. Two complete runs under Python 3.12.14 took about 8.2 seconds in this environment. All generated mathematical fields agree; polynomial lists are compared by content, independent of enumeration order.

After the independent pass, the author verifier reproduced results.json byte-for-byte. The author's SymPy cross-check also passed. Those additional passes are reproducibility controls, not the basis of independence.

The supplied proposed_corrections.patch is not applied to the frozen author directory. Before treating the whole manuscript as clean, incorporate C1 and C2 into a new author snapshot and regenerate its manifest. The scoped theorem can be reported as independently verified. The full target must retain **unsolved**, and the known examples must remain credited to Stewart. Do not describe this audit as a solution of the all-degree conjecture or evidence of historical novelty.
