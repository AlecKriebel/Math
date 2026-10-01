# Independent full analytic review: 30006395

**Verdict: PASS_SCOPED_PARTIALS_ORIGINAL_UNSOLVED_5_OF_5.** No mandatory correction found. The exact author manifest is SHA-256 `556243a7e7470afc1538a05def7256c072a87107001c932b507bb7de95342300`; RESULT.md is `7c77de864788348e9dcaf5246fc8b41afdbbb20e64b793ea7fc0040133f5ca26`, and TURN_5.md is `499e0e122a81f2a9db8e89c1123e8f89fcb60b8b5413a8e853cdec66bfb5e5cf`.

All five written derivations were reviewed, not just their receipts. The reviewer did not contribute to the author's proof search. The accepted claims concern the unknown uniform labelled-Cayley-tree mixture, with fixed mean degree except in the explicitly parameterized critical L2 window. The original mean-degree transition remains unsolved. No novelty, revealed-template lower bound, fixed-constant logarithm-squared detector, logarithmic-size detector, or polynomial-time implementation is certified.

## 1. Exact likelihood and forest expansion

The likelihood is the uniform average of forced-edge indicators divided by p^(k-1). Tree counts permit extra graph edges; they are not induced-tree counts. The weighted Prüfer contraction gives the containment probability product(s_j)/k^m, including the one-component spanning-tree case. Uniform embedding contributes (k)_v/(n)_v. Squaring this probability in the common-edge expansion and counting each unordered forest exactly gives the author's component weights, r! and falling factorials.

I checked the finite-population bound before any factorization: for 2k<=n, its logarithm is at most -v(v-1)/(2k). Allocating this Gaussian bound among components and enlarging a nonnegative index set are legitimate. This yields a convergent component series at c>e. Stirling and the Gaussian cutoff yield k^(9/4)/n at c=e with the stated constants. Bounded second moment implies one-sided contiguity and rules out strong detection; it is not equated with vanishing total variation unless the moment tends to1.

The separate edge-count detector has a mean shift (k-1)(1-p) and variance O(n); the displayed Chebyshev bound is valid. Thus the high-c square-root scale is established for this mixture. Its attribution to the standard connected-plant/edge-count method is appropriate.

## 2. The first actual unknown-tree detector

For two fixed labels in a uniform Cayley tree, each specified connecting path is unique if present. Counting its possible intermediate labels proves the exact distance distribution. Conditioning on the full path is equivalent to conditioning on its containment. After contraction, weighted Prüfer letters and independent uniform attachment endpoints give precisely the Bernoulli-plus-binomial boundary law for a strict prefix. The Hamiltonian-path exception is separately handled.

The conditions k/log^2(n)->infinity and ell=O(log n) imply that the selected path has enough interior vertices and its length is o(k), with the required high probability. The prefix boundary binomial has asymptotic mean ell. The null Chernoff exponent is conditioned only on the path edges; boundary edges remain independent. Under the alternative the prefix was selected using the tree alone, so the unforced background boundary edges retain their independent binomial law. The lower mean bound is uniform even for large k. This proves the stated strict criterion and does not imply a result at every fixed multiple of log^2(n).

The density-increase channel preserves forced edges and transforms each unforced Bernoulli law correctly. Its use for monotonicity does not reveal the hidden tree.

## 3. Critical second-moment limit and its uniformity

The coefficient recurrence is an exact exponential-formula identity. At s_j=x_j sqrt(k), the exact finite-population factor tends to exp(-(sum x_j)^2); its remainder is O(v^3/k^2+v^2/n), uniformly on positive compact sets. The component factor has the k^(-1/2) Riemann-sum normalization and coefficient lambda*e/sqrt(2pi). I checked that no extra power of k, e, component factorial or Dirichlet factor is lost.

The proof supplies the needed two uniformities. Near x=0 the scaled x^(-1/2) sums are O(sqrt(epsilon)); at large x the same sums have an integrable Gaussian envelope. For each fixed number of components this permits compact truncation and Riemann convergence. The total component-majorant mass is uniformly bounded, giving a B^r/r! bound for the component-count tail. It is therefore valid to interchange both limits and the infinite series. The lambda=0 case follows separately from the uniform bound, without using a singular positive-lambda asymptotic.

The Dirichlet/Gamma reduction and four-step coefficient recurrence agree. Keeping component sizes between sqrt(k) and2sqrt(k) yields the stated lower bound proportional to k^(9/4)/n. This matches the L2 convergence scale only. The manuscript correctly refuses to infer weak detection from a nontrivial or divergent second moment; bounded moments alone do not give uniform integrability of their squares.

## 4. Fixed high-c likelihood law

The Bernoulli edge basis is orthonormal, and a Fourier coefficient vanishes for a cyclic edge set. The coefficient for each forest is exactly its containment probability times the appropriate standardized forced-edge factor. The connected-tree normalization (n)_h/aut(H) and ordered disjoint-copy convention agree with the forest multiplicity factorial.

The sparse diagram exponent v-e-r/2 is correct. A nonzero pattern has no singly occurring edge; each connected union component then contains at least two tree occurrences. The bound v-e<=u<=r/2 leaves equality only for a forest union of disjoint identical-copy pairs. All other fixed patterns vanish. This proves the joint Gaussian moments of fixed connected-tree types. Normal moment determinacy is sufficient here.

