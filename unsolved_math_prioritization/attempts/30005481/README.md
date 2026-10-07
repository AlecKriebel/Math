# Hook-shaped operator extendability: audited partial results

Problem **30005481 / OWR-12697711-017**, queue rank 951. Publication record:
7 October 2026. **Unsolved, 5/5 substantive approaches used.**

The full equivalence between diagonal extendability and weak SOS-hyperbolicity
remains unresolved. This packet preserves the complete authored partial proofs,
independent mathematical audit, exact certificates and verification code.
Acceptance is limited to the results below. It is not a novelty claim, human
peer-review claim, formal proof-assistant certification, or full solution.

## Read first

- [Corrected proof reading copy](independent_audit/corrected/PARTIAL_THEOREMS.md)
- [Complete independent audit](independent_audit/AUDIT.md)
- [Current acceptance and conventions](PUBLICATION_ACCEPTANCE.md)
- [Source/readiness history](authored/SOURCE_AND_READINESS.md)

The only correction changes “A scalar multiple” to “A **nonzero** scalar
multiple” in the opening conventions. The original proof and all frozen author
files remain unchanged under `authored/`. The separate corrected reading copy,
exact patch, and before/after identities are under `independent_audit/`.

## Accepted scope

1. An inverse-symbol critical-value criterion for extendability, with its stated
   simple-root hypotheses, and the repeated-root obstruction for the base quintic.
2. Quadratic cases and weak-SOS product closure, without claiming arbitrary
   hook-shape preservation or extension closure for products.
3. The shifted penultimate elementary family, with a definite determinantal
   representation, a shifted-diagonal extension, and all-cone-pair SOS certificates.
4. Two exact rational Gram certificates for restrictions of a quintic Wronskian.
   These are SOS slices, not certificates for the full five-variable Wronskian
   and not a proof of weak SOS-hyperbolicity.
5. For the cited hyperbolic quintic p and p_epsilon = p + epsilon(e_1/5)D_e p,
   epsilon >= 0, extendability holds exactly for epsilon >= epsilon_*, where

       167620 epsilon_*^3 - 8871 epsilon_*^2 + 2820 epsilon_* - 752 = 0.

   There is exactly one positive root, approximately 0.146702017518328. Equality
   is included. The weak-SOS boundary for this family remains unknown.

The published nonextendable quintic is not a counterexample to the equivalence.
The source's computational full-space non-SOS result and base hyperbolicity
theorem are cited inputs; their original full-space computational certificates
are not reconstructed here.

## Portable verification

Requirements: Python 3, SymPy 1.14.0 and mpmath 1.3.0. A suitable environment can
be prepared from `requirements.txt`. The verifier itself needs no network, source
paper, dataset, optimizer, or private file.

From any working directory:

    python3 -B /path/to/30005481/verify_publication.py --selftest

The wrapper checks the exact 20-file package inventory, byte counts, SHA-256 and
Git blob hashes, pinned original/audit manifests, the sole wording replacement,
and its unified patch. It then reruns both unchanged exact verifiers and compares
their output byte-for-byte with the saved records. Expected scoped controls:
206 author assertions and 46 independently implemented checks. Nine optional
mutation controls exercise the packaging validator. The universal proofs are
written arguments; finite checks are supporting evidence, not proof strength
scores or a formalization of those arguments.

`--integrity-only` omits the mathematical replay. `--selftest` also works under
`python3 -O`; the wrapper uses explicit failures, and child processes run with
optimization disabled. Temporary copies are used for mutation controls. No
published file is modified by verification.

Use a trusted repository commit or independently obtained publication-manifest
hash as the integrity anchor. A hash inventory is not a cryptographic signature;
it cannot authenticate a package if both its files and all trust anchors are
maliciously replaced.

## Provenance and boundaries

Frozen phrases such as “independent review not yet performed” and “no repository
publication or queue edit” describe the earlier author/audit stages. They are
preserved as history; this publication record and the acceptance report state
the later accepted partial-result disposition. Source-inspection descriptions
retain their original scopes and limitations; replay does not re-inspect sources.

Primary source: Blekherman, Lindberg and Shu, *Symmetric Hyperbolic Polynomials*,
Journal of Pure and Applied Algebra 229(2), 107869 (2025),
[DOI 10.1016/j.jpaa.2025.107869](https://doi.org/10.1016/j.jpaa.2025.107869).
The published source retains Conjecture 2.3. The source's diagonality convention
is degree-shifted, as spelled out in the acceptance report and full audit.

The publication adds only this packet and the target row's Status, Turns and
Findings updates in the existing queue. All other queue bytes, including existing
Chat/DOI links and header text, are preserved. No queue regeneration is used.
No copied third-party PDF, source extract, dataset contents, private source,
personal data, or private coordination material is included. Draft PR only;
no merge, release, new DOI or outreach is part of this publication.
