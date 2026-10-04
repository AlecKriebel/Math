# Independent adversarial audit: Function Theory 7.17

Problem 2307017, rank 591. Audit date: 2026-10-04 UTC.

## Verdict

**The reconstruction and the repetition counterexample are mathematically accepted. No substantive proof gap was found.** The appropriate disposition is **already_solved, 1/5**, for the intended distinct/increasing-integer interpretation, with an explicit source-wording caveat. This is historical-status reconciliation and an independently checked reconstruction, not a new research discovery.

One presentational correction should accompany publication: describe distinctness as the interpretation/hypothesis adopted for the classical theorem, rather than claiming that the word “sequence” itself imposes it. The printed source does not explicitly say distinct or increasing. The unrestricted repetition-permitting statement is false, including for sequences tending to infinity. The candidate already supplies a valid counterexample, so no part of that ambiguity remains mathematically unresolved. See CORRECTIONS.md.

The mathematical acceptance binds exactly:

- Candidate PROOF.md SHA-256: `dbc101211ab443783f3d743361919d8db593395d70ec61664850dca314fe0afd`
- Full source manifest SHA-256: `09e7cead0b4399ce7d68f4be16b83500f0c346e556f108cdb14ce5e139aeac6b`
- Public source manifest SHA-256: `e1469113033a8a0550738f3c6d812896a2a09e3a98d3314838c9a379d478afdc`

The frozen source directory was not modified. No remote write, external communication, queue edit, or status mutation was performed.

## Exact scope accepted

For every bounded holomorphic f on Re z > 0, every fixed real alpha with |alpha| < pi/2, and every set S of positive integers with divergent sum of 1/n over n in S, the sampled and full-ray upper limits of log|f| divided by the radial parameter agree. The convention is log 0 = -infinity. If f is nonzero, both upper limits are finite and equal -a cos(alpha), where a is the nonnegative coefficient in the positive-harmonic representation after removing the Blaschke factor. If f is identically zero, both equal -infinity.

No ordinary limit, uniform estimate as alpha approaches the boundary, assertion on the boundary rays, or assertion for arbitrary repeated samples is accepted. The nonzero constant, zero-free, finite-zero, infinite-zero, and identically-zero cases are all covered. Arbitrarily sparse sets S are allowed provided their reciprocal sum diverges.

Distinct samples may be rearranged into increasing order without changing the reciprocal sum or radial limsup. There are only finitely many positive integers below any given bound, so any enumeration without repetitions tends to infinity. No asymptotic density assumption is being inserted.

## Canonical representation: independently reconstructed

Normalize a nonzero f to have norm at most one. The disk map w=(z-1)/(z+1), Jensen's zero condition, and

    1-|w|^2 = 4 Re z / |z+1|^2,
    1+|z|^2 <= |z+1|^2 <= 2(1+|z|^2)

give the half-plane Blaschke summability condition sum Re(a_j)/(1+|a_j|^2) < infinity. Multiplicities are included. For every finite prefix of the normalized disk Blaschke product, successive Schwarz division preserves the bound one. Taking the locally uniform product limit proves that f/B has a holomorphic extension through the zeros, is zero-free, and has modulus at most one. Thus h=-log|f/B| is nonnegative harmonic.

The measure transformation in the harmonic representation can be written explicitly. If mu is the finite positive disk-boundary measure and z=x+iy, set zeta(t)=(it-1)/(it+1). For w=(z-1)/(z+1),

    P_D(w,zeta(t)) = x(1+t^2)/|z-it|^2,
    P_D(w,1) = x.

Separating the atom a=mu({1}) and defining d nu(t)=(1+t^2) d mu(zeta(t)) gives exactly the candidate's equation (1), including the weighted integrability of nu. There is no finite-total-mass requirement on nu, and no identification with a finite-complex-measure Laplace transform. The zero harmonic function is the zero-measure case. The coefficient a is finite, for example because a <= h(1).

Along rq, with q=c+is and c>0, division by r yields the candidate's kernel. The denominator obeys

    r^2-2rst+t^2 >= (1-|s|)(r^2+t^2).

For r>=1 the integrand after weighting by 1+t^2 is bounded by 1/(1-|s|), and converges to zero at every fixed t. Dominated convergence with respect to d nu/(1+t^2) is valid and establishes h(rq)/r -> ac. Constants depending on fixed alpha cause no problem.

