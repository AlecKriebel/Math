# Independent adversarial audit: AIM-PROBABILITY-0162 / 20002720

## Verdict

**PASS for `already_solved` in the frozen packet's explicitly stated formal algebraic scope.** No blocking mathematical defect was found in its arguments. This is an independent AI-assisted audit, not peer review or a certificate of historical priority.

The input is exactly the author packet bound by SHA256SUMS.json with SHA-256 `d12fd724d5a5b5f27024b14eea46ff9402139a793fe2636c7f0985a5fc4e8403`, containing 11 manifested files. The complete input manifest and its own hash are bound in INPUT_BINDING.json. No original was edited. No repository write or remote publication was performed.

The 1,980 author assertions reproduce exactly. A separately written implementation, importing no author code, passes 1,067 further exact assertions. Neither finite test count substitutes for the general arguments below.

## Exact question and answer threshold

The official AIM Problem 5.2 asks for the structure of the scalar boxed-convolution unit group on formal complex series in finitely many noncommuting variables. Its adjacent remark asks for a multivariable S-transform and suggests an analogue of the one-variable free Fourier map. The page imposes no smallest-representation criterion, unique preferred coordinates, full-center classification, or analytic/convergence axioms. Printed page 11 was freshly rendered and visually checked. The ordinary-multiplication target in the one-variable remark has the zero-constant-space typo identified by the packet; Nica's Section 14 gives the correct nonzero-constant target. [AIM source](https://aimath.org/WWN/braidgroups/braidgroups.pdf), [Nica notes](https://www.math.uwaterloo.ca/~anica/NOTES/section14.pdf).

The substantive structure is a central torus times an explicitly presented pro-unipotent character group, with finite nilpotent quotients and computable compatible faithful matrix representations. This is substantially more than the abstract fact that every group has a faithful permutation representation. It supplies an admissible formal multiplicative S-type encoding of all distributions with nonzero means. Therefore the printed algebraic problem has an existing structural answer under the announced interpretation.

The wording must retain that interpretation. The regular representation does not literally return the classical scalar S-series at s=1; it recovers the distribution, from which that scalar series is recovered. It does not prove the stronger minimality requirement inserted in Friedrich--McKay's own definition. Nor does it certify a community consensus that every possible intended meaning of a higher S-transform is settled. None of these stronger claims is needed for the stated classification.

## Source checks and attribution

