# Grassmann affine-SOS: an existential negative reduction

Problem 30002816 / OWR-13498-004. Accepted in an independent AI-assisted mathematical audit; two of five proof routes used. No novelty, conventional human peer-review or journal-acceptance claim.

The full original conjecture fails at (k,n)=(4,12). The argument proves that the oriented Grassmann orbitope C(4,12) has no finite projected semidefinite lift by identifying a two-hyperplane section with the separable-state body Sep(3,3). Fawzi's published theorem excludes any finite lift of that body. A universal affine-linear SOS certificate property would force a compact size-496 moment lift with trace 2, a contradiction.

The counterexample is existential: a failing linear functional exists with rational coefficients before comass normalization. No explicit bad-calibration coefficients, exact comass, minimal dimension or lower-dimensional classification are supplied.

## Read the mathematics

- current/PROOF.md: the complete proof, with status-only publication edits
- current/AUDIT_REPORT.md: the complete mathematical audit, with one provenance-only privacy redaction
- current/STATUS_PATCH.patch: exact contextual status changes; reversing it reconstructs the pinned source proof
- current/PUBLICATION_EDITS.md: scope of edits and exact preservation guarantees
- current/PRIORITY_REPORT.md and current/SEARCH_LIMITS.md: bounded literature outcome and limitations
- ACCEPTANCE.md and ACCEPTANCE.json: acceptance scope and exclusions

## Attribution and nearby results

The proof is a reduction to established mathematics, with no claim that its component constructions are new.

- Fawzi, *The set of separable states has no finite semidefinite representation except in dimension 3×2*, CMP 386 (2021), Theorem 1, supplies the arbitrary-finite-lift obstruction for Sep(3,3). [Published article](https://doi.org/10.1007/s00220-021-04163-2)
- The Kähler equality locus and real-(p,p)/Hermitian correspondence are classical; the delivered literature report cites the relevant original question and a modern positive-form formulation.
- Schliemann, Cirac, Kuś, Lewenstein and Loss (2001) already define the convex body of mixtures of elementary Slater determinants used as the intermediate body. [Published article](https://doi.org/10.1103/PhysRevA.64.022303)
- Paul, Zhao and Dai, *Learning the closest Slater determinant*, arXiv:2607.20623v1, Appendix A.2, pp.16–17, equations (A17)–(A32), use the same opposite-spin product-to-wedge isometry and a closely related positive-observable support-function/fidelity equality. The inspected source does not state the complete Grassmann no-lift/calibration conclusion. [Primary preprint](https://arxiv.org/abs/2607.20623v1)
- Bettiol–Kummer–Mendes, Corollary 4.2 and Remark 4.3, treat nonnegative quadratics in the representation Sym²(Λ^k R^n). That no-shadow theorem differs from the current oriented degree-one Plücker body. [Revised primary preprint](https://arxiv.org/abs/1908.03713v2)

The bounded search found no exact matching or contradictory primary theorem. This does not establish priority or novelty.

## Reproduce the sealed exact checks

Requirements: Linux, Python 3.12, standard library, actual UID/EUID 1000. No SymPy, source downloads, third-party source bodies, network access or external solver is needed. The original author generator writes outputs and is deliberately not used by the sealed replay.

First authenticate the SHA-256 of BOOTSTRAP.py against an independently obtained review/PR record. Copy that authenticated file outside the packet. Keep the copy fixed and read-only. Give packet directories mode 0555 and all packet files mode 0444, with no symbolic or hard links. The verifier tests actual append, create and unlink denials; merely setting a logical read-only flag is insufficient.

Run the externally fixed bootstrap against the packet in each mode:

    python3 -I -S -B /trusted/BOOTSTRAP.py /path/to/packet
    python3 -I -S -B -O /trusted/BOOTSTRAP.py /path/to/packet
    python3 -I -S -B -OO /trusted/BOOTSTRAP.py /path/to/packet

Run its publication controls by inserting --controls before the packet path. The complete exact finite suite is nested in each replay. The preserved independent checker reads the immutable exact embedding certificate and writes only stdout. Temporary certificate mutations are stored outside the sealed packet.

Per mode, the finite suite performs one positive independent run, six actual coordinate-matrix mutations and nine certificate/schema mutations. The six matrix changes test orientation sign, the quarter factor, imaginary conjugation, a removed real off-diagonal column, a corrupted pure diagonal, and a corrupted mixed diagonal. All fifteen mutations must produce exactly their intended rejection output and exit code. The positive run must verify 225 columns, rank 225, Gram multiplicities 15/210, all 495 projector coordinates, 11760 polynomial terms in 24 variables, and nine mixed minors.

The publication controls separately test every delivered file, missing/extra/linked/special members, fixed-bootstrap resealing attacks, malformed JSON, acceptance/status changes, full-output comparator attacks and hostile import environments. A relocated actual-diff replay checks the complete raw baseline again in normal, -O and -OO modes. All before/after snapshots must agree.

## Trust structure and limits

PUBLICATION_MANIFEST.json inventories every payload member, including code and all six raw reference streams, except itself and BOOTSTRAP.py. The independently fixed bootstrap pins that manifest and the verifier/control code. The verifier enforces the exact whole-delivery allowlist. No self-hash or self-dependent final execution receipt is used. External receipts pin the whole delivery and live outside the delivered inventory.

Reference stdout/stderr are full streams, not filtered PASS markers. The verifier compares their externally authenticated mode-specific identities, exact bytes, and recursively exact JSON types and values. Rejection identities, reasons, counts, categories, optimization mode and nested raw checker output are part of the comparison. Empty stderr reference files are intentional. There is no output normalization.

All mathematical statements depend on the complete proof and its named published theorem. Exact finite algebra supports the coordinate bridge; it is not a formal proof-assistant verification. Original author regeneration, the original audit harness, source-body replay, dataset replay and a new proof of Fawzi's theorem are explicitly NOT_RUN in this delivery. The historical audit documents its own earlier executions.

Only authored mathematics/audits/acceptance and public scholarly verification metadata are delivered. Source documents, dataset contents, private sources, private coordination and identifying metadata for excluded private files are omitted. No QUEUE or unrelated repository path is changed.
