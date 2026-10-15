# Independent adversarial mathematical audit of PR 630

**Verdict: PASS for the exact mathematical claim supplied. Mandatory
mathematical corrections: 0. Optional additions: 1.**

This audit binds all 28 native files to original commit
`810cd5c148bbae7c7c5a47423c375ada98e903b6`, by size, SHA-256, Git blob hash,
and direct equality with the commit's file bytes. Its exact claim is the
failure of the IM replacement with shared a=0 allowed; it does not decide
historical interpretation, source completeness, novelty, or priority. Those
questions belong to the separate source/interpretation review family.

## Exact claim and success criterion

For nonconstant entire f, complex a,b with b!=0, and integer k>=2, the
hypotheses under review are equality of sets `{f=a}={f'=a}` and the pointwise
implication `f'=b => f^(k)=b`. A counterexample must satisfy both globally
over C and fail

    f=d*exp(cz)+((c-1)/c)*a,
    c!=0, d!=0, c^(k-1)=1.

The frozen proof gives such a counterexample for every k>=2, classifies all
polynomial instances, and gives transcendental examples for every k>=3.
All three assertions are verified. The proofs below are deductions from the
stated hypotheses, with no empirical or model assumptions.

## Independent proof and attacks

The full independent derivation was recorded in `INDEPENDENT_DERIVATION.md`
before reading the old audit or its code.

For f=b(z-z0)^k/k!, direct differentiation yields
f'=b(z-z0)^(k-1)/(k-1)! and f^(k)=b identically. Because b!=0, both zero
sets are exactly `{z0}`, with orders k and k-1. This establishes IM and
excludes CM, rather than silently assuming multiplicity equality. The
b-fiber of f' has k-1 distinct points, given by
`(z-z0)^(k-1)=(k-1)!`; the implication is therefore nonvacuous. At a=0 the
proposed conclusion is zero-free, whereas f(z0)=0. This also disposes of any
additive-constant transcription difference that vanishes when a=0. Since
b!=0, every example also satisfies the catalogue's b!=a condition.

For polynomial necessity, let n=deg f. At a!=0 every root of f-a is simple,
since f'=a there. Thus it has n distinct roots, which cannot all be roots
of a nonzero f'-a of degree at most n-1. The identically-zero exception
f'-a=0 is a linear f and has fiber C, whereas f-a has one root; it also
fails. Degree-one functions at a=0 have one zero but a constant nonzero
derivative, and fail. At a=0, if f has r distinct roots of multiplicities
m_j, shared zero sets force m_j>=2 and give all derivative roots, with
total multiplicity sum(m_j-1)=n-r=n-1. Hence r=1 and f=A(z-z0)^n.

An independent divisibility certificate completes the classification: write
x=z-z0. The b-fiber is the squarefree polynomial
`L=x^(n-1)-b/(A*n)`, of degree n-1. If k>n then f^(k)-b=-b, so H2 fails.
For 2<=k<=n, H2 implies L divides f^(k)-b; that polynomial has degree at
most n-2. It must therefore vanish identically. This forces n=k and A*n!=b.
No case is lost through evaluating only real points or selecting a particular
root. The classification is exactly complete over C.

For the transcendental family put t=exp(lambda*z). Direct composition
differentiation, or the diagonal action of lambda*t*d/dt on t^j, gives
`f'=2*lambda*t*(t-1)` and
`f^(k)=lambda^k*(2^k*t^2-2*t)` for f=(t-1)^2. The defining equation
`lambda^(k-1)=-1/(2^(k-1)-2)` has k-1 nonzero complex roots for each k>=3.
With b=-lambda/2, `f'-b=2*lambda*(t-1/2)^2`. Since t ranges over C\{0},
this fiber is infinite and its every point gives
`f^(k)=lambda^k*(2^(k-2)-1)=-lambda/2=b`. Shared zero fibers t=1 have
orders two and one because dt/dz=lambda there. Their infinitely many points
prove transcendence and rule out any nonzero exponential conclusion.

