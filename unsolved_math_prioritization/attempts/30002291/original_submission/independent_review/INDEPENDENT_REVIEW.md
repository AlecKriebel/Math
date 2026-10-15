# Independent analytic review: 30002291

**Verdict: PASS_COMPLETE_SUFFICIENT_CONDITIONS_SOURCE_TARGET.** No mandatory mathematical correction found. This verdict binds the exact frozen PROOF.md SHA-256 `508f71b81ee669d4934ef1cc9e061c129e47d36359896ad7b3e20574dbfbc539` and FROZEN_MANIFEST.json SHA-256 `55cb55f0c3417be54739796e90b6b1f6161c820ac78389ce04ac522ff8cecf53`.

The theorem answers the source's open-ended request for sufficient hypotheses with a broad, explicit class. The accepted statement is joint fixed-time stable convergence for the stated bounded-characteristic, absolutely-continuous-compensator class and exponentially controlled kernel/derivative. It does not claim all-semimartingale or functional convergence, maximal hypotheses, or novelty. The separate SOURCE_REVIEW.md records the exact source wording and prior-result attribution.

The reviewer did not contribute to the author's proof search. This audit independently checked the analytic proof, full primary preprints and official source page, replayed the author controls and constructed separate controls. The author theorem and frozen files were not edited.

## 1. Existence and deterministic kernel estimates

The hypothesis integral z^2 nu_s(dz)<=K makes the compensated all-jump martingale square-integrable on every bounded interval. Large-jump first moments are finite by |z|<=z^2/epsilon on |z|>epsilon. There is no hidden Brownian part. The driver is used through bounded-interval increments; no unjustified integral of the raw driver over the entire past is required.

For g=x_+^alpha f, the derivative is alpha*x^(alpha-1)f+x^alpha f'. The two exponential bounds give a global multiple of x^(alpha-1). They imply g in L1 and L2 and g' in L1. Near zero, the weighted derivative energy is x*|g'|^2=O(x^(2alpha-1)), integrable because alpha>0. These properties validate the drift and L2 stochastic convolutions from minus infinity.

The discrete impulse bound separates the first two increments from a tail dominated by the summable sequence (l-2)^(2alpha-2). It is uniform in the phase, the impulse time and the horizon. The single-impulse limit follows by first fixing the number of retained increments, using uniform continuity of f near0, then removing the tail. The fixed observation horizon contains any fixed retained block eventually. This argument works for every deterministic mesh sequence tending to zero.

The phase series is continuous on the torus: its uniform convergence is valid, and the endpoint equality follows by reindexing. A finite list of distinct impulse times has disjoint short right-neighborhoods. The normalized squared norm outside each neighborhood tends to zero, so the normalized cross inner products vanish by Cauchy-Schwarz. No assumption about random jump signs is needed.

## 2. The prehistory singularity and stochastic Fubini

The crucial change-of-variables identity is

    integral_(u=0)^T integral_(s<0) |g'(u-s)|^2 ds du
      = integral_(x=0)^infinity min(x,T)|g'(x)|^2 dx.

The right side is finite under the proved bounds. With the quadratic-rate bound, this is precisely the L2(Omega x [0,T]) bound for the candidate derivative D. Stochastic Fubini can also be obtained directly by approximating g'(u-s) with simple kernels in this Hilbert norm: integration in u is a bounded map to L2(Omega), and stochastic integration is a bounded isometry map. Thus the two orders of integration commute in the limit. The resulting random derivative is in L2 time almost surely, and its integral is an absolutely continuous version of the past increments. No value or finite derivative at u=0 is required.

For any such absolutely continuous path, the mesh sum is bounded by Delta times its derivative energy. After normalization this is Delta^(1-2alpha) times that energy, which vanishes. The future convolution of a bounded measurable drift has bounded derivative since g(0)=0 and g' is integrable. This also applies to the epsilon-dependent compensation drift, for each fixed epsilon. The order of limits is important and is respected.

## 3. General predictable jump-time laws

I specifically checked the passage from a bounded predictable intensity to the joint density of every finite truncated jump-time vector. Nonatomic individual marginals alone would be insufficient. Here the stronger argument works.

For m ordered distinct truncated jumps, compensate the last point in the ordered sum. The sum over earlier jump tuples, multiplied by a deterministic Borel function of those times and the candidate last time, is predictable (first check rectangular functions, then a monotone class). Bound the last conditional intensity by L=K/epsilon^2, interchange the remaining nonnegative integrations, and repeat. This gives domination of the ordered factorial measure by L^m times Lebesgue measure on the simplex.

