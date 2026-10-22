# A fixed birational map without a prime-field cycle-distribution limit

Alec Kriebel, independent researcher. ORCID: https://orcid.org/0009-0001-9320-500X
Version 1.0, 21 October 2026 UTC. Unrefereed preprint.

The paper gives the exact application for L(u,v)=(u,(u^2+1)v), at primes p = 3 (mod 4),
with point-weighted period threshold px. It credits the established triangular
family, primitive-value estimate, shifted-prime totient mean and continuous
scalar law. It proves the interval CDF failure, explicit subsequences and failure
of weak convergence on every further positive-upper-density prime subset of the
admissible class. Its exact hypotheses and boundaries are in paper/main.tex.

Run `python3 -B verify.py` from this extracted directory, using Python 3.9 or later.
The verifier writes no files, checks every payload's length/SHA256 and the exact
file set, rejects symlinks, and recomputes the deterministic exact finite result
in expected_checks.json. The new checker uses only Python's standard library.
`python3 -O -B verify.py` also executes every check; its guards do not use assert.
The expected result has 147,619 exact checks over 87 admissible primes through 1000,
eight raw affine orbit graphs containing 6,088 points, six bad-prime controls and
the elementary totient lower bound through 10,000. These are finite diagnostics,
not proofs of the infinite-prime statements or of atomlessness.

Build paper/main.tex with a standard LaTeX distribution that supplies the listed
packages (for example Tectonic 0.17.0, or a compatible XeLaTeX installation).
Two passes may be needed for references. The released PDF is supplied separately.
Ordinary compiler/platform PDF byte differences are not mathematical differences.

The original/ directory preserves all 17 research files byte for byte from commit
091bdecef6f84154f5d5c205a4b07eeb6391b8f8; SOURCE_SNAPSHOT.json binds them.
The original SymPy-dependent scripts are historical artifacts. They were not
successfully replayed during this preparation because the available default and
bundled runtimes lack SymPy. No installation is needed for the new verifier.

historical_reviews/ preserves the completed mathematical/source audit family
artifacts and their original manifests. Their earlier run receipts report
8,347,742 finite assertions and 230,780 analytic controls. These are separate
historical runs, not the new 147,619-check replay. Older reports may state that
priority was unresolved or only prove weaker selection quantifiers. They are
dated evidence of the work then performed; the present paper expressly proves
the positive-upper-density claim using the credited classical scalar law.
No old receipt is retroactively rewritten as current clearance.

SOURCE_REFERENCES.json gives primary URLs, exact downloaded PDF hashes and
declared reading scopes. Full third-party source bodies, private account records,
credentials and ledger bodies are not included. PRIORITY_SCOPE.md documents the
bounded historical conclusion and unrecovered 2011 source. No worldwide novelty,
current-open or first-resolution claim is made.

AI systems were extensively involved in research, model/proof development,
computation, literature search, writing and adversarial auditing. The author is
responsible for the claims. The work has not undergone formal independent human
peer review. Internal AI audits are not human peer review.

MANIFEST.json covers the exact payload set and deliberately excludes itself;
the separately bound ZIP hash supplies the external archive identity. The
manifest is an integrity record, not a digital signature. Authored package
content is offered under CC-BY-4.0; quoted/cited third-party works retain their
own rights and are not redistributed here.
