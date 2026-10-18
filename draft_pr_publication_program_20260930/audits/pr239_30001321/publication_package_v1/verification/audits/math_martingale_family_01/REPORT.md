# Independent adversarial review: martingale and polynomial coarse scale

**Verdict: PASS within the stated scope. No mandatory mathematical issue found.**

I independently audited the authenticated PROOF.md, TURN_2.md and the
required return-kernel/smoothing inputs in TURN_1.md at PR239 HEAD
7f17eef77c52b2d9b2ec3ad0803c016267fa6496. I read no historical independent
review or sibling report. My fresh proof and controls are in DERIVATION.md
and independent_exact_controls.py.

The following points survived adversarial checking:

- The exceptional-site backward hitting recurrence has nonnegative
  coefficients under 0<delta<=a<=1/4. It proves origin maximality and
  supports the conditional overlap bound for arbitrary exposed old laws.
  The Green-function argument includes the necessary monotonic-return
  step to turn an Abelian bound into a pointwise g_t<=C/sqrt(t+1).
- The all-order occupation bound handles repeated time indices by
  conditional time-zero overlap<=1. It assumes neither independent
  overlaps nor an unsupported instantaneous-overlap moment estimate.
- The layer-exposure increment and its conditional quadratic variance
  are correct. The exponential estimate is applied to joint events.
  A shared overlap good event is charged once, outside the exponentially
  many deterministic sign tests.
- All dyadic block endpoints, smoothing times and threshold powers work.
  For d=gamma-1/4>0 the entropy margin is 5d/4 and the boundary-variance
  margin is 3d/4. Fixed gamma is essential and is maintained.
- The periodic boundary test is valid for biased walks, nonintegral
  drift translations, half-open endpoints and arbitrary deterministic
  alignments. A physical residue modulo M reduces to a binomial-index
  residue modulo M/gcd(2,M), giving the uniform bound
  2/M+2 max binomial mass. No parity error or extra ellipticity assumption
  enters.
- The complete TURN_2 argument proves (G), uniformly over all integer
  H>=n^gamma and deterministic alignments, for every fixed gamma>1/4.
  Both its use at H=ceil(N^(5/16)), m=N-floor(N^(3/4)) and PROOF.md's
  separate N^(5/32) small-interval exponent are legitimate.

The final independent exact run passed **197,758 assertions**, exit0
with zero stderr bytes. It imports no candidate code and uses no random
simulation. It checks conditional future integration from arbitrary
rational old laws, moments through order8, full layer conditional
variance formulas, parity residues and translated boundary geometry,
dyadic coverage and exponent algebra. Four strictly elliptic test laws
include bias, symmetry, a near-arrow law and a deterministic law.
Hypothesis controls expose why future-event conditioning and dropping
delta>0 are not legitimate shortcuts. Actual stdout, source pin and
execution arguments are preserved in the finite receipts.

The analytic derivation proves the asymptotic estimates; finite controls
supplement it. Constants may depend on the fixed environment law,
epsilon, K and fixed gamma, and the asymptotic threshold can be large.
This review supplies no law-uniform bound as delta tends to zero.

This family does **not** accept the entire all-scale closure, priority,
source-conjecture interpretation, authorship or publication metadata.
In particular I did not independently audit the final moving-strip
argument. Root and the other distinct audit families must decide those
remaining parts. No input file, branch, PR, provider record, spreadsheet,
global lock or external communication was changed.

