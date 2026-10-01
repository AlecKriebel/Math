# PR13 exact-reproduction family research log

Scope: independent frozen-head replay and defining-presentation checks for
problem 11000263, frozen head `7a845f7e025a24affe1b712cf7ada648570f9c64`.
Only this family's artifacts and isolated ignored scratch are written. Historical
`REVIEW.md`, `verdict.json`, and sibling conclusions are excluded before this
family's conclusion. No external person is contacted.

## 2026-10-01T13:32:40Z — Initial checkpoint (15% complete)

- Read defining presentation in `AUDIT.md`, frozen verifier scripts, and their
  stored output receipts. Did not read historical review/verdict.
- Exact claim under audit: over F=Q(q), X3 is nonzero in both repaired
  presentations A_n=F B_n/(R2,...,R_(n-1)) and
  C_n=F B_(n+1)/(R2,...,Rn), n>=3. The literal printed terminal row is ill-typed.
- Proposed independent mechanism: formal Laurent-polynomial sparse-vector
  action, explicit inverse blocks and reversed inverse words; exact local
  support calculation establishes the all-index induction rather than
  extrapolating a finite test.
- All seven team slots are occupied; no child agent was spawned.

## Scalar conclusion before reading SCALAR_SCOPE_CHECK.md

Over an extension of Q(q), every one-dimensional braid representation on at
least three strands sends all generators to the same invertible z (the scalar
braid relation and invertibility imply equality). Write
X2=(1-z)(z+q)/z and X3=(q^2-z^4)X2/z^2. R2 has coefficient
(z^2-q)(z^2-z+1)/z^2. Nonzero X3 rules out z^2=q, leaving z^2-z+1=0.
For three strands no R3 is legal, so primitive sixth roots give scalar witnesses
in a suitable algebraic extension. For four or more strands, R3 has coefficient
(z-1)(q^2+z^5)/z^3; since z is algebraic over Q, this cannot vanish when q is
transcendental. Thus the scalar mechanism fails generically for A_n with n>=4
and for every C_n with n>=3. This does not affect a higher-dimensional witness.

Specializing q requires further care: at z^2-z+1=0, R3 forces q=+-z;
q=-z kills X2, whereas q=z retains X3 on four strands. On five or more strands,
q=z makes X4 nonzero and R4 fails. These are bounded scalar controls, not a
claim about arbitrary-dimensional representations.

## 2026-10-01T13:40:00Z — Independent conclusion checkpoint (85% complete)

- Both frozen scripts replayed successfully in isolated ignored scratch. Stored
  and fresh JSON receipts match byte-for-byte; their SHA-256 hashes match.
  All five replay input hashes are unchanged after execution.
- The different-mechanism Laurent sparse-vector checker passed 5,976 labeled checks,
  including all legal rows on m=3,...,12 and 160 exact parameter cases.
- Deliberately incorrect inverse order is rejected by both a round-trip check
  and exceptional relation R2, establishing a meaningful control.
- Independently verified arbitrary-index mechanism: homogeneous translated
  three-coordinate action followed by disjoint-support fixation; induction
  establishes all Xk images and all legal Rk, not just bounded tested indices.
- Generic X3 entry is -u+q+q^2-q^3/u; coefficient -1 at u proves nonvanishing.
  Scalar n=3/n=4 distinctions and inadmissible u=0 boundary are recorded.
- Own conclusion: PASS for the two scoped repaired F=Q(q) claims, with no
  blocking inconsistency. REPORT.md records assumptions and exact coverage.
- Next: compare SCALAR_SCOPE_CHECK only after this recorded conclusion, produce
  final verdict and hash manifest. Historical REVIEW/verdict stay unread.

## 2026-10-01T13:41:56Z — Post-conclusion comparison (95% complete)

- Read SCALAR_SCOPE_CHECK.md only after the independently recorded conclusion.
  Its generic and exceptional scalar-case claims agree with the independently
  factored expressions and exact primitive-sixth-root reductions.
- Read the stored exact verifier_rerun.json (not historical review/verdict):
  its verifier SHA-256 and 42-case/1,590-check data agree with the new replay.
- Confirmed scratch execution paths are ignored by Git. Environment unchanged;
  no Git mutation, canonical-file mutation, or external outreach performed.

## 2026-10-01T13:44:23.415688+00:00 — Final checkpoint (100% complete)

- Scoped repaired-presentation claim passes the family adversary.
- All required replay, independent exact, all-index, scalar, singular, base-ring, and coverage checks are recorded.
- Machine-readable verdict and artifact SHA-256 manifest finalized; historical review/verdict and siblings remain unread.

## 2026-10-01T13:45:35.131362+00:00 — Final checkpoint (100% complete)

- Scoped repaired-presentation claim passes the family adversary.
- All required replay, independent exact, all-index, scalar, singular, base-ring, and coverage checks are recorded.
- Machine-readable verdict and artifact SHA-256 manifest finalized; historical review/verdict and siblings remain unread.
