# Independent adversarial review of the sealed source-question reconstruction

Author: Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X.

Verdict: **PASS, conditional on the explicitly imported Sah–Sawhney Theorem 1.1.** I found no blocking mathematical error in the sealed report. The exact relative-equidistribution threshold, universal weighted folding approximation, critical profile, supercritical asymptotics, source-free necessity, and ordinary-copy counterexample follow as claimed. This review does not reprove the deep LLT and makes no novelty or priority finding.

## Scope and authentication

This initial review read only the sealed `source_question_family` authored inputs, its identified primary-source payloads, applicable root AGENTS.md, and the PDF skill. It did not read the candidate/submitted proof, root mathematical notes, any other mathematical or priority family, or outcome records. Parent operational coordination supplied the seals and cautioned that the existing checker writes beside its own script; that checker was therefore run only as a byte-identical copy in my ignored scratch directory. No external communication, Git/index/ref mutation, or publication/service mutation occurred. A read-only branch check returned `main`.

The supplied immutable anchors were authenticated at the start:

- manifest: `38baf9a41f990381cab08031876e3875911a9b6e0303caffe2cd93e447792934`;
- report: `0e4fd0fed52de636fe1567919385bdc64fb6d885bde272ff40b955f4af174187`;
- verdict: `608f71e750dc72b4209d3daec49a1b0e65e06c94aee6d0c6c3c32dc5ceb3d17d`.

All eight members of the source manifest's `files` array matched their byte sizes and SHA-256 values. Fresh downloads of both official PDFs also matched the source receipts exactly, and fresh text extraction matched both cached text hashes. Its `source_payload_inventory` and `scratch_inventory` are separate receipts, not authored membership. The end authentication is preserved with the start authentication in `input_authentication.json`.

The falsifiable target is: for one fixed p in (0,1), with T the ordinary count of unordered triangles in G(n,p), D_n(q)=max_{0<=a<q}|q P(T=a mod q)-1| tends to zero along a positive integer sequence q_n exactly when q_n=o(n²). No primality, monotonicity, or unboundedness is assumed. Statements involving sigma are understood for n>=3; the review is asymptotic in n. Nondegenerate 2K2 statements require n>=4.

## Primary-source interfaces

