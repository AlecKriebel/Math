# Independent audit: polynomial shifts in the ADKT Corollary 5 family

This AI-assisted manuscript is unrefereed. Acceptance records an independent internal AI audit, not external human peer review, journal acceptance, or formal proof-assistant certification.

The complete written proof and explicit polynomial and finite-field certificates are retained. This is not a computational reproduction package: executable code, raw integer search tables and square-root witnesses, copied source documents and images, and private coordination material are omitted. Historical finite checks are supporting evidence; the universal restrictions follow from the written arguments. The historical computations cannot be reproduced from this edition alone.

The original infinite four-total-shift question remains unresolved by this work. No novelty, priority, exhaustive literature-survey, or current-openness claim is made.

This edition preserves the complete independent logical audit. Its computational and source-inspection statements describe the original audit, not new editorial executions or scholarly-source inspection. Exact finite integer shift sets and example triples are omitted; historical counts, match results, coverage and the complete enumeration argument remain. No mathematical correction was required.

## Verdict

**PASS for the precisely restricted theorem and its stated consequences. The original infinite four-total-shift problem remains unresolved by this result.**

No mathematical correction is required in the audited `POLYNOMIAL_OBSTRUCTION.md`. The proof exhausts all polynomial shifts in Q[x] for the displayed family, including shifts without a positivity restriction, when the three products plus the shift are squares in Q(x). Exactly the three listed shifts survive. The rational-section corollary and the additional eventual-uniform-formula consequence are valid with their stated restrictions.

The bounded integer calculations independently reproduce all reported shift sets at precisely 1 <= i <= 1000, the six cited source examples, and the two credited later finite leads. They are not a proof about all integer parameters. This audit does not certify novelty, current worldwide-open status, elliptic-curve ranks or generators, a proof-assistant formalization, or the later website's claimed verification.

## 1. Identity and source scope

The audited candidate has 18 payload members. Its manifest SHA-256 is `138461ebc75d0c53fe969c845896921790c294dcce496478b807f44d1668d335`. All declared byte counts, file hashes, complete membership, and the external seal fields matched. The external seal itself is 375 bytes, SHA-256 `0fbd9bf06d43f4fbceca2c82cc19519ec525e8f194256036e60aa0fdaebc7840`.

Primary source: Adzaga, Dujella, Kreso and Tadic, *Triples which are D(n)-sets for several n's*, [arXiv:1703.10659v1](https://arxiv.org/abs/1703.10659), 2017. The retained PDF is 154,418 bytes, SHA-256 `3b9a897a78d3e354ff62c4af0d85e5d203cc33a86a79c96d01df7fe9c9e9c73f`. I independently extracted and visually inspected physical pages 6-9. Corollary 5 gives the family used here. Section 3 asks the infinite four-total-shift question and gives finite examples; Remark 3.1 supplies the divisor method. The six examples appear in the page-9 table. Page 8 displays c without Corollary 5's leading factor 4. Its rank/generator discussion is not used. A fresh public PDF text inspection corroborated these locations and the v1 identity; it did not establish an independently downloaded byte-for-byte remote match.

The original target was checked: infinitely many distinct positive-integer D(1) triples with three further pairwise distinct integer shifts, all different from 1. This is four total shifts, with no additional positivity requirement on the shifts themselves.

## 2. Parameter identification, known shifts, and positivity

Set x=i+1. Independent symbolic substitution verifies exactly

- a=2x(x-1), b=2x(x+1), c=4(2x^2-1)(4x^2-1);
- n1=1;
- n2=4(8x^4-5x^2+1);
- n3=4(64x^8-112x^6+64x^4-13x^2+1).

Both expanded shift polynomials reproduce the expressions printed in Corollary 5. All nine square identities in Section 1 of the candidate were independently expanded and checked over Q[x]. The identities n2=a+b+c and n3=(a+b+c)^2/4-ab-ac-bc also pass.

For integer x>=2, a>0 and b-a=4x>0. The candidate's factorization
c-b=2(4x^2-x-2)(4x^2+x-1) is correct; both factors are positive on this range. The positive difference a(x+1)-a(x)=4x shows distinct triples as x varies. The factorizations of n2-1 and n3-n2 are correct and positive for x>=2. Thus the known family has three distinct positive integer shifts, including 1, but does not itself supply the requested fourth shift.

## 3. Squares in Q(x), factor exhaustion, and units

If h in Q(x) satisfies h^2 in Q[x], write h=p/q with coprime p,q in Q[x]. The identity p^2=h^2 q^2 forces q to be constant by unique factorization. This also covers h=0. Therefore for polynomial n one may use polynomial square roots t,s,r in Q[x] of ab+n, ac+n, bc+n respectively. There is no hidden assumption that rational-function square roots were initially polynomial.

Independently verified identities are

- N=b(c-a)=4x(x+1)fg, where f=4x^2+x-2 and g=4x^2-x-1;
- D=c(b-a)=16x(2x^2-1)(4x^2-1).

