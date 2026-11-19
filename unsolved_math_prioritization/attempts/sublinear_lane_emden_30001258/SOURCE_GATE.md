# Source gate: sublinear Lane–Emden asymptotics

Problem 30001258 / OWR-3476-007; ordered row 1877. Checked 2026-10-21.

## Decision

**PARTIAL-LITERATURE / SCOPE-CORRECTION.** Do not claim a new solution of the original research direction. The literal unchanged extension of the displayed superlinear alternatives is false. Positive-solution asymptotics are established, and 2025 literature supplies substantial general-p nodal progress. The unnormalized least-energy nodal limit at the second eigenvalue remains unverified by this audit. That is not a proof that the residual is open.

## Original source versus extracted scope

Primary source: Enea Parini's contribution with Christopher Grumiau, “On the Lane-Emden problem for the p-Laplacian,” in Oberwolfach Report 26/2009, pp. 1457–1459, DOI https://doi.org/10.4171/OWR/2009/26; PDF https://ems.press/content/serial-article-files/46226?nt=1.

The question follows two theorems for q>p: fixed-parameter ground states and least-energy nodal solutions tend to infinity below their respective eigenvalue thresholds, to an eigenfunction at resonance, and to zero above threshold. It then asks about 1<q<p and warns that the variational structure changes. The extracted title emphasizes ground states but its statement includes nodal solutions. It suppresses the displayed alternatives and therefore obscures both the necessary reversal and the distinction between normalized convergence and an unnormalized resonant limit. Exact source text is retained privately, not reproduced here.

## Prior literature, checked before new proof work

1. Biezuner, Brown, Ercole and Martins, “Computing the first eigenpair of the p-Laplacian via inverse iteration of sublinear supersolutions,” https://arxiv.org/abs/1011.3172. This establishes normalized positive eigenpair convergence and is the extracted entry's existing reference. It does not justify leaving the entire positive branch unsettled.

2. Grey Ercole, “On the resonant Lane-Emden problem for the p-Laplacian,” https://arxiv.org/abs/1202.3980, published in Communications in Contemporary Mathematics 16 (2014), 1350023. Theorem 10 proves the positive resonant limit in C1 on smooth bounded domains, from both sides of p. With the positive first eigenfunction e normalized by its supremum, the limit is theta e, where theta=exp(-integral(e^p log e)/integral(e^p)). Corollary 13 explicitly gives zero below the first eigenvalue and infinity above it as q increases to p. This resolves the positive branch in that domain class.

3. Mieko Tanaka, “Remarks on the non-local eigenvalue problems for the p-Laplacian,” Boundary Value Problems (2025), https://doi.org/10.1186/s13661-025-02016-8. For nonnegative weight and C1,1 domains, Theorem 1.6 attains the least nodal eigenvalue mu_q; Proposition 1.7 gives mu_q→lambda_2 from below p. Lemma 2.1 supplies C1 subsequential compactness of Lq-normalized eigenfunctions. Corollary 1.12 identifies corresponding extremal nodal Lane–Emden solutions. These statements establish normalized nodal convergence; they do not by themselves establish the unnormalized resonant amplitude limit.

4. Bonheure, Moreira dos Santos, Parini, Tavares and Weth, “Nodal Solutions for Sublinear-Type Problems with Dirichlet Boundary Conditions,” https://arxiv.org/abs/2003.13587, IMRN 2022, 3760–3804, DOI https://doi.org/10.1093/imrn/rnaa233. The abstract and institutional publication record confirm nodal existence and the distinction between least-energy and mountain-pass levels for the ordinary Laplacian. This is relevant prior work, not a replacement for the general-p resonant assertion. Its full proof was not inspected here.

## Authored deductions and precise residual

Write E_lambda,q(u)=integral(|grad u|^p)/p-lambda integral(|u|^q)/q. At any nonzero solution,

E_lambda,q(u)=(1/p-1/q) integral(|grad u|^p).

For q<p the coefficient is negative. Thus least energy among actual nodal solutions means largest gradient norm, not smallest. This explains why the extremum in Tanaka's Corollary 1.12, whose exponent p(q-p)/q is negative, selects exactly least energy. It is not legitimate simply to copy the superlinear nodal Nehari minimization argument.

For a normalized nodal eigenfunction w_q with ||w_q||_q=1 and coefficient mu_q, the solution with fixed coefficient lambda is

u_lambda,q=(lambda/mu_q)^(1/(p-q)) w_q.

Direct substitution verifies the identity. The multiplier is common to all representatives of a normalized eigenpair, and the least nodal eigenvalue corresponds to least energy as above. Consequently Tanaka's convergence gives, on the indicated smooth domains, a normalized second-eigenfunction limit and the reversed nonresonant alternatives: u_lambda,q→0 for lambda<lambda_2, and its norm diverges for lambda>lambda_2. These are deductions from existing results, not claimed new theorems.

At lambda=lambda_2, the amplitude is exp(log(lambda_2/mu_q)/(p-q)). Merely knowing mu_q→lambda_2 is insufficient: the quotient in the exponent needs control. This audit has not verified the required first-order asymptotics, nor a theorem proving a nonzero finite unnormalized nodal resonant limit. Any next attempt must address this exact gap, and distinguish subsequential eigenfunction convergence from selection of a unique eigenfunction. Also retain smoothness assumptions: the extracted bare “bounded domain” is broader than the inspected results.

## Duplicate and prior-solution gate

Full local corpus scans covered 15,458 problem records and 6,701 research records. Exact identifier and relevant Lane–Emden/sublinear/resonant keyword combinations found only this problem record and no matching research result. This is a reproducible lexical negative, not a guarantee of no semantic duplicates. The existing entry's partial assessment omits the resonant positive theorem and 2025 nodal results.

## Publication boundary

No publication or queue edit was performed. This authored audit and PUBLIC_METADATA.json contain no copied PDFs, dataset entries, or private coordination. Raw PDFs, extracted text, and the dataset entry are private working evidence and must not be staged or published. Public metadata records source URLs, inspected theorem locations, corpus counts, file sizes, and hashes. All claims above are scoped to inspected evidence rather than an exhaustive assertion about current literature.
