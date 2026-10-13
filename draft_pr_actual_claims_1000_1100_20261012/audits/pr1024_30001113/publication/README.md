# A characteristic-two counterexample to dévissage for local deformation functors

Alec Kriebel, independent researcher; ORCID
[0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X).
Version 1.0, 12 October 2026. Licence: CC BY 4.0.

The [research note](research_note.pdf) gives a negative answer to Byszewski's
**unrestricted** fibre-product question. For the weakly ramified additive F4
action and its F2 subgroup, no prorepresentable recipient permits a formally
smooth restriction–induction factorization, regardless of tangent dimension.
The variant imposing prorepresentability of the subgroup and quotient
deformation functors remains unaddressed. Nilpotent constant coordinate
changes are permitted by the original category; fixing the zero section
would change the question.

The additive action, involution pathology, parameter-shift conjugacy and
tangent-cohomology framework are established prior ingredients. Recipient
tangent collapse follows from Byszewski–Cornelissen (2009), Proposition 6.1;
Proposition 4.1 supplies the matrix conjugacy. The assembled obstruction to
the unrestricted factorization is the contribution. The bounded priority
search does not certify exhaustive originality or continued openness to 2026.

AI tools were used extensively in solving, verification, source auditing and
preparation. This is an unrefereed preprint. Independent adversarial reviews
are AI reviews; conventional human peer review, journal acceptance and a
formal proof-assistant certificate are not claimed.

## Read and reproduce

- [TeX source](research_note.tex) and [scope/priority supplement](SUPPLEMENT.md).
- [Portable evidence index](evidence/INDEX.md): source URLs, stage records,
  independent derivations, exact receipts and review gates.
- [Exact metadata](metadata.json) and [file inventory](PACKAGE_MANIFEST.json).

With Python 3.10 or later and its standard library, from this directory run:

```text
python3 run_checks.py
python3 run_checks.py --output verification_receipt.json
```

The runner tests 39 executions: nine baselines, twelve actual defective-source
controls and eighteen runtime fault controls, in normal, -O and -OO modes.
It compares complete stdout, stderr and exit codes with fixed references,
including exact recursive JSON types. Two submitted mathematical programs
and their reporting adapter are unchanged. A third independently written
arithmetic program has an explicit-guard adaptation: all eleven assertion
predicates are unchanged and remain active under optimization; its original
source and AST correspondence are included. No external packages, credentials,
network access or UID1000 account are needed. Execution recorded here used
Python 3.14.6 on macOS; other operating systems have not been tested here.

These finite checks support explicit identities and selected control cases.
The complete formal-series and arbitrary-natural-transformation claims are
proved in the note and independent reports. Isolated Python flags are not a
general security sandbox. The original sealed UID1000 permission harness is
historical evidence, not replayed by this portable kit; do not use its scripts
as the reproduction entry point. Stage-specific holds and counts are retained
as history and are not current acceptance decisions.

The note compiled successfully and all five pages were rendered and visually
inspected. The first fresh whole-package adversarial review passed with zero
actionable concerns. A NEW second review remains pending in
[the current state](evidence/CURRENT_REVIEW_STATE.json). This candidate package
is not yet approved for immutable publication. Third-party source bodies are
not redistributed; public primary links and retrieved-byte hashes are provided.