Bonk's Theorem 7.6 was independently opened and checked. Its upper-half-plane formulation rotates to the representation used here; its theorem number and weighted-measure condition match the citation. [Official lecture notes, printed pp. 54–55](https://www.math.ucla.edu/~mbonk/252a.1.16f/InvPro.pdf).

## Exceptional set and nonlocal estimates

The kernel identity is correct because

    |nq+conjugate(a)|^2 - |nq-a|^2 = 4n c Re(a).

Consequently the potential is nonnegative and equals minus the logarithm of each factor modulus. The sum identity follows by locally uniform Blaschke convergence; at a zero both sides are +infinity.

In Section 2, centers nq at distinct positive integers have distance at least one, so the open radius-1/4 disks are disjoint. Selecting a zero in each relevant disk is injective even when zeros have multiplicity. If n>=1/c, then u>=cn-1/4>=cn/2 and |a|<=n+1/4. The claimed beta>=c/(6n) follows from

    2(1+(n+1/4)^2) <= 6n^2   (n>=1).

Therefore the selected integer reciprocal sum is bounded by (6/c) sum beta. The initial set n<1/c is finite. This proves the exceptional-set estimate; exact sample zeros are necessarily excluded. The small-distance exclusion is important: a zero exponentially closer than a fixed distance to one large integer can create an arbitrarily large single logarithmic summand.

In Section 3, the three nonlocal regions are disjoint and exhaustive. Their per-zero upper bounds relative to beta are respectively 10c, 10c, and 40/c. In the first region the summand for each fixed zero tends to zero; dominated convergence for the summable beta measure applies with the moving-region indicator included. The other regions have |a|>2n or |a|>=n/2, and their beta sums are tails tending to zero. Boundary equalities at n/2 and 2n belong to the middle-radius region as defined. Thus D(n)/n -> 0 and every D(n) is finite. No unproved uniformity in the zero distribution is used.

## Local estimate and completion

For a fixed zero local to some integer, R=|a|>=1/2 and all local integers obey R/2<=n<=2R. Projection onto q gives |nq-a|>=|n-Re(a conjugate(q))|. Outside E0 it is also at least 1/4. The numerator is at most n+R<=3R. This proves the logarithmic envelope in (8).

For p=Re(a conjugate(q)), the number of all integers with |n-p|<T is at most 2T+2. For layer height 0<t<log(12R), the envelope superlevel set is contained in |n-p|<3R exp(-t); above that height it is empty. Thus the layer-cake integral gives at most 6R+2log(12R). The final bound 14R is valid even at R=1/2: the function 4R-log(12R) is positive there and increasing for R>=1/2.

Weighting by 1/n^2 costs at most 4/R^2, giving 56/R. Existence of a local integer implies u>=cR/4; because R>=1/2, beta>=c/(20R). Hence the advertised 1120 beta/c bound is correct. Tonelli applies to nonnegative terms and yields sum L(n)/n^2 < infinity outside E0. For every epsilon>0,

    sum_{n not in E0, L(n)>=epsilon n} 1/n
        <= epsilon^(-1) sum_{n not in E0} L(n)/n^2 < infinity.

Subtracting any such exceptional set from S leaves a divergent reciprocal sum. The diagonal choice n_k outside E_(1/k), with D(n_k)/n_k<1/k and n_k increasing, is valid. It does not require the union of the exceptional sets to have finite reciprocal sum. It follows that the Blaschke potential divided by n has sampled liminf zero. Combining this with the harmonic limit yields sampled limsup -ac. The pointwise nonpositivity of log|B| supplies the full-ray upper bound, and the sampled subsequence supplies the lower bound. There is no circular inference from the desired ray equality.

## Repetition counterexample

The dyadic product converges locally uniformly because the differences of its factors from one are locally summable. Each factor has modulus at most one on the half-plane; the product is nonzero, for example at z=1. Repeating 2^k exactly 2^k times gives a sequence tending to infinity, with divergent reciprocal sum, all of whose sample values are zero.

For x_m=3*2^(m-1), reindexing produces exactly the lower-tail-truncated two-sided product stated in Section 6. The factors are strictly between zero and one. For j<=1 their defects are at most 2^(j+1)/3; for j>=2 the defects are at most 6/2^j. Both tails are summable, so the two-sided product is strictly positive. Every truncated lower tail is at least that positive product. Hence the full-ray limsup is zero, whereas the repeated sampled limsup is -infinity. This proof is independent of Sections 1–5.

