# Explicit local-condition correction in Schmidt Theorem 4.1

Problem 30000779 / OWR-1586-003. Independent review, 8 October 2026.

This is an authored clarification of the correction already used in the proposed audit. It is not an author-issued or publisher-issued erratum. The mathematical conclusion of the proposed audit is unchanged.

## Precise replacement

Use the notation of Schmidt's Theorem 4.1. Let Sigma contain S, T and all primes above p, and put J = Sigma minus (S union T). At every finite v, define the integral Kummer subgroup

    C_v = O_v^* k_v^{*p}/k_v^{*p} inside H^1(k_v, mu_p).

In the first Kummer-coefficient sequence in its proof, use the local target

    product_(v in S) H^1(k_v, mu_p)
      times product_(v in J) H^1(k_v, mu_p)/C_v.

Its kernel on H^1(X minus Sigma, mu_p) is exactly V_S^T. This follows from valuations outside Sigma and from the imposed local conditions inside Sigma. At v outside S union T it imposes valuation divisible by p; at S it imposes the stronger local pth-power condition; at T there is no condition.

At primes dividing p, C_v is not to be replaced by ordinary Galois-unramified H^1(k_v, mu_p). The latter need not equal the unit image. Consequently, when the printed quotient H^1_/nr(k_v, mu_p) is given its usual Galois-unramified meaning, that displayed quotient also needs correction. The phrase “read using the integral Kummer condition” in the earlier ledger is valid only with this explicit replacement understood.

## Correct dual quotient and cokernel

All groups in the remainder have F_p coefficients. Local Tate duality and local reciprocity identify the annihilator of C_v with H^1_nr(k_v, F_p): a character is unramified precisely when its reciprocity character kills units. Therefore, for

    W = product_(v in Sigma) H^1(k_v, F_p),
    B = product_(v in S) H^1(k_v, F_p)
          times product_(v in J) H^1_nr(k_v, F_p),

the dual of the preceding local target is B, embedded with zero components at T. Thus

    Q = W/B
      = product_(v in T) H^1(k_v, F_p)
          times product_(v in J) H^1(k_v, F_p)/H^1_nr(k_v, F_p).

Choose Sigma so that the p-part of the Sigma-class group over k(mu_p) is zero. The extension k(mu_p)/k has degree prime to p. Class field theory and restriction then give the required vanishing of both degree-one localization kernels. Poitou-Tate gives the degree-two localization-kernel vanishing and identifies

    coker[H^1(X minus Sigma, F_p) -> Q] = (V_S^T)^dual.

Excision with the marked local calculations identifies the same cokernel with

    ker[H^2(X minus S, T, F_p) -> H^2(X minus Sigma, F_p)].

The latter is Sha^2(k,S,T), because H^2(X minus Sigma) localizes injectively and the local degree-two restrictions at points still on the marked curve are zero. This proves the claimed duality.

Accordingly the first product in sequences (I) and (II) must have index T, not S. The S-indexed full local factors in the initial Kummer sequence, the dual subgroup B, and the H^2 localization diagram remain S. No change of the theorem's hypotheses is needed.

## Verified locations and boundary

- English author translation, p.10: initial Kummer sequence and sequences (I), (II).
- German v2, p.10: initial Kummer sequence and (I); p.11: (II).
- Both versions' quotient diagrams already display the correct T-indexed quotient.

Sources: [Schmidt English manuscript](https://www.mathi.uni-heidelberg.de/~schmidt/papers/marked.pdf), [Schmidt German v2](https://arxiv.org/pdf/0806.0772v2), and [NSW corrected edition](https://www.mathi.uni-heidelberg.de/~schmidt/NSW2e/NSW2.3.pdf), local reciprocity and duality together with 8.6.3, 8.6.7 and 8.6.10.

The source convention p odd or k totally imaginary is retained. Real-place p=2 terms are not discarded outside that convention. These are mathematical local-condition corrections, not a claim of a new duality theorem.