The two quadratic discriminants are 33 and 17, neither a rational square. Together with x and x+1, these are four pairwise nonassociate irreducibles. Consequently every factor in N has multiplicity one. From U=r-t and V=r+t, one obtains UV=N. Neither U nor V is zero because N is a nonzero polynomial.

Every factorization in Q[x] is therefore U=k d and V=4 e/k, with k an arbitrary nonzero rational unit and d,e complementary products of the four displayed factors. Negative units are allowed. No integrality or positivity restriction is imposed on k. Constant factors d=1 or e=1 are included. All 16 subsets occur before identifying complementary pairs.

Changing t to -t swaps U and V and preserves n. Under this swap one can replace (d,e,k) by (e,d,4/k). Selecting the smaller-degree representative, and one representative of each equal-degree pair, leaves exactly masks 0,1,2,3,4,5,6,8. Independent enumeration of all 16 masks confirms this list. There is no missing sign, unit, constant, or repeated-factor case.

This argument also bounds degrees without assuming a degree bound on n at the outset: U and V divide a fixed degree-six polynomial, so both have degree at most six. The proof examines every resulting case.

## 4. Degree and coefficient reconstruction

The final square condition is

Q=(U+V)^2-4D=(2s)^2.

In all cases m=max(deg d,deg e) is 3, 4, 5, or 6, while deg D=5. If the two degrees differ, the highest-degree term of U+V comes from V alone. If they are both three, the leading coefficient is L=4(k^2+4)/k. This cannot vanish for a nonzero rational k. It follows that deg Q=2m with leading coefficient L^2.

Any polynomial square root of Q has degree m and leading coefficient either L or -L. Its sign can be chosen to make the leading coefficient L. Subsequent coefficients are uniquely forced because 2L is nonzero. Thus coefficient comparison misses no roots and admits no spurious branch. The independent implementation reconstructed coefficients from their convolution equations, rather than loading any candidate computation output as proof.

The independent residual checks give:

- mask 0: coefficient of x^5 is -512;
- mask 1: coefficient of x^4 is 512;
- mask 2: coefficient of x^3 is -32;
- mask 3: full remainder 8(k^2-4)(x^3-x^2);
- mask 4: constant coefficient -96k^2;
- mask 8: constant coefficient -360k^2.

The first, second, third, fifth, and sixth entries exclude those cases, since k is nonzero. Mask 3 requires k^2=4. Both signs k=2 and k=-2 yield n3, and all remainder coefficients vanish after these substitutions.

## 5. Cubic cases and the finite-field certificates

For masks 5 and 6 I independently reconstructed all coefficients of Q and its only possible square root. Both displayed formulas for R2 and R1, including every coefficient of A5,B5,A6,B6, their scalar factors, and denominator powers, agree exactly with the resulting rational functions after z=k^2.

The denominators introduce no missing rational case: k is nonzero and k^2+4 is positive. If z differs from 4, simultaneous vanishing of R2 and R1 would force A and B to have a common root.

The two displayed Bezout identities were verified with a separate, handwritten finite-field polynomial multiplication/addition implementation:

- over F3 for A5,B5, the certificate sum is exactly 1;
- over F7 for A6,B6, the certificate sum is exactly 1.

In both cases reduction preserves the degree of both polynomials: neither leading coefficient is divisible by the chosen prime. The modular argument is consequently valid, rather than an unjustified arbitrary specialization. More explicitly, if there were a nonconstant common rational factor, choose it primitive in Z[z] and use Gauss's lemma to obtain integral cofactor factorizations. Its leading coefficient divides each original leading coefficient, so it is not divisible by the prime. Its reduction therefore remains nonconstant and divides both reductions, contradicting the certificate. Content factors cannot invalidate this reasoning because the original leading coefficients are prime units.

As an additional independent check, rational polynomial gcd computations also return 1 for both pairs. Altering a Bezout coefficient by 1 makes each modular check fail. These supplementary checks are not substituted for the explicit certificates.

Thus masks 5 and 6 also require z=4, equivalently k=+/-2. Both signs yield n1 and n2 respectively. All remaining coefficients vanish at these values, and the already checked square-root identities establish sufficiency. Together with Section 4, this proves the exact classification for Q[x].

## 6. Rational functions, integer specializations, and exceptional points

The rational-function integrality lemma is valid. For a nonpolynomial rational function F, polynomial division gives F=P+H with P in Q[x] and nonzero proper H. A single positive integer M clears the finitely many coefficients of P, so MP(m) is an integer for every integer m. Whenever F(m) is integral and defined, MH(m)=MF(m)-MP(m) is also integral. Because H tends to zero at positive infinity, MH(m) has absolute value below one for all sufficiently large m. Hence it must vanish there. A nonzero rational function has only finitely many zeros, so integral evaluations are confined to a finite set. The finitely many poles are excluded from the domain; removable singularities are handled by reducing the rational expression.

