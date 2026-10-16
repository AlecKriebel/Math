# Bounded-delta verification and targeted second analytic review

Problem 30005453, rank 798, OWR-12697708-006. Reviewed 5 October 2026 (UTC).

## 1. Scope, independence, and classification

This review began after the original candidate and first audit were frozen.
The reviewer did not prepare either or edit the proposed v2. The complete first
AUDIT.md, PROPOSED_V2.diff, and proposed proof were read. The proposed proof's
unchanged analytic core was then reconstructed, with particular attention to the
space-time maximum argument and its stochastic inputs. No nested review or
remote publication was performed.

The outcome is acceptance of the explicitly corrected positive-equilibrium
candidate. It is not acceptance of uniqueness among all nonnegative equilibria.
No new mathematical patch was needed. This targeted second review complements
the first full audit; it does not pretend to repeat its complete corpus rehash,
repository search, or literature-priority search. Those recorded findings remain
bound to the unchanged first-audit archive, not silently converted into newly
performed research.

## 2. Exact bounded delta

All three input archives match the requested hashes and sizes. Their member
lists, non-symlink regular payloads, CRCs, manifest coverage, member sizes, and
SHA-256 hashes pass an independent verifier. The local frozen directories also
match their archive members exactly.

The new verifier transcribes the six permitted replacements directly and
rebuilds the expected v2 from original bytes. It does not run or import the
first auditor's patch code. The rebuilt object equals v2 byte for byte, including
the regenerated manifest. Its independent unified diff exactly equals the first
audit's PROPOSED_V2.diff.

Only these content files change:

- PROOF.md: corrected source-attribution paragraph and equation (9) offset
- README.md: corrected distinction between the literal and positive formulations
- SOURCE_REVIEW.md: two source-scope wording changes
- RESULT.json: outcome label identifying the explicitly corrected formulation

MANIFEST.json changes only its v2 proposed-status labels and the affected file
sizes/hashes. Every other member is identical. In particular, both verifier
scripts and the saved author algebra results are unchanged. The theorem's
hypotheses are unchanged.

The exact byte slice starting at the `## 2.` heading and ending immediately
before `## 9.` is 12,593 bytes in both versions, SHA-256
`d9da7dc05a3debfd2537a00f0a193b72f6e8714bbe3e8389f5dc6b9a916a9e54`.
This definition includes the section-2 heading and all intervening whitespace.

Eleven negative controls are rejected. Five test archive structure: missing,
extra PDF, duplicate, traversal, and symlink entries. Six test unauthorized
content with internally consistent regenerated manifests: an analytic edit,
a code edit, false source attribution, the wrong initial-offset reference,
an unrelated research-log change, and silent self-acceptance. The latter checks
show that passing a self-consistent manifest alone is insufficient.

## 3. Source interpretation and the boundary counterexample

