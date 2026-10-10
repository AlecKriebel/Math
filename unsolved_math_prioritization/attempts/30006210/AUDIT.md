# Independent adversarial audit: Boolean polynomial compatibility

## Decision

ACCEPT the exact two-polynomial theorem in the frozen candidate identified below. No blocking mathematical gap was found. The claim is a source-credited consequence of a 2026 separator theorem together with the fully supplied covariance argument. This is an AI-assisted independent internal mathematical audit. The proof and audit are unrefereed; no external human peer review, formal proof-assistant certification or priority determination is claimed.

For every positive integer n and d and every pair of nonzero real multilinear polynomials f,g on {-1,1}^n of degree at most d, all coordinate relative influences at most 1/(4096 d^8) imply intersecting supports. Relative influence is the Fourier coefficient mass on sets containing the coordinate divided by the full squared L2 norm, including the constant coefficient. The contrapositive established in the candidate is the stronger lower bound 1/(1024 d^8) on the maximum influence when the supports are disjoint.

The independently accepted original `PROOF.md` was 13,421 bytes, SHA-256 `45c4e687846fd0683a97f7a35321b5ab5bbfd36c2b70c7d208040910339c09b2`. This edition explicitly updates its pending-audit header and clarifies that supplementary executable checks are not distributed. Its entire theorem and proof body, source credits and exponential-endpoint warning are unchanged. ACCEPTANCE.json distinguishes the original proof identity from the distributed editorial edition.

## 1. Target and source authentication

The original question is Per Austrin's contributed section, “Zeros of Low-Degree, Low-Influence Polynomials on the Boolean Hypercube,” on printed p. 445 of the [2025 Oberwolfach report](https://doi.org/10.4171/owr/2025/9). The displayed denominator ranges over every subset of [n]; it does not exclude the empty set. I inspected the rendered original page, not only an OCR extract.

