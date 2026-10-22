# Tail generation for symmetric free-product states: a general deduction

Alec Kriebel, Independent researcher. ORCID https://orcid.org/0009-0001-9320-500X . Version 1.0.0, 22 October 2026. Unrefereed preprint. Prose CC BY 4.0; authored code MIT.

For every unital C*-algebra A and every finite-permutation-symmetric state on its countable universal unital free product, in the original GNS representation, the DKW recursively defined tail C*-algebra D satisfies D''=T. The canonical expectation F of the represented free-product algebra is WOT dense in T with represented inputs and outputs bounded by the target norm. No faithful state/representation, separability, trace, factoriality, quantum symmetry or normal extension of F is assumed. This answers DKW 5.3.5 and the separate Question 2 in OWR 28/2015 and 40/2016. Catalog 30003208 and 30002897 are aliases. The separate D subset pi(free product) question is not answered.

The short general deduction uses prior DKW coefficient stabilization and bounded extension, Liu's related bilateral future-expectation method, and Kaplansky density. The 2x2 matrix device is already in Kaplansky's proof, credited there to Halmos. No new coefficient/Kaplansky mechanism, exclusivefirstness or exhaustive historical novelty is claimed. RELATION_TO_PRIOR_WORK.md gives a detailed original bridge explaining why the theorem is a close corollary of the earlier methods, including normal-quotient tail lifting and the important non-descent boundary. SOURCE_PROVENANCE.json pins actual source versions and discloses inaccessible journal/dissertation bodies. Copyrighted third-party bodies and private ledger/account/coordination captures are not included.

The four-page paper is paper.pdf and its complete editable source is main.tex. The main universal proof is written; finite controls cannot establish a theorem for all C*-algebras or certify literature absence.

## Offline verification

Requires Python 3.10+ and its standard library only. From this extracted directory run:

    python3 -B reproduce.py

It checks exact closed membership, source/PDF/metadata identity, and reproduces both checkers in ordinary,-O,-OO modes against complete expected outputs. exact_controls.py is reused with explicit provenance from this project's independently authored control suite:82,376 guards,3,072 permutation cases,1,708 overlaps,3,048 repeated-word cases,4,372 matrix-word cases and 8 false controls rejected. matrix_corner.py is an additional exact nonselfadjoint corner fixture with 2 false controls rejected. The original suite's output flag was renamed third_party_source_code_executed to avoid ambiguity: these project-authored checkers execute, whereas no external theorem-author program executes. No downloaded compiler, network service or source-author script is needed for these checks.

To rebuild the identical scientific ZIP and five-member upload kit, using the frozen reviewed PDF as input:

    python3 -B build_package.py --output ../rebuilt

This performs verification first. It writes only local output files and never contacts a provider. The output directory must lie outside this immutable source folder. ZIP member timestamps/permissions and ordering are fixed. This rebuild does not recompile the PDF; BUILD_RECEIPT.json records its actual TeX source/compiler identity. To recompile an edited TeX source, use an available LaTeX engine, then deliberately update the PDF, receipts, expected inventories and review. Byte-identical TeX recompilation is not claimed.

The prepared metadata is a local proposal, not a published record or DOI reservation. Fresh independent whole-package review, root adoption and separately authorized publication steps remain outstanding. Do not substitute a cited dependency/report DOI for a DOI of this note.

AI tools were extensively involved in research planning, mathematical exploration, proof development/reconstruction, computation, literature/source investigation, writing/editing and adversarial verification. Alec Kriebel is the named human author. The note and support are unrefereed, without conventional independent human peer review, journal acceptance or formal proof-assistant certification; internal AI audits do not supply those certifications.
