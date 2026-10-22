# A type-D4 counterexample to the exponent-bound converse in canonical potential coordinates

This AI-assisted manuscript is unrefereed. Acceptance records an independent internal AI audit, not external human peer review, journal acceptance, or formal proof-assistant certification.

The complete analytical proof and its explicit numerical proof tables are retained. The two documents use separately stated row orders and sign conventions for their separating vectors. The displayed formulas, exponent rows, and integer vectors make every certificate directly checkable. This is not a computational reproduction package: executable code, raw exploratory datasets, copied sources and images, and private coordination records are omitted. Historical program checks are supporting verification history and are not claimed to have been rerun for this edition.

The later pullback-varsigma converse and coefficient conjecture remain unresolved by this work. The published sufficient theorem is not refuted; no general replacement proof is supplied for its affected proof step. No novelty, priority, exhaustive literature-survey, or current-openness claim is made.

## Claim and precise scope

Let G = Spin_8(C), with Dynkin edges 1--2, 2--3, 2--4, and choose the reduced word

    i = (1,2,3,2,4,2,1,2,3,2,4,2).

Use the reduced-word cluster seed, the canonical GHKK potential W on its dual cluster torus, and the X-coordinate convention of Koshevoy--Schumann, equation (3) and Definition 7. After combining like monomials, W has 22 distinct monomials, all with coefficient 1. Every one of their tropical inequalities is essential. Nevertheless two monomials have exponent -2 on X_6.

Thus the necessary direction of the exponent-bound equivalence formulated in the 2021 Oberwolfach report, in the canonical W coordinates specified there, is false.

This is a counterexample to that W-coordinate statement. It is not a counterexample to the string-coordinate version obtained by the chamber-ansatz pullback: for this example the pullback has every exponent in {-1,0,1}. Nor does it contradict the separate coefficient-based redundancy conjecture. No claim of novelty or of the current status of other formulations is made.

The accepted authored proof is preserved here with its complete exact separating-certificate table; the independent internal audit appears in AUDIT.md.

## 1. The reduced word and seed

Write roots in the ordered simple-root basis (alpha_1,alpha_2,alpha_3,alpha_4). Successive root vectors beta_k = s_{i_1} ... s_{i_{k-1}} alpha_{i_k} are

    (1,0,0,0), (1,1,0,0), (1,1,1,0), (0,0,1,0),
    (1,1,1,1), (1,1,0,1), (1,2,1,1), (0,1,1,0),
    (0,1,1,1), (0,0,0,1), (0,1,0,1), (0,1,0,0).

These are the twelve distinct positive D4 roots. Moreover direct multiplication of the simple-reflection matrices gives -I_4. Hence the word is reduced and represents w_0. This check uses the Cartan matrix with diagonal 2 and off-diagonal -1 precisely on the three Dynkin edges.

For clarity, here is the complete seed, so no inferred diagram is required. Positions 7,9,11,12 are frozen. All arrows have multiplicity one, and the complete arrow list is

    1->7, 2->4, 3->2, 3->9, 4->6, 5->4, 5->11, 6->1,
    6->8, 7->6, 8->3, 8->10, 9->8, 10->5, 10->12, 11->10.

There are no other arrows. To recover this list from the reduced word, let k+ be the next occurrence of i_k, or 13. There is an arrow k->k+ when k+<=12, except between two frozen vertices. If k<l<k+<l+ and i_k,i_l are adjacent in the Dynkin diagram, there is an arrow l->k, again omitting frozen--frozen edges. This is the usual reduced-word quiver rule; the adjacency condition is explicit in Genz--Koshevoy--Schumann, Section 4.2.2. The later Koshevoy--Schumann displayed D4 quiver is consistent with that condition.

Set b_ab = #(a->b) - #(b->a), and set y_k = X_k^{-1}. Inverting all X variables changes the signs, not the absolute values, of exponents.

## 2. Canonical potential, derived from optimized seeds

If vertex k is mutable, the X-mutation formula of Koshevoy--Schumann becomes

    y'_k = y_k^{-1},
    y'_a = y_a (1+y_k)^{b_ak}                 if b_ak >= 0,
    y'_a = y_a y_k^{-b_ak}(1+y_k)^{b_ak}     if b_ak < 0.

The exchange matrix changes by

    b'_ab = -b_ab                              if a=k or b=k,
    b'_ab = b_ab + [b_ak]_+[b_kb]_+ - [-b_ak]_+[-b_kb]_+
                                                otherwise,

with frozen--frozen entries erased. These are exact rational identities, used with the exchange matrix before the mutation.

For the four frozen positions f, the following mutation sequences, read from left to right with the original fixed vertex labels, end at seeds optimized for f:

    f=7:  (2,6,1,3,4,8,5,10)
    f=9:  (4,8,5,10)
    f=11: (10)
    f=12: ()

