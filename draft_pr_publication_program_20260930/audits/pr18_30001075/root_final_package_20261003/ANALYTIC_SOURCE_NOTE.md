# Area-formula dependency: upstream proof slips and the corrected argument

Observation: 2026-10-03T22:21:26Z. ROOT read the displayed Case (ii) on printed page60/PDF page34 of Leon Simon's Stanford-host NTU notes through the fresh second reviewer's private rendered page. Source PDF: 1,234,390 bytes, SHA256 ba7fd4a53bf0f1d0ac54aec50bb72c4bba196b8e784d65cd0a7fd85131a3bf03. The third-party body remains private. This is a dependency audit note, not a new mathematical discovery or an edit to the cited source.

The source's error estimate for the augmented map is incorrect: for domain dimension1 and constant f, the augmented Jacobian is epsilon, which is not bounded by C epsilon-squared for a fixed C as epsilon tends to zero. The integration-domain and projection-dimension labels in the same passage also need correction. The area-formula theorem statement used by the manuscript is correct.

Here is the valid argument needed at the zero-Jacobian parameters. Write L for a Lipschitz bound and let sigma_1,...,sigma_n be the singular values of Df. At a differentiability point with Jf=0, at least one singular value is zero. For F_epsilon(x)=(f(x),epsilon x),

    JF_epsilon = product_i sqrt(sigma_i^2 + epsilon^2)
               <= epsilon (L^2 + epsilon^2)^((n-1)/2)
               <= epsilon (L^2 + 1)^((n-1)/2),  0 < epsilon <= 1.

F_epsilon is injective and has full derivative rank. The source's preceding full-rank case applies on a measurable A contained in R^n of finite measure. Integration is over A, and the projection is from R^m x R^n to R^m. The projection is 1-Lipschitz, so the n-dimensional measure of f(A) is at most the integral over A of JF_epsilon, which tends to zero by the displayed uniform bound. Countable bounded-domain exhaustion handles local Lipschitzness and domains of infinite measure; the nondifferentiability set has a null image by the Lipschitz null-image bound.

For the manuscript's n=m=3 application, the bound is simply epsilon (L^2+1). This independently supports the exact zero-Jacobian implication needed for every bounded parameter-height patch. The paper invokes the correct standard area-formula statement, with Borel selected subsets and exceptional fibers treated explicitly; none of its displayed estimates uses the upstream incorrect bound. No manuscript, metadata or portable-package repair is required for this informational source finding.

Best estimate at this dependency checkpoint: PR18 review/publication workflow80%; the second review's complete final package verdict and actual publication remain pending. Original research accounting remains1/5, with no new central-attempt credit. No outside-individual communication is proposed or initiated.
