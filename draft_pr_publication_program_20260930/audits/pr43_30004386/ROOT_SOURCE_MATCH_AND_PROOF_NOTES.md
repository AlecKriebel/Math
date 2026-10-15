# ROOT source match and proof notes: PR43 / OWR-17469-011

ROOT read the complete original16 package, including SOURCE_STATUS, source audit,
old review, both exact checker sources, complete saved receipts and empty turn
ledger. ROOT also read all12 pages of arXiv2103.16430v2, and directly inspected
the original report's rendered pp411–413. The publisher's current record confirms
Studia Mathematica264(2022),103–119, DOI10.4064/sm210413-16-9, online17December2021.
The downloaded full proof is the author manuscript, rather than the journal PDF.
The surrounding40-page workshop report and cited foundational texts have not
been read in full. This is a source-match audit; credit remains with Johnston,
Kabluchko and Prochno. It is not a paper, new discovery or novelty certificate.

The literal target has two parts: the laws of random probability measures
mu_Theta on the real line, where Theta is Haar-uniform on S^(N-1), satisfy a full
LDP in the weak topology at speedN; the possible Prohorov limits of laws of
sum(alpha_i U_i) for unit vectors are the entire stated closed-unit-ball family.
Here U_i are independent Uniform[-1,1]. The parameter law kappa_a has uniform
series plus independent Gaussian variance(1-||a||²)/3. TheoremA matches the
first claim exactly. Proposition3.1 and the all-N approximation match the second.
Probability is over directions; these statements concern fixed projection
dimension1. Marginal LDPs do not require independence of directions acrossN.

ROOT reconstructed the proof mechanisms rather than treating theorem labels or
finite computations as proof. Ordered absolute square-summable coefficients
form a compact product-topology spaceW: monotonicity and all finite partial
squared-norm bounds are closed conditions in[0,1]^N. Signed permutations
preserve the law by uniform symmetry and unconditional L2 convergence. The
series converges almost surely by the independent finite-variance convergence
criterion. Every resulting law has variance1/3.

For fixedt, ordered coefficients satisfy a_(L+1)²<=1/(L+1). The logarithmic
tail expansion log(sinc(x))=-x²/6+O(x⁴), on a fixed small real interval, gives a
uniform remainder bounded by C_t/(L+1). Adding the missing-mass Gaussian
cancels the full squared norm, leaving the quadratic tail determined by the
firstL coordinates. The finite sinc prefix converges coordinatewise. Multiplying
prefix by tail, rather than dividing full characteristic functions, proves
continuity also at characteristic-function zeros. Levy's continuity theorem
then gives weak continuity. The product is entire; its tail converges uniformly
on complex compact sets and has no additional zeros. Its smallest positive zero
recovers pi/a_1; analytic cancellation repeats this argument, with an explicitly
zero-free Gaussian ending when all remaining coefficients vanish. Thus the
canonical representation is unique. Compactness gives the inverse continuity.

The finite sphere density of the firstell coordinates has exponent
(N-ell-2)/2 and gamma ratio Gamma(N/2)/(pi^(ell/2)Gamma((N-ell)/2)). Its
logarithm divided byN has exponent limit(1/2)log(1-||x||²) in the open ball.
The prefactor has logarithmic growthO(logN) for fixedell. For a local lower
bound, integrate a strictly ordered positive wedge of radius1/N nearx. Ties
still leave volume at least C_ell N^(-ell). The remaining normalized sphere
coordinates have maximum tending to zero in probability, uniformly using its
radius<=1, so they stay below a fixed positive last prefix coordinate with
probability at least1/2 for largeN. This proves the interior prefix lower rate.
When the last coordinate is zero, approximate the prefix by arbitrarily close
positive ordered prefixes within the neighborhood and open ball, then let the
perturbation vanish. This retains the original rate, rather than choosing a
single unrelated positive center.

