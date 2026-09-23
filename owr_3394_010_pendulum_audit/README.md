# OWR-3394-010: verification and priority audit

**Verdict: the affirmative answer is correct; it is an existing result of
David Angeli and Laurent Praly, not a new open-problem resolution.**

The original problem appears in Oberwolfach Report 11/2009, pp. 670–671.
Angeli–Praly explicitly answer it in their 2010/2011 work. Their journal article
was first published online on December 6, 2010, and appeared in the July 2011
issue of *IEEE Transactions on Automatic Control*, 56(7), 1582–1592,
[DOI 10.1109/TAC.2010.2091170](https://doi.org/10.1109/TAC.2010.2091170).

This folder records a verification of the supplied candidate, with one minor
rigor clarification. It claims no new mathematical contribution.

- [AUDIT.md](AUDIT.md): precise claim, checkable derivation, limitations, and priority decision.
- [SOURCES.md](SOURCES.md): primary sources and page-level evidence.
- [reviews/](reviews/): independent adversarial and source reviews.
- [verification/verify.py](verification/verify.py): exact rational polynomial checks.
- [RESEARCH_LOG.md](RESEARCH_LOG.md): checkpoints and approach ledger.

From the repository root, run:

```sh
python3 owr_3394_010_pendulum_audit/verification/verify.py
```

Requires Python 3, with no external packages. The script verifies algebraic
certificates, not the imported theorem or the measure-zero conclusion.

The user's request for a resolution paper, GitHub Pages site, and Zenodo upload
package was conditional on a clean priority audit. That condition fails, so no
such publication package or DOI release is created. This audit is committed as
a research record. Source PDFs are linked, not redistributed.

Audit date: September 22, 2026 (America/Los_Angeles; September 23 UTC).
Research owner: Alec Kriebel, [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X).
Prepared with AI assistance; the prior mathematical result belongs to its cited authors.