Apply the lemma to a fixed rational section F with all three shifted products square in Q(x). If F is not a polynomial, it supplies integral shifts for at most finitely many positive integer x. If F is polynomial, the classification identifies it with one of the three known shifts, so it never yields a distinct fourth shift. Taking a fixed finite union preserves finiteness of the exceptional parameter set. There is no dependence on rank or an asserted generating set for an elliptic curve.

At integer parameters where a rational-function square root is defined, an integral square of a rational number is automatically an integer square. Poles or exceptional points cannot invalidate the obstruction: there are only finitely many such points for each fixed section. For a finite list, their union remains finite. The statement does not assert a uniform bound for all sections together.

The restrictions matter. An infinite list of different sections, sections chosen anew at each integer, rational functions after a non-affine algebraic parameter change, and other triple families are outside the conclusion. A rational function in a new algebraic parameter need not be a rational function of the original x. The audit makes no extension to those settings.

## 7. Eventual-square fact and arithmetic progressions

Section 6's auxiliary fact is also correct. Let P in Q[x] be a rational square at all sufficiently large integers. If P is not zero, it is eventually positive. Choose a positive integer M clearing its coefficients. The values u_m=M sqrt(P(m)) are rational and have integer squares M^2 P(m); hence u_m are integers.

Put d=deg P and K=floor(d/2)+1. On a sufficiently large positive real interval, the positive square root is smooth and has an asymptotic expansion x^(d/2) times a convergent smooth power series in 1/x. Differentiating K times gives O(x^(d/2-K)), which tends to zero. This justifies the derivative estimate used in the candidate, including constant P and even degrees where leading derivatives may vanish faster.

The K-th forward difference is the integral of the K-th derivative over a unit K-cube and is therefore an integer tending to zero. It eventually vanishes. Newton interpolation then makes the eventual sequence a rational-coefficient polynomial of degree at most K-1. Squaring on infinitely many integer arguments proves a polynomial identity, so P is a polynomial square over Q. This is an exact eventual-all-integers argument; it does not apply merely because P is a square at infinitely many isolated integers.

For a rational-function shift valid at every sufficiently large positive integer parameter, integrality first forces polynomiality, and the auxiliary fact makes each of the three square conditions a polynomial square identity. The classification then applies. The same reasoning holds for a fixed progression x=qj+r of integer parameters, with integer q>0 and integer r: substitute first and use the invertible affine Q-algebra substitution. The progression restriction is not a license for a general algebraic base change or an arbitrary infinite subsequence.

## 8. Complete finite enumeration and precise bound

For a fixed positive triple a<b<c and any integral shift n satisfying all three square conditions, take the nonnegative roots t and r of ab+n and bc+n. Since r^2-t^2=b(c-a)>0, r>t. Thus d=r-t and e=r+t are positive integers with de=N, d<=e, and the same parity. Conversely each such divisor pair uniquely determines nonnegative integral t=(e-d)/2 and r=(e+d)/2, hence n=t^2-ab; the remaining test is whether ac+n is a nonnegative integer square. This proves completeness without an artificial bound on n and includes negative n, n=0, and t=0.

The audit's independent enumerator uses trial division of the known factors, constructs all divisors, verifies their count and uniqueness, tests exact integer square roots, and compares full rows (triples, N, prime factors, eligible-pair counts, shifts, and witnesses). Candidate programs were neither executed nor imported.

Results:

- All 1,000 family rows for i=1,...,1000 agree exactly.
- Exactly two of the 1,000 checked family parameters have more than three shifts. The complete raw shift sets are omitted from this edition.
- All six source-table triples have exactly the four printed shifts.
- The two credited later finite leads have exactly the shift sets reported in the candidate. This certifies the arithmetic for those triples, not the external site's claims or the examples' novelty.
- Two independent control triples recover respectively a negative shift with a zero root and the zero shift, demonstrating that those edge cases are included. Their raw integer values are omitted from this edition.

No claim is made to reproduce the source's larger search range. In particular, this audit proves neither that the family has only two exceptional integer parameters nor that it has infinitely many. The finite checks are separate from the universal polynomial proof.

## 9. Reproducibility and acceptance boundary

The audit implementation contains explicit fail-closed checks, not Python assertions. It reconstructed and checked 8,212 conditions in ordinary Python, Python -O, and Python -OO. The three resulting receipts are byte-identical. A separate manifest checker and isolated mutation tests check the audit seal and complete membership; those integrity controls establish the state of the evidence, not mathematical truth by themselves.

The original audit included retained-source extraction and page renderings for inspection. This edition distributes only authored mathematics and permissible verification metadata, without copied source text, source renderings, raw integer search tables, executable code, or private coordination material.

Final disposition: accept the exact polynomial-shift obstruction, the fixed-finite-section integrality obstruction, the eventual-uniform-formula consequence, and the finite arithmetic at their stated scopes. Retain **PARTIAL_NOT_SOLVED** for the original target.
