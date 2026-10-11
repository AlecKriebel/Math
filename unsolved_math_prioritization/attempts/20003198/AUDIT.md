# Standalone correction patch for 20003198 / AIM-OTHER-0005

This is an AI-assisted, unrefereed authored mathematical audit and correction edition. Acceptance records an internal AI audit of prior-result status, normalization and written deductions. It is not external human peer review, journal acceptance, formal proof-assistant certification, or a novelty or priority claim.

This is not a computational reproduction package. The complete authored mathematical audit, every written formula and example, the full correction patch and all substantive acceptance qualifications are retained. Executable code, raw partition or moment datasets, copied source PDFs or text, source renderings, raw search responses and private coordination material are not distributed. Historical finite checks cannot be reproduced from this edition alone.

Retrieval, inspection and mathematical-check statements describe the original audit of October 11, 2026 UTC. Editorial preparation performed no new scholarly-source retrieval, source-body inspection, literature survey or mathematical execution.

This patch supplies corrected authored wording. Original source documents are cited, not reproduced or modified.

## Replace the mean/OCR explanation

The original AIM page visibly prints the factor a+b−1 in the preceding mean formula. This is a source-level typographical error, not merely an OCR loss. The correct mean is (a−1)(b−1)(a+b+1)/24. The requested quantity remains the unnormalized raw sum S_i=Σ|λ|^i over all coprime positive moduli a,b.

## Replace the Ekhad–Zeilberger status paragraph

Ekhad–Zeilberger arXiv:1508.07637v2 adds a September 1, 2015 front-page update stating that all its theorems are rigorously proved, crediting Johnson's polynomiality mechanism and Thiel–Williams' feedback. This update supersedes the paper's unchanged internal conjectural language. General central-moment formulas through order six, and consecutive-modulus formulas through order nine, are prior work. The present audit verifies the proof mechanism and finite supporting cases but does not independently reproduce every coefficient or its full interpolation certificate.

## Correct the third-moment normalization wherever reused

Let N=(a+b)^(−1) binom(a+b,a), μ=(a−1)(b−1)(a+b+1)/24, and

T=ab(a−1)(b−1)(a+b)(a+b+1)(2a²b+2ab²−3a²−3ab−3b²−3)/60480.

The correct relation is (1/N)Σ(|λ|−μ)^3=T, or equivalently Σ(|λ|−μ)^3=N T. The 31-page arXiv full version omits 1/N in Theorem 1.6, both on physical page 2 and its restatement on page 25. The official FPSAC 2016 Theorem 1.6 includes it. For (3,5), the central cubic sum is 90 and the normalized moment is 90/7.

## Use exact raw-sum conversions

With V=ab(a−1)(b−1)(a+b)(a+b+1)/1440, the AIM sums are S_1=Nμ, S_2=N(μ²+V), and S_3=N(μ³+3μV+T). More generally S_i=NΣ_j binom(i,j)μ^(i−j)c_j, with c_0=1,c_1=0. Fourth and higher central moments must not be substituted for cumulants.

## Replace any all-order or novelty overclaim

Polynomiality and all-order finite computation are known: normalized raw and central moments have degree at most 2i in each modulus, hence at most 4i total. The raw S_i includes N and is not itself a bounded-degree bivariate polynomial. The modulus-two Bernoulli formula is an elementary special case, not a solution for all coprime moduli. No new compact arbitrary-order formula is accepted. The AIM problem does not specify a compactness criterion; a future claim of full resolution must state and meet the intended exact requirement.

## Citation correction

The link labeled “Strange Expectations” in the Ekhad–Zeilberger update erroneously points to arXiv:1502.07934 (Johnson). Thiel–Williams' identifier is arXiv:1508.05293. The later journal and FPSAC versions are distinct documents and must not inherit the arXiv typo without inspection.
