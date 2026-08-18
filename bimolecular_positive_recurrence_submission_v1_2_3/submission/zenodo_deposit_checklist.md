# Optional manual Zenodo preservation checklist

Use this only if the human author chooses to preserve Version 1.2.3 after the
bioRxiv posting. No Zenodo deposit or DOI exists at release time.

## Recommended object

Upload the curated, manifest-verified file
`bimolecular_positive_recurrence_submission_v1_2_3.zip` manually. Do not enable
automatic archiving of the whole `Math` monorepo for this release: repository-
root metadata and a repository-wide source snapshot would describe and include
many unrelated research programs.

## Metadata source

Use the package-root `CITATION.cff` for the title, author, ORCID, version, date,
abstract, keywords, preferred citation, and tagged source URL. Classify the
mixed composite ZIP as **Other**, and describe it as a research package
accompanying an unrefereed preprint. Zenodo's current controlled vocabulary
does not contain a separate “research package” type. Do not describe the finite
verifier as proof of the universal theorem.

## Deposit-day checks

- Verify the public tag `bimolecular-positive-recurrence-v1.2.3` and run
  `validation/replay_release.sh` from a clean checkout.
- Compare the ZIP hash with the public `SHA256SUMS.txt` entry.
- Recheck Zenodo's current metadata and licensing fields rather than relying
  on a stored API-schema guess.
- The license field is required and currently defaults to CC BY 4.0. Remove
  that default unless deliberately relicensing the package. Add MIT for the
  `code/` subtree and a custom all-rights-reserved entry matching `LICENSE.md`
  for the manuscript and other materials; state each scope in the record
  description and verify both licenses before publishing.
- If bioRxiv has posted, add the bioRxiv DOI as a related identifier with the
  correct relation, not as the Zenodo DOI or journal DOI.
- After deposition, add the minted Zenodo DOI to a new version of the
  repository materials. Never insert a placeholder or anticipated DOI.

The Zenodo deposit and any metadata entry must be completed by the human
author. This package performs no external upload.

## Official guidance rechecked 17 August 2026

- Resource types: <https://help.zenodo.org/docs/deposit/describe-records/resource-type/>
- Required, multiple, and custom licenses:
  <https://help.zenodo.org/docs/deposit/describe-records/licenses/>