All mutated vertices are mutable. Iteration of the displayed matrix rule verifies that the final row b_fa is nonpositive for every mutable a in each case. That is exactly the condition that every mutable arrow adjacent to f points into f. By the defining normalization of the canonical potential, the f-summand equals y_f in this final seed. Pulling it back through the displayed sequence therefore computes the canonical summand in the original seed. This argument does not substitute an arbitrary F-polynomial for W.

Put

    A = 1 + y_3 + y_2 y_3,
    B = y_2 y_3 y_4 y_5,
    F_7 = 1 + y_6 + y_6 y_8 A
          + y_6 y_8 y_10 ((1+y_5)A + B(1+y_6+y_1 y_6)),
    F_9 = 1 + y_8 + y_8 y_10 (1+y_5+y_4 y_5).

The resulting canonical potential is

    W = y_7 F_7 + y_9 F_9 + y_11(1+y_10) + y_12.          (1)

Here the frozen-position labels 7,9,11,12 correspond to simple-root summands 1,3,4,2 respectively.

For a transparent direct check of the longer calculation, start with y_7 and pull back in reverse order 10,5,8,4,3,1,6,2. After the first four steps its quotient by y_7 is respectively

    1+y_10,
    1+y_10+y_5 y_10,
    1+y_8+y_8 y_10+y_5 y_8 y_10,
    1+y_8+y_8 y_10+y_5 y_8 y_10+y_4 y_5 y_8 y_10.

The next step produces

    1 + y_8 + y_3 y_8
      + y_8 y_10 (1+y_5+y_3+y_3 y_5+y_3 y_4 y_5).

The step at 1 adds y_1 y_3 y_4 y_5 y_8 y_10. After the step at 6 it is

    1 + y_6 + y_6 y_8(1+y_3)
      + y_6 y_8 y_10(1+y_5+y_3+y_3 y_5+y_3 y_4 y_5)
      + (1+y_1)y_3 y_4 y_5 y_6^2 y_8 y_10.

The final step at 2 gives F_7 in (1). The F_9 calculation consists of the first four steps, with frozen factor y_9; F_11 and F_12 are immediate. The historical certificate data recorded complete exchange matrices and separately obtained mutation routes. The historical standard-library verifier recomputed these identities using integer polynomial multiplication and exact division. This edition retains the complete quiver, mutation rules, four fixed-label routes, and pullback derivation above; intermediate machine records and executable code are not distributed.

There are 14 monomials in y_7 F_7, 5 in y_9 F_9, 2 in y_11(1+y_10), and 1 in y_12. Distinct frozen markers preclude coincidences between summands; inspection of the expanded expressions precludes coincidences within summands. Thus (1) has exactly 22 combined monomials, each of coefficient 1.

In particular, the monomial

    y_2 y_3 y_4 y_5 y_6^2 y_7 y_8 y_10

occurs with coefficient 1. Its X_6 exponent is -2, so the required absolute-exponent bound fails.

## 3. Every canonical inequality is essential

For a term y^a = X^{-a}, its tropical inequality in the X-cocharacter variable x is -a.x >= 0. Equivalently, in z=-x it is a.z >= 0. We supply an integer z^(j) for each row a^(j), such that

    a^(j).z^(j) = -1,
    a^(r).z^(j) >= 0 for every r != j.                    (2)

Consequently z^(j) belongs to the cone with the j-th inequality omitted and not to the full cone. Every one of the 22 inequalities is therefore essential, without any numerical optimization assumption.

In the following table an exponent vector is encoded by twelve consecutive digits in positions 1 through 12. Each digit is 0,1, or 2; there is no multi-digit entry. The right column is the complete integer separating vector.

