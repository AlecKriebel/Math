# Root mathematical scope certificate: 9500008 / AMR-094-0008

2026-10-02 UTC. This is verification of the submitted partial result, not a new
attempt to solve the missing random-origin problem. Original effort remains
2/5; new substantive attempts and audit proof attempts are both zero.

The literal reconstruction was sealed before PARTIAL.md or previous verdicts
were read. Its disclosed initial exposure included the complete dated source
and prior report, route labels, and the PR description. The seal does not claim
complete blindness. The author-maintained Problem 8 supplies the random-origin
definition omitted from the extracted statement. The target allows an almost
surely finite real random S, not necessarily a stopping time, a junction, or
independent of X, such that the two centered outward half-paths at S have the
independent standard Wiener joint law. The input is independent stopped pairs,
possibly nonidentical and of zero duration, with a common deterministic finite
strict upper bound c and divergent duration sums in both directions. Brownian
motion must be Brownian for the filtration in which its duration is stopping.

## Independently checked deduction

Write A_j=sum_{i=1}^j T_{-i}. Construct W outward in negative index order from
the original internally forward stopped paths -B^{-1}, -B^{-2}, ... . The
reflection retains the Brownian property in each original filtration, and each
duration is still a stopping time. It need not retain the joint stopped-pair
distribution. Deterministic reflection retains independence of the marks.

For any finite number of marks, append a fresh independent Brownian suffix.
Strong Markov restarting, applied from the final mark backwards, gives Wiener
law. This argument needs independence of the stopped marks, not of their
unobserved tails. The finite splice and actual infinite W agree through A_j.
On a deterministic compact [0,H], their total variation distance is at most
P(A_j<=H), which tends to zero. Divergence therefore proves W is Brownian on
every compact. Zero marks remain in the indexing; there is no conditioning on
a random positive-duration subsequence. The positive half of X is Brownian by
the same argument. Its generating nonnegative-mark sigma-field is independent
of the negative-mark sigma-field, so the entire two half-paths are independent.

For a=A_{j-1}, T=T_{-j}, and 0<=u<=T, endpoint subtraction gives

    X(-(a+u))=W(a)+W(a+T)-W(a+T-u).

Subtracting W(a+u) gives two increments, each of duration u<=T<c. If a+u<=H,
every endpoint lies in [0,H+c], including a+T when the horizon cuts a piece.
Thus sup_{t<=H}|X(-t)-W(t)|<=2 omega_W(c;H+c). This is a pathwise identity and
inequality; no stopped-piece reversal law or independence of endpoints is used.

At H_m=c 2^m, increments of duration at most c are covered by the deterministic
windows [jc,(j+2)c], 0<=j<=2^m+1. Reflection and the Gaussian Chernoff bound give
P(sup_{u<=2c}|B(u)|>r/2)<=4 exp(-r^2/(16c)). Union over the 2^m+2 windows is
valid without independence and does not count random pieces. Substituting
r=8 sqrt(cm) makes the resulting 4(2^m+2)exp(-4m) summable. First
Borel--Cantelli and monotonic interpolation prove the stated almost-sure
O(sqrt(log(2+H))) expanding-interval error. The constant can depend on c and
the sample; a deterministic universal all-sample bound is not claimed.

Set Z(t)=X(t) for t>=0 and Z(-t)=W(t). Z has the fixed-origin two-sided
Brownian law. For each fixed L, the scaled X-to-Z uniform distance on [-L,L]
vanishes almost surely. Brownian scaling leaves the comparison law constant,
so metric-space Slutsky proves weak convergence in C([-L,L]). This does not
assert almost-sure convergence of scaled Z to a single Brownian path.

The capped negative-hit example disproves only fixed-origin Brownianity; its
iid bounded positive-mean marks satisfy the published positive random-origin
theorem. Grouping periodic *entire stopped-pair laws* into a period gives iid
stopped Brownian blocks with finite positive mean. Duration marginals alone
would not suffice. Neither example supplies a counterexample to Problem 8.

## Primary proof coverage and qualifications

Root freshly inspected the university-hosted Forward Brownian Motion v4 PDF
through the web tool, and directly read the operative text of the independently
retrieved university-hosted copy: Definitions 2.1--2.2, complete Theorem 5.1
renewal/mark-kernel proof, complete Theorems 5.2--5.3 including the rotation
mechanism and finite-moment construction, and Problem 7.7 with its neighboring
remark. Its stationary renewal imports are cited foundational dependencies,
not newly recertified here. The essential iid common conditional mark kernel
cannot be supplied by a common duration bound in the nonidentical case.
Problem 7.7's almost-sure random supremum and backward-Brownian conclusion
are distinct from the author's deterministic-bound exact two-sided question.

Root also directly read Mörters--Peres Brownian Motion, Lemma 1.7 and the
operative stopping-time approximation, Theorem 2.14 proof, Theorem 2.16 proof,
Remark 2.17, and Theorem 2.18 proof (printed pp25,47--50) from the separately
retrieved primary PDF/text cache. Its Gaussian-scaling and dyadic stopping
approximations justify the standard imports; the same proof works with a
normal enlarged filtration whenever Brownian independent increments hold
relative to it. This is coverage of those imports, not the whole book or an
exhaustive literature audit. Root read both new independent mathematical
reports only after its own reconstruction and the original argument.

The original review's sentence that Brownian symmetry preserves each stopped
Brownian-pair law requires correction as an equality of joint distributions.
For T=min(first hit of -1,1), B_T has a positive atom at -1; -B_T instead has
that atom at +1. The valid statement is reflected-pair admissibility and
independence, followed by strong Markov concatenation. PARTIAL.md uses that
valid deduction and needs no theorem change. Preserve the historical review
and publish a separately recorded precision correction in current material.

The strongest verified result is the displayed uniform coupling, logarithmic
error and weak diffusive limit for the stated full bounded independent-piece
class. The remaining exact gap is one finite random origin giving the exact
independent Wiener joint law, or an admissible bounded counterexample ruling
out every such origin. Rotation modifies interiors of infinitely many pieces;
asymptotic agreement and windows sent to positive infinity do not fill this
gap. Status remains unsolved; no novelty, paper, new DOI or tracker row.

Root's actual diagnostic/provenance replays and the future new whole-current
adversarial gate remain separate prerequisites. This certificate does not
transfer earlier PASS labels into those pending executions.
