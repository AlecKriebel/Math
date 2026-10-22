# KOU-21.42 / 2551: a negative answer from earlier grading results

**Author disposition: prior-literature consequence, one substantive approach (1/5).**
Every three-generated torsion-free nilpotent group of class three is self-similar. Thus the existence question in Kourovka 21.42 has a negative answer, by combining established Lie-algebra grading and self-similarity results. This is not presented as a new theorem or a priority claim.

The load-bearing earlier result is the positive-gradability of three-generated class-three nilpotent Lie algebras, attributed to K. Dekimpe, P. Igodt and H. Pouseele (2003). It is explicitly restated in the full, inspected Dekimpe–Deré paper (arXiv:1407.8106, p.13; published version, p.365). Mathieu's Theorem 3 (arXiv:2101.11291) immediately supplies a stronger self-similarity conclusion. RESULT.md also gives a direct contraction-to-rooted-tree proof, with the classical Malcev correspondence and grading theorem clearly identified as external inputs.

## Important scope limits

- The October 2026 Notebook still lists 21.42 without a solved or unverified-AI marker. This report does not assert an editor decision or an independently located later paper explicitly resolving 21.42.
- The original 2003 article's full text was not obtained. Its full proof has **not** been audited here. The theorem is used as an external literature input, corroborated by its coauthor's later research paper, the publisher's bibliographic record and the institutional abstract.
- No alleged unpublished resolution, private recollection or search-summary claim is used as evidence.
- The universal conclusion is a theorem deduction, not a conclusion from finite tests. The exact 4,455 controls concern an illustrative three-generated lattice and errors to avoid.
- This is AI-assisted, unrefereed work. A fresh independent audit is required before publication; this author package contains no claim that such an audit has happened.

## Files and replay

- RESULT.md: exact source scope, theorem chain, complete direct bridge, explicit group example and negative controls
- SOURCE_VERIFICATION.json: public source metadata, hashes, inspection limits and repository checks
- RESEARCH_LOG.md: one approach and stopping reason
- verify_math.py / CHECK_RESULTS.json: deterministic standard-library exact rational controls
- verify_manifest.py / AUTHOR_MANIFEST.json: strict artifact-integrity controls

From this directory, run:

    python3 verify_math.py
    python3 verify_manifest.py

Only the files in AUTHOR_MANIFEST.json plus the manifest itself are proposed for publication. Scholarly PDFs, source extracts, raw dataset records and private research/coordination inputs are excluded.
