# Source-normalization and reproducibility cautions

These issues are stated narrowly for the inspected public source versions; they do not alter the target conjecture.

## Oberwolfach report, printed pp. 2187-2188

- The conjecture itself uses the correct top degree n + (g(g+1)/2-n).
- The genus-three table uses stack values, whereas the genus-four table reproduces coarse-space values. EGH explicitly explains the factor of two in the later paper.
- The report's formula -2Theta+L uses the unnormalized theta divisor. With zero-section-rigidified theta it becomes -2theta. Treating both theta symbols as the same class spoils the pushforward cancellation.
- The last displayed description of the nontrivial intersection on p. 2188 prints the Hodge exponent (g-2)(g-3)/2 beside D^(2g-1). This is not a top-dimensional monomial in general. The primary paper gives the required exponent (g-2)(g-1)/2.
- An earlier self-intersection display on p. 2187 retains exponent m on D restricted to D; the subsequent calculation correctly uses m-1. We use the dimensionally correct standard self-intersection formula.

## EGH arXiv:0707.1274v1

The source banner and abstract page identify v1, submitted 9 July 2007. The PDF body has a 2021 typesetting date, which is not a verified new submission.

1. Proposition 9.4's printed simplified correction term is inconsistent with the finite double sum in its proof on p. 33. With standard Bernoulli numbers, multiplication of that correction term by 2^(2g-4)(2g-2)! restores agreement with the preceding finite sum. At g=3 the discrepancy is -119/1920 versus -1/80.
2. In Table (30), g=6, terms II and III are twice the values from its own finite formulas with stack H_4. The source formula yields -23837/630 and 1639/630, while the table gives denominators 315. Its term I does agree with the finite calculation.
3. In Table (30), g=7, the finite term III is 203645/189, whereas the displayed value is 17594928013/16329600. The first two terms agree.
4. The theorem statement for term III on p. 27 appears without the H_(g-2) factor that its proof explicitly supplies. We implement the finite sum in the proof, including H_(g-2).

5. The intermediate theta-pushforward equality at the top of p. 33 displays sign (-1)^(-k-1). Direct expansion using its Theorem 7.1 gives (-1)^k; at g=2,k=2,n=1 the left side is 1 while the displayed right side is -1. The subsequent finite double sum uses the sign consistent with direct expansion. The checker tests 252 instances of the corrected expansion and separately verifies the Todd coefficient convolution.

The exact arithmetic and raw finite-sum route are retained in verify.py. This is not a claim that these issues persist in the 2010 journal article. That PDF was not obtained. An independently retrieved published version is the preferred next source check during audit.
