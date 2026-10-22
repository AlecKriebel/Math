# Independent adversarial audit: 30002136

Date: 2026-10-03. Review of the original frozen partial-result packet.

## Verdict

**PASS for the stated proper-subfamily theorem, with one minor terminology erratum. NOT a solution of the original problem.** No invalid universal-identity inference, counterexample to the submitted theorem, missing arbitrary-companion reduction, or substantive mathematical gap was found. The arbitrary-integer conclusions are supported by the proofs, rather than extrapolated from bounded exponent samples.

The strongest supported conclusion is exactly:

> Let u be an element of the rank-two free group. If, in some free basis, a cyclically reduced representative contains either at most three total occurrences of one generator and its inverse, with arbitrary signs, or at most five occurrences of that generator all of one sign, then every v in the whole free group satisfying tr rho(u) = tr rho(v) for every rho into SL3(C) is conjugate to u.

The other generator's exponents are unrestricted. This includes the identity, pure powers, zero same-sign gaps, negative gaps, repeated gaps, and proper powers. No restriction on the companion is assumed before proving its signed counts equal those of u.

The original problem remains **unsolved**; the partial theorem passed scoped review, without novelty certification.

## Provenance

This is a public projection of the independent audit of original commit b198d54f9810153872d92f736c24036b44721797. Operational details were removed; mathematical review conclusions are retained. The original audit SHA256 is ae58929beb831d44cfd894be5d3dfa73f1cd78432f98aaf8341d0f542d9328f9. Its required editorial correction has been applied to the included first proof; narrow confirmation of that repair subsequently passed; see NARROW_REVIEW.md. No original target solution or novelty certification is claimed.

## 1. Exact target and literature/credit

