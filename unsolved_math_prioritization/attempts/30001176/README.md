# A canonical-filtration counterexample with prescribed singleton algebras

Problem 30001176 / OWR-3392-002, rank 823. Publication checkpoint: 6 October 2026.

**Accepted scoped result; original target remains unsolved here, 1/5 substantive approaches used.**

The authored infinite construction gives a minimal, ordinary-permutation exchangeable, tail-trivial sequence in a faithful tracial von Neumann algebra with separable predual. Its canonical algebras satisfy

    dim(A_{0,1} intersect A_{0,2}) = 8 > 4 = dim(A_{0}).

Thus the canonical filtration fails the meet axiom, and the binary join axiom rules out every factorization that preserves the prescribed singleton image algebras. No mandatory mathematical correction was found in the independent audit.

The limitation is essential: enlarging each singleton to dimension eight gives a valid permutation-covariant factorization. The historical source's phrase “gives rise” does not explicitly require singleton preservation. This package therefore excludes arbitrary/existential enlargement from its negative conclusion and does not claim an unqualified resolution of Conjecture 5. It makes no claim about the current literature-wide status of that broader formulation.

Conjecture 5 has no ambient-factor hypothesis; the hypothesis in the separate Question 3 must not be imported. Ordinary exchangeability must not be replaced by CAR or quantum-permutation symmetry.

## Read in this order

1. [Publication verdict](VERDICT.json), which governs the accepted scope and original-target status.
2. [Infinite proof](author/PROOF.md).
3. [Independent audit](audit/AUDIT.md) and [expanded operator-algebra details](audit/INDEPENDENT_LEMMAS.md).
4. [Source metadata](author/SOURCE_PROVENANCE.json), [independent source checks](audit/SOURCE_AUDIT.json), and [publication metadata](PUBLICATION_METADATA.json).

The original author and audit archives and every extracted member are preserved byte-for-byte. The author's dated candidate-claim and pending-review language describe that historical checkpoint; they are not the publication disposition. The audit is AI-assisted, not human peer review or formal proof certification. No historical novelty or exhaustive literature-search claim is made.

## Reproduce

Python 3.10 or newer, standard library only, no network required:

    python3 -B /path/to/30001176/verify_publication.py
    python3 -B -O /path/to/30001176/verify_publication.py
    python3 -B /path/to/30001176/test_publication.py

Run output must be redirected outside this directory. The wrapper checks the complete file/directory inventory, sizes and hashes, original ZIP trust anchors, ZIP member inventories and member byte equality before executing the preserved verifiers. It replays 2,900,842 author finite checks and 303,279 independent finite checks. Finite diagnostics and integrity checks supplement the written infinite proof; they do not certify it.

The frozen author harness exercises eight mutation classes in normal and optimized modes. The frozen audit harness rejects 26 runs of 13 mutation types. Its actual Unix socket fixture was environment-denied and is recorded as ENV_DENIED_NOT_RUN, never as a passing socket test. `PACKAGE_REPLAY.json` records the publication replay outcomes. External source and corpus inspections are preserved historical evidence, not portable replay steps; no fresh source checks are claimed here.

The publication manifest's digest and wrapper digest must be checked against an external publication receipt. Replacing a package together with all external trust anchors is outside the integrity threat model.

Only the target queue row's Status and Turns change. Findings and all other queue bytes are preserved. No merge, release, DOI, or outside communication is part of this checkpoint.

## Primary source

Claus Köstler, “Noncommutative Factorizations,” in Oberwolfach Report 09/2009, pp. 521–523, Definition 1 and Conjecture 5. [Official report](https://ems.press/content/serial-article-files/46209), [DOI](https://doi.org/10.4171/owr/2009/09). The cited canonical-filtration definition is [Definition 1.6 of the de Finetti preprint](https://arxiv.org/abs/0806.3621).
