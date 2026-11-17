# Root substantive review: hypersingular Riesz constants on surfaces

Record 23202994, inventory row 190. Review completed 2026-11-17 UTC.
Disposition: **PASS for the exact published claims as an attributed consequence.**
Best estimate: 100% completion of this bounded manuscript review. This is not
a probability of correctness, formal certification, human refereeing, or
completion of publication or of the full inventory. Follow-up: null.

The controlling manuscript is the five-page outer Zenodo `paper.pdf`, 87,127
bytes, SHA256 `b9e7c887787b911b55f012cc640621fedc282dd71e8c57fa01c1f9db49612d9d`.
Its corresponding 333-line publication/main.tex was read completely, with
all five freshly extracted PDF text pages and all five individual rendered
pages, before supporting opinions or primary proofs were opened. The full
native API Description was also read. These first findings remain in the
separate immutable root INITIAL (seal SHA256
`8f9ade99c086123c71295abde3bfc96e75dc216768efc5688715f975d89d98fa`).
All three original-first INITIALs were committed in checkpoint
`6dbbc98d2adf0a24ff1b824f4404daed399169cb` before continuations opened.
Original author assertions were visible in the original and were treated as
unverified assertions; this is source-first review, not zero prior exposure.

The DOI is 10.5281/zenodo.23202994; native API version 1.0.0 and declared
publication date 2026-10-06. Record creation was 2026-10-07T04:37:01.947972Z;
updated time 2026-10-10T21:28:03.598305Z. Neither changes the declared date.
Native listed order is paper.pdf then source-and-verification.zip. The source
closure has 39 files and 15 child directories; no embedded PDF supersedes
the outer manuscript. Owned text, source, code, notes and results use the
native CC BY 4.0 statement. Third-party works retain their own rights; no
invented MIT or Apache exception is supplied for this deposit.

## Exact claim, assumptions and success criteria

Fix a real s>2, b=sqrt(3)/2 and the covolume-one triangular lattice
Lambda=b^(-1/2){(j+k/2,kb):j,k in Z}. Put
Z_s=sum_{v in Lambda, v!=0}|v|^(-s). All energies count ordered pairs,
assign infinity to collisions, and use ambient Euclidean distance.

The asserted square limit is

    lim_{N->infinity} N^(-1-s/2) E_s([0,1]^2,N) = Z_s.

For each fixed smooth compact embedded two-dimensional surface M of
positive ordinary area A, including smooth boundary, the asserted leading
minimum is Z_s A^(-s/2) N^(1+s/2). The unit sphere coefficient is
Z_s/(4pi)^(s/2), for chordal distance. There is no uniqueness, microscopic
crystallization, second term, critical-s, other-dimensional, intrinsic
distance, or joint uniform parameter assertion.

The target requires an actual proof of the imported triangular energy
bound, not merely a favorable theorem heading, agreement among author
audits, a finite fit, or a formal-source manifest. Only its square-periodic
specialization is needed. Correct scaling, periodic averaging, order of
limits, the exact-N upper construction and the corrected compact-surface
interface must then hold. An unsupported imported central theorem would
block the unconditional target rather than become a new assumption on a
promotional page.

## Independent root reconstruction

The determinant of the displayed lattice basis is one. Its inverse-power
series converges by a constant multiple of sum m^(1-s). The potential on
squared distances is g(t)=t^(-s/2), with
(-1)^r g^(r)(t)=(s/2)_r t^(-s/2-r)>0 on t>0. Thus the actual completely
monotone source class includes exactly this singular kernel.

For q distinct motif points in [0,L)^2, each full outgoing row is finite:
translations of sup norm m>=2 have distances at least Lm/2 and multiplicity
8m. Centered cells give n_i(R)=pi R^2/L^2+O(R). Completing rows gives the
upper disk bound, while retaining fixed-length interactions from B_(R-T)
gives the lower. First R grows at fixed T, then T grows, proving an ordinary
disk limit equal to the average of full motif rows. There is no separation
estimate uniform in the motif or N.

For any distinct closed-square configuration x_i, take y_i=sqrt(N)x_i and
period L=(1+epsilon)sqrt(N). The strict gap prevents identification of
boundary points. Cross-cell terms include i=j for nonzero translations and
satisfy

    I_(N,epsilon) <= 8 epsilon^(-s) zeta_R(s-1) N^(1-s/2).

Compressing lengths by (1+epsilon)^(-1) gives density one and multiplies
per-point energy by (1+epsilon)^s. The imported lower bound therefore yields

    a_N >= (1+epsilon)^(-s) Z_s
           - 8 epsilon^(-s) zeta_R(s-1) N^(1-s/2).

The order is disk radius first at each fixed N,epsilon, then N at fixed
epsilon, then epsilon down to zero. The error vanishes precisely because
s>2. No zero-gap periodization or interchange of a varying family of disk
limits occurs.