For the disjoint-copy variables, pairings within one such factor are forbidden. The surviving pairings are exactly those of Wick/Hermite products. Expanding the three terms in the claimed squared L2 difference requires only finitely many of the proved mixed moments. No moment-determinacy assertion for a polynomial of Gaussians is needed.

The final likelihood limit requires more than that lemma, and the manuscript supplies it: choosing1<z<c/e gives an exponentially small total-support tail, uniformly in n when k^2/n is bounded. This transfers the finite-forest limits to the whole likelihood. The limiting Hermite series has squared norm exp(sigma^2), so its infinite Gaussian sum and exponential are legitimate L2 limits. The same uniform forest tail also justifies the stated second-moment limit.

Uniform L2 boundedness gives uniform integrability of |L_n-1|, allowing the total-variation limit. The likelihood limit is positive almost surely, which supplies the reverse contiguity direction by the epsilon cutoff argument. The lognormal tilt yields the two equal limiting testing errors. A fixed-degree likelihood approximation can approximate the risk because excess classification loss is bounded by its L1 error. None of these steps extends uniformly to c=e: the generating-function radius and the variance sum both obstruct that transfer.

## 5. Finite-depth branching likelihood and actual selected roots

Superposing Poisson(c) noise-child intensity with the Poisson(1) signal-child intensity gives the exact untyped likelihood recursion. Campbell's formula yields the stated entropy recursion and Poisson generating functions yield m_(d+1)=exp(m_d/c). For fixed depth, log likelihood is bounded below and its positive part is bounded by a constant times the explored vertex count. Finite-depth branching counts have the required finite moments, so the later product laws of large numbers are justified.

The important finite-tree bridge was checked independently. The specified full path plus the exposed rooted forest is a connected tree H of V vertices. All its internal vertices have their allowed off-path neighbors completely specified. Exactly b=V-I vertices remain available as endpoints for edges from H to outside vertices. Contracting H therefore gives the extension count b(k-I)^(k-V-1). A matrix-tree determinant gives the same count independently of Prüfer coding. The full-tree case has one extension and must not be evaluated as a formal zero/zero expression.

Dividing the exact selected-root probability by independent Poisson(1) forest probabilities leaves the ratio displayed by the author. On total size at most Mr, its logarithm is uniformly O_M(rD/k+r^2/k+r/D). The chosen random-path distance interval makes all three errors vanish. The reference forest's law of large numbers gives mass1-o(1) on that size cap, and uniform likelihood ratio there transfers the cap probability and total variation; individual neighborhoods need not have uniformly bounded size.

Deleting both witness-prefix endpoints and ignoring every root-root edge removes the two spine continuations as well as its interior path edges. The off-path signal forest cannot reconnect distinct roots without creating a cycle. These details are necessary for the branching comparison and are present.

## 6. Alternative coupling and multiplicative null exploration

On the alternative side, stopping after O(r) vertices permits sequential independent Bernoulli exposure. The errors are O(rk/n+r^2/n), including background hits into other planted vertices. With k<=n/log^2(n) and r=O(log n), they vanish. The reference product branching law has total size O(r) with probability1-o(1) for a fixed sufficiently large cap, so the stopping rule can be removed. Larger k fall into the separately proved edge-count regime. This is a valid split and does not assume the hidden template is observed.

The null side correctly avoids multiplying an additive coupling error by the path count. There are I*m-I(I+1)/2 unordered pairs incident to internal vertices. Removing all binom(r,2) root-root pairs and the j present forest edges gives exactly the author's absent-edge exponent. Depth-d frontier pairs are unqueried. The label/automorphism factor is correct for roots held fixed. On the size cap, the exact ratio to the Q_d product law is exp(O(r^2/n)), a uniform multiplicative bound even on a rare score event.

The score likelihood has null mean1 after exponentiation, so Markov plus this multiplicative bound and the expected path count gives vanishing null error. Under the alternative, the product-law score mean is D_d and the finite first moment gives the required law of large numbers. Thus the criterion D_d(c)>log c applies to the actual unknown-tree experiment, with k much larger than log^2(n).

The c=3/2 certificate was independently recomputed using a different rational Taylor order and direct atanh bounds without the author's logarithm range reduction. It proves the strict entropy gap from ten nonnegative terms. The scalar second-moment recursion, entropy data processing and Jensen bound at c>=e have the stated direction. Divergence of the recursion below e is not used to assert an entropy or information transition.

## 7. Verification and disposition

All27 manifest-bound author artifacts and all three pinned primary PDFs match. All five checker outputs reproduce byte-for-byte. The 3,152 independent exact controls use Laplacian determinants rather than planted-tree enumeration for likelihoods, Kirchhoff determinants for constrained extension counts, direct queried-edge recounts, critical exponent identities, and a separate rational entropy certificate. The receipts are supplemental: the analytic uniformity and testing conclusions were reviewed above rather than inferred from finite samples.

The primary source page was read visually and in text, and both complete prior papers were checked in their relevant hypotheses. SOURCE_REVIEW.md records the resulting scope. No frozen author mathematical file was changed. The original threshold transition remains **unsolved5/5**; all accepted results are scoped partials. Only the files listed in REVIEW_MANIFEST.json are portable review artifacts.
