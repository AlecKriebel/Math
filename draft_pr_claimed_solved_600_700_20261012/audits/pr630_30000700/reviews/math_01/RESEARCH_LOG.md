# Mathematical adversarial audit log

## 2026-10-15T03:45:38Z — checkpoint, 25%

Bound the task to PR 630, original head
`810cd5c148bbae7c7c5a47423c375ada98e903b6`, and the 28 immutable native
files listed in `SCOPE_AND_SNAPSHOT.json`. Read only that scope and the
mathematical proof before deriving the main claims independently.

The direct family passes symbolic scrutiny. A separate polynomial
classification uses squarefree divisibility and degree, rather than the
supplied proof's roots-of-unity step. The exponential family reduces to an
Euler-operator identity and one exact algebraic equation in lambda. Next:
adversarial exact computation, exception branches, input binding, then
inspection and reproduction of the supplied controls. No outside contact,
Git mutation, or remote write is authorized in this audit shard.

## 2026-10-15T03:49:26Z — checkpoint, 80%

Verified every one of the 28 native files by byte count, SHA-256, Git blob
identifier, and bytes at pinned commit `810cd5c148bbae7c7c5a47423c375ada98e903b6`.
Inspected all five supplied Python verifiers before executing them. Author
controls, old independent controls, both manifest checks, and the release
wrapper pass, including clean archive extraction/replay. The two saved
control reports reproduce byte-for-byte. Optimized release execution is
correctly rejected. Deliberately incorrect factorial and lambda-relation
controls are rejected under both normal and optimized Python by the new
explicit exception checks. The full independent normal/optimized passes are
finishing; the first completed full pass has no failure.

After the initial independent derivation, read the old audit and confirmed
that its logical scope matches the supplied proof. No mathematical correction
has emerged. Distinct control coverage includes exact Gaussian coefficients,
non-real translations and scales, polynomial support computations via a CAS,
direct symbolic composition differentiation, and algebraic reduction modulo
the defining lambda equation. Constant and linear branches and the excluded
b=0 boundary were explicitly checked.

The root reviewer's optional arbitrary-b scaling is valid, as recorded in
`ROOT_PROPOSED_SCALING_COROLLARY.md`; it is a routine corollary of the frozen
transcendental family. This is not a priority claim or a native-input change.

## 2026-10-15T03:50:04Z — checkpoint, 100%

All substantive checks passed. The independent normal and optimized reports
are byte-identical; both deliberately injected faults are rejected in both
modes. Twelve scripted executions have the expected success/failure status;
the additional mutated-author experiment confirms the release wrapper's
documented need to reject optimized assertion-based scripts. No repeated
testing is needed after this checkpoint.

Final mathematical verdict: PASS with exact scope, zero mandatory corrections,
one optional routine arbitrary-b scaling corollary. `FINDINGS.md`,
`INPUT_BINDINGS.json`, `TEST_RESULTS.json`, the independent derivation, the
two executable review scripts, raw control outputs, and `VERDICT.json` form
the checkable deliverable. No gap remains in the frozen propositions under
their supplied statement. The strengthened nonzero-a question and historical
interpretation/priority remain outside what this mathematical work resolves.
