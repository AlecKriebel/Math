# Growth-input correction for the independent audit

Target: 30000707 / OWR-1460-014. The original historical freeze is retained
privately and unchanged. This correction is a condition of audit acceptance.
The public projection has its own safe-only manifest.

## Issue

PROOF.md section 2 establishes a two-sided bound for
T(r)=max(T(r,f),T(r,g)) and then asserts the exact order of the functions
individually. Its rationality sentence directly excludes only the case
where both functions are rational. The missing explicit dependency is
standard and already present in the cited Steinmetz source.

## Precise citation and hypotheses

Norbert Steinmetz, [Reminiscence Of An Open Problem](https://arxiv.org/abs/1102.3383v1),
section 1, printed page 2, the q=4 part of the Five-Value-Theorem,
formula (Na), gives

T(r,f)=T(r)+S_f(r),  T(r,g)=T(r)+S_g(r),

where the usual remainders are O(log(rT(r))) outside sets of finite
linear measure. The hypotheses are distinct meromorphic functions
sharing four distinct values ignoring multiplicities. There is no
finite-order hypothesis, no requirement for the finite values to be
CM, and no exclusion of infinity. The source's infinity footnote
modifies formula (Nc), not (Na). Thus (Na) applies to the exact target.
The formula and its surrounding hypotheses were rechecked in both the
private PDF text and the pixels of printed page 2.

## Explicit justification

If f and g were both rational, their ratio Φ=ψ1/ψ2 would be rational,
contrary to Φ=exp(2z^d). Thus at least one is transcendental. The
standard characteristic criterion for rationality gives
T(r)/log r→infinity, so O(log(rT(r)))=o(T(r)). Formula (Na) therefore
gives T(r,f)/T(r)→1 and T(r,g)/T(r)→1 away from a common
finite-linear-measure exceptional set. Either function being rational
would have characteristic O(log r), a contradiction. This rules out
the mixed rational/transcendental case as well as the all-rational case.

In the non-CM branch, the existing section 6 estimate and
T(r,Φ)=2r^d/π imply T(r) comparable to r^d off the exceptional set.
Consequently each of T(r,f) and T(r,g) is comparable to r^d there.
For all sufficiently large r, choose a good point in [r,r+1] for an
upper bound and one in [r−1,r] for a lower bound. Such points exist
because the tail measure of the union of exceptional sets is less
than one. Monotonicity of each characteristic now yields the two-sided
individual bounds for every sufficiently large r. Both individual
orders are therefore exactly d. The CM branch is handled by the
unchanged complete classification in section 3.

## Implemented changes

The corrected bundle makes exactly these changes to the original files:

1. PROOF.md section 2 explicitly cites and states (Na), proves the
   common remainder is small, and excludes mixed rationality before
   applying the section 6 growth estimate.
2. PROOF.md section 2 explicitly transfers the maximum bound to each
   individual characteristic and extends both bounds across the
   exceptional set. Its earlier abbreviated rationality sentence is
   removed.
3. SOURCE_STATUS.md records the audit's additional section 1 page 2
   dependency check. No historical source-check claim is erased.

The control files, all other mathematical propositions, the five-turn
research record, and the unresolved gap are unchanged. AUDIT.md and
this correction ledger are additional files. The original freeze and
the corrected bundle have separate manifests and must not be conflated.
