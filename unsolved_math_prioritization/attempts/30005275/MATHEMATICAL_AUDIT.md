# Independent audit of the degree three exponential sum classification

## Decision

**Theorems A and B and obstruction examples C–E are accepted at their stated scope. No mathematical proof correction is required. The required source-description correction is applied in [SOURCE_REVIEW.md](SOURCE_REVIEW.md).** The complete theorem statements and proof are byte-for-byte unchanged. The corrected source account records the extra conditions in the cited arXiv-v1 definition and its internal convention tension.

The full classification for arbitrary-degree integral polynomials remains **OPEN in both prime regimes**. No novelty conclusion follows from the historical or literature searches.

The distributed manuscript is [PROOF.md](PROOF.md), 13,571 bytes; SHA-256 `faa1a1b4cf32de451341580494bef9c3875d4cf960ba1df3d375212cd2efd878`. [ACCEPTANCE.json](ACCEPTANCE.json) binds the exact distributed proof and audit. The original manuscript is preserved byte for byte. The complete historical author and audit inventories and bound inputs were checked against external hashes; integrity verification is distinct from mathematical acceptance.

This AI-assisted manuscript and audit are unrefereed. Acceptance does not mean external human peer review, journal acceptance or formal proof-assistant certification. The complete mathematical arguments and every substantive audit finding are retained. Programs, raw outputs, generated certificates, datasets, copied source documents/text/images and private coordination material are excluded from this proof-only edition. Historical check counts are supplementary metadata in [SOURCE_METADATA.json](SOURCE_METADATA.json).

## Exact accepted scope

For a prime p at least 11 and polynomials f,g over F_p of reduced degree at most three, equality of the normalized magnitudes at one nonzero frequency is equivalent to equality at every nonzero frequency. The complete list is:

1. Constant with constant.
2. Nonconstant linear with nonconstant linear.
3. Quadratic with quadratic.
4. Cubic with cubic exactly when g(X)=f(uX+v)+w for u nonzero in F_p and v,w in F_p.
5. Nonconstant linear with a translated pure cubic A(X-r)^3+C exactly when p is 2 modulo 3.

There are no other cross-degree cases. For depressed cubics AX^3+BX and CX^3+DX, the nonzero-B,D case is exactly B^3/A=D^3/C; the B=D=0 case is exactly that C/A is a cube; exactly one zero is impossible.

For rational polynomials of degrees at most three, equality for every sufficiently large prime permits the first four cases only, with rational u,v,w in the cubic case. Finitely many denominator and degree-loss primes are excluded. Equality at merely one prime or an infinite selected subsequence of primes does not imply this rational conclusion.