At the b-fiber, f'-b has double zeros, while f^(k)-b has simple zeros: its
derivative with respect to t at 1/2 is lambda^k*(2^k-2)!=0 and dt/dz=lambda/2.
The example therefore fails a hypothetical multiplicity-dominating
b-implication. That stronger assumption is absent from the audited claim;
its failure cannot invalidate the actual setwise implication. At k=2 the
same ansatz gives f''=0 at t=1/2, so it is correctly excluded from the
transcendental proposition.

Constants are excluded explicitly. If allowed, f=K would satisfy H1 at
a=0 exactly for K=0, and at a!=0 exactly for K!=a; H2 would be vacuous for
all constants. Empty fibers and identically full fibers were separately
represented in the controls. If b=0 were allowed, f=z^3,k=2 would satisfy
the zero-value implications and defeat the asserted polynomial
classification; b!=0 is essential. Similarly k=1 would make H2 tautological
and is properly excluded. None of these boundaries is an unmentioned
assumption of the proof.

## Checkable computations and reproduction

`exact_controls.py` imports no original verification code and uses SymPy
1.14.0 with exact symbolic arithmetic and QQ(i), rather than the original
standard-library rational coefficient arrays. The pinned interpreter was
invoked as `/Users/alec/Documents/Math/draft_pr_claimed_solved_600_700_20261012/tooling/math-venv/bin/python`
without resolving its symlink. `run_review.py` records commands and raw
output hashes in `TEST_RESULTS.json`; all output is retained in `results/`.

Independent checks passed identically under normal and optimized Python:

* Symbolic complex b,z0 family identities for k=2,...,14 and squarefree
  nonempty b-fiber certificates.
* 240 exact Gaussian-coefficient polynomials of degrees 1,...,4: six
  H1 pairs, 150 H2 checks, and three admissible cases, all classified.
* 756 checks with non-real scales and translations: 42 positive and 714
  rejected coefficient/order cases, including k above degree.
* Fifteen constant and linear cases, identity/empty-fiber sentinels, the
  b=0 boundary, multiplicity checks, and invalid additive-shift repair.
* Direct symbolic derivatives and reduction modulo the defining lambda
  polynomial for all k=3,...,45, plus lambda=1, k=2, and multiplicity
  strengthening negative controls.

Wrong factorial and wrong sign in the lambda relation were independently
injected. Both faults failed in both normal and optimized Python; these
checks use explicit exceptions, which optimization cannot remove.

After inspection, all five supplied verifiers passed their intended normal
invocations. The author and old independent control output reproduced the
frozen JSON byte-for-byte. The release verifier passed exact native/archive
integrity, both manifests, and fresh archive-only replay. It rejected
optimized Python as documented. A deliberately corrupted stand-alone author
quadratic test failed normally and false-passed under optimization, confirming
why the documented release entry point guards that mode. This is already
disclosed and guarded in the frozen wrapper and README; no correction is
required. The `-O` false pass is not counted as successful verification.

These computations corroborate exact algebra and detect implementation
faults. The finite ranges do not replace the universal proofs above.

## Optional addition O1: arbitrary prescribed b

The root reviewer proposed a routine scaling, independently checked and
recorded in `ROOT_PROPOSED_SCALING_COROLLARY.md`: choose the same lambda,
let A=-2b/lambda, and take f=A(exp(lambda*(z-z0))-1)^2. For every prescribed
b!=0 and z0 in C, A!=0,
`f'-b=2*A*lambda*(t-1/2)^2`, and the kth derivative there is
`-A*lambda/2=b`. All IM, nonvacuity, transcendence, and failure-of-conclusion
arguments persist. Symbolic factorization and value controls also pass.
This can be added as a routine corollary if useful; it is optional and
carries no historical novelty claim.

## Exact remaining gap

No mathematical gap remains in the three frozen propositions under the
precisely supplied hypotheses. The work does not decide the strengthened
nonzero-a transcendental problem, the existence of transcendental k=2
counterexamples, or an entire-function classification; none is claimed.
Historical intended scope, novelty, source completeness, and priority are
not resolved by this audit. No paper, closure recommendation, Git mutation,
remote write, or outside communication was made.
