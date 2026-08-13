# Positive recurrence for three-species binary networks

This research package proves the following theorem.

> Every finite weakly reversible stochastic mass-action network whose
> complexes have total molecularity at most two, with at most three species
> and at most two linkage classes, is nonexplosive. Every state in every
> closed irreducible population class is positive recurrent, for every
> positive rate vector.

The proof first reduces each fixed population class exactly, then handles
zero, one, or two projected linkage classes. The two-linkage case is an exact
disjoint union of all 46,872 ordered support pairs:

\[
46{,}872=27{,}462+432+146+336+18{,}496.
\]

Each summand has a standalone analytic recurrence theorem. The finite code
certifies only support, tier, affine, and set identities; it never enumerates
rates, orientations, population states, or stochastic histories.

## Primary artifacts

- Main article: `output/pdf/main.pdf`
- Complete technical supplement: `output/pdf/technical-supplement.pdf`
- Global theorem: `research_notes/proof_first_t3_2_global_theorem.md`
  (`781d2520cbb3ad30e1749814f620d49d4c503c5c341ccd1add39a5fec31e2b7f`)
- Global exact-byte audit:
  `research_notes/proof_first_t3_2_global_theorem_exact_byte_audit.md`
  (`bbc47342d8d7b3cacf4b34d2ce2b5bd122798f41838787e8edafa4c70c859560`)
- Final two-linkage theorem:
  `research_notes/proof_first_two_linkage_46872_final_theorem.md`
  (`dae2a58f170836427ffc053ff931c1909d64ac591d77b971591b0d5814526cde`)
- Final two-linkage exact-byte audit:
  `research_notes/proof_first_two_linkage_46872_final_exact_byte_audit.md`
  (`a4f50dcbc2235766524ddb7000a264ec88bf04f8841b3ce9b8d4689c800ba619`)

Independent audits under distinct paths reproduce both final conclusions.
See `STATUS.md` and `CERTIFICATION_REPORT.md` for the complete release record.

## Reproduction

Run the isolated finite verifier:

```bash
python3 -I -B verify_read_only.py
```

It currently runs 418 tests and checks that its entire declared scope is
unchanged. Passing this executable layer is not, by itself, a proof of the
stochastic theorem; the analytic argument is supplied by the byte-frozen
theorems and independent audits above.

Rebuild the publication PDFs and verify all 40 supplement inputs:

```bash
./publication/build_publication.sh
```

The `inherited/` tree and many early research notes are retained as
chronological provenance. Their historical statements that the theorem was
open are superseded by the final artifacts listed here; their local
counterexamples and claim boundaries remain in force at their stated scopes.

Author, license, and submission metadata are intentionally not selected in
this research package.
