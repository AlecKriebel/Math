# Aggregate root-dependent spanning-tree cost: review package
This package contains the four-page self-contained note and portable exact supporting files for Kaibel's Problem1. It proves NP-completeness for the all-root/full-orientation objective with costs in {0,1,2}, and the uniform positive shift gives {1,2,3}. One common undirected tree is used at every root.

The corrected V2 source-preparation snapshot is preserved unchanged in source_preparation/. Its correction ledger records the whole-package R1 input-validation repair, with V1 preserved separately in the repository. Its README, preparation seal and gates record their historical preparation state. They do not certify this assembled PDF/ZIP or replace subsequent whole-package review. The copied historical PROOF.md is a byte-bound B=n+1 preparation artifact with superseded status prose; the current note presents the same mechanism at B=2. Source_preparation/PRIORITY_PROVENANCE.md explains the dated priority audit and inaccessible originals. No earlier covering proof was located by 6 October 2026; absolute first discovery and continued openness are not asserted.

The PDF is root_dependent_spanning_trees.pdf. Its LaTeX source is source_preparation/root_dependent_spanning_trees.tex. Run the standard-library diagnostics with Python 3.10+:

    python3 source_preparation/run_checks.py --include-historical

This runs both normal and optimized Python, twelve mandatory intended failures, including malformed-input suffix controls, and four scratch-copy historical replays; it writes only removed temporary files by default. To retain a new receipt, add --output with an external scratch path. Directly executing copied historical scripts writes in their own folder, so use the runner to preserve this immutable snapshot.

PACKAGE_MANIFEST.json binds the logical authored payload and exact source identity. SHA256SUMS binds the payload files other than itself; the manifest and ZIP have external seal pins. The support ZIP contains this PDF and the entire logical package plus PACKAGE_MANIFEST.json; it excludes itself and contains no third-party PDF, source extract, screenshot, raw web response, credential or native-integration helper.

The identical intended metadata is in intended_zenodo_metadata.json and zenodo-deposit.json. The latter is for the repository's top-level Zenodo kit, selecting the adjacent PDF and support ZIP. The ZIP does not recursively contain itself; reusing its deposit file requires the original support ZIP adjacent to the extracted package. No DOI placeholder is asserted.

Extensive AI assistance in solving, drafting, source checks, code generation, reproduction and adversarial audits is disclosed in the manuscript and metadata. Automated review is not human refereeing; this is an unrefereed preprint without conventional human peer review. Original author effort 2/5 was authenticated from QUEUE/prose, no original structured ledger was supplied, and subsequent audits/package preparation add zero central proof-search turns.

Assembly is preparation for fresh whole-package review. Publication clearance and any later service actions are recorded separately in the repository, not inferred from this dated assembly snapshot. The offered license for authored artifacts is CC BY 4.0, as stated in source_preparation/LICENSE.md.
