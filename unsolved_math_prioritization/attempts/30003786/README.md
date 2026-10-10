# Embedding dependence of congruence subgroups

**Problem:** 30003786 / OWR-16160-016, rank 440.  
**Classification:** already_solved; **author attempts:** 1/5.  
**Validation:** fresh uninvolved AI audit PASS. **Date:** 2026-10-03 UTC.

The broad negative answer is a verified consequence of Kucharczyk’s 2014 preprint / 2015 published congruence-rigidity theorem. [Appendix B of the audit](audit/AUDIT.md#appendix-b-verified-prior-theorem-transfer-and-attribution-boundary) supplies the complete transfer, including the arithmetic lattice, integral/projective congruence comparison, and a nongeometric Nielsen automorphism. This is an inference from the theorem; we do not claim that Kucharczyk explicitly stated this corollary or the exact example below.

The packet also gives an elementary explicit example: two faithful embeddings of the same free group into the same SL_7(Z) make the same index-five subgroup respectively noncongruence and principal level two. [The complete proof](ATTEMPT_1.md) handles every modulus. Its ingredients are classical. One substantive author attempt was written before the prior-theorem transfer was verified, explaining the 1/5 count.

## Contents

- `ATTEMPT_1.md`: full elementary certificate, with reviewed attribution
- `SOURCE_GATE.md`: exact original source, literature and prior-attempt checks
- `audit/AUDIT.md`: unchanged independent audit, with an alternate uniform witness formula and verified prior-theorem transfer
- `verify_exact.py` and `verify_exact_results.json`: original exact controls
- `audit/independent_controls.py` and `audit/independent_results.json`: independent exact controls, made portable by one input-path edit
- `public/`: exact frozen pre-audit author snapshot; its historical pending-review wording is superseded by this README and the root-level files
- `DISPOSITION.md`: precise changes after review
- `RESEARCH_LOG.md`: research and review chronology
- `reproduce.py`: portable replay of both verifiers and all file hashes

## Reproduction

Run `python3 reproduce.py` from any working directory. Only Python’s standard library is required. The author replay passes **15,667 exact assertions**; the independent replay passes **25,051**, including 10,005 constructive witness levels, 52 finite-image relation tests, 1,365 actual block-word tests and independent checks of all 64 supplied witnesses. All outputs are compared byte-for-byte with their recorded results.

Finite tests corroborate the proofs and do not replace their all-moduli arguments. The result concerns the literal unrestricted abstract-embedding formulation in Valette’s 2018 report; it does not assert failure of the familiar invariance under algebraic embeddings of a fixed algebraic group.

No novelty, first-resolution, human peer-review or proof-assistant verification claim is made. This is a draft research certificate for human review, not an assertion of external acceptance.
