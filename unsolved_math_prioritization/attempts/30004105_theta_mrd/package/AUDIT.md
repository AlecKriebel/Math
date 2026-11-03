# Theta-dimension invariants: scoped prior-work audit and exact finite test

## Result and limits

This is one scoped audit of the open-ended research direction associated with OWR-16775-009, not a solution of that research direction. The precise finite target chosen here is to test the known fixed-generator collision at q=3, n=m=7, k=3, and determine whether it survives collecting all generator profiles. It does not: the two codes below have the same profiles for theta and theta inverse, but different profiles for theta squared. Their MRD property is independently certified by exhaustive finite arithmetic, not inferred from the matching profiles. No claim of novelty is made for this example or separation. This is not a proof that all-generator profiles characterize twisted Gabidulin codes, and not a counterexample to such a characterization.

## Prior work and quantifiers

1. Alessandro Neri, joint work with Sven Puchinger and Anna-Lena Horlemann-Trautmann, *Identifying rank-metric codes using Galois group action*, in *Contemporary Coding Theory*, OWR 13/2019, printed pp.828–830, [official proceedings](https://ems.press/journals/owr/articles/16775). The final research question asks about characterizing other MRD families and constructing new ones using these invariants. It does not assert an all-family completeness conjecture or designate one target family. The theta-Gabidulin characterization already appears in the preceding theorem and must not be counted as new resolution.
2. Neri–Puchinger–Horlemann-Trautmann, *Equivalence and Characterizations of Linear Rank-Metric Codes Based on Invariants*, Linear Algebra Appl. 603 (2020), 418–469, [inspected version](https://arxiv.org/abs/1911.13059v2), [DOI](https://doi.org/10.1016/j.laa.2020.06.014). Remark 6.8 gives a fixed-theta collision between twisted Gabidulin codes and monomial-support codes. It cites MRD examples with support {0,1,3}, including n=7 and odd q, and uses unequal right idealizers for inequivalence. The discussion then explicitly leaves conditions involving several theta values as a possible direction. Its negative conclusion must not be strengthened to all-generator or augmented profiles.
3. Giuzzi–Zullo, *Identifiers for MRD-codes*, Linear Algebra Appl. 575 (2019), 66–86, [inspected version](https://arxiv.org/abs/1807.09476v3), [DOI](https://doi.org/10.1016/j.laa.2019.03.030). Theorem 3.9 presents an augmented characterization of generalized twisted Gabidulin codes. Its intended nondegenerate use, 2<k<n−1, must be distinguished from defects in the inspected printed statement, discussed below. In addition to a coprime step s and two intersection dimensions k−2 and k−3, it requires an invertible linearized polynomial p, a compatible chain representation, and a nonzero eta satisfying the norm restriction and p+eta p^[sk] in the code. These existential element conditions are not dimension data. Terminology also differs across papers: this is the extension-field-linear generalized twisted family in that theorem, not a theorem about every multi-twist construction called generalized twisted elsewhere.
4. Neri–Santonastaso–Zullo, *Extending two families of maximum rank distance codes*, Finite Fields Appl. 81 (2022), 102045, [inspected 2021 preprint](https://arxiv.org/abs/2104.07602v1), [publisher](https://www.sciencedirect.com/science/article/abs/pii/S1071579722000545). Theorem 3.8 establishes the MRD property for its dimension-two family with odd q, t≥3, and relative norm −1. Proposition 4.2 and Theorem 4.3 use sum dimensions to distinguish it from Gabidulin codes and, for t≥5, twisted Gabidulin codes. This is positive use of the invariants in validating a new construction, not an invariant-only construction recipe or universal classification. Numbering refers to the inspected preprint.

## Source-statement cautions found during adversarial review

The inspected Giuzzi–Zullo Theorem 3.9 prints membership p,q in C next to the chain span of p^[s],...,p^[s(k−1)]. Read literally with p invertible, p in C would add an independent zeroth iterate: the k iterates p,...,p^[s(k−1)] are independent, since composing with p inverse reduces them to distinct Frobenius monomials. C would then be a Gabidulin chain and its first intersection would have dimension k−1, contradicting k−2. The usable interpretation is an ambient invertible p with the displayed shifted chain in C, not an additional requirement p in C. This is a statement/indexing caution in the inspected edition, not a claim about a published erratum.

The printed k>2 also cannot be used unqualified at k=n−1: any two such subspaces have intersection dimension at least n−2, whereas the stated k−2 is n−3. The safe scope of the present discussion is 2<k<n−1, and our finite example has k=3,n=7. The surrounding normal-form argument in Lemma 3.8 explains the augmented criterion: composing by p inverse, with the appropriate Frobenius shift, produces the twisted generator and untwisted chain. Theorem 3.10 goes further in intent, deducing MRD from a rank-metric code with no rank-one element plus augmented conditions, rather than assuming MRD; it shares the same printed membership caution. These results should be credited for their algebraic content without claiming a literal full theorem audit or silently dropping their element conditions.

## Equivalence and invariant conventions

For an F_(q^m)-linear code C in F_(q^m)^n, define S_i^theta(C)=sum_(j=0)^i theta^j(C), and T_i^theta(C)=intersection_(j=0)^i theta^j(C). Dimensions are over F_(q^m), with i=0 giving k. Increments of the sum dimensions contain no additional information once k is known.

The vector semilinear equivalence used by Neri–Puchinger–Horlemann-Trautmann is C'=tau(C)A, A in GL_n(q), tau an absolute field automorphism; a nonzero scalar is immaterial for an extension-field-linear code. Linear equivalence is the case tau=id. Since finite-field automorphisms commute and theta fixes A entrywise, theta^j(C')=tau(theta^j(C))A. Consequently each fixed, labeled theta profile is invariant even under semilinear vector equivalence. One does not need to forget the generator labels or permute them. Equality is only necessary for equivalence, not sufficient.

For n=m, evaluate q-polynomials on a fixed F_q-basis of F_(q^n). Coordinatewise theta becomes postcomposition by theta, including Frobenius on coefficients. For the present codes all displayed coefficients lie in F_3, so postcomposition is exactly cyclic exponent shift. Computing profiles by shifting exponents without Frobenius on arbitrary coefficients would be incorrect.

The broader polynomial/matrix equivalence convention may allow arbitrary invertible F_q-linear maps on both sides and field automorphisms (and some conventions separately allow transposition). No claim is made that labeled theta profiles are invariants for every such broader convention. Below, the right-idealizer argument supplies a separate inequivalence certificate for ordinary two-sided polynomial equivalence; the theta-profile difference already certifies the stated vector semilinear inequivalence. These claims must not be conflated.

## Exact finite target

Let F=F_3[z]/(z^7+z^2+2), let theta(x)=x^3, and use the basis 1,z,...,z^6. Work modulo x^(3^7)−x with linearized polynomials. Define

- C=span_F{x,x^3,x^27};
- H=span_F{x+x^27,x^3,x^9}.

Their three generators are independent because their coefficient supports give independent rows. H is the twisted code with eta=1; its norm to F_3 is 1, different from (−1)^(7·3)=−1. This norm observation is consistent with the known construction but does not substitute for our exhaustive MRD check.

The attached C++17 program uses base-three coefficient encoding, polynomial convolution, and reduction by z^7=1+2z^2. It checks a*a^(2185)=1 for all 2,186 nonzero elements. Since this is the actual polynomial quotient ring, these checks certify that every nonzero residue is invertible, hence that the chosen quotient is a field. No irreducibility assumption from a library is needed.

For each code the program enumerates the normalized nonzero coefficient triples (1,a,b), (0,1,b), and (0,0,1). There are 2187^2+2187+1=4,785,157 of them. These are all projective codewords: multiplication by any nonzero element of F is an invertible F_3-linear output map, so preserves rank. It evaluates each map on the seven basis elements and performs exact F_3 Gaussian elimination. Each code has projective rank histogram

- ranks 0 through 4: zero;
- rank 5: 99,463;
- rank 6: 1,993,632;
- rank 7: 2,692,062.

The minimum nonzero rank is therefore exactly 5=n−k+1, proving both codes MRD for these parameters. Matching rank histograms alone would not prove equivalence.

## Profiles and the scope separation

The Python program uses modular Gaussian elimination on coefficient rows. All matrices have entries in F_3, so their ranks over F_3 equal their ranks after extension to F. Intersections are computed using the nondegenerate coefficient dot product and (intersection U_j)^perp=sum U_j^perp. A cyclic shift is an orthogonal permutation, so shifting a computed perpendicular basis is valid. Evaluation is an F-linear isomorphism from degree-less-than-7 linearized coefficient vectors to F^7, so dimensions computed this way equal vector-code dimensions; no claim that evaluation preserves the chosen dot product is needed.

For i=0,...,7:

- C, every generator theta^r, r=1,...,6: sums (3,5,6,7,7,7,7,7), intersections (3,1,0,0,0,0,0,0).
- H, r=1 or 6: exactly those same profiles.
- H, r=2,3,4,5: sums (3,6,7,7,7,7,7,7), intersections (3,0,0,0,0,0,0,0).

The first distinction at r=2 has a short algebraic check. C+theta^2(C) has monomial support {0,1,2,3,5} in exponent indices and dimension 5. H+theta^2(H) is spanned by e0+e3,e1,e2,e2+e5,e3,e4, six independent vectors. Thus its dimension is 6. This gives an immediate semilinear vector inequivalence certificate while preserving the published fixed-generator collision.

For completeness, their right idealizers also differ. If phi=sum a_j x^(3^j), then x∘phi, x^3∘phi, x^27∘phi all lie in C only if its support lies in {0,1,3} intersect ({0,1,3}−1) intersect ({0,1,3}−3)={0}. Conversely every ax belongs to the right idealizer of C, so its size is 3^7. For H, requiring x^3∘phi and x^9∘phi in H first limits support to {6,0,1}; the equality of coefficients at indices 0 and 3 then forces a6=a1=0. Requiring (x+x^27)∘(a0 x) in H forces a0^27=a0. In F_(3^7), the roots of this condition form F_3, so the right idealizer has size 3. Under two-sided polynomial equivalence the right idealizers are conjugate, with field automorphisms preserving size, giving the separate broader inequivalence certificate. This recovers the mechanism credited in Remark 6.8, not a new classification.

## What remains unspecified

To turn the original research direction into a further theorem task, one must choose the target family and parameter range (q,m,n,k, twists and admissibility), the invariant package (one specified generator, every generator with labels, all automorphisms including nongenerators, or explicitly augmented element/idealizer data), the equivalence group, and the desired output (membership characterization, inequivalence criterion, or construction with independent MRD proof). Without those choices there is no single remaining proposition to prove or disprove. No present-day universal openness certificate is asserted.

## Reproduction

Compile finite_test.cpp with a standard C++17 compiler and run it; run profile_test.py with Python 3.8 or newer. FINITE_TEST.json and PROFILES.json record the results. Sources are original audit/test code; no third-party paper text is included in these deliverables. The finite enumeration and profile calculation are components of this single audit, not five independent research attempts.