These statements answer a bounded-degree subproblem of [OWR 50/2022, Problem 4](https://ems.press/content/serial-article-files/46986), PDF page 38, printed page 2932. The original question has two separate prime quantifiers and no degree-three restriction. It does not assert universal affine equivalence.

## Independent proof audit

### Cyclotomic reduction and signs

Expanding S_f(a) times its complex conjugate gives the Fourier transform of the integer difference-count vector D_f. Its total mass is p^2. If two squared magnitudes agree at a nonzero frequency, their difference polynomial, of degree at most p-1, vanishes at a primitive p-th root. Divisibility by the minimal polynomial Phi_p forces all its coefficients to be the same rational number; the zero total mass forces that number to vanish. Thus D_f=D_g, with no numerical approximation or positivity assumption needed.

The same reasoning applied to a single fiber-count vector proves that a nontrivial sum vanishes exactly for a permutation function. Its coefficient sum p forces the multiple of Phi_p to be one.

Odd functions have real sums because the terms at x and -x are conjugate. After choosing one sign epsilon from equality of real absolute values, the polynomial formed from n_h-epsilon n_k is a multiple of Phi_p. Summing coefficients gives that multiple as 1-epsilon. This yields either identical fiber counts or the genuine complementary alternative n_h+n_k=2. The proof does not illegitimately assume the positive sign. Reducing the fiber identity against t^j gives the signed moment identity only in the stated range 1<=j<p-1. The zero-sum permutation case permits either sign and is handled separately.

### Both cubic moment formulas

In (AX^3+BX)^j, choosing i cubic factors gives exponent j+2i. The power sum in F_p is -1 at a positive multiple of p-1 and zero otherwise.

For p=6m+1, r=2m. At j=r, only i=r contributes, giving -A^r. At j=r+2, only i=r-1 contributes, giving -binom(r+2,3)A^(r-1)B^3. Here p>=13 and the maximum exponent p+5 is strictly below 2(p-1).

For p=6m+5, r=2m+2. At j=r, i=r-1 gives -r A^(r-1)B. At j=r+2, i=r-2 gives -binom(r+2,4)A^(r-2)B^4. Here p>=11 and the maximum exponent p+7 is strictly below 2(p-1).

In both cases r+2<p-1. The integers r and all factorial arguments in the displayed binomial coefficients lie below p; hence the coefficients being divided out are nonzero in F_p. Powers with B=0 are retained rather than cancelled improperly. There is no unhandled second multiple of p-1 in the accepted prime range.

### Cubic rigidity and conjugation

In the 1-modulo-3 regime, the first moment gives A^r=epsilon C^r. Cubing and using 3r=p-1 forces epsilon=1. Dividing the second equality by this nonzero first moment yields B^3/A=D^3/C. For nonzero B,D, u=D/B satisfies C=Au^3. When B=D=0, the first moment instead gives (C/A)^r=1, precisely the cube subgroup criterion. If only one of B,D vanishes, the second moment rules it out.

In the 2-modulo-3 regime, the first moment proves that B=0 if and only if D=0. Both-zero cubics are permutations because cubing is bijective. Otherwise division of the two nonzero first moments again gives the coefficient invariant and u=D/B. The resulting actual input substitution implies equality of the first moments, so a negative sign is impossible in this nonzero case.

Input and output translations preserve magnitudes. Depressing cubics is legal because p>3, and reversing the translations gives exactly g=f(uX+v)+w. Output negation causes no missing extra class: for odd depressed h, -h(X)=h(-X). Thus conjugation is already included. Arbitrary output scaling is not automatically allowed, and is not silently inserted into the theorem.

### All degree and degeneracy cases

The constant magnitude is sqrt(p). Attaining the maximal unnormalized magnitude p forces all unit summands to have the same argument, hence f is constant as a function. A polynomial of degree less than p representing that function is constant as a polynomial.

Nonconstant linears are permutations. In the 1-modulo-3 regime the nonzero r-th moment excludes cubic permutations. In the other regime it forces the depressed linear coefficient to be zero, and pure cubics are indeed permutations. This proves the only linear/cubic overlap and explicitly includes its zero sums.

For AX^2, the invertible change (x,y) to (x-y,x+y) gives D(0)=2p-1 and D(t)=p-1 otherwise. Thus all quadratics have normalized magnitude one and cannot match constants or linears.

For the remaining cubic/quadratic comparison, r is the first index of a nonzero moment. All positive indices below r have maximum exponent less than p-1; T_0=p=0 in F_p. The bound 0<2r<p-1 is valid in both prime regimes. If D_h were the quadratic vector, its weighted 2r-th moment would be zero. Expanding the same weighted moment as a double sum leaves only index r: (-1)^r binom(2r,r)T_r(h)^2. This is nonzero since 2r<p. The contradiction excludes all remaining cubic/quadratic cases. In particular, no unjustified Weil bound or assumption of a nondegenerate cubic enters this step.

### Rational descent and prime quantifiers

A fixed rational polynomial has its degree and relevant nonzero coefficients preserved outside finitely many primes. The finite-field classification therefore excludes distinct degrees apart from the possible linear/pure-cubic case. Infinitely many primes are 1 modulo 3, so that exception cannot hold at all sufficiently large primes. The elementary construction with a divisor of N^2+N+1 is correct: taking N divisible by 3 and every prime in a purported finite list excludes both 3 and the listed primes, and gives multiplicative order exactly three.

For nonzero depressed linear coefficients, congruence of B^3 C and D^3 A at all sufficiently large primes forces equality over Q after clearing denominators. Then u=D/B is rational. The input shifts and output shifts used in depression are rational as well.

For two pure cubics, c=C/A is nonzero. If c is not a rational cube, X^3-c is an irreducible separable cubic. Its finite Galois splitting field acts transitively on the three roots; its group therefore contains a 3-cycle. [Chebotarev, as stated by Sharifi in Theorem 7.2.2](https://www.math.ucla.edu/~sharifi/notes/algnum-ch07.html), supplies infinitely many primes in that Frobenius conjugacy class. Excluding the finitely many denominator, discriminant, and ramified primes makes reduction separable with no linear factor. This contradicts c being a cube at every sufficiently large prime. All hypotheses of this standard imported theorem and the factorization interpretation are satisfied. Chebotarev itself is not reproved in this audit.

The rational conclusion would be invalid for only infinitely many primes: X^3 and 2X^3 already agree whenever p is 2 modulo 3, but 2 is not a rational cube. The audit includes exact controls at p=11 and p=13 for this distinction.

## Obstruction examples and small primes

C is correct: X^6=(X^3)^2 and cubing permutes F_p when p is 2 modulo 3. Thus X^2 and X^6 have equal actual sums, and their nonzero normalized magnitudes are one for odd such primes. Their distinct degrees exclude affine equivalence even allowing nonzero output scaling over C. There are arbitrarily large primes in this residue class by the elementary 3P-1 argument. For primes 1 modulo 6, the collision counts 2p-1 and 6p-5 differ, so equality cannot persist for all sufficiently large primes.

D is correct: for p=1 modulo 4, (1+i)^4=-4 and 1+i is nonzero. For p=3 modulo 4, the fourth-power and square maps have identical image and fiber sizes, while multiplication by -4 changes squares into nonsquares. The two fiber counts are complementary, giving opposite nontrivial sums and equal magnitudes. Rational input scaling with output sign restricted to +/-1 would require u^4=-4 or u^4=4. The former is impossible over the reals; the latter is impossible by the 2-adic valuation of a rational fourth power. General complex affine equivalence does hold, as the report acknowledges.

E is correct: at p=5 the two stated cubic fiber vectors are complementary. Matching depressed cubics by an input affine substitution forces its translation to be zero; the linear coefficient then forces u=4, incompatible with the cubic coefficient. The independent checker also examined depressed cubics at p=7 and found no counterexample there; this is only a finite boundary control and is not used to lower the proved sufficient bound. Primes 2, 3, 5 and 7 are outside Theorem A. No claim of sharpness of the p>=11 bound is accepted or required.

## Source correction and dependency limits

The retained [arXiv v1](https://arxiv.org/abs/2107.06527v1), Definition 1.6 on PDF page 4, explicitly imposes simple roots of f and deg(f')=d-1, in addition to squarefree f' and distinct critical values. The original source account omitted the first two conditions; the distributed [SOURCE_REVIEW.md](SOURCE_REVIEW.md) includes them. This was verified both in the full bound text and visually from the PDF.

The independently required correction, applied in the distributed source account, corrects that omission. It also records an inconsistency in that source version: Lemma 6.1(2) claims invariance under arbitrary output translations, while a translation can move a critical value to zero and create a multiple root of f. This audit neither silently repairs that prior source nor relies on this disputed convention. Theorems A and B have no Morse or Sidon assumption and do not use that theorem.

The odd-polynomial condition in the symmetric Sidon–Morse definition must be retained. The stated characteristic restrictions of Theorem 6.3 are correct. The Wisconsin talk's twelve handwritten pages were independently viewed; they announce restricted generic rigidity and ask about indecomposability, without giving an unrestricted classification. The [2026 equicritical-quartic article](https://doi.org/10.1093/imrn/rnag141), section 5.3 and Corollary 5.3.1, is about p^2 and is not imported into the prime-modulus proof. The primary author publication and unpublished-note lists were checked again; absence of a later named manuscript there remains bounded negative evidence, not a novelty certificate or a proof of globally open status.

This audit does not certify every neighboring theorem or upgrade bounded negative search results into exhaustive history. Edition preparation rechecked frozen input bytes and publication integrity without new scholarly-source retrieval, source-text inspection, literature search or mathematical-computation reruns. Only Chebotarev is imported as a non-elementary proof dependency; the Sidon–Morse, monodromy, classification and equicritical-quartic machinery are not imported.

## Reproduction and independent controls

The author checker was rerun in normal and -O modes. Both outputs are byte-identical to the supplied receipts: **74,766 depressed cubics over 22 primes from 11 through 101, with 149,532 individual moment comparisons**. The enumeration trace hash is `04f6a89eb40a1150e89b15b89c64a6156369481771badfbcf3aca011e80ed053`. The number 74,666 is incorrect. The 149,532 count refers to moment comparisons, not separately enumerated polynomial pairs.

The checker compares every magnitude signature to an affine-input orbit key and conversely, so it tests the complete equivalence relation on its finite normalized domain without enumerating all pairs. Its integer packed convolution is safe: the base exceeds p^2, which bounds every ordinary convolution coefficient. The author also compares direct convolution for all B at A=1. The six deliberately wrong formulas were all rejected in both normal and -O modes, reproducing the supplied twelve failure receipts exactly.

The independent checker imports no author code and uses explicit ordered-pair difference counts plus the actual affine input group action, rather than the author's invariant or packed convolution. In normal and -O modes it passed:

- All 15,300 coefficient triples for degrees at most three at p=11,13,17,19, including 14,360 cubic triples. Arbitrary output constants were separately checked in 257,044 histogram-translation cases.
- All 371 odd functions at p=3,5,7, verifying the identical-or-complementary fiber alternative.
- Another 33,620 depressed cubics at p=103,107,109, with 67,240 direct exact moment checks.
- Thirty-nine exact adverse examples covering zero sums, nonzero quadratic/sextic equality, failure in the other prime regime, quartic arithmetic twisting, pure-cubic noncubes, output scaling, conjugation, affine shifts, and cubic/quadratic separation.

An initially mistyped translation witness used coefficient 21 in place of 28; the independent harness rejected it. The corrected identity and the incorrect version, now expected to fail, are both retained as controls. This was a test-fixture correction, not an alteration of the author proof.

The author integrity verifier passed in normal, -O and -OO modes. Seven integrity mutations were tested in each mode: missing file, extra file, same-size tamper, manifest tamper, resealed full-solution promotion, resealed scope-metadata change, and resealed proof change. All 21 combined checks rejected the mutation. A coordinated proof change plus self-reseal is naturally accepted by a self-consistency checker; the independently supplied original manifest pin rejects it. This distinction is explicitly preserved.

Neither the finite enumeration nor its hashes prove a universal theorem. Acceptance rests on the independent algebraic and arithmetic arguments audited above.

## Required disposition

Accept the degree-at-most-three results and the precisely scoped examples. The source-description correction is applied in [SOURCE_REVIEW.md](SOURCE_REVIEW.md), without changing [PROOF.md](PROOF.md). The original manuscript and source account remain preserved. Keep the arbitrary-degree target unresolved in both regimes and make no novelty claim.
