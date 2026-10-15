# Prior credited density reconstruction

This is the complete EP-1095 section of the preceding source screen, retained as dated mathematical context. Its witness-only verification through 400 and independent minimality through 20 describe that earlier screen. The separate continuation extends the independent minimality scope to 46. The density and model-ratio proofs below predate this continuation and are not claimed as new results of it.

## 1745. Erdős–Selfridge admissibility: exact finite criterion and density

For k>=2 and each prime p<=k, put a_p=floor(log_p k), and write the base-p digits of k as k_i (0<=i<=a_p). Define

M_k=product_(p<=k) p^(a_p+1),
R_k=product_(p<=k) product_(i=0)^(a_p)(p-k_i).

For n>=k, no prime at most k divides binom(n,k) if and only if every base-p digit n_i is at least k_i, for every p<=k and i<=a_p. Here is a short proof (the standard Lucas criterion): over F_p, (1+x)^(p^i)=1+x^(p^i), so expanding (1+x)^n by the base-p digits and taking the x^k coefficient gives binom(n,k) congruent to product_i binom(n_i,k_i) modulo p. Each factor is nonzero exactly when k_i<=n_i; the factors then involve factorials of integers below p. For i>a_p the digit of k is zero and imposes no restriction.

For each p there are exactly product_i(p-k_i) admissible residues modulo p^(a_p+1). The Chinese remainder theorem gives exactly R_k admissible residue classes modulo M_k. Consequently the number A_k(x) of admissible n with k+1<n<=x satisfies

A_k(x)=(R_k/M_k)x+O(R_k+k+2)

with the explicit absolute error at most R_k+k+2. This is a fixed-k statement and proves existence; it does not control the first admissible residue uniformly as k grows. In particular n=M_k-1 is admissible because all relevant digits equal p-1. For k>=3 it exceeds k+1, yielding g(k)<=M_k-1. For k=2, M_2-1=3 is the deliberately excluded value k+1, so this bound is not asserted; direct checking gives g(2)=6. This is weaker than the classical exp((1+o(1))k) bound.

The elementary modulus upper bound already appears in Ecklund–Erdős–Selfridge(1974). The CRT density is a credited reconstruction of Sorenson–Sorenson–Webster(2020), Theorem5.2; their transfer from density to typical size of the least residue explicitly uses a uniform-distribution heuristic. A numerical approximation to R_k/M_k therefore cannot establish the desired asymptotic for g(k), or either successive-ratio conjecture. The separate elementary case k=1 is g(1)=3.

The June2021 Sorenson–Sorenson–Webster addendum, arXiv1907.08559v3, was then retrieved and read in full. It gives g(376),g(377), proves limsup ghat(k+1)/ghat(k)=infinity for the density model ghat=M_k/R_k, and identifies its logarithmic asymptotic constant as sum_(a>=1) log(1+1/a)/(a+1)=0.7884305.... This improves the published2020 interval[0.530684...,1] for the model's constant, not for actual g. The limit-superior proof can be checked directly: if k+1 is prime, M_(k+1)/M_k=(k+1)^2; no base-p carry occurs in incrementing k for p<=k, and the new prime contributes k(k+1) to R. Hence

ghat(k+1)/ghat(k)=((k+1)/k) product_(p<=k) (p-(k mod p))/(p-1-(k mod p)) >= product_(p<=k) p/(p-1).

Every denominator is positive because p does not divide k+1. Mertens's product theorem, a named standard external input, makes the last product asymptotic to exp(gamma) log k along these k. This is a full credited proof for ghat only. The addendum's exact-constant proof was read, but its prime-number-theorem error estimates were not independently re-audited here. None of these statements proves either successive-ratio claim for actual g.

The October2026-read Alexander Eastwood repository and its dated14September2026 research note report a table through k=400. Our authored exact verifier checks the admissibility of each of its 400 integer witnesses by independent digit and direct binomial-mod-prime calculations, and verifies minimality only for k<=20 by an exhaustive scan. For the larger entries it supplies upper bounds, not a new minimality certification; the source itself distinguishes those tasks and records substantial shared-component GPU searches. No source-author code was run. The unrestricted asymptotic and ratio questions remain unresolved by this screen.

