# Problem 30003703: representation-ring filtration counterexample

The authored proof constructs genuine free-group automorphisms showing

* D_n(5) is not equal to A_n(5) for every n>=4;
* D_n(6) is not equal to A_n(6) for every n>=3.

The coefficient ring and representation space are exactly those of the primary OWR statement: the Q-algebra of matrix-entry functions on Hom(F_n,SL(2,C)). The lower central quotients of F_n are integral. The familiar lower-central-series conjecture for IA_n is a different problem.

Read PROOF.md for the complete mathematical argument. The result is an author-checked counterexample with independent review still pending at the time of this packet. No historical priority claim is made.

## Reproduce

Requires Python 3.8 or newer, standard library only. From this folder:

    python3 verify.py
    python3 validate_release.py

The first command recomputes all exact controls. Its JSON should match verification.json. The second checks that match and every manifest hash. There is no network request and no dependency on source PDFs, private records, or files outside this folder.

## Included material

* PROOF.md: complete argument and exact scope
* verify.py and verification.json: universal symbolic identities, free-word expansions, inverse checks, and five negative controls
* SOURCE_VERIFICATION.json: public source metadata, retrieval/inspection coverage, limitations
* RESEARCH_LOG.md and STATUS.json: authored research checkpoints and conclusion
* MANIFEST.json and validate_release.py: byte-level verification

Source PDFs, HTML pages, source extracts, source-page images, raw catalog records, prior-conversation records, and private coordination material are excluded.

The exact unsolvedmath page could not be read (HTTP 403); the identifier/title/source mapping comes from the supplied descriptor catalog. The original OWR conjecture and its definitions were independently read in the public primary PDF, including visual inspection of printed pp. 88-89. This access limitation does not alter which mathematical statement PROOF.md addresses. Raw AI-solution corpora were unavailable and were not inspected.