I read the complete Scott–Tateno contribution at printed 1279–1280 / PDF 55–56 and visually checked those two pages. Its variable is the ordinary triangle count at fixed p; its sigma is standard deviation of order n². The displayed modular metric has absolute values, and its announced LLT uses the centered Gaussian cell with endpoints (k-mu±1/2)/sigma. It announces q=o(n²/log n) and asks for the extent of the range. Its final fixed-H conjecture is a separate broader statement. [Original OWR source](https://ems.press/content/serial-article-files/46223?nt=1).

For [Sah–Sawhney arXiv:2006.11369v1](https://arxiv.org/pdf/2006.11369v1), I freshly read exact PDF pages 3, 9–10, 23–24, 31–32, and visually inspected page 3. Theorem 1.1 is genuinely an independent-edge G(n,p) theorem for connected ordinary subgraph counts, with actual mean and standard deviation and lattice (Z-mu_H)/sigma_H. Its scaled pointwise error is O(n^(epsilon-1/2)). Section 4.1 counts edge-subgraphs once each; K3 therefore has expectation binom(n,3)p³, not six times that count. Section 4 and Lemma 4.1 concern G(n,m), while page 31 concludes the independent-model density estimate. In Section 3.1 the lemma’s sigma is the G(n,p) standard deviation of W3, of order n^1.5 for triangles, and K removes W0 and W2; this is a different normalization from the full independent-model standard deviation of order n². Theorem 1.3 and Section 6 explicitly cover the ordinary 2K2 obstruction. These interfaces suffice for the import; no claim of a whole-PDF proof audit is made.

Choosing lambda=min(p,1-p)/2 and H=K3 satisfies the source hypotheses. With epsilon=1/8 the scaled pointwise error is delta_n=C_p n^(-3/8). An induced-count exceptional-density issue is irrelevant. The reconstruction does not transplant the fixed-size characteristic-function lemma into the independent model. That unsupported transplant remains a blocked route, while the valid route imports the actual independent-model theorem.

## Independent mathematical checks

### Moments, lattice, and tails

Write N=binom(n,2), C=binom(n,3), v=p(1-p), xi_e=X_e-p, and b=p²(n-2). The centered expansion is

T-mu = b sum_e xi_e + p sum_adjacent{e,f} xi_e xi_f + sum_triangles{e,f,g} xi_e xi_f xi_g.

The monomials are distinct orthogonal products of independent centered edge variables. There are 3C adjacent unordered pairs and C triangles. Hence Var L=N(n-2)²p^5(1-p), Var R=3C p^4(1-p)²+C p³(1-p)³, and

sigma²=Cp³(1-p³)+12 binom(n,4)p^5(1-p) ~ p^5(1-p)n⁴/2.

The empty graph and a single triangle with isolated vertices give T=0 and T=1 with positive probability for n>=3. Primitive span 1 is established without claiming interval support. Replacing T by 6T would invalidate small-modulus uniformity; the negative control q=2 gives D(6T)=1 at every n.

Each edge changes T by at most n-2. Bounded differences therefore gives P(|T-mu|>Lsigma)<=2 exp(-2kappa L²), kappa=p^5(1-p)>0, because sigma²>=kappa N(n-2)². Constants may depend on this fixed p. One explicit sufficient choice is L=A_p sqrt(log n), A_p²>=max(20,6/kappa): then sigma times this probability and exp(-L²/2) are O_p(n^-10). There is no uniformity claim in p approaching 0 or 1.

### Universal folding (F), including arbitrarily large q

Set m=min(q,sigma) and g(k)=sigma^-1 phi((k-mu)/sigma). The progression a+qZ has at most 2Lsigma/q+1 points in the truncation window. The weighted central error is thus at most

m delta_n sigma^-1(2Lsigma/q+1)<=delta_n(2L+1).

The actual omitted tail, weighted by m, is at most sigma times the preceding tail bound. For the Gaussian tail, with h=q/sigma, a one-sided decreasing progression is bounded by phi(L)+h^-1 integral_L^infinity phi. Multiplication by m/sigma=min(h,1) bounds both coefficients by one, and the two-sided error is at most 2[phi(L)+integral_L^infinity phi]=O(exp(-L²/2)). This argument remains valid for tiny h, q=1, q beyond the entire finite support, and unboundedly large q. Thus the report proves exactly

sup_{q>=1,0<=a<q} min(q,sigma)|P(T=a mod q)-sum_j g(a+jq)|
 <= C_p n^(-3/8)sqrt(log n)+O_p(n^-10).

It does not illegitimately sum a pointwise LLT over infinitely many sites or over the full support of order n³.

### Sufficiency and the critical profile (K)

Poisson summation for the Gaussian yields, with theta=(a-mu)/q modulo one,

q sum_j g(a+jq)=W_h(theta)
 =1+2 sum_{ell>=1} exp(-2pi²ell²/h²)cos(2pi ell theta).

If h->0, the absolute discrepancy is at most 2 sum exp(-2pi²ell²/h²)->0, and (F) has exactly the q weight needed. This proves sufficiency for every subcritical sequence, including bounded q, q=1, composite q, and arbitrarily slowly diverging sigma/q.

For h->c in (0,infinity), the multiplier q/min(q,sigma) stays bounded. The series is uniformly convergent on a compact h-neighborhood, the phase grid has mesh 1/q->0, and its translation may drift arbitrarily. All Fourier coefficients are positive, so the continuum maximum of |W_c-1| is exactly

F(c)=2 sum_{ell>=1} exp(-2pi²ell²/c²)>0,

attained at theta=0. This proves the displayed limiting maximum absolute discrepancy, independent of the mean's phase.

A useful negative boundary check: at finite q, the residue nearest the positive Gaussian peak need not maximize the absolute discrepancy. In my fresh test h=2, q=101, drift=0.4999, the sampled negative trough beats the sampled positive peak by about 6.9442e-6; the actual maximum is still only about 1.0701e-8 below F(2). My initial checker mistakenly imposed equality with the nearest positive peak and correctly failed. I replaced that unsupported finite-grid assertion with the valid mesh bound 0<=F(h)-gridmax<=F(h)-nearest_positive_peak. This is a reviewer test correction, not a defect in the sealed proof: the report uses the dense-grid limiting argument and does not assert the false finite-grid claim.

### Supercritical profile (U)

For h->infinity, select the Gaussian progression point nearest zero. Its contribution is at most phi(0), and all others sum to at most 2 sum_{j>=1}phi((j-1/2)h)=o(1). The residue containing an integer nearest mu gives a lower bound tending to phi(0), since its normalized distance is at most 1/(2sigma). Formula (F), now weighted by sigma, transfers this to max_a sigma P(T=a mod q)->phi(0).

Writing M=max_a P(T=a mod q), the positive deviation is qM-1, while every negative deviation is <=1. Because qM~h phi(0)->infinity, eventually the positive deviation dominates. Therefore D_n(q)/h->phi(0), including moduli larger than the entire support. No hidden restriction q=O(n³) occurs.

### Necessity and compact-frequency estimate (N2)

For q>=2, the first Fourier coefficient obeys |E exp(2pi i T/q)|<=sum_a|P_a-1/q|<=D_n(q). For bounded real |t|<=B, u=b/sigma=O_p(n^-1), and the centered Bernoulli factor has

log E exp(i t u xi_e) = -t²u²v/2 + O_{p,B}(|u|³).

The branch is defined near one for all sufficiently large n, uniformly in t. Summing N factors gives error O_{p,B}(n^-1); replacing N b²v/sigma² by one costs another O_{p,B}(n^-1). Finally

|E exp[it(T-mu)/sigma]-E exp(itL/sigma)|
 <= |t| E|R|/sigma <= B sqrt(Var R)/sigma = O_{p,B}(n^-1/2).

This proves the claimed uniform compact-frequency CLT. It neither assumes R independent of L nor requires such independence. The R bound only uses its variance.

If q_n is not o(sigma), take an infinite subsequence with q_n/sigma>=epsilon>0. Then t_n=2pi sigma/q_n stays in a fixed compact interval, including possible approach to zero. Centering changes no modulus, so D_n(q_n)>=exp[-2pi²(sigma/q_n)²]-o(1)>=exp(-2pi²/epsilon²)-o(1)>0. This proves necessity for oscillating sequences as well as critical and supercritical ones, independently of the deep LLT. q=1 cannot persist on this subsequence.

### Centered cells

For z=(k-mu)/sigma, the centered interval cancels the odd Taylor term. The uniform second-derivative bound gives

|c_n(k)-sigma^-1 phi(z)|<=||phi''||_infinity/(24sigma³).

Here ||phi''||_infinity=phi(0); sigma~c_p n², so the error is O_p(n^-6). The imported LLT becomes unscaled O(n^-5/2+epsilon), recovering the original o(n^-2) statement for epsilon<1/2. The sampled-density total mass differs from one only by Gaussian Poisson terms of order exp(-2pi²sigma²); no normalization correction affects the argument.

### Ordinary 2K2 obstruction

For n>=4 let M be edge count, W wedge count, and X ordinary unordered pairs of vertex-disjoint edges. Direct pair classification gives X=binom(M,2)-W. Extra edges do not remove these non-induced copies.

Conditionally on M=m, set s=3binom(n,3), d=2(n-2), A=N binom(d,2), r_j=(m)_j/(N)_j. Distinct wedges share exactly one edge in A unordered pairs, and otherwise use four edges. Exact variance expansion gives

Var(W|M=m)=s(r_2-r_4)+2A(r_3-r_4)+s²(r_4-r_2²).

For m=floor(pN), the stated fixed-j hypergeometric expansion gives r_3-r_4=f³(1-f)+O_p(N^-1) and r_4-r_2²=-4f³(1-f)/N+O_p(N^-2). The n⁴ contribution cancels through 2A-4s²/N=-2s, leaving O_p(n³). A fixed positive conditional probability then lies among O_p(n^1.5) integer X values; P(M=m)>=c_p/n gives an atom >=c_p n^-2.5.

The independent centered expansion of X has linear coefficient p binom(n-2,2) per edge and one quadratic monomial per disjoint edge pair. Thus its variance is N binom(n-2,2)²p³(1-p)+3binom(n,4)p²(1-p)²~p³(1-p)n⁶/8. Hence sigma_X max_x P(X=x)>=c_p sqrt(n), excluding a Gaussian LLT. This reproduces the credited existing obstruction, with ordinary-copy rather than homomorphism counts. The formulas with r_4 require N>=4 and nondegenerate X needs n>=4; n=3 has X identically zero and is not a contrary case. I recommend retaining that explicit domain in any promoted exposition, but it is not an asymptotic gap in this report.

## Computation, negative controls, and reproducibility

Run `python3 independent_checks.py` from this review folder. It uses only the standard library and explicit exceptions, not removable assertions. The fresh checker was written before reading the sealed checker code. It independently enumerates all 33,864 labeled host graphs through n=6 once, tests exact rational weights at p=1/5,1/2,4/5, and verifies mean, covariance/orthogonality, both forms of triangle variance, every conditional edge count for n=4–6, ordinary 2K2 identities and moments, primitive support, all finite Fourier inversions up to binom(n,3)+5, and first-coefficient bounds. Huge-modulus tests use q=10^12 and 10^100 without allocating those residue arrays. It tests actual-versus-projection characteristic-function errors against the L2 remainder bound on a bounded t grid.

It also compares Gaussian direct and dual series at 48 (h,theta) pairs, tests progression tails, critical grids with drifting phases (60 cases), supercritical maxima, the compact-t Bernoulli logarithm at n=20,100,500,2000, and centered-cell errors. The largest Fourier inversion error was 2.89e-15; the largest direct/dual Gaussian difference was 1.05e-11, at very large h. These floating checks are corroboration, not validated interval proofs or proofs of asymptotic rates. The algebraic arguments above establish the asymptotic results.

Three intentional errors were rejected: a missing factor two in triangle covariance, replacement of ordinary T by 6T, and a halved wedge-pair coefficient in conditional variance. The fresh checker also exposed my own false finite-grid peak assertion, as explained above. The source checker was separately rerun in ordinary Python mode from a hash-identical scratch copy; its assertions passed. Optimized execution of that assertion-based script was neither used nor counted as verification.

## Status and exact remaining gap

Strongest verified result: every mathematical claim in the sealed reconstruction survives this fresh adversarial review, with the independent-model LLT explicitly imported. The universal folding and CLT necessity deductions are checkable elementary postprocessing. Mechanism status: this is independent verification of the same established-LLT reconstruction mechanism, not a distinct deep LLT proof. No unsupported equivalence is being counted as a solution. The fixed-size Fourier-lemma transplant remains blocked absent a new model/normalization transfer.

Remaining gap for the stated triangle threshold: none after admitting Sah–Sawhney Theorem 1.1 as a named standard import. Deep theorem proof audit: not performed. Novelty/priority audit: not requested and not performed; no new-discovery claim is supported here. Review completion: 100%; asserted completion toward an original new discovery: 0%. The sealed outputs and exact source read scopes are inventoried in this review's manifest and provenance receipts.
