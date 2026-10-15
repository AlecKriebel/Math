# Fresh final adversarial acceptance audit of PR14

**Verdict: PASS for the current narrow theorem and its qualified credited
disposition. No mandatory mathematical or candidate-source repair identified.**

Reviewed candidate SHA-256:
`20afe8e57f91c5f6483d54389d70fc7d19fce27114549b83461289f760ac1229`.
Original PR head: `a81fa89f6613791dd55ad5b79bfe8053bd1585f3`.
Target: 30005934 / OWR-14298374-003. Audit date: 1 October 2026 UTC.

Recommend **already_solved for the intended noninteger question, as an accepted
credited partial research record; no new paper, DOI, or tracker row**. The
source's literal N convention remains unresolved, and zero is allowed.
This is an independent AI proof audit, not human peer review or formal
verification. It does not endorse the earlier manuscript's broad classification.

## Freshness and success criterion

The first access was restricted to the current CANDIDATE.md, original
source_record.json, and the three linked published primary mathematical
sources. I reconstructed the stochastic proof and sought boundary
counterexamples before reading previous reviews, family reports, acceptance
summaries, current metadata, or the earlier Anonymous manuscript.
`INDEPENDENT_CONCLUSION.md` and the first timestamped research-log checkpoint
record that independent analytic verdict before later reconciliation.

The exact tested implication is: for infinite-dimensional separable real H,
any C_0 generator A, bounded positive self-adjoint injective Q, an adapted
positive trace-class trace-norm-continuous weak solution with full real
Hilbert-Schmidt Brownian noise relative to its filtration, and finite almost
surely F_0-measurable initial value, alpha must lie in N_0. No initial moment,
semigroup injectivity, trace-class integrated covariance, or Markov property
of finite compressions is assumed. Success requires a valid checkable proof
of this implication, source/parameter fidelity, correct prior attribution,
reproducible computational evidence, and preservation of frozen history.

## Independent analytic findings

The detailed derivation is in `DERIVATION.md`. The difficult steps survive the
following challenges:

- **Moving tests and no initial moments.** D(A^2) is dense and its semigroup
  columns are graph-C^1 paths in D(A). Integrating finite-span approximants to
  their derivatives gives the required joint approximation of the path and
  derivative. Stopped drift estimates use the trace-norm bound; stochastic
  errors have squared integrand norm at most
  `4m ||Q|| ||v_k-v||^2`. The initial term converges pathwise from its finite
  trace norm. When the initial norm exceeds m, the stop is zero and all
  integrals vanish. Trace-norm continuity exhausts every finite horizon.
- **Adjoints, noise correlation and factor four.** Pairing the weak drift
  with v gives `tr[X(Av+(Av)^*)]`. The same Brownian motion appears twice;
  its combined representing integrand is `2 sqrt(X) v sqrt(Q)`, with bracket
  `4 tr(XvQv)`. The backward exponent drift is `-2 tr(X psi Q psi)` and half
  its bracket is the positive opposite quantity.
- **Bounded local martingale.** Positivity bounds the exponential by a finite
  deterministic constant for every real alpha. This supplies a true
  martingale and its F_0-conditional identity without an initial moment.
- **One conditional matrix law.** Disintegrating the joint law of (X_0,Y)
  uses standard Borel state spaces, not a special underlying sample space.
  A common null set on a countable dense test set extends by continuity to
  all positive tests. Only one deterministic n,T,J is needed for a given
  noninteger alpha.
