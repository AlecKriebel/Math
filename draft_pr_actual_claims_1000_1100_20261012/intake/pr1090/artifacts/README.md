# Strong expansions: a global spectral partial

Problem 20000886 / AIM-COMBINATORICS-0011, AIM Problem 3.2, rank 1271. Accepted scoped partial, substantive attempt 1 of 5. Novelty confidence is low and unconfirmed.

## Established mathematics

For a bounded symmetric nonnegative r-kernel W, let U be its pair marginal. If U has constant degree p>0, normalize its integral operator by p and set B=sum over negative eigenvalues of |lambda|^4. The complete [mathematical report](MATHEMATICAL_REPORT.md) proves

  B <= r-2  implies  t_C4(U)t_C5(U) >= p^9.

By integrating the distinct private leaves, this is exactly the Sidorenko inequality for the strong expansion of C4 disjoint-union C5 on this host class. W need not be close to a constant. The proof includes the p=0 case, infinite-rank trace justification, repeated positive eigenvalues, and a generalized even/odd-cycle inequality.

Consequences include:

- At r=3, every regular pair marginal with at most 16 negative eigenvalues is safe; in particular every regular step marginal on at most 17 parts is safe.
- The arbitrary-rank L2 criterion gives a dense-host exclusion for [0,1]-valued W: p>=1/[1+(r-2)(r-1)^2], hence p>=1/5 when r=3. Constant pair degree is still required.
- For the balanced binary ray U_theta=1-theta f(x)f(y), bounded nonnegative symmetric r-lifts exist exactly up to theta=1/(r-1) for even r and theta=1/r for odd r. The entire liftable ray and its finite tensor products satisfy the compensated inequality.
- The r-liftable pair-marginal cone is tensor-closed but fails normalized-principal-restriction closure for every r>=3. The report gives an explicit complete-r-partite construction, so a regularization theorem requiring both closures cannot be imported directly.
- An explicit irregular five-cell lift violates the regular normalized spectral lower bound while respecting the weighted covariance inequality.

## Scope and credit

The test core C4 disjoint-union C5 is genuinely non-Sidorenko. This work does not exhibit a Sidorenko expansion of a non-Sidorenko core and does not prove the universal converse. Irregular marginals and unrestricted regular marginals beyond the sufficient budget remain untreated. Budget failure is not evidence of a counterexample.

Spiro's disconnected-compensation strategy is expressly prior. The covariance, finite-exchangeability and spectral ingredients are standard. Public citations and recorded source identities appear in [SOURCE_METADATA.json](SOURCE_METADATA.json). The report and audit retain the full arguments explaining why Lee's nested-link criterion and Zhao's stated class hypotheses do not directly resolve this target.

## Review and distribution

The [independent mathematical audit](MATHEMATICAL_AUDIT.md) accepts the scoped analytic results. This AI-assisted, unrefereed edition is not external human peer review, journal acceptance, proof-assistant certification or novelty certification. Supporting verification totals are audit metadata only. Edition preparation claims no fresh scholarly retrieval, source-file rehash, source inspection, literature search or mathematical-program execution.

[STATUS.json](STATUS.json) records the accepted partial and exact remaining gaps. [MANIFEST.json](MANIFEST.json) lists all six members and hashes the other five; the pull-request body independently pins the manifest. Hashes establish packaging integrity, not mathematical correctness.

Programs, checker outputs, fixtures, datasets, optimizer logs, copied source bodies and private coordination are excluded. The numerical-exploration subsection is removed completely. No excluded computational output is recast as proof. This addition-only edition leaves QUEUE.md and unrelated entries unchanged; it adds no substantive proof turn and does not reset attempt accounting.