On the event N_T=m, the sole full chronologically ordered tuple is one of the tuples counted in that factorial measure. Its law is therefore absolutely continuous. Multiplication by any bounded variable measurable with respect to the entire original sigma field preserves absolute continuity and produces an L1 signed density. This last fact, rather than independence of future information, is what permits stable convergence relative to that sigma field.

For a nonzero Fourier mode q, the phase integral is the Fourier transform of that weighted L1 density at q/Delta, and vanishes by Riemann-Lebesgue. Torus trigonometric approximation proves independent uniform limiting phases. Additional random marks are included through bounded measurable weights, followed by product-test approximation on compact mark sets and tightness. The finite random number of jumps is handled by the expected-count bound. Thus dependence of jump sizes and intensities on the path does not invalidate the phase argument.

## 4. Small jumps and stable convergence together

For fixed epsilon, the raw large-jump sum, compensated small-jump martingale and compensation-adjusted drift form the exact driver decomposition. The drift bound B+K/epsilon is valid even for asymmetric kernels. The finite impulse argument and the phase argument give the truncated joint stable limit; jumps at deterministic observation horizons have probability zero.

The martingale isometry applies to the predictable small-jump integrands. With an absolutely continuous compensator there is no predictable-time atomic correction to the bracket. Summing the isometry and using the deterministic discrete-energy bound gives a normalized expected residual variation bounded by

    C * E integral_0^T integral_(|z|<=epsilon) z^2 nu_s(dz) ds.

This tends to zero by dominated convergence, uniformly in the mesh, including when the jump index is2. It uses no independence of increments or symmetry. The reverse Euclidean norm inequality gives the square-root-statistic comparison without demanding a fourth moment or separately bounding cross terms against the large-jump part.

All limits can be realized with one independent uniform per original jump. The total squared jump mass has expectation at most KT, so the coupled limit sums are finite and their omitted tails vanish almost surely. Testing the square-root vectors against bounded original-sigma-field variables and bounded Lipschitz functions proves stable convergence together. Continuous squaring then gives the claimed vector limit. This closes, rather than assumes, the removal of truncation.

## 5. Source scope and boundary challenges

The exact source requests sufficient conditions, with no defined maximal class. The stated class is genuinely general: for example, add a non-Poisson count with bounded history-dependent birth intensity to an independent square-integrable infinite-activity Lévy noise of index2. Its compensator is a history-dependent mixture, still satisfying the theorem. Such examples prevent the answer from collapsing to the original compound-Poisson model or solely to a scalar multiple of a fixed Lévy noise.

The deterministic-time counterexample is correctly outside the assumptions. For alpha=1/4 the phase function has W(0)>=1 and W(1/2)<=5/(4 sqrt(2))<1. Choosing meshes hitting the deterministic jump cannot give the fresh uniform phase law. This is a valid limitation on an unqualified statement, not a counterexample to the source request or the theorem.

The source concerns fixed-time stable convergence. The 2018 theorem already provides M1 convergence for its own Lévy-volatility model, and explicitly discusses failure of J1/J2. The candidate's finite-dimensional claim does not silently import a functional theorem. The prior phase conventions agree after U becomes1-U. The two prior papers' symmetry and activity restrictions are retained when describing their theorems; none are prerequisites of this standalone bounded-rate proof.

## 6. Verification, access and publication boundary

All nine frozen author artifacts and all three pinned primary PDF hashes match. The author checker reproduces its 2,571-control output byte-for-byte. The 227 independent exact controls check a non-Poisson two-jump joint density and phase Fourier decay, the prehistory weight identity, exact exponent conditions, phase reindexing and the index2 small-jump variance. Their finite results are supplementary; they are not presented as proofs of stable convergence or stochastic Fubini.

The primary OWR page was visually inspected. Complete primary preprints were used for the detailed 2017/2018 theorem audit; official journal materials and the author's publication list verified metadata. The unavailable final Euclid full article is an access limit, not concealed. The proof under review is self-contained apart from standard martingale integration, Fourier and weak-convergence tools.

No mathematical revision is required for this exact version. Publication should retain the full sufficient assumptions, prior theorem credit, one completed author turn, and no novelty or all-driver claim. Only the portable files listed in REVIEW_MANIFEST.json belong in the public review packet; source PDFs, full texts and rendered pages remain reading copies.
