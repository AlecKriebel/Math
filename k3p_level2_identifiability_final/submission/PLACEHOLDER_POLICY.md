# Fail-closed placeholder policy

An unresolved release-time field has the literal form `@@UPPER_CASE_TOKEN@@`.
No placeholder may be replaced by a guess. In particular:

- a GitHub URL is not a substitute for the required Zenodo record;
- no DOI is asserted until it resolves to the deposited record;
- no license is selected on the author's behalf;
- no funding or competing-interest declaration is inferred from silence;
- no corresponding address, email, telephone number, or residence is inferred;
- no exclusivity, author approval, or submission-date statement is asserted
  before author confirmation; and
- no PDF is considered present until the final rendered file exists and passes
  page-by-page QA.

`validate_submission_packages.py` scans every submission text file for the
token grammar and returns `NOT_READY` while any token remains. Validators must
not whitelist or ignore a token merely because it appears in metadata, a cover
letter, a checklist, or this policy file. (The examples in this paragraph use
backticks and are excluded only because they describe the grammar itself.)