The same product sampled at all positive integers also demonstrates why an ordinary limit cannot replace the limsup: dyadic zeros coexist with the nonzero off-zero subsequence.

## Primary source reconciliation

The supplied scan of Hayman–Lingham's printed p. 165 was visually inspected. Its update expressly attributes resolution to Korevaar and Zeinstra, and its bibliography identifies the 1985 paper and Zeinstra's 1992 paper. The arXiv record independently confirms the cited v2 and 2018 date. Therefore the imported report's claim that the problem remained open in that edition is contradicted by the source page itself. [Hayman–Lingham, arXiv:1809.07200v2](https://arxiv.org/abs/1809.07200v2).

The supplied institutional scans of Zeinstra's pp. 2, 11, and 12 were visually inspected. Equation (6.2) has bars over both limits. Theorem 4 uses sum 1/|lambda_n| divergent and |lambda_n-lambda_m| >= delta |n-m|. The transform is defined from a finite complex Borel measure on a bounded-slope curve satisfying condition (C). For a straight positive-real support ray the curve condition is immediate; sorted distinct integer radial samples satisfy the separation condition, and any fixed interior sample angle lies in a smaller admissible sector. This corroborates the intended separated sampling convention, but only in that theorem's stated transform class. [Zeinstra 1992](https://doi.org/10.1515/crll.1992.424.1); [institutional scan, printed p. 11](https://gdz.sub.uni-goettingen.de/id/PPN243919689_0424?tify=%7B%22pages%22:%5B15%5D%7D).

There is a genuine reason to avoid the class identification: a finite-measure Laplace transform on [0,infinity) extends continuously to the imaginary boundary, whereas a bounded half-plane holomorphic function need not. For instance exp(-1/z) is bounded in the right half-plane but does not admit a continuous extension at zero. The accepted proof makes no such reduction.

The word “sequence” alone does not imply distinctness in a formal theorem. The source update plus the separated-sampling reference support the intended interpretation, while the supplied counterexample resolves the literal extension. The audit did not independently recover/read the 1985 proof. That limitation does not undermine either the source's explicit historical attribution or the independent mathematical reconstruction.

## Reproducibility and limits

The original control script was copied to the separate audit directory and run there, because running it in the frozen directory would overwrite its output file. Its generated CONTROL_RESULTS.json is byte-for-byte identical to the frozen one: 48 exact rational kernel checks, 1,539 local-sum cases with 83,407 summands, and 162 near-zero cases reproduce exactly.

The independently authored audit_controls.py additionally passes 1,470 exact rational kernel checks; 1,362 nonlocal-region bound checks; 196 Poisson domination checks; 168 near-zero weight checks; 120 all-integer layer-cake envelope checks; and 401 exact dyadic defect checks. Rational angles include cosines near 10^-6, and radial parameters include 10^6. Floating-point envelope checks include R=1/2 and near-integer/half-integer shifts. These finite checks support error detection only; the analytic arguments above establish the infinite claims.

The audit independently verified frozen file integrity and the selected problem/report records. It did not redownload the roughly 149 MB corpus or rerun the original bounded remote duplicate searches. Those provenance/search statements remain the original packet's documented bounded checks, not new guarantees of global absence. Nothing in the accepted theorem depends on a duplicate search.

## Publication boundary

The actual full SHA256SUMS has **32 entries, not 31**: 24 private files, six public deliverable files, AUDIT_REQUEST.json, and PUBLIC_SHA256SUMS. All 32 pass. The directory has 34 files when SHA256SUMS and FREEZE.json are included. There are no symlinks. The full manifest's hash matches the supplied freeze exactly.

The exact safe candidate publication allowlist is:

1. public/README.md
2. public/PROOF.md
3. public/SOURCE_STATUS.md
4. public/APPROACH_LOG.md
5. controls/check_controls.py
6. controls/CONTROL_RESULTS.json

This list matches AUDIT_REQUEST.json and PUBLIC_SHA256SUMS exactly. **Do not publish the full root, private directory, source PDFs, scanned page images, downloaded HTML/responses, imported problem/research records, repository-state snapshots, or the full private-binding manifest as if it were a public export list.** The private material was used for scholarly verification only. Any later public audit attachment must be explicitly selected as an authored audit artifact; inclusion in this separate audit directory does not automatically add it to the six-file candidate allowlist. This audit does not authorize a remote publication action.
