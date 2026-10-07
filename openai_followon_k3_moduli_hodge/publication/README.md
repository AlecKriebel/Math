# Rational Hodge classes on mixed products of K3 moduli spaces

Author: Alec Kriebel. ORCID: https://orcid.org/0009-0001-9320-500X.
Manuscript date: 6 October 2026. No affiliation or coauthor is asserted.

## Result and contribution

The note combines the pinned OpenAI mixed-K3 rational Hodge theorem with
Bülles's Theorem 0.1. It records rational HC in every codimension for any
finite mixed product of smooth projective stable-sheaf or eligible
twisted/generic Bridgeland-stable moduli on complex projective K3 surfaces,
including Hilbert schemes. Bases can differ or repeat. The actual moduli
spaces must satisfy the precise smoothness, projectivity and stability
conditions in the theorem. Empty and zero-dimensional factors and S^[0]
are handled explicitly. See Theorem 1 of the paper for the exact statement.

The contribution is an explicit assembled corollary with tensor and
codimension bookkeeping. The base mixed-K3 breakthrough is attributed to
OpenAI; the motive reduction to Bülles, with prior conditional transfers by
Arapura. The earlier quadratic-locus companion already states restricted
moduli/self-power consequences, and its criterion together with universal
KS supplies an implicit unrestricted single-base application. No first,
substantial independent novelty, new base proof or new reduction is claimed.
The universal mixed-moduli target contains S^[1]=S and therefore includes
the full mixed-K3 assertion; the transfer cannot bypass that dependency.

The note does not assert HC for arbitrary K3^[n] deformations, singular or
semistable moduli, abelian-surface moduli, integral or generalized Hodge,
or finite-dimensional motives. The precise source chain and audit boundaries
are documented in the dependency ledger and validation report.

## Files and reproduction

The deposit consists of `paper.pdf` and `source-and-verification.zip`.
The source archive contains standalone `main.tex` (including its own
bibliography), upstream supplied citation blocks, this README, a dependency
ledger, dated priority and scoped mathematical audits, an upstream hash
manifest and exact small algebraic check scripts/results. It contains no
upstream manuscript copies, third-party downloads, credentials or caches.
`SHA256SUMS.json` covers the other source files; it does not hash itself.

Extract the archive, then run:

```sh
python3 reproduce.py
```

This checks the archive's source hashes, executes each exact finite check
in a fresh temporary directory and compares its results, then builds the
PDF in that directory with Tectonic 0.16.9. It copies the resulting PDF to
`reproduced/paper.pdf` and records its hash and tool versions there. Python
3.10+ and Tectonic on PATH are required; no third-party Python packages are
needed for these checks. Tectonic may need network access for its normal TeX
bundle cache on first use. A conventional LaTeX installation can also
compile `main.tex` directly, but byte-identical PDF output is only claimed
for the recorded Tectonic setup with the fixed timestamp environment.
The finite checks do not validate the full geometric HC theorem.

The main source was also opened and compiled successfully in Codex's
built-in LaTeX editor. An actual exported PDF was independently generated,
rendered and visually inspected. Publication file hashes and review
snapshots are retained separately in the project publication records.

## Source version, review and license

All OpenAI inputs use public snapshot
`adc7f1241b42e322a6451854ab7e4b4c146bf78a` of
https://github.com/openai/math, accessed 6 October 2026. Cover dates do not
establish earliest public disclosure. The supplied manuscript-specific
BibTeX blocks are preserved in `upstream-citations.bib`; the paper uses
fixed-commit links to those same manuscripts.

AI tools were used extensively in research, source and priority checks,
drafting and verification. This preprint has not undergone conventional
human peer review/refereeing. Automated adversarial audits are not human
peer review. The Lean module mentioned in the upstream material covers
Clifford/tensor identities, not universal KS, algebraic cycles or this
moduli theorem; no Lean build is relied on. Scoped source-proof audits and
finite certificates have their stated limits. There was no external outreach.

Original note, reports and check code: © 2026 Alec Kriebel, distributed
under Creative Commons Attribution 4.0 International (CC BY 4.0),
https://creativecommons.org/licenses/by/4.0/. Citation information and
dependency facts retain their original attribution. Upstream manuscripts
are linked, not redistributed.