The original [Oberwolfach report, printed p.2195, Question 0.1](https://ems.press/content/serial-article-files/46404) asks about nonconjugate elements of F2 with equal standard traces under every SL3(C) representation. It separately mentions characteristic polynomials. The packet preserves the field, universal quantifier, fixed pair, and unrestricted conjugacy requirement; it adds no positivity or primitive-word hypothesis to the target.

The current [Lawton–Louder–McReynolds version, §§4.2–4.3](https://arxiv.org/pdf/1312.1261) supports the credit to Horowitz for letter-count restrictions, the Borel-dependent inverse obstruction, the displayed twelve-letter candidate, the reported length-20 search, and the warning that the positive-pair reduction remains conjectural. Its subsequent discussion also prevents treating the reversal lemma as a theorem excluding each individual nonconjugate reversal pair. The packet's treatment is appropriately cautious. The Horowitz original was not separately retrieved; the self-contained count proof was audited directly.

[Aougab–Lahn–Loving–Miller, §1.2, published 24 February 2025](https://link.springer.com/article/10.1007/s00208-025-03103-y) explicitly treats the higher-dimensional universal-trace-pair question as open. The cited [MEGL report](https://megl.science.gmu.edu/wp-content/uploads/2021/03/MEGL_Summer_2016_Final.pdf) supplies additional project credit, not a needed proof premise. A bounded current-source search located no later primary resolution. This is evidence from checked sources, not a guarantee of global literature completeness or a novelty judgment.

## 2. Universal trace, inverse traces, and characteristic polynomials

The contragredient argument is correct: (MN)^(-T) = M^(-T)N^(-T), so rho*(g) = rho(g)^(-T) is a representation. Applying the assumed equality to rho* equates inverse traces at the original representation. This is different from the generally false matrix identity w(A^-1,B^-1) = w(A,B)^-1.

For determinant-one 3-by-3 matrices, the coefficients are 1, -tr(M), tr(M^-1), -1. Thus equality of universal standard trace is equivalent to equality of characteristic polynomials at every representation. Cayley–Hamilton yields equality of all integer power traces. Neither result implies equality of matrix-valued word maps.

The distinction from a one-representation trace coincidence matters. An independent exact negative control uses X = [[0,0,1],[1,0,-2],[0,1,3]] and Y = I. Both have determinant one and trace three, but their inverse traces are two and three. Their characteristic polynomials differ. This confirms that the universal quantifier is essential.

The nontrivial word-versus-inverse exclusion in Turn 1 is a separately credited Borel word-map application. It does not follow from the characteristic-polynomial reduction alone. The packet explicitly acknowledges that dependency and does not need it for its partial theorem.

## 3. Signed and unsigned cyclic counts; arbitrary companions

Signed exponent sums are recovered with independent Laurent coordinates: p determines the multiset (p,0), (0,p), (-p,-p), including p=0. The alternative one-variable specialization 2t^p+t^(-2p) also distinguishes positive and negative p. Abelianization alone would be inadequate, as commutators illustrate.

For unsigned b count, first cyclically reduce. A word involving both generators has a cyclic alternating maximal-block form with every p_i and q_i nonzero. With C = [[2,1],[1,1]] and D(t) = diag(t,t^-1), the trace expansion assigns one two-state index to each q_i. The largest exponent is sum |q_i|. Each nonzero q_i independently forces the unique maximizing state. All matrix entries of C^p are nonzero for nonzero integer p: positive powers are strictly positive, while negative powers have positive nonzero diagonal entries and negative nonzero off-diagonal entries. Therefore the unique maximal term has a nonzero coefficient, even with arbitrary mixed signs. No cancellation among maximizers is possible.

Embedding in SL3 adds a constant one, which cannot affect the positive maximum for words involving b. Pure a powers have constant positive trace plus one and degree zero; pure b powers have top degree |q|; the identity has trace three. Exchanging the generators recovers both unsigned cyclic counts. Combining each unsigned count n with its signed exponent sum e gives (n+e)/2 and (n-e)/2, so all four signed letter counts are forced.

This is the essential arbitrary-companion step. It applies after cyclic reduction to every v in F2, without assuming v belongs to a special family. It also prevents spurious zero-gap cancellation from creating an omitted companion.

## 4. GL3 extension and exact generic-cell contract

Equal exponent sums justify scalar normalization: for A = alpha A0 and B = beta B0, every signed word acquires the scalar alpha^(e_a) beta^(e_b). Choosing cube roots of the nonzero determinants over C gives A0,B0 in SL3. The same scalar occurs for both words. Hence universal SL3 equality extends to all GL3 pairs, including signed words. The particular choice of cube roots is irrelevant to this equality.

For positive words, the entries and trace are polynomial on all matrices, so equality on the dense invertible locus extends to singular matrices. No such literal evaluation is used for signed words. After clearing determinant denominators, polynomial coefficient comparison on the invertible locus is valid.

The LDU cell is an open dense cell of irreducible SL3, and the two independent cells supply 16 parameters: four nonzero diagonal parameters and twelve ordinary triangular entries. Inverses introduce only Laurent powers of the four diagonal parameters. Word trace differences are regular on SL3×SL3 and become Laurent polynomials on this dense product cell. Exact coefficient vanishing after a monomial denominator is cleared is therefore a necessary and sufficient fixed-pair identity certificate. It is neither a sampled-matrix test nor a finite global search bound.

The independent controls also reconstructed a generic determinant-one matrix from its entries using the first two leading principal minors, verifying the converse LDU parameterization algebraically.

**Required textual correction before any revised/public-facing presentation:** Turn 1 says the pivots are s and st. Those are the first two leading principal minors. The three diagonal pivots are s, t, (st)^(-1). The open-cell condition and every calculation use the correct minors, so the slip does not affect the argument. The included first proof applies that one-line correction; the original reviewed revision remains separately identifiable by its immutable commit. This correction is required for precise wording but is not a blocker to the scoped mathematical verdict.

## 5. Same-sign counts zero through four

After simultaneous inversion of b if needed, the signed counts put both words into a^p1 b ... a^pk b with integer gaps. Gaps zero are legitimate between like-signed b letters. Cyclic rotation of a gap tuple gives a conjugate word even with zero or negative gaps.

For k=0, signed exponent sums determine the pure a power, including the identity. For k=1, they determine a^S b. At k=2 the determinant-corrected transposition gives the stated symmetric pair of Laurent monomials plus the common last term. Removing the latter recovers the unordered gaps; exchanging them is a cyclic rotation. Repeated, zero, and opposite gaps cause no exception.

For k=3, the three-cycle gives the cyclic orbit under (p,q,r) -> (p-r,q-r). Its kernel is exactly the integer common-shift line. Equal Laurent orbit sums identify one rotated image with the first tuple's image. Equal total exponent sum removes the common shift. Constant triples are correctly handled. A control verifies that (1,2,3) and (8,9,10) really have identical three-cycle trace signatures, emphasizing why the separately proved exponent-sum invariant cannot be omitted.

At k=4, the monomial b11 b12 b23 b31 has exactly four index-path rotations. With total S fixed, the map from adjacent ordered pair (u,v) to (S-u-v,u,v) is injective in all integers. The coefficient therefore recovers a directed pair deck, without additive-aliasing assumptions. The multiplicity partitions of four exhaust the stated proof, and all four-label assignments reproduce its unique cyclic reconstruction.

## 6. Mixed-sign count two

Cyclic reduction forces both separating a gaps nonzero in a^p b a^q b^-1. Multiplication by det(B), followed by the cofactor expansion, gives one distinct generic-B monomial per determinant permutation, with coefficient sign(sigma) sum_i xi^p x_sigma(i)^q. A fresh explicit 2-by-2-minor expansion confirms all 18 diagonal-factor terms, independently of the author's symbolic implementation.

The transposition coefficient and total p+q determine the unordered pair. The 3-cycle coefficient compares the cyclic orbits of (p,q,0) and (q,p,0). As p,q are nonzero, the only zero coordinate fixes the rotation. A swap can survive only when p=q. Negative exponents and p+q=0 preserve Laurent independence because all three GL3 diagonal variables are independent. Thus the ordered gaps, and hence the cyclic word, are fixed.

## 7. Same-sign count five and the finite-pattern issue

The requested generic-B monomial b11^2 b12 b23 b31 has precisely five closed index paths, the rotations of (1,1,1,2,3). Equal total S again makes the coefficient an injective encoding of adjacent pairs. In particular, coincidences such as p_i+p_j=p_k do not merge distinct deck entries: the other two coordinates individually record the pair.

The deck determines each label's multiplicity by its outgoing degree. Equal decks consequently have the same alphabet, containing at most five labels. One simultaneous injective relabeling maps that alphabet into {0,1,2,3,4} while preserving decks and rotations. This is the rigorous bridge from a finite equality-pattern classification to **arbitrary integer labels**. A finite box of numerical exponents, without this bridge, would not suffice. Here the written partition proof and the injective encoding do supply it. No additional unproved all-integer assumption is needed.

The seven multiplicity partitions of five produce exactly one collision type: (r,r,s,r,t) versus (r,r,t,r,s), with r,s,t pairwise distinct. The independent checker uses all 52 restricted-growth equality patterns and all orders within each multiset rather than the author's 5^5 implementation. Both classifications agree.

For that exception, set p=s-r, q=t-r and C=A^r B. The first word becomes C C A^p C C A^q C, whose trace rotates to tr(A^p C^2 A^q C^3). The other has p and q interchanged. Cayley–Hamilton yields Delta = -e2(C) D3. The cubic difference is D3 = -cycle(C) det[(xi^p,xi^q,1)], so the final sign is positive:

Delta = e2(C) (c12 c23 c31 - c13 c32 c21) det[(xi^p,xi^q,1)].

Since p,q,0 are distinct, the six Laurent alternant monomials are distinct, including opposite-sign cases. The factors are all nonzero in an integral domain. Their product cannot vanish identically on the dense open invertible locus. Since B=A^-r C remains arbitrary invertible, this is a legitimate GL3 separation and hence rules out universal SL3 equality. A deck collision has not been mistaken for trace equivalence.

## 8. Mixed-sign count three

After simultaneous generator inversion, there is exactly one negative b. Cutting immediately after it yields a^p b a^q b a^r b^-1 with p,r nonzero and q arbitrary, including zero. The other two sign arrangements reduce to this same case. The count invariant gives the companion the identical sign pattern.

Multiplying the trace by det(B) permits generic adjugate expansion. Independently expanding the relevant minors gives:

- [b12 b13 b21 b31] = -x1^q (x2^p-x3^p)(x2^r-x3^r);
- [b11 b12 b23 b31] = x1^q (x1^p x2^r + x3^p x1^r - x3^p x2^r).

The first coefficient is nonzero because p,r are nonzero. Its x1 exponent identifies q without any bound on p or r. The known sum then identifies p+r. Removing the common pure powers recovers the unordered pair {p,r}, with multiplicities. When p+r=0 the common pure term is simply two; when p=r the mixed term has multiplicity two. Neither requires division or introduces an exception.

The second coefficient's swapped difference is x1^q det[(xi^p,xi^r,1)]. If p and r differ, its six monomials are distinct; if they agree, there is no swap ambiguity. This fixes all three ordered gaps. The zero outer gaps excluded by the proof are exactly the cyclic-cancellation cases, while the allowed q=0 case is covered explicitly.

## 9. Automorphisms and the remaining target

A free-group automorphism phi preserves universal trace equivalence by precomposition of representations: rho(phi(u)) = (rho composed with phi)(u). Its inverse supplies the reverse implication and also shows that phi preserves and reflects conjugacy. Thus an exclusion proved in one free basis applies whenever some basis meets its hypotheses.

The packet does not show that every conjugacy class has such a basis. A precise description of the unexcluded complement is: in every free basis, **each generator individually** has at least four occurrences when it occurs with both signs, and at least six when it occurs with only one sign. This is the logical complement of the sufficient exclusions, not a classification or an assertion that the complement is empty.

No fixed nonconjugate universally equal-trace pair, no global separation theorem, no length bound reducing the full search to a finite computation, and no proved general positive-word reduction has been produced. These are the exact missing ingredients for resolving the original problem. 

## 10. Reproducible evidence and limits

All checks pass. Evidence includes:

- The five author outputs reproduced byte-for-byte, and 27/27 final manifest entries verified.
- A new integer Laurent implementation checking both counts on 39,365 freely reduced words of lengths zero through nine: 78,730 degree checks, including 9,824 inputs requiring cyclic reduction. Additional deliberate ordinary cancellations, pure powers, and long signed blocks pass.
- Fresh generic LDU inverse-coordinate algebra, contragredient identities, signed GL3 scalar factors, and negative controls for one-trace/characteristic-polynomial confusion and commuting-matrix blindness.
- An independent exact refutation of the same cited twelve-letter candidate using a different integer SL3 pair: traces 14957 and 14917, difference 40.
- Fresh formal mixed-two cofactor expansion, four-gap paths, large-magnitude signed gap controls, and the common-shift negative control.
- Independent standard-library formal cofactor and sparse-polynomial expansions for Turns 4–5, including exact cubic and quintic identities, plus exhaustive equality-pattern classification.
- Immutable-commit readback and SHA checks for all 28 public files.

None of the finite matrix or exponent checks is promoted to a proof of universal equality. The exact symbolic coefficient identities establish algebraic formulas; the all-integer reconstruction and density arguments establish their claimed mathematical consequences. This remains a scoped audit of a partial result.
