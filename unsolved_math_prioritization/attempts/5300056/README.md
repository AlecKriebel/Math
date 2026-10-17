# Bounded Jacobian cocycles: scoped partials (5300056)

**General target: UNSOLVED in this investigation. Five of five substantive routes used. No new solution, holomorphic counterexample, or novelty credit is claimed.**

Start with `author_v2/PROOF.md` and `delta_acceptance/ACCEPTANCE.md`. The classical L2 coboundary equivalence includes noninvertible probability-preserving maps. The exponential density is e^(-u); the resulting equivalent measure is only guaranteed sigma-finite, and its branch Jacobian retains e^a times |Df|^kappa. Finiteness and an all-small-scales geometric comparison are additional hypotheses, not conclusions of the original general assumption. The binary-shift and Moran constructions refute abstract shortcuts only; neither is a holomorphic counterexample.

## Which version governs

The latest bounded-delta acceptance governs the corrected v2 proof. It accepts exactly three required covering-proof replacements: allow zero-diameter cover members, restrict ball containment to positive-diameter members, and discard countably many singleton members using their zero measure. Singleton sets are not replaced by positive-diameter balls, which need not exist at isolated points.

The immutable `author_v1/`, `independent_audit/`, `author_v2/`, and `delta_acceptance/` directories reproduce all four separately preserved ZIP archives in `archives/`. Original unaudited, correction-pending, acceptance-pending, and no-remote-write labels are historical statements at those freezes; they have deliberately not been rewritten. `delta_acceptance/FULL_DELTA.patch` records all changed and added v2 payload members. Seven original members, including all code and arithmetic results, remain byte-identical.

## Replay

Use Python 3 with its standard library. Run from any working directory:

    python3 -B /path/to/5300056/verify_publication.py --expected-manifest-sha256 PIN

Replace PIN with the external SHA-256 of `PUBLICATION_MANIFEST.json` recorded in the draft PR. The verifier authenticates a closed recursive inventory, exact ZIP bytes and expanded members before executing the included manifests, original independent audit, and complete bounded-delta replay. Python optimization is also supported. `test_publication_integrity.py` checks rejection of altered or unexpected input.

Portable replay includes 21,193 original finite checks and 20,371 independent finite checks. It does not mechanically certify infinite-dimensional analysis, measure-theoretic limits, source validity, or the general holomorphic implication. Source-complete provenance is opt-in through `independent_audit/verify_provenance.py`; omitted source bytes are not revalidated by portable replay.

Only authored proof notes, code, audit outputs, immutable safe archives, and public verification metadata are distributed. Source PDFs, source extracts, images, raw corpora, and private coordination are excluded. Queue changes are limited to this row's Status and Turns; every other queue byte, including its preexisting stale header, is preserved.