Mastnak--Nica, arXiv:0807.4169v2, Theorem 1.2 and Proposition 3.7 identify normalized distributions with characters. Definition 3.2, Lemmas 3.3--3.4, and Proposition 3.6 provide the actual coproduct and Hopf proof. Those arguments were read; the theorem page was freshly rendered and checked. Their LS-transform is additive for commuting products. It is not a map making arbitrary noncommuting products additive. The arXiv version page and the author's talk support the packet's bibliographic attribution. [Paper](https://arxiv.org/abs/0807.4169v2), [author talk](https://www.math.uwaterloo.ca/~anica/Boxtimes2013.pdf).

Friedrich--McKay's longer preprint, Sections 6.1--6.4, supplies the full-group/faithful-representation interpretation; the short announcement gives the same proposed direction. Relevant proofs and definitions were read, including the errors discussed below. Pages 42--43 of the longer paper were freshly rendered and checked. Both inspected arXiv records have v1 only and present these works as preprints/announcement. No journal-publication claim about either is made. [Long paper](https://arxiv.org/abs/1309.6194v1), [announcement](https://arxiv.org/abs/1308.0733v1).

All five locally available source PDFs match the exact hashes and byte counts recorded by the author. SOURCE_AUDIT.json records independent inspection and retrieval scope. Sources themselves, extracted text, and screenshots are excluded from this audit bundle. No attempt was made to certify exhaustive literature priority, re-download the complete public corpora, or re-run live repository queue/duplicate checks.

## Mathematical audit

### 1. Domain, all units, and the inverse recursion

For a one-letter word i, the product coefficient is f[i]g[i]. Thus every linear coefficient must be invertible. Over C this is precisely the nonzero-mean condition. Over a general commutative unital ring, merely being nonzero is insufficient.

For a word w of length n, the discrete partition is the unique right-inverse term containing the unknown r[w], with coefficient A_w equal to the product of the linear coefficients of f along w. Every other r-coefficient is shorter. Since A_w is a unit, recursive solution gives a right inverse. Separately isolating the one-block partition gives a left inverse. Associativity identifies the two. No cancellation of nonunits, integral-domain hypothesis, or characteristic-zero assumption is hidden here.

The script computes left and right inverses independently over Q and Z/mZ for m=2,3,4,6,8,9,12, using all available linear units as the sampling pool. It also explicitly tests the nonunit obstruction 2 in Z/4Z.

### 2. Central normalization is a direct product

For D_lambda linear, the only surviving partition on one side is discrete and on the other is one-block. Both products scale f[w] by the product of lambda entries along w. Hence the linear factor is central.

Dividing each f[w] by the product of its linear coefficients gives a normalized series u. This division is allowed over the stated ring domain. The map f to (lambda,u) is bijective and respects multiplication. Thus the semidirect wording can safely be sharpened to a direct product. It does not imply that the torus is the entire center.

Tests use nonuniform linear coefficients, check normalization as a homomorphism, and check full-group block matrices, so they do not accidentally verify only the normalized subgroup.

### 3. Integral Hopf structure and formal versus analytic claims

The polynomial coordinate algebra has generators Y_w of weight |w|-1 for |w|>=2, with one-letter symbols interpreted as 1. Its coproduct has integer coefficients. The known complex coassociativity identities are polynomial identities in algebraically independent variables, hence hold integrally; the grading identity follows from the Kreweras block-count relation. The connected graded antipode recursion uses subtraction and multiplication only.

Consequently the character construction works over every commutative unital coefficient ring after base change. To spell out a harmless implicit notation in the packet, V_d is the bounded-weight part of R tensor_Z H_s. Character logarithms and the BCH interpretation require the displayed characteristic-zero setting; they are not asserted over arbitrary R.

The independent program compares both sides of coproduct coassociativity as exact integer polynomials, for distinct-letter words through length 6, both before and after normalization. This catches errors that testing only repeated letters or floating-point evaluations could conceal.

### 4. Representation order, compatibility, and faithfulness

With column vectors, T_u=(id tensor chi_u)Delta is the pullback of right translation. Coassociativity yields

    T_u T_v(h) = sum h_(1) chi_u(h_(2)) chi_v(h_(3))
               = T_(u box v)(h).

Thus the stated multiplication order is correct. It is not an anti-representation. The action preserves each bounded-weight module because coproduct weights are nonnegative. The leading term is h itself, and every other first tensor factor has lower weight. Increasing-weight order therefore gives upper unitriangular matrices.

Applying the counit to T_u(Y_w) recovers u[w]. This proves faithfulness for each degree quotient and, by compatible restrictions, for the entire family. Every matrix entry is a polynomial in finitely many coefficients. Adding the diagonal torus block gives full-group faithfulness. Its entries multiply independently because the splitting is central.

The independent order-sensitive test uses f=e+z_1^2 and g=e+z_1 z_2. The counit row at Y_121 in T_f T_g is 1, while in T_g T_f it is 0. This detects a reversal rather than merely checking a commuting example. Separate tests recover a single arbitrary top-degree coefficient and show it is invisible to the immediately smaller quotient.

### 5. Filtration, nilpotence, and noncommutativity

For f in F^p and g in F^q, a mixed term needs a nonzero f-block of size at least p and a nonzero g-block of size at least q. The corresponding weights sum to n-1. Hence no mixed term can occur below length p+q-1. The two products agree modulo F^(p+q-1), giving the claimed commutator inclusion.

The quotient F^m/F^(m+1) adds length-m coordinates, has dimension s^m over a field, and degree-N quotients have class at most N-1. Full formal groups are inverse limits of these quotients, not unions of embedded finite polynomials. The degree-three noncommutativity witness remains nonzero in every nonzero coefficient ring, including characteristic 2.

### 6. Radial centrality and coefficient restrictions

For radial h, its partition coefficient depends only on block sizes. Changing variables by Kreweras complement compares K^(-1)(rho) and K(rho), which differ by cyclic rotation and therefore have the same block sizes. Commutativity of scalar coefficients makes the two sums identical. This proves the radial assertion and shows why the nonlinear zeta series prevents a torus-only center claim. The proof even gives centrality in the whole scalar semigroup, without requiring h to be a unit; the additional tests cover that case.

Ordinary noncommuting matrix coefficients invalidate the scalar formula: the explicit 2-by-2 witness produces ABAB on one side and A^2 B^2 on the other. Operator-valued free probability has a different structure and is not being solved here. Likewise, faithfulness is on formal distributions, not raw tuples with potentially identical distributions. Group-valued transforms require each mean to be a unit; restricting all means collectively or only one of them would be insufficient.

## Source corrections and their effect

The packet correctly rejects the long preprint's full derived-subgroup equality and its finite-polynomial subgroup claim. It also correctly excludes the minimality and unrestricted tuple-domain statements from its proof.

This audit found one additional false equality in the same source: Example 6.1 identifies the derived subgroup of U_2 with F^3. Projection onto the coefficients of words using only one fixed letter is a group homomorphism to the abelian one-variable boxed group. Every commutator, and every product of commutators, therefore has identity projection. But e+z_1^3 belongs to F^3 and has nonidentity projection. Thus that equality is false over every nonzero commutative ring. The packet never invokes it. This is an extra bibliographic caution, not a blocking defect. CORRECTIONS.md gives a concise reusable replacement.

No change to the frozen proof or classification is required. Any future expanded discussion of the preprint's derived-subgroup claims should include this additional correction. Continue to label the accepted transform as formal, faithful, matrix-valued, and defined on invertible-mean distributions; retain the existing exclusions on center, minimality, analytic domains, and novelty.

## Reproduction and stopping condition

From this directory, run `python3 independent_checks.py`. The JSON must match INDEPENDENT_RESULTS.json. Run `python3 verify_audit.py --submission ../submission` to verify both audit hashes and the exact bound author packet, then reproduce the author and independent runs. No third-party packages, credentials, network access, PDFs, corpora, or private materials are needed.

The audit is complete when the exact input binding, two saved replay comparisons, and all checks pass. This report concerns that frozen input only; any revised packet requires a new binding and review of the changed material.