For an upper bound, sum over ordered distinct coordinate assignments and signs:
the valid factor is2^ell(N)_ell, bounded by2^ell N^ell. It is subexponential for
fixedell. On an r-neighborhood ofx, norm>=||x||-r. The density upper rate is
(1/2)log(1-(||x||-r)²). First let r decrease to zero, then letell increase.
Finite prefix squared norms increase to the full norm, yielding the local rate
J(a)=-(1/2)log(1-||a||²), with infinity at norm1. The zero parameter has rate0.
Standard local-LDP-to-weak-LDP theory applies to the product-topology base;
W compact makes every closed-set upper bound a compact-set upper bound and
also makes exponential tightness automatic. J is lower semicontinuous and its
finite level sets are closed subsets ofW, hence compact. Continuous transport
to the compact closed imageK gives the full measure-valued LDP on P(R), with
infinite rate outsideK and, by uniqueness, at its norm-one boundary.

The limit-set necessity follows because each finite unit-vector law is inK,
which is closed. For sufficiency, retain m_N=floor(sqrtN) coefficients and fill
the other N-m_N positions by c_N with c_N²=(1-prefixmass)/(N-m_N).
The vector has norm1 and c_N->0. Its ordered jth coefficient satisfies
a_j<=b_j^(N)<=max(a_j,c_N) once j<=m_N, including zeros and ties. Hence
every coordinate converges and the laws converge to kappa_a. Equivalently, the
retained series converges inL2 and the independent filler sum's fourth-power
remainder is bounded by1/(N-m_N), giving precisely the missing Gaussian.
This works for every sufficiently largeN and includes norm-one laws, even
though those laws have infinite rate. No norm-topology compactness is assumed.

ROOT recorded the following printed-source qualifications. They do not alter
TheoremA's target or the corrected proof mechanisms above:

- The manuscript's variance-one sentence after(2) conflicts with its formula;
  variance is1/3.
- The displayed full-characteristic-function ratio in Lemma3.3 is undefined at
  zeros. The preceding uniform tail estimate and direct prefix multiplication
  supply continuity there.
- The sorted-coordinate upper union bound printed with2^ell binom(N,ell)
  omits the ell! ordered-assignment factor. Use2^ell(N)_ell; its logarithm/N
  still vanishes, so the limiting rate is unchanged.
- Proposition2.2's unrestricted converse 'fullLDP implies exponential
  tightness' is too broad without further conditions. A fixed full-support
  Gaussian law for everyN satisfies a full LDP at speedN with I identically0
  onR, while no compact set has exponentially decaying outside probability.
  That converse is unused here: W is compact and the required implication or
  simply the compact-space closed-set argument suffices.
- The original workshop report's p412 heuristic density exponent and its
  normalized log-density display contain printed errors. The actual target
  Conjecture1 and Lemma1 on p413 have the correct normalization and rate.

ROOT's genuine unchanged private helper runs produced527 current-author,
527 historical-author and664 old-independent exact checks. Historical source
bytes were obtained from the original Git commit, not guessed: only one review
status sentence distinguishes that source from the final SOURCE_STATUS.
The historical author and independent saved receipts reproduce byte for byte;
the current author receipt differs only by the source-status SHA field.
These controls verify their finite diagnostic statements, not an LDP.
The full149266659-byte raw datasets and15458-row read-only SQLite importer
comparison pass. The prior raw key OWR-17469-011 is absent;{} is its SQL
fallback. The original SOURCE_AUDIT's 'entry is null' therefore requires a
precision correction in current presentation, while its exact original body
must remain archived. Current model/reasoning/deadline are unknown/null; old
claimed runtime and review status are attributed history, not present authority.

Scientific/source match is provisionally accepted as ALREADY_SOLVED_IN_PRIOR
PUBLISHED_LITERATURE, with no project full-resolution or novelty assertion.
Independent new family comparison, current package and final acceptance remain
pending. Original substantive turns0/5; new0; audit0. No paper, new DOI,
release or tracker row is warranted under the user's process.
