# Positive recurrence of bimolecular weakly reversible stochastic reaction networks with a single linkage class

**Version 0.2 - prepared for expert and author audit - 6 August 2026**

## Status

The adversarial reconstruction found no substantive mathematical defect in the marked-target proof. The clean release therefore records **Outcome A: author-ready theorem**.

The exact theorem is limited to finite weakly reversible stochastic mass-action networks with:

- one linkage class;
- molecularity at most two at every complex;
- arbitrary positive rate constants;
- an arbitrary closed communicating class, including boundary and lattice-restricted classes.

The release does **not** claim the multiple-linkage case, higher molecularity, the full Anderson-Kim positive-recurrence conjecture, exponential ergodicity, or quantitative mixing rates.

## Release map

- `manuscript/main_arxiv.tex` and `main_arxiv.pdf`: archival/arXiv version.
- `manuscript/main_jap.tex` and `main_jap.pdf`: Journal of Applied Probability initial-submission version with identical mathematical content.
- `manuscript/references.bib`: bibliography.
- `code/`: standalone verification package (version 0.2, this author-ready layer).
- `audit/independent_proof_reconstruction.md`: the adversarial Gate A1-A12 reconstruction referenced above.
- `supplement/proof_audit.md`: independent proof audit.
- `supplement/priority_audit.md`: narrow literature and priority audit.
- `supplement/reviewer_checklist.md`: ten load-bearing reviewer checks.
- `supplement/ai_use_statement.md`: full AI-use declaration.
- `supplement/verification_report.json`: canonical deterministic verifier output, as released.
- `supplement/MANIFEST.sha256`: release-file hashes.
- `expert_audit_note.md`: two-page orientation for a subject-matter expert.
- `cover_letter.md`: neutral draft submission letter; no submission was made.
- `revision_log.md`: changes from the preserved discovery version.

The full Phase I-V discovery archive that this release was audited against is
preserved unmodified elsewhere in this same directory rather than in a
separate `discovery_version/` subfolder: see `WORKLOG.md`,
`failed_approaches/`, `phase2_trigger_drain/`, `phase3_defect_credit/`,
`phase4_critical_lamperti/`, `phase5_source_flag_closure/`, and the
top-level `src/`. Their preserved hashes and the original Phase-V manuscript
match `discovery_version/ORIGINAL_HASHES.sha256` from the author-ready
distribution bit for bit (`main_manuscript.pdf` SHA-256
`f069d986ad13ca59cddab8d9fc4fff5ba46a85ca81146a65f1a4b17900390a1a`).

## Build the manuscript

```bash
cd manuscript
./build.sh
```

The script uses `SOURCE_DATE_EPOCH` and suppresses variable PDF metadata. Byte-identical rebuilds were verified in the release environment. With a different TeX distribution, a rebuild should be expected to be content-equivalent rather than necessarily byte-identical.

The `main_jap` wrapper intentionally uses a standard article class for initial submission. Current Applied Probability Trust instructions state that the APT class is encouraged but not a condition of initial submission; an accepted manuscript would be moved to the official class during production.

## Run the standalone verifier

```bash
cd code
python -m pip install -e .
./reproduce.sh
```

Tested with Python 3.13.5 and independently rerun with Python 3.14.6 for this git mirror (`code/GIT_MIRROR_VERIFICATION.txt`); Python 3.11 or newer is required. The package has no runtime third-party dependencies. The script runs the test suite, generates the report twice, requires byte-for-byte equality, and prints the stable SHA-256 digest.

The finite atlas and fixed-seed tests are adversarial calibration. The universal theorem is proved in the manuscript, not by enumeration.

## Author metadata

Alec Kriebel
Independent researcher
Correspondence: me@aleckriebel.com

No verified ORCID was supplied or located during the audit, so the release does not invent one.

## AI disclosure

OpenAI ChatGPT, model GPT-5.6 Pro, was used extensively on 5-6 August 2026 for proof exploration, counterexample attempts, verification-code generation, drafting, and critique. The human author reviewed the released manuscript and assumes responsibility for its claims, citations, code, and conclusions. See `supplement/ai_use_statement.md`.
