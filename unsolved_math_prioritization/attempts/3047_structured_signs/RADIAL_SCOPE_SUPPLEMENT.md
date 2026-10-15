# Late scope supplement: exponential flatness is compatible with arbitrary signed factors

This is a separately pinned supplement. The two audited structural proofs are unchanged.

## Verified cited theorem and its application

[C. Sinan Güntürk, *Approximation by power series with ±1 coefficients*, IMRN 2005(26), 1601–1610](https://doi.org/10.1155/IMRN.2005.1601), Theorem 1, was checked in the [official arXiv manuscript](https://arxiv.org/pdf/math/0503373). The theorem allows 0≤μ<1 and 1≤M<∞. Its approach region is R_M={z: |1−z|≤M(1−|z|)}. Set μ=0, M=1 and target function f≡0. Since R_1=[0,1], the theorem supplies a single power series Q(z)=∑q_nz^n with every q_n∈{−1,1} and constants B,c>0 such that

|Q(r)|≤B exp(−c/(1−r)),  0≤r<1.

Multiplying Q by −1 if needed makes q_0=1 without changing the bound. Therefore a universal subexponential radial lower bound for arbitrary normalized ±1 series is false. This is a checked use of a published theorem, not an independent certification of its proof or construction.

## Elementary amplification across finitely many factors

The theorem does not identify c with the partition constant C=π²/6. Nevertheless, its unspecified positive c is sufficient for the following deduction.

Choose an integer K and replace the original factors of indices m=1,…,K by Q(q^m), retaining positive geometric factors for m>K. This is an admissible finite active set for the unrestricted sign model: each replacement has constant 1 and all other coefficients ±1. With H_K=∑_{m=1}^K1/m, the bound 1−e^{−mt}≤mt gives

∏_{m=1}^K |Q(e^{−mt})|≤B^K exp(−c H_K/t).

Because H_K diverges, some finite K satisfies cH_K>C. The exact finite-replacement identity and log E(e⁻ᵗ)≤C/t then imply

|P(e⁻ᵗ)|≤B^K exp(−(cH_K−C)/t).

Here the additional factors ∏_{m=1}^K(1−e^{−mt}) are positive and at most 1. Thus arbitrary sign sequences in a sufficiently large finite collection of factors can meet, and exceed, the necessary radial-suppression threshold identified by the structural proof.

This deduction still provides no bound on the Taylor coefficients of P. Small values on one radius allow cancellations and are not sufficient for the required coefficient-by-coefficient condition. It also gives no explicit optimal K and makes no novelty claim. Both accepted structural theorems remain intact because their restrictions supply lower bounds that this general Q cannot satisfy.

## Source/version distinction

The inspected PDF identifies arXiv:math/0503373v1, submitted 18 March 2005. Its internal typeset date is 6 July 2018; that is not treated as evidence of a later arXiv revision. Journal volume, issue, pages and DOI were separately corroborated on the Oxford publisher page. No source program was executed.
