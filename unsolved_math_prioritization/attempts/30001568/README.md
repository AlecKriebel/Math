# Orbitwise generating-function evaluation: credited finite procedure

**ID 30001568 / OWR-4426-005. Disposition: `already_solved`, 1/5 author turns.**

The independently audited certificate gives a complete finite orbit-representative procedure for a rational binomial-denominator presentation under a finite lattice-affine symmetry group, provided the total is holomorphic at the all-ones point. It applies established Guo–Paycha–Zhang theory. **No mathematical novelty, polynomial-time bound, or practical speedup is claimed.**

Start with [CURRENT_DISPOSITION.md](CURRENT_DISPOSITION.md), the unchanged [applicability certificate](author/APPLICABILITY_CERTIFICATE.md), and the [independent mathematical audit](review/INDEPENDENT_AUDIT.md).

## Implementation and input contract

`author/orbitwise_evaluator.py` implements the **scalar evaluator for one representative**, with rational center and invariant positive-definite metric supplied, plus author diagnostics. Its implementation uses a finite numerator jet, exact partial fractions, and orthogonal polynomial reduction. Orbit multiplicities then weight the resulting scalars.

The broader finite procedures for constructing a fixed center and invariant metric from a promised finite group, computing missing stabilizers or orbit multiplicities, and checking rational-function identities are proved or described in the certificate. The script is not a general group-input command-line front end. Finiteness and validity of the group/orbit input and holomorphy of the total are explicit hypotheses; it does not diagnose an arbitrary genuine pole. Bounded rational-polytope generating functions satisfy the total-holomorphy requirement.

## Reproduce

With Python 3 and SymPy 1.14.0 available, run from this directory or pass the script's absolute path:

    python VERIFY_PUBLIC.py
    python REPLAY_ALL.py

The replay creates its changing outputs in a temporary directory. It does not modify manifest-bound files or use the network. It reruns 32 author diagnostics, all 98 additional independent mathematical/implementation assertions, one author-output comparison, and nine public-subset integrity assertions. The resulting portable independent total is **108**, while the original review had **150** assertions because it also checked every artifact in the larger frozen source collection. These counts are different by design, not missing mathematical tests.

The independent projective-line reference does not invoke the author's partial-fraction or orthogonal-reduction tree. Tests support the audited proof; finite termination and correctness for all valid inputs rest on the proof.

## Provenance and citation correction

The certificate, scalar code, author output, and original source metadata are byte-identical to the reviewed frozen author files. Historical pending-review wording in that certificate is superseded by the current disposition and independent audit. The audit's mathematical sections are preserved in a transparently documented public projection; only environment/coordination wording was removed. The portable review script changes path/output/integrity plumbing, not mathematical tests. See [PUBLIC_PROJECTION.json](PUBLIC_PROJECTION.json).

The [citation erratum](CITATION_ERRATUM.md) corrects the location of GPZ (2023), Example 5.4 to **equation (47)** in the reviewed PDF. The original metadata remains available unchanged; [SOURCE_BINDINGS.json](SOURCE_BINDINGS.json) supplies current public citations and reviewed source hashes. Raw third-party PDFs/full-text extracts and private/procedural records are excluded.

`PUBLIC_MANIFEST.json` binds all public packet files except itself. The only pre-existing repository file changed by this publication is this ID's status and turn cells in `QUEUE.md`; unrelated rows, links, rankings, and audit work are preserved.
