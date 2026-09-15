# Zenodo copy-and-paste metadata — version 1.1.0

Use the existing Zenodo draft associated with **10.5281/zenodo.22770864**. The supplied identifier did not resolve publicly when checked. Confirm that the draft holds this record-specific DOI, not a DOI for a different deposit or an all-versions concept identifier. If it is the DOI reserved by this same Zenodo draft, keep its existing reservation; do not create another upload or enter it as an unrelated external DOI.

## Basic fields

| Zenodo field | Value |
| --- | --- |
| Resource type | Publication → Preprint |
| Title | An explicit odd-order p-group with as many automorphisms as elements |
| Additional title / subtitle (optional) | A computer-assisted solution to Kourovka Notebook problem 16.63 |
| Version | 1.1.0 |
| Publication date | 2026-09-15 |
| Creator given name | Alec |
| Creator family name | Kriebel |
| ORCID | 0009-0001-9320-500X |
| Affiliation | Leave blank; independent researcher |
| Language | English |
| Publisher | Zenodo |
| File visibility | Public |
| License | Choose before publication; no license has been assumed or applied |

The publication date above is the date of this revised edition. The first website edition appeared on 2026-09-14. If this version is first made public on a different date, adjust the metadata accordingly.

## Description — paste the following

We construct an explicit nontrivial finite p-group G of odd order with p = 1009 and |G| = |Aut(G)| = 1009^52359, giving an affirmative answer to D. MacHale’s problem 16.63 in the Kourovka Notebook. Here Aut(G) is the full automorphism group.

The group is obtained by the finite Baker–Campbell–Hausdorff construction from an explicitly specified rank-31 Lie ring modulo 1009^1689. Its nilpotency class is at most 846 < 1009. An asymmetric lattice and a rigid finite-field flag force every finite Lie-ring automorphism into an integral logarithm–exponential domain. A precision-preserving bijection then identifies the full automorphism set with the kernel of an exact derivation matrix. Its rank is 931, its nullity is 30, and its nonzero 1009-primary Smith valuations have multiplicities 87, 55, 758, 6, and 25 at valuations 0, 1, 2, 3, and 4. Their sum is 1689. The finite Lazard correspondence preserves the full automorphism group and completes the group-theoretic conclusion.

This record contains the unrefereed preprint and its focused companion archive: editable LaTeX, the explicit group specification, exact certificates, verification software, computational logs, and scoped AI audit reports. The underlying Lie-algebra template is credited to Omirov and Ruan, arXiv:2605.04602v1, Theorem 4.8. Version 1.1.0 adds artifact citations, two mathematical clarifications, and publication-disclosure improvements; the mathematical construction and computational data are unchanged.

The construction, proof development, and initial verification software were generated using ChatGPT-6 Astra Pro. Separate Codex sessions performed additional AI-assisted reviews and exact computational checks. All checks described in the accompanying audits were completed, with no unresolved error identified within their stated scope. These checks do not constitute external human peer review or proof-assistant formalization. No minimality claim is made for the prime or group order.

## Keywords — enter separately

finite p-groups; automorphism groups; Kourovka Notebook; problem 16.63; Lie lattices; Lazard correspondence; Baker–Campbell–Hausdorff formula; Smith normal form; computer-assisted proof

## Subjects — optional

Mathematics Subject Classification (2020): 20D45; 20D15; 17B40.

## Related works

- Is supplemented by — https://github.com/AlecKriebel/Math/tree/kourovka-16-63-v1.1.0/kourovka_16_63
- Is documented by — https://aleckriebel.github.io/Math/papers/kourovka-16-63/

## Notes — optional

Unrefereed preprint. Initial public edition: 2026-09-14. Publication revision 1.1.0: 2026-09-15. The construction, proof development, and initial verification software were generated using ChatGPT-6 Astra Pro, followed by separate Codex AI reviews and exact computational checks. AI tools are disclosed in the manuscript and description rather than listed as human creators.

## License decision

Zenodo requires a license and defaults to CC BY 4.0. Choose the terms you intend to grant before publishing. This kit does not add a license to the existing repository. If you choose different licenses for the paper and code, state each scope clearly in the record and include matching license notices with the files.

## Files to upload

Use only the two files in the kit’s `UPLOAD_THESE_FILES/` folder. The PDF is separately readable; the ZIP contains the focused source and verification package. `UPLOAD_SHA256SUMS.txt` lets you check that they match the prepared edition. The complete outer upload-kit ZIP is a convenience for you, not a substitute for these two record files.

The exact version tag above identifies the final publication snapshot. Its resolved Git commit is recorded in the post-publication repository log; the manuscript uses the tag because a commit cannot contain its own final hash.
