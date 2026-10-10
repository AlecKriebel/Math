# Corollary covering the original Hurst range and every sample count

**Accepted all-H supplement after independent AI mathematical audit, 10 October 2026.** This is separate from the companion rough-range proof and makes no new-priority claim for the already known smooth or Brownian cases. AI-assisted and unrefereed; no formal proof-assistant or novelty certification is claimed.

## Statement

For every fixed (H\in(1/4,1)), independent standard fractional Brownian components (B^1,B^2), all (T>0), and every integer (n\ge1), the canonical iterated integral (X_T=\int_0^T B^1_s\,dB^2_s) satisfies
\[
 \left\|X_T-E\left[X_T\mid B^i_{jT/n},\ i=1,2,\ j=1,\ldots,n\right]\right\|_2
 \ge c_H T^{2H}n^{1/2-2H}
\]
for a constant (c_H>0). The constant may be chosen by formula (15) of the companion proof, with its same definitions (6)–(7), for the entire range (1/4<H<1).

## Proof of the extension

Apply the companion proof without restricting (H) below (1/2). All required analytic facts still hold:

1. (D_H\in(0,\infty)) for (0<H<1), as proved in Section 2 there.
2. Now (\alpha=2H+1\in(3/2,3)). The two cell functions still obey the same Fourier bound (O(|\eta|^{-3})). Their squared weighted Fourier transforms are (O(|\eta|^{\alpha-6})) at infinity, with exponent strictly below (-3). Hence they are integrable and their periodizations are bounded. The displayed upper bound (7) remains valid: (5-\alpha>2>0). No inequality later in the proof requires (\alpha<2).
3. The identities (3)–(14), the PSD trace bound, Gaussian independence, and the scaling cancellation are unchanged.
4. The only remaining input is the left-sum (L^2) convergence in (2). Neuenkirch–Tindel–Unterberger, *Discretizing the fractional Lévy area*, [arXiv:0902.0497](https://arxiv.org/abs/0902.0497), Theorem 1.1 on p. 3, provides it in the smooth cases as well: its squared errors are of order (m^{1-4H}) when (1/2<H<3/4), (m^{-2}\log m) when (H=3/4), and (m^{-2}) when (3/4<H<1). All tend to zero. The immediately following Brownian calculation gives squared error (T^2/(2m)) when (H=1/2). Only convergence is used. The correct journal citation is SPA 120 (2010), 223–254, DOI [10.1016/j.spa.2009.10.007](https://doi.org/10.1016/j.spa.2009.10.007).

Thus every step of the witness proof applies, and formula (15) supplies a positive constant for every (H\in(1/4,1)), independently of (n,T). This directly proves the finite-(n) assertion rather than inferring it from an asymptotic lower limit.

## Attribution and exclusions

The rough residual (1/4<H<1/2) is the substantive target of the companion proof. The smooth-range asymptotic optimal rate is already established by Neuenkirch–Shalaiko, J. Complexity 33 (2016), 107–117, DOI [10.1016/j.jco.2015.09.008](https://doi.org/10.1016/j.jco.2015.09.008). The known Brownian optimum is (T/(2\sqrt n)); our explicit witness constant is weaker and not claimed sharp.

No new upper-bound proof, exact asymptotic constant, endpoint (H=1/4) construction, or arbitrary/adaptive sampling claim is included. In particular, the original question's demand for a positive rate constant does not demand the stronger existence of an exact normalized-error limit. The canonical iterated-integral normalization and conditioning on both components remain unchanged.