The decisive newer source is Longcheng Li, Qian Li, Xingjian Li, and Qipeng Liu, [*Impossibility of Perfectly Complete Many-Round Key Agreement in the QROM*, arXiv:2608.03824v1](https://arxiv.org/abs/2608.03824v1), submitted 4 August 2026. I independently retrieved the PDF and abstract page. Its Lemma 3.5, printed pp. 7–8, expressly allows real-valued polynomials. Its hypothesis is pointwise disjointness of supports on the whole cube. Neither positivity, Boolean range, normalization, nor a lower bound on nonzero values is required.

The source states a promise separator; its actual proof explicitly gives arbitrary labels to subcubes on which both restricted polynomials vanish. Consequently it defines a total Boolean function with the required support labels. This is a genuine feature of the source proof, not an additional unsupported inference from its cryptographic conclusion. I visually inspected the lemma's statement and complete proof on pp. 7–8 and its Markov ingredient on p. 5.

The primary supporting reference is Robin Kothari, Matt Kovacs-Deak, Daochen Wang, and Rain Zimin Yang, [*Rational degree is polynomially related to degree*, arXiv:2601.08727v3](https://arxiv.org/abs/2601.08727v3), revised 28 September 2026. I independently downloaded its PDF and abstract page and checked Fact 5, Theorem 1, and Corollary 1, including the rendered p. 4. Absolute-value bars on the derivative, imperfectly represented by text extraction, are visibly present in the PDF. The candidate uses the standard classical Markov inequality in exactly the correct normalization.

The versions, retrieval facts, and file digests are separately recorded as verification metadata. Both principal sources were inspected as arXiv manuscripts; this audit does not claim a separately verified journal publication or independent endorsement of their entire cryptographic contents.

## 2. Audit of the quantitative separator

I first reconstructed the source argument independently, before reading the frozen candidate. Its numerical depth bound is valid.

At a nonterminal subcube, both restricted polynomials are nonzero. Neither can be a nonzero constant, because disjointness would then force the other to be zero. Thus the degree maximum D is at least one. The function s=p^2−q^2 is not identically zero: disjoint supports prevent cancellation of the two squares at any point where either polynomial is nonzero. Its multilinear representative has degree at most 2D.

Choose a vertex maximizing |s| and call the polynomial vanishing at that vertex q, interchanging the two names if necessary. Choose a maximal disjoint family of maximum-degree monomial supports M_j of q. These are distinct notions of maximality, and the frozen candidate distinguishes them correctly. Fixing coordinates outside M_j cannot change its top coefficient: only a strict superset could contribute another term to that coefficient, and no such superset occurs. The restricted polynomial is therefore nonzero, while its value at the selected vertex is zero. Some nonempty block E_j within M_j changes its value to nonzero. All E_j are disjoint. At the changed points disjointness forces the sign of s to reverse.

Replacing each block by a single bit does not increase the degree beyond 2D, even when several original coordinates depend on that bit: after substitution, multilinearization only reduces degrees. Normalization by the maximum |s| gives a bounded polynomial R, with R(0)=1 and R(e_j)<0.

For completeness, the numerical switching bound follows directly from Bernoulli symmetrization. Let P(t) be the expectation of R under independent Bernoulli(t) coordinates. Then deg P is at most m=deg R, |P(t)|≤1 on [0,1], and P'(0)=sum_j(R(e_j)−1)≤−b. Classical Markov on [0,1] gives |P'(0)|≤2m². Hence b≤2m²≤8D². This derivation does not import a discrete/continuous interpolation assumption or an unspecified asymptotic constant.

The union of the M_j has at most 8D² deg(q)≤8d³ coordinates and hits every maximum-degree monomial. Querying that union reduces deg(q), unless q becomes zero. The other degree cannot increase. On every nonterminal branch, the degree sum starts at most 2d and drops at least once per stage. At most 2d stages, each costing at most 8d³ distinct free coordinates, prove T≤16d⁴. The zero-polynomial tests precede any use of its degree, so no undefined degree convention is hidden here.

This proof applies for every finite n, including n<d and branches that exhaust all free variables. There is no coefficient-size, integrality, positivity, numerical-computability, or dimensional constant assumption. The coordinate change from {0,1} to {-1,1} preserves multilinearity, degree, and deterministic query depth.

## 3. Adversarial audit of adaptivity and covariance

The central potential failure was multiplying unconditional coordinate variation by adaptive revealment without proving the relevant independence. The frozen candidate supplies the necessary argument correctly.

Let the tree run exclusively on an input X, and take an independent input Y. After each query, overwrite the queried coordinate in a separate hybrid vector by the corresponding Y-coordinate. The tree must continue to read the original X; the candidate expressly says that it does. Coordinates are never queried twice on a branch.

For a fixed complete transcript, the event of following that transcript is exactly the cylinder fixing the queried X-coordinates. It imposes no condition on any unqueried coordinate. The final hybrid uses independent Y-signs on queried coordinates and independent, unrestricted X-signs elsewhere. Conditional on that transcript its distribution is therefore the original uniform product distribution. In particular, the final hybrid is independent of the leaf output. This justifies the covariance-to-telescoping identity, including variable stopping times.

For a fixed pre-query transcript, the next coordinate i has already been determined but its X-value has not been seen. Every previously queried coordinate in the current hybrid has been replaced by a Y-coordinate. All other hybrid coordinates remain unrestricted X-coordinates. The current hybrid is conditionally uniform. Because i has not previously been queried, Y_i is a fresh independent uniform sign. The two consecutive hybrids consequently have precisely the unconditional law of one coordinate being independently resampled. This statement holds separately at each node, before summing the transcript probabilities; it does not assert a false unconditional independence between the original input and its adaptive query event.

Writing h for the {0,1}-valued output, centering at 1/2 gives |h−1/2|=1/2. The absolute telescoping sum therefore proves

    |Cov(h,u)| ≤ (1/2) sum_i r_i E|u(X)−u(X with i resampled)|

for every real function u on the finite cube. Monotonicity and boundedness of u are unnecessary. Summing query probabilities gives sum_i r_i=E[length]≤T. All interchanges are finite sums.

The factor 1/2 is correct and sharp for this formulation: on one fair bit, take both h and u to be the bit indicator. Their covariance is 1/4, and the resampling absolute difference is 1/2. Replacing 1/2 by 1/4 would fail. This case is a negative control in the independent exact checks.

## 4. Audit of Fourier normalization and the square estimate

With ||a||_2=1 and rho=RelInf_i(a), Parseval gives squared differences 4rho under a forced sign flip and squared sums 4(1−rho). The constant coefficient contributes to the latter quantity and to the total norm, as required by the problem. The proof has not substituted variance for squared norm.

Independent resampling flips a fair sign with probability 1/2. The candidate first uses that exact identity, then factors the difference of squares and applies Cauchy–Schwarz. It obtains

    E|a(X)^2−a(X with i resampled)^2| ≤ 2 sqrt(rho(1−rho)) ≤ 2 sqrt(rho).

This order matters: a direct Cauchy–Schwarz estimate on the resampled pair alone yields a weaker intermediate constant. The frozen proof does not make that mistake. Equivalently, writing a=A+x_i B gives the exact first expression 2E|AB|. Real coefficients of either sign are permitted. Normalizing by ||a||_2² is valid because a is nonzero.

A nonzero constant has every relative influence zero and full support, so it intersects every nonzero polynomial's support. Thus constants are neither silently excluded nor a counterexample. The zero polynomial is excluded expressly, avoiding an undefined normalization.

## 5. Closing the quantifiers and constants

Under the contradictory disjoint-support hypothesis, put u=f²/||f||² and v=g²/||g||². Both expectations equal one. The total separator has hu=u and hv=0, including at common zeros, where both densities vanish. If mu=Eh, the two covariances are 1−mu and −mu. Their absolute values sum to exactly one. This step does not require the two supports to cover the cube.

Apply the same tree's revealments to both densities. If delta is the maximum coordinate relative influence of either polynomial, the previous two estimates give

    1 ≤ 2T sqrt(delta) ≤ 32d⁴ sqrt(delta).

Hence disjoint supports force delta≥1/(1024d⁸). The candidate's inclusive sufficient threshold delta≤1/(4096d⁸) makes the last upper bound at most 1/2 and is strictly contradictory. There is no boundary-equality issue. The constants are absolute, uniform in n and all real coefficient choices. This is exactly the requested inverse-polynomial sufficient threshold, rather than an exponential bound or a necessary restriction derived from examples.

## 6. Supplemental exact checks and limitations

The independent check program enumerated every structural read-once Boolean decision tree on one, two, and three coordinates: respectively 6, 74, and 16,430 trees, including redundant branches and early stopping. For every tree it tested the covariance inequality against every Boolean indicator function on that cube. It also exhaustively repeated the three-coordinate test under the nonuniform product probabilities (1/4,1/3,2/3), a stress test of the product-law argument. Altogether 8,413,368 exact integer inequalities passed, with no floating-point tolerance.

An asymmetric adaptive tree was separately checked by enumerating all 64 input/resampling-input pairs. Both the terminal transcript-conditioned uniformity and the pre-query resampling-pair distribution matched exactly. All real functions taking values in {-2,-1,0,1,2} on cubes of dimensions one and two were checked for the square-influence estimate, excluding only the zero function: 1,272 coordinate inequalities passed. Tests passed in normal and optimized Python execution; the checks use explicit errors, not removable assertions.

These finite checks are diagnostic evidence, not a proof of the all-dimensional result. The accepted universal proof is the mathematical reconstruction above and in the frozen candidate. File-integrity and negative mutation controls likewise certify consistency of the checked packet, not truth of a theorem.

## 7. Scope, credit, and disposition

The 2026 disjoint-support separator is essential prior work and must receive prominent credit. The Markov/Bernoulli argument is also credited to its primary mathematical source. This audit makes no novelty claim for the covariance conversion or the resulting corollary. It does not infer the exact conclusion merely from a quantum key-agreement impossibility theorem.

The earlier [CRYPTO 2022 paper](https://doi.org/10.1007/978-3-031-15979-4_6) formulates a distribution version of polynomial compatibility. No general distribution theorem, other underlying group, or approximate-support statement is accepted by this audit. Those are outside the stated target, regardless of possible further deductions.

The candidate's warning about the old exponential endpoint is independently correct: at d=1 the polynomials 1+x and 1−x have disjoint supports and relative influence exactly 1/2. Thus the non-strict exponential endpoint printed in the OWR summary is false at that boundary. The 2022 text uses a strict hypothesis. This issue does not affect the new sufficient threshold.

Final disposition: ACCEPT_EXACT_TWO_POLYNOMIAL_SOURCE_CREDITED_COROLLARY. No mathematical correction is required for the accepted original proof. The distributed proof differs only in its explicit status and finite-check framing.