The primary report was independently re-extracted from the hash-verified PDF;
printed pages 654-655 were also rendered and visually inspected. Its equilibrium
definition and Conjecture 1 do not explicitly require positivity on every edge.
Thus v2 correctly describes a corrected formulation and treats intended source
scope as an inference. The original report's initialization is also more general
than the unit initialization chosen for this candidate. The reviewer does not
require restoring an unqualified claim to the original source wording.
[Primary report](https://doi.org/10.4171/OWR/2023/12).

The boundary objection is mathematical, not terminological. Let the edges of Z
alternate between 2 and 0 and put every vertex rate equal to 1. Every vertex sees
one positive edge, so its denominator is 2^alpha, which is nonzero. A positive
edge receives intensity 1+1=2; a zero edge receives zero because alpha>0. Both
phases are fixed points. The constant-one array is another fixed point. Therefore
literal uniqueness in the nonnegative class is false throughout 0<alpha<1.
Convergence from unit counts to the strictly positive equilibrium is a different,
consistent statement.

The arXiv record was freshly checked and identifies v2 dated 25 June 2021 and
the ECP publication. This review does not renew the earlier broad novelty search.
[Couzinie-Hirsch manuscript](https://arxiv.org/abs/2010.03347).

## 4. Equilibrium inputs needed by the decisive lemma

Write c=1-alpha and beta=alpha/c. For strictly positive equilibria,
x_uv^c=z_u+z_v with z_v=p_v/S_v(x), and z_v T_v(z)=p_v where
T_v(z)=sum_{w~v}(z_v+z_w)^beta. Division by x_uv^alpha is legal precisely because
this reduction concerns positive edges. It cannot be used to dispose of boundary
fixed points.

The bound z_v <= (p_v/d(v))^c <= B=P^c follows directly from
T_v(z)>=d(v)z_v^beta. Finite-volume minimization with zero exterior values has
coercive power terms and a strictly convex logarithmic barrier. At a fixed
vertex its minimizers remain between p_v/[d(v)(2B)^beta] and B. Countable diagonal
compactness and finite degree therefore produce a positive infinite-volume
solution. No uniform positive rate infimum is used.

The uniqueness estimate also uses an absolute difference, not a ratio. At a
vertex where z_v-y_v>M-epsilon for M=sup|z-y|, every incident pair sum can be
smaller by at most epsilon. A modulus of continuity gives
0 >= (M-epsilon)^(beta+1)-BD*omega(epsilon), a contradiction for small epsilon.
If the opposite sign approximates the supremum, interchange z and y. One does
not need the supremum to be attained.

## 5. Independent attack on the complete-trajectory lemma

### 5.1. Modulus and the upper strip

Assume a positive classical solution b is defined for every real time, with
common upper bound K0>=B. Set M=sup_{v,s}|b_v(s)-z_v|. If M>0, select epsilon<M/4
so that BD*omega(epsilon)/(M/2)^beta<M/4. Uniform continuity on [0,2K0] suffices.
Explicit valid moduli are epsilon^beta for 0<beta<=1 and
beta*(2K0)^(beta-1)*epsilon for beta>=1. No derivative bound at zero is needed.

At a point with d_v=b_v-z_v >= M-epsilon, every neighbor has d_w>=-M.
Consequently T_v(b)>=T_v(z)-D*omega(epsilon). Also b_v>M/2, so
T_v(b)>=(M/2)^beta. Using p_v=z_v T_v(z) gives

    p_v/T_v(b)-z_v <= BD*omega(epsilon)/(M/2)^beta < M/4.

Thus d'_v=c[p_v/T_v(b)-z_v-d_v] <= -cM/2 throughout that strip. This remains
valid if p_v is arbitrarily small: the denominator needed in this inequality
is protected by the large current b_v, rather than by a rate lower bound.

### 5.2. The lower strip and the potentially vanishing denominator

At d_v<=-M+epsilon, every neighbor has d_w<=M, so
T_v(b)<=T_v(z)+delta, where delta=D*omega(epsilon). Here z_v>M/2, whence
T_v(z)>=(M/2)^beta. The useful monotonicity is of the reciprocal denominator:

    p_v/T_v(b)-z_v
      >= z_v*T_v(z)/(T_v(z)+delta)-z_v
       = -z_v*delta/(T_v(z)+delta)
      >= -BD*omega(epsilon)/(M/2)^beta > -M/4.

It follows that d'_v>=cM/2. This calculation neither asserts nor needs a uniform
positive lower bound on T_v(b). If T_v(b) is very small, the actual drift becomes
more positive, which helps rather than harms the estimate. Replacing its
reciprocal by an absolute Lipschitz estimate would have been a gap; the candidate
does not do that.

### 5.3. Why a nonattained space-time supremum is sufficient

Some fixed coordinate v and finite time s0 satisfy |d_v(s0)|>M-epsilon. Suppose
its sign is positive. Let I be the connected component of
{s: d_v(s)>M-epsilon} containing s0. If I had a finite left endpoint l, continuity
would give d_v(l)=M-epsilon. Integrating d'_v<=-eta, eta=cM/2, on [l,s0] would
give d_v(s0)<M-epsilon, a contradiction. Thus I extends to negative infinity.
Integrating backwards on I gives d_v(s)>=d_v(s0)+eta(s0-s), which contradicts
d_v(s)<=M for sufficiently negative s. The negative case uses the same argument
for -d_v. Therefore M=0.

This is a one-coordinate scalar barrier argument after a global bound has been
chosen. It never differentiates an infinite supremum, takes a maximum over an
infinite set, or sums infinitely many Lyapunov terms. The decay of rates towards
zero does not change the fixed positive eta supplied by the hypothetical M.

Completeness cannot be weakened to existence only for future times. As a check,
on a single edge with equal endpoint rates p, symmetric trajectories satisfy
b'=c[p/(2b)^beta-b]. With y=b^(beta+1), this becomes y'=p/2^beta-y, so

    y(s)=p/2^beta+C*exp(-s).

For C>0 the positive solution is unbounded backwards; for C<0 it reaches zero
at a finite backward time. Forward bounded nonstationary solutions exist, but
only C=0 is positive, bounded, and complete. The candidate correctly establishes
all three required properties for its limiting trajectories.

**Conclusion for the critical lemma: PASS as written.** The strongest attempted
failure modes were a nonattained supremum, arbitrarily small rates, an arbitrarily
small lower-strip denominator, lack of Lipschitz continuity at zero for beta<1,
and nonstationary backward trajectories. Each is handled by a specific hypothesis
or inequality already present in the proof.

## 6. Compensator-normalized martingale law and noncircular growth

For a fixed edge, each jump of H(N) is exactly N^(-alpha), while the count intensity
is N^alpha*q. Therefore H(N)=Q+M and the predictable bracket is
integral N^(-alpha)*q <= Q. Since the endpoint clocks have bounded rates and
N>=1, finite-horizon square integrability holds before any asymptotic statement.

Let A=1+Q and L=integral A^(-1)dM. The compensator Q is continuous and adapted,
so the integrand is predictable. Its bracket is bounded pathwise by
integral (1+Q)^(-2)dQ<=1; consequently the martingale L is bounded in L2 and
converges almost surely. Integration by parts with continuous A gives

    M/A = L - A^(-1)*integral L dA.

There is no jump cross term and no assumption of independence between Q and M.
On Q tending to infinity, weighted Cesaro convergence makes the two right-hand
terms have the same limit, proving M/Q->0.

That divergence is separately established from the endpoint-clock upper bound.
For every fixed incident neighborhood and epsilon>0, all its finitely many
counts are eventually at most (2P+epsilon)t. It follows that
q_e(t)>=k_{e,epsilon}t^(-alpha), with k_{e,epsilon}>0. Thus Q_e grows at least
on the t^c scale. Only then are the transform asymptotic H(n)=n^c/c+O(1) and
M/Q->0 used to obtain positive linear lower growth.

The other direction is also sound: the clock bound makes H(N)=O(t^c), and
H(N)/Q=1+o(1) yields Q=O(t^c), then M/t^c->0. Splitting Q into its two endpoint
integrals gives X_uv^c=A_u+A_v+o(1), with the factor c exactly as in the text.
There is no circular appeal to convergence or to positive linear growth inside
the martingale law.

For initial count n0>1 the compensated identity is instead
H(N(t))-H(n0)=Q(t)+M(t), since a martingale starting at zero cannot equal H(n0)
at time zero. This is precisely equation (9), not the lower intensity estimate
(12). The subtraction is coordinatewise finite and disappears under t^(-c)
scaling, with no uniform bound on the initial-count array required.

**Conclusion for the martingale and growth step: PASS.**

## 7. Time shifts, product compactness, and actual convergence

The vertex quantities A_v(t) have a common limiting upper bound K=(2P)^c and
individual strictly positive lower bounds ell_v=p_v/[d(v)(2P)^alpha]. In logarithmic
time their derivatives are c[p_v/S_v(X)-a_v]. Positive lower growth on each
fixed finite incident set bounds that derivative eventually for each fixed v.
The bound and its starting time may depend on v. Nothing requires spatially
uniform Poisson fluctuations or a spatially uniform random starting time.

For any s_n tending to infinity, Arzela-Ascoli can be applied successively to the
countably many coordinates and compact intervals [-j,j]. Diagonal extraction
produces one subsequence valid for all these coordinates and intervals. The
limiting trajectory is defined on all real s and satisfies ell_v<=b_v(s)<=K.
The upper bound K is common in the limit because it applies separately to each
coordinate; no interchange of a spatial supremum with a limit is being used.

If r_e(t)->0, then sup_{|s|<=j}|r_e(exp(s_n+s))|->0, since the smallest physical
time exp(s_n-j) tends to infinity. Thus the edge representation transfers to
the limits locally uniformly. Raising positive edge sums to beta and taking
finite incident sums preserves this convergence. Each limiting denominator is
positive, so inversion is legitimate on the compact interval in question.
The integral form of the dynamics passes to the limit, giving a classical
solution of b'_v=c[p_v/T_v(b)-b_v].

The limiting trajectory therefore meets exactly the lemma's completeness,
positivity, and common-upper-bound hypotheses. It must equal z. If any fixed
coordinate failed to converge, a sequence of separated values would yield a
contradictory limit at time zero under the same extraction. This proves actual
coordinatewise convergence. Finally countability permits one common probability-
one event for all edges, rather than an unsupported uniform convergence claim.

At alpha=0, independent marking/thinning of each vertex clock directly gives
the deterministic limiting edge rate p_u/d(u)+p_v/d(v). The beta>0 lemma is not
misapplied to that endpoint. Alpha=1 and negative exponents remain excluded.

**Conclusion for the infinite-dimensional passage and completion: PASS.**

## 8. Computation, replay, and limitations

The independent targeted script uses 220-digit Decimal arithmetic for 216
local approximate-extremum tests, including 96 noninteger-beta cases. It covers
beta from 0.05 to 50, degrees 1, 2, 5, and 17, and small positive parameters
10^(-12) and 10^(-60). Besides the adverse-neighbor upper and lower strips, it
checks lower-strip configurations with very small actual denominators. It also
checks 100 local boundary-pattern edge equations.

Separate exact rational diagnostics check 125 transformed-jump/bracket identities,
18 single-edge scalar identities, and four nonunit-initial-count controls. These
finite checks are arithmetic diagnostics. They do not prove the infinite lemma,
the probability-one claims, or the product-topology limiting argument; the
analytic review above supplies the basis for those verdicts.

Both original and v2 author verifiers and the first audit's replay were run in
temporary extractions. All passed and every extracted file was byte-identical
after replay. No original archive or frozen directory was changed.

The accepted theorem remains a mathematical candidate reviewed by these audits.
This is not formal proof-assistant verification, journal peer review, a priority
finding, or a claim of a previously unknown published resolution. No source PDF,
source extraction, screenshot, raw corpus, or private coordination material is
included in the safe acceptance artifact.
