# Iterated adversarial preprint review

Current manuscript: **version 1.0.1, 23 September 2026**.

## Exact claim and scope

For the displayed affine group G = F_29^2 semidirect H of order 100920,
the manuscript claims b_f(G)=b(G)=3<4=mu′(G). The maximum b ranges over
all permutation representations; a base has stabilizer equal to the action
kernel. No smallest-order, formal-verification, or journal-acceptance claim
is made. This review targets mathematical soundness and preprint readiness.

## Review sequence

The first reviewer was a fresh AI agent, given the full paper and instructed
to examine it before reading earlier audit verdicts or supplied verifier code.
It independently checked the structural proof, reconstructed the finite
matrix and affine calculations, and checked the primary-source conventions.
It found one actionable wording issue in the dihedral-pair explanation and
no theorem-level defect. Its full report and independent checker are in
`round_1/`.

After the repairs below, a different fresh agent reviewed the entire revised
manuscript before reading prior verdicts. It checked the all-actions and
normality arguments, reconstructed the finite inputs, compared every
complement subgroup across implementations, checked the primary definitions,
inspected all nine PDF pages, rebuilt the PDF, and replayed the verification
and packaging checks from a clean extraction. It found **zero actionable
issues** and no mathematical gap. Its report and evidence are in `round_2/`.
This satisfies the requested stopping criterion; no third repair round was
needed. Both rounds were preprint reviews, with no journal preparation.

The second reviewer examined these exact unchanged manuscript bytes:

- `proof.tex`: SHA-256 `2c74f1291c165dbefe72ebddda0b0a47784b8202811b162cc4496d59acd04af4`.
- `proof.pdf`: SHA-256 `6225ed0ba605c1014c0e5e4954d97011f33eb8fa4c2b6243e4d071d5d82122df`.

Final archive assembly adds the completed review reports and closes current
status metadata. It does not change the reviewed proof or package builder.
`delivery_validation.json` records the final archive checks and hashes;
`deployment.json` records the live website check. These delivery records are
kept in the repository outside the frozen archive to avoid self-referential
archive hashes. The round-two archive hashes identify its earlier review
snapshot, not the final archive containing its own completed report.

## Findings and disposition

| Finding | Disposition | Effect on theorem |
|---|---|---|
| Wording could attribute dihedral generation to individual product images | Clarified that each pair of projective involutions generates a dihedral group, with product orders 2,3,5 | None |
| Pair-subgroup intersection order was compressed | Added the explicit gcd(8,12)=4 argument | None |
| Abstract's normality sentence was ambiguous | Explicitly identifies the order-two subgroup as central in the complement and nonnormal in G | None |
| Upload-kit rebuild included stale files from persistent output folders | Replaced directory enumeration with explicit archive members; planted-stale-file regression passes | Artifact correctness only |
| Current progress metadata still described completed old delivery steps | Replaced with completed version 1.0.1 review status; the old audit remains historical | Status reporting only |

The separately recorded original product-order correction (6 to 3) was
already applied in version 1.0.0 and is not a newly discovered error here.
The construction, subgroup orders, affine witnesses, and theorem are unchanged.

## Reproduce and limits

Run `make audit` and `python3 submission/test_package.py` from the source
folder. Both new independent checkers are additionally provided with their
reports. Use ordinary Python, without `-O`, for audit scripts containing
assertions. All arithmetic checks are exact.

These are separate AI adversarial reviews, not external human peer review
or a full proof-assistant formalization. No finite set of reviews guarantees
absence of every possible error. The stopping criterion is a complete fresh
review with no remaining actionable findings, together with reproducible
checks and consistent publication artifacts. Licensing is an author choice
at manual deposit and remains unset; no Zenodo submission or DOI is created.
