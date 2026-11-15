# A symmetric ideal chain with periodic Lefschetz behavior in positive characteristic

Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X. Version 1.0.0,
22 October 2026. Four-page unrefereed preprint and scientific verification source.

The proof defines one compatible two-row ideal chain over any fixed field.
For every n>=2, both WLP and SLP hold precisely when (n-1) is nonzero in
the field. Width one is separately SLP. The integral quotient is torsion free.
Over the single infinite field F_p(t), the chain therefore has arbitrarily
large good and bad widths, with period p from width two. The fixed generators
come from width three. There is no negative conclusion for characteristic zero
or for the one-row variant, and no assertion that either stronger question is
currently open.

Read `main.tex` or `paper.pdf` for the universal proof. It includes all indexing
and compatibility conditions, repeated-index cubic generators, the integral
basis, every-linear-form determinant, degree-one socle obstruction, explicit
strong Lefschetz form including characteristic two, and the n=1 case.
No external theorem beyond elementary algebra is needed for this proof.

## Offline verification

Use Python 3.8 or later, standard library only, without installing packages:

```
python3 -B reproduce.py
python3 -B build_package.py --output ../rebuilt
```

The first command reads and verifies every member named by the closed public
manifest, rejects missing or extra files, checks the TeX/PDF provenance and
metadata agreement, and runs the checker in normal, -O, and -OO modes.
All three outputs must equal `verification/EXPECTED.json` exactly.
The checker does not write files or use a network. It constructs the raw
quadratic monomials and relations, eliminates them using unimodular integral
row operations, and derives products in the resulting quotient. It checks:

- widths 1 through 7, including the exceptional initial Hilbert function;
- 72 general-form integer matrix cases with exact determinants;
- all 2,170 coefficient vectors in six small finite-field cases;
- 872 injections and width-three generation through width six;
- thirteen deliberately false controls, including omitted relations, a sums
  mutation, wrong bad-width congruence, zero x-coefficients, and characteristic two.

The sum-y diagnostic derives degree-one coordinates from the actual quotient
and checks multiplication by every x/y generator at widths3/4 in characteristic2.
These distinguish p dividing n from p dividing n-1. A false added linear relation
sum(y)=0 is rejected as a zero-sum regression. This narrow repair leaves the
paper, PDF, mathematical theorem, and other finite case ranges unchanged.

Finite computations do not prove the theorem for all widths or fields.
The written universal argument is primary. These are falsifiable diagnostics,
not a formal proof-assistant certificate or a priority test. No claimant or
third-party mathematical program, including the earlier review checker, is run.

The second command first verifies the source package, then creates the scientific
PDF, deterministic source/verification ZIP, matching metadata and deposit
proposal, upload README, and five-member upload kit. It reuses the exact frozen
PDF, so rebuilding the archives is byte reproducible. Recompiling TeX is a
separate optional operation; byte-identical TeX recompilation is not claimed.
Run any ordinary LaTeX engine with the standard packages listed in `main.tex`
to obtain another PDF. The actual export used official Tectonic 0.17.0 with
existing cached dependencies, network denied, and shared-cache writes denied.
`BUILD_RECEIPT.json` records source, PDF, and compiler hashes. Every final PDF
page was rendered and visually inspected; the original source also compiled
successfully in the desktop LaTeX editor.

## Attribution, priority, and limits

Römer's original question is in OWR31/2020, pp.1594–1596,
DOI https://doi.org/10.4171/OWR/2020/31. The report's separate one-row monomial
working-group focus is not a restriction on the original arbitrary-field,
arbitrary-fixed-row contribution. The original-question DOI is not a solution DOI.
Seceleanu–Şega's *General symmetric ideals*, arXiv:2506.15459v1 (18 June 2025),
is explicitly credited and compared in `RELATION_TO_PRIOR_WORK.md`.
Source hashes, versions, dates, and exact read limits are in `SOURCE_PROVENANCE.json`.
No raw third-party source bodies, private register captures, review packets,
provider credentials, or service/operations drivers are included.

The earlier project PR1337 is an unpublished proof source and is not an earlier
published solution. Bounded searches on 22 October 2026 authenticated no earlier
publication of this exact construction; they do not certify exclusive firstness,
exhaustive novelty, or present open status. No DOI is reserved or assigned here.
This is a local preparation package, with publication readiness false pending
new independent whole-package reviews and root adoption. No upload, merge,
release, register write, or publication is performed by these files.

## Authorship and licensing

AI tools were used extensively in all phases: planning, mathematical exploration,
proof development and reconstruction, computation, literature investigation,
writing, editing, and adversarial verification. Alec Kriebel is the named human
author. The preprint is unrefereed, without conventional independent human peer
review, journal acceptance, or formal proof-assistant certification. Internal AI
audits do not provide those certifications.

Authored prose is CC BY 4.0 (`LICENSE-PROSE-CC-BY-4.0.txt`); authored code is MIT
(`LICENSE-CODE-MIT.txt`). Third-party sources retain their own rights. Generic
packaging helpers reuse Alec Kriebel's MIT code from the PR1329 preparation;
the mathematical checker is newly authored for this note. `CODE_PROVENANCE.json`
records the distinction and upstream helper hashes.
