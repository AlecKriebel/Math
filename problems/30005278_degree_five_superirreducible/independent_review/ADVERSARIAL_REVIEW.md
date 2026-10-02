# Independent full source/proof audit: scoped PASS

Problem30005278 / OWR-11695860-018. The complete five-turn packet passes within its stated scope, with no mandatory correction. The original degree-five existence question remains **unsolved5/5**. This is AI-assisted mathematical review, not formal certification or human peer review; no novelty certification is supplied.

The verdict binds FINAL_AUTHOR_MANIFEST.json SHA256 5bed4b4e5e34969f73a03505d5106eb008caaed3682511ba53edec253c449c7e, comprising35 bound files and36 including the manifest. All earlier proofs remain unchanged. Turn5 legitimately closes the integrality substep left open in historical Turn2; it does not solve the remaining rational-point question.

## Exact source and dependencies

OWR printed2945 was visually inspected. The source's compressed degree-at-most-two wording is correctly interpreted using the same authors' later explicit positive-degree and fraction-field definitions. Constant substitutions or content factors are not a resolution. The quintic X^5+2X+1 and the ax²+c result are credited to Du. The primary finite-field paper's Capelli lemma works in Q(theta), and the packet correctly uses this root field rather than the full splitting field. The local proof supplies its own denominator control, so the imprecise splitting-field terminology in the cited manuscript is not inherited as an assumption.

Conrad's stated Dedekind and Chebotarev theorems were checked against the exact uses. They are established external inputs; the packet does not claim to prove effective prime-search bounds or foundational Galois theory. Integer/rational substitutions and nonmonic/monic hypotheses are kept distinct.

## Turn1: dyadic classification

The reduction F2[X]/(X^5+1)=F2×F16 is reduced. Therefore squaring a nonzero primitive coefficient vector remains nonzero modulo2, giving w(z²)=2w(z), even though the dyadic algebra is not a field. This justifies power-basis integrality of a primitive square root without assuming a global integral basis.

The theta² coefficient modulo4 forces the remaining exceptional cubic coordinate even; primitivity then makes the constant coordinate odd. Writing z=1+2u is consequently legitimate. The two residue-field Artin–Schreier conditions force the linear coefficient divisible by8 and the constant coefficient congruent1 modulo8. The contraction on the complete finite-free Z2-algebra proves sufficiency. Scaling gives the full rational2-adic criterion, including zero coefficients and product-algebra issues.

The resulting split condition for integer quadratics is exactly b nonzero and v2(a)>2v2(b). Only nonsquareness is used to infer global irreducibility; the opposite direction is not claimed. The degree-ten modulo11 example is independently irreducible and correctly illustrates local squareness without global reducibility. The specialized Rouche/Perron argument establishing quintic irreducibility is sound.

## Turn2: global equations and exceptional cases

The five reduced coefficients and three quadratic equations agree with exact quotient-ring multiplication. Every zero-coordinate case is handled with its divisions justified. The rational-root lists exhaust the stated primitive integer polynomials; the quartic-coordinate case is excluded by a5-adic valuation. The denominator t−s² cannot vanish at a rational solution because its exceptional equation is f(s)=0.

The identity R(s,s²)=f(s)² and the elimination formulas preserve both directions of the rational-point correspondence. A normalized nonconstant square root cannot have constant square: that would give a quadratic subfield of a degree-five field. The finite coefficient box is explicitly diagnostic and is not used to claim a complete rational-point list. Its initially retained integer-congruence condition is later addressed by Turn5.

## Turn3: prime certificates and norm limitations

The norm formula and discriminant11317 are correct. The mod17 factorization has irreducible factors of degrees2 and3, giving a transposition; transitivity gives a5-cycle. Their conjugate edge transpositions generate S5 because the underlying five-vertex graph is connected. The unique quadratic subfield is therefore the discriminant field.

In the composition splitting field, the total-sign character on the product of the five square roots detects whether a lifted5-cycle is a10-cycle. If sqrt(D) is in the quintic splitting field, that character factors through S5 and is trivial on5-cycles. Otherwise a kernel element with odd sign changes a lift into a10-cycle. Both implications are valid even if the composition has not initially been shown irreducible. A10-cycle then forces transitivity before Chebotarev is invoked. The nonmonic-to-monic change and exclusion of leading-coefficient primes correctly bridge the stated monic primary theorem.

The two excluded norm square classes precisely describe failure of a full-degree irreducible prime reduction; they do not describe global reducibility. The infinite family P_c and its primitive constant term−1 are checked. Its irreducibility follows from the credited ax²+c theorem, while every full-degree prime reduction is reducible. Degree-drop primes are properly excluded as certificates. Thus no necessary norm condition is promoted to sufficient root-field squareness.

## Turn4: finite certificate and infinite tail

The translation/reflection normal form handles both a=2 and a=−2 and every odd b. All600 initial rows are present exactly once, with correct norms and strict square-gap certificates or negative signs. The independent check verifies coverage by the Cartesian product of the stated parameter sets, not merely a row count.

The approximate-square expansion is exact. At n=200 the two uniform bounds have strict margins; the negative-power terms decrease thereafter while 2n−40/n increases. The residual signs for r=−1,0,1 are correctly separated. These estimates put the entire infinite tail strictly between consecutive squares. The resulting three bands and additional negative-norm intervals do not cover all admissible discriminants, and no such coverage is claimed.

## Turn5: odd-degree descent and local points

For p^m dividing M and v_p(N)=n<m, the leading homogeneous term has valuation dn and all others strictly larger. A nonzero square norm therefore forces n even when d is odd. After dividing the norm identity by p^(dn), the displayed unit inverse constructs the square root modulo p^(m−n); multiplying by p^(n/2) gives the needed modulus p^m. This works at2 and when M,N are noncoprime. The high-valuation branch and |M|=1 are included. CRT then supplies a genuine integer residue.

For monic irreducible odd-degree f, clearing denominators makes the norm an integer square, and the constructed G=Mx²+2rx+(r²−N)/M has integer coefficients and the exact square discriminant over the root field. This proves the stated rational/integer substitution equivalence for the monic class. It neither applies without justification to nonmonic candidates nor turns a norm-square condition alone into a root-field square. The equivalence with absence of rational points on R follows, but that absence remains unproved.

The local binomial series converges in each finite-dimensional completion algebra with the specified small parameter; it need not be a field. Integral power-basis reductions and the Catalan denominator bound justify the p-adic estimates, including2. The five leading terms and coefficient1/1024 of A2A4−A3² are nonzero in every characteristic-zero completion, so a sufficiently small nonzero parameter gives a point in the required open part. The parameter may vary with the place. No local-global principle, rationality of analytic coefficients, or fixed global square witness is asserted.

## Integrity and disposition

All35 final manifest entries,25 historical entries and9 primary-source hash entries verify. All five author checkers replay byte-exactly, totaling78,440 assertions. The separate checker passes6,044 exact controls, including the600-row certificate,768 signed lifts,2,265 odd-degree square-norm cases with independent residue enumeration, and formal square-root identities through order12. Python3 and SymPy are required for the independent checker and author turns2,3,5; author turns1,4 use the standard library.

These finite controls supplement the written universal arguments. They do not determine the rational points of R or resolve the source existence problem. Preserve the full scoped results and prior credit; publish only as original unsolved5/5 after the publication gate.
