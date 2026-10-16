# Priority audit and credited disposition

This records an audit deduction of **complete earlier mathematical coverage**.
It does not claim that an earlier author expressly announced an answer to the
February 2018 problem page, or that its proposer endorsed a particular level
of explicitness. Those historical/descriptive limits remain visible.

## Exact covering combination

Aldous–Diaconis's 1993 notes, printed 36–37, equation (42), already give the
simultaneous stationary positions as `Gamma(B_r)`: an independent unit-rate
Poisson arrival sequence evaluated at the compatible limiting pile-top ranks.
Their published 1999 account, printed 418, identifies the whole pile-top row
with the insertion tableau's first row under RSK. Restricting the tableau to
labels at most n is pathwise identical to inserting the subword of labels at
most n: high labels cannot alter lower entries. Uniform permutations therefore
give the coherent Plancherel tableau law, with each size-n tableau of shape
lambda having probability `f^lambda/n!`. This determines all joint B ranks.

If N(x) is the independent Poisson counting process, then, jointly for every
finite list of indices and thresholds,

`Gamma(B_r)>x <=> B_r>N(x) <=> lambda_1(x)<=r-1`.

The complete shape path is the horizontal ascending Poissonized Plancherel
process `C(x)=(x,1)` in Borodin–Olshanski (2004v2), equation (1.9), Remark 1.5
and Theorem 2.3. Its explicit one-box up probabilities telescope. From a shape
mu of size n to nu of size n+d over an increment Delta, the transition is

`e^-Delta Delta^d/d! * f^(nu/mu) * f^nu/f^mu * n!/(n+d)!`.

Multiplication across all thresholds cancels all intermediate ratios, giving
exactly the submitted weight

`e^-x_m D_1(lambda^m) product_j D_Delta_j(lambda^j/lambda^(j-1))`.

Summing its first-row barrier events gives the entire candidate formula,
including nonmonotone indices. This is a complete checked parameter bridge,
not inference from one-point marginals or mere availability of old tools.

## Earlier literal joint formula

Nica's Theorem 3.2 and Remark 3.3 already state the positive multi-time
skew-Schur product in arXiv1404.4015v1 (2014) and v3 (2015). Let M=x_m and
theta=sqrt(M). The area-preserving map `(u,v)->(u/theta,theta*v)` takes the
query rectangle to the square of side theta. Use Nica's positive branch in
reverse threshold order, `s=theta-x/theta`, with terminal shape at zero.
Its exact weight is

`e^-theta^2 D_theta(lambda^m) product_j D_(Delta_j/theta)(lambda^j/lambda^(j-1))`.

Homogeneity cancels theta because the skew sizes sum to the terminal size.
The result is precisely the submitted formula, with no asymptotic limit or
unidentified joint distribution. A coordinate swap gives the equivalent
negative-branch calculation. Fixed determinant dimension follows from standard
tableau transposition. The Poisson terminal-size mass supplies elementary
finite truncation. The identical shared-normalizer rational enclosure and
software may be a useful arrangement; their earlier exact appearance was not
established and is not claimed.

## Independent stationary bridge and source defects

The published 1995 Aldous–Diaconis paper, manuscript Section 2.2 pp5–6,
identifies the empty Hammersley count with the longest-chain count and gives
nearest-right dynamics; Lemma 4 p7 states simultaneous area-preserving scaling.
For inverse levels Z_i(t), the direct coordinate map
`Y_i(s)=e^s Z_i(e^s)`, `(u,v)->(uv,log v)`, has unit Jacobian and exactly the
positive linear drift and unit nearest-right jumps. Scaling gives stationarity;
finite-k uniqueness identifies the law. This verifies the old representation
without trusting the unfinished 1993 notes' erroneous scaling sign or unsafe
quantitative mean-coupling estimate.

The 2013 Borodin–Olshanski local tableau dynamics are expressly heuristic and
are **not** used as an established invariant-law theorem. The current Nica v3/v4
factorial display has a right-branch exponent typo; its correct Schur display,
full counting proof and v1 theorem resolve it. Later PDF title dates are
compilation dependent: the versioned 2015 source archive contains the actual
formula, uses the article class and has no explicit date declaration. Source
bytes, canonical version records and member pins were checked; late title dates
were not silently treated as earlier publication dates.

## Additional published finite-determinant coverage

Levikson–Rolski–Weiss, *Layering of the Poisson process in the quadrant*
(2001), printed420,423,425, equation(2.4) and Theorem2.5, give the probability
that the last ordinary finite Hammersley particle makes no jump. Define the
entire functions

`ell_a(z)=sum_(p>=max(0,a)) z^p/[p!(p-a)!]`.

For 0<x_1<...<x_k, the same stationary law is consequently

`P(X_i>x_i, all i)=e^-x_k det[ell_(i-j)(x_k-x_(k-j))]_(i,j=1..k-1)`.

The determinant is empty and equals one for k=1. The exact covering bridge is
an audit deduction, not a formula we claim LRW printed for the drift model.
Start the auxiliary pure-jump system at y_j=x_k-x_(k-j), with x_0=0. For
unrestricted patience sorting of this initial increasing word followed by the
rectangle events, let U be the number of resulting tops below x_k. The standard
variational identity is

`U=max_(j=0,...,k-1) [j+L((y_j,x_k) x (0,1))]`.

The finite first k coordinates have min(k,U) tops below x_k by prefix autonomy.
Their last top has not jumped exactly when U<k. Rotating both rectangle axes
turns these suffix-chain inequalities into L(x_i,1)<=i-1, jointly. LRW's
published last-no-jump determinant therefore supplies the displayed entire
joint-law determinant. A false intermediate assertion that unrestricted piles
can never exceed k was caught and corrected during audit; the cap min(k,U)
is essential. The negative control with initial2 and arrivals1/2,1 is retained.
The 1995 paper already states the arbitrary-initial-count variational formula.

Ties and zeros follow by continuity. An arbitrary finite query reduces to the
first K coordinates with z_i=max({0} union {t_j:r_j<=i}); these are weakly
increasing, so the determinant determines all joint events. The independent
historical and fresh falsifier controls checked the corrected finite event
identity and unequal-gap determinant coefficients. This additional route is
consistent with, and independent of, the BO/Nica joint-shape coverage above.
It does not establish earlier explicit acknowledgement of the 2018 posting.

## What this classification means

The queue's `already_solved` disposition means that the candidate target is
already completely covered by identifiable earlier explicit constructions and
formulas. It is not a claim of an earlier expressly acknowledged answer to the
named 2018 posting. The open-page chronology and bounded absence of an explicit
closure cannot erase exact prior mathematical coverage or establish novelty.
The submitted packet itself already disclaimed novelty.

The valid proof and code are retained with credit. Under the active goal's
claimed_solved-only scope, the corrected open draft is skipped. No new paper,
deposit, tracker row, merge, closure or PR comment accompanies this disposition.
All original 20 files, including older review verdicts and manifests, remain
unchanged in `original_submission/`. The broader goal remains active.

The campaign's full analytic reviews, primary-source ledgers, exact replays,
and separate novelty-saving/coverage challenges are recorded in the dedicated
PR246 audit folder on main. Whole third-party reading copies are excluded.
