# Row 1891: retrieved prior proof and author-side core audit

2026-10-21. No publication and no QUEUE edits.

## Scope and attribution

The two conjectures must remain separate. Welker's Conjecture 8 asks about positive integer coefficients with h0=1 and the numerical g-theorem property WITHOUT symmetry. Ferudun's 17 October 2026 unrefereed manuscript claims precisely this intended Macaulay-growth assertion, not Conjecture 6 on the barycentric subdivision of an arbitrary convex polytopal boundary. The original source's printed lowering binomial operator is inconsistent with its own g-theorem statement. This audit concerns the conventional upper-growth operator. It is not an independent priority claim and does not resolve the whole corpus row.

## Retrieval

Author-site source ZIP and verification-report fetches returned HTTP403. An independent official Zenodo API record was accessible and supplied its own public deposited-file URLs. All three deposited files were retrieved from those URLs; sizes and MD5 hashes match the record. See RETRIEVAL_METADATA.json. Canonical PDF: 156596 bytes, SHA256 e38749f8ac54f08d01916145dc1870d2947d45f2e7afe05aa56e8e65fbc7e062. The canonical PDF hash prefix agrees with the author landing page PDF version query. The PDF was text-extracted and its core technical page 6 rendered and visually inspected. Copied sources remain exclusively in private_sources; downloaded programs were not executed.

Official record: https://zenodo.org/records/23430747
Author status: https://eulersolve.org/papers/owr-1782-017/

## Core argument checked

Write the factorial-log-concavity assumption as i*h_i^2 >= (i+1)*h_(i-1)*h_(i+1), and lambda_i=i*h_i/h_(i-1). The lambda_i decrease weakly, whereas the consecutive h-ratios decrease strictly. Thus h increases strictly to its first peak and decreases afterwards, with at most a two-term maximum plateau. Integer boundary case r=0 reduces to h=(1,1); no growth condition is needed when r<=1.

For an increasing step k put L=lambda_k>k and g_k=h_k-h_(k-1)>0. The first k ratios imply h_k>=L^k/k!, hence k!*g_k>=L^(k-1)*(L-k). The next-ratio bound gives

(k+1)*g_(k+1)/g_k <= L-1-k/(L-k).

The elementary bound (1-u)^(1/k)>=1-u/(k*(1-u)) for 0<u<1, applied to u=k/L, shows that the last expression is at most (k!*g_k)^(1/k). Both underlying logarithmic/exponential estimates have the correct orientation. Negative right sides cause no issue, because the same upper bound then forces the next difference to be negative. This proves the continuous bound without integrality.

The discrete step is a>=1 => a^{<k>} >= (k!*a)^((k+1)/k)/(k+1)!. I checked the induction on k, not merely its numerical examples. With leading Macaulay term C(n,k), residual b is in [0,C(n,k-1)-1] and the upper-growth decomposition is C(n+1,k+1)+b^{<k-1>}. The n=k case (a<=k) is separated before dividing by n-k+1 or using the later estimates.

For n>=k+1 the reduction uses P=n falling-factorial k, beta=k!*b, and beta_max=k!*C(n,k-1). A convex power lies below its secant over the specified finite interval. Minimizing the remaining power-minus-linear term on the larger half-line only weakens the lower bound, so it is valid even when the minimizer lies outside the finite interval. The resulting coefficient is gamma_k=(k+1)*(k-1)^(k-1)/k^k. Its bound gamma_k<=3/4, together with AM-GM for P^(1/k), yields the final estimate because 3*(k+2)/8 <= (k+1)/2 for k>=2. The k=1 base case and zero residual are handled separately. I found no circularity or dropped integrality assumption.

Combining the continuous and discrete bounds for k<r proves all initial-difference Macaulay inequalities. Newton's inequalities supply factorial log-concavity for positive-coefficient real-rooted h; the additional finite-degree factor is discarded in the valid direction. This establishes the stated nonsymmetric assertion if the classical Newton/Macaulay preliminaries are accepted.

## Assessment and limits

Author-side core proof audit: PASS for Theorems A and B, subject to independent adversarial review. No mathematical gap found in the general nonsymmetric proof. This is an internal mathematical assessment, not journal peer review. I did not reproduce the manuscript's extensive computational counts, verify its historical novelty claims, or audit every downstream bibliographic/corollary statement. Those are not needed for the core proof. An independent reviewer is examining the same hash-bound manuscript without reliance on the supplied verification reports.

Conjecture 6 remains the genuine residual target. A partial-row status is appropriate; a whole-row solved claim is not.
