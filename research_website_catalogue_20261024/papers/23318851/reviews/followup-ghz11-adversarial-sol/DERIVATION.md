# Bounded GHZ11 falsification certificate

The answer to Ferudun's Problem 3.8, with the definitions in the checked edition, is **no**. A real unit tensor with eleven binary factors realizes a determinant tuple for which Q1 < Q2. This is a bounded mathematical screen; no novelty, priority or publication claim is made.

## Exact claim and source conventions

Let B be the closed Frobenius unit ball in (R^2)^{tensor n}. For each principal 2-by-2^(n-1) flattening M_i, put d_i = det(M_i M_i^T). The checked primary sources define

    Q1(d) = product_(i=1)^n (sum_(j != i) d_j - d_i),
    Q2(d) = (1/2) product_(epsilon in {-1,+1}^n)
                         (sum_(i=1)^n epsilon_i sqrt(d_i)).

The square roots are the nonnegative ones. The Q2 product contains all 2^n sign vectors, not one vector per global-sign pair. Its prefactor is exactly 1/2. Q1 has degree n in d; Q2 has degree 2^(n-1) in d. There is no additional homogenizing factor or restriction to the strict interior in the printed definitions.

Source checks were made against the actual PDFs and rendered complete pages: [Seigal, published author PDF](https://seigal.github.io/seigal2018gram.pdf), Definition 1.2 on printed p.352, definitions and Conjecture 1.5 on p.354, and the diagonal calculation in Section 3 on p.366; [Ferudun, source PDF](https://zenodo.org/api/records/23111048/files/OWR-15428-003-paper.pdf/content), definitions on p.1 and Problem 3.8 on p.6. The latter asks whether the Gram locus is contained in {Q1 >= Q2} for every n >= 4. Seigal's p.366 assertion about positivity at the diagonal for all odd n >= 5 is also tested by this calculation.

## Realization in the closed unit ball

Set

    A = (e_0^{tensor 11} + e_1^{tensor 11}) / sqrt(2).

The two basis tensors are orthogonal, so ||A||_F^2 = 1/2 + 1/2 = 1. In every flattening, the row indexed by 0 has the single coefficient 1/sqrt(2) in column 0^10, and the row indexed by 1 has that coefficient in the different column 1^10. Thus the two rows are orthogonal and each has squared norm 1/2. Consequently

    M_i M_i^T = (1/2) I_2,    d_i = 1/4,    i=1,...,11.

This is an explicit real realization. It needs no marginal-feasibility theorem. Its unit norm is allowed because the ball is closed; equality of the two singular values is allowed as well.

## Independent product evaluation

For this tuple, every Q1 factor equals 10/4 - 1/4 = 9/4. Therefore

    Q1 = (9/4)^11 = 3^22 / 2^22.

A sign vector with k minus signs contributes (11-2k)/2 to Q2, and there are binomial(11,k) such vectors. The absolute integer factors have the following multiplicities over the full sign set:

| Absolute integer factor | Total multiplicity |
| --- | ---: |
| 11 | 2 |
| 9 | 22 |
| 7 | 110 |
| 5 | 330 |
| 3 | 660 |
| 1 | 924 |

These multiplicities total 2048. Exactly 1024 factors are negative and none is zero, so the product is positive. Each of the 2048 factors has denominator 2, and the external prefactor supplies one further 2. Hence

    Q2 = 11^2 * 9^22 * 7^110 * 5^330 * 3^660 / 2^2049
       = 3^704 * 5^330 * 7^110 * 11^2 / 2^2049,

    Q2/Q1 = 3^682 * 5^330 * 7^110 * 11^2 / 2^2027.

The independently written exact control first obtains all eleven flattening Gram matrices from the two sparse tensor coefficients, then literally enumerates and multiplies all 2048 rational sign factors. A separate binomial-product loop does not use the enumeration histogram. Both agree exactly before the supplied target prime exponents are compared. The complete literal factor table is RAW_SIGN_FACTORS.tsv; EXACT_CERTIFICATE.json retains the matrix entries, grouped factors, exact rational values, exponents, signs and bounds. No floating-point arithmetic or research/support code is used.

## Short strict inequality proof

Write the ratio numerator as

    9^341 * 625^82 * 25 * 16807^22 * 121.

The elementary inequalities 9 > 8 = 2^3, 625 > 512 = 2^9,
25 > 16 = 2^4, 16807 > 16384 = 2^14, and 121 > 64 = 2^6 give

    Q2/Q1 > 2^(3*341 + 9*82 + 4 + 14*22 + 6 - 2027)
          = 2^52 > 1.

Thus A belongs to B and G(A) belongs to G(B), but Q1(G(A)) < Q2(G(A)). This single n=11 counterexample falsifies the universal inclusion asked in Problem 3.8. It also falsifies the printed all-odd-n>=5 positivity assertion at the all-1/4 diagonal. Exact integer comparison additionally places the ratio strictly between 2^135 and 2^136; the short proof above is already sufficient.

## Falsification checks and limits

The n=3 control yields Q1=1/64 and Q2=9/512, including the external 1/2 factor. The n=4 GHZ control yields Q2=0, detecting even-parity zero factors. The diagonal controls for n=5,7,9 have Q1>Q2. These checks do not establish the necessary inclusion in those dimensions and do not claim that n=11 is the least possible counterexample dimension.

The result is confined to the checked source editions and definitions. This screen does not characterize the Gram locus, settle other parameter ranges, audit or revise Alec's Gram194 paper, or assert any defect in that paper. No priority search was performed, and an immediate consequence of printed definitions may already be known. No author was contacted, no outreach prepared, no original scientific report changed, and no finding was published or promoted.
