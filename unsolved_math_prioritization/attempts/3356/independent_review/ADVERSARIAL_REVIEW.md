# Independent scoped review: problem 3356

## Verdict

**PASS for the stated partial results and finite theorem. Original problem remains UNSOLVED, five of five substantive author turns used. No mandatory mathematical revisions.**

The reviewed packet neither proves the universal primitive-root assertion nor supplies a counterexample to it. Its exact finite verification, Kummer–Chebotarev progression result, quartic phase identity and finite-algebra dichotomy are sound within their stated scopes. The broader progression and exponent-42 example do not decide the exponent-four target. The additional octic sign is correctly labeled a finite observation only. No novelty or historical-priority certification is made.

This is an independent AI-assisted mathematical and executable audit, not human peer review or formal proof-assistant certification. No sixth author search was undertaken.

## Frozen input and source alignment

The input is the 29 files listed by `FROZEN_MANIFEST.json`, together with that manifest itself. Its SHA-256 is

`4941008f76b72a5dae9d853531b9c4c12267a19ced6ab7dbb3b205c19e671aea`.

All 29 listed byte lengths and hashes were checked before review. The exact original assertion is: for every prime q>3 such that p=16q^4+1 is prime, is 3 a primitive root modulo p?

The [Open Problem Garden page](https://www.openproblemgarden.org/op/primes_p_such_that_3_is_a_primitive_root_modulo_p) was independently reopened. Its 2012 anonymous comment already supplies the quadratic-reciprocity reduction to qth-power nonresiduacity; the author packet explicitly credits this. The exact polynomial equality is indispensable. Replacing it by a progression, by exact valuations of p−1, by another exponent, or by another base would change the question.

Primary-source checks:

- [Wertheim, 1896](https://archive.ymsc.tsinghua.edu.cn/pacm_download/117/5021-11511_2006_Article_BF02418029.pdf), printed pp. 145 and 148, was downloaded, text-inspected and visually checked. The general prime-power discussion retains a residual test. The universal assertion for 16q+1 on p. 148 is the exponent-one case, not 16q^4+1.
- [Wang–Zhang, section 5.1](https://zhangshenxing.github.io/publications/WangZhang2022.pdf), PDF p. 16, was downloaded and visually checked for the primary convention and norm-based quartic reciprocity sign. These agree with the conventions used in Turn 3.
- [Milne, Algebraic Number Theory, Theorem 8.31](https://www.jmilne.org/math/CourseNotes/ANTc.pdf) was read through the web PDF text view, including the natural-density convention. A separate direct local PDF download returned HTTP 406; no successful local download or visual inspection of that PDF is claimed.

The two downloaded source PDF hashes and the unsuccessful direct fetch are recorded in `source_receipt.json`. The source PDFs are not part of the portable review evidence bundle. The pinned imported record is supplementary provenance; the original source page controls the mathematical scope.

## Turn 1: order reduction and complete Lucas certificates

For the original hypotheses p≡5 mod 12, so quadratic reciprocity gives (3/p)=−1. The order of 3 thus has the complete 2-part 16 and is 16q^j for 0≤j≤4. The order-16 case is impossible: it would imply p divides 3^8+1=6562, whereas q≥5 gives p≥10001. The original question is therefore exactly the exclusion of

    3^(16q^3) = 1 (mod p).

The cyclotomic formulations are consistent with the displayed orders. They do not decide the remaining q-primary component.

The Lucas lemma is fully sufficient, without a probable-prime assumption. If n−1=N has known complete prime-factor support and b^N≡1 mod n, with gcd(b^(N/r)−1,n)=1 for every prime r dividing N, then every prime divisor ell of n has ord_ell(b)=N. Hence N divides ell−1 and ell≥n. Thus n is prime and b has order n−1. In this problem only r=2 and r=q need checking, including their full multiplicities through the exponent N/r.

A Fermat failure is a genuine composite certificate. A prime original counterexample could not pass the primitive-root certificate and would be left unresolved rather than silently classified as composite. The author scripts explicitly reject any unresolved row.

## Turn 2: Kummer–Chebotarev theorem and neighboring exponent

For a fixed prime q>3, E=Q(zeta_q,3^(1/q)) has degree q(q−1). Eisenstein irreducibility and coprime degrees justify this degree. Its Galois group is the full affine group over F_q. The commutator subgroup is exactly its translations: conjugating translation by 1 by multiplier 2 and taking the commutator recovers that translation. Consequently its maximal abelian subfield is Q(zeta_q).

For M=96q^5 and C=Q(zeta_M), it follows that E∩C=Q(zeta_q). The residue a=16q^4+1 is coprime to M and equals 1 modulo q. Therefore the pair consisting of identity on E and the a-automorphism on C is a compatible, unique automorphism of EC. It is central, so Chebotarev gives a singleton class of natural density

    1/[EC:Q] = 1/[q phi(M)] = 1/[32q^5(q−1)].

Conversely, a prime in the stated residue class with 3 a qth power has all q roots of X^q−3 in its residue field, since q divides r−1. It has the same splitting Frobenius on E. Thus the displayed density applies to the full set in the proposition, not merely to a subset constructed in its proof.

The arithmetic r−1=16q^4(1+6qk) gives the asserted exact valuations and r≡5 mod 12. This proves infinitely many bad primes in a larger fixed-q progression. It says nothing that selects k=0. The author makes this limitation explicit.

The cyclic-group character control is correct after choosing c≡q^−1 mod 16 with q not dividing c. Then g^(qc) has index q but agrees with g on all characters of order dividing 16. The text explicitly makes the needed correction to the initially bounded choice of c.

The neighboring example

    q=5, m=42, r=3637978807091712951660156250001

has a valid base-6 full Lucas certificate. Base 3 has exact order

    727595761418342590332031250000 = 16*5^41,

by the two prime-divisor order tests. These arithmetic values were independently recomputed. It is a counterexample only to the broader varying-exponent assertion, as clearly stated in the packet.

## Turn 3: quartic sign and residual equivalence

The chosen associates pi=1−4iq^2 and rho=−3 are primary, with norms p and 9. The reciprocity sign exponent is 4q^4 times 2 and is even. Reduction modulo 3 gives pi≡1−i, whose square is i in F_9. The fourth roots of unity remain distinct there. The supplementary factor for −1 is 1. Thus (3/pi)_4=i.

Under the specified identification with F_p, i=(4q^2)^−1=−4q^2 because 16q^4≡−1. Therefore the proved identity is indeed

    3^(4q^4) = −4q^2 (mod p).

No conjugate-associate or unit sign has been suppressed. Both the formula and the choice of primary primes agree with the checked primary reference.

Writing s=−4q^2 and x=3^(4q^3), one has x^q=s and ord(s)=4. Since q is odd, q is its own inverse modulo 4, and x^4=1 is equivalent to x=s^(q mod 4). The two signs displayed in Turn 3 are correct and the implication is bidirectional.

The octic square-root alternatives ±8q^3 follow from the explicit eighth root 2q. The more precise sign involving (q/3) is only checked on a finite sample and is not used as a universal theorem. Neither the proved quartic phase nor any character of order dividing 16 can by itself determine the missing q-part.

## Turn 4: exhaustive finite theorem through q=100,000,000

The complete author scan was rerun, not just its smaller smoke tests. Its exact mathematical totals, endpoints, example certificates and canonical stream hash agree with the frozen output. The elapsed runtime differs and was appropriately excluded from mathematical comparison.

- Prime q with 3<q≤100,000,000: 5,761,453
- Proper small-factor certificates: 3,346,393
- Fermat composite certificates: 1,997,047
- Full Lucas prime-and-primitive certificates: 418,013
- Unresolved cases: 0
- Total certified composite values: 5,343,440
- Certificate-stream SHA-256: `5805127c93aa572ae3f1e129aad3930685103d3d1cecf7c330061b85dace0b00`

The segmented prime-q sieve includes the stated endpoint and starts marking each progression no earlier than the square of its prime. The small-divisor wheel follows from (2q)^4≡−1: its odd prime divisors satisfy ell≡1 mod 8 and have exactly four relevant roots. Every marked factor is checked by actual division. Every wheel prime is below the smallest possible p and hence is a proper factor. A later overwrite of a wheel mark does not invalidate a still-verified divisor.

Every prime-q row receives one of the stated exact certificates or causes an unresolved failure. No probabilistic primality test is used. The completeness of the sieve, the complete factorization of p−1 and the Lucas lemma justify the finite theorem.

The full per-q streams are generated and hashed during the scan but are **not retained in the frozen remote bundle**. A digest alone is not a stored certificate stream. This review certifies the audited algorithm and its complete replay, with independently reconstructed first-turn controls; it does not claim an absent row file was inspected or archived. The finite conclusion is exactly that any original counterexample must have q>100,000,000.

## Turn 5: Frobenius dichotomy

The algebra A=F_p[T]/(T^q−3) is reduced since p is neither q nor 3. For beta=3^((p−1)/q), beta^q=1 and T^p=beta T. On the basis 1,T,...,T^(q−1), Frobenius has eigenvalues 1,beta,...,beta^(q−1).

If beta=1, Frobenius is identity and the reduced algebra is a product of q copies of F_p. If beta≠1, it has order q; the fixed subspace has dimension one. A product of finite fields has fixed-space dimension equal to its number of factors, so A is a field. Thus complete splitting and irreducibility are the only alternatives. This is precisely the unresolved residue test in algebraic form, not a selection of the irreducible branch.

For odd q the stated discriminant formula has the correct sign. Reciprocity gives (q/p)=(p/q)=1, and the discriminant is a nonzero square. Both the identity and a q-cycle have even sign. Frobenius determinant is always 1. The trace and norm observations are consistent with both possibilities and add no missing exclusion.

The q=17 control was replayed and independently supplemented with many finite-field cases. The changed base 3^17 is expressly a control, not an original base-3 counterexample.

## Executable independence and reproducibility

All five author checkers were rerun; mathematical JSON outputs match the frozen outputs. `AUTHOR_REPLAY_RECEIPT.json` records these comparisons and replay hashes. Compact replay outputs are included, but full row streams are not.

`independent_checks.py` imports no author checker. It uses a separately written odd-index sieve, binary modular exponentiation, Euclidean gcd and exact integer/finite-field calculations. It independently reconstructs every first-turn row through q≤1,000,000 and its canonical digest, obtaining 78,496 prime-q cases, 70,827 composite values and 7,669 certified prime primitive-root values. It also checks the neighboring exponent certificate, the quartic phase and residual equivalence, character controls, the affine commutator and degree arithmetic, and 5,984 small finite-field examples of the Frobenius dichotomy.

The independent output contains **89,896 exact assertions**. These supplement the analytic proofs; finite examples do not prove reciprocity, Chebotarev, or the universal original conjecture.

Run the independent controls with:

    python independent_checks.py > replay_independent.json

Compare parsed JSON with `independent_output.json`. The original five command lines are in the frozen `FINAL_README.md`; Turn 4 must use the complete 100-million bound to reproduce the full finite theorem.

## Final disposition

Retain **unsolved, 5/5** for problem 3356. The sharp original gap is to exclude beta=1, or find an original counterexample, for primes q>100,000,000 with p=16q^4+1 prime. The progression theorem, classical quartic phase and invariant calculations leave this exact diagonal obstruction open. No mandatory revision is needed to publish the packet with this scoped disposition.
