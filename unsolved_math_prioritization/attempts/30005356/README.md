# Inverse Frobenius defeats the literal integral-polynomial claim

Problem **30005356 / OWR-12697685-001**, catalogue rank 778. Queue disposition: **claimed_solved, 1/5**, qualified as a candidate negative answer to the literal unrestricted-characteristic statement. Independent AI audit: **PASS**. Novelty review remains pending.

## Exact result and limits

In every positive-characteristic ACFH model, the inverse Frobenius map defined by y^p = x is a parameter-free definable multiplicative endomorphism outside Z[theta]. Polynomial faithfulness is proved directly from existential closedness; the independent reconstruction also supplies a self-contained existence proof for positive-characteristic models.

The characteristic-zero classification and equality with Z[1/p][theta] in positive characteristic remain **OPEN**. The localized ring is only proved to embed in the definable endomorphism ring. No novelty, priority, human-peer-review, formal-proof-assistant, or editorial-acceptance claim is made. Finite controls are sanity checks, not a proof or a simulation of ACFH.

## Read the preserved proof and later review

- [Author proof](author/PROOF.md)
- [Independent AI audit](independent_audit/AUDIT.md)
- [Independent proof, including existence and faithfulness](independent_audit/INDEPENDENT_PROOF.md)
- [Public evidence and reconstructed catalogue review hash](independent_audit/PUBLIC_EVIDENCE_RESULTS.json)
- [Machine-readable governing status](PUBLICATION_STATUS.json)

Both historical freezes and their extracted files are preserved byte for byte. Statements in the earlier author packet that independent review is pending describe its historical state; the later independent AI audit is PASS. It requires no mathematical correction and supplies only the missing catalogue review hash, 00c719d497159151748580b116c2a138f20956fbd106b60808c144bf4ca63de8. Human review and novelty assessment have not been supplied.

## Sources and publication boundary

The inspected research article is [d'Elbee, arXiv:2212.02115v4](https://arxiv.org/abs/2212.02115v4), especially Section 5.1, alongside the contribution on printed pp. 97–98 of [Oberwolfach Report 2/2023](https://ems.press/content/serial-article-files/46996). The inaccessible final journal full text was not inspected. Public bibliographic metadata identifies the [2025 APAL article](https://doi.org/10.1016/j.apal.2025.103554); it is not an endorsement of this counterexample.

Only authored proof, audit, programs, results, immutable safe archives, and public verification metadata are delivered. Source PDFs, extracted scholarly text, source images, raw corpora, raw selected records, and private coordination files are excluded.

## Reproduce

Run `python3 verify_publication.py` from this directory or by absolute path. Python 3.10+ and its standard library suffice. The verifier checks the complete recursive file inventory, archive and manifest hashes, exact ZIP-member correspondence, required disposition, and normal author and independent controls with assertions active. It refuses optimized Python execution. No source download is needed for these checks.

The separate independent `verify_public_evidence.py` accepts local copies of the public corpora and sources listed in its help. Those input bytes are deliberately not included; its preserved result and source metadata describe the provenance checks. Mathematical conclusions rest on the written proofs.

The queue edit changes only this problem's Status, Turns, and Findings cells. Its Chat and DOI cells, all other cells and rows, and the pre-existing stale header are preserved.
