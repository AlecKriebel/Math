# Even Minkowski uniqueness as a consequence of logarithmic Brunn–Minkowski

Alec Kriebel — [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X). Manuscript date: October 6, 2026. No institutional affiliation is asserted.

This concise consequence note applies OpenAI's pinned origin-symmetric logarithmic Brunn–Minkowski inequality to established Minkowski transfer machinery. It states and proves the following conclusions in ambient dimension `n >= 2`:

- For `0 <= p < 1`, every strictly positive even `f in C∞(S^(n-1))` has exactly one positive even smooth **support function** satisfying `h^(1-p) det(∇²h+hI)=f`, with the spherical curvature-radius matrix `∇²h+hI` positive definite.
- For `0 < p < 1`, identical `Lp` surface-area measures determine arbitrary full-dimensional origin-symmetric convex bodies.

The determinant is on the `(n-1)`-dimensional tangent space and spherical area measure is unnormalized. The data fix scale: dilation by `c` multiplies the prescribed measure by `c^(n-p)`. Origin symmetry fixes the center. No volume-one condition is imposed. Equal-volume coordinate boxes show that the general-body assertion fails at `p=0`; the smooth strictly positive endpoint assertion has a different scope.

OpenAI supplies the new base inequality, at commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. Böröczky–Lutwak–Yang–Zhang and other cited authors supply established logarithmic/Lp transfers; He–Liu supply the smooth endpoint mechanism. Existence and regularity are established results of the cited authors. The note supplies an explicit nonsmooth first-variation and mixed-volume strictness account and a local smooth endpoint calculation. It claims neither a new proof of logarithmic Brunn–Minkowski, a new transfer technique, nor first public announcement of the uniqueness conclusions. The priority audit records Stancu's 2018 announcement and the limits of the accessible evidence.

## Files

- `main.tex`: standalone manuscript with its full bibliography embedded.
- `paper.pdf`: exported publication PDF.
- `references.bib`: supplied manuscript-specific OpenAI citation for reuse; compilation does not require it.
- `CURRENT_THEOREMS.md`, `DEPENDENCY_LEDGER.md`, `APPROACH_TABLE.md`, `RESEARCH_LOG.md`: exact scope, dependency checks and research provenance.
- `agent_notes/`: independent analytic, regularity, priority and formal-scope audits, plus two exact rational tensor checks.
- `verification/REPRODUCIBILITY.md` and `verification/reproduce.py`: check scope and reproducible commands.
- `sources/UPSTREAM_INVENTORY.json`: pinned external source paths, versions, sizes and SHA-256 hashes; it contains no redistributed source manuscripts.
- `publication/`: archive builder, package inventories and nonsecret publication receipts.
- `zenodo-deposit.json`: exact intended production Zenodo metadata and upload file set.

The explicit public archive file list is generated as `PACKAGE_CONTENTS.json` inside `source-and-verification.zip`. Downloaded articles, upstream source copies, cloned Lean dependencies, caches, generated previews and credentials are excluded. Local source-audit paths in historical notes identify evidence inspected during research; the public archive does not include those third-party copies.

## Reproduction and evidence limits

Run `python3 verification/reproduce.py` from an extracted archive or this project directory. It runs 450 deterministic exact rational tensor cases and independent scaling, box-measure and endpoint-identity checks. These finite tests are regression and falsification evidence; the universally quantified proofs are mathematical arguments in the manuscript and analytic audits. See `verification/REPRODUCIBILITY.md` for clean TeX compilation and optional verification against a separately obtained pinned upstream checkout.

The actual upstream declaration `OAI.LogBrunnMinkowski.main` was inspected for scope and semantic agreement. Its intentionally unfinished comparator is a different file. An exact-toolchain rebuild was attempted but not completed because of available disk space. No successful kernel build, axiom extraction, Comparator run or formalization of this follow-on theorem is claimed. The note rests on the audited analytic input and explicit mathematical deductions.

AI tools were used extensively in research, drafting and verification. Automated adversarial reviews are not human peer review. At publication, this preprint has not undergone conventional human peer review or refereeing.

## Publication

The publication files are `paper.pdf`, `source-and-verification.zip` and the separate publication `README.md`. A reserved draft DOI or a prepared archive does not establish publication. The verified production record, assigned DOI and spreadsheet read-back will be recorded in `publication/README.md` and nonsecret receipts only after the authorized operations succeed. The owned contribution is licensed under CC BY 4.0; cited third-party works retain their own rights.