|j|a^(j)|z^(j)|
|---|---|---|
|1|000000000001|(0,0,0,0,0,0,0,0,0,0,0,-1)|
|2|000000000010|(0,0,0,0,-1,0,0,0,0,1,-1,0)|
|3|000000000110|(0,0,0,0,0,0,0,1,0,-1,0,0)|
|4|000000001000|(0,0,-1,0,0,0,0,1,-1,0,0,0)|
|5|000000011000|(-2,0,0,0,0,1,0,-1,0,1,0,0)|
|6|000000011100|(-2,0,0,0,1,1,0,0,0,-1,1,0)|
|7|000000100000|(-1,0,0,0,0,1,-1,0,0,0,0,0)|
|8|000001100000|(0,2,0,-1,0,-1,0,1,0,0,0,0)|
|9|000001110000|(0,0,1,-1,0,0,0,-1,1,1,0,0)|
|10|000001110100|(0,0,1,-1,1,0,0,0,1,-1,1,0)|
|11|000010011100|(-2,0,0,1,-1,1,0,0,0,0,0,0)|
|12|000011110100|(0,0,1,0,-1,0,0,0,1,0,0,0)|
|13|000110011100|(0,1,0,-1,0,0,0,0,0,0,0,0)|
|14|001001110000|(0,1,-1,-1,0,0,0,0,0,1,0,0)|
|15|001001110100|(-1,1,-1,-1,1,1,0,0,1,-1,1,0)|
|16|001011110100|(-1,1,-1,0,-1,1,0,0,1,0,0,0)|
|17|011001110000|(0,-1,0,0,0,0,0,0,0,1,0,0)|
|18|011001110100|(-1,-1,0,0,1,1,0,0,1,-1,1,0)|
|19|011011110100|(-1,-1,0,1,-1,1,0,0,1,0,0,0)|
|20|011111110100|(0,0,0,-1,-1,1,0,0,2,0,0,0)|
|21|011112110100|(1,0,0,0,0,-1,1,0,0,0,0,0)|
|22|111112110100|(-1,0,0,0,0,0,0,0,0,0,0,0)|

All 484 scalar products in (2) are integer calculations. The historical checker recomputed them; every diagonal product is -1 and all off-diagonal products are nonnegative. Each product can also be checked directly from the full table above. This finishes the counterexample proof.

## 4. Why the coordinate distinction matters

The chamber-ansatz monomial map has X_k = product_l x_l^{C_kl}, where C is upper triangular with diagonal -1. Thus y_k = product_l x_l^{K_kl}, K=-C has diagonal 1, and a monomial exponent row a becomes aK in string coordinates. The formula is

    K_kl = Cartan(i_k,i_l)       when k<l<k+,
    K_kk = K_k,k+ = 1           when the indicated position exists,
    K_kl = 0                    otherwise.

This is the monomial map in Koshevoy--Schumann Definition 9. Its determinant is 1. For all 22 rows above, every entry of aK lies in {-1,0,1}; the historical computation checked the complete matrix and all transformed rows exactly. The displayed formula and complete exponent table determine the matrix and every transformed row without the omitted machine records. In particular, the two rows with a_6=2 become

    row 21: (0,1,0,1,0,1,-1,0,0,0,0,0),
    row 22: (1,0,0,0,0,0,0,0,0,0,0,0).

A monomial torus isomorphism preserves nonredundancy, because it gives an invertible linear map of exponent vectors. It does not in general preserve a coordinatewise exponent bound. For this concrete canonical potential it does not preserve that bound. Therefore the example must not be reported as disproving the differently worded string-coordinate conjecture. The claimed equivalence of multiplicity-freeness under this map in the published proof of Theorem 2 does not follow merely from the monomial isomorphism, and the example above exhibits the distinction directly.

The separate conjecture that an inequality is redundant exactly when its combined coefficient is greater than 1 also remains unrefuted by this example: all 22 coefficients and all 22 facets are consistent with it.

## Sources and attribution

- Bea Schumann, joint work with Gleb Koshevoy, “Optimality of string cone inequalities and potential functions,” Oberwolfach Report 20/2021, printed pp.1123–1125, DOI 10.4171/owr/2021/20: https://ems.press/content/serial-article-files/46898 . The target W-coordinate converse is on printed p.1125.
- Gleb Koshevoy and Bea Schumann, “Redundancy in string cone inequalities and multiplicities in potential functions on cluster varieties,” Journal of Algebraic Combinatorics 56 (2022), 1031–1053, DOI 10.1007/s10801-022-01144-z: https://link.springer.com/article/10.1007/s10801-022-01144-z . Equation (3), Definitions 7–10, Lemmas 2–3, Proposition 5, and Section 7 supply the conventions and context. The theorem proving the sufficient direction and prior multiplicity-free cases belong to those authors.
- The earlier arXiv version is https://arxiv.org/abs/2109.14439 . Its Section 7 example word differs from the corrected published word (2,1,3,4)^3; the published correction was used only to validate the independent exploration. The proof above is derived directly from the candidate’s own seed and does not rely on the printed example polynomial.
- Volker Genz, Gleb Koshevoy and Bea Schumann, “Polyhedral parametrizations of canonical bases & cluster duality,” Advances in Mathematics 369 (2020), 107178, DOI 10.1016/j.aim.2020.107178; author preprint https://arxiv.org/abs/1711.07176 . Section 4.2.2 explicitly includes Dynkin adjacency in the inclined-arrow rule.

The proof, formulas, and explicit certificate tables in this edition are authored for this attempt. No source-author software was executed. Copied source PDFs and extracted source text are excluded; source identities and the historical inspection scope appear in SOURCES.json. Executable verification code and raw exploratory datasets are not distributed.