A bounded unit-area fundamental cell inside [-D,D]^2 implies that a crop of
side sqrt(N)+2D contains at least N lattice sites. Select exactly N of them;
each outgoing row is bounded above by Z_s. Scaling into the unit square gives
a_N<=Z_s(1+2D/sqrt(N))^s. This upper bound is unconditional and avoids an
unproved exact crop count. Together the two bounds prove the square limit
once the imported energy theorem is justified.

## Actual imported analytic proof checked

All primary sources use immutable OpenAI/math commit
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`. Twenty-six main/atomic source and
verification files plus three PDFs were copied into the root continuation
only after their full byte counts and SHA256 matched recorded pins. No
current peer mathematical report was opened before the root proof reading
and reconstruction described below.

The root read the complete main build/main.tex and Sections 1–7, comprising
the whole needed positive-energy analytic route, and the needed scalar
appendix. Lines 1–510 of the latter were read, including some later
field-approximation material; its complete later field/jellium chain and
conditional floor-matrix route are not needed and are not certified here.
The entire numeric_balls.py and its README were read. The main construction
uses a genuine compact spectral measure, a dimension-two complex Gaussian
transform, and node-uniform total variation to obtain Schwartz convergence
from unweighted l1 coefficients. Fourier involution applies to actual radial
functions; it does not compose an invalid folded complex contour.

The Fejer rule is positive, of total mass one, exact through degree 383.
Cauchy bounds give quadrature error below 10^-31 uniformly in the needed
scaled derivatives. The finite inverse is perturbed to exact integrals;
small distant outputs and a Schur complement invert the full unweighted l1
system despite the much larger full operator norm. Omitted target jets,
quadrature error and the geometric-sum residual are all included. Deleting
values and slopes before quotient estimation, then Bernstein bounds on
containing parameter boxes, controls whole finite gaps. Genuine double
zeros, a second-derivative bound and the periodic sine-product barrier close
the unbounded radial range. The unbounded Gaussian parameter box uses a
fixed left endpoint for its Taylor support. Density-only linear programming
uses a larger background disk and a uniform Schwartz tail, not an occupancy
bound. Positive shifted mixtures use Fatou along every radius sequence;
only the lattice sum loses the positive shift.

The root also read the entire 2,473-line atomic manuscript, its complete
finite-certificate appendix and bibliography, and its entire 389-line
standard-library exact checker. This is an alternative analytic route with
different damping and modulo-36 nodes. Its finite periodic columns repeat
jets at later nodes; the proof includes these own-side terms with the
correct minus sign in both sum and difference tail systems. Uniform
spectral variation controls all rational tail columns. Continuous-frequency
monotonicity, a complete tail period and geometric sums provide full
operator bounds. The Schur inverse acts on the complete l1 space. Individual
correction bounds correctly average the plus/minus bounds.

Atomic sign checks delete exact jets, retain the derivative-order-23 Taylor
tail and use a containing polytope. The exceptional first right half-cell
requires the positive Gaussian rational support and four cubic Bernstein
coefficients. Its endpoint z=0 is a bounding polytope endpoint, never a
physical Gaussian. At the radial junctions, selected nearest nodes keep
each Taylor segment inside the applicable curvature region. The fixed
signed sine-product term dominates the remaining curvature on every later
gap. Positive normalization, the Fourier complement for alpha<1,
covolume-one Poisson summation, a centered-density Fourier cutoff and the
locally finite Laplace/Fatou argument then prove the needed energy bound.
None of these infinite analytic steps is inferred from a finite execution.

The checker encloses real operations on a 10^60 integer grid and complex
operations by rectangles. Reversed zero-excluding reciprocals, integer
square roots for known nonnegative quantities, strict pivot checks, the
bounded exponential remainder and ten squarings preserve enclosure.
Algebraically known elimination entries may be reset to exact zero/one.
Its fixed loops implement all 659 Bernstein row minima and the finite
envelopes and inverse bounds used by the analytic proof.

## Classical surface theorem and attribution

The actual corrected Hardin–Saff math-ph/0311024v3 PDF is 325,401 bytes,
SHA256 d031e7c826b8400440d0681da9c4d4297e56eb8765b1f335b0dd3dd10fd57167.
The root read definition (19), Theorem 2.4, its Section 8 proof and the
complete attached four-page addendum. The root personally inspected the
fresh page-three image to confirm that the deletion argument uses a k above
the LIMSUP energy, which supplies an eventual upper bound. The PDF's
addendum heading November 23, 2018 and its arXiv v3 banner December 15,
2004 are distinct metadata and are not silently equated.

The s>d theorem applies to finite compact pieces of maps bi-Lipschitz on
open parameter neighborhoods, with ambient distances and ordinary area.
A smooth boundary chart extends across the half-plane; on a small convex
ball its derivative stays within half the smallest singular value of its
full-rank derivative at the center. Integration along straight segments
gives both Lipschitz inequalities. Compactness provides finitely many
compact pieces, satisfying exactly the source definition. The extra
without-boundary containment in its s=d clause is not needed for s>2.

The addendum's unrestricted neighborhood wording has a real outside-scope
pitfall: an unbounded neighborhood can contain tiny far-separated balls
of arbitrarily small total extra measure, giving zero finite-energy
infimum. The original note expressly uses only a compact regular thickening.
Finitely many closed parameter cubes inside the open chart domains, and
their bi-Lipschitz image union, give such a compact d-regular thickening.
Finite union preserves two-sided local volume bounds. Neighborhood closures
are compact and have a positive buffer inside a larger relative open set.
The addendum's separation/deletion/movement argument then applies as
written in the consumed compact application. This is an explicit original
qualification, not a repair or silent weakening introduced by this review.

For attribution, the root checked actual KS1998 Conjecture 1 and its
unordered-pair convention; actual BHS2012 Proposition 1 and Conjecture 2;
HSS2014 arXiv v2 Theorem 3.2 and its relevant proof; and HLSS2018 arXiv v2
definitions and Proposition 3.1, together with the published author-copy
footnote drawing the d=8,24 consequence. These establish the known nature
of the finite/periodic passage. The actual BHS printed lattice basis typo
is not imported: the present note explicitly defines the intended
covolume-one lattice. No exhaustive recent-literature or firstness claim
is made. Other results in these classical papers, including their broader
statistical conclusions, are not certified by this limited interface read.

## Independent families, computation and boundary checks

Both independent original-first families were resumed only after the
checkpoint. The root then read the full current scope FINAL, continuation
report, theorem interface, proof checks and reproducibility scope, and the
full adversarial RESULT and derivations. Both independently reconstruct the
central analytic chain and corrected compact application and identify no
material gap in the precise target. Their independence predates root and
peer mathematical findings; procedural path/hash notices are distinguished
from mathematical exposure.

Each family ran one unmodified documented inner atomic route, assertions
enabled, in its own isolated copy. Scope: 3.265237792 seconds, exit 0,
stdout 0 bytes, stderr 0 bytes. Adversarial: 3.228441457991721 seconds,
exit 0, stdout 0 bytes, stderr 0 bytes. Complete input guards match. The
659 count comes from the fully read fixed control flow, not a printed
runtime counter. Root ran zero redundant scientific routes. Neither current
family ran MAIN's 37,310 Bernstein and ten tail comparisons or the entire
outer reproduction runner. Recorded original MAIN successes are historical
evidence, not relabeled fresh runs. The full native outer runner and native
independent scalar/diagnostic code were read; the latter's floating-point
identities are diagnostic, not a universal proof.

N=1 retains nonzero self-image rows. N=2 need not have normalized finite
energy above the limiting constant. At s=2 the series diverges and the
gap error no longer decays. Large fixed s and s down to 2 do not give a
joint uniform rate. Six nearest lattice neighbors give the normalization
check Z_s>=6 b^(s/2). Dilation multiplies both the actual energy and stated
coefficient by the same factor. Close motif pairs are allowed. A fixed
disconnected compact surface has lower-order intercomponent interactions;
the claim does not cover N-dependent shrinking component separation.

Fresh root finite authentication covers 298 files and 53 child directories
across the source, three immutable INITIALs, two complete continuation
packets and the classical acquisition packet. All payload bytes, modes,
hidden/empty entries and topology match their exact externally pinned
controls. FINAL_EVIDENCE_AUTHENTICATION.json records the seven finite
namespaces. One root read-only comparator initially compared reporting
metadata as input state; its literal failure and the precise UTC/phase/
AFTER-only-field reconciliation are preserved in ADVERSARIAL_AUTHENTICATION.
It did not indicate a source change and is not retrospectively called a
successful first comparison.

No compatible Lean/Mathlib build, kernel axiom audit, Comparator run or
follow-on formalization was reproduced or inferred from source scans or
static configurations. The finite checker plus the independently examined
analytic proof is the mathematical validation route used here. The result
remains an unrefereed, extensively AI-assisted preprint and an attributed
consequence of OpenAI and classical reductions. It is suitable for a
carefully qualified research page; this verdict promises neither journal
acceptance nor conventional human peer review.

No follow-up meets the required high bar on the evidence reviewed. The
rough finite-size balancing consequence is routine algebra, and generic
critical exponents, other dimensions or subleading terms are not added as
an unsolicited research program. No outside individual was contacted and
no individual outreach was prepared. Next: record the scientific pass in
the inventory, prepare an accurate private page, then separately stage,
publish and verify it. The canonical spreadsheet cell stays blank until
the live page passes the required checks.
