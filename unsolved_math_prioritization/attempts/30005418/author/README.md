# Koszulness from the Kähler package

Problem 30005418 / OWR-12697689-014, rank 797.

**Outcome: universal target unresolved after five approach families.** This is a scoped research packet, awaiting a fresh independent audit.

- PROOF.md contains the exact real/graded/primitive/cone conventions, a local-cone lemma, the square-zero obstruction, a socle-degree-at-most-two theorem, and an explicit Koszul family with a full mixed cone.
- A credited quadratic Gorenstein non-Koszul idealization is reconstructed with a genuine hard-Lefschetz element and an exact off-diagonal bar-homology class. It fails HR and is not a counterexample to the target.
- A nonquadratic apolar HR example checks that quadraticity cannot be silently omitted.
- verify_math.py is a standalone Python-standard-library checker; MATH_RESULTS.json is its deterministic output. It uses rational arithmetic, not floating-point signatures or finite-field lifting.
- SOURCES.json and PRIOR_ATTEMPT_CHECK.json contain public verification metadata only. The optional verify_sources.py rehashes separately supplied source inputs; none of those inputs is distributed here.
- RESEARCH_LOG.md records the five families, their results, and exact gaps. AUTHOR_MANIFEST.json binds all safe payload files. verify_packet.py checks the inventory and replays the computation in a temporary directory.

Run:

    python verify_packet.py
    python verify_math.py --output /tmp/kahler-results.json

Optional separately supplied-source verification:

    python verify_sources.py PROBLEMS_JSON REPORTS_JSON CATALOG_JSON PDF_DIRECTORY

The packet contains no source PDFs, extracted source text, page images, raw corpora, third-party source code, or private coordination records. Statements about source inspection describe the author's 5 October 2026 inspection, not any later replay. All prior constructions and standard criteria remain credited. AI tools were used extensively; no novelty, full resolution, formal proof-assistant verification, editorial endorsement, or external human peer review is claimed. No remote writes were performed by this research worker.