- **Published fixed-law dependency.** The candidate transform has GMM's
  shape alpha/2, positive scale 2C, and noncentrality b. Definition 1.1 and
  Theorem 1.3(ii)<->(iii) impose the required parameter set on existence of
  one probability law. No process-Markov requirement is imported. Negative
  alpha is excluded separately by scalar-transform growth; nonnegative
  nonintegers by n>alpha+1. [GMM primary paper](https://arxiv.org/pdf/1607.00206).

I also independently recorded the tilt-and-rescale mechanism before family
comparison. Whitening a hypothetical noncentral law, tilting by its scalar
trace, and rescaling suppress its noncentrality and yield a central law. A
weighted determinant derivative, justified at a strictly positive matrix
test, has sign `product(alpha-j, j=0,...,n-1)`. A noncircular interpolation
from explicit integer Gaussian matrices proves this identity in every n.
It is negative at n=floor(alpha)+2 for noninteger alpha. This provides a
checkable second necessity mechanism without relying on the full noncentral
rank classification. Its agreement with the stochastic family's separately
developed mechanism was learned only after the independent conclusion.

## Counterexamples and limiting cases

The genuinely noninjective left shift on L^2(0,infinity) with Q=I has
`C_t` equal to multiplication by `min(t,x)`. This covariance is positive but
noncompact, hence not trace class. Smooth tests supported inside (0,T) are
killed by S(T), but still have positive compressed C_T. Thus neither a
semigroup kernel nor non-trace-class covariance breaks the transform proof.

The conclusion would fail in finite dimension: scalar squared Bessel
processes admit noninteger nonnegative drift. It would also fail after
dropping Q's injectivity: rank-one noise admits a scalar embedding in
infinite dimension. Alpha=0 with X_0=X=0 satisfies all equations. A finite
almost surely but infinite-mean random initial trace also causes no failure
of localization or the bounded exponential argument. These stress cases are
not assertions of general solution existence. No counterexample was found
under the exact hypotheses.

## Reproduction and corruption probes

`fresh_checks.py` was written independently and uses only exact Fraction
arithmetic. **117/117 checks pass.** It covers every matrix-unit Brownian
coordinate in a noncommuting 3-dimensional example, a nonnormal generator
and rectangular Riccati test, singular/full-rank/zero resolvents, tilt
normalization, determinant Taylor jets in dimensions 1--4, noncentral
determinant polynomials, obstructing dimensions and shift compressions.
It rejects the factor-two bracket, the adjointed representing integrand,
generator transpose swap, quadratic Riccati sign reversal, backward exponent
sign reversal, incorrect noncommuting inverse order, and incorrect symmetric
off-diagonal differentiation factor.

`replay_evidence.py` runs supplied code copies only inside this audit's ignored
scratch. All five suites pass, totaling **211 recorded checks**:

| Suite | Checks | Receipt comparison |
|---|---:|---|
| Original author | 8 | Byte-identical |
| Historical independent reviewer | 19 | Byte-identical |
| Reproduction-family fresh probes | 29 | Identical except intentional generated_at_utc |
| Stochastic-family exact checks | 11 | Byte-identical |
| Conditional-adversary determinant jets | 144 | Byte-identical |

The timestamp difference is explicitly recorded rather than hidden. All
mathematical, runtime, scope and result fields match. The existing replay
runtime is Python 3.9.6 / SymPy 1.14.0; no environment was installed or
modified. These checks supplement, rather than certify, the analytic proof.
Receipts and scripts are retained alongside this report.

## Source, priority and preservation challenge

After the independent conclusion, a separate source-integrity adversary
retrieved the exact primary/archived evidence and checked local/Git hashes.
Its report and reproducible receipts are under `source_integrity/`.

The source target is OWR Open problem 1, printed p.1480, and EJP Open Problem
1.2, printed p.5. Both use alpha outside N without an explicit convention
located by the audit. If N includes zero, the proposition answers the literal
question negatively. If N excludes zero, the zero process supplies a trivial
affirmative exception. The current candidate preserves this boundary and
records only the noninteger negative result. [OWR](https://ems.press/content/serial-article-files/49484),
[EJP primary article](https://pure.uva.nl/ws/files/234720765/Infinite-dimensional_Wishart_processes.pdf).

The exact earlier manuscript at commit
`73dd242a4450400e2f8f16b65929cb77fee76be1` includes this obstruction and its
random-initial extension. Its author field and Zenodo creator are Anonymous;
Git author/committer metadata is a separate fact. The versioned archive
predates the 30 September candidate. The raw manuscript, both ZIP manuscript
copies, both ZIP PDFs, four deposit MD5s and three advertised SHA-256s match.
The manuscript SHA-256 is
`8ac4fe3bf81f4ec70cf17fcd4e3413b13271cf61524dacd7209119a3ae86b184`.
[Exact earlier version](https://github.com/ipitchford/wishart-reachable-noise/blob/73dd242a4450400e2f8f16b65929cb77fee76be1/paper.md),
[version DOI](https://doi.org/10.5281/zenodo.22892681).
This verifies narrow subsumption and earlier public availability, not worldwide
first priority, human refereeing or the earlier broader classification.

All **12 frozen original files** match their actual original Git objects;
all **16 current manifest entries** and **24 family inventory entries** match.
Original changed-path count is 13 including QUEUE.md. Old reviews,
provenance, source record and attempt ledger remain historical and unchanged.
The current-vs-original candidate diff changes source labels, filtration
precision, attribution, zero qualification and acceptance wording; its proof
equations and central argument are unchanged. The new audit independently
checks the current proof rather than transferring an old verdict by hash.

## Mandatory findings, optional clarity and exact gap

**Mandatory mathematical/current-candidate revisions: none.** No scoped proof,
source, computational or integrity gap was identified.

One historical publication-scope error is preserved in frozen pr_input.json:
the original PR body says the shared queue is unchanged, although its diff
contains QUEUE.md. The parent audit acknowledged this and will rewrite the
live PR description before acceptance/merge to include the actual target
queue row, final attribution/zero qualifications and no-paper/no-deposit/no-
tracker disposition. The frozen input must remain unchanged. This is a
publication-packaging obligation, not a theorem defect.

Optional clarity only: the compact candidate could explicitly give the
stopped stochastic-error bound and the trace-rank bound for the Q-drift,
which are already supplied by the independent derivation. Its existing
explanation is sufficient, so expanding it is not required for acceptance.

**Strongest verified result:** every solution under the exact stated
hypotheses forces alpha in N_0 for arbitrary C_0 dynamics, including random
initial values without moments. **Remaining mathematical gap: none found in
this narrow necessity assertion.** General existence, uniqueness, rank and
degenerate-noise classifications and comprehensive historical-priority
certification are outside this result, not transferred dependencies.

All new audit writes are inside final_adversary/, with temporary foreign
downloads and replay scratch ignored. No external individual was contacted;
no canonical or Git mutation, environment installation, paper, deposit or
tracker row was made by this auditor. Final-audit completion: **100%**.
