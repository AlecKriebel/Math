# Scalar idempotents and projective cancellation in characteristic two

This is an attributed consequence note and independent source audit, not a new discovery announcement. The requested mathematical targets follow from the pinned October 4 OpenAI construction by classical algebra. The source audits found no substantive gap in the arguments checked, but are automated reviews rather than human refereeing or formal verification.

For the source's finitely presented torsion-free G with a finite two-dimensional classifying complex, set R=F_2[G] and e=1-ba, where ab=1, ac=0 and c≠0. Then e is a scalar idempotent different from 0 and 1. The nonzero cyclic projective right module P=eR satisfies R≅R⊕P and [P]=0 in K_0(R). The same e remains nontrivial in K[G] for every characteristic-two field K. No characteristic-zero, odd-characteristic or reduced-C*-algebra conclusion is asserted.

Publication is withheld under the user's duplication rule. Public commit [f27318d](https://github.com/AlecKriebel/Math/commit/f27318d83bd7000ef817957a9a4b3087de28d198), timestamped October 6, 2026 at 21:55:38 PDT, already contains all core consequences and the algebraic proof outline in the triage report and algebra notes. Source validation and fuller exposition do not create a new mathematical result. No Zenodo draft, publication, DOI, upload manifest or spreadsheet entry is claimed or initiated for this effort.

## Files and evidence

- `main.tex`: standalone, self-contained source including bibliography; opens in the native LaTeX editor.
- `paper.pdf`: exported, downloadable note; the reproduction command creates it.
- `notes/ALGEBRA_PROOF.md`: complete ring/module/extension proof and boundary checks.
- `reviews/source_combinatorics.md` and `reviews/source_topology.md`: separate detailed source audits.
- `notes/PRIORITY_AUDIT.md` and `notes/CLASSICAL_PROVENANCE_AUDIT.md`: affirmative duplication evidence and primary-source provenance, with stated limits.
- `sources/SOURCE_MANIFEST.json`: pinned input hashes; copied upstream evidence is locally retained and excluded from publication payloads.
- `DEPENDENCY_LEDGER.md`, `CURRENT_THEOREM.md`, `APPROACH_TABLE.md`, `RESEARCH_LOG.md`: exact scope, dependencies, approaches and timestamped checkpoints.
- `receipts/`: nonsecret reproducibility and safe-main push records.

## Reproduction

From this folder, run `python3 verification/verify.py` for the exact Fano/contraction checks and finite abstract-ring boundary checks. These are supplemental computations; they are not a numerical multiplication certificate in the target group algebra.

Run `python3 verification/reproduce.py` with Python 3, Tectonic, `pdfinfo`, `pdffonts` and `pdftotext` available. It builds `main.tex` in a fresh project-local temporary directory, checks references/text and records the engine version, source/PDF hashes and font information in `receipts/clean_reproduction.json`. Rendering/visual inspection is recorded separately. The native editor/compiler is independent of the terminal engine and also verified this standalone source.

To inspect the precise upstream dependency, obtain [OpenAI/math commit adc7f124](https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a) and its `preprints/A-Torsion-Free-Group-Algebra-That-Is-Not-Directly-Finite-October-4-2026` folder. Compare the file SHA-256 hashes against the source manifest. The source's Apache 2.0 license is retained with local copies. Earlier family-197 Lean declarations concern torsion-containing examples and do not verify the October 4 theorem. No Lean build is claimed here.

The construction selects an unlisted finite matching outcome at a sufficiently large parameter. The note supplies its finite-presentation and scalar-sum recipe, but no numerical matching, relator list or coefficient certificate was obtained. Do not confuse existential completeness with numerical explicitness.

## Authorship and review

Author: Alec Kriebel; ORCID [0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X). No affiliation or coauthor is inferred. AI tools were used extensively in research, drafting and verification. This research record has not undergone conventional human peer review or refereeing. The upstream construction is attributed to OpenAI as its supplied citation requests. Complete-package automated reviews are recorded in `reviews/`; their exact scope and hashes, rather than a generic approval label, define what was checked.
