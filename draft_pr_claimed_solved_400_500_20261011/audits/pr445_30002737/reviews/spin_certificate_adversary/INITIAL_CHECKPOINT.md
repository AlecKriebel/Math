# Sealed independent source reconstruction

UTC checkpoint: 2026-10-12T21:13:41.923899+00:00
Review completion estimate: 20% (criterion reconstructed; numerical implementation not read).

Scope: fresh adversarial review of an existing-source, finite numerical inequality, not an original proof search, candidate-paper review, priority certificate, or infinite family claim. No numerical validator code, report, result, or raw execution record was read before this checkpoint.

Primary source: Natalie Priebe Frank and Neil Mañibo, *Spectral theory of spin substitutions*, DOI 10.3934/dcds.2022105, published Example 10 (PDF page 32), Proposition 14 (PDF pages 28–29), and cocycle definition (PDF page 25). Source private PDF SHA-256: `7e4a477cbfc7c43e3384a5c082d30617418c9fd9b027921103664bd27b390954`.

## Exact source target

For the C4 spin matrix W = [[1,i],[1,-1]], the character χ1 gives B(x) = [[1,i],[exp(2πix),-exp(2πix)]]. The source cocycle uses the ordered product A_N(x)=B(x)B(2x)⋯B(2^(N−1)x). The source's almost-sure Lyapunov upper bound is f(N)=(1/(2N))∫_0^1 log ||A_N(x)||² dx. The Frobenius norm can upper-bound the relevant operator norm. The finite target is I_13=(1/13)∫_0^1 log S_13(x) dx < log 2, S_13=||A_13||_F², which implies f(13)<(log 2)/2.

Example 10 already reports Table 1 I_13≈0.682035 and all numerical errors <10^−3. This is a published claim to validate independently, not evidence that a new certificate is sound. Proposition 14's further conclusion requires its aperiodicity, primitivity, and full-rank hypotheses; its conclusion is singularity of each χ1 spectral measure (pure point or purely singular continuous). The finite certificate alone does not independently prove the proposition, these substitution hypotheses, pure singular continuity, or any novel result.

## Independent algebra reconstruction and boundary cases

Writing z=exp(2πix) and A_n=[[a,b],[c,d]], right multiplication by B(2^n x) gives (a',b',c',d')=(a+z^(2^n)b, ia−z^(2^n)b, c+z^(2^n)d, ic−z^(2^n)d), with A_0=identity. Its degree is at most 2^n−1. Since each old support lies below the shift 2^n, shifted and unshifted terms do not overlap; the nonzero polynomial coefficients are Gaussian integer units. At n≥1 there are 2^(n+1) units across all four entries, so S_n has constant coefficient 2^(n+1). Fourier coefficients satisfy C_−k=conjugate(C_k). Their real and imaginary parts are bounded in absolute value by 2^(n+1), sufficient for uniquely lifting residues modulo any prime >2^(n+2).

Each factor has determinant −(1+i)z^(2^n), so |det A_N|²=2^N and S_N≥2·2^(N/2)>0. Thus logs have no zeros or singularities on the integration domain. N=0,1 and small N are useful recurrence/order controls; x=0,1/2 and conjugate negative frequencies are important boundary controls. A transposed or reversed product needs an exact demonstrated Frobenius identity or other gauge equivalence; it cannot be silently substituted.

## Required analytic certificate chain

A checkable certificate must establish exact Gaussian polynomial coefficients and source product order; exact modular autocorrelation with unique signed recovery and no overflow; real-valued S through correct negative-frequency conjugation; valid enclosures of every cell mean m_j=cell-width^−1∫cell S; and a strictly positive lower enclosure on each mean. Concavity gives ∫log S≤(1/M)Σlog m_j. The direction is essential: upper bounds on positive m_j and on their logs produce an upper bound for I_13. The lower enclosure for log 2 must be strictly larger than the final upper I_13.

For an FFT cell-mean construction, root/half-angle intervals must be outward rounded, sinc Taylor remainders must cover the relevant arguments, every fixed-point input/twiddle/complex-multiplication/FFT-stage error must propagate to a proven final error, and the indexing must match cell centers. Power-series logarithm truncations and all printed decimals need exact integer provenance. Mathematical guards must execute under Python -O as well as normal mode. A finite set of accurate samples cannot replace this analytic chain.

## Falsifiable checks still pending

Read the producer's sealed full code and actual raw records only once final-ready. Reproduce normal and optimized runs from an immutable saved copy; verify hashes and exact threshold integers; compare small-N exact polynomial/autocorrelation against direct source-forward matrix multiplication; challenge root/error/Jensen faults with actual altered child runs where they directly test the claimed mechanism. Preserve any failed attempts and distinguish demonstrated failures from unresolved proof gaps.
