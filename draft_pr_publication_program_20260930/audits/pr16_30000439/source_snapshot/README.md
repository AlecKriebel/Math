# Embedding-dimension gap: reviewed candidate

**Result:** a complete candidate proof of a finite two-dimensional simplicial complex with PL embedding dimension exactly 3 and linear embedding dimension exactly 5. This answers the existential formulation in OWR 12/2006, pp. 701–702.

**Validation:** the exact frozen candidate passed a separate adversarial AI review on 30 September 2026, with no required mathematical correction. All 16 submitted checks and 396 independent exact assertions passed. Historical priority is unconfirmed; this is not external peer review or a formal proof certificate.

- [Candidate proof](CANDIDATE.md)
- [Independent review](independent_review/REVIEW.md) and [machine-readable verdict](independent_review/verdict.json)
- [Source and prior-attempt audit](SOURCE_AUDIT.md)
- [Research log](RESEARCH_LOG.md) and [provenance](provenance.json)

`CANDIDATE.md` is preserved byte-for-byte as reviewed. Its original “verification pending” header records its pre-review state; the review linked above supplies the current status. Candidate SHA-256: `23705f2868d66526eeded2cf644d36138acd8223af13d5202ee22da415753502`.

The construction is probabilistic and uses finite parameters $n=2^{256}$, $p=2^{-384}$, and $m=2^{320}$. The verification checks the exact inequalities without generating the enormous complex. The mathematical proof credits the affine van Kampen–Flores theorem, order-type bounds, Janson's inequality, Newman's even-dimensional mechanism, and Lee–Nevo's PL-embedding lemma.

## Reproduce

From this directory, using Python 3 (standard library only):

```sh
python3 check_bounds.py
python3 independent_review/independent_checks.py
```

The checks supplement the written proof and do not certify the imported geometric theorems.
